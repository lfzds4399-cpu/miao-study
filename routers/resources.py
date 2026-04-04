"""课程资源 + 公式速查 + B站实时搜索 + 知识点整合"""

from fastapi import APIRouter
import requests
import urllib.parse
from config import SUBJECTS
from data.chapter_notes import CHAPTER_NOTES

router = APIRouter(prefix="/api/resources", tags=["资源库"])


@router.get("/subjects")
def get_subjects():
    """获取全部科目和章节体系"""
    result = []
    for name, info in SUBJECTS.items():
        result.append({
            "name": name,
            "icon": info["icon"],
            "color": info["color"],
            "chapters": info["chapters"],
        })
    return result


@router.get("/chapter-notes")
def get_chapter_notes(subject: str = "", chapter: str = ""):
    """获取章节知识点整合"""
    if subject and chapter:
        key = f"{subject}|{chapter}"
        note = CHAPTER_NOTES.get(key)
        if note:
            return note
        return {"summary": "", "key_points": [], "formulas": [], "exam_tips": [], "difficulty": 0}
    # 返回所有
    result = {}
    for key, val in CHAPTER_NOTES.items():
        result[key] = val
    return result


@router.get("/videos")
def get_videos(subject: str = "", chapter: str = ""):
    """实时从B站搜索教学视频"""
    if not subject or not chapter:
        return []

    keyword = f"高中{subject} {chapter} 精讲"
    try:
        encoded = urllib.parse.quote(keyword)
        resp = requests.get(
            f"https://api.bilibili.com/x/web-interface/search/type",
            params={
                "search_type": "video",
                "keyword": keyword,
                "order": "totalrank",
                "duration": 4,  # 60分钟以上的长视频优先
                "page": 1,
                "pagesize": 6,
            },
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Referer": "https://www.bilibili.com",
            },
            timeout=10,
        )
        if resp.status_code == 200:
            data = resp.json()
            results = data.get("data", {}).get("result", [])
            videos = []
            for v in results[:6]:
                title = v.get("title", "").replace('<em class="keyword">', "").replace("</em>", "")
                bvid = v.get("bvid", "")
                author = v.get("author", "")
                play = v.get("play", 0)
                duration = v.get("duration", "")
                if not bvid:
                    continue
                videos.append({
                    "subject": subject,
                    "chapter": chapter,
                    "title": title,
                    "platform": "bilibili",
                    "url": f"https://www.bilibili.com/video/{bvid}/",
                    "teacher": author,
                    "play": play,
                    "duration": duration,
                    "rating": round(min(5.0, 3.5 + play / 100000), 1),
                })
            return videos
    except Exception as e:
        pass

    # B站API失败时返回搜索链接 + 权威平台链接
    search_url = f"https://search.bilibili.com/all?keyword={urllib.parse.quote(keyword)}&order=totalrank&duration=4"
    return _get_official_resources(subject, chapter) + [{
        "subject": subject,
        "chapter": chapter,
        "title": f"🔍 在B站搜索更多「{keyword}」",
        "platform": "bilibili",
        "url": search_url,
        "teacher": "B站搜索",
        "play": 0,
        "duration": "",
        "rating": 0,
    }]


def _get_official_resources(subject, chapter):
    """多平台教育资源"""
    keyword = urllib.parse.quote(f"高中 {subject} {chapter}")
    keyword_bili = urllib.parse.quote(f"高中{subject} {chapter} 精讲 全套")
    resources = [
        {
            "subject": subject, "chapter": chapter,
            "title": f"📕 国家中小学智慧教育平台 · {subject}{chapter}",
            "platform": "国家平台",
            "url": f"https://basic.smartedu.cn/syncClassroom?keyword={urllib.parse.quote(f'{subject} {chapter}')}",
            "teacher": "教育部官方", "play": 0, "duration": "官方课程", "rating": 5.0,
        },
        {
            "subject": subject, "chapter": chapter,
            "title": f"🎬 B站搜索 · {subject}{chapter}名师精讲",
            "platform": "bilibili",
            "url": f"https://search.bilibili.com/all?keyword={keyword_bili}&order=totalrank&duration=4",
            "teacher": "B站搜索", "play": 0, "duration": "长视频", "rating": 4.9,
        },
        {
            "subject": subject, "chapter": chapter,
            "title": f"📗 学科网 · {subject}{chapter}课件/试卷",
            "platform": "学科网",
            "url": f"https://www.zxxk.com/search?keyword={keyword}",
            "teacher": "学科网", "play": 0, "duration": "课件", "rating": 4.8,
        },
        {
            "subject": subject, "chapter": chapter,
            "title": f"📘 知乎 · {subject}{chapter}学习方法",
            "platform": "知乎",
            "url": f"https://www.zhihu.com/search?type=content&q={urllib.parse.quote(f'高中{subject} {chapter} 怎么学')}",
            "teacher": "知乎", "play": 0, "duration": "经验", "rating": 4.5,
        },
        {
            "subject": subject, "chapter": chapter,
            "title": f"🎓 中国大学MOOC · {subject}相关课程",
            "platform": "MOOC",
            "url": f"https://www.icourse163.org/search.htm?search={urllib.parse.quote(f'高中{subject}')}#/",
            "teacher": "大学MOOC", "play": 0, "duration": "系统课", "rating": 4.7,
        },
        {
            "subject": subject, "chapter": chapter,
            "title": f"📺 西瓜视频 · {subject}{chapter}教学",
            "platform": "西瓜视频",
            "url": f"https://www.ixigua.com/search/{urllib.parse.quote(f'高中{subject} {chapter}')}",
            "teacher": "西瓜视频", "play": 0, "duration": "视频", "rating": 4.3,
        },
    ]
    return resources


