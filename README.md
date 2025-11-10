

# 🎵 TopTen_InSpotify

A **Python-based web application** that connects to the **Spotify Web API** to fetch and display your **Top 10 most listened tracks and artists**.

Built using **Flask**, this project demonstrates how to:

* Integrate third-party APIs (Spotify)
* Handle user authentication (OAuth 2.0)
* Visualize personalized music data

---

## 🚀 Features

* 🔐 **Spotify OAuth 2.0 Authentication** — Secure login using your Spotify account
* 🎧 **Fetch Top 10 Tracks and Artists** from your Spotify profile
* 📊 **Clean and responsive UI** to display personalized music stats
* 🧠 **Demonstrates REST API calls**, token handling, and Flask routing
* ⚙️ **Well-structured and easy to extend**

---

## 🛠 Tech Stack

| Component             | Technology Used         |
| --------------------- | ----------------------- |
| **Backend Framework** | Flask (Python)          |
| **API Used**          | Spotify Web API         |
| **Authentication**    | OAuth 2.0               |
| **Frontend**          | HTML, CSS, Bootstrap    |
| **Libraries**         | requests, python-dotenv |

---

## ⚙️ How It Works

1. User logs in with their **Spotify account**
2. The app redirects to Spotify’s authentication page
3. After login, Spotify redirects back to the app with an authorization code
4. Flask exchanges that code for an **access token**
5. The app uses the token to fetch the user’s **Top 10 Tracks** and **Top 10 Artists**

---

## 🧩 Setup Instructions

1. **Clone the repository**

   ```bash
   git clone https://github.com/Spoorthiks6/TopTen_InSpotify.git
   cd TopTen_InSpotify
   ```

2. **Create and activate a virtual environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate      # Mac/Linux  
   venv\Scripts\activate         # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** in the root directory and add:

   ```env
   SPOTIFY_CLIENT_ID=your_client_id
   SPOTIFY_CLIENT_SECRET=your_client_secret
   SPOTIFY_REDIRECT_URI=http://localhost:5000/callback
   SECRET_KEY=your_flask_secret_key
   ```

5. **Run the Flask app**

   ```bash
   python app.py
   ```

6. Open your browser and go to:

   ```
   http://localhost:5000
   ```

---

## 👩‍💻 Author

**Spoorthi K S**
🎓 4th Semester CSE Student | VTU
📍 Mysuru, Karnataka
💼 [GitHub Profile](https://github.com/Spoorthiks6)
