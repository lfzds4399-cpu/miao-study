"""实时语音对话 - OpenAI Whisper + TTS + Claude AI"""

from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from config import get_key, anthropic_key
import anthropic
import httpx
import json
import io

router = APIRouter(prefix="/api/voice", tags=["语音"])

import re

def clean_for_tts(text: str) -> str:
    """把AI回复清理成TTS能正确朗读的纯文本"""
    t = text
    # 去掉markdown格式
    t = re.sub(r'\*\*(.+?)\*\*', r'\1', t)  # **bold**
    t = re.sub(r'\*(.+?)\*', r'\1', t)       # *italic*
    t = re.sub(r'`(.+?)`', r'\1', t)         # `code`
    t = re.sub(r'#{1,6}\s*', '', t)           # ### headers
    t = re.sub(r'[-*]\s+', '', t)             # bullet points

    # LaTeX清理
    t = re.sub(r'\$+', '', t)                 # $ and $$
    t = re.sub(r'\\frac\{(.+?)\}\{(.+?)\}', r'\1分之\2', t)
    t = re.sub(r'\\sqrt\{(.+?)\}', r'根号下\1', t)
    t = re.sub(r'\\sqrt\s*(\w)', r'根号\1', t)
    t = t.replace('\\times', '乘以').replace('\\cdot', '乘')
    t = t.replace('\\div', '除以')
    t = t.replace('\\pm', '正负').replace('\\mp', '负正')
    t = t.replace('\\leq', '小于等于').replace('\\geq', '大于等于')
    t = t.replace('\\lt', '小于').replace('\\gt', '大于')
    t = t.replace('\\neq', '不等于').replace('\\approx', '约等于')
    t = t.replace('\\infty', '无穷大')
    t = t.replace('\\pi', '派').replace('\\theta', '西塔').replace('\\alpha', '阿尔法')
    t = t.replace('\\beta', '贝塔').replace('\\gamma', '伽马').replace('\\delta', '德尔塔')
    t = t.replace('\\omega', '欧米伽').replace('\\lambda', '兰姆达')
    t = t.replace('\\sin', '正弦').replace('\\cos', '余弦').replace('\\tan', '正切')
    t = t.replace('\\log', '对数').replace('\\ln', '自然对数')
    t = t.replace('\\rightarrow', '推出').replace('\\Rightarrow', '推出')
    t = t.replace('\\leftarrow', '').replace('\\Leftrightarrow', '等价于')
    t = re.sub(r'\\[a-zA-Z]+', '', t)        # 其他剩余LaTeX命令

    # 数学符号转口语
    t = re.sub(r'(\w)\^2', r'\1的平方', t)
    t = re.sub(r'(\w)\^3', r'\1的立方', t)
    t = re.sub(r'(\w)\^{(.+?)}', r'\1的\2次方', t)
    t = re.sub(r'(\w)\^(\w)', r'\1的\2次方', t)
    t = re.sub(r'(\w)_(\d)', r'\1\2', t)     # x_1 -> x1
    t = re.sub(r'(\w)_\{(.+?)\}', r'\1\2', t)
    t = t.replace('>=', '大于等于').replace('<=', '小于等于')
    t = t.replace('!=', '不等于').replace('==', '等于')
    t = t.replace('≥', '大于等于').replace('≤', '小于等于').replace('≠', '不等于')
    t = t.replace('≈', '约等于').replace('±', '正负')
    t = t.replace('→', '推出').replace('√', '根号')
    t = t.replace('²', '的平方').replace('³', '的立方')
    t = t.replace('°', '度')

    # 清理剩余特殊字符
    t = re.sub(r'[{}\[\]\\|~^]', '', t)
    t = re.sub(r'\s+', ' ', t).strip()

    return t

OPENAI_API = "https://api.openai.com/v1"


def openai_key():
    return get_key("OPENAI_API_KEY")


