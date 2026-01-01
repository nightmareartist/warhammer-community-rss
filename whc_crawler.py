import requests
from bs4 import BeautifulSoup
from datetime import datetime, UTC
import xml.etree.ElementTree as ET

def crawl_warhammer_news():
    url = "https://www.warhammer-community.com/en-gb/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('a', class_='btn-cover')
    
    items = []
    for article in articles:
        title = article.get('title', '').strip()
        href = article.get('href', '')
        
        if title and href:
            full_url = f"https://www.warhammer-community.com{href}" if href.startswith('/') else href
            items.append({'title': title, 'url': full_url})
    
    return items

def generate_rss(items, output_file='feed.xml'):
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

if __name__ == '__main__':
    items = crawl_warhammer_news()
    generate_rss(items)
    print(f"Generated RSS feed with {len(items[:10])} items")
