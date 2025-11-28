from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
)
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from collections import defaultdict

# ----------------- APP + CONFIG -----------------

app = Flask(
    __name__,
    static_folder="Frontend",    # where your HTML/CSS/JS lives
    static_url_path="",
    template_folder="Frontend",
)

app.config["SECRET_KEY"] = "wise-hackathon"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///wise.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


# ----------------- MODELS -----------------


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    home_currency = db.Column(db.String(3), default="EUR", nullable=False)

    accounts = db.relationship("Account", backref="user", lazy=True)
    travel_state = db.relationship("TravelState", uselist=False, backref="user")
    # optional: access wallets via relationship
    wallets = db.relationship("TravelWallet", backref="user", lazy=True)


class Account(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(3), nullable=False)
    balance = db.Column(db.Float, default=0.0, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


class TravelState(db.Model):
    __tablename__ = "travel_states"

    id = db.Column(db.Integer, primary_key=True)
    current_country = db.Column(db.String(2), nullable=False)   # e.g. "HU"
    local_currency = db.Column(db.String(3), nullable=False)    # e.g. "HUF"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


class FxRate(db.Model):
    __tablename__ = "fx_rates"

    id = db.Column(db.Integer, primary_key=True)
    base_currency = db.Column(db.String(3), nullable=False)
    quote_currency = db.Column(db.String(3), nullable=False)
    rate = db.Column(db.Float, nullable=False)


class TravelWallet(db.Model):
    """
    One travel wallet per trip:
    - linked to a user
    - country + currency + dates
    - budgets
    """
    __tablename__ = "travel_wallets"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)          # e.g. "Japan 2025"
    country_code = db.Column(db.String(2), nullable=False)    # e.g. "JP"
    currency = db.Column(db.String(3), nullable=False)        # e.g. "JPY"

    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)

    soft_budget = db.Column(db.Float, nullable=True)          # gentle warning
    hard_budget = db.Column(db.Float, nullable=True)          # strict cap (optional)

    is_active = db.Column(db.Boolean, default=True)

    transactions = db.relationship("WalletTransaction", backref="wallet", lazy=True)

    def __repr__(self):
        return f"<TravelWallet {self.name} {self.country_code} {self.currency}>"


