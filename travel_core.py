from dataclasses import dataclass
from datetime import date
from typing import List, Dict, Optional


# ---------- Data models ----------

@dataclass
class TravelModeState:
    user_id: str
    current_country: str
    local_currency: str
    base_currency: str
    fx_rate: float
    message: str


@dataclass
class Insight:
    country: str
    title: str
    description: str
    type: str  # "card", "atm", "tip", "warning"


@dataclass
class SpendCategory:
    category: str
    amount_local: float
    amount_base: float


@dataclass
class SpendingSummary:
    user_id: str
    country: str
    local_currency: str
    date: date
    total_spent_local: float
    total_spent_base: float
    categories: List[SpendCategory]


@dataclass
class FxRate:
    base: str
    quote: str
    rate: float
    as_of: str = "hackathon-demo"


# databse

COUNTRY_TO_CURRENCY: Dict[str, str] = {
    "EE": "EUR",
    "HU": "HUF",
    "TR": "TRY",
    "GB": "GBP",
    "US": "USD",
}

FX_RATES: Dict[str, Dict[str, float]] = {
    "EUR": {"HUF": 390.0, "TRY": 35.0, "GBP": 0.86, "USD": 1.08},
    "HUF": {"EUR": 0.00256},
}

INSIGHTS: Dict[str, List[Insight]] = {
    "HU": [
        Insight(
            country="HU",
            title="Cards widely accepted",
            description="Most shops in Budapest accept contactless cards, but small kiosks may prefer cash.",
            type="card",
        ),
        Insight(
            country="HU",
            title="ATM fee warning",
            description="Avoid Euronet ATMs in tourist areas; bank-owned ATMs usually have better rates.",
            type="atm",
        ),
        Insight(
            country="HU",
            title="Pay in local currency",
            description="Always choose HUF instead of 'pay in your card currency' to avoid bad conversion.",
            type="tip",
        ),
    ],
    "TR": [
        Insight(
            country="TR",
            title="Cash still common",
            description="Cards are common in big cities, but keep some TRY for taxis and small shops.",
            type="card",
        )
    ],
}

MOCK_SPENDING: Dict[str, SpendingSummary] = {
    "demo-user": SpendingSummary(
        user_id="demo-user",
        country="HU",
        local_currency="HUF",
        date=date.today(),
        total_spent_local=45230.0,
        total_spent_base=116.0,
        categories=[
            SpendCategory("Food & Drinks", 22000, 56.5),
            SpendCategory("Transport", 8000, 20.5),
            SpendCategory("Attractions", 15230, 39.0),
        ],
    )
}

TRAVEL_STATE: Dict[str, TravelModeState] = {}


# ---------- Helper functions ----------

def get_fx_rate(base: str, quote: str) -> Optional[float]:
    if base in FX_RATES and quote in FX_RATES[base]:
        return FX_RATES[base][quote]
    return None


def get_local_currency(country: str, base_currency: str) -> str:
    return COUNTRY_TO_CURRENCY.get(country, base_currency)


#fun
def activate_travel_mode(
    user_id: str,
    current_country: str,
    base_currency: str,
) -> TravelModeState:
    """
    Core logic to 'turn on' travel mode.
    """
    local_currency = get_local_currency(current_country, base_currency)

    rate = get_fx_rate(base_currency, local_currency)
    if rate is None:
        rate = 1.0  # fallback for unknown pairs

    message = (
        f"Travel Mode activated for {current_country}. "
        f"Spending in {local_currency} with base currency {base_currency}. "
        f"Current rate: 1 {base_currency} ≈ {rate} {local_currency}."
    )

    state = TravelModeState(
        user_id=user_id,
        current_country=current_country,
        local_currency=local_currency,
        base_currency=base_currency,
        fx_rate=rate,
        message=message,
    )

    TRAVEL_STATE[user_id] = state
    return state


def get_spending_summary(user_id: str) -> SpendingSummary:
    """
    Return a demo spending summary for the user.
    """
    summary = MOCK_SPENDING.get(user_id)
    if not summary:
        summary = SpendingSummary(
            user_id=user_id,
            country="UNKNOWN",
            local_currency="XXX",
            date=date.today(),
            total_spent_local=0.0,
            total_spent_base=0.0,
            categories=[],
        )
    return summary


def get_insights(country: str) -> List[Insight]:
    """
    Return travel insights (tips/warnings) for a given country.
    """
    return INSIGHTS.get(country, [])


def get_fx(from_currency: str, to_currency: str) -> FxRate:
    rate = get_fx_rate(from_currency, to_currency)
    if rate is None:
        rate = 1.0
    return FxRate(base=from_currency, quote=to_currency, rate=rate)
