import json
import requests
from requests.exceptions import RequestException
import re
import time


def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/101.0.4951.54 Safari/537.36'
        }
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return res.text
        return None
    except RequestException:
        return None
 
 
def parse_one_page(response):
    pattern = re.compile(
        '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.'
        '*?star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>',
        re.S
    )
    items = re.findall(pattern, response)
    for item in items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2].strip(),
            'actors': item[3].strip()[3:] if len(item[3]) > 3 else '',
            'time': item[4].strip()[4:] if len(item[4]) > 4 else '',
            'score': item[5].strip() + item[6].strip()
        }
 
 
def write_to_file(content):
    with open('猫眼Top100榜单', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
 
 
def main(offset):
    url = 'https://www.maoyan.com/board/4?offset=' + str(offset)
    response = get_one_page(url)
    for item in parse_one_page(response):
        print(item)
        write_to_file(item)
 
 
if __name__ == '__main__':
    for i in range(10):
        main(offset=i * 10)
        print(i)
        time.sleep(1)
