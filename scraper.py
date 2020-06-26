from selenium import webdriver
import time
import csv
import urllib.request
import os


class Collector: #(object) in orig.
    """Collector of recent FaceBook posts.
           Note: We bypass the FaceBook-Graph-API by using a 
           selenium FireFox instance! 
           This is against the FB guide lines and thus not allowed.

           USE THIS FOR EDUCATIONAL PURPOSES ONLY. DO NOT ACTAULLY RUN IT.
    """

    def __init__(self, pages=["oxfess"], corpus_file="posts.csv", depth=5, delay=2):
        super(Collector, self).__init__()
        self.pages = pages
        self.dump = corpus_file
        self.depth = depth + 1
        self.delay = delay
        # browser instance
        self.browser = webdriver.Firefox()

        # creating CSV header
        with open(self.dump, "w", newline='', encoding="utf-8") as save_file:
            writer = csv.writer(save_file)
            writer.writerow(["Source", "utime", "Text", "Link_Title", "Link_Subtitle"])

    def strip(self, string):
        """Helping function to remove all non alphanumeric characters"""
        words = string.split()
        words = [word for word in words if "#" not in word]
        string = " ".join(words)
        clean = ""
        for c in string:
            if str.isalnum(c) or (c in [" ", ".", ","]):
                clean += c
        return clean

    def collect_page(self, page):
        # navigate to page
        self.browser.get('https://www.facebook.com/' + page + '/')

        # Scroll down depth-times and wait delay seconds to load
        # between scrolls
        for scroll in range(self.depth):

            # Scroll down to bottom
            self.browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(self.delay)

        # Once the full page is loaded, we can start scraping
        with open(self.dump, "a+", newline='', encoding="utf-8") as save_file:
            writer = csv.writer(save_file)
            posts = self.browser.find_elements_by_class_name(
                "userContentWrapper")

            for post in posts:

                # Creating first CSV row entry with the page name (eg. "DonaldTrump")
                analysis = [page]

                # Creating utime entry.
                time_element = post.find_element_by_css_selector(
                    "abbr")
                utime = time_element.get_attribute("data-utime")
                analysis.append(utime)

                # Creating post text entry
                text = ""
                text_elements = post.find_elements_by_css_selector(
                    "p")
                for p in text_elements:
                    text += self.strip(p.text)
                analysis.append(text)

                # Creating (image) link title entry
                try:
                    link_title_elements = post.find_elements_by_class_name("mbs")
                    link_title = link_title_elements[0].find_elements_by_css_selector("a")[0].get_attribute('textContent')
                    analysis.append(self.strip(link_title))
                except:
                    analysis.append("")

                # Creating (image) link subtitle entry
                try:
                    link_subtitle = post.find_elements_by_class_name("_6m7")[0].get_attribute('textContent')
                    analysis.append(self.strip(link_subtitle))
                except:
                    analysis.append("")

                # Write row to csv
                writer.writerow(analysis)

                # Donload post image
                try:
                    image = post.find_elements_by_css_selector(
                        "img")
                    src = image[1].get_attribute("src")
                    urllib.request.urlretrieve(src, "Pictures/" + str(page) + str(utime) + ".jpg")
                except:
                    pass


    def collect(self):
        if not os.path.isdir('Pictures'):
            os.mkdir('Pictures')
        for page in self.pages:
            self.collect_page(page)

if __name__ == '__main__':

    import argparse


    parser = argparse.ArgumentParser(description='Non API public FB miner')

    parser.add_argument('--pages', nargs='+',
                        dest="pages",
                        help="List the pages you want to scrape for recent posts")

    parser.add_argument("-d", "--depth", action="store",
                        dest="depth", default=5, type=int,
                        help="How many recent posts you want to gather -- in multiples of (roughly) 8.")

    args = parser.parse_args()
    

    #args, _ = parser.parse_known_args()

    C = Collector(pages=args.pages, depth=args.depth)

    C.collect()

