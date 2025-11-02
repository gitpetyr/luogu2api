import json
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any
import fake_useragent

def random_ua():
    return fake_useragent.FakeUserAgent().random

def extract_csrf_token(html: str) -> str:
    """从 HTML 中使用 BeautifulSoup 提取 CSRF token"""
    
    soup = BeautifulSoup(html, 'html.parser')
    
    meta_tag = soup.find('meta', attrs={'name': 'csrf-token'})
    
    if meta_tag:
        token = meta_tag.get('content')
        
        if isinstance(token, str):
            # 3. 在这个块内部，类型检查器知道 token 100% 是 str
            return token

    # 程序会继续执行到这里，并引发错误
    raise ValueError("CSRF token not found in login page HTML.")

def extract_lentille_context(html_content: str) -> Optional[Dict[str, Any]]:
    """
    从HTML字符串中解析ID为 'lentille-context' 的 <script> 标签中的JSON数据。

    参数:
        html_content (str): 包含目标 <script> 标签的完整HTML字符串。

    返回:
        Optional[Dict[str, Any]]: 解析后的Python字典。
        如果未找到标签、标签内容为空或JSON解析失败，则返回 None。
    """
    if not html_content:
        raise ValueError("Input HTML content is empty.")

    try:
        # 1. 初始化BeautifulSoup解析器
        soup = BeautifulSoup(html_content, 'html.parser')

        # 2. 查找具有特定ID的 <script> 标签
        script_tag = soup.find('script', id='lentille-context')

        # 3. 检查是否找到了标签
        if not script_tag:
            raise ValueError("Script tag with id 'lentille-context' not found.")

        # 4. 提取标签内的文本内容
        json_string = script_tag.string

        # 5. 检查内容是否为空
        if not json_string:
            raise ValueError("Script tag content is empty.")

        # 6. 解析JSON字符串并返回
        data_dict = json.loads(json_string)
        return data_dict

    except json.JSONDecodeError as e:
        raise ValueError(f"Json decoding failed: {e.msg}") from e
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred: {str(e)}") from e