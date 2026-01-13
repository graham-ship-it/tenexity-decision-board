# Tenexity Decision Board (Recovered)

This project has been recovered and patched to fix Supabase authentication issues.

## 🚀 How to Run

Because Supabase Authentication requires a valid web origin (it doesn't work with `file://`), you should run this using the included local server.

### 1. Start the Server
Open your terminal in this directory and run:

```bash
python3 serve.py
```

### 2. Open the App
Go to your browser and visit:

[http://localhost:3000/tenexity-decision-board.html](http://localhost:3000/tenexity-decision-board.html)

---

## 🔧 Developer Mode (Bypass Login)

If you just want to test the UI without setting up Supabase:

1. Open the app as described above.
2. On the login screen, click the **"🔧 Bypass Login (Developer Mode)"** button.
3. This will log you in as a dummy "Developer" user and let you create/manage boards immediately.

---

## 🔑 Fixing Supabase Auth (Real Login)

To make the real email magic links work:

1. Go to your [Supabase Dashboard](https://supabase.com/dashboard).
2. Navigate to **Authentication** -> **URL Configuration**.
3. Under **Redirect URLs**, add: `http://localhost:3000`
4. Save changes.

Now you can use the real email login flow!
