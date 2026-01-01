# Warhammer Community RSS

A simple Python script that crawls the Warhammer Community website and generates an RSS feed from the latest news articles.

## Requirements

- Python 3.11 or higher
- `requests` library
- `beautifulsoup4` library

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd warhammer-community-rss
```

2. Create a virtual environment:
```bash
python3 -m venv warhammer_rss
source warhammer_rss/bin/activate
```

3. Install dependencies:
```bash
pip install requests beautifulsoup4
```

## Usage

Run the script manually:
```bash
python whc_crawler.py
```

This generates `feed.xml` in the current directory containing the 10 most recent articles.

## Automated Updates

Set up a cron job to run the crawler automatically. Edit your crontab:
```bash
crontab -e
```

Add this line to run twice daily (midnight and noon):
```bash
0 */12 * * * /path/to/warhammer_rss/bin/python /path/to/whc_crawler.py
```

For a different schedule, adjust the cron expression:
- `0 */6 * * *` - Every 6 hours
- `0 8,20 * * *` - At 8 AM and 8 PM
- `0 0 * * *` - Once daily at midnight

## Serving the Feed

### Option 1: Local RSS Reader
Point your RSS reader to the local `warhammer_feed.xml` file.

### Option 2: Web Server
Serve the XML file with nginx or Apache:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location /feed.xml {
        root /path/to/;
        alias feed.xml;
    }
}
```
## Output

The script generates a standard RSS 2.0 feed with:
- Article title
- Link to the full article
- Last build date

## Customization

To change the number of articles in the feed, modify line 30 in `whc_crawler.py`:
```python
for item_data in items[:10]:  # Change 10 to desired number
```

## License

BSD 3-Clause License - feel free to modify and distribute.
