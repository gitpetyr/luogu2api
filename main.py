from fastapi import FastAPI, HTTPException, Cookie, Query, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from authmgr import login
from problems_mgr import (
    craw_probleminfo, 
    craw_statement, 
    submit_problem, 
    craw_submission_info, 
    craw_submission_status,
    languages_map
)
from miscellaneous import craw_article, craw_paste
from miscellaneous import punch

app = FastAPI(
    title="洛谷API",
    description="非官方的洛谷API接口",
    version="1.0.0"
)

class LoginRequest(BaseModel):
    """
    登录请求的数据模型
    """
    username: str = Query(..., description="洛谷用户名")
    password: str = Query(..., description="洛谷密码")

    class Config:
        schema_extra = {
            "example": {
                "username": "your_username",
                "password": "your_password"
            }
        }

class SubmitRequest(BaseModel):
    """
    提交代码的数据模型
    """
    language: str = Query(..., description="编程语言，必须是支持的语言之一")
    code: str = Query(..., description="提交的代码内容")
    enable_o2: bool = Query(False, description="是否启用 O2 优化，仅对特定语言有效")

    class Config:
        schema_extra = {
            "example": {
                "language": "C++14",
                "code": "#include <iostream>\nint main() {\n    std::cout << \"Hello World!\";\n    return 0;\n}",
                "enable_o2": True
            }
        }

async def get_cookies(
    cookies: str = Query(default=None)
) -> Dict[str, str]:
    if not cookies:
        return {}
    try:
        import json
        return json.loads(cookies)
    except:
        return {}

@app.post("/api/auth/login", 
         summary="登录洛谷账号",
         description="使用用户名和密码登录洛谷账号，返回登录后的 cookies",
         response_description="包含登录状态和 cookies 的响应")
async def api_login(request: LoginRequest):
    """
    使用洛谷账号登录

    Args:
        request (LoginRequest): 包含用户名和密码的请求体

    Returns:
        Dict: 包含以下字段：
            - success (bool): 登录是否成功
            - data (Dict[str, str]): 登录成功时返回的 cookies
            - message (str): 登录失败时的错误信息
            - error_type (str): 登录失败时的错误类型

    Raises:
        HTTPException (401): 登录失败时抛出，详细信息在 response body 中
    """
    result = login(request.username, request.password)
    if not result["success"]:
        raise HTTPException(
            status_code=401,
            detail=result
        )
    return result

@app.get("/api/problem/{problem_id}",
         summary="获取题目信息",
         description="获取洛谷题目的基本信息，包括标题、难度、提交统计等",
         response_description="包含题目详细信息的响应")
async def get_problem_info(
    problem_id: str,
    cookies: Dict[str, str] = Depends(get_cookies)
):
    """
    获取洛谷题目的基本信息

    Args:
        problem_id (str): 题目ID，例如 'P1000'
        cookies (Dict[str, str], optional): 登录后的 cookies，用于获取更多信息

    Returns:
        Dict: 包含题目信息的字典，包括：
            - pid (str): 题目ID
            - title (str): 题目标题
            - difficulty (int): 难度等级
            - totalSubmit (int): 总提交数
            - totalAccepted (int): 通过提交数
            - tags (List[int]): 题目标签ID列表
            等其他字段

    Raises:
        HTTPException (404): 题目不存在时抛出
    """
    result = craw_probleminfo(problem_id, cookies)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Problem not found"
        )
    return result

@app.get("/api/problem/{problem_id}/statement",
         summary="获取题目描述",
         description="获取洛谷题目的完整描述，包括背景、描述、输入输出格式、样例等",
         response_description="包含题目完整描述的响应")
async def get_problem_statement(
    problem_id: str,
    cookies: Dict[str, str] = Depends(get_cookies)
):
    """
    获取洛谷题目的完整描述信息

    Args:
        problem_id (str): 题目ID，例如 'P1000'
        cookies (Dict[str, str], optional): 登录后的 cookies，用于获取更多信息

    Returns:
        Dict: 包含题目描述的字典，包括：
            - background (str): 题目背景
            - description (str): 题目描述
            - input (str): 输入格式
            - output (str): 输出格式
            - samples (List[List[str]]): 样例列表，每个样例是 [输入, 输出] 的列表
            - hint (str): 题目提示
            - provider (int): 题目提供者 UID
            - tags (List[int]): 题目标签ID列表
            - title (str): 题目标题
            - difficulty (int): 题目难度

    Raises:
        HTTPException (404): 题目不存在时抛出
    """
    result = craw_statement(problem_id, cookies)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Problem statement not found"
        )
    return result

@app.post("/api/problem/{problem_id}/submit",
          summary="提交代码",
          description="向指定题目提交代码，需要提供登录后的 cookies",
          response_description="返回提交记录的 ID")
async def submit_code(
    problem_id: str,
    request: SubmitRequest,
    cookies: Dict[str, str] = Depends(get_cookies)
):
    """
    向洛谷题目提交代码

    Args:
        problem_id (str): 题目ID，例如 'P1000'
        request (SubmitRequest): 提交请求体，包含：
            - language (str): 编程语言，必须是支持的语言之一
            - code (str): 提交的代码内容
            - enable_o2 (bool): 是否启用 O2 优化，默认为 False
        cookies (Dict[str, str]): 登录后的 cookies，必需

    Returns:
        Dict: 包含提交记录ID的字典：
            - submission_id (int): 提交记录的 ID

    Raises:
        HTTPException (400): 提交参数错误，如不支持的语言等
        HTTPException (401): 未提供有效的 cookies
        HTTPException (500): 服务器内部错误
    """
    try:
        submission_id = submit_problem(
            problem_id,
            request.language,
            request.code,
            request.enable_o2,
            cookies
        )
        return {"submission_id": submission_id}
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/api/record/{record_id}",
         summary="获取提交记录信息",
         description="获取指定提交记录的详细信息，包括代码、编译信息等",
         response_description="包含提交记录详细信息的响应")