class WalletTransaction(db.Model):
    """
    A transaction inside a travel wallet:
    - pre-trip or during-trip
    - stored in local currency, with optional home-currency equivalent
    """
    __tablename__ = "wallet_transactions"

    id = db.Column(db.Integer, primary_key=True)

    wallet_id = db.Column(db.Integer, db.ForeignKey("travel_wallets.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    description = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=True)   # e.g. "Food"

    amount_local = db.Column(db.Float, nullable=False)
    currency_local = db.Column(db.String(3), nullable=False)

    amount_home = db.Column(db.Float, nullable=True)
    currency_home = db.Column(db.String(3), nullable=True)

    is_pre_trip = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f"<WalletTx {self.wallet_id} {self.amount_local} {self.currency_local}>"


# ----------------- DB INIT + SEED -----------------


@app.before_request
def init_db():
    db.create_all()

    # Demo user
    demo = User.query.filter_by(email="demo@wise.com").first()
    if not demo:
        pw_hash = bcrypt.generate_password_hash("demo123").decode("utf-8")
        demo = User(email="demo@wise.com", password_hash=pw_hash, home_currency="EUR")
        db.session.add(demo)
        db.session.commit()

        eur = Account(user_id=demo.id, currency="EUR", balance=500.0)
        huf = Account(user_id=demo.id, currency="HUF", balance=0.0)
        db.session.add_all([eur, huf])
        db.session.commit()

    # FX rates
    if FxRate.query.count() == 0:
        rates = [
            FxRate(base_currency="EUR", quote_currency="HUF", rate=390.0),
            FxRate(base_currency="HUF", quote_currency="EUR", rate=0.00256),
            FxRate(base_currency="EUR", quote_currency="TRY", rate=35.0),
            FxRate(base_currency="EUR", quote_currency="GBP", rate=0.86),
        ]
        db.session.add_all(rates)
        db.session.commit()


# ----------------- HELPERS -----------------


def current_user():
    uid = session.get("user_id")
    if not uid:
        return None
    return User.query.get(uid)


COUNTRY_TO_CURRENCY = {
    "EE": "EUR",
    "HU": "HUF",
    "TR": "TRY",
    "GB": "GBP",
    "US": "USD",
    "PL": "PLN",
    "JP": "JPY",
}


def get_rate(base: str, quote: str) -> float:
    if base == quote:
        return 1.0
    fx = FxRate.query.filter_by(base_currency=base, quote_currency=quote).first()
    if fx:
        return fx.rate
    inv = FxRate.query.filter_by(base_currency=quote, quote_currency=base).first()
    if inv and inv.rate != 0:
        return 1.0 / inv.rate
    return 1.0


def get_or_create_account(user: User, currency: str) -> Account:
    acc = Account.query.filter_by(user_id=user.id, currency=currency).first()
    if not acc:
        acc = Account(user_id=user.id, currency=currency, balance=0.0)
        db.session.add(acc)
        db.session.commit()
    return acc


def create_wallet(user: User, name: str, country_code: str, currency: str,
                  start_date, end_date, soft_budget=None, hard_budget=None) -> TravelWallet:
    wallet = TravelWallet(
        user_id=user.id,
        name=name,
        country_code=country_code,
        currency=currency,
        start_date=start_date,
        end_date=end_date,
        soft_budget=soft_budget,
        hard_budget=hard_budget,
        is_active=True,
    )
    db.session.add(wallet)
    db.session.commit()
    return wallet


def add_wallet_transaction(user, wallet, description, category,
                           amount_local, currency_local, is_pre_trip):

    # Convert to home currency
    rate_to_home = get_rate(currency_local, user.home_currency)
    amount_home = amount_local * rate_to_home

    # -------- Deduct from main account --------
    # If user has local currency account, deduct directly
    if currency_local != user.home_currency:
        acc = get_or_create_account(user, currency_local)
        if acc.balance >= amount_local:
            acc.balance -= amount_local
        else:
            # Not enough local balance → deduct via base currency
            base_acc = get_or_create_account(user, user.home_currency)
            if base_acc.balance >= amount_home:
                base_acc.balance -= amount_home
            else:
                flash("Not enough balance in wallet or main account.")
                return None
    else:
        # local currency == home currency
        acc = get_or_create_account(user, user.home_currency)
        if acc.balance >= amount_local:
            acc.balance -= amount_local
        else:
            flash("Not enough balance.")
            return None

    # Commit account update now
    db.session.commit()

    # -------- Save transaction inside wallet --------
    tx = WalletTransaction(
        wallet_id=wallet.id,
        user_id=user.id,
        description=description,
        category=category,
        amount_local=amount_local,
        currency_local=currency_local,
        amount_home=amount_home,
        currency_home=user.home_currency,
        is_pre_trip=is_pre_trip,
    )

    db.session.add(tx)
    db.session.commit()
    return tx



def wallet_summary(wallet: TravelWallet, user: User):
    txs = WalletTransaction.query.filter_by(wallet_id=wallet.id).all()

    total_pre = 0.0
    total_during = 0.0
    category_totals = defaultdict(float)

    for tx in txs:
        value = tx.amount_home or 0.0
        if tx.is_pre_trip:
            total_pre += value
        else:
            total_during += value
        if tx.category:
            category_totals[tx.category] += value

    total_spent = total_pre + total_during

    return {
        "total_pre_trip": total_pre,
        "total_during_trip": total_during,
        "total_spent": total_spent,
        "category_totals": dict(category_totals),
    }


TRAVEL_GUIDES = {
    "JP": {
        "title": "Japan spending guide",
        "tips": [
            "Carry some cash – many small places still prefer cash.",
            "Use IC cards (Suica/Pasmo) for metro and buses.",
            "Avoid currency conversion at POS, always pay in JPY.",
        ],
    },
    "PL": {
        "title": "Poland spending guide",
        "tips": [
            "Cards widely accepted, but keep small cash for kiosks.",
            "Avoid tourist ATMs, use bank ATMs instead.",
        ],
    },
}


# ----------------- ROUTES: SPLASH + AUTH -----------------


@app.route("/")
def splash():
    # Frontend/index.html = splash / landing
    return render_template("Splash screen.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            return redirect(url_for("home_screen"))

        flash("Invalid login")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ----------------- HOME + BASIC TRAVEL MODE + EXCHANGE -----------------


@app.route("/home")
def home_screen():
    user = current_user()
    if not user:
        return redirect(url_for("login"))

    accounts = user.accounts
    travel_state = user.travel_state

    return render_template(
        "Home.html",
        user=user,
        accounts=accounts,
        travel_state=travel_state,
    )


@app.route("/travel/activate", methods=["POST"])
def travel_activate():
    user = current_user()
    if not user:
        return redirect(url_for("login"))

    country = request.form["country"].strip().upper()
    local = COUNTRY_TO_CURRENCY.get(country, user.home_currency)

    state = TravelState.query.filter_by(user_id=user.id).first()
    if not state:
        state = TravelState(
            user_id=user.id,
            current_country=country,
            local_currency=local,
        )
        db.session.add(state)
    else:
        state.current_country = country
        state.local_currency = local

    db.session.commit()

    get_or_create_account(user, local)

    flash(f"Travel mode activated for {country} ({local})")
    return redirect(url_for("home_screen"))


@app.route("/exchange", methods=["POST"])
def exchange():
    user = current_user()
    if not user:
        return redirect(url_for("login"))

    from_cur = request.form["from_currency"].upper()
    to_cur = request.form["to_currency"].upper()
    try:
        amount = float(request.form["amount"])
    except ValueError:
        flash("Invalid amount")
        return redirect(url_for("home_screen"))

    if amount <= 0:
        flash("Amount must be positive")
        return redirect(url_for("home_screen"))

    from_acc = get_or_create_account(user, from_cur)
    to_acc = get_or_create_account(user, to_cur)

    if from_acc.balance < amount:
        flash("Not enough balance")
        return redirect(url_for("home_screen"))

    rate = get_rate(from_cur, to_cur)
    amount_to = amount * rate

    from_acc.balance -= amount
    to_acc.balance += amount_to
    db.session.commit()

    flash(f"Exchanged {amount} {from_cur} → {amount_to:.2f} {to_cur}")
    return redirect(url_for("home_screen"))


# ----------------- TRAVEL WALLETS -----------------


@app.route("/travel/wallets")
def travel_wallets_list():
    user = current_user()
    if not user:
        return redirect(url_for("login"))

    wallets = TravelWallet.query.filter_by(user_id=user.id).order_by(
        TravelWallet.id.desc()
    ).all()

    return render_template(
        "newstravelwallet.html",
        user=user,
        wallets=wallets,
    )


@app.route("/travel/wallets/new", methods=["GET", "POST"])
def travel_wallet_new():
    user = current_user()
    if not user:
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        country_code = request.form.get("country_code", "").strip().upper()
        currency = request.form.get("currency", "").strip().upper()

        start_str = request.form.get("start_date", "").strip()
        end_str = request.form.get("end_date", "").strip()
        soft_budget_str = request.form.get("soft_budget", "").strip()
        hard_budget_str = request.form.get("hard_budget", "").strip()

        start_date = datetime.strptime(start_str, "%Y-%m-%d").date() if start_str else None
        end_date = datetime.strptime(end_str, "%Y-%m-%d").date() if end_str else None

        soft_budget = float(soft_budget_str) if soft_budget_str else None
        hard_budget = float(hard_budget_str) if hard_budget_str else None

        if not name or not country_code or not currency:
            flash("Name, country and currency are required.")
            return redirect(url_for("travel_wallet_new"))

        wallet = create_wallet(
            user=user,
            name=name,
            country_code=country_code,
            currency=currency,
            start_date=start_date,
            end_date=end_date,
            soft_budget=soft_budget,
            hard_budget=hard_budget,
        )

        flash("Travel wallet created.")
        return redirect(url_for("travel_wallet_detail", wallet_id=wallet.id))

    return render_template("newtravelwallet.html", user=user)


@app.route("/travel/wallets/<int:wallet_id>")
def travel_wallet_detail(wallet_id):
    user = current_user()
    if not user:
        return redirect(url_for("login"))

    wallet = TravelWallet.query.filter_by(id=wallet_id, user_id=user.id).first()
    if not wallet:
        flash("Wallet not found")
        return redirect(url_for("travel_wallets_list"))

    transactions = WalletTransaction.query.filter_by(wallet_id=wallet.id).order_by(
        WalletTransaction.created_at.asc()
    ).all()

    summary = wallet_summary(wallet, user)
    guide = TRAVEL_GUIDES.get(wallet.country_code, None)

    return render_template(
        "newtravelwallet.html",
        user=user,
        wallet=wallet,
        transactions=transactions,
        summary=summary,
        guide=guide,
    )


@app.route("/travel/wallets/<int:wallet_id>/transactions/add", methods=["POST"])
def travel_wallet_add_tx(wallet_id):
    user = current_user()
    if not user:
        return redirect(url_for("login"))

    wallet = TravelWallet.query.filter_by(id=wallet_id, user_id=user.id).first()
    if not wallet:
        flash("Wallet not found")
        return redirect(url_for("travel_wallets_list"))

    description = request.form.get("description", "").strip()
    category = request.form.get("category", "").strip()
    amount_str = request.form.get("amount_local", "").strip()
    currency_local = request.form.get("currency_local", "").strip().upper() or wallet.currency
    is_pre_trip_str = request.form.get("is_pre_trip", "false")

    if not description or not amount_str:
        flash("Description and amount are required.")
        return redirect(url_for("travel_wallet_detail", wallet_id=wallet.id))

    try:
        amount_local = float(amount_str)
    except ValueError:
        flash("Invalid amount.")
        return redirect(url_for("travel_wallet_detail", wallet_id=wallet.id))

    is_pre_trip = is_pre_trip_str.lower() == "true" or is_pre_trip_str == "on"

    add_wallet_transaction(
        user=user,
        wallet=wallet,
        description=description,
        category=category,
        amount_local=amount_local,
        currency_local=currency_local,
        is_pre_trip=is_pre_trip,
    )

    flash("Transaction added.")
    return redirect(url_for("travel_wallet_detail", wallet_id=wallet.id))


# ----------------- RUN -----------------


if __name__ == "__main__":
    app.run(debug=True)
