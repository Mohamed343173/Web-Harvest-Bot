from flask import Flask, render_template, request, jsonify
from src.scraper import WebScraper
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SESSION_SECRET', 'dev-secret-key')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    url = data.get('url', '')
    max_pages = data.get('pages', 1)
    
    if not url:
        return jsonify({'error': 'Please provide a URL'}), 400
    
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    try:
        scraper = WebScraper(url, delay=0.5)
        
        if max_pages == 1:
            page_data = scraper.scrape_page(url)
            if page_data:
                result = {
                    'success': True,
                    'url': url,
                    'articles': page_data['articles'],
                    'links': page_data['links'][:50],
                    'images': page_data['images'][:30],
                    'stats': {
                        'pages_scraped': 1,
                        'total_articles': len(page_data['articles']),
                        'total_links': len(page_data['links']),
                        'total_images': len(page_data['images'])
                    }
                }
            else:
                return jsonify({'error': 'Failed to scrape the website'}), 500
        else:
            all_data = scraper.scrape_multiple_pages(max_pages=max_pages)
            result = {
                'success': True,
                'url': url,
                'articles': all_data['articles'],
                'links': all_data['links'][:100],
                'images': all_data['images'][:50],
                'stats': {
                    'pages_scraped': len(all_data['pages_scraped']),
                    'total_articles': len(all_data['articles']),
                    'total_links': len(all_data['links']),
                    'total_images': len(all_data['images'])
                }
            }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
