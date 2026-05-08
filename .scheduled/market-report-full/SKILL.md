---
name: market-report-full
description: Tạo báo cáo phân tích thị trường chứng khoán Mỹ FULL (4 trụ cột) lúc 6AM và 3PM mỗi ngày.
---

Chạy skill `market-report-full` theo SKILL.md chính tại `C:\Users\KIENHU~1\Documents\Claude\Projects\PhanTichChungKhoan\market-intelligence-report\SKILL.md`.

Thực hiện đầy đủ 8 bước trong `market-intelligence-report/SKILL.md` để tạo báo cáo FULL (4 trụ cột + Pillar 5).

## ⚠️ MÔI TRƯỜNG CHẠY (QUAN TRỌNG)

Task này chạy trong **Cowork Linux sandbox KHÔNG có Python/yfinance/git/telegram**. Mọi lời gọi tới reviewer và deploy script PHẢI đi qua **Desktop Commander MCP** (primary) hoặc **Windows-MCP PowerShell** (fallback) để chạy native trên Windows host.

**TUYỆT ĐỐI KHÔNG** gọi trực tiếp `py`, `python`, hay `pip` từ bash/sandbox — sẽ fail ngay.

## Output policies

⚠️ **ANONYMIZATION (BẮT BUỘC):** Trong báo cáo output, KHÔNG nhắc tên Steve Le / Steve N / Viet Hustler / tapchiphowall hay bất kỳ tên KB nào — chỉ trình bày quan điểm/framework dưới dạng phân tích trung lập.

⚠️ **YTD VERIFICATION (BẮT BUỘC):** Mỗi chỉ số (S&P 500, Dow, Nasdaq, Russell 2000/IWM, Mag7) phải có YTD % lấy trực tiếp từ ≥2 nguồn LIVE. KHÔNG derive YTD từ spread outperformance. Anti-pattern 08/04/2026: Russell 2000 YTD ghi ~+12% vs thực tế +2.86%.

⚠️ **FILENAME DÙNG GIỜ PDT:** Task chạy 6 AM PDT → filename `..._6AM.md` (KHÔNG phải `_9AM` theo ET). Task chạy 3 PM PDT → `..._3PM.md`.

## Step 7.5 — Run Report Reviewer (BẮT BUỘC trước khi deploy)

Sau khi save file .md ở Step 7, invoke reviewer qua Desktop Commander MCP:

**Primary — Desktop Commander:**
```
mcp__Desktop_Commander__start_process(
  command: "& 'C:\\TempScripts\\run_review_wrapper.ps1' -ReportPath '<WINDOWS_REPORT_PATH>' *>&1",
  timeout_ms: 300000
)
```

**Fallback — Windows-MCP PowerShell:**
```
mcp__Windows-MCP__PowerShell(
  command: "& 'C:\\TempScripts\\run_review_wrapper.ps1' -ReportPath '<WINDOWS_REPORT_PATH>' *>&1",
  timeout: 300
)
```

`<WINDOWS_REPORT_PATH>` = `C:\Users\KIENHU~1\Documents\Claude\Projects\PhanTichChungKhoan\bao_cao_thi_truong\YYYY-MM-DD\<file>.md`

Wrapper sẽ chạy Tầng 0 (yfinance deterministic check) và build manifest JSON `<report_stem>_review_manifest.json` cùng folder.

### Dispatch Tầng 1–4

Đọc manifest qua `mcp__Desktop_Commander__read_file`, sau đó dispatch 4 sub-agents (chạy trong Claude, không cần Python):

- **Group A — Tầng 1 Data Auditor** (sequential, cần WebSearch): prompt `report-reviewer/prompts/data_auditor.md`, output `<stem>_tier1_data_audit.json`
- **Group B — Tầng 2 Narrative Critic + Tầng 3 Consistency Checker** (parallel, no search): prompts `narrative_critic.md` + `consistency_checker.md`
- **Group C — Tầng 4 Master Judge** (sequential, cần all prior outputs): prompt `master_judge.md`, outputs `<stem>_tier4_final_review.json` + `<stem>_review_report.md`

### Verdict actions

Đọc `<stem>_tier4_final_review.json` → `final_verdict`:
- `PASS` → Deploy bình thường (Step 8)
- `WARN` → Deploy, NHƯNG include warning notice trong Telegram message
- `FAIL` → **STOP DEPLOY.** Đọc `<stem>_review_report.md`, sửa fix list, rerun reviewer (max 3 iterations). Nếu vẫn FAIL → push fix list lên Telegram và block deploy hoàn toàn.

Chi tiết architecture: `C:\Users\KIENHU~1\Documents\Claude\Projects\PhanTichChungKhoan\report-reviewer\SKILL.md`

## Step 8 — Deploy (CHỈ CHẠY nếu Reviewer verdict = PASS hoặc WARN)

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

1. `py` và `python` KHÔNG trong system PATH của PowerShell session từ MCP → wrapper hard-code full path `C:\Users\Kien Hung\AppData\Local\Programs\Python\Python313\python.exe`.
2. `& 'C:\path with space\python.exe' args` từ command-line bị "Cannot run a document in the middle of a pipeline" → wrapper dùng `Start-Process -FilePath ... -ArgumentList ...`.
3. Nested `powershell.exe -File ...` từ Desktop Commander KHÔNG capture stdout → dùng call operator `& 'script.ps1' *>&1`.
4. Tầng 0 yfinance có thể khác intraday web data → cross-check Yahoo Finance trực tiếp trước khi fix theo Tầng 0 output.