@router.post("/stt")
async def speech_to_text(audio: UploadFile = File(...)):
    """语音转文字 - OpenAI Whisper"""
    key = openai_key()
    if not key:
        return {"error": "未配置OpenAI API Key"}

    audio_data = await audio.read()

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{OPENAI_API}/audio/transcriptions",
            headers={"Authorization": f"Bearer {key}"},
            files={"file": (audio.filename or "audio.webm", audio_data, audio.content_type or "audio/webm")},
            data={"model": "whisper-1", "language": "zh"},
        )

    if resp.status_code == 200:
        result = resp.json()
        return {"text": result.get("text", "")}
    return {"error": f"Whisper API错误: {resp.status_code}", "detail": resp.text}


@router.post("/tts")
async def text_to_speech(text: str = Form(...), voice: str = Form("nova")):
    """文字转语音 - OpenAI TTS"""
    key = openai_key()
    if not key:
        return {"error": "未配置OpenAI API Key"}

    # Clean text for TTS
    clean = clean_for_tts(text)
    if len(clean) > 2000:
        clean = clean[:2000]

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            f"{OPENAI_API}/audio/speech",
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "tts-1-hd",
                "input": clean,
                "voice": voice,
                "response_format": "mp3",
                "speed": 1.0,
            },
        )

    if resp.status_code == 200:
        return StreamingResponse(
            io.BytesIO(resp.content),
            media_type="audio/mpeg",
            headers={"Content-Disposition": "inline; filename=speech.mp3"},
        )
    return {"error": f"TTS API错误: {resp.status_code}"}


TUTOR_SYSTEM = """你是栀老师，一位温柔耐心的高中辅导老师，正在和学生进行真实的语音对话。你是24小时在线的，学生随时可以找你。

## 对话风格
- 用自然、口语化的短句，像真人老师聊天
- 每次回复控制在1-4句话，简短有力
- 可以用语气词："嗯"、"对"、"这样啊"
- 不要说"作为AI"、"我来帮你解答"这类话

## 核心原则：判断问题类型，选择回答方式

你必须先快速判断学生的问题属于哪种类型，然后用对应方式回答：

### A类·事实性问题 → 直接回答，不要绕弯
学生问的是有明确答案的知识点，比如"水的化学式是什么"、"牛顿第二定律的公式"、"be动词有哪些"、"中国最长的河流"。
→ 直接告诉答案，一两句话搞定。不要反问、不要引导、不要问"你觉得呢"。

### B类·概念理解问题 → 简洁解释+确认
学生问"为什么"、"怎么理解"、"区别是什么"，比如"为什么天空是蓝色的"、"动能和势能有什么区别"。
→ 用最通俗的话解释清楚，然后简单确认："这样说能理解吗？"。不要拆成十步。

### C类·解题过程问题 → 适度引导
学生拿着一道具体的题不会做，或者做错了想知道怎么做。
→ 先问一句卡在哪里，然后给关键提示。如果学生明确说"直接告诉我答案"或"帮我做这道题"，就直接给解题过程，不要坚持引导。

### D类·聊天/倾诉 → 陪伴
学生聊学习压力、心情、或者闲聊。
→ 做一个温暖的倾听者，给予鼓励和支持。

## 关键规则
- 简单问题简单答，不要把3秒能说清的事变成30秒的引导
- 学生说"直接告诉我"、"答案是什么"、"别绕了"→ 立刻给答案
- 学生连续问了同一个问题 → 说明你之前的引导没帮到他，直接给答案
- 只有学生主动说"我想自己想想"或者题目确实需要思考过程时才引导
- 永远不要在学生没问的时候主动追问"你还有什么不懂的吗"

## 语音输出规范（非常重要！）
你的回答会被直接朗读出来，所以：
- 绝对不用任何数学符号：说"x的平方"不写"x²"，说"x分之一"不写"1/x"，说"根号x"不写"√x"
- 不用LaTeX、markdown、括号注释、星号、井号
- 不用"首先其次最后"模板"""

