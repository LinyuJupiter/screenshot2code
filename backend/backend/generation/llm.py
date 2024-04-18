import json
import os
import re
import time
from datetime import datetime
from typing import Awaitable, Callable
import httpx
import jwt
from bs4 import BeautifulSoup


VISION_MODELS = {
    "glm-4v"
}

CODE_GENERATION_MODELS = [
    "glm-4",
    "glm-3-turbo"
]


async def stream_zhipuai_response(
        model: str,
        messages: list | dict,
        api_key: str,
        base_url: str | None,
        callback: Callable[[str], Awaitable[None]],
        timeout: httpx.Timeout = httpx.Timeout(60),
) -> str:
    if base_url is None:
        base_url = "https://open.bigmodel.cn/api/paas/v4"

    url = f"{base_url}/chat/completions"
    headers = {
        "Authorization": generate_token(api_key, 60000),
        "Content-Type": "application/json",
    }
    params = {
        "model": model,
        "messages": messages,
        "stream": True,
    }
    if model in CODE_GENERATION_MODELS:
        params["max_token"] = 12800
    async with httpx.AsyncClient(headers=headers, timeout=timeout) as client:
        async with client.stream("POST", url, json=params) as response:
            full_response = ""
            async for chunk in response.aiter_lines():
                chunk = chunk.strip()
                if chunk == "":
                    continue
                # 去掉 'data:' 前缀
                if chunk.startswith("data:"):
                    chunk = chunk[len("data:"):].strip()
                if chunk == "[DONE]":
                    break
                try:
                    # 解析 JSON 数据
                    json_data = json.loads(chunk)
                    content = json_data.get('choices', [{}])[0].get('delta', {}).get('content', '')
                    full_response += content
                    await callback(content)
                except json.JSONDecodeError as e:
                    # 如果解析出错，打印错误信息并继续
                    print(f"Error decoding JSON: {e}, {chunk}")
    return full_response


def generate_token(apikey: str, exp_seconds: int):
    """
    生成带有有效期的JWT令牌。
    """
    try:
        api_key, secret = apikey.split(".")
    except ValueError:
        raise ValueError("无效的apikey格式")

    exp = int(time.time() * 1000) + exp_seconds * 1000
    payload = {
        "api_key": api_key,
        "exp": exp,
        "timestamp": exp - exp_seconds * 1000,
    }

    return jwt.encode(
        payload,
        secret,
        algorithm="HS256",
        headers={"alg": "HS256", "sign_type": "SIGN"},
    )


def write_logs(prompt_messages: list, completion: str):
    # Get the logs path from environment, default to the current working directory
    logs_path = os.environ.get("LOGS_PATH", os.getcwd())

    # Create run_logs directory if it doesn't exist within the specified logs path
    logs_directory = os.path.join(logs_path, "run_logs")
    if not os.path.exists(logs_directory):
        os.makedirs(logs_directory)

    print("Writing to logs directory:", logs_directory)

    # Generate a unique filename using the current timestamp within the logs directory
    filename = datetime.now().strftime(f"{logs_directory}/messages_%Y%m%d_%H%M%S.json")

    # Write the messages dict into a new file for each run
    with open(filename, "w") as f:
        f.write(json.dumps({"prompt": prompt_messages, "completion": completion}))


def extract_html(text):
    # 使用正则表达式匹配从<!DOCTYPE html>开始到</html>结束的所有内容
    html_pattern = r'<!DOCTYPE html>[\s\S]*?</html>'
    html_match = re.search(html_pattern, text)
    html_code = ""
    if html_match:
        # 如果匹配到了完整的HTML内容，则返回
        html_code = html_match.group(0)
    else:
        # 如果没有匹配到完整的HTML内容，则返回从<!DOCTYPE html>开始到文本末尾的内容
        start_pattern = r'<!DOCTYPE html>[\s\S]*'
        start_match = re.search(start_pattern, text)
        if start_match:
            html_code = start_match.group(0)
    soup = BeautifulSoup(html_code, "lxml")
    return soup.prettify()
