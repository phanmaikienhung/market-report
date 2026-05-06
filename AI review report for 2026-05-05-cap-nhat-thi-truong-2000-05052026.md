# AI Review Report for 2026-05-05-cap-nhat-thi-truong-2000-05052026
- **Report URL:** https://phanmaikienhung.github.io/market-report/2026-05-05-cap-nhat-thi-truong-2000-05052026.html
- **Report Date:** 2026-05-05
- **Review Date:** 2026-05-05
- **Reviewer:** AI Post-Deploy Reviewer (skill: review-deployed-report)
- **Verdict:** WARN

## Tổng Kết
Report 8PM PDT Quick Update chất lượng cao — dữ liệu chính xác, format sạch, không có source name leak. 2 lỗi MAJOR về format yield/rate change (RULE-011) và thiếu PDT equivalent cho FOMC minutes. Không có lỗi CRITICAL. Overall: report tốt, cần fix minor format issues cho lần sau.
- 🔴 Critical: 0
- 🟡 Major: 2
- 🟢 Minor: 0

## Chi Tiết Lỗi

### 🟡 MAJOR — Yield/Rate change dùng % thay vì bp/pp (RULE-011)
- **Category:** 4.3 (Arithmetic & Units)
- **Rule:** RULE-011
- **Vị trí:** Table "Commodities, Yields & FX", dòng 10Y Treasury: `4.4160% -0.0300 -0.67%`
- **Vấn đề:** Yield change ghi `-0.67%` trong ngoặc đơn sau value `%`. Không rõ -0.67% là relative change (0.67% của 4.416%) hay absolute change (67bp). RULE-011 yêu cầu dùng bp/pp để tránh nhầm lẫn.
- **Cách sửa:** Format lại: `4.416% (-3.0bp)` thay vì `4.4160% -0.0300 -0.67%`. Tương tự cho 30Y: `4.984% (-4.1bp)`.
- **Học được:** Yield/rate phải ghi change theo bp (basis points) hoặc pp (percentage points), KHÔNG dùng `%` cho change. VIX không phải yield, dùng % được.

### 🟡 MAJOR — FOMC Minutes thiếu PDT equivalent trong body (RULE-004)
- **Category:** 4.7 (Time & Pipeline Compliance)
- **Rule:** RULE-004
- **Vị trí:** Section "Sự kiện sắp tới": `**Wednesday 05/06:** FOMC Minutes (2:00 PM EDT) — tín hiệu policy sau FOMC meeting, rất quan trọng`
- **Vấn đề:** Body section có thời gian ET (2:00 PM EDT) mà không có PDT equivalent trong ngoặc. Theo RULE-004, body times phải dùng PDT hoặc có cả PDT equivalent.
- **Cách sửa:** Format lại: `**Wednesday 05/06:** FOMC Minutes (2:00 PM EDT / 11:00 AM PDT) — tín hiệu policy sau FOMC meeting, rất quan trọng`. Hoặc chỉ dùng PDT: `**Wednesday 05/06:** FOMC Minutes (11:00 AM PDT) — ...`
- **Học được:** Khi ghi event times trong body section (Sự kiện sắp tới), luôn kèm cả PDT equivalent hoặc dùng thuần PDT. Lookup: 2:00 PM EDT = 11:00 AM PDT.

## Hướng Dẫn Cho AI Report-Generator

1. **LUÔN ghi yield/rate change theo bp** — vì `%` cho yield change gây nhầm lẫn magnitute (67bp vs 0.67% relative = khác biệt ~100x). Format đúng: `4.416% (-3.0bp)`.
2. **LUÔN kèm PDT equivalent cho tất cả event times trong body** — vì readers dùng PDT, không phải ET. Format: `2:00 PM EDT / 11:00 AM PDT`.
3. **KHÔNG BAO GIỜ dùng `%` cho yield change** — yield là percentage, change nên dùng bp/pp. VIX và stock % change dùng % được.
4. **KHI có multiple yield entries** — check từng dòng 10Y, 30Y, 2Y đều dùng bp/pp format.

## Rules Mới Đề Xuất
Không có rules mới cần đề xuất. RULE-011 và RULE-004 đã cover các pattern này.

## Checklist Cho Lần Report Tiếp Theo
- [ ] Verify tất cả yield/rate change format theo bp (không dùng %)
- [ ] Verify tất cả event times trong body có PDT equivalent
- [ ] Run grep cho banned source names (RULE-005)
- [ ] Recompute tất cả percentage changes từ raw numbers
- [ ] Verify filename hour matches PDT trigger time (RULE-008)
- [ ] Verify weekday label matches actual calendar date (RULE-012)
