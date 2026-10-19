"""
二分查找算法直观：竖屏短视频演示场景
展示有序数组的高效折半查找与 O(log N) 的威力
"""
from manim import (
    VGroup, RoundedRectangle, Text, Arrow, Line,
    Create, Write, FadeIn, FadeOut, Transform, ReplacementTransform,
    Indicate, Circumscribe,
    UP, DOWN, LEFT, RIGHT, ORIGIN
)
import numpy as np
from manim_shorts import ShortsScene, ShortsPalette, CalloutCard


class BinarySearchScene(ShortsScene):
    def construct(self):
        # 1. 开场标题与金句引言
        self.setup_header(title="二分查找：对半砍的威力", tag="算法直观")
        self.say("在 100 万个数据中找一个数，最少只需要比较 20 次？", duration=2.4)

        # 2. 目标展示胶囊
        target_val = 34
        target_badge = RoundedRectangle(
            corner_radius=0.15,
            width=2.8,
            height=0.7,
            fill_color=ShortsPalette.SURFACE,
            fill_opacity=1.0,
            stroke_color=ShortsPalette.ACCENT_GOLD,
            stroke_width=2
        ).move_to(np.array([0.0, 4.3, 0.0]))
        target_text = Text(f"目标值 Target = {target_val}", font_size=20, weight="BOLD", color=ShortsPalette.ACCENT_GOLD)
        target_text.move_to(target_badge.get_center())
        target_group = VGroup(target_badge, target_text)

        self.add_to_stage(target_group)
        self.play(FadeIn(target_group, shift=DOWN * 0.2), run_time=0.6)

        # 3. 构建有序数组
        data = [3, 8, 12, 19, 27, 34, 45, 58]
        boxes = []
        labels = []
        
        box_width = 0.82
        box_height = 0.95
        spacing = 0.92
        start_x = - (len(data) - 1) * spacing / 2
        array_y = 2.4

        for i, val in enumerate(data):
            x = start_x + i * spacing
            box = RoundedRectangle(
                corner_radius=0.12,
                width=box_width,
                height=box_height,
                fill_color=ShortsPalette.SURFACE,
                fill_opacity=0.9,
                stroke_color=ShortsPalette.BORDER,
                stroke_width=2
            ).move_to(np.array([x, array_y, 0.0]))
            
            lbl = Text(str(val), font_size=24, weight="BOLD", color=ShortsPalette.TEXT_MAIN)
            lbl.move_to(box.get_center())
            
            boxes.append(box)
            labels.append(lbl)

        array_group = VGroup(*boxes, *labels)
        self.add_to_stage(array_group)
        
        self.say("二分查找的核心前提：数据必须已经排好序！", duration=2.2)
        self.play(FadeIn(array_group, shift=UP * 0.3), run_time=0.8)

        # 4. 指针 L, R, M
        def make_pointer(name: str, color: str, x: float, y_offset: float = -0.85):
            arrow = Arrow(
                start=np.array([x, array_y + y_offset - 0.4, 0]),
                end=np.array([x, array_y + y_offset + 0.1, 0]),
                buff=0,
                color=color,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.3
            )
            txt = Text(name, font_size=18, weight="BOLD", color=color)
            txt.next_to(arrow, DOWN, buff=0.08)
            return VGroup(arrow, txt)

        # 初始指针: L=0, R=7, Mid = (0+7)//2 = 3 (值 19)
        ptr_l = make_pointer("L", ShortsPalette.ACCENT_CYAN, boxes[0].get_x())
        ptr_r = make_pointer("R", ShortsPalette.ACCENT_CYAN, boxes[7].get_x())
        ptr_m = make_pointer("Mid", ShortsPalette.ACCENT_GOLD, boxes[3].get_x())

        self.add_to_stage(ptr_l, ptr_r, ptr_m)
        self.play(FadeIn(ptr_l), FadeIn(ptr_r), FadeIn(ptr_m), run_time=0.6)

        # 5. 第一轮比较
        self.say("第 1 次比较：中间值 19 < 34，目标肯定在右半区！", duration=2.4)
        self.play(Indicate(boxes[3], color=ShortsPalette.ACCENT_GOLD), run_time=0.8)
        
        # 淘汰左半区 [0..3]
        eliminated_left = VGroup(*boxes[0:4], *labels[0:4])
        self.play(
            eliminated_left.animate.set_opacity(0.25),
            run_time=0.8
        )

        # 6. 移动 L 指针到 4 (值 27), 新 Mid = (4+7)//2 = 5 (值 34)
        new_ptr_l = make_pointer("L", ShortsPalette.ACCENT_CYAN, boxes[4].get_x())
        new_ptr_m = make_pointer("Mid", ShortsPalette.ACCENT_GREEN, boxes[5].get_x())
        
        self.say("直接砍掉一半！范围缩小到右侧 4 个元素", duration=2.2)
        self.play(
            ReplacementTransform(ptr_l, new_ptr_l),
            ReplacementTransform(ptr_m, new_ptr_m),
            run_time=1.0
        )
        ptr_l = new_ptr_l
        ptr_m = new_ptr_m

        # 7. 第二轮比较：命中 34！
        self.say("第 2 次比较：中间值刚好等于 34，精准命中！", duration=2.2)
        
        hit_box = boxes[5].copy().set_fill(ShortsPalette.ACCENT_GREEN, opacity=0.4).set_stroke(ShortsPalette.ACCENT_GREEN, width=3.5)
        self.add_to_stage(hit_box)
        self.play(
            FadeIn(hit_box),
            Circumscribe(boxes[5], color=ShortsPalette.ACCENT_GREEN, run_time=1.2)
        )

        # 8. 总结卡片
        callout = CalloutCard(
            text="时间复杂度 O(log N)",
            subtext="每次减半 · 2^20 ≈ 104 万，最多只要 20 次！",
            accent_color=ShortsPalette.ACCENT_GREEN
        ).move_to(np.array([0.0, -1.8, 0.0]))

        self.add_to_stage(callout)
        self.play(FadeIn(callout, shift=UP * 0.4), run_time=0.8)
        self.say("这就是对半砍的几何级数威力。", duration=2.2)

        self.wait(1.0)
