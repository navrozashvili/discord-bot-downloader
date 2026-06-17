"""Configuration loader for Discord bot."""
import os
from typing import Set, Dict, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Bot configuration from environment variables."""
    
    def __init__(self):
        self.discord_token = os.getenv("DISCORD_TOKEN")
        if not self.discord_token:
            raise ValueError("DISCORD_TOKEN environment variable is required")
        
        # Parse allowed channel IDs
        channel_ids_str = os.getenv("ALLOWED_CHANNEL_IDS", "")
        self.allowed_channel_ids: Set[int] = set()
        if channel_ids_str:
            try:
                self.allowed_channel_ids = {
                    int(cid.strip()) 
                    for cid in channel_ids_str.split(",") 
                    if cid.strip()
                }
            except ValueError:
                raise ValueError("ALLOWED_CHANNEL_IDS must be comma-separated integers")
        
        # Max file size in bytes
        max_size_mb = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
        self.max_file_size_bytes = max_size_mb * 1024 * 1024
        
        # Concurrency limit
        self.concurrency = int(os.getenv("CONCURRENCY", "2"))
        
        # Cookies file (optional, for private/login-required Instagram/Facebook content)
        self.cookies_file = os.getenv("COOKIES_FILE", "instagram_cookies.txt")
        
        # Reddit API credentials (optional, for Reddit support)
        # Get these from https://www.reddit.com/prefs/apps
        self.reddit_client_id = os.getenv("REDDIT_CLIENT_ID")
        self.reddit_client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        
        # Optional per-channel webhook mapping to post as the user
        # Format: "channel_id=url,channel_id=url"
        self.channel_webhooks: Dict[int, str] = {}
        raw_webhooks = os.getenv("CHANNEL_WEBHOOKS", "").strip()
        if raw_webhooks:
            parts = [p.strip() for p in raw_webhooks.split(",") if p.strip()]
            for part in parts:
                if "=" not in part:
                    continue
                cid_str, url = part.split("=", 1)
                try:
                    cid = int(cid_str.strip())
                except ValueError:
                    continue
                url = url.strip()
                if url:
                    self.channel_webhooks[cid] = url
    
    def is_channel_allowed(self, channel_id: int) -> bool:
        """Check if a channel is in the allowlist."""
        # If no channels configured, allow all
        if not self.allowed_channel_ids:
            return True
        return channel_id in self.allowed_channel_ids

    def webhook_url_for_channel(self, channel_id: int) -> Optional[str]:
        """Get webhook URL for a channel if configured."""
        return self.channel_webhooks.get(channel_id)


# Global config instance
config = Config()
