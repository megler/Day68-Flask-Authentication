# flaskAuthentication
#
# Python Bootcamp Day 68 - Flask Authentication
# Usage:
#      A basic Flask app that creates new users, checks for login and shows custom
# pages based on login status.
#
# Marceia Egler January 19, 2022

from flask import (
    Flask,
    render_template,
    request,
    url_for,
    redirect,
    flash,
    send_from_directory,
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    login_required,
    current_user,
    logout_user,
)
import secrets

app = Flask(__name__)

app.config["SECRET_KEY"] = secrets.token_urlsafe(16)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    """Create user Table In DB"""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(1000))
    name = db.Column(db.String(100))


# Line below only required once, when creating DB.
# db.create_all()


@login_manager.user_loader
def load_user(id):
    """Login Manager For Flask-Login"""
    return User.query.get(int(id))


@app.route("/")
def home():
    """Home Route"""
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register new user. Check if User already in DB."""
    if request.method == "POST":
        username = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form.get("password"),
                                          method="pbkdf2:sha256",
                                          salt_length=8)
        email_check = User.query.filter_by(email=email).first()

        if email == email_check.email:
            error = (
                "There is already a user with this email. Perhaps you meant to log in?"
            )
            return redirect(url_for(
                "login",
                error=error,
            ))
        new_user = User(
            name=username,
            email=email,
            password=password,
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("secrets", name=new_user.name))
    return render_template("register.html")


@app.route("/login/", methods=["GET", "POST"])
@app.route("/login/<error>", methods=["GET", "POST"])
def login(error=None):
    """User Login."""
    if current_user.is_authenticated:
        return redirect(url_for("secrets", name=current_user.name))

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if not user:
            error = "Invalid email address. Please try again."
        elif not check_password_hash(user.password, password):
            error = "Invalid password. Please try again."
        else:
            flash("You were successfully logged in")
            login_user(user)
            return redirect(url_for("secrets"))
    return render_template("login.html", error=error)


@app.route("/secrets")
@login_required
def secrets():
    """Secrets page with link for file download."""
    return render_template("secrets.html")


@app.route("/logout")
@login_required
def logout():
    """User logout."""
    logout_user()
    return redirect(url_for("home"))


@app.route("/download/<path:filename>")
@login_required
def download(filename):
    """Download requested file."""
    from pathlib import Path

    root = Path(".")
    folder_path = root / "static/files"
    return send_from_directory(folder_path, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
