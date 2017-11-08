from lib.webapp import Web
from lib.imgspider import *
import random

webapp = Web()

@webapp.router('/loadmore.go')
def index(request):
    num = request['get_param'].split('=')[1]
    url = 'http://tu.duowan.com/m/bxgif?offset=%d&order=created&math=%s'%(int(num)*30, str(random.random()))
    cont = get_content(url)
    str_json = load_more_data(cont)
    return str_json

@webapp.router('/getDetail.go')
def getDetail(request):
    id = request['get_param'].split('=')[1]
    url = 'http://tu.duowan.com/index.php?r=show/getByGallery/&gid=%d&_=1509462959270'%(int(id))
    cont = get_content(url)
    str_json = json_any(cont)
    return str_json




if __name__ == '__main__':
    webapp.run()