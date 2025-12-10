# Intelligent Web Scraper

## Overview
A Python-based intelligent web scraper with a modern web interface. Enter any website URL and instantly extract articles, links, and images. Features both a web UI and command-line interface.

## Project Structure
```
├── app.py            # Flask web application
├── main.py           # Command-line interface entry point
├── templates/
│   └── index.html    # Web interface template
├── src/
│   ├── __init__.py   # Package initialization
│   ├── scraper.py    # WebScraper class with extraction logic
│   └── exporter.py   # DataExporter class for CSV/JSON output
└── output/           # Directory for scraped data (auto-created)
```

## Features
- **Web Interface**: Modern dark-themed UI to enter URLs and view results
- **Single & Multi-page Scraping**: Scrape one page or follow pagination automatically
- **Article Extraction**: Finds titles, descriptions, dates, links, and images
- **Link Collection**: Extracts all links from the page
- **Image Collection**: Finds all images with alt text
- **Multiple Export Formats**: JSON and CSV support (CLI mode)
- **Progress Tracking**: Displays scraping progress
- **Error Handling**: Graceful handling of failed requests

## Usage

### Web Interface
1. Open the web app in your browser
2. Enter a website URL in the input field
3. Set the number of pages to scrape (1-10)
4. Click "Start Scraping"
5. View articles, links, and images in separate tabs

### Command-Line Interface
```bash
python main.py https://example.com
```

### CLI Options
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
```

## Dependencies
- Flask: Web framework
- beautifulsoup4: HTML parsing
- requests: HTTP requests
- pandas: CSV export
- lxml: Fast HTML parser

## Recent Changes
- Added web interface with URL input and results display (December 2025)
- Initial project setup (December 2025)
