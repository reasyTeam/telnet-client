import os, shutil

def correct_path(url):
  # if os.path.isabs(url):
  #   return url
  # return os.path.join(os.getcwd(), url)
  return os.path.realpath(url)

def mkdir(url):
  if os.path.exists(url):
    return
  if os.path.basename(url).find('.') != -1:
    url = os.path.dirname(url)
  if not os.path.exists(url):
    os.makedirs(url)

def read_file(url):
  url = correct_path(url)
  if os.path.exists(url):
    f = open(url, 'r', encoding='UTF-8')
    data = f.read()
    f.close()
    return data
  else:
    print('读取失败，文件[%s]不存在' % url)
    return ''

def write_file(content, url):
  mkdir(url)
  file = open(url, 'w', encoding='UTF-8')
  file.write(content)
  file.close()
  # print('文件【%s】写入成功' % url)

# 文件拷贝
def copy_file(from_url, to_url):
  mkdir(to_url)
  shutil.copy(from_url, to_url)


