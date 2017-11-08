import re
import sys
import lib.server

__all__ = ['Web']


class Web:
    def __init__(self):
        self.routers = dict()
    
    def run(self):
        lib.server.main(self.app)
    
    def app(self, environ, start_response):
        path = environ['PATH_INFO']
        request_headers = environ['REQUEST_HEADERS']
        self.start_response = start_response
        self.response_header = {'Content-Type': 'text/html; charset=utf-8'}
        self.start_response('200 OK', self.response_header)
        # try:
            # 根据路径调用方法
            # response_body = eval(path[1:-3])(path)
        response_body = self.routers[path](request_headers)
        # except Exception as e:
        #     response_body = '你的路径写的不对：%s' % e
        return response_body
    
    def router(self, path):
        
        def dec(func):
            self.routers[path] = func
            return func
        
        return dec
    
    def read_file(self, path):
        path = re.sub(r'.py', '.html', path)
        with open('templates' + path, 'rb') as file:
            return file.read().decode('utf-8')

    # def set_header(self, header):
    #     # self.response_header = dict(self.response_header, header)
    #     self.response_header = header