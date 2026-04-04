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


# ── 高二科目与章节体系 ──
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
            {"id": "wl-1", "name": "电场", "sections": ["库仑定律", "电场强度", "电势与电势能", "电容器", "带电粒子运动"]},
            {"id": "wl-2", "name": "恒定电流", "sections": ["欧姆定律", "电阻定律", "串并联电路", "电功与电功率", "闭合电路欧姆定律"]},
            {"id": "wl-3", "name": "磁场", "sections": ["磁场基础", "安培力", "洛伦兹力", "带电粒子在磁场中运动", "复合场"]},
            {"id": "wl-4", "name": "电磁感应", "sections": ["法拉第电磁感应定律", "楞次定律", "感应电动势", "自感与互感", "电磁感应综合"]},
            {"id": "wl-5", "name": "交变电流", "sections": ["交变电流产生", "描述交变电流", "变压器", "远距离输电"]},
        ]
    },
    "化学": {
        "icon": "🧪", "color": "#f59e0b",
        "chapters": [
            {"id": "hx-1", "name": "化学反应原理", "sections": ["化学反应速率", "化学平衡", "平衡常数", "等效平衡", "化学反应方向"]},
            {"id": "hx-2", "name": "水溶液中的离子反应", "sections": ["弱电解质电离", "水的电离", "盐类水解", "沉淀溶解平衡", "酸碱中和滴定"]},
            {"id": "hx-3", "name": "电化学", "sections": ["原电池", "电解池", "金属腐蚀与防护", "电化学计算"]},
            {"id": "hx-4", "name": "有机化学基础", "sections": ["烃类", "卤代烃", "醇酚醛酮", "羧酸与酯", "有机合成"]},
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
            {"id": "dl-1", "name": "自然地理", "sections": ["地球运动", "大气环流", "天气系统", "气候类型", "水循环与洋流"]},
            {"id": "dl-2", "name": "地表形态", "sections": ["内力作用", "外力作用", "河流地貌", "风成地貌", "海岸地貌"]},
            {"id": "dl-3", "name": "自然环境整体性与差异性", "sections": ["自然带分布", "垂直地域分异", "地方性分异", "自然环境整体性"]},
            {"id": "dl-4", "name": "人口与城市", "sections": ["人口增长模式", "人口迁移", "城市化", "城市空间结构", "城市问题"]},
            {"id": "dl-5", "name": "农业与工业", "sections": ["农业区位因素", "农业地域类型", "工业区位因素", "工业集聚与分散"]},
            {"id": "dl-6", "name": "交通与区域发展", "sections": ["交通运输方式", "交通布局", "区域发展差异", "资源跨区域调配"]},
        ]
    },
}

# ── 名师视频资源（B站真实链接） ──
VIDEO_RESOURCES = {
    "数学": [
        {"chapter": "导数及其应用", "title": "「导数」一课通！1h零基础上手", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1iZ421y71z/", "teacher": "一数", "rating": 4.9},
        {"chapter": "导数及其应用", "title": "从零开始1.3小时掌握导数全部知识点", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1Ff4y1d7i7/", "teacher": "数学名师", "rating": 4.8},
        {"chapter": "圆锥曲线", "title": "【圆锥曲线大题】入门到入土，所有题型全面梳理", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1GgZUYCEHu/", "teacher": "zzk与数", "rating": 4.9},
        {"chapter": "圆锥曲线", "title": "圆锥曲线椭圆篇·焦点三角形内切圆常考结论", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1US4FzAEeD/", "teacher": "赵礼显老师", "rating": 4.8},
    ],
    "物理": [
        {"chapter": "电场", "title": "电场强度知识总结｜坤哥物理", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1c841197Bd/", "teacher": "坤哥物理", "rating": 4.9},
        {"chapter": "电场", "title": "静电感应现象与静电平衡｜坤哥物理", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV188411Q7xY/", "teacher": "坤哥物理", "rating": 4.8},
        {"chapter": "磁场", "title": "磁感应强度 高中物理选修3-1《磁场》", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1y741157e4/", "teacher": "物理名师", "rating": 4.8},
        {"chapter": "磁场", "title": "安培力作用下的平衡·运动问题：从入门到精通", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV14M411k7Lf/", "teacher": "物理名师", "rating": 4.7},
        {"chapter": "电磁感应", "title": "电磁感应现象+磁通量｜高二物理", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV16KsnzKE4F/", "teacher": "物理名师", "rating": 4.8},
        {"chapter": "电磁感应", "title": "高中物理《电磁感应专题》最全考点串讲", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1fW4y137SY/", "teacher": "物理名师", "rating": 4.9},
    ],
    "化学": [
        {"chapter": "化学反应原理", "title": "【化学平衡】化学平衡状态｜0基础开始学起", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1P34y1n7tS/", "teacher": "化学名师", "rating": 4.8},
        {"chapter": "化学反应原理", "title": "【化学平衡】化学平衡常数｜0基础愉快学习", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1SF411P7Qk/", "teacher": "化学名师", "rating": 4.7},
        {"chapter": "电化学", "title": "【核心技巧】电极反应方程式书写，4步搞定", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1AC4y127tR/", "teacher": "小球老师讲化学", "rating": 4.9},
        {"chapter": "电化学", "title": "高中化学——选修4·电化学基础", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1Bs411p7WG/", "teacher": "化学名师", "rating": 4.7},
        {"chapter": "有机化学基础", "title": "高中化学选修5《有机化学基础》", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1ct4y1y78W/", "teacher": "化学名师", "rating": 4.8},
        {"chapter": "有机化学基础", "title": "2h速通高考有机！手把手搞定有机大题", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1em4y167eM/", "teacher": "玉龍YULONG", "rating": 4.9},
    ],
    "英语": [
        {"chapter": "阅读理解", "title": "【高中英语】阅读开挂！4+2刷分模式6分钟解决阅读难题", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV12G411f7XE/", "teacher": "龙坚-中高考英语", "rating": 4.8},
        {"chapter": "阅读理解", "title": "高考英语阅读理解技巧精讲（纯干货）", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1ME411Y7Ec/", "teacher": "英语名师", "rating": 4.7},
    ],
    "语文": [
        {"chapter": "古代诗歌阅读", "title": "高中语文【诗歌鉴赏】专题详解", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1M44y1y7qB/", "teacher": "语文名师", "rating": 4.8},
        {"chapter": "古代诗歌阅读", "title": "一个视频学会诗歌鉴赏：分析表达技巧与语言风格", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1iM4m1U7Sw/", "teacher": "语文名师", "rating": 4.7},
    ],
    "生物": [],
    "地理": [
        {"chapter": "自然地理", "title": "【高中地理】10分钟搞定气压带和风带的形成及移动", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1Ji4y1L7r3/", "teacher": "老吕高中地理", "rating": 4.9},
        {"chapter": "自然地理", "title": "气压带与风带之三圈环流·分布和季节移动", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1if4y1m7B4/", "teacher": "小郑老师", "rating": 4.8},
        {"chapter": "地表形态", "title": "高中地理必修一·常见地貌类型（喀斯特地貌）", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1Nv4y1R7oC/", "teacher": "地理名师", "rating": 4.7},
        {"chapter": "地表形态", "title": "高中地理：雅丹地貌与风积地貌", "platform": "bilibili", "url": "https://www.bilibili.com/video/BV1wt4y1B7r9/", "teacher": "地理名师", "rating": 4.7},
    ],
}
