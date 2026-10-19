"""
欧拉公式几何直观：竖屏短视频演示场景
从复平面的圆周旋转直观理解 e^{i*pi} + 1 = 0
"""
from manim import (
    Axes, Circle, Arrow, Dot, Line, Arc, Text, VGroup,
    Create, Write, FadeIn, FadeOut, Transform, ReplacementTransform,
    Rotate, Indicate, Circumscribe,
    UP, DOWN, LEFT, RIGHT, ORIGIN, PI, DEGREES
)
import numpy as np
from manim_shorts import ShortsScene, ShortsPalette, CalloutCard


class EulerShortScene(ShortsScene):
    def construct(self):
        # 1. 顶部标题与开场字幕
        self.setup_header(title="欧拉公式的几何真相", tag="数学之美")
        self.say("为什么包含 e、i、π 的公式，最终会等于 -1？", duration=2.2)

        # 2. 构建复平面坐标系与单位圆
        center_stage = np.array([0.0, 1.5, 0.0])
        
        axes = Axes(
            x_range=[-1.5, 1.5, 1],
            y_range=[-1.5, 1.5, 1],
            x_length=4.2,
            y_length=4.2,
            tips=True,
            axis_config={
                "color": ShortsPalette.BORDER,
                "stroke_width": 2,
                "include_numbers": False
            }
        ).move_to(center_stage)

        # 轴标签 (实轴 Re / 虚轴 Im)
        re_label = Text("实轴 (Re)", font_size=18, color=ShortsPalette.TEXT_MUTED)
        re_label.next_to(axes.x_axis.get_end(), RIGHT, buff=0.15)
        
        im_label = Text("虚轴 (Im)", font_size=18, color=ShortsPalette.TEXT_MUTED)
        im_label.next_to(axes.y_axis.get_end(), UP, buff=0.15)

        # 单位圆 (半径 1.35)
        radius = 1.35
        unit_circle = Circle(
            radius=radius,
            color=ShortsPalette.SURFACE_LIGHT,
            stroke_width=2.5
        ).move_to(center_stage)

        self.add_to_stage(axes, re_label, im_label, unit_circle)
        self.play(
            Create(axes),
            FadeIn(re_label),
            FadeIn(im_label),
            Create(unit_circle),
            run_time=1.2
        )

        # 3. 引入乘法与旋转直觉
        self.say("在复数世界中，乘上虚数 i 代表将向量【逆时针旋转 90度】", duration=2.5)

        # 初始点 (1, 0)
        origin_pt = center_stage
        start_pt = center_stage + RIGHT * radius
        
        arrow = Arrow(
            start=origin_pt,
            end=start_pt,
            buff=0,
            color=ShortsPalette.ACCENT_CYAN,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.2
        )
        dot_one = Dot(start_pt, color=ShortsPalette.ACCENT_GOLD, radius=0.08)
        label_one = Text("1", font_size=20, weight="BOLD", color=ShortsPalette.ACCENT_GOLD)
        label_one.next_to(dot_one, DOWN + RIGHT, buff=0.1)

        self.add_to_stage(arrow, dot_one, label_one)
        self.play(FadeIn(arrow), FadeIn(dot_one), Write(label_one), run_time=0.8)

        # 4. 指数 e^{i*theta} 对应圆周连续运动
        self.say("而 e^(i * θ) 正好代表沿着单位圆周走过 θ 弧度！", duration=2.5)

        # 旋转动画：从 0 度旋转到 pi (180度)
        arc = Arc(
            radius=0.45,
            start_angle=0,
            angle=PI,
            arc_center=center_stage,
            color=ShortsPalette.ACCENT_GOLD,
            stroke_width=3
        )
        theta_label = Text("θ = π", font_size=20, color=ShortsPalette.ACCENT_GOLD)
        theta_label.next_to(arc, UP, buff=0.1)

        target_pt = center_stage + LEFT * radius
        end_dot = Dot(target_pt, color=ShortsPalette.ACCENT_CYAN, radius=0.09)
        label_neg_one = Text("-1", font_size=22, weight="BOLD", color=ShortsPalette.ACCENT_CYAN)
        label_neg_one.next_to(end_dot, DOWN + LEFT, buff=0.1)

        self.play(
            Create(arc),
            Write(theta_label),
            Rotate(arrow, angle=PI, about_point=origin_pt),
            run_time=2.0
        )
        self.play(FadeIn(end_dot), Write(label_neg_one), run_time=0.6)
        self.add_to_stage(arc, theta_label, end_dot, label_neg_one)

        # 5. 结论聚焦与金句提炼
        self.say("当转过半圆 θ = π 时，向量精准停在实轴的【-1】上！", duration=2.2)
        self.play(Indicate(end_dot, color=ShortsPalette.ACCENT_GOLD, scale_factor=1.6), run_time=1.0)

        # 6. 展示核心卡片
        callout = CalloutCard(
            text="e^(i·π) + 1 = 0",
            subtext="自然对数底 e · 虚数 i · 圆周率 π · 乘法单位 1 · 无 0",
            accent_color=ShortsPalette.ACCENT_CYAN
        ).move_to(np.array([0.0, -2.1, 0.0]))

        self.add_to_stage(callout)
        self.play(FadeIn(callout, shift=UP * 0.4), run_time=0.8)
        self.say("这便是数学史上最优雅的交响曲。", duration=2.5)

        self.wait(1.0)
