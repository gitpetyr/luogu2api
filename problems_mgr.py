from utils import *
from typing import Optional, Dict, Any
import httpx
import time
import ddddocr

ocr = ddddocr.DdddOcr(show_ad=False, beta=True)

languages_map = {
    'Pascal': 1, # Accept O2
    'C': 2, # Accept O2
    'C++14 (GCC 9)': 28, # Accept O2
    'C++98': 3, # Accept O2
    'C++11': 4, # Accept O2
    'C++14': 11, # Accept O2
    'C++17': 12, # Accept O2
    'C++20': 27, # Accept O2
    'C++23': 34, # Accept O2
    'Python 3': 7,
    'PyPy 3': 25,
    'Java 8': 8,
    'Java 21': 33,
    'Rust': 15,
    'Go': 14,
    'Haskell': 19,
    'OCaml': 30,
    'Julia': 31,
    'Lua': 32,
    'Kotlin/JVM': 21,
    'Scala': 22,
    'C# Mono': 17,
    'Node.js LTS': 9,
    'PHP': 16,
    'Ruby': 13,
    'Perl': 23
}

def craw_probleminfo(problemid: str, cookies: dict | None = None) -> Dict[str, Any] | None:
    """
    爬取洛谷题目描述页面并提取题目信息。
    """
    # Such as : {'instance': 'main', 'template': 'problem.show', 'status': 200, 'locale': 'zh-CN', 'data': {'problem': {'pid': 'P1219', 'type': 'P', 'title': '[USACO1.5] 八皇后 Checker Challenge', 'difficulty': 3, 'tags': [4, 46, 127], 'wantsTranslation': False, 'totalSubmit': 363837, 'totalAccepted': 168706, 'flag': 5, 'provider': {'uid': 3, 'avatar': 'https://cdn.luogu.com.cn/upload/usericon/3.png', 'name': '洛谷', 'slogan': '', 'badge': None, 'isAdmin': True, 'isBanned': False, 'color': 'Purple', 'ccfLevel': 0, 'xcpcLevel': 0, 'background': ''}, 'contenu': {'name': '[USACO1.5] 八皇后 Checker Challenge', 'background': '', 'description': '一个如下的 $6 \\times 6$ 的跳棋棋盘，有六个棋子被放置在棋盘上，使得每行、每列有且只有一个，每条对角线（包括两条主对角线的所有平行线）上至多有一个棋子。\n\n![](https://cdn.luogu.com.cn/upload/image_hosting/3h71x0yf.png)\n\n上面的布局可以用序列 $2\\ 4\\ 6\\ 1\\ 3\\ 5$ 来描述，第 $i$ 个数字表示在第 $i$ 行的相应位置有一个棋子，如下：\n\n行号 $1\\ 2\\ 3\\ 4\\ 5\\ 6$\n\n列号 $2\\ 4\\ 6\\ 1\\ 3\\ 5$\n\n这只是棋子放置的一个解。请编一个程序找出所有棋子放置的解。  \n并把它们以上面的序列方法输出，解按字典顺序排列。  \n请输出前 $3$ 个解。最后一行是解的总个数。\n\n', 'formatI': '一行一个正整数 $n$，表示棋盘是 $n \\times n$ 大小的。\n\n', 'formatO': '前三行为前三个解，每个解的两个数字之间用一个空格隔开。第四行只有一个数字，表示解的总数。\n', 'hint': '【数据范围】  \n对于 $100\\%$ 的数据，$6 \\le n \\le 13$。\n\n题目翻译来自NOCOW。\n\nUSACO Training Section 1.5\n', 'locale': 'zh-CN'}, 'content': {'name': '[USACO1.5] 八皇后 Checker Challenge', 'background': '', 'description': '一个如下的 $6 \\times 6$ 的跳棋棋盘，有六个棋子被放置在棋盘上，使得每行、每列有且只有一个，每条对角线（包括两条主对角线的所有平行线）上至多有一个棋子。\n\n![](https://cdn.luogu.com.cn/upload/image_hosting/3h71x0yf.png)\n\n上面的布局可以用序列 $2\\ 4\\ 6\\ 1\\ 3\\ 5$ 来描述，第 $i$ 个数字表示在第 $i$ 行的相应位置有一个棋子，如下：\n\n行号 $1\\ 2\\ 3\\ 4\\ 5\\ 6$\n\n列号 $2\\ 4\\ 6\\ 1\\ 3\\ 5$\n\n这只是棋子放置的一个解。请编一个程序找出所有棋子放置的解。  \n并把它们以上面的序列方法输出，解按字典顺序排列。  \n请输出前 $3$ 个解。最后一行是解的总个数。\n\n', 'formatI': '一行一个正整数 $n$，表示棋盘是 $n \\times n$ 大小的。\n\n', 'formatO': '前三行为前三个解，每个解的两个数字之间用一个空格隔开。第四行只有一个数字，表示解的总数。\n', 'hint': '【数据范围】  \n对于 $100\\%$ 的数据，$6 \\le n \\le 13$。\n\n题目翻译来自NOCOW。\n\nUSACO Training Section 1.5\n', 'locale': 'zh-CN'}, 'attachments': [], 'showScore': True, 'acceptSolution': False, 'acceptLanguages': [5, 1, 2, 28, 3, 4, 11, 12, 27, 34, 7, 25, 8, 33, 15, 14, 19, 30, 31, 32, 21, 22, 17, 9, 16, 13, 23], 'samples': [['6\n', '2 4 6 1 3 5\n3 6 2 5 1 4\n4 1 5 2 6 3\n4\n']], 'limits': {'time': [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000], 'memory': [128000, 128000, 128000, 128000, 128000, 128000, 128000, 128000]}, 'translation': ''}, 'translations': {'zh-CN': {'name': '[USACO1.5] 八皇后 Checker Challenge', 'background': '', 'description': '一个如下的 $6 \\times 6$ 的跳棋棋盘，有六个棋子被放置在棋盘上，使得每行、每列有且只有一个，每条对角线（包括两条主对角线的所有平行线）上至多有一个棋子。\n\n![](https://cdn.luogu.com.cn/upload/image_hosting/3h71x0yf.png)\n\n上面的布局可以用序列 $2\\ 4\\ 6\\ 1\\ 3\\ 5$ 来描述，第 $i$ 个数字表示在第 $i$ 行的相应位置有一个棋子，如下：\n\n行号 $1\\ 2\\ 3\\ 4\\ 5\\ 6$\n\n列号 $2\\ 4\\ 6\\ 1\\ 3\\ 5$\n\n这只是棋子放置的一个解。请编一个程序找出所有棋子放置的解。  \n并把它们以上面的序列方法输出，解按字典顺序排列。  \n请输出前 $3$ 个解。最后一行是解的总个数。\n\n', 'formatI': '一行一个正整数 $n$，表示棋盘是 $n \\times n$ 大小的。\n\n', 'formatO': '前三行为前三个解，每个解的两个数字之间用一个空格隔开。第四行只有一个数字，表示解的总数。\n', 'hint': '【数据范围】  \n对于 $100\\%$ 的数据，$6 \\le n \\le 13$。\n\n题目翻译来自NOCOW。\n\nUSACO Training Section 1.5\n', 'locale': 'zh-CN'}}, 'bookmarked': False, 'contest': None, 'vjudgeUsername': None, 'lastLanguage': None, 'lastCode': '', 'lastCodeAt': None, 'recommendations': [{'pid': 'P1019', 'type': 'P', 'title': '[NOIP 2000 提高组] 单词接龙（疑似错题）', 'difficulty': 3}, {'pid': 'P1135', 'type': 'P', 'title': '奇怪的电梯', 'difficulty': 3}, {'pid': 'P1443', 'type': 'P', 'title': '马的遍历', 'difficulty': 3}, {'pid': 'P1605', 'type': 'P', 'title': '迷宫', 'difficulty': 2}, {'pid': 'P2392', 'type': 'P', 'title': 'kkksc03考前临时抱佛脚', 'difficulty': 2}], 'forum': {'name': 'P1219 [USACO1.5] 八皇后 Checker Challenge', 'type': 2, 'slug': 'P1219', 'color': 'orange-3'}, 'discussions': [{'id': 1189218, 'title': '警示后人，警钟敲烂', 'author': {'uid': 1708097, 'avatar': 'https://cdn.luogu.com.cn/upload/usericon/1708097.png', 'name': 'Zhengbeichen', 'slogan': '“若管理与我斗，就斗到至死方休，管它是坎还是沟，我不知天高地厚。”', 'badge': None, 'isAdmin': False, 'isBanned': False, 'color': 'Green', 'ccfLevel': 0, 'xcpcLevel': 0, 'background': ''}, 'time': 1762052303}, {'id': 1187018, 'title': '没过样例求帮', 'author': {'uid': 1091106, 'avatar': 'https://cdn.luogu.com.cn/upload/usericon/1091106.png', 'name': 'lemon8932', 'slogan': '泪水打湿DVE C，G Bond誓要拿AC', 'badge': None, 'isAdmin': False, 'isBanned': False, 'color': 'Blue', 'ccfLevel': 0, 'xcpcLevel': 0, 'background': ''}, 'time': 1761917134}, {'id': 1186969, 'title': '求帮办', 'author': {'uid': 1091106, 'avatar': 'https://cdn.luogu.com.cn/upload/usericon/1091106.png', 'name': 'lemon8932', 'slogan': '泪水打湿DVE C，G Bond誓要拿AC', 'badge': None, 'isAdmin': False, 'isBanned': False, 'color': 'Blue', 'ccfLevel': 0, 'xcpcLevel': 0, 'background': ''}, 'time': 1761916260}, {'id': 1181723, 'title': '0分求调', 'author': {'uid': 1704379, 'avatar': 'https://cdn.luogu.com.cn/upload/usericon/1704379.png', 'name': 'maibohan123', 'slogan': '大鹏一日同风起，扶摇直上九万里', 'badge': None, 'isAdmin': False, 'isBanned': False, 'color': 'Green', 'ccfLevel': 0, 'xcpcLevel': 0, 'background': ''}, 'time': 1761472212}, {'id': 1181568, 'title': '求助，74分wa最后2点', 'author': {'uid': 1647538, 'avatar': 'https://cdn.luogu.com.cn/upload/usericon/1647538.png', 'name': 'zq111111', 'slogan': '', 'badge': None, 'isAdmin': False, 'isBanned': False, 'color': 'Green', 'ccfLevel': 0, 'xcpcLevel': 0, 'background': ''}, 'time': 1761463493}, {'id': 1178295, 'title': '求助', 'author': {'uid': 1630890, 'avatar': 'https://cdn.luogu.com.cn/upload/usericon/1630890.png', 'name': 'wjf131227', 'slogan': '他连自己的死亡都是精心策划的......', 'badge': None, 'isAdmin': False, 'isBanned': False, 'color': 'Blue', 'ccfLevel': 0, 'xcpcLevel': 0, 'background': ''}, 'time': 1761132668}], 'locale': 'zh-CN', 'canEdit': False}, 'user': None, 'time': 1762238838.786272, 'theme': None}
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

