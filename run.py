#!/usr/bin/env python3
"""
Manim Shorts 统一创作与渲染命令行工具
用法：
    python run.py list                           # 列出所有可用的视频场景
    python run.py preview <scene_name>           # 快速预览 (540x960 20fps)
    python run.py render <scene_name>            # 高清成品渲染 (1080x1920 60fps)
    python run.py snapshot <scene_name>          # 导出封面海报 (1080x1920 PNG)
    python run.py debug <scene_name>             # 带安全区网格预览
"""
import sys
import os
import glob
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SCENES_DIR = BASE_DIR / "scenes"
VENV_PYTHON = BASE_DIR / ".venv" / "bin" / "python"

if not VENV_PYTHON.exists():
    VENV_PYTHON = Path(sys.executable)


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
            if line.startswith("class ") and "(ShortsScene)" in line:
                class_name = line.split("class ")[1].split("(")[0].strip()
                scenes[class_name] = py_file
            elif line.startswith("class ") and "(Scene)" in line:
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
        print("=" * 60)
        print("  📱 Manim Shorts 竖屏科普短视频工作流")
        print("=" * 60)
        print("常用命令：")
        print("  python run.py list                  - 列出当前工程里的所有视频场景")
        print("  python run.py preview <SceneName>   - 快速低清渲染 (540x960 20fps, 秒级生成)")
        print("  python run.py render <SceneName>    - 4K/1080P 高清成品 (1080x1920 60fps)")
        print("  python run.py snapshot <SceneName>  - 导出单帧高清封面 (PNG)")
        print("\n当前已发现的场景：")
        for name, path in scenes.items():
            print(f"  • {name}  ({path.relative_to(BASE_DIR)})")
        print("=" * 60)
        return

    action = sys.argv[1]

    if action == "list":
        print("\n📹 当前工程中可渲染的竖屏场景：")
        for i, (name, path) in enumerate(scenes.items(), 1):
            print(f"  [{i}] {name:<22} -> {path.relative_to(BASE_DIR)}")
        print()
        return

    # 获取要渲染的场景名称
    scene_name = sys.argv[2] if len(sys.argv) > 2 else None
    if not scene_name:
        # 如果未指定场景名称，默认展示或者使用第一个
        if len(scenes) == 1:
            scene_name = list(scenes.keys())[0]
            print(f"ℹ️ 未指定场景名，自动选用唯一场景: {scene_name}")
        else:
            print("❌ 请指定场景名称，例如:")
            for name in scenes:
                print(f"   python run.py {action} {name}")
            return

    if scene_name not in scenes:
        # 模糊匹配
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
        print(f"❌ 未知操作: {action}。支持的动作: list, preview, render, snapshot")


if __name__ == "__main__":
    main()
