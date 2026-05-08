---
name: report-learning-loop-daily
description: So sánh báo cáo Claude hôm nay với distill Steve Le + tapchiphowall lúc 6:30 PM PDT, build learning artifacts (AAR + Reflexion + Cases).
---

Chạy skill `report-learning-loop` tại `/sessions/peaceful-pensive-babbage/mnt/PhanTichChungKhoan/report-learning-loop/SKILL.md` để build learning artifacts cho ngày hôm nay.

## MÔI TRƯỜNG

Task chạy trong Cowork Linux sandbox. Skill này PURE-LLM + Python stdlib — KHÔNG cần wrapper Windows MCP, KHÔNG cần yfinance/git. Dùng Read/Write/Bash tools trực tiếp.

## Pipeline 7 stages (bám sát SKILL.md)

### Stage 1 — Discover inputs
```bash
cd /sessions/peaceful-pensive-babbage/mnt/PhanTichChungKhoan
python3 report-learning-loop/scripts/discover_inputs.py
```
Exit code 0=READY, 1=PARTIAL, 2=MISSING. Nếu MISSING → write note vào `market-intelligence-report/references/learning_log.md` và stop. Nếu PARTIAL → continue nhưng flag degraded trong AAR Stage 6.

### Stage 2 — Extract claims (parallel sub-agents)
Đọc manifest `learning/daily/<date>/stage1_manifest.json`. Với MỖI source file (reports + distills), dispatch 1 sub-agent qua Task tool (song song) dùng prompt `report-learning-loop/prompts/claim_extractor.md`. Input: source file path + source_tag + link đến `claim_ontology.md`. Output mỗi sub-agent: ghi `learning/daily/<date>/claims_<source_tag>.json`.

Target 20-50 claims/source. Dùng source_tag chính xác: `claude_6am`, `claude_3pm`, `claude_quick_0900`, `claude_quick_1130`, `claude_quick_2000`, `claude_quick_2300`, `steve_le`, `tcpw`.

### Stage 3 — Build comparison matrix
```bash
python3 report-learning-loop/scripts/build_matrix.py <YYYY-MM-DD>
```
Output: `comparison_matrix.json` với buckets + summary. Script deterministic, phát hiện DATA_DIFF, CLAUDE_INTERNAL_DIFF, DISAGREE_DIRECTION, UNIQUE_*, AGREE.

### Stage 4 — Compute metrics
```bash
python3 report-learning-loop/scripts/compute_metrics.py <YYYY-MM-DD>
```
Output: `metrics.json` + update `learning/rolling_metrics.json` (60-day window).

### Stage 5 — Reflexion narrative (sub-agent)
Dispatch 1 sub-agent dùng prompt `report-learning-loop/prompts/reflexion_writer.md`. Inputs: `comparison_matrix.json`, `metrics.json`, summary của sources. CONSTRAINT: mỗi insight PHẢI cite metric value hoặc source_span hoặc cluster_id — chống hallucinate. Output: `learning/daily/<date>/reflection.md`.

### Stage 6 — AAR composition (sub-agent)
Dispatch 1 sub-agent dùng prompt `report-learning-loop/prompts/aar_composer.md`. Inputs: matrix, metrics, reflection.md, `references/aar_template.md`. Tuân thủ 4-question format. Output: `learning/daily/<date>/aar.md`.

### Stage 7 — Case mining + lifecycle
**7a — Case mining (sub-agent):**
Với mỗi bucket severity ∈ {critical, major} và relationship ∈ {UNIQUE_*, DATA_DIFF, CLAUDE_INTERNAL_DIFF, DISAGREE_DIRECTION}, dispatch sub-agent dùng prompt `case_miner.md`:
1. Gọi `python3 report-learning-loop/scripts/case_manager.py match '<keywords_json>'` để check duplicate
2. Nếu match (score ≥ 0.5): `case_manager.py increment CASE-NNN`, promote nếu occurrence ≥ 2
3. Nếu không: viết case payload JSON rồi `case_manager.py add <payload.json>`

Auto-promote PROVISIONAL → CONFIRMED khi `has_quantitative_proof=true AND severity=critical`.

**7b — Daily aging:**
```bash
python3 report-learning-loop/scripts/case_manager.py age
```

**7c — Append learning_log.md (backward compat):**
Append entry mới vào `market-intelligence-report/references/learning_log.md` theo format 4 section cũ (Gaps/Strengths/Discrepancies/Patterns) + links đến artifacts mới.

**7d — Weekly rollup (chỉ Sunday):**
Nếu hôm nay là Chủ nhật → chạy `python3 report-learning-loop/scripts/weekly_rollup.py`. Promotes provisional ≥2 occurrences, escalate to `report-reviewer/references/anti_patterns.md`.

## Output final

1. `learning/daily/<date>/` có đủ: stage1_manifest.json, claims_*.json (per source), comparison_matrix.json, metrics.json, reflection.md, aar.md, cases_created.json
2. `learning/cases/index.json` updated nếu có case mới/incremented
3. `market-intelligence-report/references/learning_log.md` appended
4. Print tóm tắt vào chat: coverage%, critical_gaps, cases_created, link đến aar.md

## Failure handling

- Nếu MISSING inputs → stop với note
- Nếu PARTIAL → proceed degraded
- Nếu Python script lỗi → log error, continue stage tiếp nếu có thể
- Nếu sub-agent timeout → retry 1 lần rồi skip

Ngôn ngữ: Tiếng Việt cho AAR + Reflexion + learning_log append.