# 各科重要公式速查
FORMULAS = {
    "数学": [
        {"chapter": "导数", "formulas": [
            "$(f(x) \\pm g(x))' = f'(x) \\pm g'(x)$",
            "$(f(x) \\cdot g(x))' = f'(x)g(x) + f(x)g'(x)$",
            "$(x^n)' = nx^{n-1}$",
            "$(e^x)' = e^x$, $(\\ln x)' = \\frac{1}{x}$",
            "$(\\sin x)' = \\cos x$, $(\\cos x)' = -\\sin x$",
        ]},
        {"chapter": "圆锥曲线", "formulas": [
            "椭圆: $\\frac{x^2}{a^2} + \\frac{y^2}{b^2} = 1$ $(a>b>0)$, $c^2 = a^2 - b^2$",
            "双曲线: $\\frac{x^2}{a^2} - \\frac{y^2}{b^2} = 1$, $c^2 = a^2 + b^2$",
            "抛物线: $y^2 = 2px$, 焦点 $(\\frac{p}{2}, 0)$",
            "离心率: $e = \\frac{c}{a}$",
            "焦点弦长: $|AB| = x_1 + x_2 + p$ (抛物线)",
        ]},
        {"chapter": "数列", "formulas": [
            "等差数列: $a_n = a_1 + (n-1)d$, $S_n = \\frac{n(a_1+a_n)}{2}$",
            "等比数列: $a_n = a_1 \\cdot q^{n-1}$, $S_n = \\frac{a_1(1-q^n)}{1-q}$",
            "等差中项: $2a_n = a_{n-1} + a_{n+1}$",
            "等比中项: $a_n^2 = a_{n-1} \\cdot a_{n+1}$",
        ]},
    ],
    "物理": [
        {"chapter": "电场", "formulas": [
            "库仑定律: $F = k\\frac{q_1 q_2}{r^2}$, $k = 9×10^9 N·m^2/C^2$",
            "电场强度: $E = \\frac{F}{q}$, 点电荷场 $E = k\\frac{Q}{r^2}$",
            "电势能: $E_p = qU$, 电势差: $U_{AB} = \\frac{W_{AB}}{q}$",
            "匀强电场: $E = \\frac{U}{d}$",
            "电容: $C = \\frac{Q}{U}$, 平行板 $C = \\frac{\\varepsilon S}{4\\pi kd}$",
        ]},
        {"chapter": "恒定电流", "formulas": [
            "欧姆定律: $I = \\frac{U}{R}$",
            "电阻定律: $R = \\rho \\frac{L}{S}$",
            "电功率: $P = UI = I^2R = \\frac{U^2}{R}$",
            "闭合回路: $I = \\frac{\\varepsilon}{R+r}$, $U = \\varepsilon - Ir$",
        ]},
        {"chapter": "磁场", "formulas": [
            "安培力: $F = BIL\\sin\\theta$",
            "洛伦兹力: $f = qvB\\sin\\theta$",
            "圆周运动: $r = \\frac{mv}{qB}$, $T = \\frac{2\\pi m}{qB}$",
        ]},
        {"chapter": "电磁感应", "formulas": [
            "法拉第定律: $\\varepsilon = \\frac{\\Delta\\Phi}{\\Delta t} = BLv$",
            "磁通量: $\\Phi = BS\\cos\\theta$",
            "感应电动势（旋转）: $\\varepsilon = nBS\\omega\\sin\\omega t$",
        ]},
    ],
    "化学": [
        {"chapter": "化学平衡", "formulas": [
            "平衡常数: $K = \\frac{c^p(C) \\cdot c^q(D)}{c^m(A) \\cdot c^n(B)}$",
            "转化率: $\\alpha = \\frac{已转化量}{起始量} × 100\\%$",
            "反应速率: $v = \\frac{\\Delta c}{\\Delta t}$",
        ]},
        {"chapter": "电化学", "formulas": [
            "原电池负极（氧化）: 失电子, 电解池阳极（氧化）: 失电子",
            "法拉第电解定律: $m = \\frac{MIt}{nF}$, $F = 96500 C/mol$",
        ]},
    ],
}


@router.get("/formulas")
def get_formulas(subject: str = ""):
    if subject and subject in FORMULAS:
        return FORMULAS[subject]
    return FORMULAS
