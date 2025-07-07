import requests
import time
from typing import List, Optional, Dict, Any
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from utils.logger import logger
from utils.config import Config


class WebScraperTool:
    """Web scraping tool using BeautifulSoup"""
    
    def __init__(self):
        self.timeout = Config.REQUEST_TIMEOUT
        self.max_retries = Config.MAX_RETRIES
        self.rate_limit_delay = Config.RATE_LIMIT_DELAY
        
        # Headers to mimic a real browser
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def scrape_url(self, url: str) -> Optional[str]:
        """
        Scrape content from a single URL
        
        Args:
            url: URL to scrape
            
        Returns:
            Extracted text content or None if failed
        """
        logger.log_tool_usage("WebScraperTool", f"Scraping: {url}")
        
        for attempt in range(self.max_retries):
            try:
                # Add rate limiting
                if attempt > 0:
                    time.sleep(self.rate_limit_delay * attempt)
                
                response = requests.get(
                    url, 
                    headers=self.headers, 
                    timeout=self.timeout,
                    allow_redirects=True
                )
                response.raise_for_status()
                
                # Parse HTML content
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Remove script and style elements
                for script in soup(["script", "style", "nav", "footer", "header", "aside"]):
                    script.decompose()
                
                # Extract text content
                text_content = self._extract_meaningful_text(soup)
                
                if text_content and len(text_content.strip()) > 100:
                    logger.log_tool_usage("WebScraperTool", f"Successfully scraped {len(text_content)} characters")
                    return text_content
                else:
                    logger.warning(f"Insufficient content scraped from {url}")
                    return None
                    
            except requests.exceptions.RequestException as e:
                logger.warning(f"Request failed for {url} (attempt {attempt + 1}): {str(e)}")
                if attempt == self.max_retries - 1:
                    logger.error(f"Failed to scrape {url} after {self.max_retries} attempts")
                    return None
            except Exception as e:
                logger.error(f"Unexpected error scraping {url}: {str(e)}")
                return None
        
        return None
    
    def _extract_meaningful_text(self, soup: BeautifulSoup) -> str:
        """
        Extract meaningful text content from BeautifulSoup object
        
        Args:
            soup: BeautifulSoup parsed HTML
            
        Returns:
            Cleaned text content
        """
        # Priority tags for content extraction
        content_selectors = [
            'article',
            'main',
            '.content',
            '.post-content',
            '.entry-content',
            '#content',
            '.article-body',
            '.post-body'
        ]
        
        # Try to find main content area
        main_content = None
        for selector in content_selectors:
            elements = soup.select(selector)
            if elements:
                main_content = elements[0]
                break
        
        # If no main content area found, use body
        if main_content is None:
            main_content = soup.find('body') or soup
        
        # Extract text from paragraphs, headings, and list items
        text_elements = main_content.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'div'])
        
        text_parts = []
        for element in text_elements:
            text = element.get_text(strip=True)
            if text and len(text) > 20:  # Filter out very short text
                text_parts.append(text)
        
        # Join text parts and clean up
        full_text = '\n'.join(text_parts)
        
        # Clean up whitespace
        lines = full_text.split('\n')
        cleaned_lines = [line.strip() for line in lines if line.strip()]
        
        return '\n'.join(cleaned_lines)
    
    def scrape_multiple_urls(self, urls: List[str], max_content_per_url: int = 5000) -> List[str]:
        """
        Scrape content from multiple URLs
        
        Args:
            urls: List of URLs to scrape
            max_content_per_url: Maximum characters per URL
            
        Returns:
            List of scraped content strings
        """
        scraped_contents = []
        
        for url in urls:
            try:
                content = self.scrape_url(url)
                if content:
                    # Truncate content if too long
                    if len(content) > max_content_per_url:
                        content = content[:max_content_per_url] + "..."
                    scraped_contents.append(content)
                
                # Rate limiting between requests
                time.sleep(self.rate_limit_delay)
                
            except Exception as e:
                logger.error(f"Error scraping {url}: {str(e)}")
                continue
        
        logger.info(f"Successfully scraped {len(scraped_contents)} out of {len(urls)} URLs")
        return scraped_contents
    
    def is_valid_url(self, url: str) -> bool:
        """
        Check if URL is valid and accessible
        
        Args:
            url: URL to validate
            
        Returns:
            True if URL is valid and accessible
        """
        try:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                return False
            
            # Skip certain file types
            skip_extensions = ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.zip', '.rar']
            if any(url.lower().endswith(ext) for ext in skip_extensions):
                return False
            
            # Quick HEAD request to check if URL is accessible
            response = requests.head(url, headers=self.headers, timeout=5, allow_redirects=True)
            return response.status_code == 200
            
        except Exception:
            return False
    
    def filter_valid_urls(self, urls: List[str]) -> List[str]:
        """
        Filter out invalid or inaccessible URLs
        
        Args:
            urls: List of URLs to filter
            
        Returns:
            List of valid URLs
        """
        valid_urls = []
        for url in urls:
            if self.is_valid_url(url):
                valid_urls.append(url)
            else:
                logger.debug(f"Filtered out invalid URL: {url}")
        
        logger.debug(f"Filtered {len(valid_urls)} valid URLs from {len(urls)} total")
        return valid_urls