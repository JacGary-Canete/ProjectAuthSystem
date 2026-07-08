# LapTrack

LapTrack is a Django-based laptop inventory and loan management system built for CCIS. It allows Staff/IT Admins to manage a laptop inventory and process check-ins, while Students can browse available laptops, borrow one, and return it — all backed by a Supabase (PostgreSQL) database.

## Features

- **Role-based registration and login** — users register as either Staff or Student, which determines their dashboard and permissions
- **Custom Admin Dashboard** (Staff only) — view laptop inventory, add/edit laptops, manage active loans, and process check-ins
- **Student Dashboard** — view available laptop count, browse and borrow laptops, view and return an active loan
- **One active loan per student** — students cannot borrow another laptop until their current one is returned
- **Laptop status tracking** — Available, Borrowed, and Under Maintenance

## Tech Stack

- **Backend:** Django 6.0
- **Database:** Supabase (PostgreSQL)
- **Frontend:** Django templates, vanilla CSS

## Project Structure
project_auth_system/
├── manage.py
├── project_auth_system/     # Django settings, root URL routing
├── myapp/                   # Core app: models, views, forms, templates
│   ├── models.py            # User (built-in), Laptop, Loan
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── templates/myapp/
│   └── static/myapp/
└── requirements.txt

## Setup Instructions

1. Clone the repository:
git clone https://github.com/JacGary-Canete/ProjectAuthSystem.git
cd ProjectAuthSystem

2. Create and activate a virtual environment:
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux

3. Install dependencies:
pip install -r requirements.txt

4. Create a `.env` file in the project root:
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=your-supabase-connection-string

5. Run migrations:
python manage.py migrate

6. Start the development server:
python manage.py runserver

7. Visit `http://127.0.0.1:8000/register/` to create an account.

## Database Schema

**User** — built-in Django user model, extended via `is_staff` to indicate role (Staff vs Student)

**Laptop** — asset_tag, brand, model, processor, ram_gb, storage_gb, battery_health, status, purchase_date, condition_notes

**Loan** — laptop (FK), borrower (FK to User), processed_by (FK to User, nullable), checkout_date, due_date, return_date, loan_status

## Roadmap

- Password complexity validation
- "Forgot Password" recovery flow
- Account lockout after failed login attempts
- Overdue loan detection and notifications