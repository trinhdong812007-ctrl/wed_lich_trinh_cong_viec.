# 📅 Employee Task Scheduler

> Hệ thống phân công công việc nhân viên theo tuần — đồ án môn Lập trình Python.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.x-black)
![SQLite](https://img.shields.io/badge/SQLite-DB-lightgrey)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📖 Giới thiệu

**Employee Task Scheduler** là ứng dụng web quản lý và phân công công việc cho nhân viên theo tuần, hỗ trợ xác thực người dùng, đăng ký tài khoản qua hệ thống Key kích hoạt dùng 1 lần, quản lý nhân viên/công việc, xem lịch làm việc dạng lưới, nhập dữ liệu từ Excel/CSV và xuất báo cáo thống kê.

## 🛠 Công nghệ sử dụng & Giấy phép bản quyền

Toàn bộ các thư viện và công nghệ được sử dụng trong dự án đều là **Mã nguồn mở (Open Source)**, hoàn toàn **MIỄN PHÍ** và không tốn phí bản quyền thương mại:

| Thành phần | Công nghệ / Thư viện | Giấy phép (License) |
|---|---|---|
| Ngôn ngữ | Python 3.10+ | PSF License |
| Backend Framework | Flask | BSD-3-Clause |
| Xác thực & Phân quyền | Flask-Login | MIT License |
| Cơ sở dữ liệu | SQLite + SQLAlchemy | Public Domain / MIT |
| Giao diện UI | HTML5, CSS3, Bootstrap 5, Bootstrap Icons | MIT License |
| Template Engine | Jinja2 | BSD-3-Clause |

## 📂 Cấu trúc dự án

```
wed_lich_trinh_cong_viec/
├── .git/                    # Thư mục quản lý phiên bản Git
├── .venv/                   # Môi trường ảo Python (Virtual Environment)
├── __pycache__/             # Thư mục chứa Bytecode đã biên dịch của Python
├── app.py                   # File chạy chính (entry point): khởi tạo & chạy ứng dụng
├── config.py                # Cấu hình hệ thống (Database, SECRET_KEY, ...)
├── generate_keys.py         # Script sinh mã Key kích hoạt
├── LICENSE                  # Giấy phép mã nguồn mở (MIT License)
├── Procfile                 # Cấu hình khởi chạy trên Render
├── README.md                # Tài liệu hướng dẫn & thông tin dự án
├── requirements.txt          # Danh sách thư viện Python phụ thuộc
├── employees_sample.xlsx     # File mẫu nhập danh sách nhân viên
├── tasks_sample.xlsx         # File mẫu nhập danh sách công việc
├── app/                     # Thư mục chứa mã nguồn chính
│   ├── __init__.py          # Khởi tạo Flask app (Application Factory), đăng ký Blueprints
│   ├── extensions.py        # db, login_manager và các hằng số nghiệp vụ
│   ├── models/              # Models ORM (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── user.py          # Model người dùng & Key kích hoạt
│   │   ├── employee.py      # Model nhân viên
│   │   ├── task.py          # Model công việc
│   │   ├── schedule.py      # Model phân công lịch làm việc
│   │   └── page.py          # Model trang động (CMS)
│   ├── routes/              # Routes (Flask Blueprints)
│   │   ├── __init__.py      # Đăng ký toàn bộ Blueprints
│   │   ├── auth.py          # Đăng nhập, đăng ký, đăng xuất, sinh Key
│   │   ├── dashboard.py     # Lịch làm việc tuần, báo cáo, API trạng thái
│   │   ├── employee.py      # Quản lý nhân viên
│   │   ├── task.py          # Quản lý & phân công công việc
│   │   └── schedule.py      # TKB tuần, nhập dữ liệu, tải template
│   ├── services/            # Xử lý nghiệp vụ (Business Logic)
│   │   ├── __init__.py
│   │   ├── validation.py    # Xác thực dữ liệu đầu vào
│   │   ├── helpers.py       # Hàm tiện ích (parse ngày, chuẩn hóa văn bản...)
│   │   ├── scheduling.py    # Logic phân công & kiểm tra trùng ca
│   │   └── schema.py        # Khởi tạo DB & nâng cấp schema cũ
│   ├── templates/           # Giao diện HTML (Jinja2)
│   │   ├── base.html        # Layout chung
│   │   ├── auth/            # Trang đăng nhập / đăng ký
│   │   ├── dashboard/       # Lịch trình, báo cáo, trang động
│   │   ├── employee/        # Quản lý nhân viên
│   │   ├── task/            # Công việc, phân công, lịch sử
│   │   └── schedule/        # TKB tuần, nhập dữ liệu
│   └── static/              # Tài nguyên tĩnh (CSS, JS, Images)
│       ├── css/             # style.css
│       ├── js/              # app.js
│       └── img/             # logo.svg
├── instance/               # Dữ liệu runtime (CSDL SQLite)
│   └── database.db          # Cơ sở dữ liệu SQLite chính của ứng dụng
├── migrations/             # Quản lý migration của DB (Flask-Migrate / Alembic)
└── tests/                   # Các kịch bản kiểm thử (Unit Tests)
```

## 🚀 Cài đặt & chạy cục bộ (Local)

```bash
# 1. Tạo môi trường ảo
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 2. Cài đặt thư viện
pip install -r requirements.txt

# 3. Chạy ứng dụng
python app.py
```

Mở trình duyệt tại: **http://127.0.0.1:5000**

Cơ sở dữ liệu SQLite (`instance/database.db`) cùng tài khoản Admin mặc định sẽ tự động được tạo và nạp dữ liệu mẫu khi chạy ứng dụng lần đầu.

### 🔑 Tài khoản đăng nhập mặc định

| Trường | Giá trị |
|---|---|
| Username | `admin` |
| Password | `admin123` |

> ⚠️ **Lưu ý bảo mật:** Hãy đổi mật khẩu mặc định ngay khi triển khai lên môi trường thực tế (production).

### 🗝️ Sinh Key kích hoạt (Local)

Ngoài route `/generate-keys-admin`, có thể sinh Key kích hoạt trực tiếp bằng script:

```bash
python generate_keys.py
```

### 🧪 Chạy kiểm thử (Tests)

Các kịch bản kiểm thử nằm trong thư mục `tests/`:

```bash
pytest tests/
```

## ✨ Chức năng chính & Cập nhật mới

| Module | Mô tả |
|---|---|
| **Đăng nhập & Xác thực** | Bảo vệ toàn bộ ứng dụng bằng Flask-Login. Tự động tạo tài khoản quản trị mặc định, quản lý phiên làm việc (Session) và hỗ trợ Đăng xuất. |
| **Đăng ký & Key kích hoạt** | Yêu cầu nhập Key kích hoạt dùng 1 lần (ActivationKey) để đăng ký tài khoản mới. Tránh việc tạo tài khoản bừa bãi. |
| **Tạo Key tự động cho Admin** | Tuyến đường `/generate-keys-admin` hỗ trợ sinh nhanh 5 Key kích hoạt ngẫu nhiên dạng `XXXX-XXXX-XXXX` lưu trực tiếp vào CSDL. |
| **Dashboard** | Thống kê tổng quan (tổng NV, tổng CV, tổng lịch, số NV làm việc hôm nay), panel phân công nhanh, xem trước lịch tuần. |
| **Quản lý nhân viên** | Thêm / Sửa / Xóa / Tìm kiếm — mã NV, họ tên, email, SĐT, bộ phận, chức vụ. |
| **Quản lý công việc** | Thêm / Sửa / Xóa / Tìm kiếm — mã CV, tên, mô tả, độ ưu tiên, thời lượng. |
| **Phân công công việc** | Chọn công việc, tự động gợi ý nhân viên sẵn sàng. Hỗ trợ xóa phân công trực tiếp (nút Thùng rác) trong danh sách phân công gần đây. |
| **Lịch làm việc tuần** | Xem dạng lưới (Thứ 2 → Thứ 7, theo ca) hoặc dạng danh sách. Chỉ hiển thị các công việc đã được phân công (công việc chưa giao hoặc bị hủy phân công sẽ tự động ẩn). Hỗ trợ hiển thị nhiều công việc cùng ca/ngày. |
| **Nhập dữ liệu** | Cho phép tải lên dữ liệu danh sách nhân viên / công việc từ file Excel/CSV. |
| **Báo cáo** | Thống kê khối lượng công việc theo từng nhân viên và theo bộ phận. |

## 🔧 Các điểm cải tiến giao diện & logic (cập nhật mới)

- **Hệ thống Key kích hoạt (Activation Key System):**
  - Tích hợp model `ActivationKey` trong CSDL với cờ `is_used` để quản lý trạng thái key.
  - Khi người dùng đăng ký tài khoản bằng Key hợp lệ, hệ thống tự động đổi `is_used = True` để ngăn tái sử dụng.
  - Hỗ trợ đường dẫn Admin `/generate-keys-admin` để tạo tự động hàng loạt Key mới.
- **Hệ thống Đăng nhập & Bảo mật:** Tích hợp Flask-Login giúp bảo mật các tuyến đường (routes), yêu cầu người dùng phải đăng nhập trước khi truy cập các chức năng chính.
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
   - **Start Command:** lấy từ `Procfile` có sẵn trong dự án (`web: gunicorn app:app`)
4. Để tạo Key kích hoạt trên Render, truy cập:
   ```
   https://<domain-render-cua-ban>/generate-keys-admin
   ```
   Sao chép Key được tạo ra để thực hiện đăng ký tài khoản trên môi trường Render.

## 🤖 Ghi chú sử dụng AI hỗ trợ

Dự án có sử dụng AI (Gemini / Claude) hỗ trợ sinh khung mã nguồn ban đầu, tối ưu hóa CSS Dark Mode, cài đặt logic xác thực người dùng, hệ thống Key kích hoạt và nâng cấp lọc lịch trình theo dữ liệu thực tế. Nhóm/sinh viên sử dụng lại mã nguồn này cần:

- Đọc và hiểu toàn bộ logic trước khi nộp bài.
- Tự kiểm thử các chức năng, đặc biệt là kiểm tra đăng nhập, tạo/kích hoạt Key, trùng ca và xử lý xóa phân công.
- Ghi rõ trong báo cáo phần nào có AI hỗ trợ theo đúng quy định.

## 🧭 Hướng phát triển (mở rộng)

- [ ] Phân quyền nâng cao (Admin / Trưởng bộ phận / Nhân viên).
- [ ] Trang quản trị dành riêng cho Admin để quản lý/xem danh sách Key kích hoạt đã tạo.
- [ ] Xuất lịch làm việc sang Excel / PDF.
- [ ] Kéo thả (Drag & Drop) trực tiếp trên lịch làm việc.
- [ ] Gửi thông báo tự động qua email khi có phân công mới.
- [ ] Chuyển đổi CSDL sang PostgreSQL để giữ dữ liệu bền vững khi re-deploy trên Render.

## 📄 License

Dự án được phát hành theo giấy phép [MIT License](./LICENSE).

## 👥 Đóng góp

Đây là đồ án học tập — mọi góp ý, pull request hoặc issue đều được hoan nghênh để cải thiện chất lượng mã nguồn.