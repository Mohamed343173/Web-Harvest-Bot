import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time


class WebScraper:
    def __init__(self, base_url, delay=1):
        self.base_url = base_url
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.visited_urls = set()

    def fetch_page(self, url):
        try:
            time.sleep(self.delay)
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def parse_html(self, html_content):
        return BeautifulSoup(html_content, 'lxml')

    def extract_articles(self, soup):
        articles = []
        
        article_selectors = [
            'article',
            '.article',
            '.post',
            '.story',
            '.news-item',
            '.entry',
            '[class*="article"]',
            '[class*="post"]'
        ]
        
        article_elements = []
        for selector in article_selectors:
            found = soup.select(selector)
            if found:
                article_elements.extend(found)
                break
        
        if not article_elements:
            article_elements = soup.find_all(['article', 'div'], limit=20)
        
        for element in article_elements:
            article = self._extract_article_data(element)
            if article.get('title'):
                articles.append(article)
        
        return articles

    def _extract_article_data(self, element):
        article = {
            'title': '',
            'link': '',
            'description': '',
            'image': '',
            'date': ''
        }
        
        title_tag = element.find(['h1', 'h2', 'h3', 'h4'])
        if title_tag:
            article['title'] = title_tag.get_text(strip=True)
            link_tag = title_tag.find('a') or title_tag.find_parent('a')
            if link_tag and link_tag.get('href'):
                article['link'] = urljoin(self.base_url, link_tag['href'])
        
        if not article['link']:
            link_tag = element.find('a', href=True)
            if link_tag:
                article['link'] = urljoin(self.base_url, link_tag['href'])
        
        desc_selectors = ['p', '.description', '.summary', '.excerpt', '.lead']
        for selector in desc_selectors:
            desc_tag = element.select_one(selector) if '.' in selector else element.find(selector)
            if desc_tag:
                article['description'] = desc_tag.get_text(strip=True)[:500]
                break
        
        img_tag = element.find('img')
        if img_tag:
            img_src = img_tag.get('src') or img_tag.get('data-src') or img_tag.get('data-lazy-src')
            if img_src:
                article['image'] = urljoin(self.base_url, img_src)
        
        date_selectors = ['time', '.date', '.published', '.timestamp', '[datetime]']
        for selector in date_selectors:
            date_tag = element.select_one(selector) if '.' in selector else element.find(selector)
            if date_tag:
                article['date'] = date_tag.get('datetime', '') or date_tag.get_text(strip=True)
                break
        
        return article

    def extract_all_links(self, soup):
        links = []
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(self.base_url, href)
            if self._is_valid_url(full_url):
                links.append({
                    'text': a_tag.get_text(strip=True),
                    'url': full_url
                })
        return links

    def extract_all_images(self, soup):
        images = []
        for img_tag in soup.find_all('img'):
            src = img_tag.get('src') or img_tag.get('data-src')
            if src:
                images.append({
                    'src': urljoin(self.base_url, src),
                    'alt': img_tag.get('alt', ''),
                    'title': img_tag.get('title', '')
                })
        return images

    def find_pagination_links(self, soup):
        pagination_selectors = [
            '.pagination a',
            '.pager a',
            '.page-numbers',
            '[rel="next"]',
            'a[href*="page="]',
            'a[href*="/page/"]',
            '.next',
            '.load-more'
        ]
        
        next_links = []
        for selector in pagination_selectors:
            links = soup.select(selector)
            for link in links:
                href = link.get('href')
                if href:
                    full_url = urljoin(self.base_url, href)
                    if full_url not in self.visited_urls:
                        next_links.append(full_url)
        
        return list(set(next_links))

    def _is_valid_url(self, url):
        try:
            parsed = urlparse(url)
            base_parsed = urlparse(self.base_url)
            return parsed.netloc == base_parsed.netloc and parsed.scheme in ['http', 'https']
        except:
            return False

    def scrape_page(self, url):
        print(f"Scraping: {url}")
        self.visited_urls.add(url)
        
        html = self.fetch_page(url)
        if not html:
            return None
        
        soup = self.parse_html(html)
        
        return {
            'url': url,
            'articles': self.extract_articles(soup),
            'links': self.extract_all_links(soup),
            'images': self.extract_all_images(soup),
            'pagination': self.find_pagination_links(soup)
        }

    def scrape_multiple_pages(self, max_pages=5):
        all_data = {
            'articles': [],
            'links': [],
            'images': [],
            'pages_scraped': []
        }
        
        urls_to_scrape = [self.base_url]
        pages_scraped = 0
        
        while urls_to_scrape and pages_scraped < max_pages:
            current_url = urls_to_scrape.pop(0)
            
            if current_url in self.visited_urls:
                continue
            
            page_data = self.scrape_page(current_url)
            
            if page_data:
                all_data['articles'].extend(page_data['articles'])
                all_data['links'].extend(page_data['links'])
                all_data['images'].extend(page_data['images'])
                all_data['pages_scraped'].append(current_url)
                
                for pagination_url in page_data['pagination']:
                    if pagination_url not in self.visited_urls and pagination_url not in urls_to_scrape:
                        urls_to_scrape.append(pagination_url)
                
                pages_scraped += 1
                print(f"Progress: {pages_scraped}/{max_pages} pages scraped")
        
        unique_articles = []
        seen_titles = set()
        for article in all_data['articles']:
            if article['title'] and article['title'] not in seen_titles:
                seen_titles.add(article['title'])
                unique_articles.append(article)
        all_data['articles'] = unique_articles
        
        return all_data
