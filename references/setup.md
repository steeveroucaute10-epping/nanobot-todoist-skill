# Setup

Debian (Raspberry Pi). Nanobot runs as a systemd service.

## 1. Clone

```bash
cd /home/pi/nanobot/custom-skills   # or your nanobot skills directory
git clone https://github.com/steeveroucaute10-epping/nanobot-todoist-skill.git
cd nanobot-todoist-skill
```

## 2. Todoist API token

Get from [Todoist Settings → Integrations](https://app.todoist.com/prefs/integrations).

## 3. Systemd environment

Create `/etc/nanobot/env`:
```
TODOIST_API_TOKEN=your-api-token-here
```
`chmod 600 /etc/nanobot/env`

Add to the Nanobot systemd unit:
```ini
[Service]
EnvironmentFile=/etc/nanobot/env
```

## 4. Nanobot config

Merge into your Nanobot config (e.g. `~/.nanobot/config.json` or the config your nanobot uses):

```yaml
mcpServers:
  todoist:
    command: python
    args:
      - /home/pi/nanobot/custom-skills/nanobot-todoist-skill/run.py
    env:
      TODOIST_API_TOKEN: ${TODOIST_API_TOKEN}

agents:
  main:
    mcpServers:
      - todoist
```

Adjust the path in `args` if your clone is in a different location.

## 5. Install dependencies

Use the same Python that runs nanobot (system or venv):

```bash
cd /home/pi/nanobot/custom-skills/nanobot-todoist-skill
pip install -r requirements.txt
```

If nanobot uses a venv, use that venv’s pip instead, e.g.:
```bash
/home/pi/nanobot/venv/bin/pip install -r requirements.txt
```

## 6. Reload and restart Nanobot

After editing config or the env file:

```bash
sudo systemctl daemon-reload
sudo systemctl restart nanobot-gateway   # or your nanobot unit name
```

## 7. Verify

```bash
systemctl status nanobot-gateway
journalctl -u nanobot-gateway -n 50 -f
```

Check that the Todoist MCP starts without errors.
