from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)

# Database
app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

##CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

#Line below only required once, when creating DB. 
# db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/')
def home():
    return render_template("index.html", logged_in=current_user.is_authenticated)

@app.route('/register', methods=["GET", "POST"])
def register():
    user_list = User.query.all()

    # If the request method is "POST"
    if request.method == "POST":
        # First check if the user is in the user_list first,

        # Solution 1:My solution using the 'for' loop
        # for user in user_list:
        #     if request.form.get("email") == user.email:
        #         flash("Looks like you've already registered. Please login.", "info")
        #         return redirect(url_for('login'))

        # Solution 2: Angela's solution using 'filter_by'--fewer and simpler codes
        if User.query.filter_by(email=request.form.get('email')).first():
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        # If not exist, then add in the datbase,
        # Get the data from the form in HTML
        else:
            new_user = User(
                name=request.form.get("name"),
                email=request.form.get("email"),
                password=generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
            )
            # Store the data into the database users.db
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return render_template("secrets.html", name=current_user.name)
    return render_template("register.html", logged_in=current_user.is_authenticated)

@app.route('/login' , methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        # Get the data from the database. i.e. Show password filtered by email
        email = request.form.get("email")
        password = request.form.get('password')

        # Find user
        user = User.query.filter_by(email=email).first()

        # Update the login route so that if the user's email doesn't exist in the database,
        # you send them a Flash message to let them know and redirect them back to the login route
        if user == None:
            flash("Looks like the user doesn't exist.", "info")
            return redirect(url_for('login'))

        # If the checking password hash is true
        elif check_password_hash(pwhash=user.password, password=password):
            # then login the user
            login_user(user)
            print(f"You successfully login as {current_user.email}")
            # After logging the user, redirect to 'secrets' page
            # Error here: getting the unathorized page
            return redirect(url_for('secrets'))

        # If not, i.e the checking password hash is false
        else:
            # then redirect to login page again
            message = f"Hmm...looks like the password is incorrect.\n " \
                      f"Try again with the right password for {email}."
            flash(message)
            return redirect(url_for('login'))
    return render_template("login.html", logged_in=current_user.is_authenticated)

@app.route('/secrets')
@login_required
def secrets():
    # Only show this page if user is authenticated
    return render_template("secrets.html", name=current_user.name, logged_in=current_user.is_authenticated)

@app.route('/download')
@login_required
def download():
    return send_from_directory('static', filename='files/cheat_sheet.pdf')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
