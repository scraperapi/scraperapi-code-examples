import requests
from bs4 import BeautifulSoup
import concurrent.futures
import csv
from urllib.parse import urlencode


"""
SCRAPER SETTINGS

You need to define the following values below:

- API_KEY --> Find this on your dashboard, or signup here to create a 
                free account here https://www.scraperapi.com/signup
                
- NUM_RETRIES --> We recommend setting this to 5 retries. For most sites 
                95% of your requests will be successful on the first try,
                and 99% after 3 retries. 
                
- NUM_THREADS --> Set this equal to the number of concurrent threads available
                in your plan. For reference: Free Plan (5 threads), Hobby Plan (10 threads),
                Startup Plan (25 threads), Business Plan (50 threads), 
                Enterprise Plan (up to 5,000 threads).

"""
API_KEY = 'INSERT_API_KEY_HERE'
NUM_RETRIES = 3
NUM_THREADS = 5


## Example list of urls to scrape
list_of_urls = [
            'http://quotes.toscrape.com/page/1/',
           'http://quotes.toscrape.com/page/2/',
        ]


## we will store the scraped data in this list
scraped_quotes = []

def scrape_url(url):
    """
    SEND REQUESTS TO SCRAPER API AND PARSE DATA FROM THE HTML RESPONSE
    
    INPUT/OUTPUT: Takes a single url as input, and appends the scraped data to the "scraped_quotes" list.
    METHOD: Takes the input url, requests it via scraperapi and keeps retrying the request until it gets a 
    successful response (200 or 404 status code) or up to the number of retries you define in NUM_RETRIES. 
    If it did yield a successful response then it parses the data from the HTML response and adds it to the
    "scraped_quotes" list. You can easily reconfigure this to store the scraped data in a database.
    """
    
    params = {'api_key': API_KEY, 'url': url}
   
    # send request to scraperapi, and automatically retry failed requests
    for _ in range(NUM_RETRIES):
        try:
            response = requests.get('http://api.scraperapi.com/', params=urlencode(params))
            if response.status_code in [200, 404]:
                ## escape for loop if the API returns a successful response
                break
        except requests.exceptions.ConnectionError:
            response = ''
    
    
    ## parse data if 200 status code (successful response)
    if response.status_code == 200:
        
        """
        Insert the parsing code for your use case here...
        """
        
        ## Example: parse data with beautifulsoup
        html_response = response.text
        soup = BeautifulSoup(html_response, "html.parser")
        quotes_sections = soup.find_all('div', class_="quote")
        
        ## loop through each quotes section and extract the quote and author
        for quote_block in quotes_sections:
            quote = quote_block.find('span', class_='text').text
            author = quote_block.find('small', class_='author').text
            
            ## add scraped data to "scraped_quotes" list
            scraped_quotes.append({
                'quote': quote,
                'author': author
            })


"""
CONFIGURE CONCURRENT THREADS

Create thread pools up to the NUM_THREADS you define above and splits the urls you
want to scrape amongst these threads until complete. Takes as input:

- max_workers --> the maximum number of threads it will create. Here we set it to the
                value we defined in NUM_THREADS.
                
- function to execute --> the first input to the executor.map() function is the function
                we want to execute in each thread. Here we input the "scrape_url(url)"" 
                function which accepts a single url as input.
                
- input list --> the second input to the executor.map() function is the data we want to
                be split amongst the threads created. Here we input the "list_of_urls" we
                want to scrape.

"""
with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
    executor.map(scrape_url, list_of_urls)


print(scraped_quotes)