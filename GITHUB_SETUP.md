# GitHub Repository Setup

To publish this skill and use it with nanobot's GitHub skill:

## 1. Create a new repository on GitHub

1. Go to [github.com/new](https://github.com/new)
2. Repository name: `nanobot-todoist-skill` (or your preferred name)
3. Description: "Todoist MCP skill for Nanobot - create todos when nanobot reminds you"
4. Choose **Public**
5. **Do not** initialize with README (we already have one)
6. Click **Create repository**

## 2. Push this project to your new repo

From the `nanobot-todoist-skill` directory:

```bash
cd c:\Users\felix\OneDrive\Documents\dev\nanobot-todoist-skill
git init
git add .
git commit -m "Initial commit: Todoist MCP skill for Nanobot"
git branch -M main
git remote add origin https://github.com/steeveroucaute10-epping/nanobot-todoist-skill.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username (or use steeveroucaute10-epping).

## 3. Clone into Nanobot custom skills (on Raspberry Pi)

Using nanobot's GitHub skill, or manually:

```bash
cd ~/nanobot/custom-skills  # or your nanobot skills directory
git clone https://github.com/steeveroucaute10-epping/nanobot-todoist-skill.git
```

## 4. Update pyproject.toml

Edit `pyproject.toml` and replace `YOUR_USERNAME` in the URLs with your actual GitHub username.
