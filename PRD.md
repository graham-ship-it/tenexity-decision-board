# Product Requirements Document (PRD): Tenexity Decision Board

> [!NOTE]
> This document defines the requirements for the Tenexity Decision Board. It has been updated to reflect specific user needs regarding authentication, visualization, agent behavior, and task management.

## 1. Executive Summary
The **Tenexity Decision Board** is an asynchronous decision-making platform designed to help teams make better decisions faster. It moves discussions out of chaotic chat threads and into a structured "Board" where topics can be debated using **Facts**, **Opinions**, and **Preferences**.

A key differentiator is the **Tenexity Agent**, a background service that monitors email inboxes, uses **Claude AI** to extract decision topics automatically, and posts them to the board.

## 2. User Personas
*   **The Decision Maker**: Needs clear visibility into team sentiment, facts, and final outcomes.
*   **The Contributor**: Adds facts/opinions via text or voice.
*   **The Email User**: Forwards emails to the system to initiate decisions without logging in.

## 3. Functional Requirements

### 3.1. Frontend Information Architecture
*   **Authentication & IAM**:
    *   **Dual Login Methods**: Support both Magic Link and standard Email/Password authentication via Supabase.
    *   **Developer Mode**: Offline/local testing capability.
*   **Dashboard & Navigation**:
    *   **Board Sorting**: Users can sort their list of boards (e.g., by recent activity, name).
    *   **Reminders**: In-app pop-up reminders for due decisions when logged in.
    *   **Archives**: A dedicated separate tab/view for "Decided" topics to keep the main board clean.
*   **Board Visualization**:
    *   **View Switcher**: Toggle between:
        *   **List View**: Linear, detailed view for scanning content.
        *   **Kanban View**: Column-based view (Suggested -> Open -> Pending -> Decided) for workflow management.
*   **Todo List Hub**:
    *   **Dedicated Tab**: A distraction-free "Todo" tab separate from the main board views.
    *   **Project Grouping**: Todos are automatically grouped by Project/Board name.
    *   **Review Flow**: Simple interface to check off items or click through to the relevant context.
*   **Topic Detail**:
    *   Structured debate with `Fact`, `Opinion`, `Preference` categorization.
    *   Integrated Voice Notes.

### 3.2. Background Agent & Email Logic
*   **Email Watcher Control**:
    *   **Master Toggle**: Ability for the user to turn the Email Watcher ON or OFF globally or per board.
*   **Smart Routing (Receipt Mechanism)**:
    *   **Forward-to-App**: Users can forward emails to a dedicated address.
    *   **Logic**: The system must route the email to the correct board based on the sender's address or a tag in the subject line (e.g., `[ProjectX]`).
*   **AI Engine**:
    *   **Provider**: **Claude LLM** (Anthropic) for high-quality parsing and summarization.
    *   **Extraction**: Parse emails to extract Title, Description, Facts, Opinions, and Preferences.

## 4. Technical Architecture

### 4.1. Stack
*   **Frontend**: React (Single File / Standalone for now, potential migration to Vite).
*   **Backend Agent**: Python script running as a daemon.
*   **Database**: Supabase (PostgreSQL, Realtime).
*   **AI**: Anthropic API (Claude).

### 4.2. Data Model Extensions
*   To support the new requirements, the data model will need:
    *   `boards`: Add `settings` jsonb column (for email toggles/rules).
    *   `todos`: New table for tracking individual user tasks linked to boards/topics.
    *   `user_settings`: For sort preferences and reminder configurations.

## 5. Roadmap & Future Features
1.  **Google Integration**:
    *   Google OAuth for Single Sign-On.
    *   **Calendar Sync**: Automatically place decision due dates and reminders on the user's Google Calendar.

## 6. Success Metrics
*   Reduction in decision latency.
*   Accuracy of AI-extracted topics from forwarded emails.
*   User engagement with the Todo Hub.
