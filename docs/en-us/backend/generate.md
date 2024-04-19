# generate

## generate_code
### Functionality
The main interface establishes a websocket connection through the `localhost:7001/generate-code` port and interacts with the frontend.

### Parameters Received
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
- `type`: Optional, message type, fixed as `message`
- `image`: Required, path to the image or base64 encoding of the image
- `visionModel`: Optional, image recognition model, options include `glm-4v`
- `codeGenerationModel`: Optional, code generation model, options include `glm-4`, `glm-3-turbo`
- `zhipuAiApiKey`: Optional, required if the server backend is not configured, Zhipu AI API key
- `zhipuAiBaseURL`: Optional, Zhipu AI base URL
- `isImageGenerationEnabled`: Optional, whether to enable image generation

### Example Response
#### Status Information
```python
{
    "type": "status", 
    "value": "Generating description..."
}
```
- `type`: Fixed as `status`
- `value`: Description message, according to the generation process, it can be `Generating description...`, `Generating code...`, `Generating images...` (if image generation is enabled), `Code generation complete.`.

#### AI Reply Chunk
```python
{
    "type": "chunk", 
    "value": "example value"
}
```
- `type`: Fixed as `chunk`
- `value`: Content of the reply chunk

Since the response from AI is streaming, the generated content will be continuously sent, so the frontend needs to continuously receive it.

#### Generation Completion
```python
{
    "type": "setCode", 
    "value": "all html code"
}
```
- `type`: Fixed as `setCode`
- `value`: Complete HTML code after generation.

After generation is complete, the backend will close the websocket connection.

#### Error Information
```python
{
    "type": "error", 
    "value": "error message"
}
```
- `type`: Fixed as `error`
- `value`: Error message

After sending the error message, the backend will close the websocket connection with error code `4332`.

## llm
The model area mainly consists of the following model collections:
- `VISION_MODELS`: Contains a list of all visual large model names.
- `CODE_GENERATION_MODELS`: Contains a list of all code generation model names.

The function area mainly consists of the following functional functions:
- `stream_zhipuai_response`: Sends requests to Zhipu AI and streams the reply from Zhipu AI.
- `generate_token`: Function to generate authorization tokens required by the `stream_zhipuai_response` function.
- `write_logs`: Function to write logs to the log file.
- `extract_html`: Function to extract and format HTML code from the reply of Zhipu AI.

## image_generation
The main function is the `generate_images` function, which extracts all image URLs and their alt attributes from the HTML code, and uses the alt attributes as prompts to generate these images using Zhipu's cogview-3 API.

### Steps to Generate Images
1. Extract all alt attributes of images from the HTML code.
2. Send requests to Zhipu's cogview-3 API to generate images.
3. Extract information about image size from the original image URLs in the HTML and write the size into the class attribute of the images.
4. Replace the original image URLs in the HTML code with the generated image URLs.
5. Return the modified HTML code.