from travel_core import (
    activate_travel_mode,
    get_spending_summary,
    get_insights,
    get_fx,
)

def print_divider():
    print("\n" + "-" * 50 + "\n")

def main():
    user_id = "demo-user"
    base_currency = "EUR"

    print("=== Wise Travel Mode Demo ===")
    country = input("Enter destination country code (e.g. HU, TR): ").strip().upper()

    print_divider()
    state = activate_travel_mode(user_id, country, base_currency)
    print("Travel Mode State:")
    print(state)

    print_divider()
    print("FX Rate Example:")
    fx = get_fx(base_currency, state.local_currency)
    print(f"1 {fx.base} ≈ {fx.rate} {fx.quote}")

    print_divider()
    print(f"Insights for {country}:")
    for insight in get_insights(country):
        print(f"[{insight.type.upper()}] {insight.title} -> {insight.description}")

    print_divider()
    print("Spending summary:")
    summary = get_spending_summary(user_id)
    print(f"Total spent today: {summary.total_spent_local} {summary.local_currency}")
    for cat in summary.categories:
        print(f"- {cat.category}: {cat.amount_local} {summary.local_currency}")

if __name__ == "__main__":
    main()
