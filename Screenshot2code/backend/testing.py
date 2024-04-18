import asyncio
import base64

import websockets
import json


async def communicate_with_server(uri, data):
    async with websockets.connect(uri) as ws:
        # 构造要发送的JSON数据包
        data_to_send = json.dumps(data)
        # 将字典转换为JSON字符串并发送
        await ws.send(data_to_send)

        # 持续接收服务器消息
        content = ""
        while True:
            try:
                message = await ws.recv()
                message_data = json.loads(message)
                if message_data.get('type') == 'chunk':
                    content += message_data['value']
                elif message_data.get('type') == 'status':
                    print(content)
                    content = ""  # 重置内容变量
                    print(f"Received message: {message_data}")
                else:
                    print("\n\nFinally message:", message_data['value'])
                    with open("test.html", "w", encoding="utf-8") as file:
                        file.write(message_data['value'])
            except websockets.exceptions.ConnectionClosed:
                # 处理连接关闭的情况
                print("Connection closed by the server.")
                break
            except json.JSONDecodeError:
                # 处理非JSON格式的消息
                print("Received a message that is not a valid JSON.")
            except Exception as e:
                # 处理其他可能的异常
                print(f"An error occurred: {e}")
                break


def image_to_data_url(filepath: str):
    with open(filepath, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return f"{encoded_string}"


# WebSocket服务器的URI
websocket_server_uri = "ws://localhost:7001/generate-code"
image_path = "../testimg.png"
data = {
    "type": "message",
    "image": image_to_data_url(image_path),
    "visionModel": "glm-4v",
    "codeGenerationModel": "glm-4",
    "zhipuAiApiKey": "",
    "zhipuAiBaseURL": "https://open.bigmodel.cn/api/paas/v4",
    "isImageGenerationEnabled": False
}
# 运行通信函数
asyncio.get_event_loop().run_until_complete(communicate_with_server(websocket_server_uri, data))
