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
- `app.py`: Main entry point. Contains all route definitions, session management, and business logic for authentication and expense tracking.
- `models.py`: Defines the SQLAlchemy ORM models:
    - `User`: Manages user accounts and authentication.
    - `Expense`: Stores financial records linked to a user, categorized by "to_pay" or "take_from".
- `database.py`: Handles database initialization and schema creation.

### Frontend
- `templates/`: Jinja2 templates using a base layout (`base.html`) for consistency.
- `static/css/style.css`: Core styling, utilizing a custom set of CSS variables for theme management.
- `static/js/main.js`: Basic client-side interactions.

### Database
- SQLite database located in `instance/expenses.db`.

## Key Implementation Details
- **Authentication**: Implemented using Flask sessions and `werkzeug.security` for password hashing.
- **Expense Logic**: The dashboard uses a tabbed interface to separate money owed to others from money owed by others.
- **Styling**: Uses a modern, card-based responsive design with specific breakpoints for mobile and desktop.
