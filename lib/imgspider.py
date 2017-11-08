import requests
from lxml import etree
import json


header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
}

def get_content(url):
     response = requests.get(url, header)
     return response.content

def load_more_data(content):
    dict_json = json.loads(content.decode())
    html = etree.HTML(dict_json['html'])
    li_html = html.xpath('//li')
    list_data = []
    for li in li_html:
        dict_data = {}
        dict_data['link'] = li.xpath('./a/@href')[0].split('/')[-1].split('.')[0]
        dict_data['img_src'] = li.xpath('./a/img/@src')[0]
        dict_data['title'] = li.xpath('./em/a/text()')[0].split('：')[1]
        list_data.append(dict_data)
    str_json = json.dumps(dict(code=True, data=list_data), ensure_ascii=False)
    return str_json


def load_content(content, file_name):
    with open(file_name, 'wb') as f:
        f.write(content)

def json_any(content):
    dict_json = json.loads(content.decode())
    str_json = json.dumps(dict_json, ensure_ascii=False)
    # load_content(str_json.encode(), 'res.json')
    return str_json

if __name__ == '__main__':
    # content = get_content('http://tu.duowan.com/m/bxgif?offset=30&order=created&math=0.2098298096892781')
    content = get_content('http://tu.duowan.com/index.php?r=show/getByGallery/&gid=135730&_=1509462959270')
    # load_more_data(content)
    json_any(content)