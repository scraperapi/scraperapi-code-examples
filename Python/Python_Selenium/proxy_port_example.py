from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities  
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json  

"""
SCRAPER SETTINGS

You need to define the following values below:

- API_KEY --> Find this on your dashboard, or signup here to create a 
                free account here https://dashboard.scraperapi.com/signup

- RETRY_TIMES  --> We recommend setting this to 2-3 retries, in case a request fails. 
                For most sites 95% of your requests will be successful on the first try,
                and 99% after 3 retries. 

"""

API_KEY = 'YOUR_API_KEY'
NUM_RETRIES = 2

proxy_options = {
    'proxy': {
        'http': f'http://scraperapi:{API_KEY}@proxy-server.scraperapi.com:8001',
        'https': f'http://scraperapi:{API_KEY}@proxy-server.scraperapi.com:8001',
        'no_proxy': 'localhost,127.0.0.1'
    }
}


## we will store the scraped data in this list
scraped_quotes = []

## urls to scrape
url_list = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]


def status_code_first_request(performance_log):
    """
        Selenium makes it hard to get the status code of each request,
        so this function takes the Selenium performance logs as an input
        and returns the status code of the first response.
    """
    for line in performance_log:
        try:
            json_log = json.loads(line['message'])
            if json_log['message']['method'] == 'Network.responseReceived':
                return json_log['message']['params']['response']['status']
        except:
            pass
    return json.loads(response_recieved[0]['message'])['message']['params']['response']['status']



## optional --> define Selenium options
option = webdriver.ChromeOptions()
option.add_argument('--headless') ## --> comment out to see the browser launch.
option.add_argument('--no-sandbox')
option.add_argument('--disable-dev-sh-usage')

## enable Selenium logging
caps = DesiredCapabilities.CHROME
caps['goog:loggingPrefs'] = {'performance': 'ALL'}


## set up Selenium Chrome driver
driver = webdriver.Chrome(ChromeDriverManager().install(), 
                            options=option, 
                            desired_capabilities=caps,
                            seleniumwire_options=proxy_options)

for url in url_list:

    for _ in range(NUM_RETRIES):
            try:
                driver.get(url)
                performance_log = driver.get_log('performance')
                status_code = status_code_first_request(performance_log)
                if status_code in [200, 404]:
                    ## escape for loop if the API returns a successful response
                    break
            except requests.exceptions.ConnectionError:
                driver.close()


    if status_code == 200:
        ## feed HTML response into BeautifulSoup
        html_response = driver.page_source
        soup = BeautifulSoup(html_response, "html.parser")

        ## find all quotes sections
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

        ## example --> click on the link for the next page
        link = driver.find_element_by_link_text("Next →")
        link.click()

print(scraped_quotes)

