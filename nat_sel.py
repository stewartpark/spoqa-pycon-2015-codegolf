from test import EXAMPLE as logo
from test import calculate_similarity, PASS_THRESHOLD

import binascii
import random
import zlib
import re
import copy


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


def get_similarity(gene):
    T = create_image_fast(gene, width=len(logo_img[0]), height=len(logo_img))
    similarity = calculate_similarity(logo_img, T)
    return similarity 


sp_re = re.compile('\ +\*+')
def extract_gene(text):
    split_by_rows = text.split('\n')
    split_by_rows = list(filter(lambda n: len(n.strip()) > 0, split_by_rows))
    gene = []
    for l in split_by_rows:
        _l = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        s = sp_re.findall(l)
        for i, x in enumerate(s):
            _l[i*2] = x.rfind(' ')+1
            _l[i*2+1] = len(x)-_l[i*2]
        gene.append(_l)
    return gene

def realize_gene(gene):
    text = ''
    for x in gene:
        for i, y in enumerate(x):
            text += (' *'[i%2])*y
        text+='\n'
    return text


def mutate(gene, mr=3):
    new = copy.deepcopy(gene) 
    for _ in range(mr): 
        x = random.choice(range(row))
        y = random.choice(range(col))
        new[x][y] += random.choice([-1,0,1])
    return new


def next_gen(alpha, num=10):
    gen = [mutate(alpha) for _ in range(num)] + [alpha]
    scores = [feedback(x) for x in gen]
    return sorted(zip(scores, gen), key=lambda x: x[0])
    

def feedback(gene):
    v = 0
    text = realize_gene(gene)
    if get_similarity(text) < PASS_THRESHOLD:
        v = 1000
    else:
        d = zlib.compress(text, 9).replace(b'\n', b'\\n').replace(b'\r', b'\\r').replace(b'\x00', b'\\x00')
        v = len(d)
        if d.find(b'\'') > 0 and d.find(b'\"') > 0:
            v += 1
    return v

logo_img = create_image_fast(logo)

try:
    # Load the previous alpha
    alpha = extract_gene(open('alpha.txt').read())
except:
    alpha = extract_gene(logo)

row,col=len(alpha),len(alpha[0])

try:
    i = 0
    while True:
        i += 1
        gen = next_gen(alpha)
        alpha = gen[0][1]
        print 'Gen: {0}, alpha score: {1}'.format(i, gen[0][0])
except:
    open('./alpha.txt','w').write(realize_gene(alpha))
    print 'Done!'
