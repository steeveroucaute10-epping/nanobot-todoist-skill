# Setup

Debian (Raspberry Pi). Nanobot runs as a systemd service.

## 1. Todoist API token

Get from [Todoist Settings → Integrations](https://app.todoist.com/prefs/integrations).

## 2. Systemd environment

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

## 3. Nanobot config

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

## 4. Install

```bash
cd /home/pi/nanobot/custom-skills/nanobot-todoist-skill
pip install -r requirements.txt
```
