# Day 2：FastAPI 初体验 —— 把任务变成 Web 接口

## 🎯 我做了什么？
- 安装了 FastAPI 和 Uvicorn，搭建了本地 Web 服务
- 创建了第一个 API 路由：`GET /`
- 集成 Day 1 的 `AITask` 类，实现 `GET /task/today` 接口
- 成功通过浏览器访问接口，返回结构化的 JSON 任务数据

## 🧩 核心代码亮点
```python
# 自动导入昨日成果
from week1.day1.ai_task import AITask

@app.get("/task/today")
def get_today_task():
    today_str = datetime.now().strftime("%Y%m%d")
    task = AITask(
        task_id=f"learn_{today_str}",
        description="学习 FastAPI 基础并创建今日任务接口"
    )
    return task.to_dict()  # ← FastAPI 自动转 JSON

```

## 🔍 关键理解
- FastAPI 不需要手动调用 json.dumps()：只要返回字典或 Pydantic 模型，它会自动序列化为 JSON 响应。
- 模块导入路径：在项目根目录运行时，Python 包路径为 folder.subfolder.module。
- --reload 是开发神器：代码保存后服务自动重启，无需手动停止/启动。

# 启动服务
uvicorn week1.day2.app:app --reload

# 访问接口
curl http://localhost:8000/task/today