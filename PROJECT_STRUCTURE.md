# 📦 Tóm tắt Cấu trúc Dự án — Employee Task Scheduler

> Tài liệu tổng quan toàn bộ cấu trúc thư mục, mã nguồn và luồng hoạt động của ứng dụng **EmployeeTaskScheduler** (Hệ thống phân công công việc nhân viên theo tuần).

---

## 1. Giới thiệu chung

| Thông tin | Chi tiết |
|---|---|
| **Tên dự án** | Employee Task Scheduler |
| **Ngôn ngữ** | Python 3.10+ |
| **Framework** | Flask 3.x |
| **ORM** | SQLAlchemy + Flask-SQLAlchemy |
| **Xác thực** | Flask-Login (Session) |
| **Migration DB** | Flask-Migrate (Alembic) |
| **CSDL** | SQLite (tệp `instance/database.db`) |
| **Template** | Jinja2 + Bootstrap 5 |
| **Nhập liệu** | Excel (openpyxl) / CSV |

Ứng dụng quản lý nhân viên, công việc và phân công lịch làm việc theo tuần; hỗ trợ đăng ký tài khoản bằng Key kích hoạt dùng 1 lần, xem lịch dạng lưới, gợi ý phân công tự động (AI), nhập dữ liệu từ Excel/CSV và xuất báo cáo thống kê.

---

## 2. Cây thư mục tổng quan

```
WED_LICH_TRINH_CONG_VIEC/                    🌍 THƯ MỤC GỐC
│
│  ┌──────────────────────────────────────────────────────────────┐
│  │                     FILE CẤU HÌNH & CHẠY                     │
│  ├──────────────────────────────────────────────────────────────┤
├─ app.py  ──────────► Entry point · gunicorn trỏ `app:app`
├─ config.py ────────► Cấu hình hệ thống (SECRET_KEY, DB URI)
├─ requirements.txt ─► Khai báo thư viện Python
├─ Procfile ─────────► `web: gunicorn app:app` (Render)
├─ generate_keys.py ─► Script sinh Key kích hoạt
├─ employees_sample.xlsx · tasks_sample.xlsx → File mẫu nhập liệu
├─ README.md · LICENSE · PROJECT_STRUCTURE.md
│
│  ┌──────────────────────────────────────────────────────────────┐
│  │                     MÃ NGUỒN CHÍNH (app/)                    │
│  ├──────────────────────────────────────────────────────────────┤
├─ app/ ◀─────────────────────────────── Flask Application Package
│  │
│  ├─ __init__.py ──► create_app() · Application Factory
│  │                  (khởi tạo Flask, Blueprints, DB, admin)
│  ├─ extensions.py ► db · login_manager · hằng số nghiệp vụ
│  │
│  ├─ models/ ──────► ORM — SQLAlchemy (BẢNG CSDL)
│  │  │
│  │  ├─ user.py ──────► User, ActivationKey       (tài khoản & Key)
│  │  ├─ employee.py ──► Employee                  (nhân viên)
│  │  ├─ task.py ──────► Task                      (công việc)
│  │  ├─ schedule.py ──► Schedule, WeekSchedule    (phân công & TKB)
│  │  ├─ tkbfile.py ───► TKBFile                   (file TKB đang áp dụng)
│  │  └─ page.py ──────► Page                      (trang động)
│  │
│  ├─ routes/ ──────► BLUEPRINTS — ĐIỀU HƯỚNG URL
│  │  │
│  │  ├─ auth.py ──────►  /login · /register · /logout · /generate-keys-admin
│  │  ├─ dashboard.py ─►  /lich-trinh · /reports · /api/last-update ...
│  │  ├─ employee.py ──►  /employees · /employees/add|edit|delete
│  │  ├─ task.py ──────►  /tasks · /tasks/assign · /tasks/history · API ...
│  │  └─ schedule.py ──►  /upload-schedule · /import-data · /tkb-file/download ...
│  │
│  ├─ services/ ────► BUSINESS LOGIC (xử lý nghiệp vụ)
│  │  │
│  │  ├─ validation.py ►  xác thực dữ liệu nhân viên / công việc
│  │  ├─ helpers.py ───►  hàm tiện ích (parse ngày, chuẩn hóa text...)
│  │  ├─ scheduling.py ►  phân công AI, kiểm tra trùng ca, giới hạn số NV
│  │  └─ schema.py ────►  khởi tạo DB, nâng cấp schema cũ, seed admin
│  │
│  ├─ templates/ ────► GIAO DIỆN HTML (Jinja2)
│  │  │
│  │  ├─ base.html ────► layout khung chung (sidebar, topbar)
│  │  ├─ auth/ ────────► login.html · register.html
│  │  ├─ dashboard/ ───► lich_trinh.html · reports.html · dynamic_page.html
│  │  ├─ employee/ ────► employees.html
│  │  ├─ task/ ────────► tasks.html · task_assign.html · task_history.html
│  │  └─ schedule/ ────► upload_schedule.html · import_data.html
│  │
│  └─ static/ ──────► TÀI NGUYÊN TĨNH
│     ├─ css/style.css · js/app.js · img/logo.svg
│
├─ instance/ ◀─────── DỮ LIỆU RUNTIME (không commit lên git)
│  └─ database.db ───► CSDL SQLite chính
│
├─ migrations/ ◀───── FLASK-MIGRATE / ALEMBIC
│  └─ versions/
│     ├─ 5d29e689df70_baseline_schema.py   ► schema gốc
│     └─ 1536ab89a18f_add_tkbfile.py       ► bảng tkb_file
│
└─ tests/ ◀───────── KIỂM THỬ (pytest)
   └─ test_validation.py ► test xác thực dữ liệu
```

