from lxml import html
import os
import json
import re
import sys
import requests
from time import sleep
import random

conditions = ['New', 'Good', 'Wearable', 'Broken', 'Bad']
sizes = ['Small', 'Medium', 'Large', 'X-Large', 'XX-Large']
regex = re.compile("\/dp\/.{10}\/")


def AmzonParser(url):
    headers = {
        'User-Agent': 'Mozilla/69.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/12.0.1'}
    page = requests.get(url, headers=headers)
    sleep(2)
    doc = html.fromstring(page.content)
    XPATH_NAME = '//h1[@id="title"]//text()'
    XPATH_SALE_PRICE = '//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()'
    XPATH_ORIGINAL_PRICE = '//td[contains(text(),"List Price") or contains(text(),"M.R.P") or contains(text(),"Price")]/following-sibling::td/text()'
    XPATH_COLOR = '//div[@class="a-row"]/span[@class="selection"]//text()'
    XPATH_BRAND = '//a[@id="bylineInfo"]//text()'
    XPATH_CTYPE = '//a[@class="a-link-normal a-color-tertiary"]//text()'
    XPATH_DETAIL = '//div[@id="feature-bullets"]//text()'
    XPATH_IMG = '//div[@id="imgTagWrapperId" and @class="imgTagWrapper"]/img/@data-old-hires'
    XPATH_EXTERNAL = '//a[@class="a-link-normal"]/@href'

    RAW_NAME = doc.xpath(XPATH_NAME)
    RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
    RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)
    RAW_COLOR = doc.xpath(XPATH_COLOR)
    RAW_BRAND = doc.xpath(XPATH_BRAND)
    RAW_CTYPE = doc.xpath(XPATH_CTYPE)
    RAW_DETAIL = doc.xpath(XPATH_DETAIL)
    RAW_IMG = doc.xpath(XPATH_IMG)
    RAW_EXTERNAL = doc.xpath(XPATH_EXTERNAL)

    NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
    SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
    ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
    CONDITION = random.sample(conditions, 1)[0]
    SIZE = random.sample(sizes, 1)[0]
    COLOR = ' '.join(''.join(RAW_COLOR).split()) if RAW_COLOR else None
    BRAND = ' '.join(''.join(RAW_BRAND).split()) if RAW_BRAND else None
    CTYPE = ' > '.join([i.strip() for i in RAW_CTYPE]) if RAW_CTYPE else None
    DETAIL = '; '.join([i.strip() for i in RAW_DETAIL if len(i.strip()) > 0]) if RAW_DETAIL else None
    IMG = ''.join(RAW_IMG[0]).split()[0] if RAW_IMG else None

    if RAW_EXTERNAL and len(RAW_EXTERNAL) > 0:
        EXTERNAL = [m[0].replace('/dp/', '').replace('/', '') for m in
                    [[j for j in re.findall('\/dp\/.{10}\/', i)] for i in RAW_EXTERNAL] if len(m) > 0]
    else:
        EXTERNAL = []

    if not ORIGINAL_PRICE:
        ORIGINAL_PRICE = SALE_PRICE

    if page.status_code != 200:
        raise ValueError('captha')
    data = {
        'NAME': NAME,
        'SALE_PRICE': SALE_PRICE,
        'ORIGINAL_PRICE': ORIGINAL_PRICE,
        'CONDITION': CONDITION,
        'SIZE': SIZE,
        'COLOR': COLOR,
        'BRAND': BRAND,
        'CTYPE': CTYPE,
        'IMAGE': IMG,
        'DETAIL': DETAIL,
        'CLOSED': False,
        'URL': url
    }
    return data, EXTERNAL


def ReadAsin():
    AsinList = [str(i) for i in sys.argv[2:]]
    extracted_data = json.load(open('./data.json'))
    used_urls = []

    add_length = int(sys.argv[1])
    max_length = add_length + len(extracted_data)
    total_length = len(extracted_data)
    cnt = 0
    print("Current #data:" + str(len(extracted_data)))
    if len(extracted_data) >= max_length:
        print("json file capacity reached")
    while len(extracted_data) < max_length and len(AsinList) > 0:
        try:
            curr_url = AsinList.pop(0)
            url = "http://www.amazon.com/dp/{}".format(curr_url)
            print("Processing: {}".format(url))
            data, more_links = AmzonParser(url)
            used_urls.append(curr_url)
            if len([i is not None for i in data.values()]) > 2:
                extracted_data.append(data)
                if total_length < max_length and len(more_links) > 0:
                    more_links = [link for link in more_links if link not in used_urls + AsinList]
                    total_length += len(more_links)
                    AsinList = AsinList + more_links
                    print("{} mode urls left to crawl".format(max_length - total_length))
                cnt += 1
            else:
                print("Crawler for {} blocked. Trying again later.".format(curr_url))
                AsinList.append(curr_url)

            if cnt % 10 == 0:
                f = open('data.json', 'w')
                json.dump(extracted_data, f, indent=4)
            sleep(random.randint(10, 20))

        except Exception as e:
            print(e)
            continue


if __name__ == "__main__":
    ReadAsin()
