# prompt

## _init_
Provides two functions to assemble prompt words with URLs to generate the content format required by the large model interface.
- `assemble_vision_prompt`: Assembles prompt words for visual description models with image URLs (or image base64 encoding).
- `assemble_generation_prompt`: Assembles prompt words for code generation models with text descriptions.

## system_prompt
Defines some prompt word variables:
- `VISION_PROMPT`: System prompt words for visual description models
- `VISION_USER_PROMPT`: User prompt words for visual description models
- `CODE_GENERATION_PROMPT`: System prompt words for code generation models
- `CODE_GENERATION_USER_PROMPT`: User prompt words for code generation models