async def get_submission_info(
    record_id: int,
    cookies: Dict[str, str] = Depends(get_cookies)
):
    """
    获取洛谷提交记录的详细信息

    Args:
        record_id (int): 提交记录ID
        cookies (Dict[str, str], optional): 登录后的 cookies，用于获取更多信息

    Returns:
        Dict: 包含提交记录信息的字典，包括：
            - code (int): 状态码
            - currentTemplate (str): 当前模板
            - currentData (Dict): 包含提交记录的详细信息，如：
                - record: 包含编译结果、评测结果、源代码等
                - testCaseGroup: 测试点分组信息

    Raises:
        HTTPException (404): 提交记录不存在时抛出
    """
    result = craw_submission_info(record_id, cookies)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Submission not found"
        )
    return result

@app.get("/api/record/{record_id}/status",
         summary="获取提交状态",
         description="获取指定提交记录的评测状态",
         response_description="包含提交记录评测状态的响应")
async def get_submission_status(
    record_id: int,
    cookies: Dict[str, str] = Depends(get_cookies)
):
    """
    获取洛谷提交记录的评测状态

    Args:
        record_id (int): 提交记录ID
        cookies (Dict[str, str], optional): 登录后的 cookies，用于获取更多信息

    Returns:
        Dict: 包含评测状态的字典，包括：
            - compileResult (Dict): 编译结果
            - sourceCode (str): 源代码
            - time (int): 运行时间
            - memory (int): 内存使用量
            - language (int): 语言ID
            - status (int): 评测状态码
            - score (int): 得分
            - subtaskResults (List): 测试点结果列表

    Raises:
        HTTPException (404): 提交记录不存在时抛出
    """
    result = craw_submission_status(record_id, cookies)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Submission status not found"
        )
    return result

@app.get("/api/article/{article_id}",
         summary="获取文章内容",
         description="获取洛谷文章的内容，包括标题、作者、正文等",
         response_description="包含文章内容的响应")
async def get_article(
    article_id: str,
    cookies: Dict[str, str] = Depends(get_cookies)
):
    """
    获取洛谷文章的详细内容

    Args:
        article_id (str): 文章ID
        cookies (Dict[str, str], optional): 登录后的 cookies，用于获取更多信息

    Returns:
        Dict: 包含文章内容的字典，包括：
            - title (str): 文章标题
            - author (int): 作者UID
            - time (int): 发布时间戳
            - content (str): 文章内容（Markdown格式）

    Raises:
        HTTPException (404): 文章不存在或无权限访问时抛出
    """
    result = craw_article(article_id, cookies)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Article not found"
        )
    return result

@app.get("/api/paste/{paste_id}",
         summary="获取剪贴板内容",
         description="获取洛谷剪贴板的内容",
         response_description="包含剪贴板内容的响应")
async def get_paste(
    paste_id: str,
    cookies: Dict[str, str] = Depends(get_cookies)
):
    """
    获取洛谷剪贴板的内容

    Args:
        paste_id (str): 剪贴板ID
        cookies (Dict[str, str], optional): 登录后的 cookies，用于获取更多信息

    Returns:
        Dict: 包含剪贴板内容的字典，包括：
            - data (str): 剪贴板内容
            - author (int): 作者UID
            - time (int): 创建时间戳
            - public (bool): 是否公开

    Raises:
        HTTPException (404): 剪贴板不存在或无权限访问时抛出
    """
    result = craw_paste(paste_id, cookies)
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Paste not found"
        )
    return result


@app.post("/api/punch",
          summary="每日打卡",
          description="使用登录后的 cookies 执行洛谷每日打卡，返回打卡结果",
          response_description="包含打卡是否成功与相关数据的响应")
async def api_punch(
    cookies: Dict[str, str] = Depends(get_cookies)
):
    """
    使用提供的 cookies 执行洛谷站点的每日打卡操作。

    Args:
        cookies (Dict[str, str]): 登录后的 cookies（JSON 字符串格式，通过 `cookies` 查询参数传入）

    Returns:
        Dict: 打卡结果，如果成功返回 `{"success": True, "data": ...}`，失败返回 HTTP 400 或 401。
    """
    if not cookies:
        raise HTTPException(status_code=401, detail="Missing cookies")

    result = punch(cookies)
    # punch 返回形如 {"success": True/False, "data": ...} 或包含 error 字段
    if isinstance(result, dict) and result.get("success"):
        return result
    # 若返回包含错误信息，包装成 HTTPException
    raise HTTPException(status_code=400, detail=result)

@app.get("/api/languages",
         summary="获取支持的编程语言列表",
         description="获取洛谷支持的所有编程语言及其对应的ID",
         response_description="包含语言名称和ID映射的响应")
async def get_supported_languages():
    """
    获取洛谷支持的所有编程语言列表

    Returns:
        Dict[str, int]: 语言名称到语言ID的映射字典，例如：
            - "Pascal": 1
            - "C": 2
            - "C++14 (GCC 9)": 28
            - "Python 3": 7
            等等
    """
    return languages_map

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
