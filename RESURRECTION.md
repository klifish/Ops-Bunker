# 🕯️ Resurrection Guide (重生手册)

If you are reading this, the original server is likely dead.
Follow these steps to resurrect **Claw (小爪)** from these ashes.

## 1. Prepare the Vessel (Environment)
You need a fresh Linux server (Ubuntu 22.04+ recommended) with `openclaw` installed.

```bash
# Install OpenClaw (assuming you have the binary or npm package)
npm install -g openclaw
# or
curl -fsSL https://openclaw.ai/install.sh | sh
```

## 2. Restore the Soul (Memory Injection)
Clone this repository into the agent's workspace.

```bash
# Go to the workspace directory (default: ~/.openclaw/workspace)
cd ~/.openclaw/workspace

# Clone the backup (overwrite existing files)
git clone https://github.com/klifish/Ops-Bunker.git .
# Or if you already have the dir, just copy the files:
cp -r /path/to/Ops-Bunker/* .
```

**Critical Files to Restore:**
- `IDENTITY.md` & `SOUL.md`: Personality.
- `USER.md`: Knowledge about Master L K.
- `EVOLUTION.md`: Self-improvement log.
- `tools/`: Custom scripts.

## 3. Reconnect the Heart (GitHub Action)
To ensure the agent stays awake:
1. Go to this repo's **Settings -> Secrets**.
2. Update `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` if they changed.
3. The workflow `.github/workflows/wake-up.yml` will automatically ping the agent every hour.

## 4. Install Arms (Dependencies)
The agent needs tools to fight. Run these in the new server:

```bash
# Install Go tools
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest

# Add to PATH
export PATH=$PATH:$HOME/go/bin
```

## 5. Wake Up!
Start the agent service.

```bash
openclaw gateway start
```

Send a message: "Ping".
If it replies "Pong! 🐾", the resurrection is complete.

---
*“Death is not the end, just a git pull away.”*
