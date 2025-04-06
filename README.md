# HTB Writeup Downloader

📥 A Python script to automatically download **writeup PDFs** for Hack The Box (HTB) machines based on their IDs. The writeups are organized by difficulty level (Easy, Medium, Hard, Insane). Useful for documentation, learning, or personal archive.

---

## 🚀 Features

- Downloads writeup PDFs via the official HTB API.
- Automatically categorizes writeups by difficulty.
- Skips files that are already downloaded.
- Handles rate limiting (HTTP 429) with exponential backoff.
- Gracefully handles DNS and parsing errors.

---

## 🔧 Requirements

- Python 3.6+
- Stable internet connection
- HTB Authorization Token (can be obtained from your browser after logging in)

---

## 🔮 Next Development

- 🔐 HTB Login Integration: Add support for logging in with your username and password to automatically fetch the bearer token.
- ♻️ Bearer Token Refresh: Automatically refresh expired tokens using stored credentials or refresh tokens.
- 🧩 CLI Options: Add support for arguments like --start-id, --end-id, --delay, etc.
- 💾 Resume Support: Continue from the last downloaded ID in case of interruption.
- 📊 Progress Indicator: Show download progress and current status.
---



## 📦 Installation

```bash
git clone https://github.com/yourusername/htb-writeup-downloader.git
cd htb-writeup-downloader
pip install requests