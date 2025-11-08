from utils import *
from typing import Optional, Dict, Any
import httpx

def __craw_article(id: str, cookies: dict | None = None) -> Dict[str, Any] | None:
    """爬取文章页面的 lentille-context 数据"""
    # {'instance': 'main', 'template': 'article.show', 'status': 200, 'locale': 'zh-CN', 'data': {'article': {'lid': 'v25cxsdj', 'title': '【欢迎投稿】有奖征集 OI 小知识点，技巧和思考题，包括“广为人知”但大纲未收录的内容！', 'time': 1762512066, 'author': {'uid': 40607, 'avatar': 'https://cdn.luogu.com.cn/upload/usericon/40607.png', 'name': 'CommonAnts', 'slogan': '蔡德仁 - Σ*Studio', 'badge': None, 'isAdmin': False, 'isBanned': False, 'color': 'Orange', 'ccfLevel': 10, 'xcpcLevel': 0, 'background': ''}, 'upvote': 62, 'replyCount': 36, 'favorCount': 25, 'category': 4, 'status': 2, 'solutionFor': None, 'promoteStatus': 2, 'collection': None, 'content': '# 有奖征集 OI 小知识点，技巧和思考题，包括“广为人知”但大纲未收录的内容！\n\n## 让所有重要的知识和技巧都“广为人知”，让所有偏门、鸡肋的知识和技巧都“物尽其用”。\n\n## 投稿：发送至 1525887403@qq.com 并同时回复本帖\n\n## 本文在 [LibreOJ](https://loj.ac/d/4787) 最新，不过所有平台均接受投稿！\n\n## 核心规则\n\n### 总述\n\n有奖征集 OI 中大纲未收录的**小知识，套路，技巧和思考题**！包括你觉得“**广为人知**”或者**不为人知**但**大纲里没有**的内容！\n\n> **让所有重要的知识和技巧和你的优秀笔记都被推荐“广为人知”，让所有偏门、鸡肋的知识和技巧都作为思考题“物尽其用”。**\n\n征集范围为公开资料，可以**直接推荐网络公开资料**，也可进一步提供相关的**笔记介绍、优质课件、例题、思考题**等。撰写详细公开资料者以及发明/引入人有**更多奖励**。\n\n同一知识的**推荐奖励先到先得**。但对于详细公开资料**作者**，只要有新内容就有奖励，不受他人推荐影响。对于发明/引入人，奖励不受影响。\n\n对于那些太细节/偏/杂/不实用的知识，可以造**思考题**。思考题分为 NOIP+ 和 NOI 两档难度，均有更高奖励。思考题比较类似大学算法课的思考题讨论，每个思考题围绕一个技巧/数学概念/动机等小套路展开，用于补足编程题不易表达的内容。**[思考题的例子可以参考：www.luogu.com.cn/article/voqbr1ef](https://www.luogu.com.cn/article/voqbr1ef)**\n\n> **奖励内容为 现金+等额“星尘”**（贡献分），会展示“星尘”前几名排行榜，可以选择匿名。多次贡献的同学可以**加入在线文档和群**方便查重交流。\n>\n> - 知识公开介绍**推荐**：最高 **160** 每个。\n> - 知识公开介绍**作者**：最高 **320** 每个。\n> - 思考题**作者**：最高 **1024** 每个。\n> - 知识**发明/引入者**：最高 **2048** 每个。\n\n**鼓励投稿内容的投稿者自行公开传播其知识和文章。** 去其它地方**有偿**投稿相同内容（有偿一稿多投）须事先明确告知双方并取得同意。\n\n收集的知识列表会**公开展示**（审核、整理、展示等可能有延迟）。\n\n收集的投稿内容会用在**教材，题单，资源推荐**等类型的**公开项目**，**同时**也会用于**训练课程**。\n\n### 联系方式\n\n1. **同时**将**详细内容/链接等**及您的**个人身份**发送到投稿**邮箱**：\n    - **【邮箱暂定：1525887403@qq.com】** 以后可能有更新，请关注本帖（本邮箱仍有效）。\n    - 您的**网名**，用于贡献榜展示，可以注明匿名。\n    - 您的 **[OIerDB](https://oier.baoshuo.dev/)** 个人页面，如果没有，可以写真实姓名+出生年份。用于发奖励。\n    - 您的一个 **QQ号**，以便验证身份和后续沟通。\n    - 您的个人信息不会被公开或传播给他人，除了贡献榜展示的网名外。\n    - 您可以不提供个人信息，但没有信息将无法发奖励。\n    - **即使您已经回复了本帖评论区也要发邮件**。投稿时间以**邮件**首次发送完整内容的时间为准，细节可以后续勘误补充。\n2. 直接将**小知识推荐和你的介绍/例题链接**回复到本帖评论区。\n3. 我们会用**邮箱**回复您的投稿。\n4. 可以加入蔡德仁的 OI 教研群**催促鸽子**审核：**群 QQ 435253885**\n5. “星尘”（贡献分）达到 **300** 可加入征集**讨论群 QQ 1061507046**以及**在线文档**，便于讨论。\n\n### 征集内容\n\n在 OI 中的**小知识**，即常说的**套路、技巧[tricks]**，和相关的**笔记介绍、例题、思考题**等。\n\n- 作为核心难点**能出 $\\ge 2$ 道不同 OI 题目**的算法技巧、组合结构、数学模型、经典结论、算法方法等各种均为征集范围。\n- 不能是 NOI 大纲或大纲辞典明确收录过的内容。\n- 必须 OI 可做，不能过于偏/难，至少集训队得有几个人会或能立刻学会。\n- **NOI 及以下难度的优先**。\n\n### 征集形式\n\n#### 一、小知识推荐\n\n- 必须提供：**较详细的介绍；或公开的介绍博客/资料链接。可以推荐其它人写的内容！**\n- 可选提供：**例题**（需提供 题目来源链接或题意+题解）\n- 奖励：单个知识最高 **160**。\n    - **64**（基础介绍）+**32**×（每道**不同例题**）\n- 已有人推荐过的知识不计奖励，**新例题仍计**。**先到先得**。\n\n#### 二、详细笔记\n\n- 必须提供：**本人撰写的一篇较详细的公开介绍博客/课件/资料**，必须包含知识的详细介绍、思想、典型应用以及至少一道例题及题解。\n- 奖励：单个知识最高 **320**。\n    - 基础 **160**。如果是**第一个**投稿该知识的详细笔记，则奖励至 **320**。\n- 可以投稿在本活动开始之前创作的内容，但必须是本人撰写。\n- 重复知识，必须包含相对之前投稿的新内容。**先到先得**。\n\n#### 三、思考题\n\n- 对于那些太细节/偏/杂/不实用的套路，可以用来造思考题。\n- 必须提供：思考题的详细题面和解答，以及核心知识。\n- 奖励：NOI难度 **1024**，NOIP+ 难度 **512**。\n- 建议造之前先说思路，防止撞前面的题。知识重复但仍有新内容的，奖励 **256**。**先到先得**。\n- **[思考题的例子可以参考：www.luogu.com.cn/article/voqbr1ef](https://www.luogu.com.cn/article/voqbr1ef)**\n\n#### 四、发明/引入人奖励（特殊）\n\n- 必须提供：该知识的详细介绍资料/链接。以及本人作为该知识**发明人/OI 首先引入人**的身份和初期资料。\n- 奖励：NOI 及以下难度 **2048**，更高难度 **1280**。\n- 发明/引入人奖励对大纲/经典教材收录的内容**仍然有效**。\n\n### “星尘”（贡献分）\n\n**1奖励 = ￥1 + 1“星尘”（贡献分）**\n\n想要多参与的同学，“星尘”（贡献分）达到 **300** 后，可以加入在线文档和讨论群，快速查重交流。\n\n### 其它\n- 如果你想推荐**具体代码写法**，请转[代码细节征集](https://loj.ac/d/4781)\n- 如果你想推荐**比赛注意事项**，请转[比赛注意事项](https://loj.ac/d/4782)\n- 如果你想推荐**小资源**，请转[小资源合集](https://loj.ac/d/4774)\n- 如果你想推荐**其它公开资源**，请转[网络资源推荐](https://loj.ac/d/4775)\n\n## 细则\n\n- 在 OI 中的**小知识**，即常说的**套路、技巧[tricks]**，和相关的**笔记介绍、例题、思考题**想法等。具体范围如下：\n    - 作为核心难点**能出 $\\ge 2$ 道不同 OI 题目**的算法技巧、组合结构、数学模型、经典结论、算法方法等各种均为征集范围。\n        - 例子：bfs求常数边权最短路；贪心的邻项合并；单侧递归线段树；min-max 容斥；颜色段均摊；析合树；斜二进制倍增；分散层叠的多序列二分；01原理的排序分析；下标-值域-时间换维在数据结构上的应用；均摊分步化；折线图法分析括号序列和01序列；压位分块（四毛子在特定问题上的实现优化）；Bostan-Mori；最优化推式子技巧（例如 $\\max(\\lvert x\\rvert)=\\max(\\max(x,-x))$）；完全图zig-zag构造技巧；基于 Farey 序列的 $O(1)$ 在线查询逆元；矩阵乘法的常见 OI 归约；……\n        - 下至 **CSP-J** 上至 **NOI+** 难度都可以！\n        - **这些已列出的例子如果你能提供好的例题，仍然有奖！**\n    - 不能是《NOI 大纲》《NOI 大纲辞典》明确收录过的内容\n        - 你也可以投稿其它教材目录提到过的内容！\n        - 例外情况：如果是作者/引入者本人领奖，不受限制。\n    - 必须 OI 可做：\n        - 必须是算法/计算机内容且能出 OI 题。\n        - 不能是 OI 未引入过的偏僻论文、科技。（大致标准：假设给现役集训队统一讲解该知识 5 分钟，然后出 OI 题单独作为集训队测试，能有 4 人以上在 5 小时内 AC。）\n        - 优先征集 NOI 难度以内可考的知识。\n- 奖励：\n    - 一、小知识推荐\n        - 之前有人推荐过的知识不计奖励。\n        - 之前有人推荐过该知识，但你提供了新的例题的，只计算新的例题奖励。题意足够类似的例题算一道。仍然受单个知识上限限制。\n    - 二、详细笔记\n        - 可以投稿在本活动开始之前创作的内容，但必须是本人撰写。\n        - 如果是重复知识投稿，必须包含相对之前投稿的新内容才计算奖励，如更易懂的解释，新的理解视角，或新的例题。\n        - 同一人只能对同一知识奖励一次。\n    - 三、思考题\n        - 同一人只能对同一知识奖励一次。\n    - 四、发明/引入人奖励\n        - 发明人和引入人是不同人的，独立计算奖励。\n        - 发明人或引入人是多人共同的，共同计算奖励。\n        - 同一人只能对同一知识奖励一次。\n\n> 个人著作权声明：严禁任何未经本人（刘承奥，常用笔名/网名：蔡德仁 CommonAnts LCA liu_cheng_ao）书面授权者在梦熊联盟，或者任何虚假宣传或不实营销炒作或不正当竞争行为严重的 OI 机构的课程内或交流平台（包括但不限于品牌集训线下讨论，交流群，OJ，公众号，视频号等）上引用、传播、讨论此内容，以及本人于2024年5月及之后发布的所有内容，包括声明为公开的内容在内。\n>\n> **之前已发布的本文草稿内容：[https://www.luogu.me/paste/gzsaf4gu](https://www.luogu.me/paste/gzsaf4gu)**\n>\n> 2024年及更早的**本人同类计划：[https://pqsyrcnk3fo.feishu.cn/wiki/Xk79wgM8uiBQGRk6x6TcueXznaf](https://pqsyrcnk3fo.feishu.cn/wiki/Xk79wgM8uiBQGRk6x6TcueXznaf)**\n>\n> **坚决反对打着“公共资源”旗号鼓吹“稀缺性”，妄图商业垄断的行为！**\n>\n> **坚决反对打着“公共资源”旗号进行商业炒作营销，剽窃公开资源开设付费课程坑骗家长和学生的行为！**\n>\n> 坚决反对与虎谋皮，以营销炒作的方式“推广知识”，破坏社区秩序的行为！\n>\n> 坚决反对通过向部分不懂算法的家长/教练危言耸听，吹嘘特定知识重要性，强迫学生学习，破坏教学秩序的行为！\n>\n> **坚决支持建设高质量公开资料推荐平台和刊物平台！**', 'contentFull': True, 'adminNote': None}, 'favored': False, 'voted': None, 'canReply': False, 'canEdit': False}, 'user': None, 'time': 1762575981.464822, 'theme': None}
    with httpx.Client(headers={"user-agent": random_ua()},
                      cookies=cookies,
                      follow_redirects=True) as client:
        response = client.get(f"https://www.luogu.com/article/{id}")
        response.raise_for_status()
        # print(response.text)
        return extract_lentille_context(response.text)
    
