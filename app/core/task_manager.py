import uuid
import threading
import time
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, Any, Optional, List


class TaskStatus(Enum):
    PENDING = 'pending'
    RUNNING = 'running'
    COMPLETED = 'completed'
    FAILED = 'failed'


@dataclass
class TaskProgress:
    """任务进度信息"""
    task_id: str
    status: TaskStatus
    progress: float
    message: str
    logs: List[str]
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['status'] = self.status.value
        return data


class TaskManager:
    """任务管理器 - 管理后台任务和进度"""
    
    def __init__(self):
        self.tasks: Dict[str, TaskProgress] = {}
        self.lock = threading.RLock()
    
    def create_task(self) -> str:
        """创建新任务"""
        task_id = str(uuid.uuid4())
        
        with self.lock:
            self.tasks[task_id] = TaskProgress(
                task_id=task_id,
                status=TaskStatus.PENDING,
                progress=0.0,
                message='等待开始...',
                logs=[],
                started_at=None,
                completed_at=None
            )
        
        return task_id
    
    def start_task(self, task_id: str, message: str = '开始执行...'):
        """标记任务开始"""
        with self.lock:
            if task_id in self.tasks:
                self.tasks[task_id].status = TaskStatus.RUNNING
                self.tasks[task_id].message = message
                self.tasks[task_id].started_at = time.time()
                self._add_log(task_id, f'▶️ {message}')
    
    def update_progress(self, task_id: str, progress: float, message: str, 
                       add_log: bool = True):
        """更新任务进度"""
        with self.lock:
            if task_id in self.tasks:
                self.tasks[task_id].progress = min(max(progress, 0.0), 1.0)
                self.tasks[task_id].message = message
                if add_log:
                    self._add_log(task_id, message)
    
    def complete_task(self, task_id: str, result: Dict[str, Any], message: str = '完成'):
        """标记任务完成"""
        with self.lock:
            if task_id in self.tasks:
                self.tasks[task_id].status = TaskStatus.COMPLETED
                self.tasks[task_id].progress = 1.0
                self.tasks[task_id].message = message
                self.tasks[task_id].result = result
                self.tasks[task_id].completed_at = time.time()
                self._add_log(task_id, f'✅ {message}')
    
    def fail_task(self, task_id: str, error: str, message: str = '失败'):
        """标记任务失败"""
        with self.lock:
            if task_id in self.tasks:
                self.tasks[task_id].status = TaskStatus.FAILED
                self.tasks[task_id].message = message
                self.tasks[task_id].error = error
                self.tasks[task_id].completed_at = time.time()
                self._add_log(task_id, f'❌ {error}')
    
    def get_progress(self, task_id: str) -> Optional[TaskProgress]:
        """获取任务进度"""
        with self.lock:
            return self.tasks.get(task_id)
    
    def get_all_tasks(self) -> List[TaskProgress]:
        """获取所有任务"""
        with self.lock:
            return list(self.tasks.values())
    
    def clear_task(self, task_id: str):
        """清除任务"""
        with self.lock:
            if task_id in self.tasks:
                del self.tasks[task_id]
    
    def clear_old_tasks(self, max_age_seconds: int = 3600):
        """清除旧任务"""
        current_time = time.time()
        with self.lock:
            to_remove = []
            for task_id, task in self.tasks.items():
                if task.completed_at and (current_time - task.completed_at > max_age_seconds):
                    to_remove.append(task_id)
            
            for task_id in to_remove:
                del self.tasks[task_id]
    
    def _add_log(self, task_id: str, log_message: str):
        """添加日志条目"""
        if task_id in self.tasks:
            timestamp = time.strftime('%H:%M:%S')
            self.tasks[task_id].logs.append(f'[{timestamp}] {log_message}')
            
            # 限制日志数量
            if len(self.tasks[task_id].logs) > 100:
                self.tasks[task_id].logs = self.tasks[task_id].logs[-100:]


# 全局任务管理器实例
task_manager = TaskManager()
