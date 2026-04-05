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
        {"chapter": "概率与统计", "formulas": [
            "离散型随机变量期望: $E(X) = \\sum_{i} x_i p_i$",
            "离散型随机变量方差: $D(X) = \\sum_{i} (x_i - E(X))^2 p_i$",
            "二项分布: $P(X=k) = C_n^k p^k (1-p)^{n-k}$, $E(X)=np$, $D(X)=np(1-p)$",
            "正态分布: $f(x) = \\frac{1}{\\sigma\\sqrt{2\\pi}} e^{-\\frac{(x-\\mu)^2}{2\\sigma^2}}$",
            "回归方程: $\\hat{y} = \\hat{b}x + \\hat{a}$, $\\hat{b} = \\frac{\\sum(x_i-\\bar{x})(y_i-\\bar{y})}{\\sum(x_i-\\bar{x})^2}$",
            "相关系数: $r = \\frac{\\sum(x_i-\\bar{x})(y_i-\\bar{y})}{\\sqrt{\\sum(x_i-\\bar{x})^2 \\cdot \\sum(y_i-\\bar{y})^2}}$",
            "独立性检验: $K^2 = \\frac{n(ad-bc)^2}{(a+b)(c+d)(a+c)(b+d)}$",
        ]},
        {"chapter": "空间向量与立体几何", "formulas": [
            "空间向量点积: $\\vec{a} \\cdot \\vec{b} = x_1x_2 + y_1y_2 + z_1z_2 = |\\vec{a}||\\vec{b}|\\cos\\theta$",
            "向量模: $|\\vec{a}| = \\sqrt{x^2 + y^2 + z^2}$",
            "两向量夹角: $\\cos\\theta = \\frac{\\vec{a} \\cdot \\vec{b}}{|\\vec{a}||\\vec{b}|}$",
            "二面角余弦: $\\cos\\theta = \\frac{\\vec{n_1} \\cdot \\vec{n_2}}{|\\vec{n_1}||\\vec{n_2}|}$（法向量法）",
            "点到平面距离: $d = \\frac{|\\vec{AP} \\cdot \\vec{n}|}{|\\vec{n}|}$（法向量法）",
            "线面角正弦: $\\sin\\theta = \\frac{|\\vec{a} \\cdot \\vec{n}|}{|\\vec{a}||\\vec{n}|}$（直线方向向量与平面法向量）",
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
        {"chapter": "交变电流", "formulas": [
            "瞬时电动势: $e = nBS\\omega\\sin\\omega t$（从中性面开始计时）",
            "有效值: $E = \\frac{E_m}{\\sqrt{2}}$, $I = \\frac{I_m}{\\sqrt{2}}$, $U = \\frac{U_m}{\\sqrt{2}}$",
            "变压器电压比: $\\frac{U_1}{U_2} = \\frac{n_1}{n_2}$（理想变压器）",
            "输电线损耗: $P_{\\text{损}} = I^2 R_{\\text{线}} = \\frac{P^2 R_{\\text{线}}}{U^2}$",
        ]},
        {"chapter": "运动学基础", "formulas": [
            "平均速度: $v = \\frac{\\Delta x}{\\Delta t}$",
            "加速度: $a = \\frac{\\Delta v}{\\Delta t} = \\frac{v - v_0}{t}$",
            "速度公式: $v = v_0 + at$",
            "位移公式: $x = v_0 t + \\frac{1}{2}at^2$",
            "速度位移关系: $v^2 - v_0^2 = 2ax$",
            "中间时刻速度: $v_{t/2} = \\frac{v_0 + v}{2} = \\bar{v}$",
            "逐差法: $\\Delta x = aT^2$",
            "自由落体: $h = \\frac{1}{2}gt^2$, $v = gt$",
        ]},
        {"chapter": "牛顿运动定律", "formulas": [
            "牛顿第二定律: $F_{\\text{合}} = ma$",
            "超重: $N = m(g + a)$，失重: $N = m(g - a)$",
            "胡克定律: $F = kx$",
            "滑动摩擦力: $f = \\mu N$",
            "合力范围: $|F_1 - F_2| \\leq F \\leq F_1 + F_2$",
        ]},
        {"chapter": "曲线运动与万有引力", "formulas": [
            "平抛运动: $x = v_0 t$, $y = \\frac{1}{2}gt^2$",
            "向心加速度: $a_n = \\frac{v^2}{r} = \\omega^2 r$",
            "向心力: $F_n = \\frac{mv^2}{r} = m\\omega^2 r$",
            "线速度与角速度: $v = \\omega r = \\frac{2\\pi r}{T}$",
            "万有引力: $F = G\\frac{Mm}{r^2}$",
            "卫星速度: $v = \\sqrt{\\frac{GM}{r}}$",
            "卫星周期: $T = 2\\pi\\sqrt{\\frac{r^3}{GM}}$",
            "第一宇宙速度: $v_1 = \\sqrt{gR} = 7.9$ km/s",
        ]},
        {"chapter": "机械能", "formulas": [
            "功: $W = Fx\\cos\\theta$",
            "功率: $P = \\frac{W}{t} = Fv\\cos\\theta$",
            "动能定理: $W_{\\text{合}} = \\frac{1}{2}mv^2 - \\frac{1}{2}mv_0^2$",
            "重力势能: $E_p = mgh$",
            "动能: $E_k = \\frac{1}{2}mv^2$",
            "机械能守恒: $E_{k1} + E_{p1} = E_{k2} + E_{p2}$",
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
        {"chapter": "水溶液中的离子反应", "formulas": [
            "水的离子积: $K_w = c(H^+) \\cdot c(OH^-) = 10^{-14}$（25℃）",
            "$pH = -\\lg c(H^+)$",
            "电离常数: $K_a = \\frac{c(H^+) \\cdot c(A^-)}{c(HA)}$",
            "溶度积: $K_{sp} = c^m(M^{n+}) \\cdot c^n(X^{m-})$",
            "水解常数: $K_h = \\frac{K_w}{K_a}$（强碱弱酸盐）",
        ]},
        {"chapter": "有机化学基础", "formulas": [
            "不饱和度: $\\Omega = \\frac{2C + 2 - H}{2}$（用于判断双键/环数）",
            "醇催化氧化: $2R\\text{-}CH_2OH + O_2 \\xrightarrow{Cu/\\Delta} 2R\\text{-}CHO + 2H_2O$",
            "酯化反应: $R\\text{-}COOH + R'OH \\rightleftharpoons R\\text{-}COOR' + H_2O$",
            "银镜反应: $R\\text{-}CHO + 2Ag(NH_3)_2^+ + 2OH^- \\rightarrow 2Ag\\downarrow + R\\text{-}COO^- + NH_3$",
            "加聚反应: $nCH_2=CH_2 \\xrightarrow{催化剂} [\\text{-}CH_2\\text{-}CH_2\\text{-}]_n$",
        ]},
    ],
    "地理": [
        {"chapter": "地球运动", "formulas": [
            "正午太阳高度角: $H = 90° - |\\varphi - \\delta|$（$\\varphi$为当地纬度，$\\delta$为直射点纬度）",
            "地方时计算: 所求地方时 $= $ 已知地方时 $\\pm \\frac{经度差}{15°}$（东加西减）",
            "昼弧与昼长: 昼长 $= \\frac{昼弧}{15°}$ 小时",
            "太阳直射点纬度 $\\approx 23°26' \\times \\sin\\left(\\frac{360°}{365} \\times d\\right)$（$d$为距春分日天数近似）",
        ]},
        {"chapter": "大气与气候", "formulas": [
            "气温垂直递减率: 每升高100m，气温下降约 $0.6°C$",
            "热力环流: 冷热不均 $\\rightarrow$ 垂直运动 $\\rightarrow$ 水平气压差 $\\rightarrow$ 水平风",
            "风力近似: $F = -\\frac{\\Delta P}{\\Delta n}$（气压梯度力，$\\Delta P$为气压差，$\\Delta n$为距离）",
            "地转偏向: 北半球右偏，南半球左偏（科里奥利力 $f = 2m\\omega v\\sin\\varphi$）",
        ]},
        {"chapter": "水循环与洋流", "formulas": [
            "水循环环节: 蒸发 $\\rightarrow$ 水汽输送 $\\rightarrow$ 降水 $\\rightarrow$ 地表径流/下渗 $\\rightarrow$ 地下径流",
            "洋流分布: 北半球副热带环流顺时针，南半球逆时针",
            "暖流: 低纬 $\\rightarrow$ 高纬（增温增湿），寒流: 高纬 $\\rightarrow$ 低纬（降温减湿）",
            "径流量 $\\approx$ 降水量 $-$ 蒸发量（水量平衡方程简化）",
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
        ]},
        {"chapter": "圆锥曲线", "mistakes": [
            "忘记检验斜率不存在的情况：直线 $x=c$ 时韦达定理不适用",
            "判别式 $\\Delta \\geq 0$ 忘记取等号讨论",
            "焦点位置搞混：椭圆 $a^2$ 在哪个分母下，焦点就在哪个轴上",
            "设而不求 vs 联立求解搞混策略",
            "离心率范围：椭圆 $0<e<1$，双曲线 $e>1$，抛物线 $e=1$",
        ]},
        {"chapter": "数列", "mistakes": [
            "$a_1$ 不满足递推公式时需单独验证",
            "等比数列公比 $q \\neq 0$，且 $q=1$ 时求和公式不同",
            "裂项相消要注意首尾剩余项",
            "错位相减法：公比乘错位置导致符号出错",
            "$S_n$ 与 $a_n$ 关系：$a_n = S_n - S_{n-1}$（$n \\geq 2$），$a_1 = S_1$ 需单独验证",
        ]},
        {"chapter": "概率与统计", "mistakes": [
            "古典概型忘记等可能性条件",
            "条件概率 $P(A|B) \\neq P(B|A)$",
            "互斥和独立搞混：互斥是 $P(AB)=0$，独立是 $P(AB)=P(A)P(B)$",
            "正态分布对称性：$P(X<\\mu-a) = P(X>\\mu+a)$",
            "回归方程中 $\\hat{y}$ 是预测值，不是真实值",
        ]},
    ],
    "物理": [
        {"chapter": "力与运动", "mistakes": [
            "受力分析漏力：先重力→弹力→摩擦力→其他力，按顺序不漏",
            "静摩擦力大小和方向都会变，不一定等于 $\\mu N$",
            "加速度方向与速度方向相同是加速，相反是减速（不是看正负）",
            "整体法和隔离法用错场景：求外力用整体法，求内力用隔离法",
            "绳的张力可以突变，弹簧弹力不能突变",
        ]},
        {"chapter": "电场", "mistakes": [
            "电场强度是矢量，合成时要用平行四边形法则",
            "电势高低与正负电荷受力方向搞混",
            "等势面上移动电荷，电场力做功为零",
            "平行板电容器：接电源时 $U$ 不变，断开后 $Q$ 不变",
            "带电粒子在电场中运动：注意重力是否忽略",
        ]},
        {"chapter": "电磁感应", "mistakes": [
            "楞次定律判断方向：阻碍的是磁通量的变化，不是磁通量本身",
            "感应电动势公式：$\\varepsilon = BLv$ 只适用于导体切割磁力线",
            "自感现象：通电自感阻碍电流增大，断电自感阻碍电流减小",
            "涡流方向判断：与磁通量变化方向相反",
        ]},
        {"chapter": "曲线运动", "mistakes": [
            "平抛运动水平方向匀速，竖直方向自由落体，两个方向独立",
            "向心力不是新的力，是合力提供的效果",
            "圆周运动最高点：绳模型 $v_{\\text{min}}=\\sqrt{gR}$，杆模型 $v_{\\text{min}}=0$",
            "同步卫星高度固定约36000km，不能随意改变轨道高度",
        ]},
    ],
    "化学": [
        {"chapter": "离子反应", "mistakes": [
            "强电解质不一定溶于水（如 $BaSO_4$ 是强电解质但难溶）",
            "离子共存问题：注意隐含条件（酸性、碱性、无色等）",
            "离子方程式中沉淀、气体、弱电解质不能拆",
            "$Na_2O_2 + H_2O$ 的离子方程式中 $Na_2O_2$ 不能拆",
        ]},
        {"chapter": "氧化还原反应", "mistakes": [
            "升失氧降得还：化合价升高→失电子→被氧化→是还原剂",
            "歧化反应：同一元素既升又降（如 $Cl_2 + NaOH$）",
            "电子转移总数要相等（得失电子守恒）",
            "中间价态既能做氧化剂又能做还原剂",
        ]},
        {"chapter": "化学平衡", "mistakes": [
            "等效平衡：恒温恒容看物质的量，恒温恒压看物质的量之比",
            "加催化剂不改变平衡位置，只加快反应速率",
            "平衡常数只与温度有关，与浓度压强无关",
            "勒夏特列原理：平衡移动只能减弱改变，不能消除改变",
            "$Q_c > K$ 平衡逆移，$Q_c < K$ 平衡正移",
        ]},
        {"chapter": "有机化学", "mistakes": [
            "羟基 $-OH$ 连在苯环上是酚，连在链上是醇，性质不同",
            "酯化反应：酸脱羟基醇脱氢（不是酸脱氢）",
            "同分异构体漏写：注意碳链异构、位置异构、官能团异构",
            "有机物命名：最长碳链选主链，取代基编号从近端开始",
        ]},
    ],
    "英语": [
        {"chapter": "时态语态", "mistakes": [
            "现在完成时 vs 一般过去时：have done 强调对现在的影响，did 强调过去的动作",
            "被动语态中不及物动词没有被动形式（如 happen, take place）",
            "时间/条件状语从句中用一般现在时表将来",
            "since 后面的从句用一般过去时，主句用现在完成时",
        ]},
        {"chapter": "从句", "mistakes": [
            "定语从句 that/which 混用：介词后只能用 which，不能用 that",
            "名词性从句中 what = the thing that，不要和 that 搞混",
            "同位语从句 vs 定语从句：同位语从句解释内容，定语从句修饰限定",
            "强调句 It is...that 去掉后句子完整，定语从句去掉后不完整",
        ]},
        {"chapter": "非谓语动词", "mistakes": [
            "doing 表主动/进行，done 表被动/完成",
            "remember to do（记得去做）vs remember doing（记得做过）",
            "作目的状语只能用 to do，不能用 doing",
            "独立主格结构：非谓语的逻辑主语与主句主语不同时使用",
        ]},
    ],
    "地理": [
        {"chapter": "地球运动", "mistakes": [
            "地方时计算：东加西减，每15°差1小时",
            "正午太阳高度公式中纬度取绝对值",
            "晨昏线与经线重合→春秋分，与极圈相切→夏冬至",
            "南北半球季节相反，昼夜长短相反",
        ]},
        {"chapter": "大气", "mistakes": [
            "气温日较差：大陆>海洋，晴天>阴天",
            "热力环流：近地面热的地方气压低（不是高）",
            "风向判断：先画气压梯度力（垂直等压线指向低压），再偏转",
            "气候类型判断口诀搞混：以温定带，以水定型",
            "暖锋过境后天气转晴，冷锋过境后也转晴（不要搞反过境时和过境后）",
        ]},
        {"chapter": "水循环与洋流", "mistakes": [
            "暖流增温增湿，寒流降温减湿（不要反过来）",
            "北半球洋流顺时针，南半球逆时针（副热带环流）",
            "内流河不注入海洋，但不一定没有水",
            "地下水补给河流 vs 河流补给地下水：取决于水位高低",
        ]},
    ],
}


@router.get("/mistakes")
def get_mistakes(subject: str = ""):
    if subject and subject in MISTAKES:
        return MISTAKES[subject]
    return MISTAKES
