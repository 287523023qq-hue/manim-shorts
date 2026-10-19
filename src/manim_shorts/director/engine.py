"""
全链路导演引擎与故障诊断器 (Director Engine & Repair Diagnoser)
负责：
1. 组装 4 段式爆款短视频全镜流
2. 自动化失败诊断与槽位修复 (从 repair-guide 升级为自动化规则)
3. 导出为 Markdown 分镜本、ComfyUI 生产 JSON、以及 Manim 场景骨架代码
"""

import json
from typing import List, Dict, Any, Tuple
from manim_shorts.director.contracts import (
    DirectorShot, NarrativeBeat, CameraMechanism,
    VisualIdentityLock, CameraMotionContract
)


class DiagnosticError(str):
    CAMERA_STATIC = "镜头几乎没动：缺少物理位移路径与前景视差"
    ZOOM_CONFUSION = "推进与变焦混淆：未区分机位沿光轴物理平移与焦距光学放大"
    SUBJECT_DRIFT = "主体漂移/出画：未锁定主体屏幕坐标（如居中/三分位）"
    FACE_MORPHING = "人物变形：运镜速度过快或主体动作与运镜争夺变化"
    SCENE_JUMP = "背景突变：缺少环境连续性与光线锁定，跨空间未设关键帧"
    ORBIT_SPIN = "环绕变自转：未明确声明机位绕主体旋转，导致主体自己原地旋转"
    SAFE_ZONE_BREACH = "触碰 9:16 禁区：动作或主体偏向右侧或底部平台遮挡区"


class DirectorEngine:
    """导演引擎中心"""

    def __init__(self, title: str, topic: str):
        self.title = title
        self.topic = topic
        self.shots: List[DirectorShot] = []
        self.global_identity: VisualIdentityLock = None

    def set_global_identity(self, identity: VisualIdentityLock):
        """设置全片全局一致性锚定"""
        self.global_identity = identity

    def add_shot(self, shot: DirectorShot):
        """追加分镜镜头"""
        if not shot.identity_lock and self.global_identity:
            shot.identity_lock = self.global_identity
        self.shots.append(shot)

    def diagnose_and_repair(self, shot_index: int, error_type: str) -> Tuple[bool, str]:
        """
        根据可见失败现象，精准修改对应槽位（遵循修一次只动一槽的原则）
        """
        target_shot = next((s for s in self.shots if s.shot_index == shot_index), None)
        if not target_shot or not target_shot.motion_contract:
            return False, "未找到目标镜头或该镜头无运镜合同"

        c = target_shot.motion_contract
        action_taken = ""

        if "自转" in error_type or "spin" in error_type.lower():
            c.subject_locks = "主体绝对静止且朝向固定，相机沿固定半径弧线绕行，背景产生连续差速位移"
            action_taken = "已修正主体与机位相对关系：明确主体静止，严禁主体自转。"
        elif "变焦" in error_type or "放大" in error_type:
            c.mechanism = CameraMechanism.PUSH_IN
            c.path_and_direction = "相机沿物理光轴向前平移，焦距严格保持不变，透视产生自然纵深压缩"
            action_taken = "已修正机制：将单纯画面放大改为物理平移推进，透视保持自然。"
        elif "漂移" in error_type or "drift" in error_type:
            c.subject_locks += "；主体严格保持在屏幕中央安全区内，禁止位移出画"
            action_taken = "已修正主体屏幕锁定：强制居中于安全舞台中心。"
        elif "没动" in error_type or "static" in error_type:
            c.environment_response = "近景前景物体快速穿过画面形成强烈视差，远景层次分明，证明物理运镜正在进行"
            action_taken = "已补充前景差速视差槽位：强化运动可见度。"
        else:
            c.targeted_constraints.append("机位运动平稳，背景连续，主体轮廓锁定")
            action_taken = "已补充针对性物理稳定约束。"

        return True, action_taken

    def export_production_markdown(self) -> str:
        """导出为标准化短视频生产分镜脚本文档"""
        md = [
            f"# 《{self.title}》全链路短视频导演制作手册",
            f"> 核心主题: {self.topic} | 画幅: 9:16 坚戈竖屏 | 总镜头数: {len(self.shots)}",
            "",
            "## 一、全局视觉与角色一致性锁定 (Identity Lock)",
        ]
        if self.global_identity:
            md.append(f"```text\n{self.global_identity.to_identity_prompt()}\n```")
        else:
            md.append("*未设置全局角色锁定，采用纯几何与场景图层。*")

        md.extend([
            "",
            "## 二、4段式爆款分镜运动合同表 (Shot Production Packs)",
            "| 镜号 | 节奏拍子 | 时长 | 运镜机制与指令 | 关键帧策略 | 前景 Manim 数据 | 背景 ComfyUI AI |",
            "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
        ])

        for s in self.shots:
            c = s.motion_contract
            mech_str = f"**{c.mechanism.value}**<br>{c.compile_motion_prompt()}" if c else "静态排版"
            md.append(
                f"| #{s.shot_index} | `{s.beat.value}` | {s.duration_seconds}s | "
                f"{mech_str} | {c.keyframe_strategy if c else '无'} | "
                f"{s.manim_layer_spec} | {s.comfy_ai_layer_spec or '配合运镜'} |"
            )

        md.extend([
            "",
            "## 三、旁白与字幕对齐清单",
        ])
        for s in self.shots:
            md.append(f"- **镜头 #{s.shot_index} ({s.beat.value})**: “{s.voiceover_script}” (字幕: {s.subtitle_text})")

        return "\n".join(md)

    def export_json(self) -> str:
        """导出为 ComfyUI / 自动化管线可消费的 JSON"""
        data = {
            "title": self.title,
            "topic": self.topic,
            "global_identity": self.global_identity.to_identity_prompt() if self.global_identity else None,
            "shots": [s.to_production_dict() for s in self.shots]
        }
        return json.dumps(data, ensure_ascii=False, indent=2)

    def generate_manim_scaffold(self, class_name: str) -> str:
        """自动根据导演分镜生成对应的 Manim 场景脚手架代码"""
        code = [
            'from manim import *',
            'from manim_shorts.core.scene import ShortsScene',
            'from manim_shorts.components.cards import CalloutCard, TitleHeader',
            '',
            f'class {class_name}(ShortsScene):',
            f'    """',
            f'    由 DirectorEngine 自动编译生成的竖屏场景: 《{self.title}》',
            f'    """',
            '    def construct_shorts(self):',
            f'        self.setup_header("知识探秘", "{self.title}")',
            '',
        ]

        for s in self.shots:
            code.append(f'        # === 镜头 #{s.shot_index} [{s.beat.value.upper()}] (时长: {s.duration_seconds}s) ===')
            if s.voiceover_script:
                code.append(f'        self.say("{s.voiceover_script}", duration={s.duration_seconds})')
            code.append(f'        # 前景 Manim 渲染: {s.manim_layer_spec}')
            if s.beat == NarrativeBeat.AHA_MOMENT:
                code.append('        card = CalloutCard("顿悟时刻", "核心真相结论", accent_color="#FBBF24").move_to(self.stage.get_center())')
                code.append('        self.play(FadeIn(card, shift=UP * 0.3), run_time=0.8)')
            else:
                code.append(f'        self.wait({max(0.5, s.duration_seconds - 0.5)})')
            code.append('')

        return '\n'.join(code)
