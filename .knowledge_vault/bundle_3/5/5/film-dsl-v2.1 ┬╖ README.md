# film-dsl-v2.1.3.1 — Centralized VERIFY Registry

**v2.1.3.1 (2026-09-08) — Pipeline VERIFY consolidation (schema unchanged).**

All VERIFY rules from v2.1.0 / v2.1.1 / v2.1.2 / v2.1.3 have been backfilled into a single canonical `verify_checks[]` array in `schema/pipeline-stages.json`. Each rule now carries `check_id`, `stage`, `layer`, `severity` (ERROR/WARN), `description`, and `introduced_in` (version lineage). The natural-language `rules` blocks inside `stages[].process.rules` are retained as informal narrative but are no longer the source of truth — `verify_checks[]` is.

**Registry summary (55 checks total):**
| Version | Count | New capabilities |
|---|---|---|
| 2.1.0 | 39 | base pipeline: MU segmentation, MSSS containers, DIR/PERF intents, IR provenance, S5 output completeness, render_hint_only leak guards |
| 2.1.1 | 7 | audio_beat_track alignment, transition.duration_defined, pacing.duration_hint_respected, retime_method/post_intent leak guards, montage scale_lock consistency |
| 2.1.2 | 6 | episode.container_layout, episode.beat_container_containment, episode.tension_apex_alignment, shot_container_ref time-match, bridge_beat_reachable, container.entry_transition enum |
| 2.1.3 | 3 | episode.10container_arc_apex_count, episode.cross_container_silence_pockets, episode.inter_episode_boundary_dissolve |

**By stage:** S1-MUS 6, S2-MSSS 6, S2.5-DIR 5, S2.7-PERF 5, S3-IR 14, S5-OUT 19.
**By severity:** ERROR 45, WARN 10.

A new `verify_checks_summary` block at the top of `pipeline-stages.json` exposes the same counts programmatically for downstream tooling.

All three example workflows (30s, 150s, 300s) revalidated: **PASS** against the JSON Schema. No changes to any workflow file were required.

---

# film-dsl-v2.1.3

**v2.1.3 (2026-09-08) — 10-Container Extension + Complete Shots DSL + Ready-to-Generate Apex Prompts.**

**New in v2.1.3:**
- Schema: `Container.index` max widened to 9, `Container.time_start_sec` max widened to 270.0; `Episode.container_count` max widened to 10; `Episode.total_duration_sec` max widened to 300.0; `AudioBeatTrack.total_length_sec` max widened to 300.0 (all backward compatible).
- Preset: added `container_role_arc.10_container_arcs` with 4 arc templates — `double_peak_late`, `long_climb_single_apex`, `steady_alternation`, `front_loaded_reveal`.
- Pipeline stages: added VERIFY checks `episode.10container_arc_apex_count`, `episode.cross_container_silence_pockets`, `episode.inter_episode_boundary_dissolve`.
- 150s example (`xianxia-150s-episode.workflow.json`): shots_dsl expanded from stub to complete **25 shots × 15 Hell-Grind modules** (L1 human-readable + L2 render_prompt + L3 IR reference). All 15 modules per shot: SCENE_CONTEXT / ACTIVE_REFERENCES / LOCATION_MAP / FIRST_FRAME_AND_SPATIAL_BLOCKING / FORMAT_MODE / OPTICS / CAMERA / ACTION_TIMING / PHYSICS / LIGHTING / AUDIO / CHARACTER_ACTING / STYLE / QUALITY / POSITIVE_CONSTRAINTS. Post-hint layer (retime_method, post_intent, transition_duration_frames) does NOT leak into L2 prompt bodies.
- 300s example (`xianxia-300s-episode-10container.workflow.json`) — new file: 10 containers × 30s, `double_peak` arc, 50 shots, 41 beats, 2 silence-pocket boundaries between climaxes, silk_dissolve out.
- Apex generation-ready pack: `examples/c4_apex_shot_prompts/` — 5 self-contained `.prompt.md` files (SH_16..SH_20) plus one combined file, each with the 15-module block ready to paste into Higgsfield / Runway / Kling / Veo. Generation order noted: SH_16 → SH_17 → SH_19 → SH_20 → SH_18 (defer smash_cut shot until tone is locked).

