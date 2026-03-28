# Hotel Management System (Flask + MySQL)

**Branding:** Configured for **Swagat Corner** ([swagatcorner.com](https://swagatcorner.com/)). The official logo is saved as `frontend/static/images/swagat-logo.png`. Website links, PDF menu, WhatsApp, and Vadodara outlets live in `backend/brand_data.py`. Taglines: main line matches the site (“Where Every Bite Tells a Delicious Story!”); the printed-menu line is shown as a second line. Override via `BRAND_*` in `backend/.env` if needed.

Modern web application for hotel / restaurant operations: table and parcel orders, kitchen workflow, billing with GST, staff, attendance, salary, and reports. Uses **HTML/CSS/JS** front-end (Jinja2 templates), **Flask** (MVC-style layout), and **MySQL** / MariaDB.

## Project layout

```text
hotel/
├── backend/           # Flask app (app.py, routes, models, services)
├── frontend/
│   ├── templates/     # Jinja2 pages
│   └── static/        # CSS, JS
└── database/
    └── schema.sql     # MySQL schema
```

## Requirements

- Python 3.10+
- MySQL or MariaDB

## Database setup

1. Create database and tables:

```sql
SOURCE path/to/database/schema.sql;
SOURCE path/to/database/seed.sql;
```

2. Default login after seed: **admin** / **admin123**

If you already had an older `hotel_management` schema, drop and recreate it so all new tables (`users`, `staff`, `attendance`, etc.) exist.

## Backend configuration

Copy `backend/.env.example` to `backend/.env` and set:

- `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`
- Optional: `SECRET_KEY`, `GST_PERCENT` (default 5), `PORT` (default 5000)

Alternatively set `DATABASE_URL` (overrides DB\_\*), e.g.:

`mysql+pymysql://user:pass@localhost:3306/hotel_management?charset=utf8mb4`

## Run

```powershell
cd backend
pip install -r requirements.txt
python app.py
```

Open [http://localhost:5000](http://localhost:5000) and sign in.

## Features (summary)

- **Dashboard:** tables, active orders, parcel count, daily revenue, staff present today, live order count (SSE + polling fallback).
- **Table orders:** table selection, menu search, cart JSON, duplicate active order blocked per table.
- **Parcel orders:** customer name/phone, items, kitchen + billing flow (`Delivered` instead of `Served`).
- **Kitchen:** advance status until ready, then Served/Delivered; auto bill + free table for dine-in.
- **Menu:** CRUD (admin/manager).
- **Billing:** subtotal, GST, total, print receipt, mark paid.
- **Staff / attendance / salary:** HR modules with monthly salary pro-rated by attendance (Mon–Sat working days).
- **Reports:** daily/monthly sales, table vs parcel counts, top items.

## Security

- Passwords stored with Werkzeug hashes.
- Role checks on sensitive routes (`admin` / `manager` for HR and menu).

## Old Node.js backend

The previous Express prototype was removed. Use the Flask app only.

You may delete `backend/node_modules` manually if it is still present.
