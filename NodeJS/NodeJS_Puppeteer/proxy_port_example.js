const puppeteer = require('puppeteer');
const cheerio = require('cheerio');

/*
SCRAPER SETTINGS

You need to define the following values below:

- API_KEY --> Find this on your dashboard, or signup here to create a 
                free account here https://dashboard.scraperapi.com/signup

*/


// ScraperAPI proxy configuration
PROXY_USERNAME = 'scraperapi';
PROXY_PASSWORD = 'API_KEY'; // <-- enter your API_Key here
PROXY_SERVER = 'proxy-server.scraperapi.com';
PROXY_SERVER_PORT = '8001';

// where scraped data will be stored
let scraped_quotes = [];

(async () => {
    const browser = await puppeteer.launch({
        ignoreHTTPSErrors: true,
        args: [
            `--proxy-server=http://${PROXY_SERVER}:${PROXY_SERVER_PORT}`
        ]
    });
    const page = await browser.newPage();
    await page.authenticate({
        username: PROXY_USERNAME,
        password: PROXY_PASSWORD,
      });
    

    try {
        await page.goto('http://quotes.toscrape.com/page/1/', {timeout: 180000});
        let bodyHTML = await page.evaluate(() => document.body.innerHTML);
        let $ = cheerio.load(bodyHTML);

        // find all quotes sections
        let quotes_sections = $('div.quote')

        // loop through the quotes sections and extract data
        quotes_sections.each((index, element) => {
            quote = $(element).find('span.text').text()
            author = $(element).find('small.author').text()

            // add scraped data to scraped_quotes array
            scraped_quotes.push({
                'quote': quote,
                'author': author
            })

        });

    } catch(err) {
        console.log(err);
    }
    
    await browser.close();
    console.log(scraped_quotes)
})();