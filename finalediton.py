import pprint
import os
import subprocess

import requests
import re
import json
from tqdm import tqdm
from poprogress import simple_progress
import tkinter as tk
import tkinter.ttk
from time import sleep


judeg = False
check_hit = False
window = tk.Tk()
window.title('bilibili download')
window.geometry('640x480')

var = tk.StringVar()
var_b = tk.StringVar()
var.set('输入网址')
var_b.set('确认')
l = tk.Label(window, textvariable=var, width=55, height=2, font=('Arial'))
l.pack()

l_copyright = tk.Label(window, text='Copyright © 2023 yun. All Right Reserved', height=3)
l_copyright.pack(side='bottom')

e = tk.Entry(window, show=None, width=50)
e.pack()

t = tk.Text(window, height=2)


def jindutiao():
    from poprogress import simple_progress

    a_list = [1, 2, 3, 4, 5, 6, 7, 8] * 1000000

    for a in simple_progress(a_list):
        pass


def get_url():
    global judeg
    judeg = False

    global check_hit
    if check_hit == False:
        check_hit = True
        var.set('processing')
        p = tk.ttk.Progressbar(window)
        p.pack()
        p['maximum'] = 100
        p['length'] = 280

        def value_bar():
            for i in range(100):
                p['value'] = i + 10
                sleep(0.001)
                window.update()

        value_bar()


    else:
        check_hit = False
        var.set('输入网址')

    global url
    url = e.get()
    headers = {'referer': 'https://www.bilibili.com/',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82'}
    response = requests.get(url=url, headers=headers)

    # tittle=re.findall('"true">(.*?)_哔哩哔哩_bilibili</title>',response.text)[0]  #获取视频标题

    html_data = re.findall('window.__playinfo__=(.*?)</script>', response.text)[0]
    json_data = json.loads(html_data)
    json_print = json.dumps(html_data, indent=4, ensure_ascii=False, sort_keys=False, separators=(',', ':'))
    # pprint.pprint(json_data)
    # 提取音频和视频url 根据冒号，提取左边的内用
    audio_url = json_data['data']['dash']['audio'][0]['baseUrl']
    video_url = json_data['data']['dash']['video'][0]['baseUrl']
    audio_content = requests.get(url=audio_url, headers=headers).content
    video_content = requests.get(url=video_url, headers=headers).content
    res_a = requests.get(url=audio_url, headers=headers, stream=True)
    res_v = requests.get(url=video_url, headers=headers, stream=True)
    # 403 没有访问权限 需要加请求头(headers)参数
    print(audio_url)
    print(video_url)
    content_size_a = int(res_a.headers['Content-Length']) / 1024
    content_size_v = int(res_v.headers['Content-Length']) / 1024
    filename1 = 'audio'
    filename2 = 'video'
    filename = 'download'
    if not os.path.exists(filename):
        os.mkdir(filename)
    # with open(filename1+'.mp3',mode='wb')as f:
    #     f.write(audio_content)
    # with open(filename2+'.mp4',mode='wb')as f:
    #     f.write(video_content)

    with open(os.path.join(filename, filename1 + '.mp3'), 'wb+') as f:
        # for audio_content in tqdm(iterable=response.iter_content(1024),
        #                  total=content_size_a,
        #                  unit='k',
        #                  desc='downloading'):
        #     f.write(audio_content)
        f.write(audio_content)
    with open(os.path.join(filename, filename2 + '.mp4'), 'wb+') as f:
        # for video_content in tqdm(iterable=response.iter_content(1024),
        #                  total=content_size_v,
        #                  unit='k',
        #                  desc='downloading'):
        #     f.write(video_content)
        f.write(video_content)
    with open(os.path.join(filename, 'html-json.txt'), 'w') as f:

        f.write(json_print)
    cmd = r'ffmpeg\bin\ffmpeg.exe -y -i download\video.mp4 -i download\audio.mp3 -c:v copy -c:a aac -strict experimental download\完整版.mp4'
    subprocess.Popen(cmd, shell=True)
    sleep(0.5)

    var.set('Finished')
    judeg = True

def check_video():
    global judeg
    if judeg == True:
        var.set('下载成功')
        judeg = False
        path = os.getcwd()
        os.startfile('download')

    else:
        var.set('下载失败,请输入正确网址')



b = tk.Button(window, textvariable=var_b, width=15, height=2, command=get_url)
b.pack()


b_check = tk.Button(window, text='检查', width=15, height=2, command=check_video)
b_check.pack()


window.mainloop()
