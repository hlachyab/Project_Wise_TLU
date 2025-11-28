from flask_sqlalchemy import SQLAlchemy

# Single SQLAlchemy instance for the application
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    home_currency = db.Column(db.String(3), nullable=False, default="EUR")

    accounts = db.relationship("Account", backref="user", lazy=True, cascade="all, delete-orphan")
    travel_state = db.relationship(
        "TravelState", backref=db.backref("user", uselist=False), uselist=False, cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"<User id={self.id!r} email={self.email!r} "
            f"home_currency={self.home_currency!r}>"
        )


class Account(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    balance = db.Column(db.Float, nullable=False, default=0.0)

    def __repr__(self) -> str:
        return (
            f"<Account id={self.id!r} user_id={self.user_id!r} "
            f"currency={self.currency!r} balance={self.balance!r}>"
        )


class TravelState(db.Model):
    __tablename__ = "travel_states"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    current_country = db.Column(db.String(2), nullable=False)
    local_currency = db.Column(db.String(3), nullable=False)

    def __repr__(self) -> str:
        return (
            f"<TravelState id={self.id!r} user_id={self.user_id!r} "
            f"current_country={self.current_country!r} local_currency={self.local_currency!r}>"
        )


class FxRate(db.Model):
    __tablename__ = "fx_rates"

    id = db.Column(db.Integer, primary_key=True)
    base_currency = db.Column(db.String(3), nullable=False)
    quote_currency = db.Column(db.String(3), nullable=False)
    rate = db.Column(db.Float, nullable=False)

    def __repr__(self) -> str:
        return (
            f"<FxRate id={self.id!r} base_currency={self.base_currency!r} "
            f"quote_currency={self.quote_currency!r} rate={self.rate!r}>"
        )
