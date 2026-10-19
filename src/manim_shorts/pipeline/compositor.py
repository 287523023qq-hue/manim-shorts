"""
音视频双层合成器 (Hybrid Video Compositor)
将 ComfyUI 生成的电影级 AI 背景视频 与 Manim 生成的前景安全区逻辑动画 (图表、公式、卡片、字幕)
使用 FFmpeg 完美合成，输出最终 1080x1920 60fps / 30fps 母带视频。
"""

import subprocess
import os
import shutil
from typing import Optional, Tuple


class HybridVideoCompositor:
    def __init__(self, output_dir: str = "output/composited"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.ffmpeg_path = shutil.which("ffmpeg") or "ffmpeg"

    def composite_layers(
        self,
        background_video_path: str,
        foreground_manim_path: str,
        output_filename: str = "final_output.mp4",
        audio_path: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        合成双层画面：背景 (ComfyUI) + 前景透明/半透明 (Manim)
        """
        output_path = os.path.join(self.output_dir, output_filename)

        if not os.path.exists(background_video_path):
            return False, f"背景视频不存在: {background_video_path}"
        if not os.path.exists(foreground_manim_path):
            return False, f"前景 Manim 视频不存在: {foreground_manim_path}"

        # 构建 FFmpeg 命令:
        # [0:v] 底层背景缩放至 1080x1920
        # [1:v] 前景 Manim 缩放并透明叠层
        filter_complex = (
            "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920[bg];"
            "[1:v]scale=1080:1920[fg];"
            "[bg][fg]overlay=0:0:shortest=1[outv]"
        )

        cmd = [
            self.ffmpeg_path,
            "-y",
            "-i", background_video_path,
            "-i", foreground_manim_path
        ]

        if audio_path and os.path.exists(audio_path):
            cmd.extend(["-i", audio_path, "-map", "[outv]", "-map", "2:a", "-c:a", "aac", "-b:a", "192k"])
        else:
            cmd.extend(["-map", "[outv]"])

        cmd.extend([
            "-filter_complex", filter_complex,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-crf", "18",
            "-preset", "fast",
            output_path
        ])

        try:
            res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if res.returncode == 0 and os.path.exists(output_path):
                return True, f"双层母带视频合成成功! 保存在: {output_path}"
            else:
                return False, f"FFmpeg 合成失败: {res.stderr[-400:]}"
        except Exception as e:
            return False, f"执行合成异常: {str(e)}"
