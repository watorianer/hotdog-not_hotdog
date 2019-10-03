# this scraper only works on reddit links
# with a returned search site! not on any
# other site

# import the necessary packages
import requests
import urllib.request
import os
import argparse
import time
from bs4 import BeautifulSoup

# build argument parser and parse the
# arguments
ap = argparse.ArgumentParser()
ap.add_argument('-o', '--output', required=True,
    help='path where to save the downloaded images')
ap.add_argument('-u', '--url', required=True,
    help='initial url where to scrape the images from')
ap.add_argument('-n', '--nof', required=True,
    help='number of sites to scrape')
args = vars(ap.parse_args())

# initialize a few variables to use in the crawler
counter = 0
forbidden_counter = 0
pictures_per_site = 25
url = args['url']
header = {'user-agent': 'hotdog-downloader'}

while (counter < int(args['nof'])):
    # make request for the desired page
    response = requests.get(url, headers=header)
    source = response.text

    # if we get a valid response, parse the page
    # and try to extract the images
    if response.status_code == 200:
        forbidden_counter = 0
        # parse the page
        print('[INFO] Response okay')
        soup = BeautifulSoup(source, 'lxml')

        # find all image links and download images
        footers = soup.find_all('div', class_='search-result-footer')
        print('[INFO] Downloading {} pictures on site number {} of {}'.format(
            pictures_per_site, counter+1, int(args['nof'])))
        for (i, footer) in enumerate(footers):
            try:
                img_url = footer.a['href']
                img_path = os.path.join(args['output'], 'reddit-{}.jpg'.format(
                    i + (counter * pictures_per_site)))
                urllib.request.urlretrieve(img_url, img_path)
            except:
                pass

        # go to next page and increment counter
        time.sleep(2)
        try:
            if counter == 0:
                # on the first page the next button is in the first a
                url = soup.find('div', class_='nav-buttons').span.a['href']
            else:
                # on the second page the next button is in the second a
                url = soup.find('div', class_='nav-buttons').span.find_all('a')[1]['href']
        except IndexError as identifier:
            print('[INFO] Next button was not found')
        

        # extracting the images was successful so we
        # increment the counter
        counter = counter + 1
    else:
        print('[INFO] Response forbidden, sleep for 10 seconds and try again')
        forbidden_counter = forbidden_counter + 1
        if forbidden_counter == 4:
            print('[INFO] Response was five times in a row not successfull, abort mission')
            print('[INFO] The mission was aborted after {} pages were crawled'.format(counter))
            break
        time.sleep(10)