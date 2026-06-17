# Railway Deployment Checklist

Follow these steps to deploy your Discord Meme Bot to Railway.

## Prerequisites

- [ ] Discord bot created with token (see README.md)
- [ ] Bot invited to your server with correct permissions
- [ ] Channel IDs copied from Discord
- [ ] GitHub account
- [ ] Railway account (sign up at https://railway.app)

## Deployment Steps

### 1. Push to GitHub

```bash
# Initialize git if not already done
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Discord meme bot"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/discord-meme-bot.git
git branch -M main
git push -u origin main
```

### 2. Create Railway Project

1. Go to https://railway.app
2. Sign in with GitHub
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Choose your `discord-meme-bot` repository
6. Railway will automatically detect the `Dockerfile`

### 3. Configure Environment Variables

In Railway dashboard:
1. Click on your deployed service
2. Go to the **"Variables"** tab
3. Click **"New Variable"** and add each of these:

**Required variables:**
```
DISCORD_TOKEN=your_bot_token_here
ALLOWED_CHANNEL_IDS=123456789012345678,987654321098765432
MAX_FILE_SIZE_MB=10
CONCURRENCY=2
```

**Optional variables (for Reddit support):**
```
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
```

**Optional variable (for login-gated Instagram/Facebook content):**
```
COOKIES_FILE=instagram_cookies.txt
```

### 4. Deploy & Monitor

1. Railway will automatically build and deploy
2. Click on **"Logs"** to watch the deployment
3. Look for: `INFO - Logged in as YourBot#1234`
4. Look for: `INFO - Bot is ready!`

### 5. Test the Bot

1. Go to your Discord server
2. Post a link in one of your configured channels:
   ```
   https://www.tiktok.com/@user/video/1234567890
   ```
3. The bot should:
   - React with ⏳
   - Download the video
   - Upload it to Discord
   - Delete your original message
   - Post the video with credit

## Troubleshooting

### Build fails
- Check the **"Logs"** tab for specific errors
- Ensure `Dockerfile` and `requirements.txt` are in the repository

### Bot doesn't start
- Verify all environment variables are set correctly
- Check `DISCORD_TOKEN` is valid
- Look for errors in the **"Logs"** tab

### Bot is offline in Discord
- Ensure the service is running in Railway (green status)
- Check **"Logs"** for connection errors
- Verify bot has **Message Content Intent** enabled in Discord Developer Portal

### Bot doesn't respond to links
- Check `ALLOWED_CHANNEL_IDS` is set correctly (no spaces after commas)
- Verify bot has correct permissions in Discord server
- Check **"Logs"** to see if messages are being received

## Managing Your Bot

### Restart the bot
1. In Railway dashboard, click your service
2. Click the three dots menu (⋮)
3. Select **"Restart"**

### View logs
1. Click on your service
2. Click **"Logs"** tab
3. Use the search/filter to find specific events

### Update the bot
1. Push changes to GitHub:
   ```bash
   git add .
   git commit -m "Update bot"
   git push
   ```
2. Railway will automatically rebuild and redeploy

### Pause the bot (stop billing)
1. Click your service
2. Toggle the service off
3. To resume, toggle it back on

## Cost Estimate

- **Estimated cost:** $5–$7/month for 24/7 operation
- Railway charges based on:
  - CPU usage
  - Memory usage
  - Network egress (downloading videos)
- You can monitor usage in the Railway dashboard

## Next Steps

- Set up monitoring alerts in Railway
- Add more channels to `ALLOWED_CHANNEL_IDS`
- Configure Reddit API for Reddit post support
- Monitor logs for any errors or issues

## Support

If you encounter issues:
1. Check Railway **"Logs"** tab
2. Verify Discord bot permissions
3. Check Railway status: https://status.railway.app
4. Review README.md for bot configuration details

Happy hosting! 🚀
