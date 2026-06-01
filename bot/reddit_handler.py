"""Reddit post handler for fetching and formatting Reddit posts."""
import logging
import re
from pathlib import Path
from typing import Optional, List
import tempfile
from urllib.parse import urlparse
import requests

try:
    import praw
    PRAW_AVAILABLE = True
except ImportError:
    PRAW_AVAILABLE = False

logger = logging.getLogger(__name__)


class RedditPost:
    """Represents a Reddit post with its content."""
    
    def __init__(self, title: str, author: str, subreddit: str,
                 text: Optional[str] = None, image_urls: Optional[List[str]] = None,
                 url: Optional[str] = None, video_url: Optional[str] = None):
        self.title = title
        self.author = author
        self.subreddit = subreddit
        self.text = text
        self.image_urls = image_urls or []
        self.url = url
        self.video_url = video_url


class RedditHandler:
    """Handles fetching Reddit posts using PRAW for reliable access."""
    
    def __init__(self, max_file_size_bytes: int, client_id: Optional[str] = None, 
                 client_secret: Optional[str] = None):
        self.max_file_size_bytes = max_file_size_bytes
        self.temp_dir = Path(tempfile.gettempdir()) / "discord_meme_bot"
        self.temp_dir.mkdir(exist_ok=True)
        
        # Initialize PRAW if credentials provided
        if PRAW_AVAILABLE and client_id and client_secret:
            try:
                self.reddit = praw.Reddit(
                    client_id=client_id,
                    client_secret=client_secret,
                    user_agent="discord-meme-bot/1.0 by /u/discord-bot"
                )
                logger.info("Reddit handler initialized with API credentials")
            except Exception as e:
                self.reddit = None
                logger.warning(f"Failed to initialize Reddit handler: {e}")
        else:
            self.reddit = None
            if not PRAW_AVAILABLE:
                logger.info("PRAW not installed - Reddit support disabled")
            else:
                logger.info("Reddit API credentials not provided - Reddit support disabled. "
                          "Get credentials from https://www.reddit.com/prefs/apps")
    
    def extract_post_id(self, url: str) -> Optional[str]:
        """Extract post ID from Reddit URL.

        Supports canonical URLs, share URLs, and redd.it short links.
        """
        parsed = urlparse(url)
        host = parsed.netloc.lower()
        path = parsed.path

        # Canonical Reddit URLs: /r/<sub>/comments/<id>/... or /comments/<id>/...
        match = re.search(r'/comments/([a-z0-9]+)', path, re.IGNORECASE)
        if match:
            return match.group(1)

        # redd.it short links: https://redd.it/<id>
        if host.endswith('redd.it'):
            short_id = path.strip('/').split('/', 1)[0]
            if re.fullmatch(r'[a-z0-9]+', short_id, re.IGNORECASE):
                return short_id

        return None

    def _resolve_reddit_share_url(self, url: str) -> str:
        """Resolve Reddit share URLs (e.g. /r/<sub>/s/<token>) to canonical URLs."""
        try:
            response = requests.get(
                url,
                headers={'User-Agent': 'discord-meme-bot/1.0'},
                allow_redirects=True,
                timeout=10,
            )
            resolved_url = response.url or url
            if resolved_url != url:
                logger.info(f"Resolved Reddit URL: {url} -> {resolved_url}")
            return resolved_url
        except Exception as e:
            logger.warning(f"Failed to resolve Reddit URL {url}: {type(e).__name__}: {e}")
            return url
    
    def fetch_post(self, url: str) -> Optional[RedditPost]:
        """Fetch Reddit post information using PRAW."""
        if not PRAW_AVAILABLE or self.reddit is None:
            logger.error("PRAW not available")
            return None
        
        try:
            post_id = self.extract_post_id(url)

            # Handle share-style URLs that don't include the post id directly.
            if not post_id:
                url = self._resolve_reddit_share_url(url)
                post_id = self.extract_post_id(url)

            # Fetch submission using ID when available, fallback to URL lookup.
            if post_id:
                submission = self.reddit.submission(id=post_id)
            else:
                logger.info(f"Falling back to PRAW URL lookup for {url}")
                submission = self.reddit.submission(url=url)
            
            # Get post text (if it's a text post)
            text = None
            if hasattr(submission, 'selftext') and submission.selftext:
                # Limit text length
                text = submission.selftext[:2000]
                if len(submission.selftext) > 2000:
                    text += "..."
            
            # Get images / video
            image_urls = []
            video_url = None

            canonical_url = f"https://www.reddit.com{submission.permalink}" if getattr(submission, 'permalink', None) else url

            # Check for native Reddit-hosted video posts
            if getattr(submission, 'is_video', False):
                # Prefer canonical post URL; yt-dlp can extract and merge audio/video from it.
                video_url = canonical_url or submission.url or url

            # Check if post has a direct image
            elif hasattr(submission, 'post_hint') and submission.post_hint == 'image':
                image_urls.append(submission.url)

            # Check for gallery posts
            elif hasattr(submission, 'is_gallery') and submission.is_gallery:
                if hasattr(submission, 'media_metadata'):
                    gallery_data = submission.gallery_data
                    items = gallery_data.get('items', [])
                    media_metadata = submission.media_metadata

                    for item in items:
                        media_id = item['media_id']
                        if media_id in media_metadata:
                            media_info = media_metadata[media_id]
                            # Get the highest quality image
                            if 's' in media_info:
                                if 'u' in media_info['s']:
                                    image_url = media_info['s']['u'].replace('&amp;', '&')
                                    image_urls.append(image_url)
                                elif 'gif' in media_info['s']:
                                    image_url = media_info['s']['gif'].replace('&amp;', '&')
                                    image_urls.append(image_url)

            # Check for preview images if no other media found
            elif not image_urls and not video_url and hasattr(submission, 'preview'):
                preview = submission.preview
                if 'images' in preview and preview['images']:
                    source = preview['images'][0].get('source', {})
                    if 'url' in source:
                        image_url = source['url'].replace('&amp;', '&')
                        image_urls.append(image_url)

            return RedditPost(
                title=submission.title,
                author=submission.author.name if submission.author else '[deleted]',
                subreddit=submission.subreddit.display_name,
                text=text,
                image_urls=image_urls,
                url=canonical_url,
                video_url=video_url
            )
            
        except Exception as e:
            logger.error(f"Error fetching Reddit post {url}: {type(e).__name__}: {str(e)}")
            return None
    
    def download_image(self, image_url: str) -> Optional[Path]:
        """Download a single image from URL."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            response = requests.get(image_url, headers=headers, stream=True, timeout=15)
            if response.status_code != 200:
                logger.warning(f"Failed to download image: HTTP {response.status_code}")
                return None
            
            # Check content type
            content_type = response.headers.get('Content-Type', '')
            if not content_type.startswith('image/'):
                logger.warning(f"URL is not an image: {content_type}")
                return None
            
            # Determine extension
            ext = 'jpg'
            if 'png' in content_type:
                ext = 'png'
            elif 'webp' in content_type:
                ext = 'webp'
            elif 'gif' in content_type:
                ext = 'gif'
            
            # Create temp file
            file_path = self.temp_dir / f"reddit_{hash(image_url)}.{ext}"
            
            # Download with size check
            total_size = 0
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=64 * 1024):
                    if not chunk:
                        continue
                    total_size += len(chunk)
                    if total_size > self.max_file_size_bytes:
                        logger.warning(f"Image exceeds size limit: {total_size} bytes")
                        file_path.unlink(missing_ok=True)
                        return None
                    f.write(chunk)
            
            return file_path
            
        except Exception as e:
            logger.error(f"Error downloading image {image_url}: {type(e).__name__}: {str(e)}")
            return None
    
    def download_images(self, post: RedditPost) -> List[Path]:
        """Download all images from a Reddit post."""
        downloaded_files = []
        
        # Limit to first 4 images (Discord embed limit)
        for image_url in post.image_urls[:4]:
            filepath = self.download_image(image_url)
            if filepath:
                downloaded_files.append(filepath)
        
        return downloaded_files
    
    def cleanup(self, filepath: Path) -> None:
        """Delete downloaded file."""
        try:
            if filepath.exists():
                filepath.unlink()
        except Exception:
            pass

