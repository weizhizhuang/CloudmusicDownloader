import flet
from fleter import HeaderBar, SwichThemeButton
import requests
from dld import *
#from flet import Page, Checkbox, ElevatedButton, Row, TextField, Text, ProgressBar, FilePicker, ProgressRing

def getSongs(id):
    url='https://cm-api.scc.lol/playlist/detail?id='+id
    res = requests.post(url).json()
    return res['playlist']['tracks']#[0]['name']
def getMp3Url(id):
    url='https://cm-api.scc.lol/song/url?id='+id
    res = requests.post(url).json()
    return res['data']#[0]['url']
def pushBark(n):
    try:
        key=open('key.txt','r',encoding='utf-8').read()
    except:
        return
    url=f'https://api.day.app/{key}/CloudMusic_Downloader/{n}首歌曲下载完成?group=cm_downloader&icon=https://s2.loli.net/2023/03/10/1ygLRmWDzr3FOjc.png'
    requests.post(url)

cbList=[]
idList=[]
nameList=[]
def main(page: flet.Page):
    global cbList
    titlebar = HeaderBar(page, title="CloudMusic Playlist Downloader", title_align="left")
    titlebar.controls.insert(1, SwichThemeButton(page))
    page.add(titlebar)

    def getPlaylist(e):
        global cbList,idList,nameList
        #clear all
        for i in range(len(cbList)):
            lv.controls.remove(cbList[i])
        cbList=[]
        idList=[]
        nameList=[]
        #get new
        ring=flet.ProgressRing()
        inp.controls.append(ring)
        page.update()
        l=getSongs(new_task.value)
        #append lists
        for i in l:
            #print(i['name'],i['id'])
            idList.append(i['id'])
            nameList.append(i['name'])
            cb=flet.Checkbox(label=i['name'],on_change=isDownload)
            cbList.append(cb)
            lv.controls.append(cb)
        inp.controls.remove(ring)
        page.update()
        print(nameList,'\n',idList)

    def check(e):
        global cbList
        if checkBtn.text=='全选' and cbList:
            for i in cbList:
                i.value=True
            checkBtn.text='全不选'
        elif checkBtn.text=='全不选' and cbList:
            for i in cbList:
                i.value=False
            checkBtn.text='全选'
        isDownload(1)
        page.update()
    
    def isDownload(e):
        global cbList
        t=0
        for i in cbList:
            if i.value==True and selectPathBtn.text!='选择下载路径':
                downloadBtn.disabled=False
                t=1
                page.update()
                return
        if t==0:
            downloadBtn.disabled=True
        page.update()
    
    def getPath(e: flet.FilePickerResultEvent):
        #file_picker.get_directory_path()
        global p
        p=e.path
        selectPathBtn.text=p
        isDownload(1)
        page.update()
    file_picker = flet.FilePicker(on_result=getPath)
    page.overlay.append(file_picker)
    def download(e):
        global p,idList
        page.add(bar)
        n=0
        for i in range(len(idList)):
            if cbList[i].value==True:
                name=nameList[i]
                resp=getMp3Url(str(idList[i]))
                url=resp[0]['url']
                try:
                    dlder(url,f'{p}\{name}.mp3')
                    n+=1
                except:
                    page.controls.remove(bar)
                    page.add(flet.Text("下载失败"))
                    return
        page.controls.remove(bar)
        page.add(flet.Text("下载完成"))
        pushBark(n)
        return


    new_task = flet.TextField(hint_text="歌单id", width=300)
    inp=flet.Row([new_task, flet.ElevatedButton("Get", on_click=getPlaylist)])
    page.add(inp)
    checkBtn=flet.ElevatedButton("全选", on_click=check)
    lv = flet.ListView(expand=1, spacing=10, padding=20)
    downloadBtn=flet.ElevatedButton("Download", on_click=download, disabled=True)
    selectPathBtn=flet.ElevatedButton("选择下载路径", on_click=lambda _: file_picker.get_directory_path())
    bar=flet.ProgressBar(width=400)
    page.add(checkBtn,lv,flet.Row([selectPathBtn,downloadBtn]))
    page.update()
    

flet.app(target=main)


#7834420381
#7772229014
