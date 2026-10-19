"""
ComfyUI 工作流动态适配器 (Workflow Adapter)
将 DirectorEngine 产出的 L2 15-Module 提示词与时序参数动态注入到 ComfyUI 画布节点图中
"""

import json
import copy
from typing import Dict, Any
from manim_shorts.director.contracts import DirectorShot


class ComfyUIWorkflowAdapter:
    def __init__(self, template_workflow_path: str = "comfyui_workflows/wan21_hunyuan_production_pipeline.json"):
        with open(template_workflow_path, "r", encoding="utf-8") as f:
            self.template = json.load(f)

    def inject_shot(self, shot: DirectorShot, fps: int = 24) -> Dict[str, Any]:
        """
        为单个镜头动态编译 ComfyUI 工作流参数
        """
        workflow = copy.deepcopy(self.template)
        
        # 编译 L2 提示词
        l2_prompt = shot.comfy_ai_layer_spec
        if not l2_prompt and shot.motion_contract:
            l2_prompt = shot.motion_contract.compile_motion_prompt()
            if shot.identity_lock:
                l2_prompt = f"{shot.identity_lock.to_identity_prompt()}\n\n{l2_prompt}"

        # 帧数计算 (时长 x fps)
        total_frames = int(shot.duration_seconds * fps)

        # 遍历节点注入参数
        for node in workflow.get("nodes", []):
            title = node.get("title", "")
            node_type = node.get("type", "")

            # 注入正向提示词
            if "正向提示词" in title or (node_type == "CLIPTextEncode" and node.get("id") == 1):
                node["widgets_values"][0] = l2_prompt

            # 注入帧数与分辨率
            if "空潜空间" in title or node_type == "EmptyHunyuanLatentVideo":
                # width, height, num_frames, batch_size
                node["widgets_values"] = [540, 960, max(17, total_frames), 1]

            # 注入输出文件名前缀
            if "VHS_VideoCombine" in node_type or "视频封装" in title:
                if isinstance(node.get("widgets_values"), dict):
                    node["widgets_values"]["filename_prefix"] = f"shot_{shot.shot_index:02d}_{shot.beat.value}"
                    node["widgets_values"]["frame_rate"] = fps

        return workflow
