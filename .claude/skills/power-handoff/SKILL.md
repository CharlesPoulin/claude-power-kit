---
name: power-handoff
description: Save a concise resumable work checkpoint before changing chats or pausing a coding task. Use when asked to hand off, checkpoint, or preserve progress.
argument-hint: "[handoff file path]"
---

# Save a resumable checkpoint

Use the requested path, or `HANDOFF.md` in the project. Read an existing handoff before updating it, preserving unrelated work.

Record the objective, current branch and commit if available, changed files, decisions that affect the next step, exact checks run and outcomes, blockers, and the next concrete action. Separate completed facts from unverified assumptions. Keep it short enough for a fresh agent to use without reading the previous conversation.

Do not copy secrets, tokens, private message contents, or large logs. Do not infer permission to commit or publish the handoff. End with the saved path and a one-sentence resume prompt.
