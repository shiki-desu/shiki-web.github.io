import json
import requests
from pathlib import Path
from bs4 import BeautifulSoup

url = 'http://xsb.scnu.edu.cn/tongzhigonggao/'
headers = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
"Referer": "https://www.google.com",
"Cookie": "sessionid=abc123"
}

def crawler():
    data_list = []
    try:
        response = requests.get(url,headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text,'lxml')
    except Exception as e:
        return f'出错了:{e}'
    newlist = soup.find('div',class_='newslist listshow cl')
    news = newlist.find_all('li')[:11]
    for new in news:
        #链接
        url_next_web = new.find('a')
        link = url_next_web.get('href') if url_next_web else None
        #日期
        date_span = new.find('span')
        date = date_span.get_text(strip=True) if date_span else None
        #标题
        title = new.get_text(strip=True)
        if date and title.startswith(date):
            title = title[len(date):].strip()
        if title and link and date:
            new_item = {
                '标题':title,
                '链接':link,
                '日期':date
            }
        data_list.append(new_item)
                # 把数据打包成json并储存到data/notices.json
        data = json.dumps(data_list, ensure_ascii=False, indent=2)
        path = Path('data/notices.json')
        path.write_text(data, encoding='utf-8')
crawler()