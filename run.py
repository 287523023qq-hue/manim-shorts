#!/usr/bin/env python3
"""
Manim Shorts 统一全链路视频创作与渲染命令行工具
用法：
    python run.py list                           # 列出所有可用的视频场景
    python run.py preview <scene_name>           # 快速预览 (540x960 20fps)
    python run.py render <scene_name>            # 高清成品渲染 (1080x1920 60fps)
    python run.py snapshot <scene_name>          # 导出封面海报 (1080x1920 PNG)
    python run.py create <topic>                 # 一键依据世界模型+导演引擎生成全套分镜、Manim代码与ComfyUI工作流
    python run.py composite <bg.mp4> <fg.mp4>    # 合成 ComfyUI 背景 + Manim 前景双层视频
    python run.py comfy-check                    # 检查本地 ComfyUI API 连通性
"""
import sys
import os
import glob
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SCENES_DIR = BASE_DIR / "scenes"
VENV_PYTHON = BASE_DIR / ".venv" / "bin" / "python"

if VENV_PYTHON.exists() and Path(sys.executable) != VENV_PYTHON:
    os.execv(str(VENV_PYTHON), [str(VENV_PYTHON)] + sys.argv)

# 确保 src 目录在 pythonpath 中
sys.path.insert(0, str(BASE_DIR / "src"))


def discover_scenes():
    """扫描 scenes 目录下所有包含 Scene 类的文件"""
    scenes = {}
    for py_file in SCENES_DIR.glob("*.py"):
        if py_file.name.startswith("__"):
            continue
        with open(py_file, "r", encoding="utf-8") as f:
            content = f.read()
        for line in content.splitlines():
            line = line.strip()
            if line.startswith("class ") and "Scene)" in line:
                class_name = line.split("class ")[1].split("(")[0].strip()
                scenes[class_name] = py_file
    return scenes


def run_command(cmd_args):
    """运行 Manim 命令并实时输出"""
    print(f"🎬 执行命令: {' '.join(cmd_args)}")
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{BASE_DIR / 'src'}:{env.get('PYTHONPATH', '')}"
    result = subprocess.run(cmd_args, env=env, cwd=BASE_DIR)
    return result.returncode


