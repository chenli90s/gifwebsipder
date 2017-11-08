from gevent import monkey
import gevent
import socket
import re
import sys
import os


monkey.patch_all()


class WSCI:
    def __init__(self, app, port=8080, document_root='./'):
        self.port = port
        self.document_root = document_root
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('', port))
        print('server start port:', port)
        self.server_socket.listen(128)
        self.app = app

    def run_forever(self):
        while True:
            print('server listening ....')
            # 服务器开启
            client_socket, client_addr = self.server_socket.accept()
            gevent.spawn(self.handle_request, client_socket)

    def handle_request(self, client_socket):
        """处理接收请求"""
        while True:
            # 接收数据
            request_msg = client_socket.recv(1024)
            # 如果数据不为空
            if not request_msg:
                client_socket.close()
                return
            lines = request_msg.decode().splitlines()
            
            regx_msg = re.match('([^/]*) (/[^ ]*)', lines[0])
            request_method = regx_msg.group(1)
            request_path = regx_msg.group(2)
            request_headers = dict()
            if request_method == "GET":
                request_paths = request_path.split('?')
                if len(request_paths) > 1:
                    request_path = request_paths[0]
                    request_GET_param = request_paths[1]
                    request_headers['get_param'] = request_GET_param
            else:
                for index, line in enumerate(lines):
                    print(line)
            print('请求方法:', request_method, '请求路径:', request_path)
            if request_path == '/':
                request_path = '/index.html'
                
            if not request_path.endswith('.go'):
                self.handler_client_response(client_socket, request_path)
            else:
                
                for index,line in enumerate(lines):
                    if index>0 and line != '':
                        # print(index, line)
                        str = line.split(': ')
                        request_headers[str[0]] = str[1]
                response = self.app({'PATH_INFO': request_path,
                                     'REQUEST_HEADERS': request_headers}, self.start_response)
                response = self.handle_dyna_response(response)
                client_socket.send(response)
    
    def start_response(self, state, header):
        self.state = state
        self.header = header
        

    def handle_dyna_response(self, response):
        response_body = response.encode()
        
        response_header = self.header
        state = self.state
        
        header = 'HTTP/1.1 %s\r\n' % str(state)
        for key, value in response_header.items():
            header += "%s:%s \r\n" % (key, value)

        header += 'Content-Length: %s\r\n' % len(response_body)
        header += '\r\n'
        response = header.encode() + response_body
        return response

    def handler_client_response(self, client_socket, request_path):
        try:
            file = open(self.document_root + request_path, 'rb')
            content = file.read()
            content_length = os.path.getsize(self.document_root + request_path)
            file.close()

        except Exception as e:
            print('错误', e)
            response_header = 'HTTP/1.1 404 YOU PATH IS NONE\r\n'
            response_header += 'content-type: text/html; charset=utf-8\r\n'
            content = '<h1 style="color: red; text-align: center; margin-top: ' \
                      '100px">没有找到你需要的文件</h1>'.encode()
            response_header += 'Content-Length: %d\r\n' % len(content)
        else:
            response_header = 'HTTP/1.1 200 OK\r\n'
            # print(content_length)
            response_header += 'Content-Length: %d\r\n' % content_length
        finally:
            response_header += '\r\n'
            client_socket.send(response_header.encode() + content)




def main(app):
    input_args = sys.argv

    # 内建导入
    # 导入
    # sys.path.append('./dynamic')
    # sys.path.append('./lib')
    # modul = __import__('webapp')
    # app = getattr(modul, 'app')
    if len(input_args) > 1:
        server = WSCI(app, port=int(input_args[1]), document_root='./static')
        server.run_forever()
    else:
        server = WSCI(app, document_root='./static')
        server.run_forever()


if __name__ == '__main__':
    main()
