from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from database import engine
import models
import os
import requests

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="四面体学习平台", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routers import ai_tutor, notes, wrong_questions, progress, resources
app.include_router(ai_tutor.router)
app.include_router(notes.router)
app.include_router(wrong_questions.router)
app.include_router(progress.router)
app.include_router(resources.router)

BASE_DIR = os.path.dirname(__file__)
FRONTEND = os.path.join(BASE_DIR, "frontend")


def _serve(filename):
    resp = FileResponse(os.path.join(FRONTEND, filename))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return resp


@app.get("/")
def index():
    return _serve("index.html")


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
