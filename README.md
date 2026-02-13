# Nanobot Todoist Skill

A Python MCP (Model Context Protocol) server that integrates Todoist with [Nanobot](https://nanobot.ai/). When nanobot reminds you about something, it can automatically create a Todoist task so you never forget.

## Features

- **create_task** – Create Todoist tasks with content, due dates, priority, and project
- **create_reminder_task** – Quick reminder creation (convenience wrapper)
- **list_projects** – List your Todoist projects (useful for choosing where to add tasks)

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

```bash
export TODOIST_API_TOKEN="your-api-token-here"
```

On Raspberry Pi, add to `~/.bashrc` or create a `.env` file (and load it before starting).

## Nanobot Configuration

Add the Todoist MCP server to your nanobot config.

### Option A: Command (stdio) – recommended for Raspberry Pi

Add to your `nanobot.yaml` or `mcp-servers.yaml`:

```yaml
mcpServers:
  todoist:
    command: python
    args:
      - /path/to/nanobot-todoist-skill/run.py
    env:
      TODOIST_API_TOKEN: ${TODOIST_API_TOKEN}
```

Replace `/path/to/nanobot-todoist-skill` with the actual path (e.g. `~/nanobot/custom-skills/nanobot-todoist-skill`).

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
```

## Usage with Nanobot

Once configured, you can say things like:

- "Remind me to call the dentist tomorrow"
- "Add 'buy groceries' to my todo list"
- "Create a task to review the report by Friday"
- "Put 'water the plants' in my Inbox for today"

Nanobot will use the Todoist tools to create the tasks.

## Testing locally

```bash
# Set your token
export TODOIST_API_TOKEN="your-token"   # or on Windows: $env:TODOIST_API_TOKEN = "your-token"

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
├── run.py                 # Entry point
├── test_skill.py           # Local test script
├── requirements.txt
├── pyproject.toml
├── .env.example
├── nanobot-todoist.example.yaml
└── README.md
```

## License

MIT
