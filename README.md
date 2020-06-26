# Non-API-FaceBook-Scraper [2020]
### Adapted from [LeviBorodenko](https://github.com/LeviBorodenko/non-api-fb-scraper)
_Scrape public posts from any group or user into a .csv file without needing to register for any API access. Additionally, post images will be saved into a folder 'Pictures' and the image title and subtitle will be added to the csv._


![result](https://i.imgur.com/EgObJWb.png)


### How to use it?

Firstly, make sure you have selenium >= 3.141.0 and FireFox installed.

Use `scraper.py` to collect the data. 
```
usage: scrape.py [-h] [--pages PAGES [PAGES ...]] [-d DEPTH]
Data Collection
arguments:
  -h, --help            show this help message and exit
  --pages PAGES [PAGES ...]
                        List the pages you want to scrape
                        for recent posts
  
  -d DEPTH, --depth DEPTH
                        How many recent posts you want to gather in
                        multiples of (roughly) 8.
```
Example: ```python scraper.py --pages DonaldTrump senatorsanders -d 20```
____
The output is `posts.csv` inside the script folder.
