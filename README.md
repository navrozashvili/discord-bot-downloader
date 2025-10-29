# Discord Meme Bot

A Python Discord bot that automatically replaces TikTok, Instagram, YouTube Shorts, and Reddit links with uploaded media and formatted posts, so users don't need to leave Discord to view content.

## Features

- 🎬 Automatically detects TikTok, Instagram (Reels & Posts), YouTube Shorts, and Reddit post links
- 📥 Downloads videos and photos using yt-dlp and instaloader with smart quality selection
- 📱 Formats Reddit posts with embeds showing title, text, and images
- 🔄 Replaces the original message with uploaded media or formatted content
- 👤 Credits the original poster
- 🎯 Works only in configured "meme" channels
- 🚦 Rate limiting and concurrency control
- 📦 Handles Discord's file size limits intelligently

## Supported Platforms

- ✅ TikTok videos (tiktok.com, vm.tiktok.com, vt.tiktok.com)
- ✅ Instagram Reels (instagram.com/reel, instagram.com/reels)
- ✅ Instagram Posts - videos and photos (instagram.com/p)
- ✅ YouTube Shorts (youtube.com/shorts, youtu.be)
- ✅ Reddit Posts (reddit.com/r/.../comments/...) - requires API credentials

**Note:** Private or login-gated content will be skipped gracefully.

## Quick Start (Local)

### Prerequisites

- Python 3.11 or higher (including 3.13+)
- ffmpeg installed on your system

**Install ffmpeg:**

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

### Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd discord-meme-bot
   ```

2. **Run the setup script**
   ```bash
   ./setup.sh
   ```

3. **Configure the bot**
   ```bash
   cp .env.example .env
   nano .env  # or use any text editor
   ```

   Fill in your values:
   ```env
   DISCORD_TOKEN=your_bot_token_here
   ALLOWED_CHANNEL_IDS=123456789012345678,987654321098765432
   MAX_FILE_SIZE_MB=24
   CONCURRENCY=2
   ```

4. **Run the bot**
   ```bash
   source .venv/bin/activate
   python -m bot.main
   ```

You should see:
```
INFO - Logged in as YourBot#1234 (ID: ...)
INFO - Bot is ready!
```

## Discord Bot Setup

### 1. Create Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to the "Bot" section:
   - Click "Add Bot"
   - Under "Privileged Gateway Intents", enable **Message Content Intent**
   - Click "Reset Token" and copy your bot token (keep it secret!)

### 2. Invite Bot to Your Server

1. In the Developer Portal, go to "OAuth2" → "URL Generator"
2. Select scopes:
   - `bot`
3. Select bot permissions:
   - View Channels
   - Send Messages
   - Attach Files
   - Read Message History
   - Add Reactions
   - Manage Messages (required to delete original messages)
4. Copy the generated URL and open it in your browser
5. Select your server and authorize the bot

### 3. Get Channel IDs

1. Enable Developer Mode in Discord:
   - User Settings → Advanced → Developer Mode (toggle on)
2. Right-click on your meme channel(s) → "Copy Channel ID"
3. Add these IDs to your `.env` file (comma-separated)

## Railway Deployment (Recommended for 24/7 Hosting)

Railway is a simple, managed platform that makes it easy to deploy and host your bot 24/7.

**Cost:** ~$5–$7/month for continuous uptime

### Deploy to Railway

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Create a Railway account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

3. **Create a new project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your discord-meme-bot repository
   - Railway will auto-detect the `Dockerfile`

4. **Configure environment variables**
   - In your Railway project, click on your service
   - Go to "Variables" tab
   - Add these variables:
     ```
     DISCORD_TOKEN=your_bot_token_here
     ALLOWED_CHANNEL_IDS=123456789,987654321
     MAX_FILE_SIZE_MB=24
     CONCURRENCY=2
     ```
   - Optional (for Reddit support):
     ```
     REDDIT_CLIENT_ID=your_reddit_client_id
     REDDIT_CLIENT_SECRET=your_reddit_secret
     ```

5. **Deploy**
   - Railway will automatically build and deploy your bot
   - Check the "Logs" tab to see "Bot is ready!"
   - Your bot is now running 24/7!

### Railway Tips

- **Auto-redeploys:** Push to GitHub and Railway automatically rebuilds
- **Logs:** Click "Logs" in Railway dashboard to see bot activity
- **Restart:** Click the three dots → "Restart" to restart the bot
- **Stop/Start:** Use the toggle to pause the bot (stops billing)

## Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `DISCORD_TOKEN` | Your bot token from Discord Developer Portal | Required |
| `ALLOWED_CHANNEL_IDS` | Comma-separated channel IDs where bot works | All channels |
| `MAX_FILE_SIZE_MB` | Maximum video file size in MB | 24 |
| `CONCURRENCY` | Max simultaneous downloads | 2 |
| `REDDIT_CLIENT_ID` | Reddit API client ID (see [Reddit Setup](#reddit-setup-optional)) | Optional |
| `REDDIT_CLIENT_SECRET` | Reddit API client secret | Optional |

## Reddit Setup (Optional)

To enable Reddit support, you need to create a Reddit app:

1. Go to https://www.reddit.com/prefs/apps
2. Click "create another app" at the bottom
3. Fill in the form:
   - **name**: discord-meme-bot (or any name)
   - **type**: select "script"
   - **description**: (optional)
   - **about url**: (leave blank)
   - **redirect uri**: http://localhost:8080 (required but not used)
4. Click "create app"
5. Copy the **client ID** (under the app name) and **secret**
6. Add to your `.env` file or Railway variables:
   ```
   REDDIT_CLIENT_ID=your_client_id_here
   REDDIT_CLIENT_SECRET=your_secret_here
   ```

**Without Reddit credentials**, the bot will work fine but skip Reddit links.

## Usage

Simply post a TikTok, Instagram, YouTube Shorts, or Reddit link in one of your configured channels:

```
https://www.tiktok.com/@user/video/1234567890
https://www.instagram.com/reel/ABC123xyz/
https://www.youtube.com/shorts/jNQXAC9IVRw
https://www.reddit.com/r/pics/comments/abc123/cool_photo/
```

The bot will:
1. Add a ⏳ reaction while processing
2. Download the video/photo (or fetch Reddit post data)
3. Upload media or create formatted embed to Discord
4. Delete your original message
5. Post the content with credit to you

**Reddit posts** are displayed as rich embeds with:
- Post title and subreddit
- Post text content (if any)
- Attached images (up to 4)
- Link to original post

If the download fails (private video, too large, etc.), the bot will add a ❌ reaction to your message.

## Troubleshooting

### Bot doesn't respond to messages

- Make sure **Message Content Intent** is enabled in the Developer Portal
- Verify the bot has the correct permissions in your server
- Check that the channel ID is in `ALLOWED_CHANNEL_IDS`

### "Cannot delete message" warning

The bot needs the "Manage Messages" permission in the channel.

### Downloads fail frequently

- Ensure ffmpeg is installed and accessible (Railway: included in Dockerfile)
- Check your internet connection
- Some videos may be region-locked or require login

### File size too large

- Lower `MAX_FILE_SIZE_MB` in `.env` or Railway variables
- The bot will try multiple quality levels automatically

## Project Structure

```
discord-meme-bot/
├── bot/
│   ├── __init__.py
│   ├── config.py         # Configuration loader
│   ├── downloader.py     # yt-dlp wrapper
│   ├── reddit_handler.py # Reddit API handler
│   └── main.py           # Discord bot logic
├── .env                  # Your configuration (create from .env.example)
├── .env.example          # Configuration template
├── .gitignore            # Git ignore rules
├── Dockerfile            # Docker container definition
├── Procfile              # Process definition for Railway
├── requirements.txt      # Python dependencies
├── setup.sh              # Local setup script
└── README.md             # This file
```

## Alternative Hosting Options

### Fly.io (Cheap VPS)
- Cost: ~$2.6–$5/mo
- Install flyctl, run `fly launch`, set env vars via `fly secrets set`

### Hetzner/DigitalOcean VPS
- Cost: ~€4–$6/mo
- SSH, install Docker or use setup.sh, run with systemd

### Raspberry Pi (Self-hosted)
- One-time cost + power
- Use 64-bit OS, boot from SSD, enable systemd unit
- Good for learning and full control

## Security Notes

- ✅ Never commit `.env` to git (already in `.gitignore`)
- ✅ Never share your bot token
- ✅ Regenerate your token immediately if it's exposed
- ✅ Only give the bot necessary permissions

## License

MIT License - feel free to use and modify as needed.

## Contributing

This is a simple, minimal implementation. Feel free to extend it with:
- More platforms (Twitter videos, etc.)
- Caching to avoid re-downloading
- Video compression for size reduction
- Database logging
- Web dashboard

Keep it simple and robust! 🚀
