"""
竖屏短视频专用的高质感 UI 组件库
无需 LaTeX，纯 Pango / Text 高性能渲染
"""
from manim import (
    VGroup, RoundedRectangle, Rectangle, Text, Line,
    FadeIn, FadeOut, Transform, ReplacementTransform,
    UP, DOWN, LEFT, RIGHT, ORIGIN
)
import numpy as np
from manim_shorts.core.layout import LAYOUT, ShortsPalette


class TitleHeader(VGroup):
    """顶部标题栏组件：分类胶囊 + 主标题 + 科技感分割线"""
    def __init__(self, title: str, tag: str = "科普探索", **kwargs):
        super().__init__(**kwargs)
        
        # 标签背景胶囊
        tag_text = Text(tag, font_size=20, weight="BOLD", color=ShortsPalette.BG_DARK)
        tag_bg = RoundedRectangle(
            corner_radius=0.15,
            height=tag_text.height + 0.16,
            width=tag_text.width + 0.36,
            fill_color=ShortsPalette.ACCENT_CYAN,
            fill_opacity=1.0,
            stroke_width=0
        )
        tag_group = VGroup(tag_bg, tag_text)
        tag_group.move_to(np.array([0.0, LAYOUT.TAG_Y, 0.0]))
        
        # 主标题
        main_title = Text(
            title,
            font_size=32,
            weight="BOLD",
            color=ShortsPalette.TEXT_MAIN
        )
        main_title.next_to(tag_group, DOWN, buff=0.22)
        
        # 渐变微光装饰线
        line = Line(
            start=LEFT * 3.6,
            end=RIGHT * 3.6,
            stroke_width=1.5,
            stroke_color=ShortsPalette.SURFACE_LIGHT
        )
        line.next_to(main_title, DOWN, buff=0.25)
        
        accent_dot = RoundedRectangle(
            corner_radius=0.05,
            height=0.08,
            width=0.8,
            fill_color=ShortsPalette.ACCENT_CYAN,
            fill_opacity=1.0,
            stroke_width=0
        )
        accent_dot.move_to(line.get_center())

        self.tag = tag_group
        self.main_title = main_title
        self.line = line
        self.accent_dot = accent_dot
        self.add(tag_group, main_title, line, accent_dot)


class SubtitleBox(VGroup):
    """底部口播字幕卡片：半透明毛玻璃底板 + 高对比度文案"""
    def __init__(self, initial_text: str = "", width: float = 7.4, height: float = 1.3, **kwargs):
        super().__init__(**kwargs)
        
        self.box_width = width
        self.box_height = height
        
        self.bg = RoundedRectangle(
            corner_radius=0.25,
            width=width,
            height=height,
            fill_color=ShortsPalette.SURFACE,
            fill_opacity=0.92,
            stroke_color=ShortsPalette.BORDER,
            stroke_width=1.5
        )
        
        self.text_obj = Text(
            initial_text,
            font_size=24,
            weight="MEDIUM",
            color=ShortsPalette.TEXT_MAIN
        )
        self.text_obj.move_to(self.bg.get_center())
        
        self.add(self.bg, self.text_obj)
        self.move_to(np.array([0.0, LAYOUT.SUBTITLE_Y, 0.0]))

    def update_text(self, new_text: str, color: str = ShortsPalette.TEXT_MAIN) -> Text:
        """生成新的文本对象用于动画替换"""
        new_text_obj = Text(
            new_text,
            font_size=24,
            weight="MEDIUM",
            color=color
        )
        # 限制字幕不要超出卡片宽度
        if new_text_obj.width > self.box_width - 0.6:
            new_text_obj.scale_to_fit_width(self.box_width - 0.6)
            
        new_text_obj.move_to(self.bg.get_center())
        return new_text_obj


class CalloutCard(VGroup):
    """重点公式/结论提炼卡片"""
    def __init__(self, text: str, subtext: str = "", accent_color: str = ShortsPalette.ACCENT_GOLD, **kwargs):
        super().__init__(**kwargs)
        
        card_bg = RoundedRectangle(
            corner_radius=0.2,
            width=7.2,
            height=1.8,
            fill_color=ShortsPalette.SURFACE,
            fill_opacity=0.95,
            stroke_color=accent_color,
            stroke_width=2.5
        )
        
        main_t = Text(text, font_size=32, weight="BOLD", color=ShortsPalette.TEXT_MAIN)
        if main_t.width > 6.6:
            main_t.scale_to_fit_width(6.6)
            
        if subtext:
            sub_t = Text(subtext, font_size=20, color=ShortsPalette.TEXT_MUTED)
            content = VGroup(main_t, sub_t).arrange(DOWN, buff=0.15)
        else:
            content = main_t
            
        content.move_to(card_bg.get_center())
        self.add(card_bg, content)


class TopProgressBar(VGroup):
    """顶部细进度条"""
    def __init__(self, total_width: float = 9.0, **kwargs):
        super().__init__(**kwargs)
        self.total_width = total_width
        self.bg_bar = Rectangle(
            width=total_width,
            height=0.06,
            fill_color=ShortsPalette.SURFACE,
            fill_opacity=0.5,
            stroke_width=0
        )
        self.fill_bar = Rectangle(
            width=0.001,
            height=0.06,
            fill_color=ShortsPalette.ACCENT_CYAN,
            fill_opacity=1.0,
            stroke_width=0
        )
        self.bg_bar.move_to(np.array([0.0, 7.97, 0.0]))
        self.fill_bar.align_to(self.bg_bar, LEFT)
        self.fill_bar.move_to(np.array([-total_width / 2, 7.97, 0.0]), aligned_edge=LEFT)
        self.add(self.bg_bar, self.fill_bar)