**Ghi chú đọc sơ đồ:** `─►` = trỏ tới chức năng/mô tả · `app/` là package trung tâm gồm 4 tầng: **Models → Routes → Services → Templates**.

---

## 3. Chi tiết từng thành phần

### 3.1. Các tệp ở thư mục gốc

| Tệp | Vai trò |
|---|---|
| `app.py` | Entry point duy nhất. Gọi `create_app()` từ package `app` và chạy server (debug). Gunicorn trỏ tới `app:app`. |
| `config.py` | Lớp `Config` chứa `SECRET_KEY`, `SQLALCHEMY_DATABASE_URI` (trỏ `instance/database.db`), `SQLALCHEMY_TRACK_MODIFICATIONS`. Hỗ trợ `DevelopmentConfig` / `ProductionConfig`. |
| `requirements.txt` | Khai báo: Flask, Flask-SQLAlchemy, SQLAlchemy, Flask-Login, Flask-Migrate, Werkzeug, gunicorn, openpyxl. |
| `Procfile` | `web: gunicorn app:app` — dùng khi triển khai lên Render. |
| `generate_keys.py` | Script CLI sinh `n` Key kích hoạt ngẫu nhiên dạng `XXXX-XXXX-XXXX`, lưu vào bảng `activation_keys`. |
| `employees_sample.xlsx`, `tasks_sample.xlsx` | File mẫu dùng cho chức năng tải template & nhập dữ liệu. |

### 3.2. Package `app/`

#### `app/__init__.py` — Application Factory
- Hàm `create_app(config_class=Config)`:
  1. Tạo đối tượng `Flask` với `instance_relative_config=True`.
  2. Nạp cấu hình, tạo thư mục `instance/` nếu chưa có.
  3. Khởi tạo `db.init_app(app)`, `login_manager.init_app(app)`, `Migrate(app, db)`.
  4. Đăng ký toàn bộ Blueprints qua `register_blueprints(app)`.
  5. Đăng ký `user_loader` cho Flask-Login.
  6. Trong `app_context`: gọi `init_db()` (tạo bảng + nâng cấp schema cũ) và `seed_admin()` (tạo tài khoản `admin/admin123` nếu chưa có).

