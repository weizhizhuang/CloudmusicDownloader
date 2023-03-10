import requests


headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"}

def dlder(url,file_name):
    response = requests.get(url, headers=headers)
    content = response.content

    with open(file_name, mode='wb') as f:
        f.write(content)
    print(f'下载完成: {file_name}')