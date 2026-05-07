# AI Review Report for 2026-05-07-cap-nhat-thi-truong-1130-07052026
- **Report URL:** https://phanmaikienhung.github.io/market-report/2026-05-07-cap-nhat-thi-truong-1130-07052026.html
- **Report Date:** 2026-05-07
- **Review Date:** 2026-05-07
- **Reviewer:** AI Post-Deploy Reviewer (skill: review-deployed-report)
- **Verdict:** ⚠️ WARN

## Tổng Kết
Báo cáo Quick Update 11:30 chất lượng tốt — data accuracy cao, logic mạch lạc, định dạng tiếng Việt chuẩn, không có source name leak. Các vấn đề phát hiện đều thuộc dạng **formatting inconsistencies** trong bảng Treasuries và FX: double-plus notation, sai `$` prefix, và tính toán phần trăm thay đổi của 30Y Yield không khớp với điểm thay đổi. Không có lỗi dữ liệu hay logic nghiêm trọng.

- 🔴 Critical: 0
- 🟡 Major: 3
- 🟢 Minor: 0

## Chi Tiết Lỗi

### 🟡 MAJOR — 10Y Yield change column: double-plus notation (++)

- **Category:** 4.3 (Arithmetic & Units)
- **Rule:** RULE-007 (format consistency), FORMAT-001 (convention)
- **Vị trí:** Bảng "Treasuries" — hàng 10Y Yield: `++0.032`, `++0.73%`
- **Vấn đề:** Change column dùng `++` thay vì `+`. Đây là double-plus notation — có thể gây nhầm lẫn là "tăng gấp đôi" hoặc lỗi rendering. Quy ước báo cáo sử dụng `+`/`-` (xem Indices và Commodities columns).
- **Cách sửa:** Thay `++0.032` → `+0.032` và `++0.73%` → `+0.73%` (hoặc format đúng basis points như `+3.2bp`).
- **Học được:** Change column PHẢI dùng ký hiệu đơn `+`/`-`. Không dùng `++` hoặc `--`.

### 🟡 MAJOR — 30Y Yield change value và percentage không khớp toán học

- **Category:** 4.3 (Arithmetic & Units)
- **Rule:** RULE-007 (arithmetic verified)
- **Vị trí:** Bảng "Treasuries" — hàng 30Y Yield: `+0.026`, `+0.53%`
- **Vấn đề:** 
  - Change column hiển thị `+0.026` (thiếu `$` sign — xem lỗi MAJOR bên dưới)
  - Nhưng nếu 30Y yield trước đó ~4.9440 và hiện tại 4.9690, thì change thực tế là `+0.025`, không phải `+0.026`
  - Percentage: nếu change là +0.025, thì `(0.025 / 4.9690) * 100 = 0.503%` ≈ `0.50%`, không phải `0.53%`. Nếu change là +0.026, thì `(0.026 / 4.9690) * 100 = 0.523%` ≈ `0.52%`, vẫn không khớp `0.53%`
  - Không có cặp giá trị (change, %) nào khớp chính xác → inconsistency nội tại
- **Cách sửa:** Verify 30Y yield trước đó từ 6AM baseline hoặc live source. Recompute: `(4.9690 - 4.9440) / 4.9440 * 100 = 0.506%`. Ghi chính xác change = +0.025, % = +0.51%.
- **Học được:** Khi ghi yield change, compute BOTH change và % từ cùng base value. Đảm bảo `(change / base) * 100 = stated %`.

### 🟡 MAJOR — FX table: inconsistent `$` sign convention

- **Category:** 4.4 (Format & Language)
- **Rule:** FORMAT-002 (convention consistency)
- **Vị trí:** Bảng "FX" — ba hàng EUR/USD, GBP/USD, USD/JPY
- **Vấn đề:** 
  - EUR/USD: `~0.0000` (không có `$`) — đúng vì đây là rate, change là pip/point
  - GBP/USD: `-$0.001` (có `$`) — sai vì change trong forex là điểm/pip, không phải USD
  - USD/JPY: `+$0.406` (có `$`) — sai tương tự
  - Inconsistency: GBP/USD dùng `-$0.001` (có `$`) trong khi EUR/USD dùng `~0.0000` (không `$`). Cả ba đều là FX rates → quy ước phải giống nhau.
  - Ngoài ra, USD/JPY có `+` sign trong khi EUR/USD có `~` — mixing conventions
- **Cách sửa:** Tiêu chuẩn hóa FX change column: không dùng `$`. Dùng `+`/`-` cho change points, ví dụ: `EUR/USD: +0.0000`, `GBP/USD: -0.001`, `USD/JPY: +0.406`.
- **Học được:** FX rates change column KHÔNG dùng `$` sign — change là điểm/pip, không phải USD amount.

## Hướng Dẫn Cho AI Report-Generator

1. **LUÔN dùng `+`/`-` đơn cho change column, KHÔNG dùng `++`/`--`** — vì `++` dễ gây hiểu nhầm là "gấp đôi" hoặc lỗi formatting, không phải quy ước báo cáo chuẩn.

2. **KHI ghi yield/bond data** thì phải verify change và percentage từ cùng base value — không được ghi hai số không khớp nhau toán học. Recompute `(new - old) / old * 100` và check match.

3. **FX rates change column KHÔNG dùng `$` sign** — vì change là point/pip difference, không phải USD amount. Dùng `+`/`-` plain number (hoặc `+0.001` format). Chỉ dùng `$` cho assets priced in USD (Gold, Oil, BTC, stock prices).

4. **KHI dùng `~` cho near-zero values** thì phải nhất quán across table — không mix `~0.0000` với `+$0.406` trong cùng column.

## Rules Mới Đề Xuất
Không có rule mới đề xuất — các issue phát hiện đều thuộc pattern formatting đã biết.

## Checklist Cho Lần Report Tiếp Theo
- [ ] Verify tất cả change % từ `(new - old) / old * 100` cho Treasuries, trước khi ghi
- [ ] FX table: change column dùng `+`/`-` plain number, KHÔNG `$`
- [ ] Change column: dùng `+`/`-` đơn (không `++`/`--`)
- [ ] Inconsistent sign conventions trong cùng table → chuẩn hóa
- [ ] Sau khi viết markdown, render preview và kiểm tra formatting (bảng align, sign convention)
