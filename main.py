from collect import Get_list
from lanzou import get_down_url
import requests, threading, os, re

if not os.path.exists('file'):
    os.mkdir('file')


url = input('蓝奏云文件夹分享地址：')
password = input('请输入密码，可留空：')
get_list = Get_list()
get_list.get_list(url, password)
result = get_list.result
lock = threading.Lock()
sem = threading.Semaphore(5)
threads = []


def down(_id: str, name: str):
    name = re.sub(r'[\/:*?"<>|]', '', name)
    down_url = get_down_url(_id)
    lock.acquire()
    print(f'开始下载：{name}')
    lock.release()
    r = requests.get(
        down_url,
        headers={
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        },
    )
    open('file/' + name, 'wb').write(r.content)
    sem.release()


for i in result:
    _id = i['id']
    name = i['name_all']
    sem.acquire()
    thread = threading.Thread(target=down, args=(_id, name))
    thread.start()
    threads.append(thread)

for i in threads:
    i.join()

print('文件全部下载完成')
