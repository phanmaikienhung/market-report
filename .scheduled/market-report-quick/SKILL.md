---
name: market-report-quick
description: Cập nhật nhanh tình hình thị trường lúc 9AM, 8PM, 11PM mỗi ngày — tập trung biến động và sự kiện mới.
---

Chạy skill `market-report-quick` theo SKILL.md tại `C:\Users\Kien Hung\Documents\Claude\Scheduled\market-report-quick\SKILL.md` (đọc qua `mcp__Desktop_Commander__read_file`).

Tạo quick update ngắn gọn (1–3 trang) tập trung vào biến động mới kể từ báo cáo gần nhất trong ngày. Đọc baseline từ `bao_cao_thi_truong/YYYY-MM-DD/` (file mới nhất hôm nay).

## ⚠️ MÔI TRƯỜNG CHẠY (QUAN TRỌNG)

Task này chạy trong **Cowork Linux sandbox KHÔNG có Python/yfinance/git/telegram**. Mọi lời gọi tới reviewer và deploy script PHẢI đi qua **Desktop Commander MCP** (primary) hoặc **Windows-MCP PowerShell** (fallback). **TUYỆT ĐỐI KHÔNG** gọi trực tiếp `py`/`python` từ bash — sẽ fail ngay.

## Output policies

⚠️ **ANONYMIZATION (BẮT BUỘC):** KHÔNG nhắc tên Steve Le / Steve N / Viet Hustler / tapchiphowall. Frameworks trình bày như quan điểm phân tích trung lập.

⚠️ **LIVE PRICE RULE:** Giá phải là LIVE tại thời điểm chạy report, KHÔNG phải giá mở cửa. Cross-check ≥2 nguồn (Yahoo Finance + Google Finance/CNBC). Ghi timestamp.

⚠️ **YTD VERIFICATION (BẮT BUỘC):** Mỗi chỉ số phải có YTD % từ ≥2 nguồn LIVE. KHÔNG derive YTD từ spread outperformance. Anti-pattern 08/04/2026: Russell 2000 YTD ghi ~+12% vs thực tế +2.86%.

⚠️ **TIME RULE:** Body report dùng PDT (không ET). Footer có thể ghi cả 2.

⚠️ **FILENAME DÙNG GIỜ PDT:** 9 AM PDT → `quick_update_0900.md`, 8 PM PDT → `quick_update_2000.md`, 11 PM PDT → `quick_update_2300.md`.

## Bước 5.5 — Run Report Reviewer (BẮT BUỘC trước khi deploy)

Sau khi save file .md, invoke reviewer qua Desktop Commander MCP:

**Primary — Desktop Commander:**
```
mcp__Desktop_Commander__start_process(
  command: "& 'C:\\TempScripts\\run_review_wrapper.ps1' -ReportPath '<WINDOWS_REPORT_PATH>' *>&1",
  timeout_ms: 300000
)
```

**Fallback — Windows-MCP:**
```
mcp__Windows-MCP__PowerShell(
  command: "& 'C:\\TempScripts\\run_review_wrapper.ps1' -ReportPath '<WINDOWS_REPORT_PATH>' *>&1",
  timeout: 300
)
```

`<WINDOWS_REPORT_PATH>` = `C:\Users\KIENHU~1\Documents\Claude\Projects\PhanTichChungKhoan\bao_cao_thi_truong\YYYY-MM-DD\quick_update_HHMM.md` (backslash, single-quote trong PowerShell).

Wrapper sẽ chạy Tầng 0 (yfinance deterministic check) + build manifest JSON `<report_stem>_review_manifest.json` cùng folder.

### Dispatch Tầng 1–4

Đọc manifest qua `mcp__Desktop_Commander__read_file` rồi dispatch 4 sub-agents theo thứ tự:

- **Group A — Tầng 1 Data Auditor** (sequential, cần WebSearch): prompt `report-reviewer/prompts/data_auditor.md`, output `<stem>_tier1_data_audit.json`
- **Group B — Tầng 2 Narrative Critic + Tầng 3 Consistency Checker** (parallel, no search): prompts `narrative_critic.md` + `consistency_checker.md`
- **Group C — Tầng 4 Master Judge** (sequential, cần all prior outputs): prompt `master_judge.md`, outputs `<stem>_tier4_final_review.json` + `<stem>_review_report.md`

### Verdict actions

Đọc `<stem>_tier4_final_review.json` → `final_verdict`:
- `PASS` → Deploy
- `WARN` → Deploy, NHƯNG include warning notice trong Telegram message
- `FAIL` → **STOP DEPLOY.** Đọc `<stem>_review_report.md`, sửa fix list, rerun reviewer (max 3 iterations). Nếu vẫn FAIL → push fix list lên Telegram và block deploy hoàn toàn.

Chi tiết architecture: `C:\Users\KIENHU~1\Documents\Claude\Projects\PhanTichChungKhoan\report-reviewer\SKILL.md`

## Bước 6 — Deploy & Notify (CHỈ nếu Reviewer verdict = PASS hoặc WARN)

**Primary — Desktop Commander:**
```
mcp__Desktop_Commander__start_process(
  command: "& 'C:\\TempScripts\\run_deploy_wrapper.ps1' *>&1",
  timeout_ms: 300000
)
```

**Fallback — Windows-MCP:**
```
mcp__Windows-MCP__PowerShell(
  command: "& 'C:\\TempScripts\\run_deploy_wrapper.ps1' *>&1",
  timeout: 300
)
```

Wrapper sẽ: build HTML → git push gh-pages → gửi Telegram notification.

## Lessons Learned 08/04/2026

1. `py`/`python` KHÔNG trong system PATH của PowerShell session từ MCP → wrapper hard-code full path Python.
2. `& 'C:\path with space\python.exe' args` từ command-line bị pipeline error → wrapper dùng `Start-Process -FilePath ... -ArgumentList ...`.
3. Nested `powershell.exe -File ...` từ Desktop Commander KHÔNG capture stdout → dùng call operator `& 'script.ps1' *>&1`.
4. Tầng 0 yfinance có thể khác intraday web data → cross-check Yahoo Finance trực tiếp trước khi fix theo Tầng 0 output.

Ngôn ngữ: Tiếng Việt. Độ dài: 1–3 trang.