def main():
    scenes = discover_scenes()

    if len(sys.argv) < 2 or sys.argv[1] in ["-h", "--help"]:
        print("=" * 65)
        print("  📱 Manim Shorts 全链路智能短视频工作流 (World Model + AI Video)")
        print("=" * 65)
        print("基础渲染命令：")
        print("  python run.py list                    - 列出当前工程里的所有视频场景")
        print("  python run.py preview <SceneName>     - 快速低清渲染 (540x960 20fps, 秒级生成)")
        print("  python run.py render <SceneName>      - 1080P/4K 高清母带渲染 (1080x1920 60fps)")
        print("  python run.py snapshot <SceneName>    - 导出单帧高清封面 (PNG)")
        print("\n全链路创作与 AI 编排命令：")
        print("  python run.py create <Topic>          - 一键生成分镜、Manim代码与ComfyUI工作流")
        print("  python run.py generate '<Prompt>'     - 对话式生成：输入一句话直接编译并触发视频生成")
        print("  python run.py composite <bg> <fg>     - 合成 ComfyUI 电影背景 + Manim 前景几何")
        print("  python run.py comfy-check             - 探测本地 ComfyUI API (127.0.0.1:8188)")
        print("\n当前已发现的场景：")
        for name, path in scenes.items():
            print(f"  • {name}  ({path.relative_to(BASE_DIR)})")
        print("=" * 65)
        return

    action = sys.argv[1]

    if action == "list":
        print("\n📹 当前工程中可渲染的竖屏场景：")
        for i, (name, path) in enumerate(scenes.items(), 1):
            print(f"  [{i}] {name:<25} -> {path.relative_to(BASE_DIR)}")
        print()
        return

    elif action == "generate":
        if len(sys.argv) < 3:
            print("❌ 请输入提示词，例如: python run.py generate '雪山之巅剑修拔剑出鞘，镜头慢速推近，5秒'")
            return
        prompt_text = sys.argv[2]
        image_arg = None
        if "--image" in sys.argv:
            idx = sys.argv.index("--image")
            if idx + 1 < len(sys.argv):
                image_arg = sys.argv[idx + 1]

        from manim_shorts.pipeline.prompt_to_video import ChatToVideoEngine
        engine = ChatToVideoEngine(str(BASE_DIR))
        print(f"\n⚡ 正在处理自然语言提示词: \"{prompt_text}\"...")
        res = engine.generate_video(prompt_text, input_image=image_arg)
        print("✅ 语义推演与 15 模块编译完成！")
        print(f"  🎬 镜头机制: {res['parsed_params']['mechanism']} ({res['parsed_params']['duration']}s, {res['parsed_params']['aspect_ratio']})")
        print(f"  🎨 生成载荷: {res['payload_path']}")
        print(f"  📡 ComfyUI 状态: {res['status']}")
        return

    elif action == "create":
        topic = sys.argv[2] if len(sys.argv) > 2 else "科学探秘"
        print(f"\n🚀 正在依据【世界模型 + 导演中枢】创建全套视频工程: 《{topic}》...")
        from manim_shorts.pipeline.orchestrator import MasterVideoOrchestrator
        orchestrator = MasterVideoOrchestrator(str(BASE_DIR))
        result = orchestrator.create_video_project(title=topic, topic=f"关于{topic}的颠覆性认知解析")
        print("✅ 创建成功！成果清单：")
        print(f"  📄 导演分镜手册: {result['storyboard']}")
        print(f"  🐍 Manim 场景代码: {result['scene_code']}")
        print(f"  🎨 ComfyUI 工作流包: {len(result['comfyui_workflows'])} 个镜头 JSON 已就绪")
        return

    elif action == "comfy-check":
        from manim_shorts.comfyui.client import ComfyUIClient
        client = ComfyUIClient()
        if client.is_alive():
            print("🟢 ComfyUI 服务在线! (http://127.0.0.1:8188 可通信)")
        else:
            print("⚪ ComfyUI 当前未在 http://127.0.0.1:8188 运行 (不影响离线分镜与代码生成)")
        return

    elif action == "composite":
        if len(sys.argv) < 4:
            print("❌ 用法: python run.py composite <bg_video.mp4> <fg_manim.mp4> [output_name.mp4]")
            return
        bg = sys.argv[2]
        fg = sys.argv[3]
        out = sys.argv[4] if len(sys.argv) > 4 else "final_composited.mp4"
        from manim_shorts.pipeline.compositor import HybridVideoCompositor
        compositor = HybridVideoCompositor()
        ok, msg = compositor.composite_layers(bg, fg, out)
        print(("✅ " if ok else "❌ ") + msg)
        return

    # 获取要渲染的场景名称
    scene_name = sys.argv[2] if len(sys.argv) > 2 else None
    if not scene_name:
        if len(scenes) == 1:
            scene_name = list(scenes.keys())[0]
            print(f"ℹ️ 未指定场景名，自动选用唯一场景: {scene_name}")
        else:
            print("❌ 请指定场景名称，例如:")
            for name in scenes:
                print(f"   python run.py {action} {name}")
            return

    if scene_name not in scenes:
        matches = [k for k in scenes if scene_name.lower() in k.lower()]
        if len(matches) == 1:
            scene_name = matches[0]
            print(f"💡 自动匹配场景: {scene_name}")
        else:
            print(f"❌ 未找到场景 '{scene_name}'。可用列表:")
            for k in scenes:
                print(f"   - {k}")
            return

    target_file = str(scenes[scene_name])

    if action == "preview":
        print(f"\n⚡ 正在快速预览渲染: {scene_name} (540x960 20fps)...")
        cmd = [
            str(VENV_PYTHON), "-m", "manim",
            target_file, scene_name,
            "-r", "540,960", "--fps", "20"
        ]
        run_command(cmd)

    elif action == "render":
        print(f"\n💎 正在高清生产渲染: {scene_name} (1080x1920 60fps)...")
        cmd = [
            str(VENV_PYTHON), "-m", "manim",
            target_file, scene_name,
            "-r", "1080,1920", "--fps", "60"
        ]
        run_command(cmd)

    elif action == "snapshot":
        print(f"\n📸 正在导出单帧封面: {scene_name} (1080x1920)...")
        cmd = [
            str(VENV_PYTHON), "-m", "manim",
            target_file, scene_name,
            "-s", "-r", "1080,1920"
        ]
        run_command(cmd)

    else:
        print(f"❌ 未知操作: {action}。支持的动作: list, preview, render, snapshot, create, composite, comfy-check")


if __name__ == "__main__":
    main()
