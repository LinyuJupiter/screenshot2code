from .system_prompt import *


def assemble_vision_prompt(image_data_url: str):
    """
    Assemble the vision prompt with the given image data URL.
    :param image_data_url: image's base64 encoded data or URL
    :return: The 'message' parameter sent to the vision model
    """
    system_content = VISION_PROMPT
    user_prompt = VISION_USER_PROMPT
    user_content = [
        {
            "type": "image_url",
            "image_url": {"url": image_data_url},
        },
        {
            "type": "text",
            "text": user_prompt,
        },
    ]
    return [
        {
            "role": "system",
            "content": system_content,
        },
        {
            "role": "user",
            "content": user_content,
        },
    ]


def assemble_generation_prompt(description: str):
    """
    Assemble the code generation prompt with the given description.
    :param description: description of the web page
    :return: The 'message' parameter sent to the language model
    """
    system_content = CODE_GENERATION_PROMPT
    user_prompt = CODE_GENERATION_USER_PROMPT
    user_content = [
        {
            "type": "text",
            "text": user_prompt + description,
        },
    ]
    return [
        {
            "role": "system",
            "content": system_content,
        },
        {
            "role": "user",
            "content": user_content,
        },
    ]
