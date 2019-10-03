from google_images_download import google_images_download

response = google_images_download.googleimagesdownload()

arguments = {'keywords': 'hotdog', 'format': 'jpg', 'output_directory': '.\\downloads\\', 'limit': 2000, 'chromedriver': '.\\webdriver\\chromedriver.exe'}
response.download(arguments)