# Kick Points Farm 🎯

Automatically farm points on Kick.com

## Installation

```bash
pip install curl-cffi rnet loguru
```

## Setup

1. **Get your Kick.com token:**
   - Open [kick.com](https://kick.com) and login
   - Press **F12** (Developer Tools)
   - Go to **Network** tab
   - Refresh the page (**F5**)
   - Find any request to `kick.com`
   - In **Headers** find: `Authorization: Bearer YOUR_TOKEN`
   - Copy the token (without "Bearer ")

2. **Edit `config.json`:**
```json
{
    "Private": {
        "token": "YOUR_TOKEN_HERE"
    },
    "Streamers": [
        {
            "name": "streamer_name",
            "chat_message": "[emote:37226:KEKW]",
            "chat_interval_minutes": 30
        }
    ]
}
```

## Usage

**Start:**
```bash
python main.py
```

**Stop:** `Ctrl+C`

## Features

- ✅ Farm points automatically
- ✅ Send chat messages
- ✅ Monitor points balance
- ✅ Auto-reconnect on disconnect

---

**Disclaimer:** Use at your own risk. May violate Kick.com ToS.
