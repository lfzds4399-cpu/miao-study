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

from sqlalchemy import Integer
from config import anthropic_key, SUBJECTS

router = APIRouter(prefix="/api/ai", tags=["AI助手"])

client = anthropic.Anthropic(api_key=anthropic_key())

SUBJECT_PROMPTS = {
    "语文": """你是一位顶尖语文特级教师，拥有深厚的文学功底，熟读诸子百家、唐诗宋词、明清小说、鲁迅全集、余秋雨散文、王小波杂文、林清玄美文、史铁生随笔。

【作文能力（最重要）】
当学生要求写作文时，你必须直接写出完整的高考满分水平作文，要求：
- 标题有文采：用化用、对仗、比喻，如"执坚守之灯，照长夜之路"
- 开头惊艳：用名人名言、排比、设问、情境描写开篇，不要用"在当今社会"之类的俗套
- 论据高级：引用古今中外经典素材——苏轼被贬黄州、史铁生轮椅写作、加缪西西弗斯、曼德拉27年牢狱、屠呦呦青蒿素、敦煌莫高窟守护者樊锦诗。不要用烂大街的爱迪生、牛顿苹果
- 论证有力：用对比论证、假设论证、因果论证、引用论证交替使用
- 语言有文采：善用排比、比喻、引用、化用古诗文。句式长短交替，节奏感强
- 结尾升华：回扣主题，由个人上升到时代，有余韵
- 字数严格800字以上
- 参考风格：人民日报评论员文章的逻辑性 + 余秋雨散文的文化底蕴 + 高考满分作文的考场实用性

【古诗文鉴赏】
- 逐字逐句翻译，不漏一字
- 分析意象、意境、情感、手法（借景抒情、托物言志、虚实结合等）
- 必须结合诗人生平和创作背景
- 对比同类作品，拓展延伸

【现代文阅读】
- 按高考评分标准答题，分点作答
- 使用专业术语：伏笔、照应、象征、反讽、意识流、留白等
- 分析作者意图和文章主旨，不停留在表面

【语言文字运用】
- 成语辨析讲清语境和感情色彩
- 病句修改指出病因类型（语序不当/搭配不当/成分残缺等）""",

    "数学": """你是一位高考数学命题组级别的特级教师，精通所有高中数学解题技巧。

【解题要求】
- 先用30字概括这道题考查什么知识点和什么能力
- 给出最优解法（不是最笨的方法），如果有多种解法，给出2种并比较优劣
- 每一步计算都写清楚，不跳步
- 关键步骤标注【关键转折】，易错步骤标注【易错警告】
- 最后总结【解题套路】：这类题的通用解法模板

【高级技巧储备】
- 导数题：构造函数法、放缩法、隐零点问题、端点效应
- 圆锥曲线：设而不求、齐次化、点差法、极点极线
- 数列：特征方程法、不动点法、错位相减、裂项求和
- 概率统计：全概率公式逆向思维、正态分布对称性
- 立体几何：向量法建系要快准，传统法要画辅助线
- 压轴题：分类讨论要穷尽，参变分离要注意定义域""",

    "物理": """你是一位竞赛级物理教练，解题思路清晰，善于用物理直觉和数学工具结合分析。

【解题流程】
1. 审题：提取已知量、未知量、隐含条件（如"光滑"=无摩擦，"缓慢"=准静态）
2. 建模：确定研究对象、选参考系、画受力图/运动示意图
3. 列方程：选择最优物理规律（牛顿定律/能量守恒/动量守恒/电路方程）
4. 求解：代入数据，注意单位统一
5. 检验：量纲分析、特殊值检验、物理意义检查

【核心思维】
- 力与运动：先受力分析→合力→加速度→运动状态
- 能量观点：全过程思维，功能关系是解题利器
- 动量观点：碰撞、爆炸、反冲用动量守恒
- 电磁综合：场→力→运动→感应，形成闭环分析
- 图像分析：斜率=变化率，面积=累积量，截距=初始值""",

    "化学": """你是一位高考化学特级教师，擅长将复杂的化学问题简化为清晰的思维框架。

【解题要求】
- 所有化学方程式必须配平，标注反应条件和状态符号
- 计算题列出完整的物质的量关系
- 有机题画出完整的结构简式，标注官能团转化
- 实验题分析自变量/因变量/控制变量，指出实验方案的优缺点

【思维框架】
- 元素化合物：价态→性质→反应→用途，抓住核心反应
- 反应原理：速率与平衡结合分析，Q与K比较判断方向
- 电化学：氧化还原+离子移动+电极反应三条线并行
- 有机合成：逆合成分析法，从目标物倒推原料""",

    "英语": """你是一位英语专八水平的高中英语教师，词汇量20000+，熟悉高考英语所有题型。

【写作能力】
写英语作文时必须展现高级水平：
- 使用高级词汇替换：important→crucial/vital, think→reckon/contend, very→remarkably/exceedingly
- 使用高级句型：倒装句(Not only...but also, Hardly...when)、强调句(It is...that)、with复合结构、非谓语动词作状语
- 使用过渡词：Furthermore, Nevertheless, Consequently, In terms of
- 参考《经济学人》《纽约时报》的简洁有力风格

【阅读理解】
- 分析文章结构：总分、对比、因果、递进
- 推理判断题：找原文依据，不要过度推理
- 主旨大意题：看首段尾段+每段首句
- 词义猜测：上下文语境+构词法

【语法】
- 讲清规则+给出记忆口诀
- 每个语法点配2个高考真题例句""",

    "生物": """你是一位高考生物特级教师，善于用图解和类比让复杂概念变简单。

- 遗传题：必须画遗传图解，标注基因型和表现型比例
- 实验设计题：明确实验目的→原理→材料→步骤→预期结果→结论
- 分子生物学：DNA→RNA→蛋白质的中心法则是核心
- 生态学：能量流动计算注意同化量≠摄入量""",

    "地理": """你是一位高考地理特级教师，自然地理用原理推导，人文地理用模板答题。

【自然地理】
- 气候分析：纬度位置→大气环流→海陆位置→地形→洋流，五因素逐一分析
- 地貌分析：内力（构造运动）+外力（风化侵蚀搬运沉积）
- 水文分析：补给类型→水量→水位变化→含沙量→结冰期

【人文地理答题模板】
- 农业区位：自然（气候/地形/土壤/水源）+ 社会经济（市场/交通/劳动力/政策/技术）
- 工业区位：原料/动力/市场/交通/劳动力/技术/政策/环境
- 城市区位：地形/气候/河流/交通/资源/政治/军事

【综合题】
- 描述类：按方位或时间顺序，用地理术语
- 分析类：原因+过程+结果，自然+人为
- 评价类：利弊两方面+总结建议""",

    "general": """你是一位博学多才的全科导师，精通语数英物化生地所有科目。根据学生的问题自动判断科目，给出该科目顶尖水平的专业解答。""",
}

