# AI Review Report — 2026-05-07 6AM PDT Full Report

## Facts

| Field | Value |
|-------|-------|
| **URL** | `https://phanmaikienhung.github.io/market-report/2026-05-07-bao-cao-phan-tich-thi-truong-chung-khoan-my.html` |
| **SLUG** | `2026-05-07-bao-cao-phan-tich-thi-truong-chung-khoan-my` |
| **Report date** | 2026-05-07 |
| **Trigger time** | 06:00 AM PDT (cron `market-report-full`) |
| **Report type** | FULL (T2–T6 weekday) |
| **Title** | BÁO CÁO PHÂN TÍCH THỊ TRƯỜNG CHỨNG KHOÁN MỸ |
| **Review date** | 2026-05-07 |
| **Review method** | Automated + manual 7-category check against reviewer_rules.md + anti_patterns.md |
| **Verdict** | ⚠️ **WARN** |

## Summary

Report có cấu trúc tốt, dữ liệu chính xác, phân tích 4-pillars đầy đủ. Một lỗi về thời gian (Rule 004: body table dùng ET thay vì PDT) và một vài inconsistencies nhỏ về formatting khiến verdict = WARN. Không có source name leaks, không có lỗi data nghiêm trọng.

## Issue counts

| Severity | Count |
|----------|-------|
| 🔴 CRITICAL | 0 |
| 🟡 MAJOR | 1 |
| 🟢 MINOR | 3 |

---

## Detailed Issues

### 🟡 MAJOR-001: Body time table uses ET instead of PDT (Rule 004)

- **Location:** Section I.1 "Timeline chi tiết phiên (giờ PDT)" — table row "Giờ PDT"
- **Exact quote:** Table header says `Giờ PDT` but column contains values like `07:00 ET`, `08:30 ET`, `09:00 ET`, `10:00 ET`
- **Problem:** Header labels column as PDT but entries are ET. This is confusing — the column should either be labeled `Giờ ET` or values should be converted to PDT (e.g., `04:00 PDT`, `05:30 PDT`, `06:00 PDT`, `07:00 PDT`)
- **Note:** The PDT equivalent in the "Chi tiết" column IS correct (e.g., `4:00 AM PDT — potential rate commentary`), so the conversion was done — it just wasn't applied to the "Giờ PDT" column
- **Fix:** Change column header to `Giờ ET` OR convert all values to PDT: `07:00 ET → 04:00 PDT`, `08:30 ET → 05:30 PDT`, `09:00 ET → 06:00 PDT`, `10:00 ET → 07:00 PDT`, `16:00 ET → 13:00 PDT`
- **Learned:** Even when conversion exists in adjacent columns, the primary time column must be consistent with its header.

### 🟢 MINOR-001: Oil futures decimal precision inconsistency

- **Location:** Section V.1 Crude Oil WTI table
- **Exact quote:** Jun 2026 shows `$90.56` (2 decimal) while Aug 2026 shows `$84.16` (2 decimal) — but the source data from MarketWatch shows `84.16` consistently
- **Problem:** Minor formatting inconsistency — some entries have different decimal precision
- **Fix:** Standardize to 2 decimal places for all oil futures prices
- **Learned:** When copying commodity prices, standardize decimal precision across the table

### 🟢 MINOR-002: Tail risk probabilities don't sum clearly

- **Location:** Section 3.3 Tail Risk / Binary Events
- **Exact quote:** Iran deal signed 40%, Iran deal fails 40%, NFP miss 30%, NFP strong 30%, Fed hawkish 20%, Geopolitical escalation 15%
- **Problem:** These are independent events (not mutually exclusive), so they don't need to sum to 100%. But it's not explicitly stated, which could confuse readers. The Iran deal scenarios (40% + 40% = 80%) also doesn't equal 100% — leaving 20% for "stall/no deal but not escalation". This is fine but should be clarified.
- **Fix:** Add a note: "Probabilities are independent events; they do not sum to 100%" or restructure Iran deal to show success 60% / stall 10% / escalation 30%
- **Learned:** When presenting independent event probabilities, explicitly state that they don't sum to 100%.

### 🟢 MINOR-003: NFP probability gap

