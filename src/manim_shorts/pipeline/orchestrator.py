"""
全流程主编排器 (Master Video Production Orchestrator)
打通：
世界模型 (CSCA World Model) -> 导演分镜 (DirectorEngine) -> ComfyUI 电影级生图 -> Manim 前景几何 -> FFmpeg 双层合成
"""

import os
import json
from typing import Dict, Any, Optional, Tuple
from manim_shorts.world_model import WorldModelAgent, WorldState, WorldEntity, WorldRule, MUS, MSSS, PacingLock, NarrativeProportion, CNCCompiler
from manim_shorts.director import DirectorEngine, DirectorShot, NarrativeBeat, CameraMechanism, VisualIdentityLock, CameraMotionContract
from manim_shorts.comfyui.adapter import ComfyUIWorkflowAdapter
from manim_shorts.comfyui.client import ComfyUIClient
from manim_shorts.pipeline.compositor import HybridVideoCompositor


class MasterVideoOrchestrator:
    def __init__(self, project_root: str = "/Users/guopeng/manim-shorts"):
        self.project_root = project_root
        self.comfy_adapter = ComfyUIWorkflowAdapter(os.path.join(project_root, "comfyui_workflows/wan21_hunyuan_production_pipeline.json"))
        self.comfy_client = ComfyUIClient()
        self.compositor = HybridVideoCompositor(os.path.join(project_root, "output/composited"))

    def create_video_project(self, title: str, topic: str, character_name: str = "智慧导师") -> Dict[str, Any]:
        """
        根据主题自动推演世界模型与分镜
        """
        # 1. 初始化导演中枢
        engine = DirectorEngine(title=title, topic=topic)
        engine.set_global_identity(VisualIdentityLock(
            subject_name=character_name,
            face_and_silhouette="圆润面容，三头身Q版比例，特征鲜明",
            color_palette="克莱因蓝(#0284C7) + 琥珀金(#FBBF24)",
            wardrobe_and_props="深色定制战袍，手持推演法器",
            render_style="3D超高清微缩手办模型，柔美漫反射环境光"
        ))

        # 2. 自动化 4 段式短视频标准分镜
        # Shot 1: Hook
        engine.add_shot(DirectorShot(
            shot_index=1,
            beat=NarrativeBeat.HOOK,
            duration_seconds=3.0,
            voiceover_script=f"为什么99%的人都在【{title}】上存在致命误区？",
            subtitle_text=f"【{title}】颠覆常识的真相！",
            motion_contract=CameraMotionContract(
                start_framing="广阔场景全貌",
                mechanism=CameraMechanism.CRASH_ZOOM,
                path_and_direction="沿光轴高速向前冲入，末段平稳制动",
                speed_curve="前1秒极速冲进，后0.5秒精准制动",
                end_framing="核心道具中景，细节锐利可辨",
                subject_locks="核心主体保持正中，纹理质感清晰",
                environment_response="丁达尔光束穿梭产生强烈景深视差",
                keyframe_strategy="首尾双关键帧控制"
            ),
            manim_layer_spec=f"顶部标题【{title}】，中央醒目疑问高光",
            comfy_ai_layer_spec=f"神秘宏大场景，正中央放置关于【{topic}】的核心标志物，电影级深色背景"
        ))

        # Shot 2: Deduction
        engine.add_shot(DirectorShot(
            shot_index=2,
            beat=NarrativeBeat.DEDUCTION,
            duration_seconds=12.0,
            voiceover_script="我们顺着底层逻辑拆解，一切规律立刻无所遁形！",
            subtitle_text="逐步推导演示底层逻辑：",
            motion_contract=CameraMotionContract(
                start_framing="主角侧面中景",
                mechanism=CameraMechanism.TRACKING_SLIDE,
                path_and_direction="相机保持高度水平平移",
                speed_curve="平稳匀速横移滑轨",
                end_framing="主角操作分析仪器",
                subject_locks="主角保持在黄金分割线，动作自然",
                environment_response="前景虚化物体掠过提供明显运动证据，背景数据流持续展开",
                keyframe_strategy="单参考图运镜"
            ),
            manim_layer_spec="中央安全舞台绘制推导图表与数学公式演化",
            comfy_ai_layer_spec="未来科技感与古典东方融合的研究室，流光溢彩"
        ))

        # Shot 3: Aha Moment
        engine.add_shot(DirectorShot(
            shot_index=3,
            beat=NarrativeBeat.AHA_MOMENT,
            duration_seconds=5.0,
            voiceover_script="看！真正的底层规律，其实如此简单纯粹！",
            subtitle_text="这就是决定性的核心结论！",
            motion_contract=CameraMotionContract(
                start_framing="主角面部特写",
                mechanism=CameraMechanism.VERTIGO_ZOOM,
                path_and_direction="相机沿光轴缓慢后退同时焦距等速放大",
                speed_curve="平稳缓入缓出",
                end_framing="主角头肩尺度锁定，背景剧烈透视拉伸",
                subject_locks="主角面容绝对稳定，五官形态锁定",
                environment_response="背景产生震撼的空间扭曲与拉伸感",
                keyframe_strategy="Dolly-Zoom潜变量控制"
            ),
            manim_layer_spec="高光 CalloutCard 顿悟卡片弹出，金光粒子环绕",
            comfy_ai_layer_spec="震撼顿悟时刻，时空仿佛定格，金色光环与流光粒子爆发"
        ))

        # 3. 导出分镜
        sb_path = os.path.join(self.project_root, f"storyboards/{title}_production_pack.md")
        os.makedirs(os.path.join(self.project_root, "storyboards"), exist_ok=True)
        with open(sb_path, "w", encoding="utf-8") as f:
            f.write(engine.export_production_markdown())

        # 4. 生成 Manim 骨架
        manim_code = engine.generate_manim_scaffold(f"{title.replace(' ', '')}GeneratedScene")
        scene_path = os.path.join(self.project_root, f"scenes/{title.lower().replace(' ', '_')}_scene.py")
        with open(scene_path, "w", encoding="utf-8") as f:
            f.write(manim_code)

        # 5. 生成对应的 ComfyUI 工作流
        comfy_workflows = []
        for shot in engine.shots:
            cw = self.comfy_adapter.inject_shot(shot)
            cw_path = os.path.join(self.project_root, f"comfyui_workflows/{title}_shot_{shot.shot_index:02d}.json")
            with open(cw_path, "w", encoding="utf-8") as f:
                json.dump(cw, f, ensure_ascii=False, indent=2)
            comfy_workflows.append(cw_path)

        return {
            "title": title,
            "storyboard": sb_path,
            "scene_code": scene_path,
            "comfyui_workflows": comfy_workflows,
            "shots_count": len(engine.shots)
        }