#### `app/extensions.py` — Đối tượng dùng chung
| Thành phần | Mô tả |
|---|---|
| `db` | Instance `SQLAlchemy()` dùng chung cho mọi model/service. |
| `login_manager` | Instance `LoginManager()`, `login_view = "auth.login"`, kèm thông báo mặc định. |
| `CA_LAM_VIEC` | Giờ từng ca: `{"Sáng": "07:30 - 11:30", "Chiều": "13:00 - 17:00"}`. |
| `THU_TRONG_TUAN` | Danh sách thứ trong tuần (Thứ 2 → Chủ nhật). |
| `DO_UU_TIEN_LIST` | Các mức độ ưu tiên: Thấp, Trung bình, Cao, Khẩn cấp. |
| `TRINH_DO_LIST` | Trình độ: Cơ bản, Khá, Thành thạo, Chuyên gia. |
| `VI_TRI_MAP` | Bản đồ bộ phận → danh sách vị trí/chức danh. |
| `DO_UU_TIEN_COLORS`, `DO_UU_TIEN_BG` | Màu chữ / nền theo độ ưu tiên (dùng cho lịch). |
| `TRINH_DO_ORDER` | Thứ tự xếp hạng trình độ. |

### 3.3. Models (`app/models/`)

| Model | Bảng | Các trường chính |
|---|---|---|
| `User` | `users` | `id`, `username`, `password_hash`; phương thức `set_password`, `check_password`. |
| `ActivationKey` | `activation_keys` | `id`, `key` (unique), `is_used`, `created_at`. |
| `Employee` | `employee` | `id`, `ma_nv` (unique), `ho_ten`, `email`, `bo_phan`, `vi_tri`, `trinh_do`, `created_at`, `created_by_id`, `updated_by_id`; quan hệ `schedules`. |
| `Task` | `task` | `id`, `ma_cv` (unique), `ten_cv`, `ghi_chu`, `do_uu_tien`, `ngay_gio`, `bo_phan`, `so_luong_nv`, `thoi_luong`, `ca_requirement`, `completed`, `completed_at`, timestamps, `created_by_id/updated_by_id`; quan hệ `schedules`. |
| `WeekSchedule` | `week_schedule` | `id`, `task_id`, `ngay_lam_viec`, `ca`, `vi_tri`, `week_start`, timestamps, audit; unique(`task_id, ngay_lam_viec, ca`). |
| `Schedule` | `schedule` | `id`, `employee_id`, `task_id`, `ngay_lam_viec`, `ca`, `week_schedule_id`, timestamps, audit; unique(`employee_id, ngay_lam_viec, ca`). |
| `TKBFile` | `tkb_file` | `id`, `filename`, `content` (bytes), `week_start`, `uploaded_at` — lưu file TKB **đang áp dụng** theo tuần (mỗi `week_start` 1 bản). |
| `Page` | `page` | `id`, `slug` (unique), `tieu_de`, `noi_dung`, `created_at`. |

> Ghi chú: `Employee.vi_tri` có thể chứa cả mức trình độ dạng `"Nhân viên IT(Khá)"` — được tách bằng `parse_vi_tri_with_level()`.

### 3.4. Routes (Blueprints) — `app/routes/`

