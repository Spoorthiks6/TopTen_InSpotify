

# 🎵 Spotify Top 10 Tracks — Flask App

A Python web application built using **Flask** and **Spotipy** that connects to the **Spotify Web API** to fetch and display a user’s **Top 10 most listened tracks**.

It demonstrates **OAuth 2.0 authentication**, secure token handling, and clean integration with Spotify’s APIs — all wrapped in a simple, minimal UI.

---

## 🚀 Features

* 🔐 **Spotify Login (OAuth 2.0)** – Secure login via Spotify account
* 🎧 **Fetch Top 10 Tracks** from your Spotify listening history
* 🔄 **Dynamic session management** with cached tokens per user
* 🧹 **Logout / Switch User** functionality
* ⚙️ **Simple Flask-based backend** for easy customization

---

## 🧩 Tech Stack

| Component                  | Technology              |
| -------------------------- | ----------------------- |
| **Backend Framework**      | Flask                   |
| **Spotify API Wrapper**    | Spotipy                 |
| **Authentication**         | OAuth 2.0               |
| **Environment Management** | python-dotenv           |
| **Frontend**               | Basic HTML + Inline CSS |

---

## 🛠️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Spoorthiks6/Spotify-Top10-Flask.git
cd Spotify-Top10-Flask
```

### 2️⃣ Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

> If you don’t have a `requirements.txt`, create one with:
>
> ```bash
> Flask
> spotipy
> python-dotenv
> ```

---

## 🎧 4️⃣ Spotify Developer Setup

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Click **“Create an App”**
3. Copy the **Client ID** and **Client Secret**
4. Add a Redirect URI:

   ```
   http://127.0.0.1:5000/callback
   ```

---

## 🔑 5️⃣ Add Environment Variables

Create a `.env` file in your project root with:

```env
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REDIRECT_URI=http://127.0.0.1:5000/callback
```

---

## ▶️ 6️⃣ Run the App

```bash
python app.py
```

Then open your browser and visit:
👉 [http://127.0.0.1:5000](http://127.0.0.1:5000)

---
## 👩‍💻 Author

**Spoorthi K S**
🎓 4th Semester CSE | VTU
📍 Mysuru, Karnataka
💼 [GitHub](https://github.com/Spoorthiks6)
