const cheerio = require("cheerio");

/*
SCRAPER SETTINGS

You need to define the following values below:

- API_KEY --> Find this on your dashboard, or signup here to create a 
                free account here https://dashboard.scraperapi.com/signup

- NUM_CONCURRENT_THREADS --> Set this equal to the number of concurrent threads available
                in your plan. For reference: Free Plan (5 threads), Hobby Plan (10 threads),
                Startup Plan (25 threads), Business Plan (50 threads), 
                Enterprise Plan (up to 5,000 threads).

*/


const API_KEY = 'INSERT_API_KEY_HERE'; 
const NUM_CONCURRENT_THREADS = 5;

const scraperapiClient = require('scraperapi-sdk')(API_KEY)

// Example list of URLs to scrape
const urlsToScrape = [
    'http://quotes.toscrape.com/page/1/',
    'http://quotes.toscrape.com/page/2/',
    'http://quotes.toscrape.com/page/3/',
    'http://quotes.toscrape.com/page/4/',
    'http://quotes.toscrape.com/page/5/',
    'http://quotes.toscrape.com/page/6/',
    'http://quotes.toscrape.com/page/7/',
    'http://quotes.toscrape.com/page/8/',
    'http://quotes.toscrape.com/page/9/'
  ];


let freeThreads = NUM_CONCURRENT_THREADS;
let responsePromises = []

// Store scraped data in this list
let scrapedData = [];


const wait = ms => new Promise(resolve => setTimeout(() => resolve(true), ms));


const checkFreeThreads = (availableThreads, maxThreads) => {
    /*
        Function that returns True or False depending on if there is a concurrent thread 
        free or not. Used to manage the scrapers concurrency.
    */
    if(0 < availableThreads && availableThreads <= maxThreads){
        return true
    } else {
        return false
    }
}


const makeConcurrentRequest = async (inputUrl) => {
    /*
        Function that makes a request with the ScraperAPI SDK, while 
        also incremeneting/decrementing the available number of concurrent threads
        available to the scraper.
    */
    freeThreads--
    try {
        const response = await scraperapiClient.get(inputUrl);
        freeThreads++
        return response
    } catch (e) {
        freeThreads++
        return e
    }
}




(async () => {
    /*
        MAIN SCRAPER SCRIPT
        While there are still urls left to scrape, it will make requests and 
        parse the response whilst ensuring the scraper doesn't exceed the 
        number of concurrent threads available in the Scraper API plan.
    */

    while(urlsToScrape.length > 0){

        if(checkFreeThreads(freeThreads, NUM_CONCURRENT_THREADS)){

            // take URL from the list of URLs to scrape
            url = urlsToScrape.shift()

            try {
                // make request and return promise
                response = makeConcurrentRequest(url)

                // log promise so we can make sure all promises resolved before exiting scraper
                responsePromises.push(response)

                // once response is recieved then parse the data from the page
                response.then(htmlResponse => {

                        // load html with cheerio
                        let $ = cheerio.load(htmlResponse);

                        // find all quotes sections
                        let quotes_sections = $('div.quote')

                        // loop through the quotes sections and extract data
                        quotes_sections.each((index, element) => {
                            quote = $(element).find('span.text').text()
                            author = $(element).find('small.author').text()

                            // add scraped data to scrapedData array
                            scrapedData.push({
                                'quote': quote,
                                'author': author
                            })

                        });


                }).catch(error => {
                    console.log(error)
                })
   
            } catch (error){
                console.log(error)
            }
                
        }
        // if no freeThreads available then wait for 200ms before retrying.
        await wait(200);
    
    } // end of while loop

    
    // don't output scraped data until all promises have been resolved
    Promise.all(responsePromises).then(() => {
        console.log('scrapedData: ', scrapedData); 
    });


})();




