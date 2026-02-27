# Setup

Debian (Raspberry Pi). Nanobot runs as a systemd service.

## 1. Clone into nanobot workspace

Clone directly into nanobot's skill discovery directory so that nanobot finds the `SKILL.md` automatically:

```bash
cd ~/.nanobot/workspace/skills
git clone https://github.com/steeveroucaute10-epping/nanobot-todoist-skill.git todoist
cd todoist
```

The skill directory name (`todoist`) is what nanobot uses as the skill name.

## 2. Install dependencies

Use the **same Python that runs nanobot**. If nanobot uses a venv:

```bash
/home/pi/nanobot-venv/bin/pip install -r ~/.nanobot/workspace/skills/todoist/requirements.txt
```

Or if using system Python:

```bash
pip install -r ~/.nanobot/workspace/skills/todoist/requirements.txt
```

## 3. Todoist API token

Get from [Todoist Settings → Integrations](https://app.todoist.com/prefs/integrations).

## 4. Systemd environment

Create `/etc/nanobot/env` (or add to existing):

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

## 5. Nanobot config

Merge into `~/.nanobot/config.json`. The config is **JSON** and MCP servers live under `tools.mcpServers`:

```json
{
  "tools": {
    "mcpServers": {
      "todoist": {
        "command": "/home/pi/nanobot-venv/bin/python",
        "args": ["/home/pi/.nanobot/workspace/skills/todoist/run.py"],
        "env": {
          "TODOIST_API_TOKEN": "${TODOIST_API_TOKEN}"
        }
      }
    }
  }
}
```

Adjust `command` to match the Python that has `mcp` and `todoist-api-python` installed (the same one from step 2). Adjust the `args` path if you cloned elsewhere.

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

1. **Check Python path**: Run `/home/pi/nanobot-venv/bin/python -c "import mcp; import todoist_api_python"` to confirm deps are installed.
2. **Check run.py manually**: `/home/pi/nanobot-venv/bin/python ~/.nanobot/workspace/skills/todoist/run.py` — it should start and wait on stdin (Ctrl+C to exit). If it errors, fix the import/env issue.
3. **Check config format**: `~/.nanobot/config.json` must be valid JSON. Use `python -m json.tool ~/.nanobot/config.json` to validate.
4. **Check env**: Confirm `TODOIST_API_TOKEN` reaches the process — add `echo $TODOIST_API_TOKEN` in a test or check `journalctl` for "not set" errors.
5. **Exec fallback**: If MCP still doesn't work, the agent can call `run.py` directly via the `exec` tool. See `SKILL.md` for details.
