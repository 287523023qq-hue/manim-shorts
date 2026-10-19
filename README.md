# 📱 Manim Shorts - 竖屏科普动画短视频创作工坊

基于 **Python + Manim Community** 专为竖屏短视频平台（**抖音、小红书、微信视频号、B站竖屏、TikTok**）打造的高质感科普与学术动画创作脚手架。

---

## ✨ 核心特性

- 📱 **原生 9:16 竖屏优化**：预置 1080x1920 高清坐标系，无需手动调整画幅比例。
- 🛡️ **平台安全区自适应**：避让抖音/TikTok 右侧交互区（点赞、评论、分享）与底部文案音乐区，动画核心内容永远处于视觉中心。
- 💬 **口播与字幕联动**：内置 `self.say("讲解词", duration=2.5)`，字幕卡片与语音时长自然同步替换。
- 🎨 **极客科技风 UI 组件库**：
  - `TitleHeader`：分类胶囊 + 主标题 + 科技感分割线
  - `SubtitleBox`：毛玻璃暗色底部字幕条
  - `CalloutCard`：重点公式 / 核心结论提炼卡片
  - `TopProgressBar`：顶部阅读进度条
- ⚡ **分级渲染工作流**：
  - 草稿预览（540x960 20fps）：秒级渲染，极速调试动画逻辑与视效。
  - 高清成品（1080x1920 60fps）：广播级画质，直接用于平台发布。
  - 封面快照：一键导出单帧 1080x1920 高清封面图。

---

## 📂 项目结构

```text
manim-shorts/
├── scenes/                         # 🎬 视频场景代码
│   ├── euler_identity.py           # 示例1：欧拉公式的几何真相
│   └── binary_search.py            # 示例2：二分查找对半砍的威力
├── storyboards/                    # 📝 视频文案与分镜库
│   ├── template_short_script.md    # 4段式爆款短视频脚本模板
│   └── euler_identity_script.md    # 欧拉公式分镜与口播对齐表
├── src/manim_shorts/               # 🧩 核心框架与组件
│   ├── core/
│   │   ├── layout.py               # 9:16 坐标规范与配色方案
│   │   └── scene.py                # ShortsScene 竖屏场景基类
│   └── components/
│       └── cards.py                # 标题栏、字幕卡片、公式高光卡
├── output/                         # 📦 渲染产物 (视频 mp4、图片 png)
├── run.py                          # 🚀 统一渲染命令行工具
├── manim.cfg                       # Manim 竖屏配置文件
└── pyproject.toml                  # 依赖管理文件
```

---

## 🚀 快速上手

本项目已配置好虚拟环境与全部图形依赖（Pango、Cairo、FFmpeg 等）。

### 1. 查看已有场景
```bash
python run.py list
```

### 2. 秒级草稿预览 (540x960 20fps)
```bash
# 预览欧拉公式场景
python run.py preview EulerShortScene

# 预览二分查找场景
python run.py preview BinarySearchScene
```
渲染生成的文件将保存在 `output/videos/<scene_name>/`。

### 3. 高清成品渲染 (1080x1920 60fps)
```bash
python run.py render EulerShortScene
```

### 4. 导出高清封面图 (1080x1920 PNG)
```bash
python run.py snapshot EulerShortScene
```

---

## 🎨 编写你的第一个竖屏短视频

只需继承 `ShortsScene`，30 行代码即可写出一个丝滑的科普动画：

```python
from manim import *
from manim_shorts import ShortsScene, ShortsPalette, CalloutCard

class MyFirstShortScene(ShortsScene):
    def construct(self):
        # 1. 顶部标题与开场
        self.setup_header(title="为什么光速无法超越？", tag="物理直观")
        self.say("如果一艘飞船以 99% 光速飞行，打开手电筒会怎样？", duration=2.5)

        # 2. 舞台动画 (位于核心安全区)
        circle = Circle(radius=1.5, color=ShortsPalette.ACCENT_CYAN)
        self.add_to_stage(circle)
        self.play(Create(circle))

        # 3. 步骤讲解联动
        self.say("狭义相对论的核心结论：光速在任何惯性系下恒定不变！", duration=2.5)

        # 4. 高光总结卡片
        card = CalloutCard(
            text="光速恒定原理 c = 3x10^8 m/s",
            subtext="时间膨胀 · 质能等价 · 宇宙最高速度上限"
        ).move_to(np.array([0.0, -2.0, 0.0]))
        
        self.add_to_stage(card)
        self.play(FadeIn(card, shift=UP * 0.3))
        self.say("关注我，带你看懂宇宙底层规律。", duration=2.0)
```

---

## 🎙️ 声音与音效整合建议

1. **自动配音 (TTS)**：
   可以使用微软 `edge-tts` 或开源的 `CosyVoice` / `ChatTTS` 生成口播音频。
2. **时间轴对齐**：
   通过调整 `self.say(..., duration=秒数)` 与 `self.play(..., run_time=秒数)` 使得动画节奏与语音完美契合。
3. **音视频合成**：
   使用 FFmpeg 一行命令将生成的配音 `audio.mp3` 与视频合并：
   ```bash
   ffmpeg -i output/videos/euler_identity/1080p60/EulerShortScene.mp4 -i audio.mp3 -c:v copy -c:a aac -shortest final_short.mp4
   ```
