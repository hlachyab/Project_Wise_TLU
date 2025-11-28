# 🎨 HTML Snippets with Proper Connections

Copy and paste these code snippets into your HTML files to connect them properly to Flask.

---

## 1️⃣ Splash Screen (Phase1/1_splash_screen.html)

```html
<div class="splash-buttons">
    <!-- Login Button -->
    <a href="{{ url_for('login') }}" class="btn btn-primary">
        Login
    </a>
    
    <!-- Demo: Go to Home -->
    <a href="{{ url_for('home_screen') }}" class="btn btn-secondary">
        Demo Home
    </a>
</div>
```

---

## 2️⃣ Login Page (Phase1/login.html)

```html
<form method="POST" action="{{ url_for('login') }}" class="login-form">
    <input 
        type="email" 
        name="email" 
        placeholder="Enter your email" 
        required
    >
    
    <input 
        type="password" 
        name="password" 
        placeholder="Enter your password" 
        required
    >
    
    <button type="submit" class="btn btn-primary">
        Login
    </button>
    
    <p class="form-hint">
        Demo: demo@wise.com / demo123
    </p>
</form>

<!-- Flash messages -->
{% with messages = get_flashed_messages() %}
    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-error">
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
{% endwith %}
```

---

## 3️⃣ Home Screen (Phase1/2_home.html)

```html
<div class="header">
    <div class="greeting">
        Welcome, {{ user.email }}!
    </div>
    
    <button class="logout-btn" onclick="location.href='{{ url_for('logout') }}'">
        Logout
    </button>
</div>

<div class="main-buttons">
    <!-- Start Travel Mode -->
    <a href="{{ url_for('travel_mode') }}" class="btn btn-large">
        <span class="icon">✈️</span>
        Activate Travel Mode
    </a>
    
    <!-- View Travel Hub -->
    <a href="{{ url_for('travel_hub') }}" class="btn btn-large">
        <span class="icon">🗺️</span>
        Travel Hub
    </a>
    
    <!-- Pre-trip Planning -->
    <a href="{{ url_for('pre_trip') }}" class="btn btn-large">
        <span class="icon">📋</span>
        Pre-trip Planning
    </a>
    
    <!-- Notifications -->
    <a href="{{ url_for('notifications') }}" class="btn btn-large">
        <span class="icon">🔔</span>
        Notifications
    </a>
    
    <!-- My Wallets -->
    <a href="{{ url_for('travel_wallets_list') }}" class="btn btn-large">
        <span class="icon">💼</span>
        My Wallets
    </a>
</div>

<!-- Accounts Section -->
<div class="accounts-section">
    <h3>Your Accounts</h3>
    {% for account in accounts %}
        <div class="account-card">
            <div class="currency">{{ account.currency }}</div>
            <div class="balance">{{ "%.2f"|format(account.balance) }}</div>
        </div>
    {% endfor %}
</div>

<!-- Current Travel State -->
{% if travel_state %}
    <div class="travel-state-card">
        <h4>Currently Traveling:</h4>
        <p><strong>Country:</strong> {{ travel_state.current_country }}</p>
        <p><strong>Currency:</strong> {{ travel_state.local_currency }}</p>
    </div>
{% endif %}
```

---

## 4️⃣ Travel Mode Activation (Phase1/4_travel_mode.html)

```html
<form method="POST" action="{{ url_for('travel_activate') }}" class="travel-form">
    <h2>Activate Travel Mode</h2>
    
    <label>Select Destination Country:</label>
    <select name="country" required>
        <option value="">-- Choose Country --</option>
        <option value="JP">Japan (JPY)</option>
        <option value="HU">Hungary (HUF)</option>
        <option value="TR">Turkey (TRY)</option>
        <option value="GB">United Kingdom (GBP)</option>
        <option value="US">United States (USD)</option>
        <option value="PL">Poland (PLN)</option>
        <option value="EE">Estonia (EUR)</option>
    </select>
    
    <button type="submit" class="btn btn-primary btn-large">
        Activate Travel Mode
    </button>
</form>

<div class="navigation">
    <!-- Back to Home -->
    <a href="{{ url_for('home_screen') }}" class="btn-back">
        ← Back to Home
    </a>
</div>
```

