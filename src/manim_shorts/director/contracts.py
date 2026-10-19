"""
全链路时空影视导演协议 (Spatiotemporal Directing Contracts)
融合：
1. Nano-Banana 静态视觉资产锁定 (Identity Lock & Visual Continuity)
2. 40 类电影镜头 7 槽位运动物理合同 (Camera Motion Contract & Repair Guide)
3. 9:16 坚戈竖屏移动端注意力心流 (Hook -> Deduction -> Aha -> CTA)
4. Manim 严谨几何动画 + ComfyUI/Wan2.1 电影级画面双图层协同 (Hybrid Dual-Layer)
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Dict, Any


class NarrativeBeat(str, Enum):
    """短视频 4 段式爆款叙事心流拍子"""
    HOOK = "hook"                # 0~3s 黄金抓眼球/反直觉痛点
    DEDUCTION = "deduction"      # 3~18s 逻辑推导/动态展开
    AHA_MOMENT = "aha_moment"    # 18~25s 顿悟时刻/认知重塑/高光结论
    CALL_TO_ACTION = "cta"       # 25~30s 引导争论/思考/互动


class CameraMechanism(str, Enum):
    """消歧物理运镜机制"""
    PUSH_IN = "push_in"                  # 沿光轴平移推进 (靠近情绪)
    PULL_OUT = "pull_out"                # 沿光轴平移拉远 (交代宏观环境)
    CRASH_ZOOM = "crash_zoom"            # 快速冲入/冲击变焦 (强调冲击)
    VERTIGO_ZOOM = "vertigo_zoom"        # 眩晕变焦 (Dolly Zoom: 移动+反向变焦，空间扭曲)
    MACRO_DEEP = "macro_deep"            # 宏观深入至微观结构
    REVEAL_OBSTACLE = "reveal_obstacle"  # 遮挡物后移出揭示主体
    RACK_FOCUS = "rack_focus"            # 固定机位前后景拉焦 (转移注意力)
    TRACKING_SLIDE = "tracking_slide"    # 滑轨水平横移 (产生深度视差)
    ORBIT_ARC = "orbit_arc"              # 半环绕/大弧线绕行 (立体展示，严禁主体自转)
    PEDESTAL_VERTICAL = "pedestal_vert"  # 垂直升降机位 (气势展开/贴地压迫)
    FOLLOW_RETREAT = "follow_retreat"    # 倒退跟拍 (等速边退边讲)
    WHIP_PAN = "whip_pan"                # 快速甩镜转场 (运动模糊硬切)


@dataclass
class VisualIdentityLock:
    """静态视觉资产与角色一致性锁定 (Nano-Banana 架构)"""
    subject_name: str
    face_and_silhouette: str             # 脸型与剪影轮廓
    color_palette: str                   # 核心主色与辅助色
    wardrobe_and_props: str              # 服饰、配饰或物理标志
    render_style: str                    # 渲染艺术风格 (如: 极简暗黑粒子 / 赛博写实 / 柔和黏土 / 电影级光追)
    proportions: str = "标准比例，轮廓清晰"
    negative_drift_locks: List[str] = field(default_factory=lambda: [
        "禁止发型服饰变化", "禁止脸部特征漂移", "禁止画面出现多余水印或文字"
    ])

    def to_identity_prompt(self) -> str:
        """编译为一致性锁定语句"""
        return (
            f"【角色与视觉锁定】主体: {self.subject_name}; "
            f"外观与剪影: {self.face_and_silhouette}; "
            f"色彩基调: {self.color_palette}; "
            f"材质与风格: {self.render_style}; "
            f"严格约束: {', '.join(self.negative_drift_locks)}。"
        )


@dataclass
class CameraMotionContract:
    """
    7 槽位电影镜头运动物理合同 (Cinematic Shot Contract)
    让运镜具备数学级的确定性，杜绝“电影感”、“高级感”等模糊形容词。
    """
    start_framing: str                   # 槽位1: 起始构图与景别 (如: 人物腰部中景 / 低角度微距全景)
    mechanism: CameraMechanism           # 槽位2: 物理运镜机制
    path_and_direction: str              # 槽位3: 几何路径与方向 (如: 沿光轴前推并向左轻微平移)
    speed_curve: str                     # 槽位4: 速度曲线与制动 (如: 匀速前进，最后0.5秒平稳减速停住)
    end_framing: str                     # 槽位5: 终止构图与清晰落点 (如: 面部眼部特写，瞳孔锐利)
    subject_locks: str                   # 槽位6: 主体动作与屏幕坐标锁定 (如: 主体保持画面中心，动作微幅)
    environment_response: str            # 槽位7: 环境视差与物理反馈 (如: 前景光斑快速掠过，背景星云缓慢位移)
    keyframe_strategy: str = "单参考图生成" # 关键帧策略 (单图 / 首尾双帧 / 跨尺度中间关键帧)
    targeted_constraints: List[str] = field(default_factory=list)

    def compile_motion_prompt(self, has_reference_image: bool = True) -> str:
        """
        编译为 AI 视频大模型 (Wan2.1 / HunyuanVideo / Sora / Runway) 可执行的自然语言提示词
        """
        prompt_parts = []
        
        # 1. 镜头指令在最前
        motion_core = (
            f"相机从{self.start_framing}开始，"
            f"采用{self.mechanism.value}机制，{self.path_and_direction}，"
            f"{self.speed_curve}，最终稳定停在{self.end_framing}。"
        )
        prompt_parts.append(motion_core)
        
        # 2. 主体状态约束
        prompt_parts.append(f"主体要求: {self.subject_locks}。")
        
        # 3. 环境视差与物理响应
        prompt_parts.append(f"环境响应: {self.environment_response}。")
        
        # 4. 关键针对性约束
        if self.targeted_constraints:
            prompt_parts.append(f"物理约束: {', '.join(self.targeted_constraints)}。")
            
        return "".join(prompt_parts)


@dataclass
class DirectorShot:
    """
    全链路双层分镜镜头定义
    """
    shot_index: int
    beat: NarrativeBeat
    duration_seconds: float
    screen_ratio: str = "9:16"           # 默认 9:16 移动竖屏
    voiceover_script: str = ""           # 旁白台词
    subtitle_text: str = ""              # 字幕文本
    
    # 视觉与运镜
    identity_lock: Optional[VisualIdentityLock] = None
    motion_contract: Optional[CameraMotionContract] = None
    
    # 双层渲染定义 (Manim 几何数据层 + ComfyUI 电影级 AI 层)
    manim_layer_spec: str = ""           # Manim 前景安全区组件 (公式、图表、卡片)
    comfy_ai_layer_spec: str = ""        # ComfyUI 背景/主体生成 Prompt
    
    def to_production_dict(self) -> Dict[str, Any]:
        """导出为结构化生产数据包"""
        motion_prompt = self.motion_contract.compile_motion_prompt() if self.motion_contract else ""
        identity_prompt = self.identity_lock.to_identity_prompt() if self.identity_lock else ""
        
        return {
            "shot_index": self.shot_index,
            "beat": self.beat.value,
            "duration": f"{self.duration_seconds}s",
            "ratio": self.screen_ratio,
            "voiceover": self.voiceover_script,
            "subtitle": self.subtitle_text,
            "visual_identity_prompt": identity_prompt,
            "camera_motion_prompt": motion_prompt,
            "keyframe_strategy": self.motion_contract.keyframe_strategy if self.motion_contract else "单图",
            "manim_foreground": self.manim_layer_spec,
            "comfyui_background": self.comfy_ai_layer_spec or motion_prompt
        }
