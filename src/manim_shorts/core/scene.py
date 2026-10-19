"""
竖屏短视频场景基类 ShortsScene
提供自动布局、分步讲解字幕联动、安全区域检测与舞台管理
"""
from manim import (
    Scene, VGroup, Rectangle, Text,
    FadeIn, FadeOut, ReplacementTransform, Indicate,
    UP, DOWN, LEFT, RIGHT, ORIGIN, config
)
import numpy as np
from manim_shorts.core.layout import LAYOUT, ShortsPalette
from manim_shorts.components.cards import TitleHeader, SubtitleBox, TopProgressBar


class ShortsScene(Scene):
    """
    专门为竖屏 9:16 短视频打造的 Scene 基类
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.header: TitleHeader = None
        self.subtitle_box: SubtitleBox = None
        self.stage_mobjects = []

    def setup_header(self, title: str, tag: str = "硬核科普", animate: bool = True):
        """初始化顶部标题栏"""
        self.header = TitleHeader(title=title, tag=tag)
        if animate:
            self.play(FadeIn(self.header, shift=DOWN * 0.3), run_time=0.8)
        else:
            self.add(self.header)
        return self.header

    def setup_subtitle(self, initial_text: str = "", animate: bool = True):
        """初始化底部讲解字幕栏"""
        self.subtitle_box = SubtitleBox(initial_text=initial_text)
        if animate:
            self.play(FadeIn(self.subtitle_box, shift=UP * 0.3), run_time=0.6)
        else:
            self.add(self.subtitle_box)
        return self.subtitle_box

    def say(self, text: str, duration: float = 2.0, color: str = ShortsPalette.TEXT_MAIN):
        """
        更新底部字幕并停留指定时间（模拟口播配合）
        """
        if self.subtitle_box is None:
            self.setup_subtitle(initial_text=text)
            if duration > 0:
                self.wait(duration)
            return

        new_text = self.subtitle_box.update_text(text, color=color)
        old_text = self.subtitle_box.text_obj
        self.play(
            ReplacementTransform(old_text, new_text),
            run_time=0.35
        )
        self.subtitle_box.text_obj = new_text
        self.subtitle_box.remove(old_text)
        self.subtitle_box.add(new_text)

        if duration > 0.35:
            self.wait(duration - 0.35)

    def add_to_stage(self, *mobjects):
        """将对象标记为舞台对象，方便后续批量清理"""
        for m in mobjects:
            self.stage_mobjects.append(m)

    def clear_stage(self, run_time: float = 0.5):
        """清空视觉舞台（保留标题与字幕栏）"""
        if self.stage_mobjects:
            to_remove = [m for m in self.stage_mobjects]
            self.play(*[FadeOut(m) for m in to_remove], run_time=run_time)
            for m in to_remove:
                self.remove(m)
            self.stage_mobjects.clear()

    def show_safe_area_debug(self):
        """
        调试模式：在画面上绘制抖音/小红书/TikTok的遮挡盲区
        """
        # 核心舞台区域指示框
        stage_box = Rectangle(
            width=LAYOUT.STAGE_RIGHT - LAYOUT.STAGE_LEFT,
            height=LAYOUT.STAGE_TOP - LAYOUT.STAGE_BOTTOM,
            stroke_color=ShortsPalette.ACCENT_CYAN,
            stroke_width=1.5,
            stroke_opacity=0.6
        )
        stage_box.move_to(np.array([
            (LAYOUT.STAGE_RIGHT + LAYOUT.STAGE_LEFT) / 2,
            (LAYOUT.STAGE_TOP + LAYOUT.STAGE_BOTTOM) / 2,
            0
        ]))
        stage_label = Text("【核心视觉安全舞台】", font_size=18, color=ShortsPalette.ACCENT_CYAN)
        stage_label.next_to(stage_box, UP, buff=0.1)

        # 右侧交互区（点赞评论）
        right_danger = Rectangle(
            width=1.2,
            height=6.0,
            fill_color=ShortsPalette.ACCENT_RED,
            fill_opacity=0.2,
            stroke_color=ShortsPalette.ACCENT_RED,
            stroke_width=1
        )
        right_danger.move_to(np.array([3.9, -1.0, 0]))
        right_label = Text("右侧\n按钮区", font_size=16, color=ShortsPalette.ACCENT_RED)
        right_label.move_to(right_danger.get_center())

        # 底部信息区（文案和音乐）
        bottom_danger = Rectangle(
            width=9.0,
            height=1.8,
            fill_color=ShortsPalette.ACCENT_RED,
            fill_opacity=0.2,
            stroke_color=ShortsPalette.ACCENT_RED,
            stroke_width=1
        )
        bottom_danger.move_to(np.array([0, -7.1, 0]))
        bottom_label = Text("底部平台标题/话题/音乐信息避让区", font_size=16, color=ShortsPalette.ACCENT_RED)
        bottom_label.move_to(bottom_danger.get_center())

        debug_group = VGroup(stage_box, stage_label, right_danger, right_label, bottom_danger, bottom_label)
        self.add(debug_group)
        return debug_group