---

## 5️⃣ New Travel Wallet Step 1 (Phase1/5_new_travel_wallet.html)

```html
<form method="POST" action="{{ url_for('travel_wallet_new') }}" class="wallet-form">
    <h2>Create New Travel Wallet</h2>
    
    <div class="form-group">
        <label>Wallet Name:</label>
        <input 
            type="text" 
            name="name" 
            placeholder="e.g., Japan 2025" 
            required
        >
    </div>
    
    <div class="form-group">
        <label>Destination Country:</label>
        <select name="country_code" required>
            <option value="">-- Choose --</option>
            <option value="JP">Japan</option>
            <option value="PL">Poland</option>
            <option value="HU">Hungary</option>
            <option value="TR">Turkey</option>
            <option value="GB">United Kingdom</option>
        </select>
    </div>
    
    <div class="form-group">
        <label>Currency:</label>
        <select name="currency" required>
            <option value="">-- Choose --</option>
            <option value="JPY">JPY (Japan)</option>
            <option value="PLN">PLN (Poland)</option>
            <option value="HUF">HUF (Hungary)</option>
            <option value="TRY">TRY (Turkey)</option>
            <option value="GBP">GBP (UK)</option>
            <option value="USD">USD (USA)</option>
            <option value="EUR">EUR (Europe)</option>
        </select>
    </div>
    
    <div class="form-group">
        <label>Trip Start Date:</label>
        <input type="date" name="start_date">
    </div>
    
    <div class="form-group">
        <label>Trip End Date:</label>
        <input type="date" name="end_date">
    </div>
    
    <div class="form-group">
        <label>Soft Budget (gentle warning):</label>
        <input 
            type="number" 
            name="soft_budget" 
            step="0.01" 
            placeholder="e.g., 1000"
        >
    </div>
    
    <div class="form-group">
        <label>Hard Budget (strict cap):</label>
        <input 
            type="number" 
            name="hard_budget" 
            step="0.01" 
            placeholder="e.g., 1500"
        >
    </div>
    
    <button type="submit" class="btn btn-primary btn-large">
        Create Wallet
    </button>
</form>

<div class="navigation">
    <a href="{{ url_for('home_screen') }}" class="btn-back">
        ← Back to Home
    </a>
</div>

<!-- List of Existing Wallets -->
<div class="wallets-section">
    <h3>Your Travel Wallets</h3>
    {% if wallets %}
        {% for wallet in wallets %}
            <div class="wallet-card">
                <div class="wallet-name">{{ wallet.name }}</div>
                <div class="wallet-info">
                    <span>{{ wallet.country_code }}</span>
                    <span>{{ wallet.currency }}</span>
                </div>
                <a href="{{ url_for('travel_wallet_detail', wallet_id=wallet.id) }}" 
                   class="btn btn-small">
                    View Details
                </a>
            </div>
        {% endfor %}
    {% else %}
        <p class="empty-state">No travel wallets yet. Create one above!</p>
    {% endif %}
</div>
```

---

## 6️⃣ Wallet Details (Phase1/7_japan_travel_wallet.html)

