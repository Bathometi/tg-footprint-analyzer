# TG-Footprint-Analyzer 🔍

A lightweight Python CLI tool built on **Telethon** for collecting Telegram user profile metadata available to an authenticated account session.

---

## 📌 Features

- **Session-Based Extraction:** Collects basic profile information (User ID, Name, Username, Bio, Phone number) as returned to the authenticated Telegram session.
- **Telegram Flags:** Displays official Telegram-provided `scam` and `fake` flags.
- **Profile Photo DC:** Identifies the Datacenter ID associated with the target's current profile picture.
- **Common Chats:** Collects shared chats returned to the authenticated session.
- **JSON Export:** Saves structured findings into a local JSON report. Reports may contain sensitive account metadata and are excluded from Git via `.gitignore`.

---

## 🛠️ Installation & Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Bathometi/tg-footprint-analyzer.git
   cd tg-footprint-analyzer
