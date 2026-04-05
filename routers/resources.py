"""课程资源 + 公式速查 + 知识点整合"""

from fastapi import APIRouter
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
    """返回指定UP主的B站教学视频"""
    if not subject or not chapter:
        return []

    from config import VIDEO_RESOURCES
    videos = []
    for v in VIDEO_RESOURCES.get(subject, []):
        if v.get("chapter") and (v["chapter"] in chapter or chapter in v.get("chapter", "")):
            videos.append({
                "subject": subject, "chapter": chapter,
                "title": v["title"], "platform": "bilibili",
                "url": v["url"], "teacher": v.get("teacher", "名师"),
                "play": 0, "duration": "精讲", "rating": v.get("rating", 4.5),
            })
    return videos


# 各科重要公式速查
FORMULAS = {
    "数学": [
        {"chapter": "导数", "formulas": [
            "$(f(x) \\pm g(x))' = f'(x) \\pm g'(x)$",
            "$(f(x) \\cdot g(x))' = f'(x)g(x) + f(x)g'(x)$",
            "$\\left(\\frac{f(x)}{g(x)}\\right)' = \\frac{f'(x)g(x) - f(x)g'(x)}{g^2(x)}$",
            "$(x^n)' = nx^{n-1}$",
            "$(e^x)' = e^x$, $(a^x)' = a^x \\ln a$",
            "$(\\ln x)' = \\frac{1}{x}$, $(\\log_a x)' = \\frac{1}{x\\ln a}$",
            "$(\\sin x)' = \\cos x$, $(\\cos x)' = -\\sin x$",
            "$(\\tan x)' = \\frac{1}{\\cos^2 x} = \\sec^2 x$",
            "链式法则: $[f(g(x))]' = f'(g(x)) \\cdot g'(x)$",
        ]},
        {"chapter": "三角函数", "formulas": [
            "同角基本关系: $\\sin^2\\alpha + \\cos^2\\alpha = 1$, $\\tan\\alpha = \\frac{\\sin\\alpha}{\\cos\\alpha}$",
            "二倍角: $\\sin 2\\alpha = 2\\sin\\alpha\\cos\\alpha$",
            "$\\cos 2\\alpha = \\cos^2\\alpha - \\sin^2\\alpha = 2\\cos^2\\alpha - 1 = 1 - 2\\sin^2\\alpha$",
            "辅助角: $a\\sin x + b\\cos x = \\sqrt{a^2+b^2}\\sin(x+\\varphi)$, $\\tan\\varphi = \\frac{b}{a}$",
            "和差角: $\\sin(\\alpha \\pm \\beta) = \\sin\\alpha\\cos\\beta \\pm \\cos\\alpha\\sin\\beta$",
            "$\\cos(\\alpha \\pm \\beta) = \\cos\\alpha\\cos\\beta \\mp \\sin\\alpha\\sin\\beta$",
            "正弦定理: $\\frac{a}{\\sin A} = \\frac{b}{\\sin B} = \\frac{c}{\\sin C} = 2R$",
            "余弦定理: $a^2 = b^2 + c^2 - 2bc\\cos A$",
            "三角形面积: $S = \\frac{1}{2}ab\\sin C = \\frac{1}{2}|\\vec{a} \\times \\vec{b}|$",
            "降幂公式: $\\cos^2\\alpha = \\frac{1+\\cos 2\\alpha}{2}$, $\\sin^2\\alpha = \\frac{1-\\cos 2\\alpha}{2}$",
        ]},
        {"chapter": "圆锥曲线", "formulas": [
            "椭圆: $\\frac{x^2}{a^2} + \\frac{y^2}{b^2} = 1$ $(a>b>0)$, $c^2 = a^2 - b^2$",
            "双曲线: $\\frac{x^2}{a^2} - \\frac{y^2}{b^2} = 1$, $c^2 = a^2 + b^2$, 渐近线 $y = \\pm\\frac{b}{a}x$",
            "抛物线: $y^2 = 2px$, 焦点 $(\\frac{p}{2}, 0)$, 准线 $x = -\\frac{p}{2}$",
            "离心率: $e = \\frac{c}{a}$（椭圆 $0<e<1$, 双曲线 $e>1$）",
            "焦点弦长: $|AB| = x_1 + x_2 + p$ (抛物线)",
            "椭圆焦点三角形面积: $S = b^2\\tan\\frac{\\theta}{2}$（$\\theta$为 $\\angle F_1PF_2$）",
            "焦半径: 椭圆 $|PF_1| = a + ex_0$, $|PF_2| = a - ex_0$",
        ]},
        {"chapter": "数列", "formulas": [
            "等差数列: $a_n = a_1 + (n-1)d$, $S_n = \\frac{n(a_1+a_n)}{2} = na_1 + \\frac{n(n-1)}{2}d$",
            "等比数列: $a_n = a_1 \\cdot q^{n-1}$, $S_n = \\frac{a_1(1-q^n)}{1-q}$（$q \\neq 1$）",
            "等差中项: $2a_n = a_{n-1} + a_{n+1}$",
            "等比中项: $a_n^2 = a_{n-1} \\cdot a_{n+1}$",
            "$a_n$ 与 $S_n$ 的关系: $a_n = S_n - S_{n-1}$（$n \\geq 2$）, $a_1 = S_1$",
            "裂项求和: $\\frac{1}{n(n+1)} = \\frac{1}{n} - \\frac{1}{n+1}$",
            "等差数列性质: $S_n, S_{2n}-S_n, S_{3n}-S_{2n}$ 也成等差",
        ]},
        {"chapter": "概率与统计", "formulas": [
            "离散型随机变量期望: $E(X) = \\sum_{i} x_i p_i$, $E(aX+b) = aE(X)+b$",
            "离散型随机变量方差: $D(X) = E(X^2) - [E(X)]^2$, $D(aX+b) = a^2 D(X)$",
            "二项分布: $P(X=k) = C_n^k p^k (1-p)^{n-k}$, $E(X)=np$, $D(X)=np(1-p)$",
            "超几何分布: $P(X=k) = \\frac{C_M^k C_{N-M}^{n-k}}{C_N^n}$",
            "正态分布: $f(x) = \\frac{1}{\\sigma\\sqrt{2\\pi}} e^{-\\frac{(x-\\mu)^2}{2\\sigma^2}}$",
            "回归方程: $\\hat{y} = \\hat{b}x + \\hat{a}$, $\\hat{b} = \\frac{\\sum(x_i-\\bar{x})(y_i-\\bar{y})}{\\sum(x_i-\\bar{x})^2}$, $\\hat{a} = \\bar{y} - \\hat{b}\\bar{x}$",
            "相关系数: $r = \\frac{\\sum(x_i-\\bar{x})(y_i-\\bar{y})}{\\sqrt{\\sum(x_i-\\bar{x})^2 \\cdot \\sum(y_i-\\bar{y})^2}}$, $|r|$ 越接近1相关性越强",
            "独立性检验: $K^2 = \\frac{n(ad-bc)^2}{(a+b)(c+d)(a+c)(b+d)}$",
            "组合数: $C_n^k = \\frac{n!}{k!(n-k)!}$, $C_n^k = C_n^{n-k}$",
        ]},
        {"chapter": "空间向量与立体几何", "formulas": [
            "空间向量点积: $\\vec{a} \\cdot \\vec{b} = x_1x_2 + y_1y_2 + z_1z_2 = |\\vec{a}||\\vec{b}|\\cos\\theta$",
            "向量模: $|\\vec{a}| = \\sqrt{x^2 + y^2 + z^2}$",
            "两向量夹角: $\\cos\\theta = \\frac{\\vec{a} \\cdot \\vec{b}}{|\\vec{a}||\\vec{b}|}$",
            "二面角余弦: $\\cos\\theta = \\frac{\\vec{n_1} \\cdot \\vec{n_2}}{|\\vec{n_1}||\\vec{n_2}|}$（法向量法）",
            "点到平面距离: $d = \\frac{|\\vec{AP} \\cdot \\vec{n}|}{|\\vec{n}|}$（法向量法）",
            "线面角正弦: $\\sin\\theta = \\frac{|\\vec{a} \\cdot \\vec{n}|}{|\\vec{a}||\\vec{n}|}$（直线方向向量与平面法向量）",
            "两平面平行: $\\vec{n_1} \\times \\vec{n_2} = \\vec{0}$（法向量平行）",
            "线面垂直: 直线方向向量与平面法向量平行",
        ]},
        {"chapter": "函数与不等式", "formulas": [
            "二次函数: $f(x) = ax^2 + bx + c$, 顶点 $\\left(-\\frac{b}{2a}, \\frac{4ac-b^2}{4a}\\right)$",
            "韦达定理: $x_1 + x_2 = -\\frac{b}{a}$, $x_1 \\cdot x_2 = \\frac{c}{a}$",
            "指数与对数互换: $a^b = N \\Leftrightarrow b = \\log_a N$",
            "换底公式: $\\log_a b = \\frac{\\ln b}{\\ln a} = \\frac{\\lg b}{\\lg a}$",
            "均值不等式: $\\frac{a+b}{2} \\geq \\sqrt{ab}$（$a,b>0$，等号条件 $a=b$）",
            "柯西不等式: $(a^2+b^2)(c^2+d^2) \\geq (ac+bd)^2$",
            "绝对值不等式: $|a| - |b| \\leq |a \\pm b| \\leq |a| + |b|$",
        ]},
    ],
    "物理": [
        {"chapter": "电场", "formulas": [
            "库仑定律: $F = k\\frac{q_1 q_2}{r^2}$, $k = 9×10^9 N·m^2/C^2$",
            "电场强度: $E = \\frac{F}{q}$, 点电荷场 $E = k\\frac{Q}{r^2}$",
            "电势能: $E_p = qU$, 电势差: $U_{AB} = \\frac{W_{AB}}{q}$",
            "匀强电场: $E = \\frac{U}{d}$",
            "电容: $C = \\frac{Q}{U}$, 平行板 $C = \\frac{\\varepsilon S}{4\\pi kd}$",
            "电场力做功: $W = qU_{AB} = q(\\varphi_A - \\varphi_B)$",
            "电场线密→场强大，等势面密→场强大",
        ]},
        {"chapter": "恒定电流", "formulas": [
            "欧姆定律: $I = \\frac{U}{R}$",
            "电阻定律: $R = \\rho \\frac{L}{S}$",
            "电功率: $P = UI = I^2R = \\frac{U^2}{R}$",
            "电功: $W = UIt = I^2Rt = \\frac{U^2}{R}t$",
            "闭合回路: $I = \\frac{\\varepsilon}{R+r}$, $U = \\varepsilon - Ir$",
            "串联: $R = R_1 + R_2$, 并联: $\\frac{1}{R} = \\frac{1}{R_1} + \\frac{1}{R_2}$",
            "电流定义: $I = \\frac{q}{t} = nqvS$（微观）",
        ]},
        {"chapter": "磁场", "formulas": [
            "安培力: $F = BIL\\sin\\theta$",
            "洛伦兹力: $f = qvB\\sin\\theta$（方向用左手定则）",
            "圆周运动: $r = \\frac{mv}{qB}$, $T = \\frac{2\\pi m}{qB}$（与速度无关！）",
            "磁通量: $\\Phi = BS\\cos\\theta$（$\\theta$为B与面法线夹角）",
            "安培力方向: 左手定则（四指指向电流方向，磁力线穿手心）",
            "通电螺线管: 安培定则（右手四指弯曲方向为电流方向，拇指为N极）",
        ]},
        {"chapter": "电磁感应", "formulas": [
            "法拉第定律: $\\varepsilon = n\\frac{\\Delta\\Phi}{\\Delta t}$",
            "导体切割: $\\varepsilon = BLv$（$L$为有效切割长度）",
            "磁通量: $\\Phi = BS\\cos\\theta$",
            "感应电动势（旋转）: $\\varepsilon = nBS\\omega\\sin\\omega t$（从中性面计时）",
            "楞次定律: 感应电流的磁场总是阻碍引起感应电流的磁通量的变化",
            "感应电流: $I = \\frac{\\varepsilon}{R+r}$, 感应电荷: $q = \\frac{\\Delta\\Phi}{R}$（与时间无关！）",
        ]},
        {"chapter": "交变电流", "formulas": [
            "瞬时电动势: $e = nBS\\omega\\sin\\omega t$（从中性面开始计时）",
            "有效值: $E = \\frac{E_m}{\\sqrt{2}}$, $I = \\frac{I_m}{\\sqrt{2}}$, $U = \\frac{U_m}{\\sqrt{2}}$",
            "变压器电压比: $\\frac{U_1}{U_2} = \\frac{n_1}{n_2}$（理想变压器）",
            "变压器功率: $P_1 = P_2$（理想变压器）, $U_1I_1 = U_2I_2$",
            "输电线损耗: $P_{\\text{损}} = I^2 R_{\\text{线}} = \\frac{P^2 R_{\\text{线}}}{U^2}$",
            "频率: $f = \\frac{\\omega}{2\\pi} = \\frac{n \\cdot 转速}{60}$（$n$为线圈匝数取1时）",
        ]},
        {"chapter": "运动学基础", "formulas": [
            "平均速度: $v = \\frac{\\Delta x}{\\Delta t}$",
            "加速度: $a = \\frac{\\Delta v}{\\Delta t} = \\frac{v - v_0}{t}$",
            "速度公式: $v = v_0 + at$",
            "位移公式: $x = v_0 t + \\frac{1}{2}at^2$",
            "速度位移关系: $v^2 - v_0^2 = 2ax$",
            "中间时刻速度: $v_{t/2} = \\frac{v_0 + v}{2} = \\bar{v}$",
            "逐差法: $\\Delta x = aT^2$（相邻等时间间隔位移差恒定）",
            "自由落体: $h = \\frac{1}{2}gt^2$, $v = gt$, $g \\approx 9.8 m/s^2$",
            "竖直上抛: $v = v_0 - gt$, $h = v_0t - \\frac{1}{2}gt^2$",
        ]},
        {"chapter": "牛顿运动定律", "formulas": [
            "牛顿第二定律: $F_{\\text{合}} = ma$（矢量式！）",
            "超重: $N = m(g + a)$，失重: $N = m(g - a)$",
            "胡克定律: $F = kx$（$x$为弹簧形变量，非长度）",
            "滑动摩擦力: $f = \\mu N$（$N$不一定等于$mg$！）",
            "合力范围: $|F_1 - F_2| \\leq F \\leq F_1 + F_2$",
            "连接体加速度: $a = \\frac{F_{\\text{合外}}}{m_{\\text{总}}}$（整体法）",
        ]},
        {"chapter": "曲线运动与万有引力", "formulas": [
            "平抛运动: $x = v_0 t$, $y = \\frac{1}{2}gt^2$, $v = \\sqrt{v_0^2 + (gt)^2}$",
            "向心加速度: $a_n = \\frac{v^2}{r} = \\omega^2 r = \\frac{4\\pi^2 r}{T^2}$",
            "向心力: $F_n = \\frac{mv^2}{r} = m\\omega^2 r$",
            "线速度与角速度: $v = \\omega r = \\frac{2\\pi r}{T}$",
            "万有引力: $F = G\\frac{Mm}{r^2}$, $G = 6.67×10^{-11} N·m^2/kg^2$",
            "卫星速度: $v = \\sqrt{\\frac{GM}{r}}$（$r$越大，$v$越小）",
            "卫星周期: $T = 2\\pi\\sqrt{\\frac{r^3}{GM}}$（$r$越大，$T$越大）",
            "第一宇宙速度: $v_1 = \\sqrt{gR} = 7.9$ km/s（最大环绕速度）",
            "天体表面重力加速度: $g = \\frac{GM}{R^2}$",
        ]},
        {"chapter": "机械能", "formulas": [
            "功: $W = Fx\\cos\\theta$（$\\theta$为力与位移夹角）",
            "功率: $P = \\frac{W}{t} = Fv\\cos\\theta$（$Fv$为瞬时功率当$v$为瞬时速度时）",
            "动能定理: $W_{\\text{合}} = \\frac{1}{2}mv^2 - \\frac{1}{2}mv_0^2$",
            "重力势能: $E_p = mgh$（$h$相对参考面）",
            "弹性势能: $E_p = \\frac{1}{2}kx^2$",
            "动能: $E_k = \\frac{1}{2}mv^2$",
            "机械能守恒: $E_{k1} + E_{p1} = E_{k2} + E_{p2}$（只有重力/弹力做功时）",
            "功能关系: 合外力做功=动能变化，重力做功=重力势能变化的负值",
        ]},
        {"chapter": "动量", "formulas": [
            "动量: $p = mv$（矢量！）",
            "冲量: $I = Ft$（矢量！）",
            "动量定理: $F_{\\text{合}}t = mv - mv_0 = \\Delta p$",
            "动量守恒: $m_1v_1 + m_2v_2 = m_1v_1' + m_2v_2'$（系统合外力为零时）",
            "完全非弹性碰撞: $v = \\frac{m_1v_1 + m_2v_2}{m_1+m_2}$（碰后一起走）",
            "弹性碰撞（一维）: $v_1' = \\frac{(m_1-m_2)v_1 + 2m_2v_2}{m_1+m_2}$",
        ]},
    ],
    "化学": [
        {"chapter": "物质的量", "formulas": [
            "物质的量: $n = \\frac{N}{N_A}$, $N_A = 6.022 \\times 10^{23} mol^{-1}$",
            "摩尔质量: $M = \\frac{m}{n}$（单位 g/mol，数值上等于相对分子质量）",
            "气体摩尔体积: $V_m = \\frac{V}{n} = 22.4 L/mol$（标准状况）",
            "物质的量浓度: $c = \\frac{n}{V}$（单位 mol/L）",
            "稀释定律: $c_1V_1 = c_2V_2$",
            "质量分数与物质的量浓度: $c = \\frac{1000\\rho w}{M}$",
        ]},
        {"chapter": "化学平衡", "formulas": [
            "平衡常数: $K = \\frac{c^p(C) \\cdot c^q(D)}{c^m(A) \\cdot c^n(B)}$（只含气态和溶液态）",
            "转化率: $\\alpha = \\frac{已转化量}{起始量} × 100\\%$",
            "反应速率: $v = \\frac{\\Delta c}{\\Delta t}$（单位 mol/(L·min)）",
            "速率比 = 化学计量数之比: $v(A):v(B) = m:n$",
            "压强平衡常数: $K_p = \\frac{p_C^p \\cdot p_D^q}{p_A^m \\cdot p_B^n}$",
            "反应热: $\\Delta H = \\sum E_{\\text{断键}} - \\sum E_{\\text{成键}}$（键能法）",
            "盖斯定律: 总反应的 $\\Delta H = \\sum \\Delta H_i$（可加减拼凑）",
        ]},
        {"chapter": "电化学", "formulas": [
            "原电池: 负极氧化（失电子），正极还原（得电子）",
            "电解池: 阳极氧化（失电子），阴极还原（得电子）",
            "法拉第电解定律: $m = \\frac{MIt}{nF}$, $F = 96500 C/mol$",
            "电池电动势: $E = E_{\\text{正}} - E_{\\text{负}}$",
            "电解顺序: 阳极 $S^{2-}>I^->Br^->Cl^->OH^-$, 阴极 $Ag^+>Cu^{2+}>H^+$",
        ]},
        {"chapter": "水溶液中的离子反应", "formulas": [
            "水的离子积: $K_w = c(H^+) \\cdot c(OH^-) = 10^{-14}$（25℃）",
            "$pH = -\\lg c(H^+)$, $pOH = -\\lg c(OH^-)$, $pH + pOH = 14$",
            "电离常数: $K_a = \\frac{c(H^+) \\cdot c(A^-)}{c(HA)}$",
            "溶度积: $K_{sp} = c^m(M^{n+}) \\cdot c^n(X^{m-})$",
            "水解常数: $K_h = \\frac{K_w}{K_a}$（强碱弱酸盐）, $K_h = \\frac{K_w}{K_b}$（强酸弱碱盐）",
            "电荷守恒: 阳离子电荷总量 = 阴离子电荷总量",
            "物料守恒: 某元素各形态浓度之和 = 初始投入浓度",
            "质子守恒: 水电离产生的 $H^+$ = 水电离产生的 $OH^-$",
        ]},
        {"chapter": "有机化学基础", "formulas": [
            "不饱和度: $\\Omega = \\frac{2C + 2 + N - H}{2}$（含N时公式修正）",
            "醇催化氧化: $2R\\text{-}CH_2OH + O_2 \\xrightarrow{Cu/\\Delta} 2R\\text{-}CHO + 2H_2O$",
            "酯化反应: $R\\text{-}COOH + R'OH \\rightleftharpoons R\\text{-}COOR' + H_2O$（酸脱羟基醇脱氢）",
            "银镜反应: $R\\text{-}CHO + 2Ag(NH_3)_2^+ + 2OH^- \\rightarrow 2Ag\\downarrow + R\\text{-}COO^- + NH_3$",
            "加聚反应: $nCH_2=CH_2 \\xrightarrow{催化剂} [\\text{-}CH_2\\text{-}CH_2\\text{-}]_n$",
            "缩聚反应: 酯类/酰胺类缩合，注意 $-H_2O$ 的计量",
            "有机物燃烧: $C_xH_yO_z + (x+\\frac{y}{4}-\\frac{z}{2})O_2 \\rightarrow xCO_2 + \\frac{y}{2}H_2O$",
        ]},
        {"chapter": "金属及其化合物", "formulas": [
            "$Na$ 与水: $2Na + 2H_2O \\rightarrow 2NaOH + H_2\\uparrow$",
            "$Na_2O_2$ 与水: $2Na_2O_2 + 2H_2O \\rightarrow 4NaOH + O_2\\uparrow$",
            "$Na_2O_2$ 与 $CO_2$: $2Na_2O_2 + 2CO_2 \\rightarrow 2Na_2CO_3 + O_2$",
            "$Al$ 与 $NaOH$: $2Al + 2NaOH + 2H_2O \\rightarrow 2NaAlO_2 + 3H_2\\uparrow$",
            "$Al(OH)_3$ 两性: 酸 $\\rightarrow Al^{3+}$, 碱 $\\rightarrow AlO_2^-$",
            "$Fe^{2+}$ 与 $Fe^{3+}$ 检验: $Fe^{3+}$ 遇 $KSCN$ 变红, $Fe^{2+}$ 先加 $KSCN$ 不变再加氧化剂变红",
            "铝热反应: $2Al + Fe_2O_3 \\xrightarrow{点燃} 2Fe + Al_2O_3$",
        ]},
        {"chapter": "非金属及其化合物", "formulas": [
            "$Cl_2$ 与 $NaOH$: $Cl_2 + 2NaOH \\rightarrow NaCl + NaClO + H_2O$",
            "实验室制 $Cl_2$: $MnO_2 + 4HCl(浓) \\xrightarrow{\\Delta} MnCl_2 + Cl_2\\uparrow + 2H_2O$",
            "$SO_2$ 与 $NaOH$: $SO_2 + 2NaOH \\rightarrow Na_2SO_3 + H_2O$（过量NaOH）",
            "硝酸氧化性: $Cu + 4HNO_3(浓) \\rightarrow Cu(NO_3)_2 + 2NO_2\\uparrow + 2H_2O$",
            "稀硝酸: $3Cu + 8HNO_3(稀) \\rightarrow 3Cu(NO_3)_2 + 2NO\\uparrow + 4H_2O$",
            "$NH_3$ 实验室制法: $2NH_4Cl + Ca(OH)_2 \\xrightarrow{\\Delta} CaCl_2 + 2NH_3\\uparrow + 2H_2O$",
            "$SiO_2$ 与 $HF$: $SiO_2 + 4HF \\rightarrow SiF_4\\uparrow + 2H_2O$（酸中唯一能溶 $SiO_2$ 的）",
        ]},
    ],
    "地理": [
        {"chapter": "地球运动", "formulas": [
            "正午太阳高度角: $H = 90° - |\\varphi - \\delta|$（$\\varphi$为当地纬度，$\\delta$为直射点纬度）",
            "地方时计算: 所求地方时 $= $ 已知地方时 $\\pm \\frac{经度差}{15°}$（东加西减）",
            "昼弧与昼长: 昼长 $= \\frac{昼弧}{15°}$ 小时",
            "太阳直射点纬度 $\\approx 23°26' \\times \\sin\\left(\\frac{360°}{365} \\times d\\right)$（$d$为距春分日天数近似）",
            "区时计算: 区时 $= $ 已知区时 $\\pm$ 时区差（东加西减）",
            "日期变更: 向东过日界线（180°经线）日期减一天，向西加一天",
        ]},
        {"chapter": "大气与气候", "formulas": [
            "气温垂直递减率: 每升高100m，气温下降约 $0.6°C$",
            "热力环流: 冷热不均 $\\rightarrow$ 垂直运动 $\\rightarrow$ 水平气压差 $\\rightarrow$ 水平风",
            "风力近似: $F = -\\frac{\\Delta P}{\\Delta n}$（气压梯度力，$\\Delta P$为气压差，$\\Delta n$为距离）",
            "地转偏向: 北半球右偏，南半球左偏（科里奥利力 $f = 2m\\omega v\\sin\\varphi$）",
            "气候类型判断: 以温定带（最冷月气温），以水定型（降水季节分配）",
            "大气保温: 太阳短波→地面→地面长波→大气→大气逆辐射→保温",
        ]},
        {"chapter": "水循环与洋流", "formulas": [
            "水循环环节: 蒸发 $\\rightarrow$ 水汽输送 $\\rightarrow$ 降水 $\\rightarrow$ 地表径流/下渗 $\\rightarrow$ 地下径流",
            "洋流分布: 北半球副热带环流顺时针，南半球逆时针",
            "暖流: 低纬 $\\rightarrow$ 高纬（增温增湿），寒流: 高纬 $\\rightarrow$ 低纬（降温减湿）",
            "径流量 $\\approx$ 降水量 $-$ 蒸发量（水量平衡方程简化）",
            "河流补给类型: 雨水补给（最常见）、冰雪融水、地下水、湖泊水",
        ]},
        {"chapter": "地表形态", "formulas": [
            "内力作用: 地壳运动（褶皱+断层）、岩浆活动、变质作用",
            "外力作用: 风化 $\\rightarrow$ 侵蚀 $\\rightarrow$ 搬运 $\\rightarrow$ 沉积 $\\rightarrow$ 固结成岩",
            "岩石圈物质循环: 岩浆→岩浆岩→沉积岩→变质岩→岩浆（三类岩石互相转化）",
            "河流侵蚀: 上游下蚀+溯源侵蚀（V形谷），中下游侧蚀（河曲、牛轭湖）",
            "河流堆积: 冲积扇（山口）→冲积平原（中下游）→三角洲（入海口）",
            "背斜成谷向斜成山: 地形倒置现象（背斜顶部受张力易被侵蚀）",
        ]},
        {"chapter": "人口与城市", "formulas": [
            "人口自然增长率 $= $ 出生率 $-$ 死亡率",
            "城镇化率 $= \\frac{城镇人口}{总人口} \\times 100\\%$",
            "人口密度 $= \\frac{人口数}{面积}$（人/km²）",
            "人口增长模式: 原始型（高高低）→传统型（高低高）→现代型（低低低）",
            "城市等级体系: 等级越高 → 数量越少、服务范围越大、功能越多",
        ]},
        {"chapter": "产业与区位", "formulas": [
            "农业区位: 气候、地形、土壤、水源 + 市场、交通、政策、劳动力",
            "工业区位: 原料、动力、劳动力、市场、交通、政策、科技",
            "工业导向类型: 原料导向型（制糖）、市场导向型（啤酒）、动力导向型（电解铝）、技术导向型（芯片）、劳动力导向型（服装）",
            "农业地域类型: 季风水田农业、商品谷物农业、大牧场放牧业、混合农业、乳畜业",
            "韦伯工业区位论: 运费最低点→综合最低运费+劳动力+集聚",
        ]},
        {"chapter": "自然环境整体性与差异性", "formulas": [
            "纬度地带性（水平）: 赤道→两极，热量递减 → 自然带更替",
            "经度地带性（干湿）: 沿海→内陆，降水递减 → 自然带更替",
            "垂直地带性: 山麓→山顶，类似赤道→两极，基带=当地水平地带",
            "雪线高度: 阳坡>阴坡（温度），迎风坡<背风坡（降水多雪线低）",
            "非地带性: 地形、洋流、海陆分布等局地因素打破地带性规律",
        ]},
    ],
    "英语": [
        {"chapter": "核心语法公式", "formulas": [
            "五种基本句型: SV / SVO / SVP / SVOO / SVOC",
            "被动语态: $be + done$（时态体现在be上）",
            "现在完成时: $have/has + done$（强调过去对现在的影响）",
            "过去完成时: $had + done$（过去的过去）",
            "虚拟语气（与现在事实相反）: If + did/were, would/could + do",
            "虚拟语气（与过去事实相反）: If + had done, would/could + have done",
            "强调句: It is/was + 被强调部分 + that/who + 其余",
            "倒装句: Only/Never/Hardly/Not until... + 助动词 + 主语 + 谓语",
        ]},
        {"chapter": "从句要点", "formulas": [
            "定语从句关系词: who(人主), whom(人宾), which(物), whose(谁的), that(通用), where(地点), when(时间)",
            "名词性从句引导词: that(无意义), what(什么/所...的), whether/if(是否), wh-疑问词",
            "同位语从句: 解释说明抽象名词（news/fact/idea/belief...）+ that从句",
            "状语从句连词: because/since/as(原因), although/though(让步), if/unless(条件), so that/in order that(目的)",
            "非限制性定语从句: 用which不用that，用逗号隔开",
        ]},
        {"chapter": "非谓语动词公式", "formulas": [
            "doing: 主动/进行（作主语、宾语、表语、定语、状语）",
            "done: 被动/完成（作定语、表语、补语、状语）",
            "to do: 目的/将来（作主语、宾语、表语、定语、状语、补语）",
            "remember/forget + to do（未做）vs + doing（已做）",
            "see/hear/watch + do（全过程）vs + doing（正在进行）",
            "独立主格: 名词/代词 + doing/done/to do（逻辑主语≠句子主语）",
        ]},
        {"chapter": "写作高频句型", "formulas": [
            "It is universally acknowledged that...（众所周知……）",
            "Not only...but also...（不仅……而且……，not only在句首要倒装）",
            "The reason why...is that...（……的原因是……）",
            "There is no denying that...（不可否认……）",
            "Only by doing...can we...（只有通过……我们才能……，倒装）",
            "So + adj./adv. + 助动词 + 主语 + that...（如此……以至于……）",
        ]},
    ],
}


