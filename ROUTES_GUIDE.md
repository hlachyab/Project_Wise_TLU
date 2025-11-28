# Project Wise TLU - Routes Guide

## Overview
Your Flask app is now fully connected to all HTML files organized in Phase folders. Here's a complete map of all routes and their corresponding HTML templates.

---

## **PHASE 1: Core Travel Wallet Flow**

| Route | URL | HTML File | Purpose |
|-------|-----|-----------|---------|
| `splash()` | `/` | `Phase1/1_splash_screen.html` | Landing/splash screen |
| `login()` | `/login` | `Phase1/login.html` | User login page (GET/POST) |
| `home_screen()` | `/home` | `Phase1/2_home.html` | Main home/account screen |
| `transitions()` | `/transitions` | `Phase1/3_transitions.html` | Loading/transition screen |
| `travel_mode()` | `/travel-mode` | `Phase1/4_travel_mode.html` | Travel mode activation |
| `new_travel_wallet()` | `/new-travel-wallet` | `Phase1/5_new_travel_wallet.html` | Create new travel wallet |
| `new_travel_wallet_second()` | `/new-travel-wallet-second` | `Phase1/6_new_travel_wallet_second.html` | Second step of wallet creation |
| `travel_wallet_details()` | `/travel-wallet-details` | `Phase1/7_japan_travel_wallet.html` | View wallet details & transactions |
| `travel_hub()` | `/travel-hub` | `Phase1/8_travel_hub_guide.html` | Travel hub guide |
| `pre_trip()` | `/pre-trip` | `Phase1/9_pre_trip.html` | Pre-trip planning |
| `notifications()` | `/notifications` | `Phase1/10_notifications.html` | Notifications list |

---

## **PHASE 2: OS Notifications & Modals**

| Route | URL | HTML File | Purpose |
|-------|-----|-----------|---------|
| `os_notification()` | `/os-notification` | `Phase2/1_os_notification.html` | OS notification display |
| `travel_mode_activation_modal()` | `/travel-mode-activation-modal` | `Phase2/2_travel_mode_activation_modal.html` | Travel mode activation modal |

---

## **PHASE 3: Trip Ended Notifications**

| Route | URL | HTML File | Purpose |
|-------|-----|-----------|---------|
| `travel_mode_on()` | `/travel-mode-on` | `Phase3/1_travel_mode_on.html` | Travel mode active screen |
| `trip_notification()` | `/trip-notification` | `Phase3/2_os_notification.html` | In-trip notification |
| `trip_ended()` | `/trip-ended` | `Phase3/3_os_notification_end.html` | Trip ended notification |

---

## **PHASE 4: Summary**

| Route | URL | HTML File | Purpose |
|-------|-----|-----------|---------|
| `trip_summary()` | `/trip-summary` | `Phase4/1_summary.html` | Trip summary/report screen |

---

## **Travel Wallet Management Routes**

| Route | URL | Method | HTML File | Purpose |
|-------|-----|--------|-----------|---------|
| `travel_wallets_list()` | `/travel/wallets` | GET | `Phase1/5_new_travel_wallet.html` | List all user wallets |
| `travel_wallet_new()` | `/travel/wallets/new` | GET/POST | `Phase1/5_new_travel_wallet.html` | Create new wallet form |
| `travel_wallet_detail()` | `/travel/wallets/<id>` | GET | `Phase1/7_japan_travel_wallet.html` | View specific wallet details |
| `travel_wallet_add_tx()` | `/travel/wallets/<id>/transactions/add` | POST | - | Add transaction to wallet |

---

## **Authentication Routes**

| Route | URL | Method | Purpose |
|-------|-----|--------|---------|
| `login()` | `/login` | GET/POST | Handle user login |
| `logout()` | `/logout` | GET | Clear session and redirect to login |

---

## **How to Use**

### Starting the App
```bash
python APP.py
```
The app will run at `http://localhost:5000`

### Navigate Between Screens
- Add links in your HTML files pointing to the routes above
- Use Flask's `url_for()` function in templates:
  ```html
  <a href="{{ url_for('home_screen') }}">Home</a>
  <a href="{{ url_for('travel_mode') }}">Activate Travel Mode</a>
  ```

### Database Models
Your app includes:
- **User**: Email, password hash, home currency, relationships to accounts and wallets
- **Account**: Currency accounts per user with balance
- **TravelWallet**: Multi-trip support with budgets and date ranges
- **WalletTransaction**: Track spending in travel wallets
- **TravelState**: Current travel status per user
- **FxRate**: Exchange rates for currency conversion

---

## **Quick Navigation Examples**

Add these to your HTML buttons/links:

```html
<!-- From home screen -->
<a href="{{ url_for('travel_mode') }}">Start Travel</a>

<!-- From travel mode -->
<a href="{{ url_for('new_travel_wallet') }}">Create Wallet</a>

<!-- View wallet -->
<a href="{{ url_for('travel_wallet_detail', wallet_id=123) }}">View Details</a>

<!-- Travel hub -->
<a href="{{ url_for('travel_hub') }}">Travel Hub</a>
```

---

## **Protected Routes**
These routes check for logged-in users:
- `/home`
- `/travel-mode`
- `/new-travel-wallet`
- `/travel-wallet-details`
- `/travel-hub`
- `/pre-trip`
- `/notifications`
- `/os-notification`
- `/travel-mode-activation-modal`
- `/travel-mode-on`
- `/trip-notification`
- `/trip-ended`
- `/trip-summary`
- `/travel/wallets/*`

If not logged in, users are redirected to `/login`

---

## **Next Steps**

1. ✅ **Routes Connected**: All HTML files are now connected to Flask routes
2. **Link the HTML**: Update your HTML files with proper links using `url_for()`
3. **Add Forms**: Connect form submissions to your routes
4. **Test Navigation**: Click through all the screens to ensure smooth flow
5. **Add Session Data**: Pass real data from the database to your templates

---

## **File Structure**
```
Frontend/
├── css/
│   └── main.css
├── images/
│   └── [all images]
├── Phase1/
│   ├── 1_splash_screen.html
│   ├── 2_home.html
│   ├── 3_transitions.html
│   ├── 4_travel_mode.html
│   ├── 5_new_travel_wallet.html
│   ├── 6_new_travel_wallet_second.html
│   ├── 7_japan_travel_wallet.html
│   ├── 8_travel_hub_guide.html
│   ├── 9_pre_trip.html
│   ├── 10_notifications.html
│   └── login.html
├── Phase2/
│   ├── 1_os_notification.html
│   └── 2_travel_mode_activation_modal.html
├── Phase3/
│   ├── 1_travel_mode_on.html
│   ├── 2_os_notification.html
│   └── 3_os_notification_end.html
└── Phase4/
    └── 1_summary.html
```

---

**Last Updated**: November 28, 2025

