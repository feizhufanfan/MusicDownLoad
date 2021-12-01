# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
import os
from sys import argv
import re
import requests
import time
from multiprocessing.pool import ThreadPool
def GetJson(filePAth):
    file_Object=open(filePAth,"r",encoding="UTF-8")
    data=file_Object.read()
    json_data=json.loads(data)
    return json_data
def GetsingList(JsonData):
    singlist=[]
    playerList=JsonData["playerlists"]
    for list in playerList:
        for key,value in JsonData[list].items():
            if (key=="tracks"):
                for item in value:
                    singlist.append(item)

    return singlist


def Url_response(url):
    path,url=url
    r=requests.get(url,stream=True)
    with open(path,"wb") as f:
        for ch in r:
            f.write(ch)


def GetDownLoadList(path,data):
    for value in data:

        id,title,artist=value["id"],value["title"],value["artist"]
        title = title.replace("/", "")
        title = title.replace("\"", "\'")
        print('下载[{file}]'.format(file=title))
        # char_index=0
        # for char in title:
        #     if not (char in range(128)):
        #         title[char_index]=""
        #     char_index+=1
        # artist = artist.replace("/", "")
        # artist = artist.replace("\"", "\'")
        # for char in artist:
        #     if not (char in range(128)):
        #         artist[char_index] = ""
        #     char_index += 1
        size = 0  # 初始化已下载大小
        chunk_size = 1024  # 每次下载的数据大小
        id=re.findall("\d+",id)
        filepath = path + "/" + artist + "-" +  title+ ".mp3"
        if not os.path.exists(path):
            os.makedirs(path)
        if os.path.exists(filepath):
            continue
        url_data="http://music.163.com/song/media/outer/url?id="+id[0]+".mp3"
        start = time.time()  # 下载开始时间
        r = requests.get(url_data, stream=True)
        if r.status_code != 200:
            print("资源地址异常")
            continue

        if not "Content-Length" in r.headers.keys():
            print("资源地址异常")
            continue

        content_size = int(r.headers['Content-Length'])  # 下载文件总大小


        print('开始下载[{file}]:{size:.2f} MB'.format(file=title,size=content_size / chunk_size / 1024))  # 开始下载，显示下载文件大小

        with open(filepath, "wb") as f:
            for data in r.iter_content(chunk_size = chunk_size):
                f.write(data)
                size+=len(data)
                print(
                    '\r' + '[下载进度]:%s%.2f%%' % ('>' * int(size * 50 / content_size), float(size / content_size * 100)),
                    end=' ')
        f.close()
        end = time.time()  # 下载结束时间
        print('下载完成times: %.2f秒' % (end - start))  # 输出下载用时时间



def main(filePath):
    # Use a breakpoint in the code line below to debug your script.
    data=GetJson(filePath)
    singlist= GetsingList(data)
    GetDownLoadList("./mymusic",singlist)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(argv[1])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