def submit_problem(problemid: str, language: str, code: str, enableO2 : bool, cookies: dict, max_captcha_retries: int = 3, retry_delay: float = 1.0) -> int:
    """
    提交代码到洛谷指定题目。

    返回是否提交成功。
    """
    lang_id = languages_map.get(language)
    if lang_id is None:
        raise ValueError(f"Unsupported language: {language}")

    with httpx.Client(headers={"user-agent": random_ua()},
                      cookies=cookies,
                      follow_redirects=True) as client:
        # 首先打开题目页面以获取 csrf token
        response = client.get(f"https://www.luogu.com.cn/problem/{problemid}")
        response.raise_for_status()
        client.headers.update({"x-csrf-token": extract_csrf_token(response.text)})

        last_json = None
        for attempt in range(1, max_captcha_retries + 1):
            # 获取验证码图片并识别
            img = client.get(f"https://www.luogu.com.cn/api/verify/captcha?_t={time.time()}").content
            captcha_text = ocr.classification(img)

            payload = {
                "lang": lang_id,
                "code": code,
                "captcha": captcha_text
            }
            if lang_id in [1, 2, 3, 4, 11, 12, 27, 34]:  # C/C++ languages and Pascal
                payload["enableO2"] = int(enableO2)

            response = client.post(f"https://www.luogu.com.cn/fe/api/problem/submit/{problemid}",
                                 json=payload,
                                 headers={"referer": f"https://www.luogu.com.cn/problem/{problemid}"})
            try:
                json_resp = response.json()
            except Exception:
                raise RuntimeError(f"Submission failed, non-json response: {response.text}")

            last_json = json_resp

            # 如果包含 rid，认为提交成功并返回 rid
            if 'rid' in json_resp:
                return int(json_resp['rid'])

            # 检查是否为验证码相关错误，若是则重试；否则直接报错
            error_type = str(json_resp.get('errorType', ''))
            low = error_type.lower()
            if 'captcha' in low or 'invalidcaptcha' in low or 'captcha_not_match' in low:
                # 如果还可以重试，则等待并重试
                if attempt < max_captcha_retries:
                    time.sleep(retry_delay)
                    continue
                else:
                    raise RuntimeError(f"Submission failed due to invalid captcha after {max_captcha_retries} attempts: {json_resp}")
            else:
                raise RuntimeError(f"Submission failed: {json_resp}")

        # 如果循环结束仍未返回，则抛出最后一次的错误信息
        raise RuntimeError(f"Submission failed after {max_captcha_retries} attempts: {last_json}")

