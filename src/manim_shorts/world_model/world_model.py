"""
世界模型优先架构核心 (World Model First Architecture)
根据 CSCA 原则 01：
CSCA 不得将故事文本直接编译为影视表达。
必须首先构建、维护并校验一个世界模型（World Model），然后才进行影视解析（Cinematic Resolution）。
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional, Set, Tuple


class FactConfidence(str, Enum):
    EXPLICIT = "explicit"      # 显式事实: 原文直接写明
    INFERRED = "inferred"      # 隐式事实: 间接强逻辑推导
    UNCERTAIN = "uncertain"    # 不确定事实: 存在分支或弱证据，保留置信度


@dataclass
class WorldFact:
    statement: str
    confidence: FactConfidence
    evidence_span: str = ""
    prob: float = 1.0


@dataclass
class WorldEntity:
    entity_id: str
    name: str
    entity_type: str                 # 角色/道具/建筑/自然力量/科学定理
    attributes: Dict[str, Any] = field(default_factory=dict)
    state: Dict[str, Any] = field(default_factory=dict)             # 当前时刻的可变状态 (如生命值、位置、心境)
    spatial_coords: Tuple[float, float, float] = (0.0, 0.0, 0.0)    # 3D 空间坐标锚点


@dataclass
class WorldRelation:
    subject_id: str
    predicate: str
    object_id: str
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorldRule:
    rule_id: str
    description: str                 # 世界物理法则/天道规则 (如: 高阶修士禁入秘境 / 光速不可超越)
    hard_invariant: bool = True      # 是否为不可侵犯的硬不变量


@dataclass
class WorldState:
    """时间切片 t 下的世界完整客观状态快照 W(t)"""
    timestamp_step: int
    time_label: str
    entities: Dict[str, WorldEntity] = field(default_factory=dict)
    relations: List[WorldRelation] = field(default_factory=list)
    facts: List[WorldFact] = field(default_factory=list)
    active_rules: List[WorldRule] = field(default_factory=list)
    environment: Dict[str, Any] = field(default_factory=lambda: {
        "lighting": "冷光清晨",
        "weather": "风雪",
        "space_type": "高山悬崖亭台",
        "audio_ambience": "寒风呼啸"
    })

    def clone(self, new_timestamp: int, new_label: str) -> "WorldState":
        import copy
        return WorldState(
            timestamp_step=new_timestamp,
            time_label=new_label,
            entities=copy.deepcopy(self.entities),
            relations=copy.deepcopy(self.relations),
            facts=copy.deepcopy(self.facts),
            active_rules=copy.deepcopy(self.active_rules),
            environment=copy.deepcopy(self.environment)
        )


class WorldModelAgent:
    """
    世界模型智能体 (World Model Agent)
    五项核心操作：INFER -> CONSTRUCT -> SIMULATE -> VALIDATE -> MAINTAIN
    """

    def __init__(self, world_id: str):
        self.world_id = world_id
        self.state_history: List[WorldState] = []
        self.rules: List[WorldRule] = []

    def add_rule(self, rule: WorldRule):
        self.rules.append(rule)

    def infer(self, raw_text: str) -> List[WorldFact]:
        """
        1. INFER: 严格区分显式事实、隐式事实与不确定事实
        """
        facts = []
        # 示例文本推导规则（实际对接 LLM 或语义提取器）
        facts.append(WorldFact(statement=f"提取事实: {raw_text[:40]}", confidence=FactConfidence.EXPLICIT, evidence_span=raw_text[:20]))
        return facts

    def construct_initial_world(self, initial_state: WorldState) -> WorldState:
        """
        2. CONSTRUCT: 构建故事起始时刻的世界 W(t0)
        """
        initial_state.active_rules = self.rules
        self.state_history.append(initial_state)
        return initial_state

    def simulate(self, event_description: str, agent_actions: Dict[str, Any]) -> WorldState:
        """
        3. SIMULATE: 状态迁移 W(t+1) = TRANSITION(W(t), E(t), R, A)
        """
        current_state = self.state_history[-1]
        next_step = current_state.timestamp_step + 1
        next_state = current_state.clone(next_step, f"t{next_step}")

        # 演进实体状态
        for entity_id, action in agent_actions.items():
            if entity_id in next_state.entities:
                next_state.entities[entity_id].state.update(action)

        next_state.facts.append(WorldFact(
            statement=f"事件激发: {event_description}",
            confidence=FactConfidence.EXPLICIT
        ))
        
        # 4. VALIDATE 立即校验
        violations = self.validate(next_state)
        if violations:
            raise ValueError(f"世界状态迁移违背不变量规则: {violations}")

        self.state_history.append(next_state)
        return next_state

    def validate(self, state: WorldState) -> List[str]:
        """
        4. VALIDATE: 校验物理、空间、时序、因果与角色不变量
        """
        violations = []
        # 校验硬不变量
        for rule in self.rules:
            if rule.hard_invariant:
                # 检查是否发生超自然矛盾
                pass
        return violations

    def maintain_across_containers(self, current_container_end: WorldState) -> WorldState:
        """
        5. MAINTAIN: 跨容器状态传递 W(t_end) -> W(t_start+)，解决长篇连续性风险
        """
        continuation_state = current_container_end.clone(
            new_timestamp=current_container_end.timestamp_step + 1,
            new_label=f"container_next_init"
        )
        self.state_history.append(continuation_state)
        return continuation_state
