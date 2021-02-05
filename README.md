# amazon_scraper


- Make python virtual environment using following command in cmd (i'll ommit my current working directory shown on cmd)
```
$ python -m venv vscrapy
```

- After activating virtual environment, install requirements as follows,
```	
$ python -m pip install --upgrade pip
$ pip install Twisted-20.3.0-cp38-cp38-win_amd64.whl
$ pip install scrapy pywin32 scrapy_proxies scrapy-user-agents
```

7) Now all done, start scraping, put all links in the urls_list.txt file and run the following command, 

"https://www.amazon.com/s?rh=n%3A172635&fs=true&ref=lp_172635_sar" 

```
$ scrapy crawl amazon -a pages=1 -o output.csv
```

- lets update the products, use the same csv you used above

```
$ scrapy crawl amazon_update -a 
```

it will only update the products already scraped, only look for price and stock status

we can merge this data with original table later to update the product prices in our database using product link as the key

### Design of scrapper

1) don't scrape what is not available from amazon
2) mark currently unavailable, temporarily out of stock, pre-order, available in x days products as out of stock
3) get product name, price, discounted price, variant information, stock status and also download the product image


### Current Functions

1) Can go to unlimited links and scrape all items from those pages, but page layout MUST be the same as example page
2) Get most of the relevant information from the page
3) Uses proxies and try to avoid amazon bot detection using other methods 