| Blueprint | Endpoint chính | Mô tả |
|---|---|---|
| **auth** | `auth.index`, `auth.login`, `auth.register`, `auth.logout`, `auth.generate_keys_admin` | Xác thực người dùng, đăng ký bằng Key kích hoạt, sinh Key online. |
| **dashboard** | `dashboard.lich_trinh`, `dashboard.reports_page`, `dashboard.api_last_update`, `dashboard.api_check_ai_readiness` | Xem lịch tuần dạng lưới, báo cáo thống kê, các API trạng thái. |
| **employee** | `employee.employees_page`, `employee.employee_add/edit/delete` | Quản lý nhân viên: danh sách, tìm kiếm, thêm, sửa, xóa. |
| **task** | `task.tasks_page`, `task.task_add/edit/delete/complete`, `task.task_history`, `task.task_assign`, `task.delete_assignment_route`, `task.assign_get_employees`, `task.assign_ai_suggest`, `task.assign_save`, `task.auto_assign_all_tasks`, `task.api_check_conflict` | Quản lý & phân công công việc (thủ công + AI gợi ý), lịch sử hoàn thành, API phân công & kiểm tra trùng ca. |
| **schedule** | `schedule.upload_schedule`, `schedule.schedule_delete`, `schedule.schedule_delete_slot`, `schedule.tkb_file_download`, `schedule.download_template`, `schedule.import_data_page`, `schedule.dynamic_page`, `schedule.page_add` | Nhập TKB tuần từ Excel (lưu file vào DB), xóa toàn bộ tuần, xóa 1 ô (task+ngày+ca), mở file TKB đang áp dụng, tải template mẫu, nhập nhân viên/công việc từ Excel/CSV, trang động. |

### 3.5. Services (Business Logic) — `app/services/`

| Module | Chức năng |
|---|---|
| `validation.py` | `validate_employee_payload()`, `validate_task_payload()` — kiểm tra các trường bắt buộc, định dạng, giá trị hợp lệ. |
| `helpers.py` | `normalize_text()`, `parse_date()`, `parse_date_value()`, `get_week_start()`, `parse_vi_tri_with_level()`, `touch_last_update()`. |
| `scheduling.py` | `check_trung_ca()` (kiểm tra trùng ca), `get_department_filter()`, `get_ai_suggested_employee_ids()` (gợi ý nhân viên theo điểm trình độ/khả dụng), `assign_task_ai()` (tự động phân công 1 mục TKB — **không vượt quá `so_luong_nv`** của công việc). |
| `schema.py` | `ensure_task_schema()` (ALTER TABLE bổ sung cột cho DB cũ), `init_db()` (tạo bảng), `seed_admin()` (tạo tài khoản admin mặc định). |

### 3.6. Templates — `app/templates/`

| Thư mục | Tệp | Giao diện |
|---|---|---|
| (gốc) | `base.html` | Layout chung: sidebar điều hướng, topbar, flash messages, khối `content`/`scripts`. |
| `auth/` | `login.html`, `register.html` | Trang đăng nhập & đăng ký (nhập Key kích hoạt). |
| `dashboard/` | `lich_trinh.html`, `reports.html`, `dynamic_page.html`, `dashboard.html` | Lịch làm việc tuần, báo cáo, trang động, trang tổng quan. |
| `employee/` | `employees.html` | Danh sách + modal thêm/sửa nhân viên. |
| `task/` | `tasks.html`, `task_assign.html`, `task_history.html` | Danh sách công việc, trang phân công (thủ công/AI), lịch sử hoàn thành. |
| `schedule/` | `upload_schedule.html`, `import_data.html` | Nhập TKB tuần từ Excel — **hiển thị "File đang áp dụng"** kèm nút mở để chỉnh sửa; nhập dữ liệu Excel/CSV. |

> Tất cả template con dùng `{% extends "base.html" %}`; URL được sinh qua `url_for('<blueprint>.<endpoint>')` (đã namespace hóa).

---

## 4. Cơ sở dữ liệu

- Vị trí: `instance/database.db` (thư mục `instance/` đã nằm trong `.gitignore`, không đẩy lên git).
- URI cấu hình: `sqlite:///<project_root>/instance/database.db` (trong `config.py`).
- Khi khởi động ứng dụng:
  1. `ensure_task_schema()` — tự động thêm các cột còn thiếu cho DB cũ (tương thích dữ liệu cũ).
  2. `db.create_all()` — tạo toàn bộ bảng nếu chưa tồn tại.
  3. `seed_admin()` — tạo tài khoản **admin / admin123** nếu chưa có.