def craw_article(id: str, cookies: dict | None = None) -> Dict[str, Any] | None:
    """爬取文章页面的信息"""
    result = __craw_article(id, cookies)
    if result is None:
        return None
    try:
        payload = {
            "title": result["data"]["article"]["title"],
            "author": result["data"]["article"]["author"]["uid"],
            "time": result["data"]["article"]["time"],
            "content": result["data"]["article"]["content"],
            "title": result["data"]["article"]["title"]
        }
    except KeyError:
        return None
    return payload

def _craw_paste(id: str, cookies: dict | None = None) -> Dict[str, Any] | None:
    """爬取 Paste 页面的信息"""
    #{'code': 200, 'currentTemplate': 'PasteShow', 'currentData': {'paste': {'id': '1t4zskm7', 'user': {'uid': 1010774, 'avatar': 'https://cdn.luogu.com.cn/upload/usericon/1010774.png', 'name': 'liveless', 'slogan': '青天白日闪耀全世界 | linux.do liveless | 3673398763', 'badge': None, 'isAdmin': False, 'isBanned': False, 'color': 'Orange', 'ccfLevel': 0, 'xcpcLevel': 0, 'background': 'https://cdn.luogu.com.cn/upload/image_hosting/i1ct5rjs.png'}, 'time': 1760700337, 'public': True, 'data': 'lgs_register_verification'}, 'canEdit': False}, 'currentTitle': '云剪贴板', 'currentTheme': None, 'currentUser': None, 'currentTime': 1762576415}
    with httpx.Client(headers={"user-agent": random_ua()},
                      cookies=cookies,
                      follow_redirects=True) as client:
        response = client.get(f"https://www.luogu.com/paste/{id}")
        response.raise_for_status()
        return extract_and_parse_fe_injection_regex(response.text)
    
def craw_paste(id: str, cookies: dict | None = None) -> Dict[str, Any] | None:
    """爬取 Paste 页面的信息"""
    result = _craw_paste(id, cookies)
    if result is None:
        return None
    try:
        payload = {
            "data": result["currentData"]["paste"]["data"],
            "author": result["currentData"]["paste"]["user"]["uid"],
            "time": result["currentData"]["paste"]["time"],
            "public": result["currentData"]["paste"]["public"],
        }
    except KeyError:
        return None
    return payload