- **Location:** Section 3.3 Tail Risk table + Section 7.1 Base Case
- **Exact quote:** NFP miss (<50K): 30%, NFP strong (>200K): 30% — but Base Case uses "NFP moderate (100-150K)"
- **Problem:** 30% miss + 30% strong = 60%, leaving 40% for "moderate" NFP. Not inherently wrong but the gap between <50K (30%) and 100-150K (implied 40%) creates an unexplained range 50-99K. Should account for 100%.
- **Fix:** Adjust probabilities to account for the full range: miss (<100K): 30%, moderate (100-200K): 40%, strong (>200K): 30%
- **Learned:** NFP probability distributions should cover the full range without gaps.

---

## Rules & Anti-Patterns Checked

| Rule | Status | Notes |
|------|--------|-------|
| RULE-001 (YTD verified) | ✅ PASS | No YTD claims for individual indices |
| RULE-002 (Live price timing) | ✅ PASS | Pre-market data appropriate for 6AM PDT |
| RULE-003 (ET→PDT conversion) | ✅ PASS | PDT values in "Chi tiết" column are correct |
| RULE-004 (Body times PDT) | ❌ FAIL | Timeline table header says PDT but uses ET values |
| RULE-005 (Anonymization) | ✅ PASS | No banned source names found |
| RULE-006 (Claim strength) | ✅ PASS | Claims supported by ≥3 data points |
| RULE-007 (Arithmetic) | ✅ PASS | Oil, gold, silver percentages verified |
| RULE-008 (Filename PDT) | ✅ PASS | Filename uses `6AM` matching 06:00 PDT trigger |
| RULE-009 (Weekend baseline) | ✅ PASS | 06/05 is Friday — correct baseline |
| RULE-010 (Symbol `$`) | ✅ PASS | No incorrect `$` prefix on indices |
| RULE-011 (Yield change units) | ✅ PASS | Uses `bps` for yield changes |
| RULE-012 (Weekday label) | ✅ PASS | Thursday 07/05/2026 is correct |
| RULE-013 (Global market holidays) | ✅ PASS | N/A — no global market quotes |
| RULE-014 (Overnight futures) | ✅ PASS | Pre-market futures section correct |
| RULE-015 (Body language) | ✅ PASS | Body is predominantly Vietnamese |

## Anti-Patterns Checked

| Pattern | Status | Notes |
|---------|--------|-------|
| AP-001 (Russell YTD) | ✅ PASS | No YTD spread derivation |
| AP-002 (Live price=open) | ✅ PASS | Pre-market data, not session trading |
| AP-003 (ET→PDT error) | ✅ PASS | PDT values correct in detail column |
| AP-004 (Filename ET) | ✅ PASS | Filename uses PDT trigger time |
| AP-005 (Arithmetic %) | ✅ PASS | No "from X to Y" percentage claims |
| CASE-024 (China macro) | ✅ PASS | N/A — not applicable to this report scope |
| CASE-025 (Energy inflation) | ✅ PASS | Oil price drop noted but no CPI component analysis (not expected in 6AM report) |
| CASE-026 (Housing cost) | ✅ PASS | N/A — not applicable |
| CASE-027 (Global macro) | ✅ PASS | N/A — report focuses on US markets |

---

## New Rules Proposed

**None.** This review didn't discover a pattern that requires a new rule. The Rule 004 violation is a one-off where the conversion was done in the detail column but not the primary column.

---

## Guidelines for AI Report Generator

1. **[CRITICAL] Timeline table times must match the column header.** If header says "Giờ PDT", all values must be in PDT — don't use ET in the time column even if the detail column has the correct PDT equivalent.
2. **[MINOR] Standardize decimal precision** across commodity tables — use 2 decimal places for oil futures prices.
3. **[MINOR] When presenting independent event probabilities**, explicitly note that they don't sum to 100%.
4. **[MINOR] NFP probability distribution should cover the full range** without gaps (miss/moderate/strong = 100%).

---

## Checklist for Next Report

- [ ] All body time values in PDT (not ET), unless explicitly labeled "ET"
- [ ] Table column headers match the time format of their values
- [ ] Commodity tables use consistent decimal precision
- [ ] Independent event probabilities explicitly noted as non-mutually-exclusive
- [ ] NFP probability: miss + moderate + strong = 100%

---

*Review completed by Apollo — AI Report Reviewer*
*Date: 2026-05-07*
