import telnetlib, time, os, re
from config import username, password, local_ip, dir_path, telnet_ip

base_path = dir_path
if base_path[0] != '/' and base_path[0] != '\\':
  base_path = '/' + base_path
class TelnetClient():
  def __init__(self):
    self.tn = telnetlib.Telnet()
    self.level = 0
    self.telnet_ip = ''
    self.username = ''
    self.password = ''
    # tftp方式 tftp 命令行模式commond 普通模式 normal
    # narmal 即 tftp -g-r xxx.asp 192.168.1.2(自己的ip地址)
    # command 即 tftp 192.168.1.2\n 进入tftp命令模式中
    # get xxx.asp\n (往路由器中传)
    # put xxx.asp\n (获取到电脑中)
    # q\n 退出该命令模式
    self.currentType = 'normal'

  # 登录telnet服务器
  def log_in(self, telnet_ip, username, password):
    try:
      self.telnet_ip = telnet_ip
      self.username = username
      self.password = password
      print('[log]: 开始尝试连接telnet服务器[%s]...' % telnet_ip)
      self.tn.open(telnet_ip, port=23)
    except:
      print('[error]: %s网络连接失败，可能是连接已被占用' % telnet_ip)
      return False

    # 输入登录用户名
    self.tn.read_until('login: '.encode(encoding="ascii"))
    self.tn.write(username.encode('ascii') + b"\n")

    # 输入登录密码
    self.tn.read_until('Password: '.encode(encoding="ascii"))
    self.tn.write(password.encode('ascii') + b"\n")
    # 延迟2秒，保证能拿到响应
    time.sleep(2)

    command_result = self.tn.read_very_eager().decode('ascii')
    if 'Login incorrect' not in command_result:
      print('[success]: telnet服务器[%s]登录成功！' % telnet_ip)
      # 确定当前路由器支持的 tftp 方式
      self.get_current_type()
      return True
    else:
      print('[error]: telnet服务器[%s]登录失败，请确认服务器地址是否正确！' % telnet_ip)
      return False

  def reopen(self):
    self.log_in(self.telnet_ip, self.username, self.password)

  # 判断当前方式
  def get_current_type(self):
    self.exec_cmd("tftp", 2)
    self.tn.write("q\n".encode('ascii'))
    # 能进入 tftp 后输入q 退出没有任何打印 即为commond模式
    # normal 打印 q not found
    command_result = self.tn.read_very_eager().decode('ascii')
    if command_result == "":
      self.currentType = "commond"

  # 执行shell命令
  def exec_cmd(self, command, sleepTime=1):
    print('[log][运行命令]: %s' % command)
    command = command + '\n'
    self.tn.write(command.encode('ascii'))
    time.sleep(sleepTime)
    self.print()

  # tftp 拉取文件
  def get(self, file_name):
    self.switch_dir(file_name)
    if(self.currentType == "commond"):
      self.tftp_get(file_name)
    else:
      command = "tftp -p -r %s %s" % (os.path.basename(file_name), local_ip)
      self.exec_cmd(command, 2)
    
    self.back_to_root()

  # tftp 上传文件
  def put(self, file_name):
    self.switch_dir(file_name)
    if(self.currentType == "commond"):
      self.tftp_put(file_name)
    else:
      command = "tftp -g -r %s %s" % (os.path.basename(file_name), local_ip)
      self.exec_cmd(command, 2)
    
    self.back_to_root()

  # 根据文件目录进行地址切换
  def switch_dir(self, file_name):
    dir = os.path.dirname(file_name)
    if dir == '':
      return

    dir = re.sub(r'\\', '/', dir)
    self.level = len(dir.split('/'))
    self.exec_cmd('cd %s && pwd' % dir)

  # 返回到web文件存放的根目录
  def back_to_root(self):
    if self.level == 0:
      return

    self.exec_cmd('cd %s && pwd' % base_path)

  # 命令行模式
  # 进入tftp 命令行
  def tftp_in(self):
    self.exec_cmd("tftp %s" % local_ip)

  # 命令行get
  def tftp_get(self,file_name):
    self.tftp_in()
    self.exec_cmd("put %s" % os.path.basename(file_name), 2)
    self.tftp_out()

 # 命令行put
  def tftp_put(self,file_name):
    self.tftp_in()
    self.exec_cmd("get %s" % os.path.basename(file_name), 2)
    self.tftp_out()

 # 命令行退出
  def tftp_out(self):
    self.exec_cmd("q")

  # 断开telnet连接
  def log_out(self):
    self.tn.write(b"exit\n")
    self.tn.write(b"exit\n")

  # 控制台消息打印输出
  def print(self):
    command_result = self.tn.read_very_eager().decode('ascii')
    # if command_result.strip() == '':
    #   command_result = '完成'
    print('[log][命令执行结果]：%s' % command_result)
    print('-------------------------------------------------')

if __name__ == "__main__":
  # host = '192.168.1.1' # Telnet服务器IP
  # username = 'admin' # 登录用户名
  # password = 'system' # 登录密码
  telnet_client = TelnetClient()
  if telnet_client.log_in(telnet_ip, username, password):
    # 切换到linux shell命令模式
    telnet_client.exec_cmd("sh")
    # 切换到web目录文件夹
    telnet_client.exec_cmd("cd %s \n" % base_path)
    print('##############################\n')
    print(' 注意：如果文件上传/下载失败，请确认本机IP(%s)是否正确 \n' % local_ip)
    print('##############################\n')

    # 测试文件下载
    telnet_client.exec_cmd("tftp -p -r wlft.asp %s \n" % local_ip, 2)
    # try:
    #   while True:
    #     time.sleep(1)
    # except:
    #   telnet_client.log_out()