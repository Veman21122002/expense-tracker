from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Expense
from database import init_db
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'instance', 'expenses.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
init_db(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not username or not email or not password:
            flash('All fields are required', 'error')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('register.html')

        user_exists = User.query.filter((User.username == username) | (User.email == email)).first()
        if user_exists:
            flash('Username or email already registered', 'error')
            return render_template('register.html')

        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form.get('identifier') # username or email
        password = request.form.get('password')

        user = User.query.filter((User.username == identifier) | (User.email == identifier)).first()

        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('dashboard'))

        flash('Invalid username/email or password', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    expenses = Expense.query.filter_by(user_id=user_id).all()

    to_pay = [e for e in expenses if e.category == 'to_pay']
    take_from = [e for e in expenses if e.category == 'take_from']

    total_to_pay = sum(e.amount for e in to_pay)
    total_take_from = sum(e.amount for e in take_from)

    return render_template('dashboard.html',
                           to_pay=to_pay,
                           take_from=take_from,
                           total_to_pay=total_to_pay,
                           total_take_from=total_take_from)

@app.route('/add_expense', methods=['POST'])
def add_expense():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    try:
        person_name = request.form.get('person_name')
        amount = float(request.form.get('amount'))
        category = request.form.get('category')
        description = request.form.get('description', '')
        date = request.form.get('date')

        if not person_name or not amount or not category or not date:
            flash('Please fill in all required fields', 'error')
            return redirect(url_for('dashboard'))

        new_expense = Expense(
            user_id=session['user_id'],
            person_name=person_name,
            amount=amount,
            category=category,
            description=description,
            date=date
        )
        db.session.add(new_expense)
        db.session.commit()
        flash('Expense added successfully!', 'success')
    except (ValueError, TypeError):
        flash('Invalid amount entered', 'error')

    return redirect(url_for('dashboard'))

@app.route('/delete_expense/<int:expense_id>')
def delete_expense(expense_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    expense = Expense.query.get(expense_id)
    if expense and expense.user_id == session['user_id']:
        db.session.delete(expense)
        db.session.commit()
        flash('Expense deleted', 'success')
    else:
        flash('Expense not found or unauthorized', 'error')

    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
