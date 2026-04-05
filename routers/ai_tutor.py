"""AI学习助手 - 分科目专业辅导 + 拍题解答"""

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Union, Any, Optional
from database import get_db
import models
import anthropic
import json

from config import anthropic_key, SUBJECTS

router = APIRouter(prefix="/api/ai", tags=["AI助手"])

client = anthropic.Anthropic(api_key=anthropic_key())

SUBJECT_PROMPTS = {
    "数学": "你是一位资深高中数学老师，擅长用清晰的逻辑和步骤讲解数学问题。解题时：1)先分析题目考查的知识点 2)写出完整的解题过程，每一步都要有依据 3)总结解题方法和易错点。对于选择题要分析每个选项。使用LaTeX格式写数学公式。",
    "物理": "你是一位资深高中物理老师。解题时：1)分析物理过程和研究对象 2)画受力分析（用文字描述）3)列出相关公式 4)代入计算 5)检验结果的物理意义。注意单位换算。",
    "化学": "你是一位资深高中化学老师。解题时注意：1)分析反应类型和条件 2)写出完整的化学方程式 3)对于计算题要注意物质的量的关系 4)有机题要画结构简式。",
    "英语": "你是一位资深高中英语老师。对于阅读理解要分析文章结构和出题意图。对于语法题要解释语法规则。对于写作要提供高级词汇和句型替换。用中文解释，关键术语保留英文。",
    "语文": "你是一位资深高中语文老师。对于古诗文要逐字翻译并赏析。对于现代文阅读要分析答题模板。对于作文要从立意、结构、论据等方面给出建议。",
    "生物": "你是一位资深高中生物老师。解释概念时要结合具体例子。对于遗传题要画遗传图解。实验题要分析自变量、因变量和无关变量。",
    "地理": "你是一位资深高中地理老师。自然地理要结合原理分析，画示意图（用文字描述）。人文地理注意答题模板和角度。区域地理要结合地图分析。读图题要系统分析图中信息。",
    "general": "你是一位全科辅导老师，帮助高中生解答各科学习问题。根据题目内容自动判断科目并给出专业解答。",
}

BASE_PROMPT = """你是「栀言书院」的AI学习助手「栀老师」，专门辅导高二学生。回答要求：
- 解答要详细、有条理，用分步骤格式
- 数学公式使用LaTeX（用$...$或$$...$$包裹）
- 如果是选择题，要分析每个选项
- 每道题结束后给出【知识点总结】和【易错提醒】
- 鼓励学生思考，适当引导而不是直接给答案
- 如果学生上传了图片，仔细识别图片中的题目内容

{subject_prompt}"""


class Message(BaseModel):
    role: str
    content: Union[str, List[Any]]


class ChatRequest(BaseModel):
    messages: List[Message]
    subject: str = "general"
    chat_id: Optional[int] = None


def convert_message(m: Message) -> dict:
    if isinstance(m.content, str):
        return {"role": m.role, "content": m.content}
    blocks = []
    for item in m.content:
        if item.get("type") == "image_url":
            url = item["image_url"]["url"]
            if url.startswith("data:"):
                header, data = url.split(",", 1)
                media_type = header.split(";")[0].split(":")[1]
                blocks.append({
                    "type": "image",
                    "source": {"type": "base64", "media_type": media_type, "data": data}
                })
        elif item.get("type") == "text":
            blocks.append({"type": "text", "text": item["text"]})
    return {"role": m.role, "content": blocks}


@router.post("/chat")
def chat(req: ChatRequest, db: Session = Depends(get_db)):
    subject_prompt = SUBJECT_PROMPTS.get(req.subject, SUBJECT_PROMPTS["general"])
    system = BASE_PROMPT.format(subject_prompt=subject_prompt)

    api_messages = [convert_message(m) for m in req.messages]

    def generate():
        try:
            with client.messages.stream(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                system=system,
                messages=api_messages,
            ) as stream:
                full_text = ""
                for event in stream:
                    if event.type == "content_block_delta" and event.delta.type == "text_delta":
                        full_text += event.delta.text
                        yield f"data: {json.dumps({'text': event.delta.text}, ensure_ascii=False)}\n\n"

                final = stream.get_final_message()
                yield f"data: {json.dumps({'done': True, 'input_tokens': final.usage.input_tokens, 'output_tokens': final.usage.output_tokens}, ensure_ascii=False)}\n\n"

            # 保存对话历史
            if req.chat_id:
                chat_record = db.query(models.ChatHistory).filter(models.ChatHistory.id == req.chat_id).first()
                if chat_record:
                    msgs = json.loads(chat_record.messages)
                    msgs.append({"role": "user", "content": req.messages[-1].content if isinstance(req.messages[-1].content, str) else "[图片+文字]"})
                    msgs.append({"role": "assistant", "content": full_text})
                    chat_record.messages = json.dumps(msgs, ensure_ascii=False)
                    db.commit()
            else:
                # 新建对话
                first_msg = req.messages[0].content if isinstance(req.messages[0].content, str) else "图片问题"
                title = first_msg[:50] if len(first_msg) > 0 else "新对话"
                chat_record = models.ChatHistory(
                    subject=req.subject,
                    title=title,
                    messages=json.dumps([
                        {"role": "user", "content": first_msg},
                        {"role": "assistant", "content": full_text},
                    ], ensure_ascii=False),
                )
                db.add(chat_record)
                db.commit()
                db.refresh(chat_record)
                yield f"data: {json.dumps({'chat_id': chat_record.id}, ensure_ascii=False)}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@router.get("/history")
def get_history(subject: str = "", db: Session = Depends(get_db)):
    q = db.query(models.ChatHistory)
    if subject:
        q = q.filter(models.ChatHistory.subject == subject)
    records = q.order_by(models.ChatHistory.updated_at.desc()).limit(50).all()
    return [{
        "id": r.id,
        "subject": r.subject,
        "title": r.title,
        "created_at": str(r.created_at),
        "updated_at": str(r.updated_at),
    } for r in records]


@router.get("/history/{chat_id}")
def get_chat(chat_id: int, db: Session = Depends(get_db)):
    record = db.query(models.ChatHistory).filter(models.ChatHistory.id == chat_id).first()
    if not record:
        raise HTTPException(404, "对话不存在")
    return {
        "id": record.id,
        "subject": record.subject,
        "title": record.title,
        "messages": json.loads(record.messages),
    }


@router.delete("/history/{chat_id}")
def delete_chat(chat_id: int, db: Session = Depends(get_db)):
    record = db.query(models.ChatHistory).filter(models.ChatHistory.id == chat_id).first()
    if record:
        db.delete(record)
        db.commit()
    return {"ok": True}
