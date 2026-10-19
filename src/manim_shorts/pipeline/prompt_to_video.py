"""
对话式提示词到视频生成引擎 (Chat-to-Video Engine)
实现：
用户在对话栏输入一句话或一段提示词 -> 自动语义推演与 15-Module 编译 -> 组装 ComfyUI API 图 -> 触发生成与双层合成
"""

import os
import json
import re
import random
from typing import Dict, Any, Optional, Tuple
from pathlib import Path

from manim_shorts.director.contracts import (
    NarrativeBeat, CameraMechanism, VisualIdentityLock,
    CameraMotionContract, DirectorShot
)
from manim_shorts.world_model.compiler import HellGrind15Modules
from manim_shorts.comfyui.client import ComfyUIClient
from manim_shorts.pipeline.compositor import HybridVideoCompositor


class ChatToVideoEngine:
    def __init__(self, project_root: str = "/Users/guopeng/manim-shorts"):
        self.project_root = Path(project_root)
        self.template_dir = self.project_root / "src/manim_shorts/comfyui/templates"
        self.output_dir = self.project_root / "output"
        self.comfy_client = ComfyUIClient()
        self.compositor = HybridVideoCompositor(str(self.output_dir / "composited"))
        os.makedirs(self.output_dir / "payloads", exist_ok=True)
        os.makedirs(self.output_dir / "videos/comfyui", exist_ok=True)

    def parse_user_prompt(self, user_text: str) -> Dict[str, Any]:
        """
        从用户口语化自然语言中智能提取关键影视参数
        """
        # 1. 时长提取 (如 "5秒", "8s")
        duration = 5.0
        dur_match = re.search(r"(\d+(\.\d+)?)\s*(秒|s|second)", user_text, re.IGNORECASE)
        if dur_match:
            duration = float(dur_match.group(1))

        # 2. 画幅提取 (9:16 或 16:9)
        aspect_ratio = "9:16"
        width, height = 540, 960
        if "16:9" in user_text or "横屏" in user_text:
            aspect_ratio = "16:9"
            width, height = 960, 540

        # 3. 运镜机制推演
        mechanism = "dolly push-in"
        camera_desc = "smooth dolly push-in along optical axis, continuous tracking"
        if "拉远" in user_text or "后退" in user_text:
            mechanism = "dolly pull-out"
            camera_desc = "smooth pull-out along optical axis, revealing expansive environment"
        elif "横移" in user_text or "滑轨" in user_text:
            mechanism = "tracking slide"
            camera_desc = "smooth horizontal tracking slide, establishing rich foreground parallax"
        elif "环绕" in user_text:
            mechanism = "orbital arc"
            camera_desc = "controlled 180-degree orbital pan around static subject, continuous parallax"
        elif "冲入" in user_text or "冲击" in user_text:
            mechanism = "crash zoom"
            camera_desc = "high speed crash zoom into target with elegant deceleration settle"

        # 4. 艺术风格与核心意向
        style = "cinematic photorealism, teal and amber grade, subtle volumetric dust"
        if "二次元" in user_text or "动漫" in user_text:
            style = "high quality anime aesthetic, Makoto Shinkai style sky, vivid vibrant tones"
        elif "仙侠" in user_text or "古风" in user_text:
            style = "classical oriental xianxia realism, silk and mist atmosphere, ink wash undertones"
        elif "科幻" in user_text or "太空" in user_text:
            style = "hard sci-fi aesthetic, interstellar accretion glow, deep obsidian void, anamorphic flare"

        return {
            "raw_text": user_text,
            "duration": duration,
            "aspect_ratio": aspect_ratio,
            "width": width,
            "height": height,
            "mechanism": mechanism,
            "camera_desc": camera_desc,
            "style": style
        }

    def compile_15_modules(self, params: Dict[str, Any]) -> HellGrind15Modules:
        """
        自动将用户一句话扩展为完备严密的 15 模块工业级提示词
        """
        raw = params["raw_text"]
        dur = params["duration"]
        ratio = params["aspect_ratio"]
        cam = params["camera_desc"]
        style = params["style"]

        return HellGrind15Modules(
            scene_context=f"Single continuous take. Container duration: {dur}s. Aspect ratio: {ratio}. Real time. Prompt: {raw}",
            active_references=f"Subject locked based on query: {raw[:50]}. Consistent anatomical proportions, no morphing.",
            location_map="Defined 3D space, key light from frame-left, balanced fill, 180-degree axis strictly preserved.",
            first_frame_spatial_blocking=f"Shot 01 ({dur}s) — subject anchored at safe stage center, clear depth separation.",
            format_mode=f"vertical {ratio}, 24fps high bitrate, photorealistic cinema render, zero artifacts",
            optics="85mm prime lens, shallow depth of field, f/1.8 aperture, natural bokeh",
            camera=cam,
            action_timing=f"0s-1s establish, 1s-{dur-1}s continuous evolution, {dur-1}s-{dur}s settle",
            physics="realistic gravity, fluid dynamic flow, light scattering and atmospheric depth",
            lighting="volumetric cinematic lighting, balanced key-to-fill ratio, soft shadows",
            audio="ambient soundscape matching visual tone, subtle cinematic atmosphere",
            character_acting="natural breathing and micro-movements, controlled poise",
            style=style,
            quality="masterpiece 8k render, razor-sharp focal plane, impeccable physical realism",
            positive_constraints="exact single subject, continuous smooth motion path, zero internal cuts"
        )

    def generate_video(
        self,
        user_prompt: str,
        input_image: Optional[str] = None,
        seed: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        核心对外入口：输入对话一句话 -> 全流程出片或生成准备
        """
        params = self.parse_user_prompt(user_prompt)
        modules = self.compile_15_modules(params)
        compiled_l2_prompt = modules.compile_l2_prompt()
        shot_seed = seed if seed is not None else random.randint(100000, 999999)

        # 选用文生视频 (T2V) 或图生视频 (I2V) 模板
        is_i2v = input_image is not None and os.path.exists(input_image)
        template_name = "wan21_i2v_api.json" if is_i2v else "wan21_t2v_api.json"
        with open(self.template_dir / template_name, "r", encoding="utf-8") as f:
            api_graph = json.load(f)

        # 动态组装 API Graph 节点
        fps = 24
        total_frames = max(17, int(params["duration"] * fps))

        if is_i2v:
            api_graph["1"]["inputs"]["image"] = input_image
            api_graph["2"]["inputs"]["text"] = compiled_l2_prompt
            api_graph["8"]["inputs"]["seed"] = shot_seed
            api_graph["11"]["inputs"]["filename_prefix"] = "chat2video_i2v"
        else:
            api_graph["1"]["inputs"]["text"] = compiled_l2_prompt
            api_graph["6"]["inputs"]["width"] = params["width"]
            api_graph["6"]["inputs"]["height"] = params["height"]
            api_graph["6"]["inputs"]["length"] = total_frames
            api_graph["7"]["inputs"]["seed"] = shot_seed
            api_graph["10"]["inputs"]["filename_prefix"] = "chat2video_t2v"

        # 保存为独立可执行的 Payload JSON
        slug = re.sub(r"[^\w\u4e00-\u9fa5]+", "_", user_prompt)[:20].strip("_") or "shot"
        payload_filename = f"chat2video_{slug}_{shot_seed}.json"
        payload_path = self.output_dir / "payloads" / payload_filename
        with open(payload_path, "w", encoding="utf-8") as f:
            json.dump(api_graph, f, ensure_ascii=False, indent=2)

        # 尝试与 ComfyUI 交互
        is_online = self.comfy_client.is_alive()
        status_msg = ""
        prompt_id = ""

        if is_online:
            success, msg, res = self.comfy_client.queue_prompt(api_graph)
            status_msg = msg
            prompt_id = res.get("prompt_id", "")
        else:
            status_msg = (
                f"ComfyUI 服务未在 http://127.0.0.1:8188 运行。"
                f"已为你自动生成高精度标准 API 载荷: {payload_path}。"
                f"启动 ComfyUI 后可一键执行，或直接将 JSON 拖入界面！"
            )

        return {
            "user_prompt": user_prompt,
            "parsed_params": params,
            "seed": shot_seed,
            "compiled_prompt": compiled_l2_prompt,
            "payload_path": str(payload_path),
            "comfyui_online": is_online,
            "prompt_id": prompt_id,
            "status": status_msg
        }
