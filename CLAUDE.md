# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands
- Run application: `python app.py`
- Install dependencies: `pip install flask flask-sqlalchemy`
- Environment variables: `SECRET_KEY` (used for session encryption)
- Tests: No tests currently implemented. Use `pytest` if adding new tests.

## Architecture & Structure
The application is a full-stack expense tracker built with Flask and SQLite.

### Backend
- `app.py`: Main entry point. Contains all route definitions, session management, and business logic for authentication, expense tracking, and person-based views.
- `models.py`: Defines the SQLAlchemy ORM models:
    - `User`: Manages user accounts and authentication.
    - `Expense`: Stores financial records linked to a user, categorized by "to_pay" or "take_from", associated with a specific person.
- `database.py`: Handles database initialization and schema creation.

### Frontend
- `templates/`: Jinja2 templates using a base layout (`base.html`) for consistency.
    - `index.html`: Landing page.
    - `login.html` & `register.html`: Authentication pages.
    - `dashboard.html`: View all expenses using a tabbed interface.
    - `add_expense.html`: Dedicated page for creating new expense entries.
    - `people.html`: List of all people associated with expenses.
    - `person_details.html`: Detailed view of expenses and net balance for a specific person.
- `static/css/style.css`: Core styling, utilizing a custom set of CSS variables for theme management.
- `static/js/main.js`: Basic client-side interactions.

### Database
- SQLite database located in `instance/expenses.db`.

## Key Implementation Details
- **Authentication**: Implemented using Flask sessions and `werkzeug.security` for password hashing. Supports registration and login via username or email.
- **Expense Logic**: Expenses are categorized into "To Pay" (money owed by user) and "Take From" (money owed to user). Managed via `/add_expense` and `/dashboard`. Includes functionality to delete individual expenses.
- **Person-based Tracking**: Unique people are extracted from the `Expense` records to provide summary views per person (`/people` and `/person/<name>`), calculating a net balance based on expense categories.
- **Styling**: Uses a modern, card-based responsive design with specific breakpoints for mobile and desktop.
