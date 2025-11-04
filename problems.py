from utils import extract_csrf_token, extract_lentille_context, random_ua
from typing import Optional, Dict, Any
import httpx
import time
# import ddddocr
import getpass


def craw_probleminfo(problemid: str, cookies: dict | None = None) -> Dict[str, Any] | None:
    """
    爬取洛谷题目描述页面并提取题目信息。
    Such as : {'instance': 'main', 'template': 'problem.show', 'status': 200, 'locale': 'zh-CN', 'data': {'problem': {'pid': 'P1219', 'type': 'P', 'title': '[USACO1.5] 八皇后 Checker Challenge', 'difficulty': 3, 'tags': [4, 46, 127], 'wantsTranslation': False, 'totalSubmit': 363837, 'totalAccepted': 168706, 'flag': 5, 'provider': {'uid': 3, 'avatar': 'https://cdn.luogu.com.cn/upload/usericon/3.png', 'name': '洛谷', 'slogan': '', 'badge': None, 'isAdmin': True, 'isBanned': False, 'color': 'Purple', 'ccfLevel': 0, 'xcpcLevel': 0, 'background': ''}, 'contenu': {'name': '[USACO1.5] 八皇后 Checker Challenge', 'background': '', 'description': '一个如下的 $6 \\times 6$ 的跳棋棋盘，有六个棋子被放置在棋盘上，使得每行、每列有且只有一个，每条对角线（包括两条主对角线的所有平行线）上至多有一个棋子。\n\n![](https://cdn.luogu.com.cn/upload/image_hosting/3h71x0yf.png)\n\n上面的布局可以用序列 $2\\ 4\\ 6\\ 1\\ 3\\ 5$ 来描述，第 $i$ 个数字表示在第 $i$ 行的相应位置有一个棋子，如下：\n\n行号 $1\\ 2\\ 3\\ 4\\ 5\\ 6$\n\n列号 $2\\ 4\\ 6\\ 1\\ 3\\ 5$\n\n这只是棋子放置的一个解。请编一个程序找出所有棋子放置的解。  \n并把它们以上面的序列方法输出，解按字典顺序排列。  \n请输出前 $3$ 个解。最后一行是解的总个数。\n\n', 'formatI': '一行一个正整数 $n$，表示棋盘是 $n \\times n$ 大小的。\n\n', 'formatO': '前三行为前三个解，每个解的两个数字之间用一个空格隔开。第四行只有一个数字，表示解的总数。\n', 'hint': '【数据范围】  \n对于 $100\\%$ 的数据，$6 \\le n \\le 13$。\n\n题目翻译来自NOCOW。\n\nUSACO Training Section 1.5\n', 'locale': 'zh-CN'}, 'content': {'name': '[USACO1.5] 八皇后 Checker Challenge', 'background': '', 'description': '一个如下的 $6 \\times 6$ 的跳棋棋盘，有六个棋子被放置在棋盘上，使得每行、每列有且只有一个，每条对角线（包括两条主对角线的所有平行线）上至多有一个棋子。\n\n![](https://cdn.luogu.com.cn/upload/image_hosting/3h71x0yf.png)\n\n上面的布局可以用序列 $2\\ 4\\ 6\\ 1\\ 3\\ 5$ 来描述，第 $i$ 个数字表示在第 $i$ 行的相应位置有一个棋子，如下：\n\n行号 $1\\ 2\\ 3\\ 4\\ 5\\ 6$\n\n列号 $2\\ 4\\ 6\\ 1\\ 3\\ 5$\n\n这只是棋子放置的一个解。请编一个程序找出所有棋子放置的解。  \n并把它们以上面的序列方法输出，解按字典顺序排列。  \n请输出前 $3$ 个解。最后一行是解的总个数。\n\n', 'formatI': '一行一个正整数 $n$，表示棋盘是 $n \\times n$ 大小的。\n\n', 'formatO': '前三行为前三个解，每个解的两个数字之间用一个空格隔开。第四行只有一个数字，表示解的总数。\n', 'hint': '【数据范围】  \n对于 $100\\%$ 的数据，$6 \\le n \\le 13$。\n\n题目翻译来自NOCOW。\n\nUSACO Training Section 1.5\n', 'locale': 'zh-CN'}, 'attachments': [], 'showScore': True, 'acceptSolution': False, 'acceptLanguages': [5, 1, 2, 28, 3, 4, 11, 12, 27, 34, 7, 25, 8, 33, 15, 14, 19, 30, 31, 32, 21, 22, 17, 9, 16, 13, 23], 'samples': [['6\n', '2 4 6 1 3 5\n3 6 2 5 1 4\n4 1 5 2 6 3\n4\n']], 'limits': {'time': [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000], 'memory': [128000, 128000, 128000, 128000, 128000, 128000, 128000, 128000]}, 'translation': ''}, 'translations': {'zh-CN': {'name': '[USACO1.5] 八皇后 Checker Challenge', 'background': '', 'description': '一个如下的 $6 \\times 6$ 的跳棋棋盘，有六个棋子被放置在棋盘上，使得每行、每列有且只有一个，每条对角线（包括两条主对角线的所有平行线）上至多有一个棋子。\n\n![](https://cdn.luogu.com.cn/upload/image_hosting/3h71x0yf.png)\n\n上面的布局可以用序列 $2\\ 4\\ 6\\ 1\\ 3\\ 5$ 来描述，第 $i$ 个数字表示在第 $i$ 行的相应位置有一个棋子，如下：\n\n行号 $1\\ 2\\ 3\\ 4\\ 5\\ 6$\n\n列号 $2\\ 4\\ 6\\ 1\\ 3\\ 5$\n\n这只是棋子放置的一个解。请编一个程序找出所有棋子放置的解。  \n并把它们以上面的序列方法输出，解按字典顺序排列。  \n请输出前 $3$ 个解。最后一行是解的总个数。\n\n', 'formatI': '一行一个正整数 $n$，表示棋盘是 $n \\times n$ 大小的。\n\n', 'formatO': '前三行为前三个解，每个解的两个数字之间用一个空格隔开。第四行只有一个数字，表示解的总数。\n', 'hint': '【数据范围】  \n对于 $100\\%$ 的数据，$6 \\le n \\le 13$。\n\n题目翻译来自NOCOW。\n\nUSACO Training Section 1.5\n', 'locale': 'zh-CN'}}, 'bookmarked': False, 'contest': None, 'vjudgeUsername': None, 'lastLanguage': None, 'lastCode': '', 'lastCodeAt': None, 'recommendations': [{'pid': 'P1019', 'type': 'P', 'title': '[NOIP 2000 提高组] 单词接龙（疑似错题）', 'difficulty': 3}, {'pid': 'P1135', 'type': 'P', 'title': '奇怪的电梯', 'difficulty': 3}, {'pid': 'P1443', 'type': 'P', 'title': '马的遍历', 'difficulty': 3}, {'pid': 'P1605', 'type': 'P', 'title': '迷宫', 'difficulty': 2}, {'pid': 'P2392', 'type': 'P', 'title': 'kkksc03考前临时抱佛脚', 'difficulty': 2}], 'forum': {'name': 'P1219 [USACO1.5] 八皇后 Checker Challenge', 'type': 2, 'slug': 'P1219', 'color': 'orange-3'}, 'discussions': [{'id': 1189218, 'title': '警示后人，警钟敲烂', 'author': {'uid': 1708097, 'avatar': 'https://cdn.luogu.com.cn/upload/usericon/1708097.png', 'name': 'Zhengbeichen', 'slogan': '“若管理与我斗，就斗到至死方休，管它是坎还是沟，我不知天高地厚。”', 'badge': None, 'isAdmin': False, 'isBanned': False, 'color': 'Green', 'ccfLevel': 0, 'xcpcLevel': 0, 'background': ''}, 'time': 1762052303}, {'id': 1187018, 'title': '没过样例求帮', 'author': {'uid': 1091106, 'avatar': 'https://cdn.luogu.com.cn/upload/usericon/1091106.png', 'name': 'lemon8932', 'slogan': '泪水打湿DVE C，G Bond誓要拿AC', 'badge': None, 'isAdmin': False, 'isBanned': False, 'color': 'Blue', 'ccfLevel': 0, 'xcpcLevel': 0, 'background': ''}, 'time': 1761917134}, {'id': 1186969, 'title': '求帮办', 'author': {'uid': 1091106, 'avatar': 'https://cdn.luogu.com.cn/upload/usericon/1091106.png', 'name': 'lemon8932', 'slogan': '泪水打湿DVE C，G Bond誓要拿AC', 'badge': None, 'isAdmin': False, 'isBanned': False, 'color': 'Blue', 'ccfLevel': 0, 'xcpcLevel': 0, 'background': ''}, 'time': 1761916260}, {'id': 1181723, 'title': '0分求调', 'author': {'uid': 1704379, 'avatar': 'https://cdn.luogu.com.cn/upload/usericon/1704379.png', 'name': 'maibohan123', 'slogan': '大鹏一日同风起，扶摇直上九万里', 'badge': None, 'isAdmin': False, 'isBanned': False, 'color': 'Green', 'ccfLevel': 0, 'xcpcLevel': 0, 'background': ''}, 'time': 1761472212}, {'id': 1181568, 'title': '求助，74分wa最后2点', 'author': {'uid': 1647538, 'avatar': 'https://cdn.luogu.com.cn/upload/usericon/1647538.png', 'name': 'zq111111', 'slogan': '', 'badge': None, 'isAdmin': False, 'isBanned': False, 'color': 'Green', 'ccfLevel': 0, 'xcpcLevel': 0, 'background': ''}, 'time': 1761463493}, {'id': 1178295, 'title': '求助', 'author': {'uid': 1630890, 'avatar': 'https://cdn.luogu.com.cn/upload/usericon/1630890.png', 'name': 'wjf131227', 'slogan': '他连自己的死亡都是精心策划的......', 'badge': None, 'isAdmin': False, 'isBanned': False, 'color': 'Blue', 'ccfLevel': 0, 'xcpcLevel': 0, 'background': ''}, 'time': 1761132668}], 'locale': 'zh-CN', 'canEdit': False}, 'user': None, 'time': 1762238838.786272, 'theme': None}
    """
    with httpx.Client(headers={"user-agent": random_ua()},
                      cookies=cookies,
                      follow_redirects=True) as client:
        response = client.get(f"https://www.luogu.com.cn/problem/{problemid}")
        response.raise_for_status()
        return extract_lentille_context(response.text)

