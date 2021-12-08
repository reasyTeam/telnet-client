# 接入开发本地服务器

适用于接入前端项目的telnet自动连接，通过tftp进行文件替换工具，开启服务，将会自动对修改的文件进行重新编码和服务器文件替换，避免手动输入命令进行文件替换，提高开发效率。

依赖于python3.x，请确保本机已安装对应版本python

## 运行

### 安装依赖

npm run init

### 启动服务器

npm run serve

开起tftp服务器

## 配置项

修改`config.py`文件中的配置即可。

| 配置         | 描述                                                                                               | 值     |
| ------------ | -------------------------------------------------------------------------------------------------- | ------ |
| lang_path    | C语言中存储词条的文件路径                                                                          | string |
| monitor_path | 被监听文件根目录即前端源代码根目录                                                                 | string |
| out_path     | 对源码进行重新编码后文件输出的根目录，也是tftp服务器配置的与telnet服务器进行文件交互的本地文件目录 | string |
| telnet_ip    | telnet服务器地址                                                                                   | string |
| local_ip     | 本机IP                                                                                             | string |
| username     | telnet服务器用户名                                                                                 | string |
| password     | telnet服务器密码                                                                                   | string |
| dir_path     | telnet服务器中web文件存放的根目录                                                                  | string |


## 手动tftp

目前软件共有2种tftp方式，不同软件支持不同方式。
另外，大多数软件编译时，web的权限为只读，需要后台重新编译支持

1. 进入到web路劲
cd \home\httpd\web
2. tftp
替换板子里的文件
  tftp -g -r xxx.asp 192.168.1.2(电脑的IP地址)
获取板子里的文件
  tftp -p -r xxx.asp 192.168.1.2(电脑的IP地址)

另一种方式
  tftp 192.168.1.2(电脑的IP地址)
替换板子里的文件
  get xxx.asp 
获取板子里的文件
  put xxx.asp 
退出
  q


