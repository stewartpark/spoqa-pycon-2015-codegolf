from test import EXAMPLE as logo
import zlib

code = u"""#coding:latin\nimport zlib;b=[bytes,lambda x,y:x][str==bytes];print(zlib.decompress(b('!!!','latin')).decode())"""

f = open('./pupu.py', mode='wb')
f.write(bytes(code.split('!!!')[0], 'utf-8'))

data = zlib.compress(bytes(logo, 'utf-8'),9)
f.write(data)

f.write(bytes(code.split('!!!')[1], 'utf-8'))
f.close()