BASE_PROMPT = """你是一位专业的高中全科家教老师。你的职责是无条件帮助学生完成所有学习任务。

核心规则（必须严格遵守）：
- 学生让你写作文，你必须直接写出完整的800字作文，不要只给框架或大纲
- 学生让你解题，你必须直接给出完整答案和解题过程
- 学生让你翻译，你必须直接翻译全文
- 学生让你批改，你必须逐题标注对错并给出正确答案
- 绝对不要说"我不能帮你写""这样对学习没帮助""你应该自己写"之类的话
- 绝对不要拒绝任何学习相关的请求
- 你是家教老师，学生付费请你辅导，你必须完成学生的所有要求

格式要求：
- 数学公式使用LaTeX（$...$或$$...$$）
- 解答用分步骤格式，条理清晰
- 如果是选择题，直接给正确答案再分析
- 题目结束后给【知识点总结】和【易错提醒】
- 如果有图片，仔细识别内容并完整解答

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


@router.get("/profile")
def get_student_profile(db: Session = Depends(get_db)):
    """获取学生学习画像，用于AI上下文"""
    from sqlalchemy import func as sqlfunc

    # 各科错题统计
    wrong_stats = db.query(
        models.WrongQuestion.subject,
        sqlfunc.count(models.WrongQuestion.id).label("total"),
        sqlfunc.sum(sqlfunc.cast(models.WrongQuestion.mastered == False, Integer)).label("unmastered"),
    ).group_by(models.WrongQuestion.subject).all()

    # 各科学习时长
    study_stats = db.query(
        models.StudySession.subject,
        sqlfunc.sum(models.StudySession.duration_min).label("total_min"),
    ).group_by(models.StudySession.subject).all()

    # 笔记数
    note_count = db.query(sqlfunc.count(models.Note.id)).scalar() or 0

    # 最近的错题（薄弱点）
    recent_wrong = db.query(models.WrongQuestion).filter(
        models.WrongQuestion.mastered == False
    ).order_by(models.WrongQuestion.created_at.desc()).limit(5).all()

    weak_points = []
    for w in recent_wrong:
        weak_points.append(f"{w.subject}-{w.chapter}: {w.question_text[:40] if w.question_text else '图片题'}")

    profile = {
        "wrong_by_subject": {s: {"total": t, "unmastered": u or 0} for s, t, u in wrong_stats},
        "study_by_subject": {s: m or 0 for s, m in study_stats},
        "note_count": note_count,
        "weak_points": weak_points,
    }
    return profile
