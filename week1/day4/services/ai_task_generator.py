# services/ai_task_generator.py

import logging
import json
from openai import AsyncOpenAI, APIStatusError, APIConnectionError, RateLimitError

logger = logging.getLogger(__name__)
logger.info("✅ ai_task_generator 模块已加载！")
class QwenTaskGenerator:
    def __init__(self, api_key: str, model: str = "qwen3-max-2026-01-23"):
        self.client = AsyncOpenAI(
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            api_key=api_key
        )
        self.model = model

    async def generate_task(self) -> dict:
        """
        调用 Qwen 模型生成结构化任务（直接返回 JSON 字典）
        """
        messages = [
            {
                "role": "system",
                "content": (
                    "你是一个专业的开发任务生成器。请严格按照以下 JSON 格式输出，"
                    "不要包含任何额外文本、解释或 markdown：\n"
                    "{\n"
                    '  "description": "任务描述",\n'
                    '  "priority": "高",\n'
                    '  "estimated_hours": 3\n'
                    "}\n"
                    "要求：\n"
                    "- description: 清晰、可执行的编程任务，包含技术关键词\n"
                    '- priority: 必须是 "高"、"中" 或 "低"\n'
                    "- estimated_hours: 整数，范围 1~8"
                )
            },
            {
                "role": "user",
                "content": "请生成一个今日开发任务。"
            }
        ]

        try:
            logger.info("Sending request to Qwen for structured task...")

            completion = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=False,
                timeout=30.0
            )
            raw_content = completion.choices[0].message.content.strip()
            logger.info(f"Raw AI response: {raw_content[:100]}...")

            # 尝试提取 JSON（兼容 AI 偶尔加 ```json ... ```）
            if raw_content.startswith("```json"):
                raw_content = raw_content[7:]  # 去掉 ```json
            if raw_content.endswith("```"):
                raw_content = raw_content.rstrip("`")

            # 解析 JSON
            task_data = json.loads(raw_content)

            # 验证必要字段
            required_keys = {"description", "priority", "estimated_hours"}
            if not required_keys.issubset(task_data.keys()):
                raise ValueError(f"缺少必要字段，实际返回: {task_data.keys()}")

            # 补全固定字段（前端仍需要）
            task_data.update({
                "id": 1,  # 暂时固定，历史功能再改
                "status": "待完成",
                "tags": ["ai-generated"],
                "created_at": "2026-03-19"  # 实际用 datetime.now().strftime("%Y-%m-%d")
            })

            logger.info("AI task parsed successfully.")
            return task_data

        except json.JSONDecodeError as e:
            logger.error(f"JSON 解析失败: {e} | Raw: {raw_content}")
            raise Exception("AI 返回格式错误，请重试")

        except RateLimitError as e:
            logger.error(f"Rate limit exceeded: {e}")
            raise Exception("API 调用频率超限，请稍后再试")

        except APIStatusError as e:
            logger.error(f"DashScope API error: {e.status_code} - {e.response.text}")
            raise Exception(f"AI 服务异常: {e.status_code}")

        except APIConnectionError as e:
            logger.error(f"Connection failed: {e}")
            raise Exception("网络连接失败，请检查网络")

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise Exception("AI 生成失败，请稍后重试")