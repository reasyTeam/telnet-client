import re
from core.util import read_file

def get_lang(file_path):
  langs = {}
  content = read_file(file_path)

  if content == '':
    return langs

  match = re.compile(r'[{](.*)[}]', re.S)
  matchObj = re.findall(match, content)
  if len(matchObj) > 0:
    code = matchObj[0]

    for line in code.splitlines():
      lang = line.strip()
      if lang == '':
        continue

      try:
        index = lang.rindex('[')
        lang = lang[index+1:]
        lang = re.sub(r',*$', '', lang)
        lang = re.sub(r']\s*=\s*"', '#-#-#-#', lang)
        lang = lang.split('#-#-#-#')
        if len(lang) >= 2:
          key = lang[0].strip()
          langs[key] = lang[1].rstrip('"')
      finally:
        continue

  return langs

if __name__ == "__main__":
  get_lang('test/lang.c')