import requests
from bs4 import BeautifulSoup
from datetime import datetime, UTC
import xml.etree.ElementTree as ET
import sys

def crawl_warhammer_news():
    url = "https://www.warhammer-community.com/en-gb/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        print("Error: Request timed out after 30 seconds", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("Error: Failed to connect to Warhammer Community", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.HTTPError as e:
        print(f"Error: HTTP {e.response.status_code} - {e.response.reason}", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to fetch page - {e}", file=sys.stderr)
        sys.exit(1)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('a', class_='btn-cover')
    
    if not articles:
        print("Warning: No articles found - site structure may have changed", file=sys.stderr)
        return []
    
    items = []
    for article in articles:
        title = article.get('title', '').strip()
        href = article.get('href', '')
        
        if title and href:
            full_url = f"https://www.warhammer-community.com{href}" if href.startswith('/') else href
            items.append({'title': title, 'url': full_url})
    
    if not items:
        print("Warning: Articles found but no valid title/href pairs extracted", file=sys.stderr)
    
    return items

def generate_rss(items, output_file='warhammer_feed.xml'):
    try:
        rss = ET.Element('rss', version='2.0')
        channel = ET.SubElement(rss, 'channel')
        
        ET.SubElement(channel, 'title').text = 'Warhammer Community News'
        ET.SubElement(channel, 'link').text = 'https://www.warhammer-community.com'
        ET.SubElement(channel, 'description').text = 'Latest news from Warhammer Community'
        ET.SubElement(channel, 'lastBuildDate').text = datetime.now(UTC).strftime('%a, %d %b %Y %H:%M:%S GMT')
        
        for item_data in items[:10]:
            item = ET.SubElement(channel, 'item')
            ET.SubElement(item, 'title').text = item_data['title']
            ET.SubElement(item, 'link').text = item_data['url']
            ET.SubElement(item, 'guid', isPermaLink='true').text = item_data['url']
        
        tree = ET.ElementTree(rss)
        ET.indent(tree, space='  ')
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
        
        print(f"Successfully generated RSS feed with {len(items[:10])} items")
        
    except PermissionError:
        print(f"Error: Permission denied writing to {output_file}", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"Error: Failed to write RSS feed - {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    items = crawl_warhammer_news()
    
    if items:
        generate_rss(items)
    else:
        print("Error: No items to generate RSS feed", file=sys.stderr)
        sys.exit(1)
