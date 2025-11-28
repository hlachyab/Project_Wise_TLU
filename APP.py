from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt


app = Flask(__name__,static_folder="Frontend",
    static_url_path="",
    template_folder="Frontend",)
app.config["SECRET_KEY"] = "wise-hackathon"   # can be anything
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///wise.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    home_currency = db.Column(db.String(3), default="EUR")

    accounts = db.relationship("Account", backref="user", lazy=True)
    travel_state = db.relationship("TravelState", uselist=False, backref="user")


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(3), nullable=False)   # "EUR", "HUF", etc.
    balance = db.Column(db.Float, default=0.0)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class TravelState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    current_country = db.Column(db.String(2), nullable=False)   # "HU"
    local_currency = db.Column(db.String(3), nullable=False)    # "HUF"

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class FxRate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    base_currency = db.Column(db.String(3), nullable=False)
    quote_currency = db.Column(db.String(3), nullable=False)
    rate = db.Column(db.Float, nullable=False)

@app.before_request
def init_db():
    db.create_all()

    # 1) Demo user
    user = User.query.filter_by(email="demo@wise.com").first()
    if not user:
        pw_hash = bcrypt.generate_password_hash("demo123").decode("utf-8")
        user = User(email="demo@wise.com", password_hash=pw_hash, home_currency="EUR")
        db.session.add(user)
        db.session.commit()

        # 2) Start with some accounts
        eur = Account(user_id=user.id, currency="EUR", balance=500.0)
        huf = Account(user_id=user.id, currency="HUF", balance=0.0)
        db.session.add_all([eur, huf])
        db.session.commit()

    # 3) FX rates
    if not FxRate.query.first():
        rates = [
            FxRate(base_currency="EUR", quote_currency="HUF", rate=390.0),
            FxRate(base_currency="HUF", quote_currency="EUR", rate=0.00256),
            FxRate(base_currency="EUR", quote_currency="TRY", rate=35.0),
        ]
        db.session.add_all(rates)
        db.session.commit()


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.before_request
def create_tables():
    db.create_all()

    # 1) Demo user
    demo = User.query.filter_by(email="demo@wise.com").first()
    if not demo:
        pw_hash = bcrypt.generate_password_hash("demo123").decode("utf-8")
        demo = User(
            email="demo@wise.com",
            password_hash=pw_hash,
            home_currency="EUR",
        )
        db.session.add(demo)
        db.session.commit()

        # 2) Start with 500 EUR in main account
        eur_acc = Account(user_id=demo.id, currency="EUR", balance=500.0)
        db.session.add(eur_acc)
        db.session.commit()

    # 3) Seed some FX rates (only if table is empty)
    if FxRate.query.count() == 0:
        fx_data = [
            FxRate(base_currency="EUR", quote_currency="HUF", rate=390.0),
            FxRate(base_currency="HUF", quote_currency="EUR", rate=0.00256),
            FxRate(base_currency="EUR", quote_currency="TRY", rate=35.0),
            FxRate(base_currency="EUR", quote_currency="GBP", rate=0.86),
        ]
        db.session.add_all(fx_data)
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)

