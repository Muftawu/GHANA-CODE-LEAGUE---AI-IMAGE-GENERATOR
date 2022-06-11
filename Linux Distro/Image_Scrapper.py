import pygame
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import io
import cv2
import numpy as np
from PIL import Image
import time
import numpy as np

from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--headless")

# Path for linux
PATH = "chromedriver_linux64/chromedriver"

# Path for windows
# PATH = "chromedriver.exe"
# query = input("Enter any word or sentence to generate an image:   ")

query1 = ""


# wd = webdriver.Chrome(PATH)
# wd.minimize_window()

def load_web_browser():
    # wd = webdriver.Chrome(path)
    wd = webdriver.Chrome(executable_path=PATH, options=chrome_options)
    return wd


def get_images_from_google(wd, delay, max_images, query):
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

    url = f"https://www.google.com/search?q={query}&tbm=isch&ved=2ahUKEwjykJ779tbzAhXhgnIEHSVQBksQ2-cCegQIABAA&oq={query}&gs_lcp=CgNpbWcQAzIHCAAQsQMQQzIHCAAQsQMQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzIECAAQQzoHCCMQ7wMQJ1C_31NYvOJTYPbjU2gCcAB4AIABa4gBzQSSAQMzLjOYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=7vZuYfLhOeGFytMPpaCZ2AQ&bih=817&biw=1707&rlz=1C1CHBF_enCA918CA918"
    wd.get(url)

    image_urls = set()
    skips = 0

    while len(image_urls) + skips < max_images:
        scroll_down(wd)

        thumbnails = wd.find_elements(By.CLASS_NAME, "Q4LuWd")

        for img in thumbnails[len(image_urls) + skips:max_images]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue

            images = wd.find_elements(By.CLASS_NAME, "n3VNCb")
            for image in images:
                if image.get_attribute('src') in image_urls:
                    max_images += 1
                    skips += 1
                    break

                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    print(f"Found {len(image_urls)}")

    return image_urls


def display_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")
            image = np.asarray(image)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # cv2.imshow("Generated Image", image)
            cv2.waitKey(0)

        print("Success")

    except Exception as e:
        print('FAILED - ', e)


def place_image_on_UI(win, x, y, image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = np.rot90(image)
    # 750, 20, 500, 600
    image = cv2.resize(image, (600, 540))
    generated_image = pygame.surfarray.make_surface(image).convert()
    generated_image = pygame.transform.flip(generated_image, True, False)
    win.blit(generated_image, (x, y))

# load_web_browser(PATH)
# urls = get_images_from_google(wd, 1, 1)
#
# for i, url in enumerate(urls):
#     download_image("", url, str(i) + ".jpg")
#
# wd.quit()
# wd.close()
