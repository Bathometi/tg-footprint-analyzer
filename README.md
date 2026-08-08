# TG-Footprint-Analyzer 🔍

A lightweight Python CLI tool built on **Telethon** for collecting Telegram user profile metadata available to an authenticated account session.

This project is an educational OSINT prototype focused on structured data collection, evidence accuracy, and responsible handling of potentially sensitive metadata.

---

## 📌 Features

- **Session-Based Extraction:** Collects basic profile information such as User ID, Name, Username, Bio, and Phone number when returned to the authenticated Telegram session.
- **Telegram Flags:** Displays official Telegram-provided `scam` and `fake` account flags.
- **Profile Photo DC:** Identifies the Datacenter ID associated with the target's current profile picture.
- **Common Chats:** Collects shared chats returned to the authenticated session.
- **Profile Photo Download:** Can download the current profile photo when available.
- **JSON Export:** Saves structured findings into a local JSON report.
- **Text Summary:** Generates a human-readable TXT summary of the collected metadata.

Generated reports may contain sensitive account metadata and are excluded from Git via `.gitignore`.

---

## 🛠️ Installation & Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Bathometi/tg-footprint-analyzer.git
   cd tg-footprint-analyzer
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv venv
   ```

   Linux / macOS:

   ```bash
   source venv/bin/activate
   ```

   Windows:

   ```bash
   venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

---

## ⚙️ Configuration

Create a `.env` file in the project directory.

You can use `.env.example` as a template:

```env
TG_API_ID=your_api_id
TG_API_HASH=your_api_hash
```

Do not commit real Telegram API credentials or session files.

The analyzer uses a local Telethon session named:

```text
footprint_session
```

Session files are excluded from Git via `.gitignore`.

---

## ▶️ Usage

Run the analyzer with a Telegram username:

```bash
python analyzer.py @username
```

A Telegram ID can also be provided as the target when supported by the current authenticated session:

```bash
python analyzer.py 123456789
```

To run the analyzer without downloading the profile photo:

```bash
python analyzer.py @username --no-photo
```

The analyzer generates local output files:

```text
report_<telegram_id>.json
summary_<telegram_id>.txt
```

If profile photo downloading is enabled and a photo is available, it is stored inside:

```text
downloads/
```

Generated reports and downloaded media are excluded from Git.

---

## 📂 Output

The JSON report may include:

- Telegram User ID
- First and last name
- Username
- Phone field returned to the authenticated session
- Bio
- Bot status
- Verification status
- Restriction status
- Premium status
- Telegram-provided `scam` and `fake` flags
- Profile Photo DC ID
- Common chats returned to the session
- Profile photo download path

A missing value should not automatically be interpreted as hidden, private, or unavailable.

For example, if the phone field is not returned, the tool reports that it was:

```text
Not returned to the current session
```

rather than assuming why the value is missing.

---

## 🔐 Privacy, OpSec & Limitations

- The tool only collects metadata returned to the authenticated Telegram session.
- Available information may differ depending on account permissions, privacy settings, Telegram behavior, and the relationship between accounts.
- Missing information should not automatically be interpreted as hidden or intentionally restricted.
- `scam` and `fake` are Telegram-provided account flags. They are **not** an independent risk assessment performed by this tool.
- The Profile Photo DC refers to the Datacenter ID associated with the profile photo and should not be interpreted as the physical location or infrastructure location of the user.
- Common chats are relationships returned to the authenticated session. Their presence alone does not prove a meaningful relationship between accounts.
- Generated JSON/TXT reports and downloaded media may contain sensitive metadata and should not be committed to public repositories.
- `.env`, Telegram session files, generated reports, and downloaded media are excluded through `.gitignore`.
- Sensitive output was removed from the reachable Git history during project cleanup, and `.gitignore` rules were added to reduce the risk of similar files being committed again.
- Credentials exposed during development should be treated as compromised and rotated.
- Collected metadata should be treated as evidence, not automatic attribution.

---

## ⚠️ Responsible Use

This project is intended for **educational OSINT research and controlled testing**.

It should not be used to claim that multiple accounts belong to the same person based only on usernames, profile information, shared chats, or other individual indicators.

**Correlation is not attribution.**

Use the tool responsibly and respect applicable privacy, legal, and platform requirements.

---

## 📚 Project Status

**Educational prototype — v1.0**

The current version demonstrates:

- Telegram API interaction through Telethon
- authenticated-session metadata collection
- structured JSON reporting
- basic relationship collection through common chats
- local evidence handling
- environment-based credential management
- Git/OpSec practices for sensitive output

The project is not intended to be a production-ready OSINT platform or an automated identity attribution system.
