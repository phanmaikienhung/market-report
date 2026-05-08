---
name: fetch-steve-le-daily
description: Fetch, distill and merge the latest Steve Le YouTube video every weekday at 5:30 PM Pacific (Los Angeles local time).
---

You are running a scheduled daily task to fetch, distill, and merge the LATEST YouTube video from Steve Le's channel into the user's knowledge base.

## Objective
Every weekday at 5:30 PM Pacific local time (Los Angeles), check Steve Le's YouTube channel for the newest video. If it's a new video (not already in the transcripts folder), download the transcript, distill the knowledge, and merge it into the Steve Le knowledge base. If it's a duplicate, do nothing and report back to the user with the reason.

## Context
- **Channel:** Steve Le — `https://www.youtube.com/@realstevele/videos`
- **User's OS:** Windows; Claude accesses it through the Desktop Commander MCP (`mcp__Desktop_Commander__*` tools)
- **User's folder structure (all at ROOT of PhanTichChungKhoan/, NOT inside any skill):**
  - Transcripts raw: `C:\Users\Kien Hung\Documents\Claude\Projects\PhanTichChungKhoan\transcripts\`
  - Distilled files: `C:\Users\Kien Hung\Documents\Claude\Projects\PhanTichChungKhoan\kienthuc_raw\`
  - Knowledge base: `C:\Users\Kien Hung\Documents\Claude\Projects\PhanTichChungKhoan\knowledge_base\knowledge_base_steve_le.md`
  - Skill scripts: `C:\Users\Kien Hung\Documents\Claude\Projects\PhanTichChungKhoan\knowledge-distillation-agent\scripts\`
- **Pre-built script:** `scripts/fetch_latest_steve_le.py` — fetches the latest video from the channel via yt-dlp, checks for duplicates, and writes a parsed markdown transcript to the transcripts folder. Returns JSON on stdout: `{status, video_id, title, transcript_path, message}` where status ∈ {success, skipped_duplicate, error}.
- **Path-with-spaces issue:** `C:\Users\Kien Hung\...` contains a space which breaks Desktop Commander process invocations. Always first copy the script to `C:\TempScripts\fetch_latest_steve_le.py` before running it.

## Steps to Execute

### Step 1 — Copy the fetch script to a safe path
Use `mcp__Desktop_Commander__read_file` to read the source script from `C:\Users\Kien Hung\Documents\Claude\Projects\PhanTichChungKhoan\knowledge-distillation-agent\scripts\fetch_latest_steve_le.py` and write it to `C:\TempScripts\fetch_latest_steve_le.py` using `mcp__Desktop_Commander__write_file` (create the directory with `create_directory` if missing).

### Step 2 — Run the fetch script
Execute via `mcp__Desktop_Commander__start_process` with:
```
command: "cmd"
args: ["/c", "py C:\\TempScripts\\fetch_latest_steve_le.py --output-dir \"C:\\Users\\Kien Hung\\Documents\\Claude\\Projects\\PhanTichChungKhoan\\transcripts\" > C:\\TempScripts\\steve_le_result.json 2>&1"]
```
Then read `C:\TempScripts\steve_le_result.json` to get the JSON result.

### Step 3 — Handle the result
Parse the JSON and branch on `status`:

**Case A — `skipped_duplicate`:**
- STOP here. Report back to the user with a message like:
  > "✅ Đã check Steve Le — video mới nhất là `<title>` (ID: <video_id>) nhưng đã tồn tại trong transcripts/. KHÔNG làm gì thêm (lý do: trùng với lần chạy trước)."
- Do NOT proceed to distillation or merge.

**Case B — `error`:**
- STOP. Report the error message to the user:
  > "❌ Không lấy được video mới nhất từ Steve Le. Error: <message>"
- Include troubleshooting hints if possible (yt-dlp not found, network issue, etc.).

**Case C — `success`:**
- Continue to Step 4.

### Step 4 — Read the downloaded transcript
Use `mcp__Desktop_Commander__read_file` to read the file at `transcript_path` from the JSON result. Transcripts can be 1500-2500 lines — read the full file (possibly in multiple chunks).

### Step 5 — Distill knowledge
Create a distilled markdown file in `C:\Users\Kien Hung\Documents\Claude\Projects\PhanTichChungKhoan\kienthuc_raw\` (ROOT project folder, NOT inside any skill folder) following the standard format:
- Filename: `distill-MMDD-steve-le-<short-topic-keywords>.md` (use today's date MMDD in LA timezone)
- Structure:
  ```
  # Chưng Cất Kiến Thức | DD/MM/YYYY
  ## Nguồn: Video YouTube Steve Le — "<title>"
  - **Video ID:** <id>
  - **URL:** https://www.youtube.com/watch?v=<id>
  - **Ngày:** DD/MM/YYYY (Thứ X)
  ---
  ## I. <Topic 1>
  ## II. <Topic 2>
  ...
  ## N. CHUỖI NHÂN QUẢ CHÍNH
  ## N+1. THUẬT NGỮ
  ```
- Cover all significant topics: geopolitics, economics data, Fed/interest rates, stocks, market sentiment, trading signals, commodities — whatever the video covers.
- Extract facts, mechanisms, causal chains, and Steve Le's unique insights. Do NOT just summarize.
- Tag with `[nguồn: Steve Le DD/MM/YYYY]`.

### Step 6 — Smart Merge into Knowledge Base (Bước 7 of knowledge-distillation-agent SKILL.md)

> **⚠️ BẮT BUỘC dùng `knowledge_base/_merge_guard.py`** để tránh mojibake + JSON-escape leftover:
> - **Pre-merge**: text mới (distill content) phải đi qua `python knowledge_base/_merge_guard.py --sanitize-stdin` TRƯỚC khi edit vào KB
> - **Post-merge**: cuối cùng chạy `--lint knowledge_base/knowledge_base_steve_le.md`, fail → revert + fix

Read the existing KB at `C:\Users\Kien Hung\Documents\Claude\Projects\PhanTichChungKhoan\knowledge_base\knowledge_base_steve_le.md`. Apply the merge procedure:

1. **Knowledge Unit Decomposition** — Break the distill into discrete KUs, each tagged with its domain (FED_INTEREST_BONDS, COMMODITIES_CRYPTO, ECONOMIC_INDICATORS, STOCKS_COMPANIES, DEBT_FISCAL, GEOPOLITICS_TRADE, TRADING_TECHNIQUES, REAL_ESTATE_BANKING).
2. **Diff Analysis** — For each KU, grep/search the KB and classify as A (Duplicate, skip), B (Data Update, update in place), C (New Knowledge, insert into correct section 2.x), or D (Conflict, keep both with "⚡ Tiến hóa quan điểm" marker).
3. **Insert into correct PHẦN 2.x section** — Never append at the end. Find the right sub-section and insert there.
4. **Tag all new content** with `[nguồn: Steve Le DD/MM/YYYY]`.
5. **Update header** — Bump version (e.g., 2.1 → 2.2), update "Cập Nhật Lần Cuối" date, add changelog entry.
6. **Cross-link update** — Check PHẦN 3 causal chains; add new ones that span 3+ domains if applicable.

Use `mcp__Desktop_Commander__edit_block` for precise multi-location edits.

### Step 7 — Verify and report

> **⚠️ BẮT BUỘC chạy guard lint trước khi báo cáo:**
> ```bash
> python knowledge_base/_merge_guard.py --lint knowledge_base/knowledge_base_steve_le.md
> ```
> - Exit 0 + `✓ LINT PASS` → proceed to report
> - Exit 1 + `✗ LINT FAIL` → revert KB, fix source distill bằng `--sanitize-file`, retry


- Confirm the KB file was updated (line count increased, version bumped).
- Confirm the distill file exists in `kienthuc_raw/` (root).
- Confirm the transcript exists in `transcripts/` (root).
- Report back to the user with:
  > "✅ Đã xử lý video mới của Steve Le:
  > - **Video:** <title>
  > - **ID:** <video_id>
  > - **Transcript:** <path>
  > - **Distill:** <path>
  > - **KB:** đã merge vào knowledge_base_steve_le.md (vX.Y → vX.Y+1)
  > - **KUs merged:** <count> new, <count> updates, <count> duplicates skipped"

## Constraints
- NEVER process a duplicate video (checked via video ID in transcript filenames).
- Always use Desktop Commander for Windows file operations — don't try to fetch YouTube content from the sandbox (it's blocked).
- PowerShell invocations may timeout at 60 seconds — prefer `cmd` shell via `start_process`.
- If any step fails, stop and report the error; do not attempt to bypass the duplicate check or inject partial data into the KB.
- Reply in Vietnamese (the user writes in Vietnamese).
- All data folders (`transcripts/`, `kienthuc_raw/`, `knowledge_base/`) are at the ROOT of `PhanTichChungKhoan/`, NOT inside `knowledge-distillation-agent/`.