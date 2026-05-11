# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## GitHub Repository

This project is synced to **https://github.com/jonevaz/calputwiz**.

After every response that modifies files, automatically run:
```
git add -A && git diff --cached --quiet || git commit -m "chore: auto-sync changes" && git push origin main
```

This ensures all changes are immediately pushed to GitHub.

## Repository state

This repository currently contains no source files or project structure. No stack, framework, or tooling has been chosen yet.

## Working in this repository

- Confirm the intended technology stack, language, and project goals before generating any code.
- Do not assume a frontend, backend, or library layout.
- When asked to initialize a project, propose a minimal scaffold and ask for approval first.
- Ask clarifying questions before creating files; prefer small incremental changes over large scaffolding without direction.
- Preserve the user's choice of conventions and tooling once established.
