from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import secrets
import string
import datetime

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

skills_array = ['Education and Mentoring', 'Graphic Design', 'Communication and Outreach', 'Manual work', 'IT/Programming']
causes_array = ['Education', 'Social Justice', 'Communities/Individuals in need','Environment']

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    verification_code = db.Column(db.String(10), nullable=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(50), nullable=True)
    date = db.Column(db.String(50), nullable=False)
    skills = db.Column(db.String(400), nullable=False)
    causes = db.Column(db.String(400), nullable=False)
    online = db.Column(db.Boolean, nullable=True)
    location = db.Column(db.String(100), nullable=True)
    additional_info = db.Column(db.String(300), nullable=True)
    time_required = db.Column(db.Integer, nullable=False)
    min_age = db.Column(db.Integer, nullable=True)


with app.app_context():
        db.create_all()

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/logout')
def logout():
    session['user_email'] = None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['user_email'] = user.email  # Store the user's email in the session
            session['name'] = user.name
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
    tasks = Task.query.all()
    user_email = session.get('user_email')

    if not user_email:
        return redirect('/login')

    user = User.query.filter_by(email=user_email).first()
    return render_template('success.html', name=user.name, email=user.email, tasks=tasks, skills=skills_array,causes=causes_array)

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

@app.route('/needahand', methods=['GET', 'POST'])
def need_a_hand():
    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        print(request.form.getlist('skills'))
        skills = ', '.join(request.form.getlist('skills[]'))
        causes = ', '.join(request.form.getlist('causes[]'))

        location = request.form['location']
        additional_info = request.form['additional-info']
        time_required = request.form['time-required']
        min_age = request.form['min-age']

        user_email = session['user_email']
        online = False
        if request.form['online'] == "online":
            online = True


        new_task = Task(
            title = title,
            causes=causes,
            online = online,
            date=date,
            user_email = user_email,
            skills=skills,
            location=location,
            additional_info=additional_info,
            min_age=min_age,
            time_required=time_required
        )

        db.session.add(new_task)
        db.session.commit()

        return redirect('/success')

    return render_template('task_page.html', skills=skills_array,causes=causes_array)

@app.route('/volunteer', methods=['POST'])
def volunteer():
    if request.method == 'POST':
        email_content = request.form.get('emailContent')

        msg = Message('Volunteer Alert', recipients=['onawhim1612@gmail.com'])
        msg.body = email_content
        try:
            mail.send(msg)
            return "Email sent successfully!"
        except Exception as e:
            return f"Error sending email: {str(e)}"

if __name__ == '__main__':

    app.run(debug=True)