**Validation (300s 10-container example): 14/14 PASS** — schema; container layout; narrative_proportion sum; shots total; frame_precision; shots_per_container; duration.container; beat_container_containment; transition.duration_defined; pacing.duration_hint_respected; audio_beat_alignment; tension_apex_alignment; 10container_arc_apex_count; cross_container_silence_pockets; inter_episode_boundary_dissolve; montage_group_integrity.

---

# film-dsl-v2.1.2

**v2.1.2 (2026-09-08) — Episode Layer Patch (backward compatible with v2.1.0 and v2.1.1).**
Adds top-level `episode` + `containers[]` + cross-container audio beats so a full 150s (5×30s) or 300s (10×30s) episode fits the same DSL.

**New in v2.1.2:**
- Top-level `episode` (episode_id, total_duration_sec, container_count=N, tension_arc_shape, apex_container_ref, cold_open, tag_out)
- Top-level `containers[]` (container_id, index, time_start_sec, role, tension_peak, asl_target_sec, beat_range, entry_transition, bridge_to_next)
- `AudioBeatTrack.beats[]` extended: `container_ref` (which container the beat lives in) + `role` (container_open/peak/close/cross_container_bridge/episode_apex/internal)
- Cross-container `montage_groups[].container=null` support (group can span multiple containers)
- Preset: `container_role_arc.5_container_arcs`, `tension_peak_hints_by_role`, `asl_target_by_role_sec`
- VERIFY: +3 checks — `episode.container_layout`, `episode.beat_container_containment`, `episode.tension_apex_alignment`

**Fully-populated example:** `examples/xianxia-150s-episode.workflow.json` — 25 shots, 25 beats across 5 containers (setup/escalation/turn/apex/coda), arc=long_tail_late_break, apex at C4 (tension_peak=0.90 at `@beat_realization_release` + `@beat_mountain_roar_far`), coda ends on silk_dissolve to `@beat_c5_close`. All 13 verdict checks PASS.

---

# film-dsl-v2.1.1

**v2.1.1 (2026-09-08) — Rhythm & Post-Edit Layer Patch (backward compatible with v2.1.0).**
Adds six field extensions and three VERIFY checks so the pipeline covers post-edit trim/slip/slide intent, audio-anchored cuts, retime method hints, transition durations, and preset-driven duration recommendations.

**Backward compatibility:** `workflow_id` and `version` now accept both v2.1 and v2.1.1 constants; all new fields are optional; the v2.1.0 example remains valid.

**New in v2.1.1:**
- Top-level `audio_beat_track` (diegetic/metronome/placeholder/scratch) with named `@beat_xxx` beats
- `Temporal.retime_method` (optical_flow / frame_blend / nearest / timewarp) — L3 post hint only
- `Temporal.cut_in_beat_ref` / `cut_out_beat_ref` — bind edges to named audio beats
- `RhythmProfile.cut_triggers[].transition_duration_frames` — silk_dissolve = 36 default (xianxia) / 24 (wuxia)
- `Shot.post_intent` — trim priority, slip/slide flags, head/tail handles, preferred anchor
- `CanonicalDSL.montage_groups[].scale_lock + rhythm_signature`
- Preset: `duration_hint_by_function` (10 function types) + `transition_duration_defaults_frames`
- VERIFY: +3 checks — `pacing.duration_hint_respected`, `transition.duration_defined`, `audio_beat_alignment`

**All L3-only fields (post_intent, retime_method, transition_duration_frames) are explicitly barred from L2 render_prompt by the extended `render_hint_leak` check.**

---

# film-dsl-v2.1

Cinematic Semantic Compilation workflow — v2.1. Extends the CSCA + film-generation-v2 baseline with:

- structured **genre_lock** + preset registry
- five-axis **narrative_proportion** (visual / dialogue / action / sound / silence)
- **pacing_lock** (ASL, silence ratio, hard-cut ratio, container size)
- **direction_lock** + **performance_lock** — driving rule layers, not IR fields
- new stages **S2.5-DIR** and **S2.7-PERF** between MSSS and IR
- **three-tier output** L1/L2/L3 — only L2 is fed to video models
- **delta-encoded shots** — first shot of each sequence is FULL; others inherit + override
- **library refs** for mise_en_scene / sound / location — no duplication
- **per-hard-field provenance** with three states (explicit / inferred / decision)
- **render_hint_only** fields marked so they never leak into video-model prompts

