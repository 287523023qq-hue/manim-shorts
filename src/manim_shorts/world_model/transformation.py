"""
世界状态迁移与场景序列规范 (MUS & MSSS)
MUS: Minimum Meaningful World Transformation Unit (最小有效世界变换单元)
由世界状态迁移驱动，而非文本长度或段落。
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from manim_shorts.world_model.world_model import WorldState


@dataclass
class NarrativeProportion:
    """五轴叙事比重 (film-dsl v2.1 规范)"""
    visual: float = 0.50     # 视觉画面比重
    silence: float = 0.15    # 留白/静音比重 (留白亦是内容)
    sound: float = 0.15      # 声音音效比重
    action: float = 0.15     # 动作与形体比重
    dialogue: float = 0.05   # 对白比重 (克制对白，视觉为主)


@dataclass
class PacingLock:
    """节奏与剪辑锁"""
    target_asl_seconds: float = 4.0      # 平均镜头时长 (Average Shot Length)
    container_duration_seconds: float = 30.0 # 标准容器时长 (如30秒小周天)
    silence_ratio: float = 0.15
    hard_cut_ratio: float = 0.80
    transition_frames: int = 24          # 转场默认帧数


@dataclass
class MUS:
    """
    最小有效世界变换单元 (Minimum Meaningful World Transformation Unit)
    """
    mus_id: str
    from_state_step: int
    to_state_step: int
    trigger_event: str
    entity_delta: Dict[str, Any]         # 发生了改变的实体状态
    relation_delta: List[str]            # 新增或断裂的关系
    narrative_significance: str          # 戏剧重要性与因果意义
    dramatic_intensity: float = 0.5      # 戏剧张力 (0.0 ~ 1.0)


@dataclass
class MSSS:
    """
    场景序列规范 (Meta Scene-Sequence Spec)
    负责将 MUS 的世界变换转化为候选影视镜头序列
    """
    msss_id: str
    target_mus_id: str
    pacing: PacingLock
    proportion: NarrativeProportion
    candidate_shot_count: int
    camera_movement_strategy: str        # 整体运镜感知策略
    audio_beat_refs: List[str] = field(default_factory=list) # 锚定音频节拍点
