# 接入开发本地服务器
依赖于python3.x，请确保本机已安装对应版本python

## 运行

### 安装依赖

npm run init

### 启动服务器

npm run serve

## 配置项

修改`config.py`文件中的配置即可。

| 配置      | 描述 | 值   |
| --------- | ---- | ---- |
| lang_path | 词条文件路径 | string |
| monitor_path | 被监听文件根目录 | string |
| out_path |重新编码后文件输出的根目录| string |
| telnet_ip |  telnet服务器地址    | string |
| local_ip |  本机IP    | string |
| username | 用户名     | string |
| password | 密码     | string |
| dir_path | 服务器web文件地址     | string |

