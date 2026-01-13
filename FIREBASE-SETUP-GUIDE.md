# Firebase Setup Guide for Cofounder Decision Board

This guide walks you through setting up Firebase to enable user authentication and real-time data sync for your Decision Board.

## Step 1: Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click **"Create a project"**
3. Enter a project name (e.g., "cofounder-board")
4. Optionally enable Google Analytics (not required)
5. Click **"Create project"**

## Step 2: Enable Authentication

1. In your Firebase project, go to **Build → Authentication**
2. Click **"Get started"**
3. Go to the **"Sign-in method"** tab
4. Click **"Email/Password"**
5. Enable **"Email/Password"** (first toggle)
6. Enable **"Email link (passwordless sign-in)"** (second toggle)
7. Click **"Save"**

### Configure Authorized Domains

1. Still in Authentication, go to **"Settings"** tab
2. Under **"Authorized domains"**, add any domains where you'll host the app
   - `localhost` is already added by default for testing
   - Add your production domain if deploying

## Step 3: Create Firestore Database

1. Go to **Build → Firestore Database**
2. Click **"Create database"**
3. Choose **"Start in production mode"** (we'll add rules next)
4. Select a location closest to your users
5. Click **"Enable"**

### Set Firestore Security Rules

1. In Firestore, go to the **"Rules"** tab
2. Replace the default rules with:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users can read/write their own profile
    match /users/{userId} {
      allow read, write: if request.auth != null && request.auth.uid == userId;
      allow read: if request.auth != null;
    }

    // Board access - members only
    match /boards/{boardId} {
      allow read, write: if request.auth != null &&
        request.auth.uid in resource.data.members;
      allow create: if request.auth != null;

      // Allow reading board by invite code (for joining)
      allow read: if request.auth != null;

      // Topics within boards
      match /topics/{topicId} {
        allow read, write: if request.auth != null &&
          request.auth.uid in get(/databases/$(database)/documents/boards/$(boardId)).data.members;
      }
    }
  }
}
```

3. Click **"Publish"**

## Step 4: Get Your Firebase Configuration

1. Go to **Project Settings** (gear icon in the top left)
2. Scroll down to **"Your apps"**
3. Click the **"</>"** (Web) icon to add a web app
4. Enter an app nickname (e.g., "decision-board-web")
5. Don't check "Firebase Hosting" for now
6. Click **"Register app"**
7. You'll see a code snippet with your config. Copy these values:

```javascript
const firebaseConfig = {
  apiKey: "AIza...",
  authDomain: "your-project.firebaseapp.com",
  projectId: "your-project-id",
  storageBucket: "your-project.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abc123"
};
```

## Step 5: Update the Decision Board Code

1. Open `cofounder-board-v2.html` in a text editor
2. Find this section near the top (around line 30):

```javascript
const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_PROJECT.firebaseapp.com",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_PROJECT.appspot.com",
    messagingSenderId: "YOUR_SENDER_ID",
    appId: "YOUR_APP_ID"
};
```

3. Replace with your actual Firebase config values
4. Save the file

## Step 6: Test Locally

1. Open `cofounder-board-v2.html` in your browser
2. Enter your email address
3. Check your email for the magic link
4. Click the link to sign in
5. Create your first board!

## Inviting Nick

Once you're signed in and have created a board:

1. Click the green **"+ Invite Cofounder"** button
2. You'll see two options:

### Option A: Share Invite Link
- Copy the invite link and send it to Nick via text, email, or chat
- When Nick clicks the link, he'll be prompted to sign in with his email
- After signing in, he'll automatically join your board

### Option B: Share Invite Code
- Share the 8-character code with Nick
- Nick goes to the app URL, signs in, and enters the code when prompted

## Hosting Options

### Free Hosting with Firebase Hosting

1. Install Firebase CLI: `npm install -g firebase-tools`
2. Login: `firebase login`
3. Initialize: `firebase init hosting`
4. Deploy: `firebase deploy --only hosting`

### Other Options
- **GitHub Pages** - Free, simple static hosting
- **Vercel** - Free tier, great for web apps
- **Netlify** - Free tier with forms and functions

## Troubleshooting

### "Magic link not received"
- Check your spam folder
- Ensure email is correct
- Wait a few minutes - sometimes there's a delay

### "Invalid invite code"
- Codes are case-insensitive but must match exactly
- Ask your cofounder to regenerate the invite

### "Permission denied" errors
- Make sure Firestore rules are published
- Both users must be authenticated
- The inviting user must have added the invited user to the board

## Optional: Email Invites via Cloud Functions

For automatic email invites, you'd need to set up Firebase Cloud Functions. Here's a basic template:

```javascript
// functions/index.js
const functions = require('firebase-functions');
const nodemailer = require('nodemailer');

exports.sendInviteEmail = functions.https.onCall(async (data, context) => {
  const { email, inviteLink, boardName, inviterName } = data;

  // Configure your email service (Gmail, SendGrid, etc.)
  const transporter = nodemailer.createTransporter({...});

  await transporter.sendMail({
    to: email,
    subject: `${inviterName} invited you to collaborate on ${boardName}`,
    html: `<p>Click here to join: <a href="${inviteLink}">${inviteLink}</a></p>`
  });

  return { success: true };
});
```

This requires a paid Firebase plan (Blaze) for external network calls.

---

## Need Help?

- [Firebase Documentation](https://firebase.google.com/docs)
- [Firestore Guides](https://firebase.google.com/docs/firestore)
- [Firebase Auth Guides](https://firebase.google.com/docs/auth)
