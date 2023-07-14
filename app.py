from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import secrets
import string
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database file
app.config['SECRET_KEY'] = ''  # Add a secret key
app.config['MAIL_SERVER'] = ''
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

db = SQLAlchemy(app)
mail = Mail(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)


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
            return redirect('/success?name=' + user.name)

        return render_template('login.html', message='Invalid credentials')

    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the email is already registered
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template('signup.html', message='Account with email already exists')

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/success?name=' + name)

    return render_template('signup.html')


@app.route('/success')
def success():
    name = request.args.get('name')
    return render_template('success.html', name=name)

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')

        # Check if the email exists in the database
        user = User.query.filter_by(email=email).first()
        if user:
            # Generate a secure token
            token = generate_token()


            user.token = token
            db.session.commit()


            send_reset_email(user.email, token)

        return redirect('/')

    return render_template('forgot_password.html')

def generate_token():
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(32))

def send_reset_email(email, token):
    reset_link = f"http://example.com/reset_password?token={token}"
    msg = Message("Password Reset Request", sender="noreply@example.com", recipients=[email])
    msg.body = f"Please click the link below to reset your password:\n\n{reset_link}"
    mail.send(msg)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    token = request.args.get('token')

    if request.method == 'POST':
        new_password = request.form.get('password')

        # Find the user with the provided token
        user = User.query.filter_by(token=token).first()

        if user:
            # Update the password
            user.password = new_password
            user.token = None  # Clear the token
            db.session.commit()

            return redirect('/success')

    return render_template('reset_password.html', token=token)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
