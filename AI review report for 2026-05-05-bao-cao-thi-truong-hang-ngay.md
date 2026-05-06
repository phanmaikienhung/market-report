# AI Review Report for 2026-05-05-bao-cao-thi-truong-hang-ngay

- **Report URL:** https://phanmaikienhung.github.io/market-report/2026-05-05-bao-cao-thi-truong-hang-ngay.html
- **Report Date:** 2026-05-05
- **Review Date:** 2026-05-06
- **Reviewer:** AI Post-Deploy Reviewer (skill: review-deployed-report)
- **Verdict:** WARN

## Tổng Kết

Báo cáo full daily 05/05/2026 (Thứ Ba) có cấu trúc tốt, dữ liệu chỉ số chính được xác nhận đúng từ Google Finance (S&P 500, Dow, Russell 2000). Tuy nhiên có 3 lỗi MAJOR liên quan đến định dạng bond yields (vi phạm RULE-011), thứ tự ranking sector sai, và VIX calculation notation không rõ ràng. Không có source name leak. Không có CRITICAL nào.

- 🔴 Critical: 0
- 🟡 Major: 3
- 🟢 Minor: 2

## Chi Tiết Lỗi

### 🟡 MAJOR — Bond yields thay đổi ghi %, vi phạm RULE-011

- **Category:** 4.3 Arithmetic & Units — RULE-011
- **Rule:** RULE-011
- **Vị trí:** "10Y Treasury Yield 4.4160 −0.0300 −0.67%" và "30Y Treasury Yield 4.9840 −0.0410 −0.82%"
- **Vấn đề:** Yield change ghi "-0.67%" và "-0.82%" — nhưng yield đã là % rồi (4.4160%). Thay đổi tuyệt đối là -0.0300 percentage points (= -3.0bp). Việc ghi "-0.67%" gây nhầm lẫn giữa percentage change và percentage point change. Đây chính xác là vi phạm RULE-011.
- **Cách sửa:** Ghi: "10Y: 4.416% (-3.0bp)" hoặc "10Y: 4.416% (-0.030pp)". Không bao giờ dùng "%" cho yield change.
- **Học được:** Khi yield/rate đã là % → change phải ghi bp hoặc pp, không dùng %.

### 🟡 MAJOR — Sector ranking table không đúng thứ tự theo %

- **Category:** 4.6 Cross-Reference Consistency
- **Rule:** Không có rule cụ thể → đề xuất RULE mới
- **Vị trí:** Bảng Sector Performance: Rank 1=Industrials +1.66%, Rank 2=Technology +1.60%, Rank 3=Basic Materials +1.63%
- **Vấn đề:** Basic Materials (+1.63%) có % change cao hơn Technology (+1.60%) nhưng lại xếp ở rank 3 trong khi Technology rank 2. Thứ tự ranking không match với % change thực tế. Phải sắp xếp giảm dần: Industrials +1.66% → Basic Materials +1.63% → Technology +1.60%.
- **Cách sửa:** Sắp xếp sector theo % change giảm dần. Không tự gán rank 1,2,3 nếu không đúng thứ tự.
- **Học được:** Bảng ranking phải luôn sort descending theo giá trị thực tế, không phải hard-coded.

### 🟡 MAJOR — VIX notation gây hiểu nhầm về previous close

- **Category:** 4.2 Data Accuracy
- **Rule:** Không có rule cụ thể → đề xuất RULE mới
- **Vị trí:** "VIX: 17.38 (−0.88, −4.82%)"
- **Vấn đề:** Notation "17.38 (−0.88, −4.82%)" dễ đọc nhầm là: current=17.38, prev=17.38, change=-0.88. Nhưng thực tế prev close phải là ~18.26 (17.38 + 0.88). Tỷ lệ -4.82% = -0.88/18.26, không phải -0.88/17.38. Notation không rõ ràng cho người đọc biết prev close là bao nhiêu.
- **Cách sửa:** Ghi: "VIX: 17.38 (prev: 18.26, −0.88/−4.82%)" để rõ ràng.
- **Học được:** Khi ghi price + change + % → phải rõ current, prev, và change tính từ prev nào.

### 🟢 MINOR — Futures table: Russell 2000 (RTY) empty

- **Category:** 4.4 Format & Language
- **Vị trí:** Bảng FUTURES, dòng "Russell 2000 (RTY) — — — —"
- **Vấn đề:** Toàn bộ dòng RTY futures là dấu "—" (empty). Trong khi các futures khác có giá, RTY bị thiếu. Đây là gap data.
- **Cách sửa:** Nếu không có data → ghi "N/A" thay vì "—" và add note giải thích. Hoặc tìm giá real-time cho RTY futures.
- **Học được:** Không để row hoàn toàn empty trong bảng data. Dùng N/A có giải thích.

### 🟢 MINOR — Source attribution "VBLGoldFix analysis" không rõ nguồn

