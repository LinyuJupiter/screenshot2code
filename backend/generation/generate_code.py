import os
import traceback
from typing import Dict

import httpx
import zhipuai
from fastapi import APIRouter, WebSocket
from .llm import stream_zhipuai_response, extract_html, write_logs, CODE_GENERATION_MODELS, VISION_MODELS
from .image_generation import generate_images
from prompts import assemble_vision_prompt, assemble_generation_prompt

router = APIRouter()
APP_ERROR_WEB_SOCKET_CODE = 4332


@router.websocket("/generate-code")
async def stream_code(websocket: WebSocket):
    await websocket.accept()

    print("Incoming websocket connection...")

    async def throw_error(
            message: str,
    ):
        await websocket.send_json({"type": "error", "value": message})
        await websocket.close(APP_ERROR_WEB_SOCKET_CODE)

    # TODO: Are the values always strings?
    params: Dict[str, str] = await websocket.receive_json()

    print("Received params")

    # Read the vision model from the request. Fall back to default if not provided.
    vision_model = params.get("visionModel", "glm-4v")
    if vision_model not in VISION_MODELS:
        await throw_error(f"Invalid vision model: {vision_model}")
        raise Exception(f"Invalid vision model: {vision_model}")

    print(f"Using vision model: {vision_model}")

    # Read the code generation model from the request. Fall back to default if not provided.
    code_generation_model = params.get("codeGenerationModel", "glm-4")
    if code_generation_model not in CODE_GENERATION_MODELS:
        await throw_error(f"Invalid code generation model: {code_generation_model}")
        raise Exception(f"Invalid generation model: {code_generation_model}")

    print(f"Using code generation model: {code_generation_model}")

    # Get the ZhipuAI API key from the request. Fall back to environment variable if not provided.
    # If neither is provided, we throw an error.
    zhipuai_api_key = None
    if "zhipuAiApiKey" in params and params["zhipuAiApiKey"]:
        zhipuai_api_key = params["zhipuAiApiKey"]
        print("Using ZhipuAI API key from client-side settings dialog")
    else:
        zhipuai_api_key = os.environ.get("ZHIPUAI_API_KEY")
        if zhipuai_api_key:
            print("Using ZhipuAI API key from environment variable")

    if not zhipuai_api_key or zhipuai_api_key == "":
        print("ZhipuAI API key not found")
        await throw_error(
            "No ZhipuAI API key found. Please add your API key in the settings dialog or add it to backend/.env file. If you add it to .env, make sure to restart the backend server."
        )
        return

    # Get the ZhipuAI Base URL from the request. Fall back to environment variable if not provided.
    zhipuai_base_url = None
    if "zhipuAiBaseURL" in params and params["zhipuAiBaseURL"]:
        zhipuai_base_url = params["zhipuAiBaseURL"]
        print("Using ZhipuAI Base URL from client-side settings dialog")
    else:
        zhipuai_base_url = os.environ.get("ZHIPUAI_BASE_URL")
        if zhipuai_base_url:
            print("Using ZhipuAI Base URL from environment variable")

    if not zhipuai_base_url or zhipuai_base_url == "":
        print("Using official ZhipuAI URL")

    # Get the image generation flag from the request. Fall back to False if not provided.
    should_generate_images = (
        params["isImageGenerationEnabled"]
        if "isImageGenerationEnabled" in params
        else False
    )

    async def process_chunk(content: str):
        await websocket.send_json({"type": "chunk", "value": content})

    print("generating description...")
    await websocket.send_json({"type": "status", "value": "Generating description..."})

    # Assemble the vision prompt
    try:
        prompt_messages = assemble_vision_prompt(params["image"])
    except Exception as e:
        print(e)
        await websocket.send_json(
            {
                "type": "error",
                "value": "Error assembling vision prompt. Contact support at support@picoapps.xyz",
            }
        )
        await websocket.close()
        return

    try:
        completion = await stream_zhipuai_response(
            model=vision_model,
            messages=prompt_messages,  # type: ignore
            api_key=zhipuai_api_key,
            base_url=zhipuai_base_url,
            callback=lambda x: process_chunk(x),
        )
    except zhipuai.APIAuthenticationError as e:
        print("[GENERATE_DESCRIPTION] Authentication failed", e)
        error_message = "Incorrect ZhipuAI key. Please make sure your ZhipuAI API key is correct, " \
                        "or create a new ZhipuAI API key on your ZhipuAI dashboard."
        return await throw_error(error_message)
    except zhipuai.APIStatusError as e:
        print("[GENERATE_DESCRIPTION] Model not found", e)
        error_message = f"{e}. Please make sure you have followed the instructions correctly " \
                        f"to obtain an ZhipuAI key with GLM4 vision access."
        return await throw_error(error_message)
    except zhipuai.APITimeoutError as e:
        print("[GENERATE_DESCRIPTION] Rate limit exceeded", e)
        error_message = "ZhipuAI error - 'You exceeded your current quota, please check your plan and billing details.'"
        return await throw_error(error_message)
    except httpx.ReadError as e:
        print("[GENERATE_DESCRIPTION] Read error", e)
        error_message = "Incorrect ZhipuAI key. Please make sure your ZhipuAI API key is correct, " \
                        "or create a new ZhipuAI API key on your ZhipuAI dashboard."
        return await throw_error(error_message)
    print("Exact used model for description: ", vision_model)

    # Write the messages dict into a log so that we can debug later
    write_logs(prompt_messages, completion)  # type: ignore

    print("generating code...")
    await websocket.send_json({"type": "status", "value": "Generating code..."})

    # Assemble the generation prompt
    try:
        prompt_messages = assemble_generation_prompt(completion)
    except:
        await websocket.send_json(
            {
                "type": "error",
                "value": "Error assembling generation prompt. Contact support at support@picoapps.xyz",
            }
        )
        await websocket.close()
        return

    try:
        completion = await stream_zhipuai_response(
            model=code_generation_model,
            messages=prompt_messages,  # type: ignore
            api_key=zhipuai_api_key,
            base_url=zhipuai_base_url,
            callback=lambda x: process_chunk(x),
        )
    except zhipuai.APIAuthenticationError as e:
        print("[GENERATE_CODE] Authentication failed", e)
        error_message = "Incorrect ZhipuAI key. Please make sure your ZhipuAI API key is correct, " \
                        "or create a new ZhipuAI API key on your ZhipuAI dashboard."
        return await throw_error(error_message)
    except zhipuai.APIStatusError as e:
        print("[GENERATE_CODE] Model not found", e)
        error_message = f"{e}. Please make sure you have followed the instructions correctly " \
                        f"to obtain an ZhipuAI key with GLM4 vision access."
        return await throw_error(error_message)
    except zhipuai.APITimeoutError as e:
        print("[GENERATE_CODE] Rate limit exceeded", e)
        error_message = "ZhipuAI error - 'You exceeded your current quota, please check your plan and billing details.'"
        return await throw_error(error_message)

    print("Exact used model for generation: ", code_generation_model)

    # Write the messages dict into a log so that we can debug later
    write_logs(prompt_messages, completion)  # type: ignore

    # Extract the HTML code from the completion
    completion = extract_html(completion)

    try:
        if should_generate_images:
            await websocket.send_json(
                {"type": "status", "value": "Generating images..."}
            )
            updated_html = await generate_images(
                completion,
                api_key=zhipuai_api_key,
                base_url=zhipuai_base_url,
                model="cogview-3",
            )
        else:
            updated_html = completion
        await websocket.send_json({"type": "setCode", "value": updated_html})
        await websocket.send_json(
            {"type": "status", "value": "Code generation complete."}
        )
    except Exception as e:
        traceback.print_exc()
        print("Image generation failed", e)
        # Send set code even if image generation fails since that triggers
        # the frontend to update history
        await websocket.send_json({"type": "setCode", "value": completion})
        await websocket.send_json(
            {"type": "status", "value": "Image generation failed but code is complete."}
        )

    await websocket.close()
