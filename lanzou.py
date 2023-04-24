import requests
import re
import json


def __get_post_data(frame_url: str):
    r = requests.get(frame_url, headers=headers)
    r.encoding = 'utf-8'
    signs = re.search(r'var ajaxdata = \'(.*?)\'', r.text).group(1)
    sign = re.search(r'\'sign\':\'(.*?)\'', r.text).group(1)
    websignkey = re.search(r'var wsk_sign = \'(.*?)\'', r.text).group(1)
    return {
        'action': 'downprocess',
        'signs': signs,
        'sign': sign,
        'websign': '',
        'websignkey': websignkey,
        'ves': 1,
    }


def __get_url(post_data) -> str:
    r = requests.post(base_url + '/ajaxm.php', headers=headers, data=post_data)
    r.encoding = 'utf-8'
    data = json.loads(r.text)
    down_url = data['dom'] + '/file/' + data['url']
    return down_url


def get_down_url(file_id: str) -> str:
    '''获取下载 URL'''
    full_url = base_url + '/' + file_id
    r = requests.get(full_url, headers=headers)
    r.encoding = 'utf-8'
    frame_url = base_url + re.search(r'\<iframe.*?src="([^"]{10,}?)"', r.text).group(1)
    post_data = __get_post_data(frame_url)
    down_url = __get_url(post_data)
    return down_url


base_url = 'https://www.lanzoui.com'
headers = {'User-Agent': 'github@oyps', 'Referer': base_url}
