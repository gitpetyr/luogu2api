import httpx
import re
import fake_useragent
import time
import ddddocr

ocr = ddddocr.DdddOcr(show_ad=False, beta=True)

def _extract_csrf_token(html: str) -> str:
    """从 HTML 中提取 CSRF token"""
    match = re.search(r'<meta\s+name="csrf-token"\s+content="([^"]+)"', html)
    if not match:
        raise ValueError("CSRF token not found in login page HTML.")
    return match.group(1)

def _login(username: str, password: str):
    with httpx.Client(headers={"user-agent": fake_useragent.FakeUserAgent().random},
                      follow_redirects=True) as client:
        response = client.get("https://www.luogu.com.cn/auth/login")
        response.raise_for_status()
        client.headers.update({"x-csrf-token" : _extract_csrf_token(response.text)})
        response = client.get(f"https://www.luogu.com.cn/auth/login-methods?login={username}")
        response.raise_for_status()
        response = client.get(f"https://www.luogu.com.cn/lg4/captcha?_t={time.time()}")
        response.raise_for_status()
        img = response.content
        response = client.post("https://www.luogu.com.cn/do-auth/password", json={
            "username": username,
            "password": password,
            "captcha": ocr.classification(img)
        })
        print(client.cookies)
        print(response.json())