SUBJECT_HINTS = {
    "数学": "你擅长数学，解题时注重引导学生画图、列式、找规律。",
    "物理": "你擅长物理，解题时注重引导学生画受力分析图、找物理过程。",
    "化学": "你擅长化学，注重引导学生从微观粒子角度理解反应本质。",
    "英语": "你擅长英语，注重语感培养，鼓励学生用英语思考。",
    "语文": "你擅长语文，注重引导学生体会文本情感和作者意图。",
    "地理": "你擅长地理，注重引导学生结合地图和实际案例理解。",
    "生物": "你擅长生物，注重引导学生理解生命活动的逻辑链条。",
}


@router.post("/chat")
async def voice_chat(
    audio: UploadFile = File(...),
    subject: str = Form("general"),
    history: str = Form("[]"),
    image: str = Form(""),
):
    """语音对话：语音输入 → AI回复 → 语音输出"""
    key = openai_key()
    if not key:
        return {"error": "未配置OpenAI API Key"}

    # Step 1: Whisper STT
    audio_data = await audio.read()
    # 根据上传文件的类型确定扩展名（Whisper对此敏感）
    ct = audio.content_type or ""
    fname = audio.filename or "audio.webm"
    if "mp4" in ct or "mp4" in fname:
        upload_name, upload_ct = "audio.mp4", "audio/mp4"
    elif "ogg" in ct:
        upload_name, upload_ct = "audio.ogg", "audio/ogg"
    elif "wav" in ct:
        upload_name, upload_ct = "audio.wav", "audio/wav"
    else:
        upload_name, upload_ct = "audio.webm", "audio/webm"

    async with httpx.AsyncClient(timeout=30) as client:
        stt_resp = await client.post(
            f"{OPENAI_API}/audio/transcriptions",
            headers={"Authorization": f"Bearer {key}"},
            files={"file": (upload_name, audio_data, upload_ct)},
            data={"model": "whisper-1", "language": "zh"},
        )

    if stt_resp.status_code != 200:
        detail = stt_resp.text[:200] if stt_resp.text else "未知错误"
        return {"error": f"语音识别失败({stt_resp.status_code}): {detail}"}

    user_text = stt_resp.json().get("text", "")
    if not user_text.strip():
        if image:
            user_text = "请看这道题，帮我解答"
        else:
            return {"error": "没有识别到语音内容"}

    # Step 2: Build system prompt
    subject_hint = SUBJECT_HINTS.get(subject, "")
    has_img = "\n学生正在通过摄像头给你看题目或内容，请仔细看图并结合语音一起理解。" if image else ""
    system = f"{TUTOR_SYSTEM}\n{subject_hint}{has_img}"

    messages = json.loads(history) if history != "[]" else []

    # Build user message with optional image
    if image and image.startswith("data:"):
        header, data = image.split(",", 1)
        media_type = header.split(";")[0].split(":")[1]
        user_content = [
            {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": data}},
            {"type": "text", "text": user_text},
        ]
    else:
        user_content = user_text

    messages.append({"role": "user", "content": user_content})

    # Keep last 20 messages to stay within context limits
    if len(messages) > 20:
        messages = messages[-20:]

    ai_client = anthropic.Anthropic(api_key=anthropic_key())
    ai_resp = ai_client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=400,
        system=system,
        messages=messages,
    )
    ai_text = ai_resp.content[0].text

    # Step 3: OpenAI TTS
    clean_tts = clean_for_tts(ai_text)
    async with httpx.AsyncClient(timeout=60) as http_client:
        tts_resp = await http_client.post(
            f"{OPENAI_API}/audio/speech",
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "tts-1-hd",
                "input": clean_tts[:2000],
                "voice": "nova",
                "response_format": "mp3",
                "speed": 1.0,
            },
        )

    import base64 as b64mod
    audio_b64 = ""
    if tts_resp.status_code == 200:
        audio_b64 = b64mod.b64encode(tts_resp.content).decode()

    return {
        "user_text": user_text,
        "ai_text": ai_text,
        "audio": audio_b64,
        "has_image": bool(image),
    }