def craw_submission_info(rid: int, cookies: dict | None = None) -> Dict[str, Any] | None:
    """
    爬取洛谷提交状态页面并提取提交结果信息。
    """
    """
    eg: {'code': 200, 'currentTemplate': 'RecordShow', 'currentData': {'record': {'detail': {'compileResult': {'success': True, 'message': None, 'opt2': False, '__CLASS_NAME': 'Luogu\\DataClass\\Record\\JudgeResult\\CompileResult'}, 'judgeResult': {'subtasks': [{'id': 0, 'score': 100, 'status': 12, 'testCases': {'1': {'id': 1, 'status': 12, 'time': 4, 'memory': 788, 'score': 5, 'signal': 0, 'exitCode': 0, 'description': 'ok accepted', 'subtaskID': 0, '__CLASS_NAME': 'Luogu\\DataClass\\Record\\JudgeResult\\TestCaseJudgeResult'}, '0': {'id': 0, 'status': 12, 'time': 4, 'memory': 788, 'score': 5, 'signal': 0, 'exitCode': 0, 'description': 'ok accepted', 'subtaskID': 0, '__CLASS_NAME': 'Luogu\\DataClass\\Record\\JudgeResult\\TestCaseJudgeResult'}, '8': {'id': 8, 'status': 12, 'time': 4, 'memory': 816, 'score': 5, 'signal': 0, 'exitCode': 0, 'description': 'ok accepted', 'subtaskID': 0, '__CLASS_NAME': 'Luogu\\DataClass\\Record\\JudgeResult\\TestCaseJudgeResult'}, '3': {'id': 3, 'status': 12, 'time': 4, 'memory': 788, 'score': 5, 'signal': 0, 'exitCode': 0, 'description': 'ok accepted', 'subtaskID': 0, '__CLASS_NAME': 'Luogu\\DataClass\\Record\\JudgeResult\\TestCaseJudgeResult'}, '10': {'id': 10, 'status': 12, 'time': 4, 'memory': 1064, 'score': 5, 'signal': 0, 'exitCode': 0, 'description': 'ok accepted', 'subtaskID': 0, '__CLASS_NAME': 'Luogu\\DataClass\\Record\\JudgeResult\\TestCaseJudgeResult'}, '4': {'id': 4, 'status': 12, 'time': 4, 'memory': 788, 'score': 5, 'signal': 0, 'exitCode': 0, 'description': 'ok accepted', 'subtaskID': 0, '__CLASS_NAME': 'Luogu\\DataClass\\Record\\JudgeResult\\TestCaseJudgeResult'}, '9': {'id': 9, 'status': 12, 'time': 5, 'memory': 816, 'score': 5, 'signal': 0, 'exitCode': 0, 'description': 'ok accepted', 'subtaskID': 0, '__CLASS_NAME': 'Luogu\\DataClass\\Record\\JudgeResult\\TestCaseJudgeResult'}, '5': {'id': 5, 'status': 12, 'time': 4, 'memory': 792, 'score': 5, 'signal': 0, 'exitCode': 0, 'description': 'ok accepted', 'subtaskID': 0, '__CLASS_NAME': 'Luogu\\DataClass\\Record\\JudgeResult\\TestCaseJudgeResult'}, '12': {'id': 12, 'status': 12, 'time': 4, 'memory': 812, 'score': 5, 'signal': 0, 'exitCode': 0, 'description': 'ok accepted', 'subtaskID': 0, '__CLASS_NAME': 'Luogu\\DataClass\\Record\\JudgeResult\\TestCaseJudgeResult'}, '13': {'id': 13, 'status': 12, 'time': 4, 'memory': 816, 'score': 5, 'signal': 0, 'exitCode': 0, 'description': 'ok accepted', 'subtaskID': 0, '__CLASS_NAME': 'Luogu\\DataClass\\Record\\JudgeResult\\TestCaseJudgeResult'}, '7': {'id': 7, 'status': 12, 'time': 4, 'memory': 788, 'score': 5, 'signal': 0, 'exitCode': 0, 'description': 'ok accepted', 'subtaskID': 0, '__CLASS_NAME': 'Luogu\\DataClass\\Record\\JudgeResult\\TestCaseJudgeResult'}, '2': {'id': 2, 'status': 12, 'time': 4, 'memory': 788, 'score': 5, 'signal': 0, 'exitCode': 0, 'description': 'ok accepted', 'subtaskID': 0, '__CLASS_NAME': 'Luogu\\DataClass\\Record\\JudgeResult\\TestCaseJudgeResult'}, '14': {'id': 14, 'status': 12, 'time': 4, 'memory': 1064, 'score': 5, 'signal': 0, 'exitCode': 0, 'description': 'ok accepted', 'subtaskID': 0, '__CLASS_NAME': 'Luogu\\DataClass\\Record\\JudgeResult\\TestCaseJudgeResult'}, '16': {'id': 16, 'status': 12, 'time': 4, 'memory': 816, 'score': 5, 'signal': 0, 'exitCode': 0, 'description': 'ok accepted', 'subtaskID': 0, '__CLASS_NAME': 'Luogu\\DataClass\\Record\\JudgeResult\\TestCaseJudgeResult'}, '11': {'id': 11, 'status': 12, 'time': 4, 'memory': 764, 'score': 5, 'signal': 0, 'exitCode': 0, 'description': 'ok accepted', 'subtaskID': 0, '__CLASS_NAME': 'Luogu\\DataClass\\Record\\JudgeResult\\TestCaseJudgeResult'}, '19': {'id': 19, 'status': 12, 'time': 4, 'memory': 816, 'score': 5, 'signal': 0, 'exitCode': 0, 'description': 'ok accepted', 'subtaskID': 0, '__CLASS_NAME': 'Luogu\\DataClass\\Record\\JudgeResult\\TestCaseJudgeResult'}, '6': {'id': 6, 'status': 12, 'time': 4, 'memory': 792, 'score': 5, 'signal': 0, 'exitCode': 0, 'description': 'ok accepted', 'subtaskID': 0, '__CLASS_NAME': 'Luogu\\DataClass\\Record\\JudgeResult\\TestCaseJudgeResult'}, '15': {'id': 15, 'status': 12, 'time': 4, 'memory': 1064, 'score': 5, 'signal': 0, 'exitCode': 0, 'description': 'ok accepted', 'subtaskID': 0, '__CLASS_NAME': 'Luogu\\DataClass\\Record\\JudgeResult\\TestCaseJudgeResult'}, '17': {'id': 17, 'status': 12, 'time': 4, 'memory': 812, 'score': 5, 'signal': 0, 'exitCode': 0, 'description': 'ok accepted', 'subtaskID': 0, '__CLASS_NAME': 'Luogu\\DataClass\\Record\\JudgeResult\\TestCaseJudgeResult'}, '18': {'id': 18, 'status': 12, 'time': 5, 'memory': 816, 'score': 5, 'signal': 0, 'exitCode': 0, 'description': 'ok accepted', 'subtaskID': 0, '__CLASS_NAME': 'Luogu\\DataClass\\Record\\JudgeResult\\TestCaseJudgeResult'}}, 'judger': '', 'time': 82, 'memory': 1064, '__CLASS_NAME': 'Luogu\\DataClass\\Record\\JudgeResult\\SubtaskJudgeResult'}], 'finishedCaseCount': 20, 'status': 0, 'time': 0, 'memory': 0, 'score': 0, '__CLASS_NAME': 'Luogu\\DataClass\\Record\\JudgeResult\\JudgeResult'}, 'version': 400, '__CLASS_NAME': 'Luogu\\DataClass\\Record\\RecordDetail'}, 'sourceCode': '#include <bits/stdc++.h>\nusing namespace std;\n\nint main() {\n    ios::sync_with_stdio(0);\n    cin.tie(0);\n    int n, m;\n    cin >> n >> m;\n    vector<int> a(n * m + 1, 0);\n    for (int i = 1; i <= n * m; i++){\n        cin >> a[i];\n    }\n    int t = a[1];\n    sort(a.begin() + 1, a.begin() + n * m + 1, greater<int>());\n    int cnt = 0;\n    for (int j = 1; j <= m; j++){\n        if (j % 2 == 1){\n            for (int i = 1; i <= n; i++){\n                cnt++;\n                if (a[cnt] == t){\n                    cout << j << " " << i << endl;\n                    return 0;\n                }\n            }\n        }\n        else {\n            for (int i = n; i >= 1; i--){\n                cnt++;\n                if (a[cnt] == t){\n                    cout << j << " " << i << endl;\n                    return 0;\n                }\n            }\n        }\n    }\n    return 0;\n}', 'time': 82, 'memory': 1064, 'problem': {'pid': 'P14358', 'title': '[CSP-J 2025] 座位 / seat（官方数据）', 'difficulty': 2, 'fullScore': 100, 'type': 'P'}, 'contest': None, 'sourceCodeLength': 874, 'submitTime': 1762512158, 'language': 28, 'user': {'uid': 1010774, 'name': 'liveless', 'avatar': 'https://cdn.luogu.com.cn/upload/usericon/1010774.png', 'slogan': '矢志不渝，矢志不渝。 | linux.do liveless | 3673398763', 'badge': None, 'isAdmin': False, 'isBanned': False, 'color': 'Orange', 'ccfLevel': 5, 'xcpcLevel': 0, 'background': 'https://cdn.luogu.com.cn/upload/image_hosting/i1ct5rjs.png'}, 'id': 245839197, 'status': 12, 'enableO2': True, 'score': 100}, 'testCaseGroup': [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]], 'showStatus': True}, 'currentTitle': 'R245839197', 'currentTheme': {'id': 224610, 'header': {'imagePath': 'https://cdn.luogu.com.cn/upload/image_hosting/guyqtngi.png', 'color': [[35, 37, 38, 1], [65, 67, 69, 1]], 'blur': 0, 'brightness': 0, 'degree': 90, 'repeat': 0, 'position': [58, 52], 'size': [-1, -1], 'type': 1, '__CLASS_NAME': 'Luogu\\DataClass\\User\\ThemeConfig\\HeaderFooterConfig'}, 'sideNav': {'logoBackgroundColor': [34, 192, 231, 1], 'color': [0, 0, 0, 1], 'invertColor': False, '__CLASS_NAME': 'Luogu\\DataClass\\User\\ThemeConfig\\SideNavConfig'}, 'footer': {'imagePath': 'https://cdn.luogu.com.cn/upload/image_hosting/guyqtngi.png', 'color': [[51, 51, 51, 1]], 'blur': 0, 'brightness': 0, 'degree': 0, 'repeat': 0, 'position': [98, 86], 'size': [-1, -1], 'type': 1, '__CLASS_NAME': 'Luogu\\DataClass\\User\\ThemeConfig\\HeaderFooterConfig'}}, 'currentTime': 1762521846, 'currentUser': {'followingCount': 83, 'followerCount': 39, 'ranking': 13187, 'eloValue': 917, 'blogAddress': 'https://www.luogu.com.cn/blog/zhongxm/', 'unreadMessageCount': 0, 'unreadNoticeCount': 0, 'uid': 1010774, 'name': 'liveless', 'avatar': 'https://cdn.luogu.com.cn/upload/usericon/1010774.png', 'slogan': '矢志不渝，矢志不渝。 | linux.do liveless | 3673398763', 'badge': None, 'isAdmin': False, 'isBanned': False, 'color': 'Orange', 'ccfLevel': 5, 'xcpcLevel': 0, 'background': 'https://cdn.luogu.com.cn/upload/image_hosting/i1ct5rjs.png', 'verified': True}}
    """
    with httpx.Client(headers={"user-agent": random_ua()},
                      cookies=cookies,
                      follow_redirects=True) as client:
        response = client.get(f"https://www.luogu.com.cn/record/{rid}")
        response.raise_for_status()
        # print(response.text)
        return extract_and_parse_fe_injection_regex(response.text)

