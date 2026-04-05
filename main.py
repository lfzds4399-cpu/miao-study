from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from database import engine
import models
import os
import requests

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="栀言书院", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routers import ai_tutor, notes, wrong_questions, progress, resources, messages, voice
app.include_router(ai_tutor.router)
app.include_router(notes.router)
app.include_router(wrong_questions.router)
app.include_router(progress.router)
app.include_router(resources.router)
app.include_router(messages.router)
app.include_router(voice.router)

BASE_DIR = os.path.dirname(__file__)
FRONTEND = os.path.join(BASE_DIR, "frontend")


def _serve(filename):
    resp = FileResponse(os.path.join(FRONTEND, filename))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return resp


app.mount("/static", StaticFiles(directory=FRONTEND), name="static")


@app.get("/")
def index():
    return _serve("index.html")


@app.get("/api/daily")
def daily_inspiration():
    """每日金句+猫咪"""
    import random, hashlib
    from datetime import date
    quotes = [
        "努力不一定成功，但放弃一定失败。",
        "今天的汗水，是明天的勋章。",
        "你现在的努力，是未来的你最感谢的事。",
        "不怕慢，只怕站。每天进步一点点。",
        "星光不负赶路人，时光不负有心人。",
        "把优秀变成习惯，把努力变成日常。",
        "高考不是终点，是你人生的起跑线。",
        "你比你想象的更强大。",
        "再长的路，一步步也能走完。",
        "此刻打盹，你将做梦；此刻学习，你将圆梦。",
        "没有人能随随便便成功，所有的光鲜都有代价。",
        "当你觉得累了，说明你在走上坡路。",
        "每一次认真做题，都是在为高考攒分。",
        "你的对手在看书，你的闺蜜在刷题，你还有什么理由不努力？",
        "别让未来的你，讨厌现在的自己。",
        "做一个温暖的人，用知识改变命运。",
        "不是因为看到了希望才坚持，而是坚持了才看到希望。",
        "每个不曾起舞的日子，都是对生命的辜负。",
        "你的潜力远超你的想象，加油！",
        "聪明出于勤奋，天才在于积累。",
        "越努力越幸运，你值得最好的未来。",
        "今天多一份努力，明天多一个选择。",
        "书山有路勤为径，学海无涯苦作舟。",
        "所有的努力都不会白费，时间会给你答案。",
        "你现在偷的每一个懒，都是给未来挖的坑。",
        "梦想不会逃跑，逃跑的永远是自己。",
        "熬过最苦的日子，做最酷的自己。",
        "把每一天都当作最后的冲刺。",
        "没有等出来的辉煌，只有拼出来的美丽。",
        "愿你合上笔盖的那一刻，有武士收刀入鞘般的骄傲。",
    ]
    today = date.today().isoformat()
    idx = int(hashlib.md5(today.encode()).hexdigest(), 16) % len(quotes)
    # 猫咪图片（使用免费API）
    cat_url = f"https://cataas.com/cat?t={today}"
    return {
        "quote": quotes[idx],
        "cat_image": cat_url,
        "date": today,
    }


# ── 天气API（衡阳市） ──
@app.get("/api/weather")
def get_weather():
    """获取衡阳市实时天气 - 使用wttr.in免费API"""
    try:
        resp = requests.get(
            "https://wttr.in/Hengyang,China?format=j1",
            timeout=10,
            headers={"Accept-Language": "zh-CN"},
        )
        if resp.status_code == 200:
            data = resp.json()
            current = data.get("current_condition", [{}])[0]
            weather_desc_cn = {
                "Sunny": "晴", "Clear": "晴", "Partly cloudy": "多云",
                "Cloudy": "阴", "Overcast": "阴", "Mist": "雾",
                "Light rain": "小雨", "Moderate rain": "中雨",
                "Heavy rain": "大雨", "Rain": "雨",
                "Light drizzle": "毛毛雨", "Thunderstorm": "雷暴",
                "Snow": "雪", "Light snow": "小雪",
            }
            desc_en = current.get("weatherDesc", [{}])[0].get("value", "")
            desc_cn = weather_desc_cn.get(desc_en, desc_en)

            # 判断是否需要带伞
            rain_keywords = ["rain", "drizzle", "thunder", "shower", "storm"]
            need_umbrella = any(k in desc_en.lower() for k in rain_keywords)

            # 判断是否需要注意保暖
            temp = int(current.get("temp_C", "20"))
            feels_like = int(current.get("FeelsLikeC", str(temp)))
            need_warm = feels_like < 15

            # 未来天气
            forecast = []
            for day in data.get("weather", [])[:3]:
                day_desc = day.get("hourly", [{}])[4].get("weatherDesc", [{}])[0].get("value", "")
                forecast.append({
                    "date": day.get("date"),
                    "max_temp": day.get("maxtempC"),
                    "min_temp": day.get("mintempC"),
                    "desc": weather_desc_cn.get(day_desc, day_desc),
                    "rain_chance": any(k in day_desc.lower() for k in rain_keywords),
                })

            tips = []
            if need_umbrella:
                tips.append("🌂 今天有雨，记得带伞！")
            if need_warm:
                tips.append(f"🧥 体感温度{feels_like}°C，注意保暖别着凉！")
            if temp > 35:
                tips.append("☀️ 高温天气，注意防暑多喝水！")

            return {
                "city": "衡阳市",
                "temp": temp,
                "feels_like": feels_like,
                "humidity": current.get("humidity", ""),
                "wind_speed": current.get("windspeedKmph", ""),
                "desc": desc_cn,
                "desc_en": desc_en,
                "need_umbrella": need_umbrella,
                "need_warm": need_warm,
                "tips": tips,
                "forecast": forecast,
            }
        return {"error": "天气服务暂时不可用"}
    except Exception as e:
        return {"error": str(e)}


# ── 校园信息 ──
@app.get("/api/school")
def school_info():
    return {
        "name": "衡阳市第一中学",
        "motto": "崇德、笃学、健体、尚美",
        "address": "湖南省衡阳市蒸湘区",
        "established": 1884,
        "type": "湖南省重点中学",
        "schedule": {
            "morning_read": "07:00 - 07:30",
            "period_1": "07:40 - 08:25",
            "period_2": "08:35 - 09:20",
            "break_exercise": "09:20 - 10:00",
            "period_3": "10:00 - 10:45",
            "period_4": "10:55 - 11:40",
            "lunch": "11:40 - 14:00",
            "period_5": "14:00 - 14:45",
            "period_6": "14:55 - 15:40",
            "period_7": "15:50 - 16:35",
            "self_study_eve": "19:00 - 21:30",
        },
        "reminders": [
            "距离2027年高考还在倒计时中",
            "高二下学期是打基础的关键期",
        ],
    }
