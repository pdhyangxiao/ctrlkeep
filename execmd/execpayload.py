import os, subprocess

# os.system('dir')  #执行系统命令，没有获取返回值

# while True:
#     cmd = input()
#     result = os.popen(cmd)       #执行系统命令，返回值为result
#     res = result.read()
#     for line in res.splitlines():
#         print(line)

# 用subprocess库获取返回值。
# while True:
#     cwd = 'F:\isofile'
#     cmd = input()
#     p = subprocess.Popen(cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE)
#     out, err = p.communicate()
#     for line in out.splitlines():
#         try:
#             print(line.decode())
#         except:
#             line = "con't decode... %s" % line
#             print(line)

class execpayload():
    cwd = None

    @classmethod
    def exec_cmd(cls, cmd):

        cmds = cmd.split('&')
        for tmp_cmd in cmds:
            tmp_cmd = tmp_cmd.lstrip()
            if tmp_cmd.startswith('cd '):
                cls.cwd = tmp_cmd[3:]
            elif tmp_cmd.strip() == 'c:' or tmp_cmd.strip() == 'd:' or tmp_cmd.strip() == 'e:' or tmp_cmd.strip() == 'f:' or tmp_cmd.strip() == 'g:' or tmp_cmd.strip() == 'h:':
                cls.cwd = tmp_cmd[:2]
            # print("切换至目录：%s" % cls.cwd)

        p = subprocess.Popen(cmd, shell=True, cwd=cls.cwd, stdout=subprocess.PIPE)
        out, err = p.communicate()

        result = ''

        # 报错执行
        if p.returncode:
            result = '--error:%s' % cmd
            return result

        for line in out.splitlines():
            try:
                line = line.decode()
                # print(line)
            except:
                line = "con't decode... %s" % line
                # print(line)
            result += "%s\r\n" % line
        if result.endswith('\r\n'):
            result = result[:len(result) - 2]

        return result



# if __name__ == '__main__':
#     execpayload = execpayload()
#
#     while True:
#         cmd = input()
#         result = execpayload.exec_cmd(cmd)
#         print(result)
