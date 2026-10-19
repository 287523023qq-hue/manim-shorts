from manim import *
from manim_shorts.core.scene import ShortsScene
from manim_shorts.components.cards import CalloutCard, TitleHeader

class 三门问题GeneratedScene(ShortsScene):
    """
    由 DirectorEngine 自动编译生成的竖屏场景: 《三门问题》
    """
    def construct_shorts(self):
        self.setup_header("知识探秘", "三门问题")

        # === 镜头 #1 [HOOK] (时长: 3.0s) ===
        self.say("为什么99%的人都在【三门问题】上存在致命误区？", duration=3.0)
        # 前景 Manim 渲染: 顶部标题【三门问题】，中央醒目疑问高光
        self.wait(2.5)

        # === 镜头 #2 [DEDUCTION] (时长: 12.0s) ===
        self.say("我们顺着底层逻辑拆解，一切规律立刻无所遁形！", duration=12.0)
        # 前景 Manim 渲染: 中央安全舞台绘制推导图表与数学公式演化
        self.wait(11.5)

        # === 镜头 #3 [AHA_MOMENT] (时长: 5.0s) ===
        self.say("看！真正的底层规律，其实如此简单纯粹！", duration=5.0)
        # 前景 Manim 渲染: 高光 CalloutCard 顿悟卡片弹出，金光粒子环绕
        card = CalloutCard("顿悟时刻", "核心真相结论", accent_color="#FBBF24").move_to(self.stage.get_center())
        self.play(FadeIn(card, shift=UP * 0.3), run_time=0.8)
