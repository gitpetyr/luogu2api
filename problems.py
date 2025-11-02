from utils import extract_csrf_token, extract_lentille_context, random_ua
from typing import Optional, Dict, Any
import httpx
import time
# import ddddocr
import getpass


def craw_statement(problemid: str, cookies: dict | None = None) -> Dict[str, Any] | None:
    """
    爬取洛谷题目描述页面并提取题目信息。
    """
    with httpx.Client(headers={"user-agent": random_ua()},
                      cookies=cookies,
                      follow_redirects=True) as client:
        response = client.get(f"https://www.luogu.com.cn/problem/{problemid}")
        response.raise_for_status()
        return extract_lentille_context(response.text)
    
# print(craw_statemet("P121912328"))
