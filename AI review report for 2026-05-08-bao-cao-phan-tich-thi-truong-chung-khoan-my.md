# AI Review Report — 2026-05-08 6AM PDT Full Report

## Facts

| Field | Value |
|-------|-------|
| **URL** | `https://phanmaikienhung.github.io/market-report/2026-05-08-bao-cao-phan-tich-thi-truong-chung-khoan-my.html` |
| **SLUG** | `2026-05-08-bao-cao-phan-tich-thi-truong-chung-khoan-my` |
| **Report date** | 2026-05-08 (Friday/T6) |
| **Trigger time** | 06:00 AM PDT (cron `market-report-full`) |
| **Report type** | FULL — Daily Intelligence Report (T2–T6) |
| **Title** | BÁO CÁO PHÂN TÍCH THỊ TRƯỜNG CHỨNG KHOÁN MỸ |
| **Review date** | 2026-05-08 |
| **Review method** | Automated + manual 7-category check against reviewer_rules.md + anti_patterns.md |
| **Verdict** | ✅ **PASS** |

## Summary

Report chất lượng cao với cấu trúc 7-section đầy đủ, 4-pillar analysis (Macro, Geopolitics, Sector/Micro, Commodities/FX), convergence/divergence analysis rõ ràng. Tất cả dữ liệu số chính xác, so khớp với Yahoo Finance close May 7 và pre-market futures. Không có source name leaks, không có lỗi arithmetic, không có lỗi ET/PDT conversion. Report có độ sâu phân tích tốt với 3 scenarios + probability + risk register. Verdict = PASS.

## Issue counts

| Severity | Count |
|----------|-------|
| 🔴 CRITICAL | 0 |
| 🟡 MAJOR | 0 |
| 🟢 MINOR | 2 |

---

## Detailed Issues

### 🟢 MINOR-001: Index ticker notation (`^XXX`) inconsistent with previous style

- **Location:** Section I.2 "Verified Closes" — Equity Indices table
- **Exact quote:** `S&P 500 (^GSPC)` | `NASDAQ Composite (^IXIC)` | `Dow Jones (^DJI)` | `Russell 2000 (^RUT)` | `30Y Treasury Yield (^TYX)`
- **Problem:** Uses Yahoo Finance `^` ticker notation for indices. Previous reports (e.g., 2026-05-07) used plain names like "S&P 500" without tickers, or tickers only in data source footer. Not an error per se, but inconsistent with site-wide style. Also `^TYX` is a yield index, not a stock — the `^` prefix is more commonly associated with stock/ETF tickers.
- **Fix:** Standardize to plain index names in tables: `S&P 500`, `NASDAQ Composite`, `Dow Jones`, `Russell 2000`, `30Y Treasury Yield`. Keep tickers only in "Data sources" footer if needed for transparency.
- **Learned:** Maintain consistent index naming style across reports — use plain names in body tables, reserve tickers for footnotes/data sources.

### 🟢 MINOR-002: Section IV.1 table header mislabeled

- **Location:** Section IV.1 "Sector Performance" table
- **Exact quote:** Header: `| Sector | % Change | Xu hướng |`
- **Problem:** The `% Change` column header is misleading because the column actually shows percentage changes (e.g., `-1.92%`, `-1.82%`). This IS correct — the column does contain % values. However, in previous reports, the header was typically labeled `Thay đổi` or `Change`. The `%` symbol in the header is redundant since the values already have `%`. Minor style preference.
- **Fix:** Change to `Thay đổi` or `%` (just the symbol, not `% Change`) for consistency. Or keep as-is — this is extremely minor.
- **Learned:** Standardize table headers across reports for visual consistency.

---

## Rules & Anti-Patterns Checked

