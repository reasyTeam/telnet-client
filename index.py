#-*- coding: utf-8 -*-
import time, os, re, sys
import config
from core.monitor import DirMonitor
from core.recoder import Recoder
from core.telnet import TelnetClient
from core.util import copy_file

# 监听器
def monitor(dir_path, call_back, telnet_client):
  monitor = DirMonitor(dir_path)
  monitor.start(call_back)

  try:
    while True: 
      time.sleep(300)
      print('[log]: 向telnet发送消息，避免无操作超时断开')   
      telnet_client.exec_cmd('pwd')
  except:
    monitor.stop()
    telnet_client.log_out()

  monitor.observer.join()

def telnet():
  telnet_client = TelnetClient()
  if telnet_client.log_in(config.telnet_ip, config.username, config.password):
    # 切换到linux shell命令模式
    telnet_client.exec_cmd("sh")
    # 切换到web目录文件夹
    telnet_client.exec_cmd("cd %s" % config.dir_path)
    print('# 注意：如果文件上传/下载失败或显示tftp: timeout，请确认本机IP[%s]是否正确' % config.local_ip)
    print('# 注意：如果文件上传/下载失败或显示tftp: timeout，请确认本机IP[%s]是否正确' % config.local_ip)
    print('# 注意：如果文件上传/下载失败或显示tftp: timeout，请确认本机IP[%s]是否正确' % config.local_ip)
    print('-------------------------------------------------')
  return telnet_client

if __name__ == "__main__":
  # 初始化解码器
  print('*******************************')   
  print('telnet')
  print('*******************************')
  recoder = Recoder(config.lang_path)
  # 开启telnet
  try:
    telnet_client = telnet()  
  except:
    print('[error]: 网络连接失败，可能是【用户名密码错误】或【连接已被占用】')
    sys.exit() 
  # 开启监控
  def coder(file_path):
    # 对变化的文件进行重新监控
    ext_name = os.path.splitext(file_path)
    if re.search(r'^\.(asp(x?)|js|html)$', ext_name[1]):
      recoder.recode(file_path)
    else:
      # 直接将文件进行拷贝即可
      print('[拷贝文件]：%s' % file_path)
      copy_file(file_path, config.out_path)

    # 获取变化文件的相对于根目录的路径
    rel_path = os.path.relpath(os.path.realpath(file_path), os.path.realpath(config.monitor_path))
    # 文件上传
    print("[log]: 开始上传文件到tftp服务器")
    try:
      telnet_client.put(rel_path)
    except EOFError:
      # 重新连接
      telnet_client.reopen()

  monitor(config.monitor_path, coder, telnet_client)


# 注意：切换目录后，对应的tftp服务器也需要切换相应的目录，否则会出错
