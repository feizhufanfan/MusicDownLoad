# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import json
import os
from sys import argv
import re
import requests
from time import time
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
        id=re.findall("\d+",id)
        url_data="http://music.163.com/song/media/outer/url?id="+id[0]+".mp3"
        r = requests.get(url_data, stream=True)
        title=title.replace("/","")
        artist=artist.replace("/","")

        if not os.path.exists(path):
            os.makedirs(path)
        filepath=path+"/"+title+"-"+artist+".mp3"
        with open(filepath, "wb") as f:
            for ch in r:
                f.write(ch)
        f.close()

def Downloads(filename,path,url):

    pass

def main(filePath):
    # Use a breakpoint in the code line below to debug your script.
    data=GetJson(filePath)
    singlist= GetsingList(data)
    GetDownLoadList("./mymusic",singlist)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(argv[1])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
