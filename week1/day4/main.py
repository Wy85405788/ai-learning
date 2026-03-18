# main.py

import os
print("main.py 已加载")
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
from datetime import datetime
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from schemas import AITask
from services.ai_task_generator import QwenTaskGenerator
from typing import List

# 初始化日志
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

if not DASHSCOPE_API_KEY:
    raise ValueError("❌ 未找到 DASHSCOPE_API_KEY，请检查 .env 文件")


# 初始化 AI 任务生成器
task_generator = QwenTaskGenerator(api_key=DASHSCOPE_API_KEY)


# 创建 FastAPI 应用
app = FastAPI(
    title="AI Task Generator",
    description="使用 Qwen3 自动生成每日开发任务",
    version="1.0.0"
)

task_history: List[dict] = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/task/today", response_model=AITask)
async def get_today_task():
    try:
        # 现在 generate_task() 返回 dict
        task_dict = await task_generator.generate_task()
        # 动态设置 created_at
        task_dict["created_at"] = datetime.now().strftime("%Y-%m-%d")

        #存入历史
        task_history.insert(0, task_dict) #插在开头
        if len(task_history) > 10:
            task_history.pop()

        # Pydantic 会自动验证并转换
        return AITask(**task_dict)

    except Exception as e:
        logger.error(f"生成任务失败: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/task/history", response_model=List[AITask])
async def get_task_history():
    """
    返回最近 10 条 AI 生成任务（按时间倒序）
    """
    try:
        # 将 dict 列表转为 AITask 列表（触发验证）
        history_tasks = [AITask(**task) for task in task_history]
        return history_tasks
    except Exception as e:
        logger.error(f"获取历史任务失败: {str(e)}")
        raise HTTPException(status_code=500, detail="历史任务加载失败")