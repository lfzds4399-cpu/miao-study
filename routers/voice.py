"""实时语音对话 - OpenAI Whisper + TTS + Claude AI"""

from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from config import get_key, anthropic_key
import anthropic
import httpx
import json
import io

router = APIRouter(prefix="/api/voice", tags=["语音"])

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
async def text_to_speech(text: str = Form(...), voice: str = Form("shimmer")):
    """文字转语音 - OpenAI TTS"""
    key = openai_key()
    if not key:
        return {"error": "未配置OpenAI API Key"}

    # Clean text for TTS
    clean = text.replace("$", "").replace("\\", "").replace("#", "").replace("*", "").replace("`", "")
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
                "model": "tts-1",
                "input": clean,
                "voice": voice,  # shimmer = warm female voice
                "response_format": "mp3",
                "speed": 1.05,
            },
        )

    if resp.status_code == 200:
        return StreamingResponse(
            io.BytesIO(resp.content),
            media_type="audio/mpeg",
            headers={"Content-Disposition": "inline; filename=speech.mp3"},
        )
    return {"error": f"TTS API错误: {resp.status_code}"}


@router.post("/chat")
async def voice_chat(
    audio: UploadFile = File(...),
    subject: str = Form("general"),
    history: str = Form("[]"),
    image: str = Form(""),  # base64 image from camera (optional)
):
    """语音+视频对话：语音输入 → (可选图片) → AI回复 → 语音输出"""
    key = openai_key()
    if not key:
        return {"error": "未配置OpenAI API Key"}

    # Step 1: Whisper STT
    audio_data = await audio.read()
    async with httpx.AsyncClient(timeout=30) as client:
        stt_resp = await client.post(
            f"{OPENAI_API}/audio/transcriptions",
            headers={"Authorization": f"Bearer {key}"},
            files={"file": ("audio.webm", audio_data, "audio/webm")},
            data={"model": "whisper-1", "language": "zh"},
        )

    if stt_resp.status_code != 200:
        return {"error": "语音识别失败"}

    user_text = stt_resp.json().get("text", "")
    # If camera is on but no speech, still allow image-based Q&A
    if not user_text.strip():
        if image:
            user_text = "请看这道题，帮我解答"
        else:
            return {"error": "没有识别到语音内容"}

    # Step 2: Claude AI response (with optional image)
    subject_prompts = {
        "数学": "你是高中数学老师，用简洁口语化的方式回答。",
        "物理": "你是高中物理老师，用简洁口语化的方式回答。",
        "化学": "你是高中化学老师，用简洁口语化的方式回答。",
        "英语": "你是高中英语老师，用简洁口语化的方式回答。",
        "语文": "你是高中语文老师，用简洁口语化的方式回答。",
        "地理": "你是高中地理老师，用简洁口语化的方式回答。",
        "生物": "你是高中生物老师，用简洁口语化的方式回答。",
    }

    has_img = "学生通过摄像头展示了内容，请仔细识别图中的题目并解答。" if image else ""
    system = f"""你是栀老师，高中辅导AI。{subject_prompts.get(subject, '')}
{has_img}
口语化回答，简短2-4句话，不用公式符号和markdown。"""

    messages = json.loads(history) if history != "[]" else []

    # Build user message with optional image
    if image and image.startswith("data:"):
        header, data = image.split(",", 1)
        media_type = header.split(";")[0].split(":")[1]
        user_content = [
            {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": data}},
            {"type": "text", "text": user_text or "请看这个图片，帮我解答"},
        ]
    else:
        user_content = user_text

    messages.append({"role": "user", "content": user_content})

    client = anthropic.Anthropic(api_key=anthropic_key())
    ai_resp = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        system=system,
        messages=messages,
    )
    ai_text = ai_resp.content[0].text

    # Step 3: OpenAI TTS
    async with httpx.AsyncClient(timeout=60) as http_client:
        tts_resp = await http_client.post(
            f"{OPENAI_API}/audio/speech",
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
            json={
                "model": "tts-1",
                "input": ai_text[:2000],
                "voice": "shimmer",
                "response_format": "mp3",
                "speed": 1.05,
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
