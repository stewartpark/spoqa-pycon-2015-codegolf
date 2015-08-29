import zlib
logo = open('./alpha.txt').read()
data = zlib.compress(bytes(logo, 'utf-8'),9)

if data.find(b"'") == -1: quote = b"'"
elif data.find(b'"') == -1: quote = b'"'
else:
    print('!!! Quote problem!')
    quote = "\""
    data=data.replace(b'\"', b'\\\"')

data=data.replace(b'\n',b'\\n')
data=data.replace(b'\r',b'\\r')
data=data.replace(b'\x00',b'\\x00')

print(data,"    ", len(data))

code = u"""#coding:L1\nimport zlib;print(zlib.decompress([bytes,lambda x,y:x][str==bytes](!!!,'L1')).decode())"""

f = open('./pupu.py', mode='wb')
f.write(bytes(code.split('!!!')[0], 'L1'))

f.write(quote)
f.write(data)
f.write(quote)

f.write(bytes(code.split('!!!')[1], 'L1'))
f.close()

import os
os.system('python3 pupu.py')
