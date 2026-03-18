# schemas.py
from typing import Literal

from pydantic import BaseModel

class AITask(BaseModel):
    id: int
    description: str
    status: str
    priority: Literal["高", "中", "低"]  # 实际可加 Literal["高", "中", "低"]
    estimated_hours: int
    tags: list[str]
    created_at: str