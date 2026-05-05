# AI Review Report: 2026-05-05 Cap Nhật Thị Trường 0900

| Field | Value |
|-------|-------|
| **Report URL** | https://phanmaikienhung.github.io/market-report/2026-05-05-cap-nhat-thi-truong-0900-05052026.html |
| **Report Date** | 2026-05-05 |
| **Report Time** | 09:00 PDT (but generated at 15:15 PDT with closing data) |
| **Report Type** | Quick Update |
| **Filename** | quick_update_0900.md |
| **Verdict** | ⚠️ WARN |
| **Reviewed At** | 2026-05-05 22:20 UTC |

## Tổng Kết

Báo cáo cập nhật thị trường phiên 05/05/2026 với dữ liệu đóng cửa. Tổng thể chất lượng tốt, data chính xác cho phần lớn assets. Tuy nhiên có **vấn đề dữ liệu Russell 2000** cần được sửa — discrepancy giữa giá trị bảng (+0.49%) và narrative (+1.68% từ IWM).

| Severity | Count |
|----------|-------|
| 🔴 CRITICAL | 0 |
| 🟡 MAJOR | 1 |
| 🟢 MINOR | 2 |

## Chi Tiết Lỗi

### 🟡 MAJOR — Russell 2000 data discrepancy

- **Quote:** Bảng "Major Indices": `Russell 2000 | 2,853 | +13.89 | +0.49%`; Section "Biến động đáng chú ý": `IWM đạt 282.945 (52w high), +1.68%`
- **Vấn đề:** Russell 2000 trong bảng ghi +0.49% nhưng narrative ghi +1.68%. IWM (ETF tracking Russell 2000) từ 277.88 → 282.56 = **+1.68%**. Nếu Russell 2000 track IWM, giá trị đúng phải ~+1.43-1.68%, không phải +0.49%.
- **Cách sửa:** Tính lại Russell 2000 change từ IWM: `(282.56 - 277.88) / 277.88 * 100 = 1.68%`. Nếu baseline close 4/04 là 2,841.11 → prev close 3/04 ≈ 2,812.82 → change = +40.18 = **+1.43%**. Sửa table thành: `Russell 2000 | 2,853 | +40.18 | +1.43%` hoặc lấy data từ IWM.
- **Học được:** Khi không có Yahoo Finance symbol cho Russell 2000 index (^RTY không tồn tại), phải tính từ IWM ETF và giữ consistency giữa table và narrative.

### 🟢 MINOR — DXY estimated, không có direct data

- **Quote:** `DXY (tính từ USD/CAD) | ~110.5 | — | —`
- **Vấn đề:** DXY không có giá trị chính xác từ Yahoo Finance (symbol ^DXY không có data trong daily chart). Dùng USD/CAD (1.362) để suy ra ~110.5 nhưng không có % change.
- **Cách sửa:** Hoặc tìm DXY từ source khác (Bloomberg, Investing.com), hoặc ghi rõ "DXY ≈ 110.5 (estimated từ USD/CAD = 1.362)".
- **Học được:** Có thể thử symbol `DX-Y.NYB` (ICE DXY futures) hoặc `UUP` (US Dollar Index Bullish Fund) làm proxy thay thế.

### 🟢 MINOR — Russell 2000 giá trị ghi thiếu decimal

- **Quote:** `Russell 2000 | 2,853 | +13.89 | +0.49%`
- **Vấn đề:** Các indices khác có 2 decimal places (7,259.22 / 25,326.13), nhưng Russell 2000 chỉ có 0 decimal (2,853). Inconsistent formatting.
- **Cách sửa:** Ghi `2,853.00` hoặc lấy chính xác từ IWM conversion.
- **Học được:** Giữ consistent decimal places cho tất cả indices trong cùng bảng.

## Rules & Patterns Checked

| Rule/Pattern | Status | Notes |
|-------------|--------|-------|
| RULE-001 YTD verify | ✅ PASS | Không có claim YTD% nào trong báo cáo |
| RULE-002 Live price timing | ✅ PASS | Ghi rõ "closing data" do report chạy late |
| RULE-003 ET→PDT conversion | ✅ PASS | Không có ET time trong body |
| RULE-004 Body times PDT | ✅ PASS | Chỉ có PDT times |
| RULE-005 Source name leak | ✅ PASS | Không tìm thấy banned names |
| RULE-006 Claim strength | ⚠️ NOTE | Russell "breakout tiếp diễn" với data inconsistency |
| RULE-007 Arithmetic | ✅ PASS | Tái tính các % change đều khớp (trừ Russell discrepancy) |
| RULE-008 Filename PDT | ✅ PASS | `0900` match PDT trigger time |
| RULE-009 Weekend baseline | ✅ PASS | Monday, baseline là Friday 4/04 |
| RULE-010 Index $prefix | ⚠️ NOTE | Russell 2000 không có $ trong table ✅, nhưng "IWM đạt 282.945" không có $ cho ETF (correct for ETF) |
| RULE-011 Yield % change | ✅ PASS | Không có 10Y yield với % change |
| RULE-012 Weekday label | ✅ PASS | 05/05/2026 = Tuesday (Thứ Ba) ✅ |
| RULE-013 Global market calendar | ✅ PASS | Không có global market quotes |
| RULE-014 Overnight futures | ✅ PASS | Không có overnight futures section |
| RULE-015 Body language | ✅ PASS | 100% Vietnamese |
| AP-001 Russell YTD | ✅ PASS | Không có YTD claim |
| AP-002 Live price | ✅ PASS | Ghi rõ closing data |
| AP-003 ET→PDT | ✅ PASS | Không có ET times |
| AP-004 Filename ET | ✅ PASS | 0900 = PDT |
| AP-005 Arithmetic | ✅ PASS | Percentages verified |

## Hướng dẫn cho AI report-generator

1. **Khi không có Yahoo Finance symbol cho Russell 2000 index**, dùng IWM ETF data: tính % change từ IWM và apply cho Russell 2000. Giữ consistency: nếu narrative ghi +1.68% từ IWM, table cũng phải ghi +1.68% (hoặc ±1.0-1.5% nếu Russell 2000 có tracking error nhỏ).
2. **DXY proxy**: nếu `^DXY` không có data, dùng `DX-Y.NYB` (ICE DXY futures) hoặc `UUP` làm proxy. Ghi chú rõ khi dùng estimated.
3. **Decimal consistency**: giữ 2 decimal places cho tất cả indices trong cùng bảng (ngay cả khi giá trị tròn).

## Rules mới đề xuất

**Không có rules mới** — các issues phát hiện đã nằm trong existing rules (RULE-007, RULE-010).

## Checklist cho lần report tiếp theo

- [ ] Verify Russell 2000 từ IWM: `(today_IWM - prev_IWM) / prev_IWM * 100`
- [ ] DXY: thử `DX-Y.NYB` trước, fallback `UUP` hoặc ghi "estimated"
- [ ] Giữ decimal consistency: 2 decimal cho tất cả indices
- [ ] Table change % phải khớp narrative % — không được khác biệt

---
*Review completed at 2026-05-05 22:20 UTC | Reviewer: Apollo (post-deploy automated)*