- **Category:** 4.5 Logic & Reasoning
- **Vị trí:** "Goldman Sachs và Deutsche Bank nâng mục tiêu giá dầu lên $120/barrel: 'Chúng tôi không loại trừ việc Mỹ hạn chế xuất khẩu dầu...' — VBLGoldFix analysis"
- **Vấn đề:** "VBLGoldFix" không phải là nguồn tin cậy được công nhận (khác với CNBC, Bloomberg, WSJ...). Có thể là blog cá nhân, newsletter, hoặc thậm chí AI hallucination. Attribution từ nguồn thứ cấp (VBLGoldFix) thay vì nguồn gốc (Goldman Sachs, Deutsche Bank).
- **Cách sửa:** Chỉ cite trực tiếp từ nguồn gốc (Goldman Sachs, DB Research) hoặc nguồn tin uy tín (Reuters, Bloomberg, CNBC). Không cite từ secondary/tertiary sources không rõ.
- **Học được:** Luôn cite trực tiếp từ nguồn gốc hoặc financial news uy tín. Không cite blog/newsletter không xác minh.

## Hướng Dẫn Cho AI Report-Generator

1. **LUÔN dùng basis points (bp) cho bond yield changes** — vì yield đã là % rồi, ghi thêm % sẽ gây nhầm lẫn giữa percentage point change và percentage change. Ví dụ đúng: "4.416% (-3.0bp)".

2. **LUÔN sort descending cho ranking tables** — trước khi gán rank 1,2,3 → verify rằng giá trị thực tế đúng thứ tự. Không hard-coded rank nếu không sort đúng.

3. **LUÔN rõ ràng khi ghi price + change notation** — khi ghi "17.38 (-0.88, -4.82%)" → đảm bảo người đọc biết prev close từ đâu. Tốt hơn: "17.38 (prev: 18.26, -0.88)".

4. **KHÔNG BAO GIỜ để row empty trong bảng data** — nếu không có giá trị → dùng "N/A" + note. Không dùng "—" vì không rõ nghĩa.

5. **LUÔN cite từ nguồn gốc** — không cite từ secondary/tertiary sources không uy tín (blog, newsletter, "VBLGoldFix analysis"). Chỉ dùng CNBC, Bloomberg, Reuters, WSJ, hoặc nguồn chính thức.

6. **KHI có geopolitical narrative → verify bằng ≥2 sources** — "ceasefire được duy trì" cần được xác nhận từ cả Reuters + Bloomberg hoặc CNBC + AP, không chỉ một nguồn duy nhất.

## Rules Mới Đề Xuất

### RULE-016 — Sector ranking table phải sort descending theo % change

- **Severity:** MAJOR
- **Detection:** Bảng sector ranking → extract all % values → verify descending order
- **Anti-pattern:** "Rank 1=Tech +1.60%, Rank 2=BasMat +1.63%" — không giảm dần
- **Fix template:** Sort sectors by % change descending before assigning rank numbers
- **Learned from:** 2026-05-05, bao_cao_thi_truong_hang_ngay (Basic Materials +1.63% > Technology +1.60% nhưng xếp thấp hơn)

### RULE-017 — VIX/price change notation phải rõ previous close

- **Severity:** MAJOR
- **Detection:** Pattern `(\d+\.?\d*)\s*[\(]([+-]\d+\.?\d*)\s*,\s*([+-]\d+\.?\d*%)[\)]` → compute expected prev = current + change, verify % = change / prev
- **Anti-pattern:** "VIX: 17.38 (−0.88, −4.82%)" — % tính từ 17.38 ≠ -4.82% (cần prev ≈ 18.26)
- **Fix template:** Format: "VIX: {current} (prev: {prev}, {change_abs} / {change_pct}%)"
- **Learned from:** 2026-05-05, bao_cao_thi_truong_hang_ngay

### RULE-018 — Futures table không được có row hoàn toàn empty

- **Severity:** MINOR
- **Detection:** Row futures có tất cả giá trị là "—" hoặc "N/A" → flag
- **Anti-pattern:** "Russell 2000 (RTY) — — — —"
- **Fix template:** Nếu không có data → ghi "N/A (không có pre-market data)" với note
- **Learned from:** 2026-05-05, bao_cao_thi_truong_hang_ngay

## Checklist Cho Lần Report Tiếp Theo

- [ ] **Compute** tất cả bond yield changes → convert sang basis points (bp) trước khi ghi vào report
- [ ] **Sort** descending tất cả ranking tables (sectors, indices performance, vv.) trước khi gán rank numbers
- [ ] **Verify** VIX notation: write "current (prev: X, change / pct%)" format
- [ ] **Check** futures table: ensure NO row has all empty values — fill or note N/A with explanation
- [ ] **Cite** directly from primary sources (CNBC, Bloomberg, Reuters) — never from secondary/tertiary sources
- [ ] **Cross-verify** geopolitical claims (ceasefire, trade deals) against ≥2 independent sources before narrative inclusion
- [ ] **Validate** all arithmetic: computed_delta vs stated_delta must match within 0.5pp tolerance
