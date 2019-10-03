# a simple web scraper to get images on reddit
# only works on non search pages and old reddit

# import the necessary packages
from selenium import webdriver
import time
import os
import argparse
import urllib.request

# later construct here the argument parser
# and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('-o', '--output', required=True,
    help='path where to save the downloaded images')
ap.add_argument('-u', '--url',
    default='https://old.reddit.com/r/food/top/?sort=top&t=week',
    help='initial url where to scrape the images from')
ap.add_argument('-n', '--nof', required=True,
    help='number of sites to scrape')
args = vars(ap.parse_args())

# initialize some variables for later use
# reddit shows 25 images per default
url = args['url']
images_endpoint = 26
images_start = images_endpoint - 25
current_page = 1
last_page = int(args['nof']) + 1

# initialize the webdriver and open
# the desired webpage
driver = webdriver.Chrome('.\\webdriver\\chromedriver.exe')

# scrape the current page
for current_page in range(1, last_page): 

    driver.get(url)  

    # find all image urls on the page
    print('[INFO] Download images on site {} of site {}'.format(current_page, last_page-1))
    for image_counter in range(images_start, images_endpoint):
        # get the urls for the images
        first_post = driver.find_element_by_xpath('//*[@data-rank="{}"]'.format(image_counter))
        img_url = first_post.get_attribute('data-url')

        # download the image
        img_path = os.path.join(args['output'], '{}.jpg'.format(image_counter))
        urllib.request.urlretrieve(img_url, img_path)

    # get the next page, on the first page
    # to crawl there is no back button, so the
    # xpath to the next button is different
    if current_page == 1:
        next_button = driver.find_element_by_xpath('//*[@id="siteTable"]/div[55]/span/span/a')
        url = next_button.get_attribute('href')
        time.sleep(2)
    else:
        next_button = driver.find_element_by_xpath('//*[@id="siteTable"]/div[55]/span/span[3]/a')
        url = next_button.get_attribute('href')
        time.sleep(2)
    
    # get the next image start and endpoint and
    # increment the counter for the current page
    images_endpoint = (25 * (current_page + 1)) + 1
    images_start = images_endpoint - 25
    current_page += 1