- Migration: dùng **Flask-Migrate**:
  ```bash
  flask --app app db migrate -m "mô tả thay đổi"
  flask --app app db upgrade
  ```
  Hiện có 2 revision trong `migrations/versions/`: `5d29e689df70_baseline_schema.py` (schema gốc) và `1536ab89a18f_add_tkbfile.py` (thêm bảng `tkb_file`) — schema hiện tại khớp với models.

---

## 5. Cách chạy

```bash
# 1. Tạo môi trường ảo
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Cài đặt thư viện
pip install -r requirements.txt

# 3. Chạy ứng dụng
python app.py
```

Mở trình duyệt: **http://127.0.0.1:5000** — đăng nhập bằng `admin / admin123`.

**Sinh Key kích hoạt:** truy cập `/generate-keys-admin` hoặc chạy `python generate_keys.py`.

**Chạy kiểm thử:**
```bash
pytest tests/
```

**Triển khai trên Render:** Start Command lấy từ `Procfile` → `gunicorn app:app`.

---

## 6. Luồng hoạt động chính

1. **Đăng ký / Đăng nhập** → nhập Key kích hoạt (bảng `activation_keys`) tạo tài khoản mới; đăng nhập bằng Flask-Login.
2. **Quản lý nhân viên** (`/employees`) → thêm/sửa/xóa, hoặc nhập hàng loạt từ Excel/CSV (`/import-data`) hoặc tải file mẫu (`/download-template/employees`).
3. **Quản lý công việc** (`/tasks`) → thêm/sửa/xóa, đánh dấu hoàn thành, xem lịch sử (`/tasks/history`).
4. **Nhập TKB tuần** (`/upload-schedule`) → tải file Excel mẫu (`/download-template/tkb_tuan`), điền mã công việc vào ô theo ca/ngày, hệ thống tạo `week_schedule`; **file đã áp dụng được lưu vào DB** (`tkb_file`) và hiển thị kèm nút mở để chỉnh sửa.
5. **Phân công công việc** (`/tasks/assign`) → chọn công việc, ngày, ca; dùng **AI gợi ý** hoặc chọn thủ công; lưu vào `schedule`; hệ thống ngăn trùng ca (unique constraint + kiểm tra ứng dụng) và **không phân công vượt quá `so_luong_nv`** của công việc.
6. **Xem lịch** (`/lich-trinh`) → hiển thị lịch tuần theo ca, tô màu theo độ ưu tiên; điều hướng tuần trước/sau.
7. **Báo cáo** (`/reports`) → thống kê số ca & tổng giờ làm việc theo nhân viên, theo bộ phận.
8. **Xóa 1 ô trên lịch** → nút xóa mỗi ô trong `lich_trinh.html` gọi `schedule.schedule_delete_slot` để xóa đúng cặp `task_id + ngay_lam_viec + ca` khỏi cả `schedule` lẫn `week_schedule`.

---

## 7. Quy tắc nghiệp vụ

- Tuần làm việc: **Thứ 2 → Chủ nhật**, tuần bắt đầu từ Thứ 2 (`get_week_start`).
- Mỗi ngày 2 ca: **Sáng (07:30–11:30)** và **Chiều (13:00–17:00)**.
- Một nhân viên **không được phân công quá 1 công việc trong cùng 1 ca** — ràng buộc ở tầng DB (`uq_emp_day_ca`) và kiểm tra ứng dụng (`check_trung_ca`).
- Trong lịch tuần, mỗi cặp (công việc + ngày + ca) là duy nhất (`uq_week_schedule`).
- Công việc **hoàn thành** sẽ ẩn khỏi lịch và xóa các mục `week_schedule` liên quan.
