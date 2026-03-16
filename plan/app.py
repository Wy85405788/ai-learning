import os
import json
import csv
from datetime import datetime, date
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

_plan_cache = None  # 全局缓存
def get_cached_plan():
    global _plan_cache
    if _plan_cache is None:
        _plan_cache = load_plan()  # 只读一次
    return _plan_cache

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

DATA_DIR = "data"
PLAN_FILE = os.path.join(DATA_DIR, "plan.csv")
PROGRESS_FILE = os.path.join(DATA_DIR, "progress.json")

os.makedirs(DATA_DIR, exist_ok=True)

# 初始化 progress.json(如果不存在)
if not os.path.exists(PROGRESS_FILE):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f)



def load_plan():
    print(f"正在读取计划文件: {os.path.abspath(PLAN_FILE)}")  # 👈 加这行
    if not os.path.exists(PLAN_FILE):
        print("❌ plan.csv 不存在！")
        return []
    plan = []
    try:
        with open(PLAN_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                plan.append(row)
        print(f"✅ 成功加载 {len(plan)} 条计划")
    except Exception as e:
        print(f"❌ 读取CSV出错: {e}")
        return []
    return plan


def load_progress():
    with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_progress(data):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    plan = get_cached_plan()  # ← 使用缓存
    progress = load_progress()

    today_str = str(date.today())
    enriched_plan = []
    completed_weight = 0.0

    for item in plan:
        date_key = item.get("Date") or item.get("date")
        if not date_key:
            continue
        prog = progress.get(date_key, {})
        item["progress"] = prog.get("value", 0)
        item["note"] = prog.get("note", "")
        item["is_today"] = (date_key == today_str)
        enriched_plan.append(item)
        completed_weight += item["progress"] / 100.0

    total_tasks = len(enriched_plan)
    overall_percent = round(completed_weight / total_tasks * 100, 1) if total_tasks > 0 else 0.0

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "plan": enriched_plan,
            "overall_percent": overall_percent,
            "today": today_str
        }
    )

@app.post("/update_progress")
async def update_progress(request: Request):
    data = await request.json()
    date_key = data["date"]
    value = int(data["value"])
    note = data.get("note", "")

    progress = load_progress()
    progress[date_key] = {"value": value, "note": note}
    save_progress(progress)
    return JSONResponse({"status": "ok"})

def refresh_progress():
    plan = get_cached_plan()  # ← 使用缓存
    progress = load_progress()

    today_str = str(date.today())
    enriched_plan = []
    completed_weight = 0.0

    for item in plan:
        date_key = item.get("Date") or item.get("date")
        if not date_key:
            continue
        prog = progress.get(date_key, {})
        item["progress"] = prog.get("value", 0)
        item["note"] = prog.get("note", "")
        item["is_today"] = (date_key == today_str)
        enriched_plan.append(item)
        completed_weight += item["progress"] / 100.0

    total_tasks = len(enriched_plan)
    overall_percent = round(completed_weight / total_tasks * 100, 1) if total_tasks > 0 else 0.0