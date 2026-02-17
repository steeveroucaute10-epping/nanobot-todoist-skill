# Nanobot Todoist Skill

A Python MCP (Model Context Protocol) server that integrates Todoist with [Nanobot](https://nanobot.ai/). When nanobot reminds you about something, it can automatically create a Todoist task so you never forget.

Includes an **Agent Skill** (`SKILL.md`) per [Nanobot skill guidance](context/SKILLGuidance.md) so the agent knows when to use Todoist tools.

**Target platform:** Debian (Raspberry Pi). Nanobot runs as a systemd service.

## Features

- **create_task** – Create Todoist tasks with content, due dates, priority, and project
- **create_reminder_task** – Quick reminder creation (convenience wrapper)
- **list_projects** – List your Todoist projects (useful for choosing where to add tasks)
- **list_tasks_today** – List tasks due today
- **list_tasks_overdue** – List late/overdue tasks
- **list_tasks_this_week** – List tasks due this week

## Setup

### 1. Get your Todoist API token

1. Log in to [Todoist](https://todoist.com)
2. Go to **Settings → Integrations**
3. Copy your **API token**

### 2. Clone into Nanobot custom skills

If you use nanobot's GitHub skill to clone repos:

```bash
# Clone into your nanobot custom skills directory (replace YOUR_USERNAME with your GitHub username)
git clone https://github.com/steeveroucaute10-epping/nanobot-todoist-skill.git
cd nanobot-todoist-skill
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

Or with uv:

```bash
uv pip install -r requirements.txt
```

### 4. Set the API token

**Local development / interactive use:**
```bash
export TODOIST_API_TOKEN="your-api-token-here"
```
Or create a `.env` file next to `run.py` with `TODOIST_API_TOKEN=...` (loaded automatically).

**Nanobot running as systemd service (e.g. Raspberry Pi):**  
Do *not* rely on `.env` or `~/.bashrc`—systemd services don't inherit the user's shell environment. Set the token in the Nanobot service environment so it's available when Nanobot spawns the MCP subprocess. See [Running as a systemd service](#running-as-a-systemd-service) below.

## Nanobot Configuration

Add the Todoist MCP server to your nanobot config.

### Option A: Command (stdio) – recommended for Raspberry Pi / local

Add to your `nanobot.yaml` or `mcp-servers.yaml`:

```yaml
mcpServers:
  todoist:
    command: python
    args:
      - /home/pi/nanobot/custom-skills/nanobot-todoist-skill/run.py
    env:
      TODOIST_API_TOKEN: ${TODOIST_API_TOKEN}
```

Adjust the path if your skill is installed elsewhere.

**Note:** `run.py` resolves paths from its own location, so it works correctly when Nanobot spawns it from any working directory.

#### Running as a systemd service

When Nanobot runs under systemd (e.g. `systemctl start nanobot`), the token must be provided via the service environment. The Nanobot config's `env: TODOIST_API_TOKEN: ${TODOIST_API_TOKEN}` passes it to the MCP subprocess—but `${TODOIST_API_TOKEN}` must exist in Nanobot's process environment first.

**Option 1: Environment file (recommended)**

1. Create a secrets file (e.g. `/etc/nanobot/env` or `~/.config/nanobot/env`):
   ```
   TODOIST_API_TOKEN=your-api-token-here
   ```
2. Restrict permissions: `chmod 600 /path/to/env`
3. Add to your Nanobot systemd unit (e.g. `/etc/systemd/system/nanobot.service`):
   ```ini
   [Service]
   EnvironmentFile=/etc/nanobot/env
   ```
4. Reload and restart: `sudo systemctl daemon-reload && sudo systemctl restart nanobot`

**Option 2: Inline in the unit**

```ini
[Service]
Environment=TODOIST_API_TOKEN=your-api-token-here
```

The `.env` file next to `run.py` is only used when the MCP process starts and can load it; when Nanobot spawns the subprocess, the `env` block in the config overrides that. For systemd, setting the variable in the Nanobot service ensures it's available for the config to pass through.

### Option B: HTTP (if running as a service)

1. Start the server:
   ```bash
   python run.py --http
   ```
   Server runs at `http://localhost:8000/mcp`

2. Add to nanobot config:
   ```yaml
   mcpServers:
     todoist:
       url: http://localhost:8000/mcp
   ```

### Option C: Todoist hosted MCP (OAuth)

Todoist provides a hosted MCP at `https://ai.todoist.net/mcp` with OAuth—no API token needed. See [Todoist MCP docs](https://developer.todoist.com/api/v1/#tag/Todoist-MCP).

```yaml
mcpServers:
  todoist:
    command: npx
    args:
      - -y
      - mcp-remote
      - https://ai.todoist.net/mcp
```

Requires Node.js. OAuth flow runs when you first connect.

### Add to your agent

In your agent definition, include the todoist MCP server:

```yaml
agents:
  main:
    name: My Assistant
    model: gpt-4.1
    mcpServers:
      - todoist
    instructions: |
      You can create Todoist tasks when the user asks to be reminded of something.
      Use the create_task or create_reminder_task tool when they say things like
      "remind me to..." or "add to my todo list...".
      You can also answer questions about their tasks using list_tasks_today,
      list_tasks_overdue, and list_tasks_this_week when they ask "what do I have
      today?", "what's overdue?", or "what's due this week?".
```

## Usage with Nanobot

Once configured, you can say things like:

**Creating tasks:**
- "Remind me to call the dentist tomorrow"
- "Add 'buy groceries' to my todo list"
- "Create a task to review the report by Friday"
- "Put 'water the plants' in my Inbox for today"

**Asking about your tasks:**
- "What do I have due today?"
- "What tasks are overdue?"
- "What's on my plate this week?"

Nanobot will use the Todoist tools to create tasks or answer questions about your task list.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'todoist_mcp'` | Ensure `run.py` is in the skill directory and `src/` exists. Path resolution uses the script location, not cwd. |
| `TODOIST_API_TOKEN environment variable is not set` | Set the token in Nanobot's `env` block or in a `.env` file next to `run.py`. **For systemd:** use `EnvironmentFile=` or `Environment=` in the Nanobot service unit so the token is available to Nanobot. |
| MCP server doesn't start | Run `python run.py` manually to see errors. Ensure dependencies are installed (`pip install -r requirements.txt`). |

## Testing locally

```bash
# Set your token
export TODOIST_API_TOKEN="your-token"

# Run the test script
python test_skill.py
```

## Development

```bash
# Run with stdio (for testing with MCP Inspector)
python run.py

# Run with HTTP (for testing in browser)
python run.py --http
```

Test with MCP Inspector:

```bash
npx -y @modelcontextprotocol/inspector
# Connect to http://localhost:8000/mcp when using --http
```

## Project structure

```
nanobot-todoist-skill/
├── src/
│   └── todoist_mcp/
│       ├── __init__.py
│       ├── __main__.py
│       └── server.py      # MCP tools
├── context/
│   └── SKILLGuidance.md   # Nanobot skill creation guidance
├── run.py                 # Entry point (stdio/HTTP)
├── SKILL.md               # Agent Skill (when/how to use Todoist tools)
├── test_skill.py          # Local test script
├── requirements.txt
├── pyproject.toml
├── .env.example
├── nanobot-todoist.example.yaml
└── README.md
```

## License

MIT
