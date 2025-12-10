import argparse
import sys
from src.scraper import WebScraper
from src.exporter import DataExporter


def main():
    parser = argparse.ArgumentParser(
        description='Intelligent Web Scraper - Extract articles, links, and images from websites',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py https://example.com
  python main.py https://news.bbc.co.uk --pages 3
  python main.py https://example.com --output my_data --delay 2
  python main.py https://example.com --format json
        """
    )
    
    parser.add_argument('url', help='The URL of the website to scrape')
    parser.add_argument('--pages', '-p', type=int, default=1, 
                        help='Maximum number of pages to scrape (default: 1)')
    parser.add_argument('--delay', '-d', type=float, default=1.0,
                        help='Delay between requests in seconds (default: 1.0)')
    parser.add_argument('--output', '-o', type=str, default='output',
                        help='Output directory for scraped data (default: output)')
    parser.add_argument('--format', '-f', choices=['all', 'json', 'csv'], default='all',
                        help='Output format: all, json, or csv (default: all)')
    
    args = parser.parse_args()
    
    if not args.url.startswith(('http://', 'https://')):
        args.url = 'https://' + args.url
    
    print("\n" + "="*50)
    print("INTELLIGENT WEB SCRAPER")
    print("="*50)
    print(f"Target URL: {args.url}")
    print(f"Max pages: {args.pages}")
    print(f"Request delay: {args.delay}s")
    print(f"Output directory: {args.output}")
    print(f"Output format: {args.format}")
    print("="*50 + "\n")
    
    try:
        scraper = WebScraper(args.url, delay=args.delay)
        
        if args.pages == 1:
            data = scraper.scrape_page(args.url)
            if data:
                data = {
                    'articles': data['articles'],
                    'links': data['links'],
                    'images': data['images'],
                    'pages_scraped': [args.url]
                }
        else:
            data = scraper.scrape_multiple_pages(max_pages=args.pages)
        
        if not data:
            print("Error: Failed to scrape the website")
            sys.exit(1)
        
        exporter = DataExporter(output_dir=args.output)
        
        exporter.print_summary(data)
        
        if args.format == 'json':
            exporter.export_to_json(data)
        elif args.format == 'csv':
            exporter.export_articles_to_csv(data.get('articles', []))
            exporter.export_links_to_csv(data.get('links', []))
            exporter.export_images_to_csv(data.get('images', []))
        else:
            exporter.export_all(data)
        
        print("\nScraping completed successfully!")
        
    except KeyboardInterrupt:
        print("\nScraping interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nError during scraping: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
