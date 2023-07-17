from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import secrets
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'lendahand_ika@outlook.com'
app.config['MAIL_PASSWORD'] = 'Q#f3^eCGshT-9Nb'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'lendahand_ika@outlook.com'

db = SQLAlchemy(app)
mail = Mail(app)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    verification_code = db.Column(db.String(10), nullable=True)

with app.app_context():
        db.create_all()

@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['user_email'] = user.email  # Store the user's email in the session
            return redirect('/success')

        return render_template('login.html', message='Invalid credentials')

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template('signup.html', message='Account with email already exists')

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        session['user_email'] = email  # Store the user's email in the session
        return redirect('/success')

    return render_template('signup.html')


@app.route('/success')
def success():
    user_email = session.get('user_email')

    if not user_email:
        return redirect('/login')

    user = User.query.filter_by(email=user_email).first()
    return render_template('success.html', name=user.name, user_email=user.email)
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')

        user = User.query.filter_by(email=email).first()
        if user:
            # Generate a verification code
            verification_code = generate_verification_code()
            user.verification_code = verification_code
            db.session.commit()

            # Send the verification email
            send_verification_email(user.email, verification_code)

            session['user_email'] = user.email  # Store the user's email in the session for verification

            return redirect('/verify')

        return render_template('forgot_password.html', message='Email not found')

    return render_template('forgot_password.html')


@app.route('/verify', methods=['GET', 'POST'])
def verify():
    user_email = session.get('user_email')

    if not user_email:
        return redirect('/forgot_password')

    if request.method == 'POST':
        verification_code = request.form.get('verification_code')

        user = User.query.filter_by(email=user_email).first()
        if user and user.verification_code == verification_code:
            session['reset_email'] = user.email  # Store the user's email in the session for password reset
            return redirect('/reset_password')

        return render_template('verify.html', message='Invalid verification code')

    return render_template('verify.html')


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    reset_email = session.get('reset_email')

    if not reset_email:
        return redirect('/forgot_password')

    if request.method == 'POST':
        password = request.form.get('password')

        user = User.query.filter_by(email=reset_email).first()
        if user:
            user.password = password
            user.verification_code = None  # Clear the verification code after successful password reset
            db.session.commit()
            session.pop('reset_email', None)  # Remove the reset_email from the session
            return redirect('/success?name=' + user.name)

        return render_template('reset_password.html', message='Email not found')

    return render_template('reset_password.html')


def generate_verification_code():
    code_length = 6
    characters = string.digits
    verification_code = ''.join(secrets.choice(characters) for _ in range(code_length))
    return verification_code


def send_verification_email(email, verification_code):
    msg = Message('Password Reset Verification Code', recipients=[email])
    msg.body = f'Your verification code is: {verification_code}'
    mail.send(msg)

@app.route('/needahand')
def need_a_hand():
    return render_template('task_page.html')


if __name__ == '__main__':

    app.run(debug=True)

