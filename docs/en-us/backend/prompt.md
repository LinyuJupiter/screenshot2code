# prompt

## _init_
提供两个函数，用来组装提示词与URL，生成大模型接口所需的content格式。
- `assemble_vision_prompt`：组装视觉描述模型提示词与图片URL（或图片base64编码）
- `assemble_generation_prompt`：组装代码生成模型提示词与文本描述

## system_prompt
定义了一些提示词变量：
- `VISION_PROMPT`：视觉描述模型系统提示词
- `VISION_USER_PROMPT`：视觉描述模型用户提示词
- `CODE_GENERATION_PROMPT`：代码生成模型系统提示词
- `CODE_GENERATION_USER_PROMPT`：代码生成模型用户提示词