## Files

```
film-dsl-v2.1/
├── schema/
│   ├── film-dsl-v2.1.schema.json      # JSON Schema (draft 2020-12), authoritative type spec
│   └── pipeline-stages.json           # canonical 7-stage list with process rules & VERIFY checks
├── presets/
│   └── genre-preset-registry.json     # @preset_classical_xianxia_v1, @preset_wuxia_grounded_v1
├── examples/
│   └── xianxia-30s-example.workflow.json  # complete 30s container, five shots, all 7 stages populated
└── README.md
```

## Design principles (three lines)

1. **Locks compress payload.** Every default lives in a top-level `*_lock`; per-shot content only overrides.
2. **Grammar is enumerated, prose is banned.** `MotionGrammar`, `CutGrammar`, `MicroLifeAtom` are closed enums — extend via preset, never per-shot free text.
3. **Provenance travels with every hard value.** No value enters the render prompt without an `explicit:<span>`, `inferred:<span>+evidence`, or `decision:<D-ID>` marker.

## Resolution order (top → bottom, later wins)

```
genre_lock.cinematography_preset_ref → resolved from presets/genre-preset-registry.json
                            │
                            ▼
                   preset defaults
                            │
                            ▼
                genre_lock.preset_override (replaces, not merges)
                            │
                            ▼
              *_lock top-level explicit values
                            │
                            ▼
        S2.5-DIR + S2.7-PERF intents (sequence/MU scoped)
                            │
                            ▼
               per-shot delta (SH_02..SH_05)
                            │
                            ▼
                     final IR shot
```

## Output tiers

| Tier | Size | Consumer | Rule |
|---|---|---|---|
| L1 | ~200 B/shot | director review | shot_no, size, motion, duration, one-line beat |
| L2 | ~2 KB/shot | video model (Higgsfield / Sora / Veo / Kling / Seedance) | Hell Grind 15 modules, natural language, Style Prefix unmodified, Closing Tag unmodified, NO render_hint fields |
| L3 | ~4 KB/shot | post pipeline (DaVinci Resolve, After Effects, editor timeline) | full typed IR + provenance + render_hints |

**A single L2 render_prompt module bag must never reference vibration.spectrum, motion_blur_samples, bezier control points, or numeric acceleration curves — those are `render_hint_only` and live only in L3.**

## Genre presets available

- `@preset_classical_xianxia_v1` — 85mm long lens (default), teal+amber grade, candlelight ancient key, silk dissolve transitions, silence-is-content policy, xianxia-specific rules for flying wire / sword qi / silk ribbon motion blur.
- `@preset_wuxia_grounded_v1` — extends xianxia; 50mm, handheld default, ASL ~2.8s, silence ratio 0.10, no flying wire, no sword qi projectiles.

Extend by adding new `@preset_<name>_v<n>` entries. Use `extends` to inherit and override.

## Consuming the schema

- Validators: any Draft 2020-12 JSON Schema validator (Ajv 2020, python-jsonschema ≥ 4.18).
- Preset resolver: implement in your S3-IR generator; deep-merge preset defaults, then apply preset_override (as REPLACE), then explicit lock values, then intents, then per-shot delta.
- VERIFY runner: consume `pipeline-stages.json` S4-VERIFY.process.checks; each check is a rule id + human rule string — implement as unit tests over the IR.

## Interop with the existing Hell Grind + NSA + Gates pipeline

- NSA H1–H8 feed **S1-MUS** provenance (spans and D-IDs).
- Gate 1 asset stress test consumes **character_lock + prop_lock**.
- Gate 2 scene sheet consumes **libraries.location_library[].geo_map**.
- Gate 2b Shootability consumes **S3-IR shots + libraries.location_library**.
- Gate 3 prompt lint consumes **L2 render_prompt.modules**; witness check consumes **_provenance**.
- Gates 4–10 operate on generated media, unchanged.
