import json

from datetime import datetime


# print("我的 Python 环境正常")

# 用字典表示一个 AI 学习任务
# task = {
#     "task_id": "learn_20260317",
#     "description": "学习如何定义 Python 类",
#     "status": "pending",
#     "created_at": "2026-03-17"
# }
#
# # 打印整个任务
# print("任务内容：")
# print(task)
#
# # 打印任务描述
# print("\n📝 任务描述：", task["description"])

# 定义一个“任务”模具
class AITask:
    def __init__(self, task_id, description):
        self.task_id = task_id
        self.description = description
        self.status = "pending"
        self.created_at = datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        """把对象转成字典"""
        return {
            "task_id": self.task_id,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at
        }

    def to_json(self):
        """把对象转成json字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)


# # 用模具做一个具体任务
# my_task = AITask(
#     task_id="learn_20260317",
#     description="学习 Python 类的基本用法"
# )
#
# # 打印任务信息
# print("任务ID:", my_task.task_id)
# print("任务描述:", my_task.description)
# print("状态:", my_task.status)

my_task = AITask("learn_today", "完成 Day1 学习")
print(my_task.to_json())