```html
<div class="wallet-header">
    <h2>{{ wallet.name }}</h2>
    <div class="wallet-meta">
        <span>{{ wallet.country_code }}</span>
        <span>{{ wallet.currency }}</span>
        {% if wallet.start_date %}
            <span>{{ wallet.start_date }} to {{ wallet.end_date }}</span>
        {% endif %}
    </div>
</div>

<!-- Wallet Summary -->
<div class="summary-cards">
    <div class="summary-card">
        <div class="label">Pre-trip Spent</div>
        <div class="amount">{{ "%.2f"|format(summary.total_pre_trip) }} {{ user.home_currency }}</div>
    </div>
    
    <div class="summary-card">
        <div class="label">During Trip</div>
        <div class="amount">{{ "%.2f"|format(summary.total_during_trip) }} {{ user.home_currency }}</div>
    </div>
    
    <div class="summary-card">
        <div class="label">Total Spent</div>
        <div class="amount">{{ "%.2f"|format(summary.total_spent) }} {{ user.home_currency }}</div>
    </div>
</div>

<!-- Budget Warnings -->
{% if wallet.soft_budget and summary.total_spent > wallet.soft_budget %}
    <div class="alert alert-warning">
        ⚠️ You've exceeded your soft budget of {{ wallet.soft_budget }}!
    </div>
{% endif %}

{% if wallet.hard_budget and summary.total_spent > wallet.hard_budget %}
    <div class="alert alert-danger">
        🛑 You've exceeded your hard budget of {{ wallet.hard_budget }}!
    </div>
{% endif %}

<!-- Add Transaction Form -->
<div class="add-transaction">
    <h3>Add Expense</h3>
    <form method="POST" action="{{ url_for('travel_wallet_add_tx', wallet_id=wallet.id) }}">
        <input 
            type="text" 
            name="description" 
            placeholder="What did you spend on?" 
            required
        >
        
        <select name="category">
            <option value="">Category</option>
            <option value="Food">Food</option>
            <option value="Transport">Transport</option>
            <option value="Accommodation">Accommodation</option>
            <option value="Entertainment">Entertainment</option>
            <option value="Shopping">Shopping</option>
            <option value="Other">Other</option>
        </select>
        
        <input 
            type="number" 
            name="amount_local" 
            step="0.01" 
            placeholder="Amount" 
            required
        >
        
        <input type="hidden" name="currency_local" value="{{ wallet.currency }}">
        
        <label>
            <input type="checkbox" name="is_pre_trip" value="true">
            Pre-trip expense?
        </label>
        
        <button type="submit" class="btn btn-primary">
            Add Expense
        </button>
    </form>
</div>

<!-- Transactions List -->
<div class="transactions">
    <h3>Transactions</h3>
    {% if transactions %}
        <ul class="transaction-list">
            {% for tx in transactions %}
                <li class="transaction-item">
                    <div class="tx-description">
                        <strong>{{ tx.description }}</strong>
                        {% if tx.category %}
                            <span class="tx-category">{{ tx.category }}</span>
                        {% endif %}
                    </div>
                    <div class="tx-amount">
                        -{{ "%.2f"|format(tx.amount_local) }} {{ tx.currency_local }}
                    </div>
                    <div class="tx-date">{{ tx.created_at.strftime('%Y-%m-%d') }}</div>
                </li>
            {% endfor %}
        </ul>
    {% else %}
        <p class="empty-state">No transactions yet.</p>
    {% endif %}
</div>

<!-- Category Breakdown -->
{% if summary.category_totals %}
    <div class="category-breakdown">
        <h3>Spending by Category</h3>
        <div class="category-list">
            {% for category, total in summary.category_totals.items() %}
                <div class="category-item">
                    <span>{{ category }}</span>
                    <span>{{ "%.2f"|format(total) }} {{ user.home_currency }}</span>
                </div>
            {% endfor %}
        </div>
    </div>
{% endif %}

<!-- Travel Guide -->
{% if guide %}
    <div class="travel-guide">
        <h3>{{ guide.title }}</h3>
        <ul>
            {% for tip in guide.tips %}
                <li>{{ tip }}</li>
            {% endfor %}
        </ul>
    </div>
{% endif %}

<!-- Navigation -->
<div class="navigation">
    <a href="{{ url_for('travel_wallets_list') }}" class="btn btn-secondary">
        ← Back to Wallets
    </a>
    
    <a href="{{ url_for('trip_summary') }}" class="btn btn-primary">
        View Summary →
    </a>
</div>
```

---

## 7️⃣ Travel Hub (Phase1/8_travel_hub_guide.html)

```html
<div class="travel-hub">
    <h2>Travel Hub Guide</h2>
    
    <div class="hub-content">
        <!-- Your travel hub content here -->
    </div>
</div>

<div class="navigation">
    <a href="{{ url_for('home_screen') }}" class="btn-back">
        ← Back to Home
    </a>
</div>
```

---

## 8️⃣ Pre-trip Planning (Phase1/9_pre_trip.html)

