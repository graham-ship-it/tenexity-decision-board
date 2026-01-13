# Supabase Setup Guide for Tenexity Decision Board

This guide walks you through setting up Supabase to enable user authentication and real-time data sync.

## Step 1: Create a Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Click **"Start your project"** and sign in with GitHub
3. Click **"New project"**
4. Choose your organization
5. Enter project details:
   - **Name**: `tenexity-decision-board`
   - **Database Password**: Generate a strong password (save this!)
   - **Region**: Choose closest to your users
6. Click **"Create new project"**
7. Wait for project to finish setting up (~2 minutes)

## Step 2: Create Database Tables

1. Go to **SQL Editor** in the left sidebar
2. Click **"New query"**
3. Paste the following SQL and click **"Run"**:

```sql
-- Profiles table (extends auth.users)
CREATE TABLE profiles (
    id UUID REFERENCES auth.users(id) PRIMARY KEY,
    email TEXT,
    display_name TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Profiles policies
CREATE POLICY "Users can view all profiles" ON profiles
    FOR SELECT USING (true);

CREATE POLICY "Users can update own profile" ON profiles
    FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can insert own profile" ON profiles
    FOR INSERT WITH CHECK (auth.uid() = id);

-- Boards table
CREATE TABLE boards (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL,
    owner_id UUID REFERENCES auth.users(id),
    invite_code TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE boards ENABLE ROW LEVEL SECURITY;

-- Board members table
CREATE TABLE board_members (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    board_id UUID REFERENCES boards(id) ON DELETE CASCADE,
    user_id UUID REFERENCES auth.users(id),
    email TEXT,
    joined_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(board_id, user_id)
);

ALTER TABLE board_members ENABLE ROW LEVEL SECURITY;

-- Topics table
CREATE TABLE topics (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    board_id UUID REFERENCES boards(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'open',
    due_date DATE,
    created_by UUID REFERENCES auth.users(id),
    contributions JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE topics ENABLE ROW LEVEL SECURITY;

-- Board policies
CREATE POLICY "Members can view boards" ON boards
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM board_members
            WHERE board_members.board_id = boards.id
            AND board_members.user_id = auth.uid()
        )
        OR invite_code IS NOT NULL  -- Allow viewing for joining
    );

CREATE POLICY "Users can create boards" ON boards
    FOR INSERT WITH CHECK (auth.uid() = owner_id);

CREATE POLICY "Members can update boards" ON boards
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM board_members
            WHERE board_members.board_id = boards.id
            AND board_members.user_id = auth.uid()
        )
    );

-- Board members policies
CREATE POLICY "Members can view board members" ON board_members
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM board_members bm
            WHERE bm.board_id = board_members.board_id
            AND bm.user_id = auth.uid()
        )
    );

CREATE POLICY "Users can join boards" ON board_members
    FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Topics policies
CREATE POLICY "Members can view topics" ON topics
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM board_members
            WHERE board_members.board_id = topics.board_id
            AND board_members.user_id = auth.uid()
        )
    );

CREATE POLICY "Members can create topics" ON topics
    FOR INSERT WITH CHECK (
        EXISTS (
            SELECT 1 FROM board_members
            WHERE board_members.board_id = topics.board_id
            AND board_members.user_id = auth.uid()
        )
    );

CREATE POLICY "Members can update topics" ON topics
    FOR UPDATE USING (
        EXISTS (
            SELECT 1 FROM board_members
            WHERE board_members.board_id = topics.board_id
            AND board_members.user_id = auth.uid()
        )
    );

CREATE POLICY "Members can delete topics" ON topics
    FOR DELETE USING (
        EXISTS (
            SELECT 1 FROM board_members
            WHERE board_members.board_id = topics.board_id
            AND board_members.user_id = auth.uid()
        )
    );

-- Enable realtime for topics
ALTER PUBLICATION supabase_realtime ADD TABLE topics;
```

## Step 3: Configure Authentication

1. Go to **Authentication** in the left sidebar
2. Click **Providers** tab
3. Ensure **Email** is enabled
4. Click on **Email** to configure:
   - **Enable Email Signup**: ON
   - **Confirm email**: OFF (for easier testing, turn ON for production)
   - **Enable Magic Link**: ON (should be on by default)
5. Click **Save**

### Configure Site URL

1. Go to **Authentication** → **URL Configuration**
2. Set **Site URL** to your app URL:
   - For local testing: `http://localhost:3000` or `file://`
   - For production: Your actual domain
3. Add to **Redirect URLs**:
   - `http://localhost:3000`
   - Your production URL

## Step 4: Get Your API Credentials

1. Go to **Project Settings** (gear icon in sidebar)
2. Click **API** in the left menu
3. Copy these values:
   - **Project URL** (looks like `https://xxxxx.supabase.co`)
   - **anon public** key (the longer one starting with `eyJ...`)

## Step 5: Update the Application

1. Open `tenexity-decision-board.html` in a text editor
2. Find this section near the top (around line 40):

```javascript
const SUPABASE_URL = 'YOUR_SUPABASE_URL';
const SUPABASE_ANON_KEY = 'YOUR_SUPABASE_ANON_KEY';
```

3. Replace with your actual values:

```javascript
const SUPABASE_URL = 'https://your-project-id.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...your-key';
```

4. Save the file

## Step 6: Test the Application

1. Open `tenexity-decision-board.html` in your browser
2. Enter your email address
3. Check your email for the magic link (check spam folder too)
4. Click the link to sign in
5. Set your display name
6. Create your first board!

## Inviting Nick

Once signed in with a board created:

1. Click **"+ Invite Cofounder"**
2. Share the invite link or code with Nick
3. Nick opens the link, enters his email
4. After signing in, Nick is automatically added to your board

## Hosting Options

### Option 1: Vercel (Recommended, Free)

1. Create a GitHub repo with your HTML file
2. Sign up at [vercel.com](https://vercel.com)
3. Import your GitHub repo
4. Deploy!

### Option 2: Netlify (Free)

1. Go to [netlify.com](https://netlify.com)
2. Drag and drop your HTML file
3. Get your URL!

### Option 3: GitHub Pages (Free)

1. Create a GitHub repo
2. Go to Settings → Pages
3. Enable GitHub Pages from main branch

## Troubleshooting

### "Invalid API key"
- Double-check you're using the **anon** key, not the service role key
- Ensure no extra spaces in the key

### "Magic link not received"
- Check spam folder
- Verify email in Authentication → Users
- Check if "Confirm email" is enabled (disable for testing)

### "Permission denied"
- Run the SQL setup again
- Check that Row Level Security policies are correct
- Ensure user is properly added to board_members

### Real-time updates not working
- Verify topics table is added to realtime publication
- Check browser console for WebSocket errors

## Security Notes

- The `anon` key is safe to expose in client-side code
- Row Level Security (RLS) protects your data
- Never expose the `service_role` key in client code

## Next Steps

For production:
1. Enable email confirmation in Auth settings
2. Set up custom email templates (Authentication → Email Templates)
3. Configure a custom domain
4. Enable additional auth providers (Google, etc.) if desired

---

## Need Help?

- [Supabase Documentation](https://supabase.com/docs)
- [Supabase Discord](https://discord.supabase.com)
- [Supabase GitHub](https://github.com/supabase/supabase)
