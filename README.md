# Employee Task Scheduler
 
Hệ thống phân công công việc nhân viên theo tuần — đồ án môn Lập trình Python.
 
## Công nghệ sử dụng
- Python 3.10+
- Flask
- SQLite + SQLAlchemy (Flask-SQLAlchemy)
- HTML5, CSS3, Bootstrap 5, Bootstrap Icons
- Jinja2 Templates
## Cấu trúc dự án
```
employee_task_scheduler/
├── applist.py              # File chạy chính: models, routes, business logic
├── requirements.txt
├── README.md
├── .gitignore
├── LICENSE
├── templates/
│   ├── base.html           # Layout chung (sidebar + topbar, tích hợp Dark Theme CSS)
│   ├── dashboard.html      # Trang Dashboard
│   ├── employees.html      # Quản lý nhân viên (CRUD + tìm kiếm)
│   ├── tasks.html          # Quản lý công việc (CRUD + tìm kiếm)
│   ├── task_assign.html    # Phân công công việc (chọn NV, xem phân công gần đây, xóa phân công)
│   ├── lich_trinh.html     # Lịch làm việc theo tuần (dạng bảng grid)
│   ├── reports.html        # Báo cáo / thống kê
│   └── import_data.html    # Nhập dữ liệu từ Excel / CSV
└── static/
    ├── css/style.css
    ├── js/app.js
    └── img/logo.svg
```
 
## Cài đặt & chạy
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
python applist.py
```
Mở trình duyệt tại: **http://127.0.0.1:5000**
 
Cơ sở dữ liệu SQLite (`scheduler.db`) sẽ tự động được tạo và nạp dữ liệu mẫu
khi chạy ứng dụng lần đầu.
 
## Chức năng chính & Cập nhật mới
 
| Module | Mô tả |
|---|---|
| Dashboard | Thống kê tổng quan (tổng NV, tổng CV, tổng lịch, số NV làm việc hôm nay), panel phân công nhanh, xem trước lịch tuần. |
| Quản lý nhân viên | Thêm / Sửa / Xóa / Tìm kiếm — mã NV, họ tên, email, SĐT, bộ phận, chức vụ. |
| Quản lý công việc | Thêm / Sửa / Xóa / Tìm kiếm — mã CV, tên, mô tả, độ ưu tiên, thời lượng. |
| Phân công công việc | Chọn công việc, tự động gợi ý nhân viên sẵn sàng. Hỗ trợ xóa phân công trực tiếp (nút Thùng rác) trong danh sách phân công gần đây. |
| Lịch làm việc tuần | Xem dạng lưới (Thứ 2 → Thứ 7, theo ca) hoặc dạng danh sách. Chỉ hiển thị các công việc **đã được phân công** (công việc chưa giao hoặc bị hủy phân công sẽ tự động ẩn). Hỗ trợ hiển thị nhiều công việc cùng ca/ngày. |
| Nhập dữ liệu | Cho phép tải lên dữ liệu danh sách nhân viên / công việc từ file Excel/CSV. |
| Báo cáo | Thống kê khối lượng công việc theo từng nhân viên và theo bộ phận. |
 
## Các điểm cải tiến giao diện & logic (cập nhật mới)
- **Tối ưu hóa lịch trình:** Kết nối dữ liệu dạng INNER JOIN giữa bảng Task và Schedule, giúp tự động đồng bộ hiển thị — khi xóa hết nhân viên khỏi công việc, công việc đó sẽ tự động ẩn khỏi bảng Lịch trình.
- **Xử lý hiển thị đa công việc:** Một ô (Ngày / Ca) có thể hiển thị danh sách xếp chồng nhiều công việc cùng lúc, phân biệt theo màu độ ưu tiên (Khẩn cấp, Cao, Trung bình, Thấp).
- **Cải tiến UI Dark Mode:** Đồng bộ bộ màu chuẩn Dark Theme với độ tương phản cao, xử lý triệt để lỗi trùng màu nền/chữ bị tối ở các ô Input, Table, Label, Select Box giúp giao diện dễ nhìn và rõ nét hơn.
- **Xóa phân công linh hoạt:** Bổ sung nút thao tác xóa phân công nhầm ngay tại trang Phân công nhân viên.
## Quy tắc nghiệp vụ quan trọng
- Hệ thống hoạt động từ **Thứ Hai đến Thứ Bảy** (nghỉ Chủ Nhật).
- Mỗi ngày có 2 ca: **Sáng (07:30–11:30)** và **Chiều (13:00–17:00)**.
- Một nhân viên **không được phân công quá 1 công việc trong cùng 1 ca** — được ràng buộc ở tầng cơ sở dữ liệu (Unique Constraint) và kiểm tra ở tầng ứng dụng trước khi lưu.
## Ghi chú sử dụng AI hỗ trợ
Dự án có sử dụng AI (Gemini / Claude) hỗ trợ sinh khung mã nguồn ban đầu, tối ưu hóa CSS Dark Mode và nâng cấp logic lọc lịch trình theo dữ liệu thực tế. Nhóm/sinh viên sử dụng lại mã nguồn này cần:
- Đọc và hiểu toàn bộ logic trước khi nộp bài.
- Tự kiểm thử các chức năng, đặc biệt là kiểm tra trùng ca và xử lý xóa phân công.
- Ghi rõ trong báo cáo phần nào có AI hỗ trợ theo đúng quy định.
## Hướng phát triển (mở rộng)
- Đăng nhập & phân quyền (admin / trưởng bộ phận).
- Xuất lịch làm việc sang Excel / PDF.
- Kéo thả (Drag & Drop) lịch làm việc.
- Gửi thông báo qua email khi có phân công mới.
- Triển khai lên Render / Railway.