# generate
## generate_code
### 功能
总接口，通过`localhost:7001/generate-code`端口建立websocket连接，并与前端交互。
### 接收参数
```python
{
    "type": "message",
    "image": "image_path",
    "visionModel": "glm-4v",
    "codeGenerationModel": "glm-4",
    "zhipuAiApiKey": "",
    "zhipuAiBaseURL": "https://open.bigmodel.cn/api/paas/v4",
    "isImageGenerationEnabled": False
}
```
- `type`: 选填，消息类型，固定为`message`
- `image`: 必填，图片路径或图片的base64编码
- `visionModel`: 选填，图像识别模型，可选`glm-4v`
- `codeGenerationModel`: 选填，代码生成模型，可选`glm-4`、`glm-3-turbo`
- `zhipuAiApiKey`: 选填，若服务器后端没有配置则必填，智谱API密钥
- `zhipuAiBaseURL`: 选填，智谱API基础URL
- `isImageGenerationEnabled`: 选填，是否启用图像生成

### 返回示例
#### 状态信息
```python
{
    "type": "status", 
    "value": "Generating description..."
}
```
- `type`: 固定为`status`
- `value`: 描述信息，按照生成流程分别为`Generating description...`、`Generating code...`、`Generating images...`（如果启用图像生成）、`Code generation complete.`。

#### AI回复段
```python
{
    "type": "chunk", 
    "value": "example value"
}
```
- `type`: 固定为`chunk`
- `value`: 回复段内容

由于AI的响应是流式响应，生成内容会源源不断发送，所以需要前端不断接收。

#### 生成完成
```python
{
    "type": "setCode", 
    "value": "all html code"
}
```
- `type`: 固定为`setCode`
- `value`: 生成完成后的完整HTML代码。

生成完成后，后端会关闭websocket连接。

#### 错误信息
```python
{
    "type": "error", 
    "value": "error message"
}
```
- `type`: 固定为`error`
- `value`: 错误信息

发送错误信息后，后端会关闭websocket连接，错误码`4332`。

## llm
模型区主要有以下模型集合：
- `VISION_MODELS`：包含所有视觉大模型名称的列表。
- `CODE_GENERATION_MODELS`：包含所有代码生成模型名称的列表。

函数区主要有以下功能函数：
- `stream_zhipuai_response`：向智谱AI发送请求，并流式转发智谱AI的回复。
- `generate_token`：`stream_zhipuai_response`函数所需的由API-key生成授权令牌的函数。
- `write_logs`：向日志文件写入日志的函数。
- `extract_html`：从智谱AI的回复中提取并格式化HTML代码的函数。

## image_generation
主要函数是`generate_images`函数，该函数从HTML代码中提取出所有图片的URL及其alt，并以alt作为prompt，使用智谱的cogview-3 API生成这些图片。

### 生成图片的步骤
1. 提取HTML代码中的所有图片的alt。
2. 向智谱的cogview-3 API发送请求，生成图片。
3. 提取原HTML中图片URL中关于图片尺寸的信息，将尺寸写入图片的class属性。
4. 将生成的图片URL替换掉原HTML代码中的URL。
5. 返回替换后的HTML代码。



