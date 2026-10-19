"""
ComfyUI API 自动化客户端 (ComfyUI Python Bridge)
负责：
1. 与本地或远程 ComfyUI (默认 http://127.0.0.1:8188) 建立连接
2. 注入 DirectorEngine 生成的 L2 15-Module 提示词与人设垫图
3. 自动提交任务、轮询进度、下载生成的背景视频
4. 若 ComfyUI 未启动，优雅降级并输出可执行 payload.json
"""

import json
import urllib.request
import urllib.error
import urllib.parse
import os
import time
from typing import Dict, Any, Optional, Tuple


class ComfyUIClient:
    def __init__(self, host: str = "http://127.0.0.1:8188"):
        self.host = host.rstrip("/")

    def is_alive(self) -> bool:
        """检查 ComfyUI 是否在线"""
        try:
            req = urllib.request.Request(f"{self.host}/system_stats", headers={"User-Agent": "ManimShorts/1.0"})
            with urllib.request.urlopen(req, timeout=2.0) as resp:
                return resp.status == 200
        except Exception:
            return False

    def queue_prompt(self, workflow_prompt: Dict[str, Any], client_id: str = "manim_shorts_client") -> Tuple[bool, str, Dict[str, Any]]:
        """
        提交工作流至 ComfyUI 队列
        """
        if not self.is_alive():
            fallback_path = "output/comfyui_offline_payload.json"
            os.makedirs("output", exist_ok=True)
            with open(fallback_path, "w", encoding="utf-8") as f:
                json.dump(workflow_prompt, f, ensure_ascii=False, indent=2)
            return False, f"ComfyUI 服务未在 {self.host} 启动。已将当前任务载荷保存至: {fallback_path}", {}

        try:
            payload = json.dumps({"prompt": workflow_prompt, "client_id": client_id}).encode("utf-8")
            req = urllib.request.Request(
                f"{self.host}/prompt",
                data=payload,
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=10.0) as resp:
                res_data = json.loads(resp.read().decode("utf-8"))
                prompt_id = res_data.get("prompt_id", "")
                return True, f"已成功提交任务至 ComfyUI! 任务 ID: {prompt_id}", res_data
        except Exception as e:
            return False, f"提交 ComfyUI 异常: {str(e)}", {}

    def wait_for_execution(self, prompt_id: str, timeout_seconds: int = 300) -> Optional[Dict[str, Any]]:
        """
        轮询查询任务执行历史与输出文件
        """
        start_time = time.time()
        while time.time() - start_time < timeout_seconds:
            try:
                req = urllib.request.Request(f"{self.host}/history/{prompt_id}")
                with urllib.request.urlopen(req, timeout=5.0) as resp:
                    history = json.loads(resp.read().decode("utf-8"))
                    if prompt_id in history:
                        return history[prompt_id]
            except Exception:
                pass
            time.sleep(2.0)
        return None
