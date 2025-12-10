import json
import csv
import pandas as pd
from datetime import datetime
import os


class DataExporter:
    def __init__(self, output_dir='output'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def _generate_filename(self, prefix, extension):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return os.path.join(self.output_dir, f"{prefix}_{timestamp}.{extension}")

    def export_to_json(self, data, filename=None):
        if filename is None:
            filename = self._generate_filename('scraped_data', 'json')
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Data exported to JSON: {filename}")
        return filename

    def export_articles_to_csv(self, articles, filename=None):
        if filename is None:
            filename = self._generate_filename('articles', 'csv')
        
        if not articles:
            print("No articles to export")
            return None
        
        df = pd.DataFrame(articles)
        df.to_csv(filename, index=False, encoding='utf-8')
        
        print(f"Articles exported to CSV: {filename}")
        return filename

    def export_links_to_csv(self, links, filename=None):
        if filename is None:
            filename = self._generate_filename('links', 'csv')
        
        if not links:
            print("No links to export")
            return None
        
        df = pd.DataFrame(links)
        df.to_csv(filename, index=False, encoding='utf-8')
        
        print(f"Links exported to CSV: {filename}")
        return filename

    def export_images_to_csv(self, images, filename=None):
        if filename is None:
            filename = self._generate_filename('images', 'csv')
        
        if not images:
            print("No images to export")
            return None
        
        df = pd.DataFrame(images)
        df.to_csv(filename, index=False, encoding='utf-8')
        
        print(f"Images exported to CSV: {filename}")
        return filename

    def export_all(self, data):
        files = {}
        
        files['json'] = self.export_to_json(data)
        
        if data.get('articles'):
            files['articles_csv'] = self.export_articles_to_csv(data['articles'])
        
        if data.get('links'):
            files['links_csv'] = self.export_links_to_csv(data['links'])
        
        if data.get('images'):
            files['images_csv'] = self.export_images_to_csv(data['images'])
        
        return files

    def print_summary(self, data):
        print("\n" + "="*50)
        print("SCRAPING SUMMARY")
        print("="*50)
        print(f"Pages scraped: {len(data.get('pages_scraped', []))}")
        print(f"Articles found: {len(data.get('articles', []))}")
        print(f"Links found: {len(data.get('links', []))}")
        print(f"Images found: {len(data.get('images', []))}")
        print("="*50)
        
        if data.get('articles'):
            print("\nSample articles:")
            for i, article in enumerate(data['articles'][:5], 1):
                print(f"  {i}. {article['title'][:60]}..." if len(article['title']) > 60 else f"  {i}. {article['title']}")
