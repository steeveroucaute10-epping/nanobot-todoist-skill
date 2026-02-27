# Setup

Debian (Raspberry Pi). Nanobot runs in a **venv** (`/home/pi/nanobot-venv/`) as a **systemd service**.

## 1. Clone into nanobot workspace

Clone directly into nanobot's skill discovery directory so that nanobot finds the `SKILL.md` automatically:

```bash
cd ~/.nanobot/workspace/skills
git clone https://github.com/steeveroucaute10-epping/nanobot-todoist-skill.git todoist
cd todoist
```

The skill directory name (`todoist`) is what nanobot uses as the skill name.

## 2. Install dependencies

Install into the **same venv** that runs nanobot:

```bash
/home/pi/nanobot-venv/bin/pip install -r ~/.nanobot/workspace/skills/todoist/requirements.txt
```

## 3. Todoist API token

Get from [Todoist Settings → Integrations](https://app.todoist.com/prefs/integrations).

## 4. Systemd environment (recommended)

The recommended way to pass secrets on the Pi is via systemd `EnvironmentFile`. This keeps secrets out of the repo, survives `git pull`, and is secured with file permissions.

Add the token to `/etc/nanobot/env` (create the file if it doesn't exist):

```
TODOIST_API_TOKEN=your-api-token-here
```

Secure it:

```bash
sudo chmod 600 /etc/nanobot/env
```

Add to the nanobot systemd unit (if not already present):

```ini
[Service]
EnvironmentFile=/etc/nanobot/env
```

The token is inherited by nanobot and all child processes (including MCP servers) automatically.

> **Note:** The `.env` file in this repo is for **local development/testing only** (e.g. on your PC). It should not exist on the Pi — use the systemd `EnvironmentFile` instead.

## 5. Nanobot config

Merge into `~/.nanobot/config.json`. The config is **JSON** and MCP servers live under `tools.mcpServers`.

If using systemd `EnvironmentFile` (recommended — the token is already in the environment):

```json
{
  "tools": {
    "mcpServers": {
      "todoist": {
        "command": "/home/pi/nanobot-venv/bin/python",
        "args": ["/home/pi/.nanobot/workspace/skills/todoist/run.py"]
      }
    }
  }
}
```

Alternative — if not using systemd `EnvironmentFile`, pass the token explicitly via the `env` block:

```json
{
  "tools": {
    "mcpServers": {
      "todoist": {
        "command": "/home/pi/nanobot-venv/bin/python",
        "args": ["/home/pi/.nanobot/workspace/skills/todoist/run.py"],
        "env": {
          "TODOIST_API_TOKEN": "your-api-token-here"
        }
      }
    }
  }
}
```

`command` must point to the **venv Python** that has `mcp` and `todoist-api-python` installed (the same one from step 2). Adjust the `args` path if you cloned elsewhere.

## 6. Reload and restart nanobot

```bash
sudo systemctl daemon-reload
sudo systemctl restart nanobot-gateway   # or your nanobot unit name
```

## 7. Verify

```bash
systemctl status nanobot-gateway
journalctl -u nanobot-gateway -n 50 -f
```

Check that the Todoist MCP server starts without errors and that nanobot logs show the `todoist` tools being registered.

## Troubleshooting

If nanobot does not register the Todoist tools:

1. **Check Python path**: Run `/home/pi/nanobot-venv/bin/python -c "import mcp; import todoist_api_python"` to confirm deps are installed in the venv.
2. **Check run.py manually**: `/home/pi/nanobot-venv/bin/python ~/.nanobot/workspace/skills/todoist/run.py` — it should start and wait on stdin (Ctrl+C to exit). If it errors, fix the import/env issue.
3. **Check config format**: `~/.nanobot/config.json` must be valid JSON. Use `python -m json.tool ~/.nanobot/config.json` to validate.
4. **Check env**: Confirm `TODOIST_API_TOKEN` reaches the process — check `journalctl -u nanobot-gateway` for "not set" errors. If using systemd `EnvironmentFile`, verify `/etc/nanobot/env` exists and the unit references it.
5. **Exec fallback**: If MCP still doesn't work, the agent can call `run.py` directly via the `exec` tool. See `SKILL.md` for details.
