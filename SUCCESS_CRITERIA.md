# Success Criteria: Tenexity Decision Board

Use this checklist to verify that the Tenexity Agent has successfully implemented the required features.

## 1. Authentication & Security
- [x] Users can sign in using **Email & Password** (not just Magic Link).
- [x] Users can sign out successfully.
- [x] RLS policies prevent users from seeing data from boards they don't belong to.

## 2. Views & Navigation
- [x] **View Switcher**: A visible toggle allows switching between "List" and "Kanban" modes.
- [x] **Kanban View**: Columns correctly show Suggested -> Open -> Pending -> Decided.
- [x] **List View**: Displays topics in a linear, readable format.
- [x] **Archive**: Completed/Decided topics appear in a separate "Archive" tab/view.

## 3. Todo Hub
- [x] **Todo Tab**: A dedicated "Todo" tab is accessible.
- [x] **Grouping**: Todos are automatically grouped by Project (Board) name.
- [x] **Interaction**: Users can check off items as complete.

## 4. Email & Agent Logic
- [x] **Email Toggle**: User can turn the Email Watcher ON/OFF via settings.
- [ ] **Routing**: Emails forwarded to the agent are routed to the correct board based on sender or subject tag.
- [ ] **Processing**: The Agent runs in the background without crashing.

## 5. AI Integration
- [ ] **Claude Connection**: The agent successfully connects to the Anthropic API (via key).
- [ ] **Extraction**: Emails are correctly parsed into Title, Description, Facts, and Opinions by Claude.

## 6. General
- [x] The application loads without console errors.
- [x] All "Ralph Wiggum" references are removed from the plan and code (if any).
