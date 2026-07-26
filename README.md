# 📅 Employee Task Scheduler
 
> Hệ thống phân công công việc nhân viên theo tuần — đồ án môn Lập trình Python.
 
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.x-black)
![SQLite](https://img.shields.io/badge/SQLite-DB-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)
 
---
 
## 📖 Giới thiệu
 
**Employee Task Scheduler** là ứng dụng web quản lý và phân công công việc cho nhân viên theo tuần, hỗ trợ xác thực người dùng, quản lý nhân viên/công việc, xem lịch làm việc dạng lưới, nhập dữ liệu từ Excel/CSV và xuất báo cáo thống kê. Dự án phù hợp làm đồ án môn Lập trình Python với Flask.
 
## 🛠 Công nghệ sử dụng
 
| Thành phần | Công nghệ |
|---|---|
| Ngôn ngữ | Python 3.10+ |
| Backend Framework | Flask |
| Xác thực & Phân quyền | Flask-Login |
| Cơ sở dữ liệu | SQLite + SQLAlchemy (Flask-SQLAlchemy) |
| Giao diện | HTML5, CSS3, Bootstrap 5, Bootstrap Icons |
| Template Engine | Jinja2 |
 
## 📂 Cấu trúc dự án
 
```
employee_task_scheduler/
├── applist.py              # File chạy chính: models, routes, logic xác thực & phân công
├── requirements.txt
├── README.md
├── .gitignore
├── LICENSE
├── templates/
│   ├── base.html           # Layout chung (sidebar + topbar, tích hợp Dark Theme CSS)
│   ├── login.html          # Trang đăng nhập hệ thống
│   ├── dashboard.html      # Trang Dashboard
│   ├── employees.html      # Quản lý nhân viên (CRUD + tìm kiếm)
│   ├── tasks.html          # Quản lý công việc (CRUD + tìm kiếm)
│   ├── task_assign.html    # Phân công công việc (chọn NV, xem phân công gần đây, xóa phân công)
│   ├── lich_trinh.html     # Lịch làm việc theo tuần (dạng bảng grid, tự động căn chỉnh)
│   ├── reports.html        # Báo cáo / thống kê
│   └── import_data.html    # Nhập dữ liệu từ Excel / CSV
└── static/
    ├── css/style.css
    ├── js/app.js
    └── img/logo.svg
```
 
## 🚀 Cài đặt & chạy cục bộ (Local)
 
```bash
# 1. Tạo môi trường ảo
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
 
# 2. Cài đặt thư viện
pip install -r requirements.txt
 
# 3. Chạy ứng dụng
python applist.py
```
 
Mở trình duyệt tại: **http://127.0.0.1:5000**
 
Cơ sở dữ liệu SQLite (`scheduler.db`) cùng tài khoản Admin mặc định sẽ tự động được tạo và nạp dữ liệu mẫu khi chạy ứng dụng lần đầu.
 
### 🔑 Tài khoản đăng nhập mặc định
 
| Trường | Giá trị |
|---|---|
| Username | `admin` |
| Password | `admin123` |
 
> ⚠️ **Lưu ý bảo mật:** Hãy đổi mật khẩu mặc định ngay khi triển khai lên môi trường thực tế (production).
 
## ✨ Chức năng chính & Cập nhật mới
 
| Module | Mô tả |
|---|---|
| **Đăng nhập & Xác thực** | Bảo vệ toàn bộ ứng dụng bằng Flask-Login. Tự động tạo tài khoản quản trị mặc định, quản lý phiên làm việc (Session) và hỗ trợ Đăng xuất. |
| **Dashboard** | Thống kê tổng quan (tổng NV, tổng CV, tổng lịch, số NV làm việc hôm nay), panel phân công nhanh, xem trước lịch tuần. |
| **Quản lý nhân viên** | Thêm / Sửa / Xóa / Tìm kiếm — mã NV, họ tên, email, SĐT, bộ phận, chức vụ. |
| **Quản lý công việc** | Thêm / Sửa / Xóa / Tìm kiếm — mã CV, tên, mô tả, độ ưu tiên, thời lượng. |
| **Phân công công việc** | Chọn công việc, tự động gợi ý nhân viên sẵn sàng. Hỗ trợ xóa phân công trực tiếp (nút Thùng rác) trong danh sách phân công gần đây. |
| **Lịch làm việc tuần** | Xem dạng lưới (Thứ 2 → Thứ 7, theo ca) hoặc dạng danh sách. Chỉ hiển thị các công việc đã được phân công (công việc chưa giao hoặc bị hủy phân công sẽ tự động ẩn). Hỗ trợ hiển thị nhiều công việc cùng ca/ngày. |
| **Nhập dữ liệu** | Cho phép tải lên dữ liệu danh sách nhân viên / công việc từ file Excel/CSV. |
| **Báo cáo** | Thống kê khối lượng công việc theo từng nhân viên và theo bộ phận. |
 
## 🔧 Các điểm cải tiến giao diện & logic (cập nhật mới)
 
- **Hệ thống Đăng nhập (Authentication):** Tích hợp Flask-Login giúp bảo mật các tuyến đường (routes), yêu cầu người dùng phải đăng nhập trước khi truy cập hệ thống.
- **Tối ưu hóa lịch trình & Giao diện:**
  - Kết nối dữ liệu dạng INNER JOIN giữa bảng Task và Schedule, giúp tự động đồng bộ hiển thị — khi xóa hết nhân viên khỏi công việc, công việc đó sẽ tự động ẩn khỏi bảng Lịch trình.
  - Tự động căn chỉnh chiều cao các ô lịch trình, cải tiến hiển thị danh sách xếp chồng nhiều công việc cùng ca/ngày, phân biệt theo màu độ ưu tiên.
- **Cải tiến UI Dark Mode:** Đồng bộ bộ màu chuẩn Dark Theme với độ tương phản cao, xử lý triệt để lỗi trùng màu nền/chữ bị tối ở các ô Input, Table, Label, Select Box giúp giao diện dễ nhìn và rõ nét hơn.
- **Sẵn sàng Cloud Deploy:** Chuẩn hóa mã nguồn và cấu hình thư viện để sẵn sàng triển khai thực tế trên Render (Web Service).
## 📌 Quy tắc nghiệp vụ quan trọng
 
- Hệ thống hoạt động từ **Thứ Hai đến Thứ Bảy** (nghỉ Chủ Nhật).
- Mỗi ngày có 2 ca: **Sáng (07:30–11:30)** và **Chiều (13:00–17:00)**.
- Một nhân viên **không được phân công quá 1 công việc trong cùng 1 ca** — được ràng buộc ở tầng cơ sở dữ liệu (Unique Constraint) và kiểm tra ở tầng ứng dụng trước khi lưu.
## ☁️ Triển khai lên Render (Cloud Deploy)
 
1. Đẩy mã nguồn lên GitHub repository.
2. Trên [Render](https://render.com), tạo mới **Web Service** và liên kết với repository.
3. Cấu hình:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn applist:app`
4. Thêm biến môi trường (nếu cần, ví dụ `SECRET_KEY`).
5. Deploy và truy cập theo domain do Render cung cấp.
> Gợi ý: thêm `gunicorn` vào `requirements.txt` nếu chưa có, vì `python applist.py` chỉ phù hợp cho môi trường local (dev server).
 
## 🤖 Ghi chú sử dụng AI hỗ trợ
 
Dự án có sử dụng AI (Gemini / Claude) hỗ trợ sinh khung mã nguồn ban đầu, tối ưu hóa CSS Dark Mode, cài đặt logic xác thực người dùng và nâng cấp lọc lịch trình theo dữ liệu thực tế. Nhóm/sinh viên sử dụng lại mã nguồn này cần:
 
- Đọc và hiểu toàn bộ logic trước khi nộp bài.
- Tự kiểm thử các chức năng, đặc biệt là kiểm tra đăng nhập, trùng ca và xử lý xóa phân công.
- Ghi rõ trong báo cáo phần nào có AI hỗ trợ theo đúng quy định.
## 🧭 Hướng phát triển (mở rộng)
 
- [ ] Phân quyền nâng cao (Admin / Trưởng bộ phận / Nhân viên).
- [ ] Xuất lịch làm việc sang Excel / PDF.
- [ ] Kéo thả (Drag & Drop) trực tiếp trên lịch làm việc.
- [ ] Gửi thông báo tự động qua email khi có phân công mới.
- [ ] Thêm API RESTful cho tích hợp bên ngoài.
- [ ] Viết unit test cho các nghiệp vụ trùng ca / xóa phân công.
## 📄 License
 
Dự án được phát hành theo giấy phép [MIT License](./LICENSE).
 
## 👥 Đóng góp
 
Đây là đồ án học tập — mọi góp ý, pull request hoặc issue đều được hoan nghênh để cải thiện chất lượng mã nguồn.