def craw_statement(problemid: str, cookies: dict | None = None) -> Dict[str, Any] | None:
    """
    爬取洛谷题目描述页面并提取题目描述的内容。
    
    返回格式如：
    {'background' : '题目背景',
     'description' : '题目描述',
     'input' : '输入格式',
     'output' : '输出格式',
     'samples' : [['输入样例1', '输出样例1'], ['输入样例2', '输出样例2']],
     'hint' : '题目提示',
     'attachments' : [{'filename': '附件文件名', 'url': '附件下载链接'}, ...],
     'locale' : '题目语言',
     'translation' : '题目翻译内容',
     'provider' : '题目提供者UID',
     'tags': [题目标签ID列表],
     'title': '题目标题',
     'difficulty': 题目难度系数,
    }

    失败时返回 None。
    """
    probleminfo = craw_probleminfo(problemid, cookies)
    if probleminfo is None:
        return None
    statement = {
                    'background' : probleminfo['data']['problem']['content']['background'],
                    'description' : probleminfo['data']['problem']['content']['description'], 
                    'input' : probleminfo['data']['problem']['content']['formatI'], 
                    'output' : probleminfo['data']['problem']['content']['formatO'], 
                    'samples' : probleminfo['data']['problem']['samples'],
                    'hint' : probleminfo['data']['problem']['content']['hint'],
                    'attachments' : probleminfo['data']['problem']['attachments'],
                    'locale' : probleminfo['data']['problem']['content']['locale'],
                    'translation' : probleminfo['data']['problem']['translation'],
                    'provider' : probleminfo['data']['problem']['provider']['uid'],
                    'tags': probleminfo['data']['problem']['tags'],
                    'title': probleminfo['data']['problem']['title'],
                    'difficulty': probleminfo['data']['problem']['difficulty'],
               }
    return statement

# print(craw_statement("P12198"))
