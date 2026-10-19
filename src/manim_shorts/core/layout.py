"""
竖屏短视频布局与安全区域配置 (9:16 画幅)
"""
from dataclasses import dataclass
import numpy as np

# 调色盘规范：极客科技感、高对比度、暗色 OLED 护眼风
class ShortsPalette:
    BG_DARK = "#0E1117"
    SURFACE = "#1E293B"
    SURFACE_LIGHT = "#334155"
    BORDER = "#475569"
    
    TEXT_MAIN = "#F8FAFC"
    TEXT_MUTED = "#94A3B8"
    
    ACCENT_CYAN = "#38BDF8"
    ACCENT_BLUE = "#3B82F6"
    ACCENT_GOLD = "#FBBF24"
    ACCENT_GREEN = "#34D399"
    ACCENT_RED = "#F87171"
    ACCENT_PURPLE = "#C084FC"


@dataclass(frozen=True)
class ShortsLayout:
    """
    9:16 竖屏坐标系:
    X 范围: [-4.5, 4.5] (宽度 9.0)
    Y 范围: [-8.0, 8.0] (高度 16.0)
    """
    FRAME_WIDTH: float = 9.0
    FRAME_HEIGHT: float = 16.0

    # 顶部标题栏区域
    HEADER_Y: float = 6.8
    TAG_Y: float = 7.4
    
    # 核心视觉舞台（最佳视觉中心）
    STAGE_TOP: float = 5.8
    STAGE_BOTTOM: float = -3.2
    STAGE_LEFT: float = -3.8
    # 考虑抖音/TikTok/小红书右侧交互按钮（点赞/评论/收藏/头像），右边距收敛
    STAGE_RIGHT: float = 3.2

    # 底部字幕与讲解区
    SUBTITLE_Y: float = -4.8
    
    # 底部避让区（平台标题、话题、音乐转盘遮挡）
    DANGER_BOTTOM_THRESHOLD: float = -6.2

    @property
    def STAGE_CENTER(self) -> np.ndarray:
        return np.array([0.0, 1.2, 0.0])


LAYOUT = ShortsLayout()
