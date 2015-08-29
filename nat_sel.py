from test import EXAMPLE as logo
from test import calculate_similarity, create_image, PASS_THRESHOLD

import binascii
import random
import zlib

mr = 3
br = 10

def create_image_fast(text, width=None, height=None):
    split_by_rows = text.split('\n')
    split_by_rows = list(filter(lambda n: len(n.strip()) > 0, split_by_rows))
    rows = len(split_by_rows)
    cols = max(map(lambda n: len(n), split_by_rows))
    if width is None:
        width = cols
    if height is None:
        height = rows
    new = []
    for x in split_by_rows:
        n = width-len(x)
        new.append(x + (' '*n if n > 0 else '')) # add insufficient columns

    # Add insufficient rows
    n = height-rows
    if n > 0:
        for _ in range(n):
            new.append(' '*width)
    return new

logo_img = create_image_fast(logo)

def get_similarity(gene):
    T = create_image_fast(gene, width=len(logo_img[0]), height=len(logo_img))
    similarity = calculate_similarity(logo_img, T)
    return similarity 

def mutate(gene, _mr=None):
    if _mr is None: 
        _mr = mr
    n_gene = list(gene)
    for _ in range(_mr):
        i = random.choice(range(0,len(gene)))
        if n_gene[i] != '\n':
            n_gene[i] = random.choice(['', '*', ' '])
    gene = ''.join(n_gene)
    return gene

def feedback(gene):
    v = 0
    if get_similarity(gene) < PASS_THRESHOLD:
        v = 1000
    else:
        d = zlib.compress(gene, 9).replace(b'\n', b'\\n').replace(b'\r', b'\\r').replace(b'\x00', b'\\x00')
        v = len(d)
        if d.find(b'\'') > 0 and d.find(b'\"') > 0:
            v += 1
    return v


def print_gen(gen):
    print map(lambda x:x[0], gen)

# load the previous alpha if it exists
try:
    _alpha = open('./alpha.txt').read()
    alpha = [feedback(_alpha), _alpha]
except:
    alpha = [feedback(logo), logo]

cur_gen = [alpha, alpha, alpha]
i = 0
try:
    while True:
        print 'Generation:', i, ', Alpha:', alpha[0]
        i += 1

        cur_gen = sorted(map(lambda x: [feedback(x), x], 
            [mutate(alpha[1]) for _ in range(br)] +
            [mutate(cur_gen[1][1], _mr=mr*2) for _ in range(br)] +
            [alpha[1], cur_gen[1][1]]), 
            key=lambda x: x[0])
        print_gen(cur_gen)
        alpha = cur_gen[0]
except KeyboardInterrupt:
    print 'Saving...'
    open('alpha.txt', 'w').write(alpha[1])
    import os
    os.system('python3 gen.py')
    print len(open('pupu.py','rb').read())
