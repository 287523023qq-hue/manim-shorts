"""
叙事转影视编译器 (CNC - Cinematic Semantic Compiler)
以及三层输出生成器 (L1 审查 / L2 视频大模型 15 模块 / L3 剪辑与 Manim 强类型 IR)
遵循 CSCA 主公式：
WORLD STATE + TRANSITION (MUS) -> PERCEPTION DESIGN -> CINEMATIC STRATEGY -> 15-MODULE HELL GRIND
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from manim_shorts.world_model.world_model import WorldState
from manim_shorts.world_model.transformation import MUS, MSSS, NarrativeProportion, PacingLock


@dataclass
class HellGrind15Modules:
    """Hell Grind 15 模块工业级提示词包 (L2 层专属，绝不泄露渲染提示内部字段)"""
    scene_context: str
    active_references: str
    location_map: str
    first_frame_spatial_blocking: str
    format_mode: str = "vertical 9:16, 24fps high bitrate, photorealistic cinematic grade"
    optics: str = "85mm prime lens, f/1.8 shallow depth of field, subtle chromatic aberration"
    camera: str = "slow smooth dolly push-in along optical axis, no internal cuts"
    action_timing: str = "0.0s-2.0s hold, 2.0s-6.0s primary character action, 6.0s-7.5s settle"
    physics: str = "realistic fabric drape, natural gravity, wind driven snow particle drift"
    lighting: str = "cold ambient dawn, 20-degree hard keylight, rich volumetric atmosphere"
    audio: str = "ambient wind howl, soft footstep on crusted snow, distant bell chime"
    character_acting: str = "subtle micro-expression, controlled breathing, stoic demeanor"
    style: str = "classical xianxia cinematic realism, restrained palette, teal-amber tone"
    quality: str = "masterpiece 8k render, razor sharp focal plane, immaculate texture"
    positive_constraints: str = "exact single character, continuous camera path, perfect anatomy"

    def compile_l2_prompt(self) -> str:
        """编译为标准 15 模块文本，可直接喂给视频生成大模型"""
        blocks = [
            f"[[ MODULE SCENE_CONTEXT ]]\n{self.scene_context}",
            f"[[ MODULE ACTIVE_REFERENCES ]]\n{self.active_references}",
            f"[[ MODULE LOCATION_MAP ]]\n{self.location_map}",
            f"[[ MODULE FIRST_FRAME_AND_SPATIAL_BLOCKING ]]\n{self.first_frame_spatial_blocking}",
            f"[[ MODULE FORMAT_MODE ]]\n{self.format_mode}",
            f"[[ MODULE OPTICS ]]\n{self.optics}",
            f"[[ MODULE CAMERA ]]\n{self.camera}",
            f"[[ MODULE ACTION_TIMING ]]\n{self.action_timing}",
            f"[[ MODULE PHYSICS ]]\n{self.physics}",
            f"[[ MODULE LIGHTING ]]\n{self.lighting}",
            f"[[ MODULE AUDIO ]]\n{self.audio}",
            f"[[ MODULE CHARACTER_ACTING ]]\n{self.character_acting}",
            f"[[ MODULE STYLE ]]\n{self.style}",
            f"[[ MODULE QUALITY ]]\n{self.quality}",
            f"[[ MODULE POSITIVE_CONSTRAINTS ]]\n{self.positive_constraints}"
        ]
        return "\n\n".join(blocks)


@dataclass
class ThreeTierShotOutput:
    """三层解耦输出 (film-dsl v2.1 规范)"""
    shot_id: str
    shot_no: int
    duration_seconds: float
    
    # L1: ~200B 导演极简审查层
    l1_review_card: Dict[str, Any]
    
    # L2: ~2KB 视频模型生成包 (15 Modules, 自然语言，零 L3 参数泄露)
    l2_render_modules: HellGrind15Modules
    
    # L3: ~4KB 剪辑后期与 Manim 强类型 IR (包含时间线、EDL、几何安全区)
    l3_typed_ir: Dict[str, Any]


class CNCCompiler:
    """
    叙事转影视编译器 (Cinematic Semantic Compiler)
    """

    def __init__(self, world_name: str, genre_preset: str = "@preset_classical_xianxia_v1"):
        self.world_name = world_name
        self.genre_preset = genre_preset

    def compile_mus_to_shots(self, mus: MUS, msss: MSSS, state: WorldState) -> List[ThreeTierShotOutput]:
        """
        核心编译步骤：
        MUS (世界状态迁移) -> 感知设计 -> 视听动力学 -> L1/L2/L3 三层输出
        """
        shots = []
        duration_per_shot = msss.pacing.container_duration_seconds / max(1, msss.candidate_shot_count)

        for i in range(msss.candidate_shot_count):
            shot_no = i + 1
            shot_id = f"SH_{shot_no:02d}"

            # 1. L1 极简审查卡 (约 200 Bytes)
            l1 = {
                "shot_id": shot_id,
                "beat": mus.trigger_event,
                "duration": f"{duration_per_shot:.1f}s",
                "scale": "medium_shot",
                "motion": msss.camera_movement_strategy,
                "tension": mus.dramatic_intensity
            }

            # 2. L2 15-Module 工业级提示词包 (约 2 KB)
            l2 = HellGrind15Modules(
                scene_context=f"Single continuous take. Container duration: {duration_per_shot:.1f}s. Real time. {mus.trigger_event}",
                active_references=f"World: {self.world_name}. State: {state.time_label}.",
                location_map=f"Space: {state.environment['space_type']}. 180-degree axis locked.",
                first_frame_spatial_blocking=f"Shot {shot_no} — spatial anchor at center safe stage.",
                camera=msss.camera_movement_strategy,
                action_timing=f"0s-1s establish, 1s-{duration_per_shot-1:.1f}s transition, {duration_per_shot-1:.1f}s settle."
            )

            # 3. L3 强类型 IR 与 Manim 联动参数 (约 4 KB)
            l3 = {
                "shot_id": shot_id,
                "timecode_in": f"00:00:{(i * duration_per_shot):04.1f}",
                "timecode_out": f"00:00:{((i + 1) * duration_per_shot):04.1f}",
                "duration_frames": int(duration_per_shot * 24),
                "manim_safe_zone": {
                    "center": [0.0, -0.4, 0.0],
                    "width": 6.0,
                    "height": 5.6
                },
                "post_intent": {
                    "trim_priority": "trim_tail",
                    "slip_allowed": False
                },
                "world_provenance": {
                    "mus_id": mus.mus_id,
                    "state_timestamp": state.timestamp_step
                }
            }

            shots.append(ThreeTierShotOutput(
                shot_id=shot_id,
                shot_no=shot_no,
                duration_seconds=duration_per_shot,
                l1_review_card=l1,
                l2_render_modules=l2,
                l3_typed_ir=l3
            ))

        return shots
