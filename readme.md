
# 🧹 AI Telegram Spam Channel Cleaner

Automate the cleanup of spam, crypto, and unwanted channels from your **personal Telegram account** using Machine Learning — safely and responsibly.

---

## 📌 Overview
Telegram users are often added to spam channels without consent. This project automatically identifies and leaves such channels using rule-based filters and an ML model.

---

## 🚨 Problem
- Forced additions to spam channels  
- Chat clutter  
- Manual cleanup is slow  

---

## 💡 Solution
A 3-layer spam detection system:
1. **Whitelist Protection**
2. **Keyword Blacklist**
3. **Machine Learning Spam Scoring**

---

## ⚙️ Prerequisites
- Python 3.8+
- Telegram API ID & Hash

---

## 🚀 Installation

```bash
git clone https://github.com/YOUR_USERNAME/Telegram-Spam-Cleaner.git
cd Telegram-Spam-Cleaner
pip install -r requirements.txt
```

---

## 🔧 Configuration

Rename `config_example.py` to `config.py` and edit:

```python
api_id = 123456
api_hash = "your_api_hash"

SPAM_THRESHOLD = 0.75
MESSAGE_CHECK_LIMIT = 10
MAX_LEAVES_PER_RUN = 15
DELAY_SECONDS = 30

SAFE_CHANNELS = ["Family", "Movies", "Work"]
```

---

## ▶️ How to Run

```bash
python telegram_cleaner.py
```

First run will ask for:
- Phone number (+country code)
- OTP
- 2FA password (if enabled)

---

## 📊 Logs
Left channels are logged in `leave_log.txt`.

---

## 🛡️ Safety Tips
- Do not exceed 15 leaves per run
- Run twice a day max
- Respect Telegram ToS

---

## 📂 Project Structure

```
telegram_cleaner.py
spam_detector.py
config.py
requirements.txt
leave_log.txt
model/
```

---

## ⚠️ Disclaimer
Use at your own risk. Excessive automation can lead to restrictions.

---

## 📜 License
MIT License
