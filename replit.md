# Intelligent Web Scraper

## Overview
A Python-based intelligent web scraper that automatically visits websites and extracts useful information including articles, links, images, and descriptions. The extracted data can be saved in CSV or JSON formats.

## Project Structure
```
├── main.py           # Command-line interface entry point
├── src/
│   ├── __init__.py   # Package initialization
│   ├── scraper.py    # WebScraper class with extraction logic
│   └── exporter.py   # DataExporter class for CSV/JSON output
└── output/           # Directory for scraped data (auto-created)
```

## Features
- **Single & Multi-page Scraping**: Scrape one page or follow pagination automatically
- **Article Extraction**: Finds titles, descriptions, dates, links, and images
- **Link Collection**: Extracts all links from the page
- **Image Collection**: Finds all images with alt text
- **Multiple Export Formats**: JSON and CSV support
- **Progress Tracking**: Displays scraping progress in console
- **Error Handling**: Graceful handling of failed requests

## Usage

### Basic Usage
```bash
python main.py https://example.com
```

### Options
- `--pages, -p`: Maximum pages to scrape (default: 1)
- `--delay, -d`: Delay between requests in seconds (default: 1.0)
- `--output, -o`: Output directory (default: output)
- `--format, -f`: Output format: all, json, or csv (default: all)

### Examples
```bash
# Scrape 3 pages from BBC
python main.py https://www.bbc.com/news --pages 3

# Export only JSON with 2 second delay
python main.py https://example.com --format json --delay 2

# Custom output directory
python main.py https://example.com --output my_data
```

## Dependencies
- beautifulsoup4: HTML parsing
- requests: HTTP requests
- pandas: CSV export
- lxml: Fast HTML parser

## Recent Changes
- Initial project setup (December 2025)
