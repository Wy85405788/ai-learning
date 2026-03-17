from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # 必须导入
from datetime import datetime
from week1.day1.ai_task import AITask

app = FastAPI()

# ⚠️ CORS 中间件必须在路由定义之前添加！
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "AI Developer!"}

@app.get("/task/today")
def get_today_task():
    today_str = datetime.now().strftime("%Y%m%d")
    task_id = f"learn_{today_str}"

    task = AITask(
        task_id=task_id,
        description="学习FastAPI基础并创建今日任务接口"
    )

    return task.to_dict()