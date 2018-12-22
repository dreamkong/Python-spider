import os
import requests
from bs4 import BeautifulSoup

BASE_URL = 'http://www.mmjpg.com'

headers = {
    'Referer': "http://www.mmjpg.com",
    'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}


def get_page_count(url):
    '''获取套图总数'''
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        soup = BeautifulSoup(res.content.decode('utf-8'), 'lxml')
        return soup.select('div.pic > ul > li > span.title > a')[0]['href'].split('/')[-1]
    return None


def get_page(url):
    '''获取套图页面'''
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        return res.content.decode('utf-8')
    return None


def parse_page(url, html):
    '''解析套图页面'''
    soup = BeautifulSoup(html, 'lxml')
    image_title = soup.select('h2')[0].get_text()
    image_count = int(soup.select('#page a')[-2].get_text())
    image_urls = [url+'/'+str(i) for i in range(1, image_count+1)]
    for image_url in image_urls:
        print(image_url)
        res = requests.get(image_url, headers=headers)
        if res.status_code == 200:
            soup = BeautifulSoup(res.content.decode('utf-8'), 'lxml')
            img = soup.select('#content > a > img')[0]
            yield (image_title, img['src'])


def download_image(title, url):
    res = requests.get(url, headers=headers)
    if res.status_code == 200:
        if not os.path.exists(title):
            os.makedirs(title)
        with open(title+'/'+url.split('/')[-1], 'wb') as f:
            f.write(res.content)


def main():
    count = int(get_page_count(BASE_URL))
    urls = [BASE_URL + '/mm/' + str(i) for i in range(count, count-1, -1)]
    for url in urls:
        html = get_page(url)
        download_urls = parse_page(url, html)
        for title, download_url in download_urls:
            download_image(title, download_url)


if __name__ == "__main__":
    main()