@router.get("/formulas")
def get_formulas(subject: str = ""):
    if subject and subject in FORMULAS:
        return FORMULAS[subject]
    return FORMULAS


# ── 各科易错点 ──
MISTAKES = {
    "数学": [
        {"chapter": "导数", "mistakes": [
            "含参讨论忘记分类：$f'(x)=0$ 有根时需讨论参数取值范围",
            "极值点≠最值点：极值是局部的，最值要比较端点和极值",
            "隐零点问题：$f'(x)=0$ 不能直接解时，用零点存在定理",
            "导数符号看错：$f'(x)>0$ 单调递增，不是 $f(x)>0$",
            "复合函数求导漏链式法则：$[f(g(x))]' = f'(g(x)) \\cdot g'(x)$",
            "极值点两侧导数变号才是极值，导数为零不一定是极值（如 $x^3$）",
        ]},
        {"chapter": "三角函数", "mistakes": [
            "辅助角公式中 $\\varphi$ 的象限判断容易出错，要看 $a$ 和 $b$ 的正负",
            "正弦定理求角时注意大角对大边，且可能有两解（SSA 情况）",
            "余弦定理算角时 $\\cos A$ 可能为负（钝角），不要漏掉",
            "三角函数图像平移：先缩再移 vs 先移再缩结果不同",
            "$\\sin(A+B) = \\sin C$ 在三角形中成立（因为 $A+B = \\pi - C$），但不要乱用",
            "弧度制和角度制混用：计算器模式要切换，公式中统一用弧度",
        ]},
        {"chapter": "圆锥曲线", "mistakes": [
            "忘记检验斜率不存在的情况：直线 $x=c$ 时韦达定理不适用",
            "判别式 $\\Delta \\geq 0$ 忘记取等号讨论",
            "焦点位置搞混：椭圆 $a^2$ 在哪个分母下，焦点就在哪个轴上",
            "设而不求 vs 联立求解搞混策略",
            "离心率范围：椭圆 $0<e<1$，双曲线 $e>1$，抛物线 $e=1$",
            "抛物线焦点到准线距离是 $p$，焦点到顶点是 $\\frac{p}{2}$，别搞混",
        ]},
        {"chapter": "数列", "mistakes": [
            "$a_1$ 不满足递推公式时需单独验证",
            "等比数列公比 $q \\neq 0$，且 $q=1$ 时求和公式不同",
            "裂项相消要注意首尾剩余项",
            "错位相减法：公比乘错位置导致符号出错",
            "$S_n$ 与 $a_n$ 关系：$a_n = S_n - S_{n-1}$（$n \\geq 2$），$a_1 = S_1$ 需单独验证",
            "数列单调性≠函数单调性：$a_{n+1} > a_n$ 才是递增，不能直接对 $n$ 求导",
        ]},
        {"chapter": "概率与统计", "mistakes": [
            "古典概型忘记等可能性条件",
            "条件概率 $P(A|B) \\neq P(B|A)$",
            "互斥和独立搞混：互斥是 $P(AB)=0$，独立是 $P(AB)=P(A)P(B)$",
            "正态分布对称性：$P(X<\\mu-a) = P(X>\\mu+a)$",
            "回归方程中 $\\hat{y}$ 是预测值，不是真实值",
            "超几何分布 vs 二项分布：不放回用超几何，有放回用二项",
        ]},
        {"chapter": "函数与不等式", "mistakes": [
            "均值不等式等号成立条件：$a=b$ 且 $a+b$ 或 $ab$ 为定值",
            "对数真数必须大于0，底数大于0且不等于1",
            "指数函数底数 $a>0$ 且 $a \\neq 1$，$0<a<1$ 时函数递减",
            "分段函数求值域时每段都要算，再取并集",
            "二次函数在闭区间上最值要讨论对称轴与区间的关系",
        ]},
    ],
    "物理": [
        {"chapter": "力与运动", "mistakes": [
            "受力分析漏力：先重力→弹力→摩擦力→其他力，按顺序不漏",
            "静摩擦力大小和方向都会变，不一定等于 $\\mu N$",
            "加速度方向与速度方向相同是加速，相反是减速（不是看正负）",
            "整体法和隔离法用错场景：求外力用整体法，求内力用隔离法",
            "绳的张力可以突变，弹簧弹力不能突变",
            "力的合成时不要忘了力是矢量，不能直接相加减",
        ]},
        {"chapter": "电场", "mistakes": [
            "电场强度是矢量，合成时要用平行四边形法则",
            "电势高低与正负电荷受力方向搞混：正电荷从高电势到低电势",
            "等势面上移动电荷，电场力做功为零",
            "平行板电容器：接电源时 $U$ 不变，断开后 $Q$ 不变",
            "带电粒子在电场中运动：注意重力是否忽略（质子/电子忽略，带电小球不忽略）",
            "电场线不是电荷运动轨迹！曲线运动时合力方向不一定沿电场线",
        ]},
        {"chapter": "磁场", "mistakes": [
            "安培力方向用左手定则，不是右手定则（右手定则判磁场方向）",
            "洛伦兹力永远不做功（垂直于速度方向），只改变速度方向",
            "带电粒子在磁场中做圆周运动，周期 $T = \\frac{2\\pi m}{qB}$ 与速度无关！",
            "复合场（电场+磁场+重力）中要画受力图，分析哪个力提供向心力",
            "速度选择器中 $v = \\frac{E}{B}$，只有这个速度的粒子能直线通过",
        ]},
        {"chapter": "电磁感应", "mistakes": [
            "楞次定律判断方向：阻碍的是磁通量的变化，不是磁通量本身",
            "感应电动势公式：$\\varepsilon = BLv$ 只适用于导体切割磁力线",
            "自感现象：通电自感阻碍电流增大，断电自感阻碍电流减小",
            "涡流方向判断：与磁通量变化方向相反",
            "感应电荷 $q = \\frac{\\Delta\\Phi}{R}$ 与时间无关，不要用 $I \\cdot t$ 去算",
            "法拉第定律中的 $n$ 是线圈匝数，不要漏乘",
        ]},
        {"chapter": "曲线运动与万有引力", "mistakes": [
            "平抛运动水平方向匀速，竖直方向自由落体，两个方向独立",
            "向心力不是新的力，是合力提供的效果",
            "圆周运动最高点：绳模型 $v_{\\text{min}}=\\sqrt{gR}$，杆模型 $v_{\\text{min}}=0$",
            "同步卫星高度固定约36000km，不能随意改变轨道高度",
            "卫星轨道越高，速度越小、周期越大、加速度越小（别搞反）",
            "变轨：加速→升轨，减速→降轨（喷气方向与速度方向相反→加速）",
        ]},
        {"chapter": "交变电流与变压器", "mistakes": [
            "有效值不是峰值除以2，是除以 $\\sqrt{2}$（正弦交流电）",
            "非正弦交流电的有效值不能用 $\\frac{U_m}{\\sqrt{2}}$，要回归定义",
            "变压器电压比适用于理想变压器，实际变压器有能量损耗",
            "远距离输电升压是为了减小电流从而减小线路损耗 $P_{\\text{损}}=I^2R$",
            "变压器不改变频率！输入输出频率相同",
        ]},
        {"chapter": "动量", "mistakes": [
            "动量是矢量！方向与速度相同，计算时要注意正方向",
            "动量守恒条件：系统所受合外力为零（或内力远大于外力）",
            "碰撞必须满足：动量守恒 + 动能不增加 + 速度关系合理",
            "完全非弹性碰撞动能损失最大（碰后一起走），但动量仍守恒",
            "反冲运动（如火箭）：系统动量守恒，不要只看一个物体",
        ]},
        {"chapter": "机械能", "mistakes": [
            "机械能守恒条件：只有重力和弹簧弹力做功（摩擦力做功则不守恒）",
            "功率 $P=Fv$ 中 $v$ 是瞬时速度时得到瞬时功率，是平均速度时得到平均功率",
            "汽车启动问题：恒力启动→先匀加速后加速减小→最终匀速（$P=Fv_{max}$）",
            "功是标量但有正负：力与位移同向做正功，反向做负功",
            "弹性势能不一定能算出来，但弹力做功=弹性势能减少量",
        ]},
    ],
    "化学": [
        {"chapter": "物质的量", "mistakes": [
            "气体摩尔体积 22.4L/mol 只在标准状况（0℃, 101kPa）下适用",
            "配制溶液时：先计算→称量/量取→溶解冷却→转移→洗涤→定容→摇匀",
            "稀释不改变溶质的物质的量，但体积不能简单相加（密度不同）",
            "$N_A$ 陷阱：标况下水是液态（不能用22.4L），$NO_2$ 存在二聚",
        ]},
        {"chapter": "离子反应", "mistakes": [
            "强电解质不一定溶于水（如 $BaSO_4$ 是强电解质但难溶）",
            "离子共存问题：注意隐含条件（酸性、碱性、无色等）",
            "离子方程式中沉淀、气体、弱电解质不能拆",
            "$Na_2O_2 + H_2O$ 的离子方程式中 $Na_2O_2$ 不能拆",
            "微溶物：做生成物不拆（写化学式），做反应物且稀溶液才拆",
        ]},
        {"chapter": "氧化还原反应", "mistakes": [
            "升失氧降得还：化合价升高→失电子→被氧化→是还原剂",
            "歧化反应：同一元素既升又降（如 $Cl_2 + NaOH$）",
            "电子转移总数要相等（得失电子守恒）",
            "中间价态既能做氧化剂又能做还原剂",
            "浓硫酸是氧化剂（热的浓硫酸），稀硫酸中 $H^+$ 才是氧化剂",
            "$Fe$ 与 $Cl_2$ 反应生成 $FeCl_3$（不是 $FeCl_2$），$Fe$ 与 $HCl$ 反应生成 $FeCl_2$",
        ]},
        {"chapter": "化学平衡", "mistakes": [
            "等效平衡：恒温恒容看物质的量，恒温恒压看物质的量之比",
            "加催化剂不改变平衡位置，只加快反应速率",
            "平衡常数只与温度有关，与浓度压强无关",
            "勒夏特列原理：平衡移动只能减弱改变，不能消除改变",
            "$Q_c > K$ 平衡逆移，$Q_c < K$ 平衡正移",
            "增大压强：有气体参与且两边气体计量数不等时才移动",
        ]},
        {"chapter": "水溶液中的离子反应", "mistakes": [
            "盐类水解是微弱的，不能说完全水解（除少数如 $Al_2S_3$）",
            "水解和电离是竞争关系：$NaHCO_3$ 水解>电离（碱性），$NaHSO_3$ 电离>水解（酸性）",
            "三大守恒（电荷/物料/质子）要全写对，缺一种就可能算错",
            "滴定终点≠恰好完全反应，指示剂变色范围不同会导致微小误差",
            "溶度积 $K_{sp}$ 只与温度有关，$Q > K_{sp}$ 沉淀生成，$Q < K_{sp}$ 沉淀溶解",
        ]},
        {"chapter": "电化学", "mistakes": [
            "原电池中阴阳离子移动方向：阳离子移向正极，阴离子移向负极",
            "电解池阳极材料如果是活性金属（非Pt/C），阳极本身会溶解",
            "电镀时：镀件做阴极，镀层金属做阳极，电镀液含镀层金属离子",
            "计算电解产物时注意放电顺序，先放电完了才轮到下一个",
        ]},
        {"chapter": "有机化学", "mistakes": [
            "羟基 $-OH$ 连在苯环上是酚，连在链上是醇，性质不同",
            "酯化反应：酸脱羟基醇脱氢（不是酸脱氢）",
            "同分异构体漏写：注意碳链异构、位置异构、官能团异构",
            "有机物命名：最长碳链选主链，取代基编号从近端开始",
            "苯环上的取代基有定位效应：-OH/-NH₂邻对位活化，-NO₂/-COOH间位钝化",
            "醛基既能被氧化（银镜反应）又能被还原（加氢），是有机中独特的双面官能团",
        ]},
        {"chapter": "金属及其化合物", "mistakes": [
            "$Na$ 保存在煤油中，$K$ 保存在煤油中，$Li$ 保存在石蜡中（密度比煤油小会浮）",
            "$Na_2O_2$ 不是碱性氧化物（与水反应生成 $O_2$，是过氧化物）",
            "$Al(OH)_3$ 两性但不溶于氨水，只溶于强酸强碱",
            "$Fe^{2+}$ 和 $Fe^{3+}$ 转化：$Fe^{2+}$ 加氧化剂（$Cl_2$, $H_2O_2$）→ $Fe^{3+}$，$Fe^{3+}$ 加还原剂（$Fe$, $Cu$）→ $Fe^{2+}$",
            "铝热反应需要引燃剂（镁条+氯酸钾），不是直接点铝粉",
        ]},
    ],
    "英语": [
        {"chapter": "时态语态", "mistakes": [
            "现在完成时 vs 一般过去时：have done 强调对现在的影响，did 强调过去的动作",
            "被动语态中不及物动词没有被动形式（如 happen, take place, break out）",
            "时间/条件状语从句中用一般现在时表将来（主将从现）",
            "since 后面的从句用一般过去时，主句用现在完成时",
            "过去完成时表示「过去的过去」，不能单独使用必须有参照时间点",
            "进行时态表将来：be doing（已有安排），be going to do（打算），will do（临时决定）",
        ]},
        {"chapter": "从句", "mistakes": [
            "定语从句 that/which 混用：介词后只能用 which，不能用 that",
            "名词性从句中 what = the thing that，不要和 that 搞混",
            "同位语从句 vs 定语从句：同位语从句解释内容，定语从句修饰限定",
            "强调句 It is...that 去掉后句子完整，定语从句去掉后不完整",
            "where 引导定语从句修饰地点名词，引导状语从句表示「在...的地方」",
            "whoever = anyone who, whatever = anything that（名词性从句），no matter who/what 只引导让步状语从句",
        ]},
        {"chapter": "非谓语动词", "mistakes": [
            "doing 表主动/进行，done 表被动/完成",
            "remember to do（记得去做）vs remember doing（记得做过）",
            "作目的状语只能用 to do，不能用 doing",
            "独立主格结构：非谓语的逻辑主语与主句主语不同时使用",
            "有些动词只接 doing（enjoy/finish/mind/avoid/suggest），有些只接 to do（want/hope/decide/refuse）",
            "be used to doing（习惯做）vs used to do（过去常做）vs be used to do（被用来做）",
        ]},
        {"chapter": "完形填空与词汇", "mistakes": [
            "熟词生义陷阱：meet（满足）、address（解决）、cover（报道/覆盖/支付）、charge（收费/充电/指控）",
            "近义词辨析：affect（影响）vs effect（效果）, rise（不及物）vs raise（及物）",
            "固定搭配不要拆：be accustomed to, look forward to, pay attention to 中 to 是介词+doing",
            "完形填空要通读全文再选，不要看一空填一空",
        ]},
        {"chapter": "阅读与写作", "mistakes": [
            "推理判断题不要过度推理，答案必须有原文依据",
            "主旨大意题看首段和各段首句，不要被细节干扰",
            "七选五注意代词指代（this/that/these/such）和逻辑连接词",
            "读后续写要延续原文风格和情感基调，不要突然转变",
            "应用文写作格式分（信/通知/演讲稿）不要搞混",
        ]},
    ],
    "地理": [
        {"chapter": "地球运动", "mistakes": [
            "地方时计算：东加西减，每15°差1小时",
            "正午太阳高度公式中纬度差取绝对值（同侧相减异侧相加）",
            "晨昏线与经线重合→春秋分，与极圈相切→夏冬至",
            "南北半球季节相反，昼夜长短相反",
            "地方时≠区时：地方时按经度算，区时按时区中央经线算",
            "近日点（1月初）不是冬至，远日点（7月初）不是夏至（相差约半个月）",
        ]},
        {"chapter": "大气", "mistakes": [
            "气温日较差：大陆>海洋，晴天>阴天",
            "热力环流：近地面热的地方气压低（不是高），高空相反",
            "风向判断：先画气压梯度力（垂直等压线指向低压），再偏转",
            "气候类型判断口诀搞混：以温定带，以水定型",
            "暖锋过境后天气转晴，冷锋过境后也转晴（不要搞反过境时和过境后）",
            "焚风效应：气流翻山后温度升高、湿度降低（湿绝热递减率<干绝热递减率）",
        ]},
        {"chapter": "水循环与洋流", "mistakes": [
            "暖流增温增湿，寒流降温减湿（不要反过来）",
            "北半球洋流顺时针，南半球逆时针（副热带环流）",
            "内流河不注入海洋，但不一定没有水",
            "地下水补给河流 vs 河流补给地下水：取决于水位高低",
            "人类活动主要影响地表径流环节（修水库、植树造林等）",
        ]},
        {"chapter": "地表形态", "mistakes": [
            "背斜不一定是山，向斜不一定是谷（地形倒置很常考）",
            "判断背斜向斜：看岩层新老关系，中间老两边新=背斜",
            "河流凹岸侵蚀凸岸堆积（凹岸适合建港口，凸岸适合建聚落）",
            "河流三角洲在入海口，冲积扇在出山口，不要搞混",
            "喀斯特地貌条件：可溶性岩石（石灰岩）+ 流水溶蚀",
            "风力沉积：近处颗粒大（沙丘），远处颗粒细（黄土）",
        ]},
        {"chapter": "人口与城市", "mistakes": [
            "人口增长模式转变：先死亡率下降，后出生率下降",
            "城市热岛效应：城区气温高→气流上升→郊区风吹向城区（近地面风向城区）",
            "城市功能分区：商业区在市中心（地租最高），工业区在外围（交通便利处）",
            "逆城镇化≠城镇化水平下降，是人口从城市迁往郊区/小城镇",
        ]},
        {"chapter": "产业与区位", "mistakes": [
            "农业区位中市场决定农业类型和规模，自然条件决定适不适合种",
            "工业区位：科技是第一生产力，但不是所有工业都是技术导向型",
            "产业转移方向：发达→发展中，沿海→内地（劳动力成本驱动）",
            "交通运输方式选择：贵重急用→航空，大宗笨重→水运/铁路，短途灵活→公路",
        ]},
        {"chapter": "自然环境整体性与差异性", "mistakes": [
            "水平地域分异：从赤道到两极是热量差异，从沿海到内陆是水分差异",
            "垂直地带性基带=山麓自然带=当地水平自然带",
            "雪线高度受温度和降水共同影响：迎风坡降水多但雪线反而低（降雪多）",
            "非地带性实例：南半球缺少亚寒带针叶林带（没有足够的陆地面积）",
            "牧场、荒漠等受经度地带性（干湿度）影响，不是纬度地带性",
        ]},
    ],
}


@router.get("/mistakes")
def get_mistakes(subject: str = ""):
    if subject and subject in MISTAKES:
        return MISTAKES[subject]
    return MISTAKES