```html
<div class="pre-trip">
    <h2>Pre-trip Planning</h2>
    
    <div class="planning-content">
        <!-- Your pre-trip planning content here -->
    </div>
</div>

<div class="navigation">
    <a href="{{ url_for('home_screen') }}" class="btn-back">
        ← Back to Home
    </a>
</div>
```

---

## 9️⃣ Notifications (Phase1/10_notifications.html)

```html
<div class="notifications">
    <h2>Notifications</h2>
    
    <div class="notifications-list">
        <!-- Your notifications content here -->
    </div>
</div>

<div class="navigation">
    <a href="{{ url_for('home_screen') }}" class="btn-back">
        ← Back to Home
    </a>
</div>
```

---

## 🔟 Phase 2 - OS Notification

```html
<!-- Phase2/1_os_notification.html -->
<div class="os-notification">
    <div class="notification-content">
        <!-- Your notification content here -->
    </div>
    
    <div class="notification-actions">
        <a href="{{ url_for('home_screen') }}" class="btn btn-primary">
            Go to Home
        </a>
    </div>
</div>
```

---

## 1️⃣1️⃣ Phase 4 - Trip Summary

```html
<!-- Phase4/1_summary.html -->
<div class="trip-summary">
    <h2>Trip Summary</h2>
    
    <!-- Your summary content here -->
</div>

<div class="summary-actions">
    <a href="{{ url_for('travel_wallets_list') }}" class="btn btn-secondary">
        ← Back to Wallets
    </a>
    
    <a href="{{ url_for('travel_mode') }}" class="btn btn-primary">
        Start New Trip →
    </a>
    
    <a href="{{ url_for('home_screen') }}" class="btn btn-outline">
        Home
    </a>
</div>
```

---

## 📱 Header/Navigation Component (Use in all files)

```html
<!-- Add this at the top of your main content area -->
<div class="app-header">
    <div class="header-left">
        <a href="{{ url_for('home_screen') }}" class="btn-back">
            ← Back
        </a>
    </div>
    
    <div class="header-title">
        <h1>{{ page_title }}</h1>
    </div>
    
    <div class="header-right">
        <button class="user-menu" onclick="toggleUserMenu()">
            <span>{{ user.email }}</span>
            <a href="{{ url_for('logout') }}" class="menu-item">Logout</a>
        </button>
    </div>
</div>
```

---

## ⚠️ Flash Messages (Use in all files)

```html
<!-- Add this to show success/error messages -->
{% with messages = get_flashed_messages() %}
    {% if messages %}
        <div class="flash-messages">
            {% for message in messages %}
                <div class="alert alert-info">
                    {{ message }}
                    <button onclick="this.parentElement.style.display='none';">×</button>
                </div>
            {% endfor %}
        </div>
    {% endif %}
{% endwith %}
```

---

## 🎯 Complete Page Template

Here's a complete template structure you can use as a base:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ page_title }} - Wise Travel</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
</head>
<body>
    <div class="app-container">
        <!-- Header -->
        <header class="app-header">
            <a href="{{ url_for('home_screen') }}" class="btn-back">← Back</a>
            <h1>{{ page_title }}</h1>
            <div class="user-profile">
                <span>{{ user.email }}</span>
                <a href="{{ url_for('logout') }}">Logout</a>
            </div>
        </header>
        
        <!-- Flash Messages -->
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                <div class="flash-messages">
                    {% for message in messages %}
                        <div class="alert">{{ message }}</div>
                    {% endfor %}
                </div>
            {% endif %}
        {% endwith %}
        
        <!-- Main Content -->
        <main class="app-main">
            <!-- Your page content here -->
        </main>
        
        <!-- Footer/Navigation -->
        <footer class="app-footer">
            <div class="nav-buttons">
                <a href="{{ url_for('home_screen') }}" class="btn">Home</a>
                <a href="{{ url_for('travel_mode') }}" class="btn">Travel</a>
                <a href="{{ url_for('notifications') }}" class="btn">Notifications</a>
            </div>
        </footer>
    </div>
</body>
</html>
```

---

**Start using these snippets to connect your HTML files!** 🚀


