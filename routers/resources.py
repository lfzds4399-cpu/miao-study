"""课程资源 + 公式速查"""

from fastapi import APIRouter
from config import SUBJECTS, VIDEO_RESOURCES

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


@router.get("/videos")
def get_videos(subject: str = "", chapter: str = ""):
    """获取视频资源"""
    result = []
    for subj, videos in VIDEO_RESOURCES.items():
        if subject and subj != subject:
            continue
        for v in videos:
            if chapter and v["chapter"] != chapter:
                continue
            result.append({"subject": subj, **v})
    return result


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
