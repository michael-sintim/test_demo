import requests
from bs4 import BeautifulSoup
import csv
import time
import random

class WebScraper:
    def __init__(self, base_url):
        """
        Initialize the web scraper with a base URL and set up headers
        to mimic a browser request.
        """
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }

    def fetch_page(self, url):
        """
        Fetch the webpage content with error handling and politeness delay.
        
        :param url: URL of the webpage to scrape
        :return: BeautifulSoup object of the page content
        """
        try:
            # Add a random delay to be respectful to the website
            time.sleep(random.uniform(1, 3))
            
            # Send a GET request with custom headers
            response = requests.get(url, headers=self.headers)
            
            # Raise an exception for bad status codes
            response.raise_for_status()
            
            # Parse the content with BeautifulSoup
            return BeautifulSoup(response.content, 'html.parser')
        
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def scrape_books(self, num_pages=5):
        """
        Scrape book information from multiple pages.
        
        :param num_pages: Number of pages to scrape
        :return: List of dictionaries containing book information
        """
        all_books = []
        
        for page_num in range(1, num_pages + 1):
            # Construct the URL for each page
            page_url = f"{self.base_url}/catalogue/page-{page_num}.html"
            
            # Fetch the page
            soup = self.fetch_page(page_url)
            
            if not soup:
                print(f"Skipping page {page_num}")
                continue
            
            # Find all book containers
            book_containers = soup.find_all('article', class_='product_pod')
            
            # Extract information from each book
            for book in book_containers:
                # Extract title
                title = book.h3.a['title']
                
                # Extract price
                price = book.find('p', class_='price_color').text
                
                # Extract stock availability
                availability = book.find('p', class_='instock availability').text.strip()
                
                # Extract star rating
                star_rating = book.find('p', class_='star-rating')['class'][1]
                
                # Compile book information
                book_info = {
                    'title': title,
                    'price': price,
                    'availability': availability,
                    'star_rating': star_rating
                }
                
                all_books.append(book_info)
            
            print(f"Scraped page {page_num}")
        
        return all_books

    def save_to_csv(self, books, filename='books.csv'):
        """
        Save scraped book information to a CSV file.
        
        :param books: List of dictionaries containing book information
        :param filename: Name of the output CSV file
        """
        if not books:
            print("No books to save.")
            return
        
        # Specify the CSV columns
        keys = books[0].keys()
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                dict_writer = csv.DictWriter(csvfile, fieldnames=keys)
                dict_writer.writeheader()
                dict_writer.writerows(books)
            
            print(f"Successfully saved {len(books)} books to {filename}")
        
        except IOError as e:
            print(f"Error saving to CSV: {e}")

def main():
    # Example usage (Note: Replace with an actual website URL)
    base_url = "https://en.wikipedia.org/wiki/Web_scraping "
    
    # Create scraper instance
    scraper = WebScraper(base_url)
    
    # Scrape books
    books = scraper.scrape_books(num_pages=3)
    
    # Save to CSV
    scraper.save_to_csv(books)

if __name__ == "__main__":
    main()

# Important Notes for Responsible Web Scraping:
# 1. Always check the website's robots.txt file
# 2. Add delays between requests to avoid overwhelming the server
# 3. Respect the website's terms of service
# 4. Be aware of potential legal and ethical considerations
# 5. Some websites may have terms that prohibit scraping

# Required libraries (install via pip):
# - requests
# - beautifulsoup4
# 
# Install with:
# pip install requests beautifulsoup4