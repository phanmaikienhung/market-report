---
name: tcpw-daily-update
description: Kiểm tra bài mới trên tapchiphowall.com, tải PDF, chưng cất kiến thức, và tích hợp vào knowledge base (5h chiều mỗi ngày).
---

## Mục tiêu
Kiểm tra tapchiphowall.com có bài viết mới không. Nếu có, tải PDF, chưng cất kiến thức, và tích hợp vào knowledge base bằng Smart Merge Protocol.

## Skills cần dùng
1. **tcpw-update** (tại `.claude/skills/tcpw-update/SKILL.md`) — cho quy trình fetch + distill
2. **knowledge-distillation-agent** (tại `knowledge-distillation-agent/SKILL.md`) — cho Smart Merge Protocol (Bước 7)

Đọc cả hai SKILL.md trước khi bắt đầu để nắm rõ quy trình.

## Đường dẫn quan trọng
- **Knowledge Base:** `knowledge_base/knowledge_base_viet_hustler.md` (trong mounted folder PhanTichChungKhoan)
- **Distill files:** `kienthuc_raw/distill-MMDD-topic.md`
- **PDF output:** `kienthuc_raw/` (trên máy Windows: `C:\Users\Kien Hung\Documents\Claude\Projects\PhanTichChungKhoan\kienthuc_raw`)
- **Script tạo PDF:** `C:\Users\Kien Hung\PhanTichChungKhoan\knowledge-distillation-agent\scripts\tapchiphowall_pdf.py`
- **Python:** `C:\Users\Kien Hung\AppData\Local\Programs\Python\Python313\python.exe`

## Quy trình 5 bước

### Bước 1: Kiểm tra bài mới
Dùng Claude in Chrome navigate đến https://tapchiphowall.com. Đọc section "Bài Viết Mới Nhất". So sánh với danh sách PDF đã có trong `kienthuc_raw/` (dùng `list_directory` qua Desktop Commander). Xác định bài nào chưa có PDF.

Nếu không có bài mới → báo "Không có bài mới hôm nay" và dừng.

### Bước 2: Tải PDF
Chạy script tapchiphowall_pdf.py qua Desktop Commander để tải PDF cho từng bài mới. Xem chi tiết cách chạy trong tcpw-update SKILL.md (phần "Chạy script trên Windows").

Kiểm tra kết quả: PDF tốt = 7-26MB, có hình ảnh. Nếu < 3MB → session expired, cần báo user login lại.

### Bước 3: Đọc nội dung bài viết
Dùng Claude in Chrome navigate đến URL bài viết, gọi get_page_text để lấy toàn bộ nội dung text.

### Bước 4: Chưng cất kiến thức
Tạo file `kienthuc_raw/distill-MMDD-topic.md` theo cấu trúc trong tcpw-update SKILL.md (Bước 4). Giữ lại tất cả con số, data, bảng so sánh, chuỗi nhân quả.

### Bước 5: Smart Merge vào Knowledge Base
**KHÔNG dùng phương pháp append cũ.** Áp dụng Smart Merge Protocol từ knowledge-distillation-agent SKILL.md (Bước 7):

1. Phân tách distill thành Knowledge Units (KU)
2. Mỗi KU: grep KB tìm nội dung liên quan → phân loại:
   - A (Trùng lặp) → bỏ qua
   - B (Cập nhật dữ liệu) → sửa tại chỗ + timestamp
   - C (Kiến thức mới) → chèn vào đúng lĩnh vực trong PHẦN 2
   - D (Mâu thuẫn) → giữ cả hai + marker "⚡ Tiến hóa quan điểm"
3. Kiểm tra cross-links → bổ sung PHẦN 3 nếu cần
4. Cập nhật header version + changelog
5. Chạy checklist merge (không duplicate, đúng section, conflict markers)

## Kết quả mong đợi
- PDF mới trong `kienthuc_raw/`
- File distill trong `kienthuc_raw/distill-MMDD-topic.md`
- Knowledge base `knowledge_base/knowledge_base_viet_hustler.md` đã tích hợp kiến thức mới
- Báo cáo ngắn: N bài mới, M KU tích hợp, K bỏ qua (trùng), J conflict markers