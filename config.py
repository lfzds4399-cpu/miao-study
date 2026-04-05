import os

_env_cache = {}
_loaded = False

def _load_env():
    global _loaded
    if _loaded:
        return
    # 复用 Tetrahedron 的 .env
    for env_path in [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"),
        os.path.join("D:/作品/AI工具/claude-saas", ".env"),
    ]:
        if os.path.exists(env_path):
            with open(env_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, val = line.split("=", 1)
                        _env_cache[key.strip()] = val.strip().strip('"').strip("'")
            break
    _loaded = True

def get_key(name: str) -> str:
    val = os.environ.get(name)
    if val:
        return val
    _load_env()
    return _env_cache.get(name, "")

def anthropic_key() -> str:
    return get_key("ANTHROPIC_API_KEY")

def deepseek_key() -> str:
    return get_key("DEEPSEEK_API_KEY")

def openai_key() -> str:
    return get_key("OPENAI_API_KEY")

def ai_provider() -> str:
    """返回当前使用的AI提供商: deepseek / anthropic"""
    if deepseek_key():
        return "deepseek"
    return "anthropic"


# ── 高中科目与章节体系（高一+高二） ──
SUBJECTS = {
    "语文": {
        "icon": "📖", "color": "#e86450",
        "chapters": [
            {"id": "yw-1", "name": "古代诗歌阅读", "sections": ["诗歌鉴赏技巧", "意象与意境", "表达技巧分析", "诗歌对比阅读"]},
            {"id": "yw-2", "name": "文言文阅读", "sections": ["实词与虚词", "文言句式", "翻译技巧", "文言文断句"]},
            {"id": "yw-3", "name": "现代文阅读", "sections": ["论述类文本", "文学类文本", "实用类文本", "信息类文本"]},
            {"id": "yw-4", "name": "语言文字运用", "sections": ["成语辨析", "病句修改", "语言表达", "修辞手法"]},
            {"id": "yw-5", "name": "写作", "sections": ["议论文写作", "记叙文写作", "材料作文审题", "作文结构技巧"]},
        ]
    },
    "数学": {
        "icon": "📐", "color": "#3b82f6",
        "chapters": [
            {"id": "sx-1", "name": "导数及其应用", "sections": ["导数的概念", "导数的运算", "导数与函数单调性", "导数与极值最值", "导数综合应用"]},
            {"id": "sx-2", "name": "圆锥曲线", "sections": ["椭圆", "双曲线", "抛物线", "直线与圆锥曲线", "圆锥曲线综合"]},
            {"id": "sx-3", "name": "概率与统计", "sections": ["离散型随机变量", "二项分布", "正态分布", "回归分析", "独立性检验"]},
            {"id": "sx-4", "name": "数列", "sections": ["等差数列", "等比数列", "数列求和", "数列递推", "数列综合"]},
            {"id": "sx-5", "name": "空间向量与立体几何", "sections": ["空间向量基础", "空间角的计算", "空间距离", "向量法证明"]},
        ]
    },
    "英语": {
        "icon": "🌍", "color": "#10b981",
        "chapters": [
            {"id": "yy-1", "name": "阅读理解", "sections": ["主旨大意", "细节理解", "推理判断", "词义猜测", "七选五"]},
            {"id": "yy-2", "name": "完形填空", "sections": ["记叙文完形", "说明文完形", "议论文完形", "解题技巧"]},
            {"id": "yy-3", "name": "语法填空", "sections": ["时态语态", "非谓语动词", "定语从句", "名词性从句", "虚拟语气"]},
            {"id": "yy-4", "name": "写作", "sections": ["应用文写作", "读后续写", "概要写作", "高级句型积累"]},
            {"id": "yy-5", "name": "词汇积累", "sections": ["高频词汇", "词组搭配", "词根词缀", "熟词生义"]},
        ]
    },
    "物理": {
        "icon": "⚡", "color": "#8b5cf6",
        "chapters": [
            # 高一
            {"id": "wl-g1-1", "name": "【高一】运动的描述", "sections": ["质点与参考系", "位移与路程", "速度与速率", "加速度"]},
            {"id": "wl-g1-2", "name": "【高一】匀变速直线运动", "sections": ["速度公式v=v₀+at", "位移公式x=v₀t+½at²", "速度位移公式", "自由落体运动", "追及相遇问题"]},
            {"id": "wl-g1-3", "name": "【高一】相互作用——力", "sections": ["重力与弹力", "摩擦力", "力的合成与分解", "共点力平衡", "受力分析方法"]},
            {"id": "wl-g1-4", "name": "【高一】牛顿运动定律", "sections": ["牛顿第一定律", "牛顿第二定律F=ma", "牛顿第三定律", "超重与失重", "连接体问题"]},
            {"id": "wl-g1-5", "name": "【高一】曲线运动", "sections": ["运动的合成与分解", "平抛运动", "圆周运动", "向心力与向心加速度", "生活中的圆周运动"]},
            {"id": "wl-g1-6", "name": "【高一】万有引力与宇宙航行", "sections": ["开普勒三定律", "万有引力定律", "天体质量计算", "卫星运动", "宇宙速度"]},
            {"id": "wl-g1-7", "name": "【高一】机械能守恒", "sections": ["功和功率", "动能定理", "重力势能", "机械能守恒定律", "能量守恒定律"]},
            # 高二
            {"id": "wl-1", "name": "【高二】电场", "sections": ["库仑定律", "电场强度", "电势与电势能", "电容器", "带电粒子运动"]},
            {"id": "wl-2", "name": "【高二】恒定电流", "sections": ["欧姆定律", "电阻定律", "串并联电路", "电功与电功率", "闭合电路欧姆定律"]},
            {"id": "wl-3", "name": "【高二】磁场", "sections": ["磁场基础", "安培力", "洛伦兹力", "带电粒子在磁场中运动", "复合场"]},
            {"id": "wl-4", "name": "【高二】电磁感应", "sections": ["法拉第电磁感应定律", "楞次定律", "感应电动势", "自感与互感", "电磁感应综合"]},
            {"id": "wl-5", "name": "【高二】交变电流", "sections": ["交变电流产生", "描述交变电流", "变压器", "远距离输电"]},
        ]
    },
    "化学": {
        "icon": "🧪", "color": "#f59e0b",
        "chapters": [
            # 高一
            {"id": "hx-g1-1", "name": "【高一】物质的量", "sections": ["物质的量与摩尔", "摩尔质量", "气体摩尔体积", "物质的量浓度", "配制一定浓度溶液"]},
            {"id": "hx-g1-2", "name": "【高一】离子反应", "sections": ["电解质与非电解质", "电离方程式", "离子反应发生条件", "离子方程式书写", "离子共存"]},
            {"id": "hx-g1-3", "name": "【高一】氧化还原反应", "sections": ["氧化还原概念", "氧化剂与还原剂", "电子转移表示", "氧化还原配平", "常见氧化剂还原剂"]},
            {"id": "hx-g1-4", "name": "【高一】金属及其化合物", "sections": ["钠及其化合物", "铝及其化合物", "铁及其化合物", "金属冶炼"]},
            {"id": "hx-g1-5", "name": "【高一】非金属及其化合物", "sections": ["硅及其化合物", "氯及其化合物", "硫及其化合物", "氮及其化合物"]},
            {"id": "hx-g1-6", "name": "【高一】元素周期律", "sections": ["原子结构", "元素周期表", "元素周期律", "化学键", "分子间作用力"]},
            # 高二
            {"id": "hx-1", "name": "【高二】化学反应原理", "sections": ["化学反应速率", "化学平衡", "平衡常数", "等效平衡", "化学反应方向"]},
            {"id": "hx-2", "name": "【高二】水溶液中的离子反应", "sections": ["弱电解质电离", "水的电离", "盐类水解", "沉淀溶解平衡", "酸碱中和滴定"]},
            {"id": "hx-3", "name": "【高二】电化学", "sections": ["原电池", "电解池", "金属腐蚀与防护", "电化学计算"]},
            {"id": "hx-4", "name": "【高二】有机化学基础", "sections": ["烃类", "卤代烃", "醇酚醛酮", "羧酸与酯", "有机合成"]},
        ]
    },
    "生物": {
        "icon": "🧬", "color": "#06b6d4",
        "chapters": [
            {"id": "sw-1", "name": "遗传与进化", "sections": ["基因的本质", "基因的表达", "基因突变与重组", "染色体变异", "人类遗传病"]},
            {"id": "sw-2", "name": "生命活动的调节", "sections": ["神经调节", "体液调节", "免疫调节", "植物激素调节"]},
            {"id": "sw-3", "name": "种群和群落", "sections": ["种群特征", "种群数量变化", "群落结构", "群落演替"]},
            {"id": "sw-4", "name": "生态系统", "sections": ["生态系统结构", "能量流动", "物质循环", "信息传递", "生态系统稳定性"]},
        ]
    },
    "地理": {
        "icon": "🌏", "color": "#14b8a6",
        "chapters": [
            # 高一 必修一（自然地理）
            {"id": "dl-g1-1", "name": "【高一】地球的宇宙环境", "sections": ["天体系统", "太阳对地球的影响", "地球的圈层结构"]},
            {"id": "dl-g1-2", "name": "【高一】地球的运动", "sections": ["自转与公转", "昼夜交替与时差", "正午太阳高度", "昼夜长短变化", "四季与五带"]},
            {"id": "dl-g1-3", "name": "【高一】大气", "sections": ["大气受热过程", "热力环流", "大气水平运动", "气压带风带", "常见天气系统", "气候类型"]},
            {"id": "dl-g1-4", "name": "【高一】水循环与洋流", "sections": ["水循环过程", "河流特征", "洋流分布规律", "洋流对地理环境的影响"]},
            {"id": "dl-g1-5", "name": "【高一】地表形态", "sections": ["内力作用与地貌", "外力作用与地貌", "岩石圈物质循环", "河流地貌", "风成地貌"]},
            # 高一 必修二（人文地理）
            {"id": "dl-g1-6", "name": "【高一】人口", "sections": ["人口增长模式", "人口迁移", "人口合理容量"]},
            {"id": "dl-g1-7", "name": "【高一】城镇与乡村", "sections": ["城镇化进程", "城市空间结构", "城市问题与可持续发展"]},
            {"id": "dl-g1-8", "name": "【高一】产业区位", "sections": ["农业区位因素", "农业地域类型", "工业区位因素", "工业集聚与分散", "服务业区位"]},
            # 高二 选择性必修
            {"id": "dl-1", "name": "【高二】自然环境整体性与差异性", "sections": ["自然带分布", "垂直地域分异", "地方性分异", "自然环境整体性"]},
            {"id": "dl-2", "name": "【高二】资源、环境与国家安全", "sections": ["自然资源利用", "环境问题", "生态保护", "资源安全"]},
            {"id": "dl-3", "name": "【高二】区域发展", "sections": ["区域发展差异", "资源跨区域调配", "产业转移", "国际合作"]},
            {"id": "dl-4", "name": "【高二】交通运输", "sections": ["交通运输方式", "交通布局因素", "交通对区域发展的影响"]},
        ]
    },
}

# ── 名师视频资源（B站真实链接 · 指定UP主+官方平台） ──
VIDEO_RESOURCES = {
    "语文": [
        # 戴建业
        {"chapter": "古代诗歌阅读", "title": "【戴建业】14个字包含8层含义？杜甫的《登高》真的这么牛？", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1Fo4y1m7Da/", "teacher": "戴建业", "rating": 4.9},
        {"chapter": "古代诗歌阅读", "title": "【戴建业】《登高》的对仗，汉语形式美运用到出神入化", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1eb4y1f7e6/", "teacher": "戴建业", "rating": 4.9},
        {"chapter": "古代诗歌阅读", "title": "【戴建业】从陶渊明看中国人的生死观", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV15Y4y1S72B/", "teacher": "戴建业", "rating": 4.8},
        {"chapter": "古代诗歌阅读", "title": "【戴建业】李白精神的绝对自由·《梦游天姥吟留别》", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1QW4y1W75L/", "teacher": "戴建业", "rating": 4.9},
    ],
    "数学": [
        # 一数
        {"chapter": "导数及其应用", "title": "【一数】高中数学基础全集！奥数保送生主讲", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1VD4y1D7UB/", "teacher": "一数", "rating": 4.9},
        {"chapter": "导数及其应用", "title": "【一数】高中数学基础与解法全集", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV147411K7xu/", "teacher": "一数", "rating": 4.9},
        {"chapter": "圆锥曲线", "title": "【一数】圆锥曲线技巧大全！平移齐次+点乘双根+垂径定理", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1UXW4zNEBS/", "teacher": "一数", "rating": 4.9},
        {"chapter": "数列", "title": "【一数】120+拔高系统合集", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV14gu3zmEko/", "teacher": "一数", "rating": 4.8},
        # 李永乐
        {"chapter": "导数及其应用", "title": "【李永乐】高三数学复习100讲·函数", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1z441147P4/", "teacher": "李永乐", "rating": 4.9},
        {"chapter": "空间向量与立体几何", "title": "【李永乐】高三数学复习100讲·立体几何", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1V4411e7pA/", "teacher": "李永乐", "rating": 4.8},
        # 数学微课帮
        {"chapter": "导数及其应用", "title": "【数学微课帮】高中数学必修合集（第一册与第二册）", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV154411i7JS/", "teacher": "数学微课帮", "rating": 4.8},
        {"chapter": "圆锥曲线", "title": "【数学微课帮】高考数学专题复习（基础篇+提高篇）", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1bt411C7E8/", "teacher": "数学微课帮", "rating": 4.8},
    ],
    "英语": [
        # 英语兔
        {"chapter": "语法填空", "title": "【英语兔】英语语法精讲合集（全面、通俗、有趣）", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1XY411J7aG/", "teacher": "英语兔", "rating": 4.9},
        {"chapter": "语法填空", "title": "【英语兔】16种时态终极详解合集", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1Sv411y7d8/", "teacher": "英语兔", "rating": 4.9},
        {"chapter": "语法填空", "title": "【英语兔】所有英语从句，一个合集搞定！", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1764y1f7nq/", "teacher": "英语兔", "rating": 4.9},
        {"chapter": "阅读理解", "title": "【英语兔】一个视频说清整个英语语法体系", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1r54y1m7gd/", "teacher": "英语兔", "rating": 4.8},
        # 赖世雄
        {"chapter": "词汇积累", "title": "【赖世雄】48个英语音标朗读示范·美音英音对照", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1NZ4y187A5/", "teacher": "赖世雄", "rating": 4.8},
        {"chapter": "词汇积累", "title": "【赖世雄】自然拼读法（已完结45集）", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1XM411o7ZA/", "teacher": "赖世雄", "rating": 4.8},
        {"chapter": "写作", "title": "【赖世雄】如何学英语系列", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1jp411o7oo/", "teacher": "赖世雄", "rating": 4.7},
        # 阿滴英文
        {"chapter": "完形填空", "title": "【阿滴英文】30句让英文更生动的实用片语", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1Bh411k7VQ/", "teacher": "阿滴英文", "rating": 4.7},
        # 学而思
        {"chapter": "语法填空", "title": "【学而思】高三英语·从句复习·名词性从句重难点", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1K741187De/", "teacher": "学而思网校", "rating": 4.7},
        # 新东方
        {"chapter": "词汇积累", "title": "【新东方】高考必背单词秘籍", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1A7411p7vn/", "teacher": "新东方在线", "rating": 4.7},
    ],
    "物理": [
        # ── 选择性必修一（动量+振动+波） ──
        {"chapter": "【高二】电场", "title": "【跳跳学长】选修全系统课（动量+振动+波+电磁感应+交变电流）", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1qm4y1i7zf/", "teacher": "跳跳学长", "rating": 4.9},
        {"chapter": "【高二】电场", "title": "【2025新版】选择性必修一同步精讲·动量+振动+波", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1Z7twzdEkn/", "teacher": "名师精讲", "rating": 4.8},
        {"chapter": "【高二】电场", "title": "动量守恒本质·全模型动画演示·一看就懂", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1cajKzCEE9/", "teacher": "物理动画", "rating": 4.8},

        # ── 选择性必修二（电磁学·高考压轴核心） ──
        {"chapter": "【高二】电场", "title": "【全63集】选择性必修二精讲·安培力+电磁感应+交变电流+电磁波", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV17ZUaBCEnQ/", "teacher": "同步精讲", "rating": 4.9},
        {"chapter": "【高二】电场", "title": "【黄夫人】高中物理电学篇（新教材版）", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1ob411p7xr/", "teacher": "黄夫人", "rating": 4.9},
        {"chapter": "【高二】磁场", "title": "安培力、洛伦兹力和安培定则·难点突破", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1or4y1Q7Cb/", "teacher": "高二物理", "rating": 4.8},
        {"chapter": "【高二】电磁感应", "title": "【黄夫人】巧记物理公式合集", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1uh411J7ia/", "teacher": "黄夫人", "rating": 4.8},
        {"chapter": "【高二】电磁感应", "title": "【黄夫人】电磁感应系列·电容器运动学解题模板", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1vZ4y1x74H/", "teacher": "黄夫人", "rating": 4.8},
        {"chapter": "【高二】交变电流", "title": "【大宽物理】5分钟高中物理·远距离输电精讲", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1FW411W7xV/", "teacher": "大宽物理", "rating": 4.7},

        # ── 选择性必修三（热学+光+原子物理） ──
        {"chapter": "【高二】交变电流", "title": "高中物理选修3-3·分子动理论与热学合集", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV12E411w7PV/", "teacher": "物理合集", "rating": 4.7},

        # ── 高二电磁学基础 ──
        {"chapter": "【高二】电场", "title": "【跳跳学长】必修3系统课·库仑力平衡问题", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1VF411773F/", "teacher": "跳跳学长", "rating": 4.8},
        {"chapter": "【高二】恒定电流", "title": "【跳跳学长】必修3系统课·电流微观表达式", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1LN4y1M7Gg/", "teacher": "跳跳学长", "rating": 4.8},
        {"chapter": "【高二】恒定电流", "title": "【跳跳学长】必修3系统课·电源与电动势", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1CW4y117Rf/", "teacher": "跳跳学长", "rating": 4.8},
        {"chapter": "【高二】电场", "title": "【北京数字学校】高二物理第一学期合集", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1yt4y1S7qw/", "teacher": "北京数字学校", "rating": 4.7},

        # ── 高一基础 ──
        {"chapter": "曲线运动", "title": "【黄夫人】高中物理一轮复习·平抛运动（已完结）", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1b54y1r7LD/", "teacher": "黄夫人", "rating": 4.9},
        {"chapter": "交变电流", "title": "【北京数字学校】高中物理选修3-2·传感器", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV177411s7tm/", "teacher": "北京数字学校", "rating": 4.7},
    ],
    "化学": [
        # 真·凤舞九天
        {"chapter": "化学反应原理", "title": "【真·凤舞九天】疯狂化学系列·化学反应的魅力", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1Cx411i7em/", "teacher": "真·凤舞九天", "rating": 4.9},
        {"chapter": "元素周期律", "title": "【真·凤舞九天】疯狂化学2：元素奇迹", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1Xs411f7a6/", "teacher": "真·凤舞九天", "rating": 4.9},
        {"chapter": "电化学", "title": "【真·凤舞九天】如何打造爆款锂电池", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1yJ411a7kG/", "teacher": "真·凤舞九天", "rating": 4.8},
        {"chapter": "有机化学基础", "title": "【真·凤舞九天】疯狂化学1.5", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1dx411i7QW/", "teacher": "真·凤舞九天", "rating": 4.8},
        # 毕啸天/毕导
        {"chapter": "化学反应原理", "title": "【毕导】诺贝尔化学奖为何总颁给生物？", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1ti4y177SH/", "teacher": "毕啸天", "rating": 4.8},
        {"chapter": "元素周期律", "title": "【毕导】谁才是世界上最懒惰的惰性气体？", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1Q197YCEpi/", "teacher": "毕啸天", "rating": 4.8},
        {"chapter": "化学反应原理", "title": "【毕导】在这个简单问题上，你学的教材可能一直是错的", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1ZJ9CY4EzR/", "teacher": "毕啸天", "rating": 4.7},
        # 高途课堂
        {"chapter": "离子反应", "title": "【高途课堂】高一化学·离子反应（上）·吕子正", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV18U4y1n7tb/", "teacher": "高途课堂", "rating": 4.8},
        {"chapter": "氧化还原反应", "title": "【高途课堂】高一化学·离子反应+氧化还原反应·吕子正", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1AL411n7U3/", "teacher": "高途课堂", "rating": 4.8},
        {"chapter": "氧化还原反应", "title": "【高途课堂】高一化学·氧还性比较+配平·吕子正", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV18M4y1N7zy/", "teacher": "高途课堂", "rating": 4.7},
    ],
    "生物": [],
    "地理": [
        # 羊羊的地理教室
        {"chapter": "大气", "title": "【羊羊的地理教室】对流层大气的受热过程·超详细手绘讲解", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1iG4y1f73B/", "teacher": "羊羊的地理教室", "rating": 4.9},
        {"chapter": "地表形态", "title": "【羊羊的地理教室】潟湖还是泻湖？手绘动画讲解", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1Dp421m74C/", "teacher": "羊羊的地理教室", "rating": 4.9},
        {"chapter": "地表形态", "title": "【羊羊的地理教室】层理、节理、片理、解理一次说清", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV14f421e716/", "teacher": "羊羊的地理教室", "rating": 4.8},
        {"chapter": "水循环与洋流", "title": "【羊羊的地理教室】海水顶托/倒灌/入侵三秒分辨", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1yM4y1E7tt/", "teacher": "羊羊的地理教室", "rating": 4.8},
        # 高中地理老师-小7
        {"chapter": "地表形态", "title": "【小7老师】构造地貌的形成·褶皱与断层详解", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1a1xMevE54/", "teacher": "高中地理老师-小7", "rating": 4.8},
        {"chapter": "水循环与洋流", "title": "【小7老师】洋流分布规律与对地理环境的影响", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV19g41187d5/", "teacher": "高中地理老师-小7", "rating": 4.8},
        {"chapter": "地表形态", "title": "【小7老师】等高线地形图判读技巧", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1V44y1D7L3/", "teacher": "高中地理老师-小7", "rating": 4.8},
        {"chapter": "自然环境整体性与差异性", "title": "【小7老师】植被类型详解·热带雨林到苔原", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1W24y1y7da/", "teacher": "高中地理老师-小7", "rating": 4.7},
        {"chapter": "资源、环境与国家安全", "title": "【小7老师】生态脆弱区的综合治理", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1sv4y127yX/", "teacher": "高中地理老师-小7", "rating": 4.7},
        # 李说地理
        {"chapter": "地表形态", "title": "【李说地理】雅丹地貌与风积地貌·解题思路", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1wt4y1B7r9/", "teacher": "李说地理", "rating": 4.7},
        {"chapter": "水循环与洋流", "title": "【李说地理】堰塞湖与牛轭湖·地理名词辨析", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1T54y1W7p4/", "teacher": "李说地理", "rating": 4.7},
    ],
}