| Rule | Status | Notes |
|------|--------|-------|
| RULE-001 (YTD verified) | ✅ PASS | No YTD claims for individual indices |
| RULE-002 (Live price timing) | ✅ PASS | Pre-market data appropriate for 6AM PDT |
| RULE-003 (ET→PDT conversion) | ✅ PASS | No ET→PDT conversions in body — all times already PDT or EDT for specific data points |
| RULE-004 (Body times PDT) | ✅ PASS | All body times in PDT or explicitly labeled as EDT (e.g., "10:00 AM EDT" for U Mich which is ET-based) |
| RULE-005 (Anonymization) | ✅ PASS | No banned source names found (grep: Steve Le, Viet Hustler, tapchiphowall, Ryan Tran, Nhật Thanh Lê, Ashley Truong) |
| RULE-006 (Claim strength) | ✅ PASS | Claims like "Weak NFP → less rate hike" supported by ≥3 data points (NFP 115K vs 178K, VIX 16.88, bond futures up) |
| RULE-007 (Arithmetic) | ✅ PASS | All pct changes verified (SPX -0.38%, NQ -0.13%, Dow -0.63%, VIX -1.17%, Gold +0.55%, WTI +0.26%, etc.) |
| RULE-008 (Filename PDT) | ✅ PASS | Filename `bao_cao_thi_truong_20260508_6AM.md` matches 06:00 PDT trigger |
| RULE-009 (Weekend baseline) | ✅ PASS | Baseline is May 7 (Friday) — correct for T6 report |
| RULE-010 (Symbol `$`) | ✅ PASS | No incorrect `$` prefix on indices (VIX, Russell use plain numbers) |
| RULE-011 (Yield change units) | ✅ PASS | `30Y Treasury Yield (^TYX) | 4.9540 | -0.0150 | -0.30%` — value in decimal, change in decimal points, pct in % — unambiguous |
| RULE-012 (Weekday label) | ✅ PASS | "Thứ Sáu 08/05/2026" — 08/05/2026 is indeed Friday |
| RULE-013 (Global market holidays) | ✅ PASS | N/A — report uses US market data (May 7 Friday close) |
| RULE-014 (Overnight futures) | ✅ PASS | Pre-market futures section correct for Friday morning |
| RULE-015 (Body language) | ✅ PASS | Body is 100% Vietnamese |

## Anti-Patterns Checked

| Pattern | Status | Notes |
|---------|--------|-------|
| AP-001 (Russell YTD) | ✅ PASS | No YTD spread derivation |
| AP-002 (Live price=open) | ✅ PASS | Pre-market data, correct for 6AM PDT |
| AP-003 (ET→PDT error) | ✅ PASS | No conversion errors |
| AP-004 (Filename ET) | ✅ PASS | Filename uses PDT trigger time |
| AP-005 (Arithmetic %) | ✅ PASS | No "from X to Y" percentage claims |
| CASE-024 (China macro) | ✅ PASS | N/A — report scope is US markets |
| CASE-025 (Energy inflation) | ✅ PASS | Oil price analysis present (WTI $95, Shell warning, Iraq discovery) |
| CASE-026 (Housing cost) | ✅ PASS | N/A — report focuses on market data, not CPI detail |
| CASE-027 (Global macro) | ✅ PASS | International markets mentioned (DAX, Nikkei, Hang Seng, CAC, STOXX) in headline section |

---

## New Rules Proposed

**None.** This review didn't discover a pattern that requires a new rule. Both minor issues are style preferences.

---

## Guidelines for AI Report Generator

1. **[MINOR] Standardize index naming:** Use plain index names (`S&P 500`, `NASDAQ Composite`) in body tables. Reserve `^` ticker notation for data source footers only.
2. **[MINOR] Standardize table headers:** Use consistent header labels across reports for sector performance tables (`Thay đổi` instead of `% Change`).

---

## Checklist for Next Report

- [ ] All body time values in PDT (not ET), unless explicitly labeled
- [ ] Table column headers match the data format of their values
- [ ] Index names use plain English/Vietnamese, not Yahoo Finance tickers
- [ ] Commodity tables use consistent decimal precision
- [ ] Scenario probabilities sum to 100% and are explicitly noted

---

*Review completed by Apollo — AI Report Reviewer*
*Date: 2026-05-08*
