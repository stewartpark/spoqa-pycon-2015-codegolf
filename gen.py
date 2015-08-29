import zlib
logo = open('./alpha.txt').read()
data = zlib.compress(bytes(logo, 'utf-8'), 9)

if data.find(b"'") == -1: quote = "'"
elif data.find(b'"') == -1: quote = '"'
else:
    print('!!! Quote problem!')
    quote = "\""
    data=data.replace(b'\"', b'\\\"')

data=data.replace(b'\n',b'\\n')
data=data.replace(b'\r',b'\\r')
data=data.replace(b'\x00',b'\\x00')

code = u"""#coding:L1\nimport zlib;print(zlib.decompress([bytes,lambda x,y:x][str==bytes]({0}!!!{0},'L1')).decode())""".format(quote)

f = open('./pupu.py', mode='wb')
f.write(bytes(code.split('!!!')[0], 'utf-8'))
f.write(data)
f.write(bytes(code.split('!!!')[1], 'utf-8'))
f.close()
