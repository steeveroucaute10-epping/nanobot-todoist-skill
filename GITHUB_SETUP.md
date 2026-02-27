# GitHub Repository Setup

To publish this skill and use it with nanobot:

## 1. Create a new repository on GitHub

1. Go to [github.com/new](https://github.com/new)
2. Repository name: `nanobot-todoist-skill` (or your preferred name)
3. Description: "Todoist MCP skill for Nanobot - create todos when nanobot reminds you"
4. Choose **Public**
5. **Do not** initialize with README (we already have one)
6. Click **Create repository**

## 2. Push this project to your new repo

From your project directory (where you have the skill code):

```bash
cd /path/to/nanobot-todoist-skill   # or: cd path\to\nanobot-todoist-skill on Windows
git init
git add .
git commit -m "Initial commit: Todoist MCP skill for Nanobot"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/nanobot-todoist-skill.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username (and the repo URL if you created a different repo name).

## 3. Clone into nanobot workspace on Raspberry Pi

Clone directly into nanobot's skill discovery directory:

```bash
cd ~/.nanobot/workspace/skills
git clone https://github.com/YOUR_USERNAME/nanobot-todoist-skill.git todoist
```

The directory name (`todoist`) must match the skill `name` in `SKILL.md`.

## 4. Follow setup steps

See [references/setup.md](references/setup.md) for the remaining steps (install deps, env, config, restart).
