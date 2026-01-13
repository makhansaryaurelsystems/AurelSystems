import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json
import time
import sys
from collections import defaultdict
from datetime import datetime

class OutputLogger:
    """Custom logger that writes to both terminal and file"""
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.log = open(filename, 'w', encoding='utf-8')
        
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        
    def flush(self):
        self.terminal.flush()
        self.log.flush()
        
    def close(self):
        self.log.close()

class WebsiteCrawler:
    def __init__(self, base_url, delay=1):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.visited = set()
        self.pages_data = {}
        self.link_map = defaultdict(list)
        self.delay = delay
        
    def is_valid_url(self, url):
        """Check if URL belongs to the same domain"""
        parsed = urlparse(url)
        return parsed.netloc == self.domain or parsed.netloc == ''
    
    def normalize_url(self, url):
        """Normalize URL by removing fragments and trailing slashes"""
        parsed = urlparse(url)
        normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        return normalized.rstrip('/')
    
    def extract_content(self, soup, url):
        """Extract meaningful content from the page"""
        page_data = {
            'url': url,
            'title': '',
            'meta_description': '',
            'headings': [],
            'paragraphs': [],
            'images': [],
            'internal_links': [],
            'external_links': []
        }
        
        # Extract title
        if soup.title:
            page_data['title'] = soup.title.string.strip() if soup.title.string else ''
        
        # Extract meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            page_data['meta_description'] = meta_desc['content'].strip()
        
        # Extract headings
        for i in range(1, 7):
            headings = soup.find_all(f'h{i}')
            for h in headings:
                text = h.get_text(strip=True)
                if text:
                    page_data['headings'].append({
                        'level': i,
                        'text': text
                    })
        
        # Extract paragraphs
        paragraphs = soup.find_all('p')
        for p in paragraphs:
            text = p.get_text(strip=True)
            if text:
                page_data['paragraphs'].append(text)
        
        # Extract images
        images = soup.find_all('img')
        for img in images:
            src = img.get('src', '')
            alt = img.get('alt', '')
            if src:
                page_data['images'].append({
                    'src': urljoin(url, src),
                    'alt': alt
                })
        
        # Extract links
        links = soup.find_all('a', href=True)
        for link in links:
            href = link['href']
            full_url = urljoin(url, href)
            link_text = link.get_text(strip=True)
            
            if self.is_valid_url(full_url):
                page_data['internal_links'].append({
                    'url': self.normalize_url(full_url),
                    'text': link_text
                })
            else:
                page_data['external_links'].append({
                    'url': full_url,
                    'text': link_text
                })
        
        return page_data
    
    def crawl_page(self, url):
        """Crawl a single page and extract its content"""
        normalized_url = self.normalize_url(url)
        
        if normalized_url in self.visited:
            return
        
        print(f"Crawling: {normalized_url}")
        self.visited.add(normalized_url)
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(normalized_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            page_data = self.extract_content(soup, normalized_url)
            
            self.pages_data[normalized_url] = page_data
            
            # Build link map (which pages link to which)
            for link in page_data['internal_links']:
                target_url = link['url']
                self.link_map[target_url].append({
                    'from': normalized_url,
                    'text': link['text']
                })
            
            # Recursively crawl internal links
            for link in page_data['internal_links']:
                target_url = link['url']
                if target_url not in self.visited:
                    time.sleep(self.delay)  # Be polite
                    self.crawl_page(target_url)
                    
        except Exception as e:
            print(f"Error crawling {normalized_url}: {str(e)}")
    
    def save_results(self, filename='website_migration_data.json'):
        """Save crawled data to JSON file"""
        output = {
            'base_url': self.base_url,
            'total_pages': len(self.pages_data),
            'pages': self.pages_data,
            'link_map': dict(self.link_map)
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\nCrawling complete!")
        print(f"Total pages crawled: {len(self.pages_data)}")
        print(f"Data saved to: {filename}")
    
    def generate_sitemap(self, filename='sitemap.txt'):
        """Generate a simple sitemap"""
        with open(filename, 'w') as f:
            for url in sorted(self.pages_data.keys()):
                f.write(f"{url}\n")
        print(f"Sitemap saved to: {filename}")

# Main execution
if __name__ == "__main__":
    # Setup output logging
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = f'crawler_output_{timestamp}.out'
    logger = OutputLogger(output_file)
    sys.stdout = logger
    
    print("=" * 70)
    print("WEBSITE CRAWLER FOR MIGRATION")
    print("=" * 70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Output file: {output_file}")
    print("=" * 70)
    print()
    
    base_url = "https://www.aurelsystems.com/"
    
    # Create crawler instance
    crawler = WebsiteCrawler(base_url, delay=1)
    
    # Start crawling
    print("Starting website crawl...")
    print(f"Base URL: {base_url}\n")
    
    try:
        crawler.crawl_page(base_url)
        
        # Save results
        json_file = f'aurelsystems_migration_data_{timestamp}.json'
        sitemap_file = f'aurelsystems_sitemap_{timestamp}.txt'
        
        crawler.save_results(json_file)
        crawler.generate_sitemap(sitemap_file)
        
        # Print detailed summary
        print("\n" + "=" * 70)
        print("CRAWL SUMMARY")
        print("=" * 70)
        print(f"Total pages crawled: {len(crawler.pages_data)}")
        print(f"Total URLs visited: {len(crawler.visited)}")
        print()
        
        # Pages with most incoming links
        print("Top 10 pages by incoming links:")
        print("-" * 70)
        sorted_links = sorted(crawler.link_map.items(), 
                             key=lambda x: len(x[1]), 
                             reverse=True)[:10]
        for i, (url, links) in enumerate(sorted_links, 1):
            print(f"{i:2d}. [{len(links):2d} links] {url}")
        
        print()
        
        # Pages with most content
        print("Pages with most paragraphs:")
        print("-" * 70)
        pages_by_content = sorted(
            crawler.pages_data.items(),
            key=lambda x: len(x[1]['paragraphs']),
            reverse=True
        )[:10]
        for i, (url, data) in enumerate(pages_by_content, 1):
            print(f"{i:2d}. [{len(data['paragraphs']):3d} paragraphs] {data['title'][:50]}")
            print(f"     {url}")
        
        print()
        
        # Image statistics
        total_images = sum(len(data['images']) for data in crawler.pages_data.values())
        print(f"Total images found: {total_images}")
        
        # External links
        all_external = set()
        for data in crawler.pages_data.values():
            for link in data['external_links']:
                all_external.add(link['url'])
        print(f"Unique external links: {len(all_external)}")
        
        print()
        print("=" * 70)
        print("OUTPUT FILES GENERATED")
        print("=" * 70)
        print(f"1. {json_file} - Complete structured data")
        print(f"2. {sitemap_file} - List of all URLs")
        print(f"3. {output_file} - This log file")
        print()
        print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
    except KeyboardInterrupt:
        print("\n\nCrawl interrupted by user.")
        print(f"Partial results saved. Pages crawled so far: {len(crawler.pages_data)}")
    except Exception as e:
        print(f"\n\nError during crawl: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        # Restore stdout and close log file
        sys.stdout = logger.terminal
        logger.close()
        print(f"\nAll output has been saved to: {output_file}")