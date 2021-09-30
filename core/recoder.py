import os
import re, os
from config import lang_path, out_path
from core.lang import get_lang
from core.util import read_file, write_file

def handle_if(content, file_path):
  lines = content.splitlines(True)
  out_lines = []
  status = False
  level = 0
  file_type = ''
  split = os.path.splitext(file_path)
  if len(split) >= 2:
    file_type = split[1]

  for line in lines:
    if re.match(r'^\s*\#(if(?:def)?|else|endif|elif|ifndef)\s*(.*)', line):
      # 对于js文件包含#if等语句不进行额外处理，工作量太大
      # if file_type == '.js':
        # if re.match(r'^\s*\#(else|elif)\s*(.*)', line):
        #   if not status:
        #     level += 1
        #   status = True
        #   # out_lines.append(',')
        #   # need_delete = True
        # elif re.match(r'^\s*\#(endif)\s*(.*)', line):
        #   status = False
        #   if level > 0:
        #     level -= 1
          # need_delete = False
      continue
    # js文件中<% xxx %>格式的其它内容全部去除
    elif file_type == '.js' and re.match(r'\s*<%(.*?)\%>?', line):
      continue
    if level == 0:
      out_lines.append(line)
  return ''.join(out_lines)


class Recoder():
  def __init__(self, lang_path):
    self.langs = get_lang(lang_path)

  def recode(self, file_path):
    content = read_file(file_path)

    def recoder(match):
      key = match.group(1)
      if self.langs.__contains__(key):
        return self.langs[key]
      else:
        key =key.split('"')
        if len(key) == 5:
          key = key[3]
          if self.langs.__contains__(key):
            return self.langs[key]
      return key

    content = re.sub(r'<%\s*multilang\((.*?)\);\s*%>?', recoder, content)
    # 处理宏相关内容
    content = handle_if(content, file_path)
    out_file_path = os.path.join(out_path, os.path.basename(file_path))
    write_file(content, out_file_path)
    print('[log][重新编码]：文件[%s]编码完成，输出到[%s]' % (os.path.basename(file_path), out_file_path))

  # def re_path(self, file_path):
  #   rel = os.path.relpath(os.path.realpath(file_path), os.path.realpath(monitor_path))
  #   return os.path.join(out_path, rel)

if __name__ == "__main__":
  recoder = Recoder(lang_path)
  recoder.recode('test/src/date.asp', 'out/date.asp')