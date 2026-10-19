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
