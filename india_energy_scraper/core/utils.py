import httpx
import logging
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse
from pathlib import Path
import os
import time

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

logger = setup_logger(__name__)

class RateLimitedClient:
    def __init__(self, requests_per_second: float = 1.0, user_agent: str = "AntigravityScraper/1.0 (+mailto:youremail@example.com)"):
        self.delay = 1.0 / requests_per_second
        self.last_request_time = 0.0
        self.client = httpx.Client(headers={"User-Agent": user_agent}, timeout=30.0)
        self.robot_parsers = {}
        
    def _check_robots(self, url: str) -> bool:
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        if base_url not in self.robot_parsers:
            rp = RobotFileParser()
            robots_url = f"{base_url}/robots.txt"
            try:
                rp.set_url(robots_url)
                rp.read()
                self.robot_parsers[base_url] = rp
            except Exception as e:
                logger.warning(f"Failed to read robots.txt for {base_url}: {e}")
                self.robot_parsers[base_url] = None
                return True # Allow if we can't fetch robots.txt, but warn
        
        rp = self.robot_parsers[base_url]
        if rp:
            return rp.can_fetch(self.client.headers["User-Agent"], url)
        return True

    def get(self, url: str, retries: int = 3, **kwargs) -> httpx.Response:
        if not self._check_robots(url):
            logger.warning(f"Access denied by robots.txt for {url}")
            raise Exception("Access denied by robots.txt")
            
        now = time.time()
        time_since_last = now - self.last_request_time
        if time_since_last < self.delay:
            time.sleep(self.delay - time_since_last)
            
        for attempt in range(retries):
            try:
                self.last_request_time = time.time()
                response = self.client.get(url, **kwargs)
                response.raise_for_status()
                return response
            except httpx.HTTPError as e:
                logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt == retries - 1:
                    raise
                time.sleep(2 ** attempt)  # Exponential backoff