def craw_submission_status(rid: int, cookies: dict | None = None) -> Dict[str, Any] | None:
    """
    爬取洛谷提交状态页面并提取提交的代码内容。
    """
    submit_info = craw_submission_info(rid, cookies)
    if submit_info is None:
        return None

    # Helper to safely dig nested dict keys. Returns default if any key is missing or intermediate value is not a dict.
    def dig(d: dict | None, *keys, default=None):
        cur = d
        for k in keys:
            if not isinstance(cur, dict):
                return default
            if k not in cur:
                return default
            cur = cur[k]
        return cur

    payload = {
        "compileResult": dig(submit_info, 'currentData', 'record', 'detail', 'compileResult', default=None),
        "sourceCode": dig(submit_info, 'currentData', 'record', 'sourceCode', default=None),
        "time": dig(submit_info, 'currentData', 'record', 'time', default=None),
        "memory": dig(submit_info, 'currentData', 'record', 'memory', default=None),
        "language": dig(submit_info, 'currentData', 'record', 'language', default=None),
        "status": dig(submit_info, 'currentData', 'record', 'status', default=None),
        "score": dig(submit_info, 'currentData', 'record', 'score', default=None),
        # subtasks may be missing; return empty list as a sensible default
        "subtaskResults": dig(submit_info, 'currentData', 'record', 'detail', 'judgeResult', 'subtasks', default=[]),
    }
    return payload