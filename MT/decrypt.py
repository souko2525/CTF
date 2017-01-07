# -*- coding: utf-8 -*-
#メルセンヌ・ツイスタで生成した乱数とファイルでXORを取ったものを暗号化したファイルとする
#平文のファイルと暗号化したファイルがあった場合使用した乱数が求まる
#その乱数が624個以上の場合以降の乱数は予測可能になり同じ種を与えた場合すべて解読可能になる
#ここでは平文のファイルをencrypt.cpp,暗号化されたファイルをencrypt.enc,復号したいファイルをflag.encとする。
#なお暗号化されたファイルの最初には4byte1ブロックとした際に何ブロックになるかが入っている。
#つまり暗号化されたファイルは平文のファイル+4バイトになる
from struct import *
import random
import os.path


#平文と暗号文をXORして鍵（乱数）の抽出
def makekey():
    fp = open('encrypt.cpp', 'rb')
    fe = open('encrypt.enc', 'rb')
    fk = open("sample.key", "wb")
    ed = fe.read(4)
    blocks = unpack('<L', ed)[0]
    while True:
        pd = fp.read(4)
        ed = fe.read(4)
        if pd == "":
            break
        fk.write(pack('<L', unpack('<L', pd)[0] ^ unpack('<L', ed)[0]))
    fp.close()
    fe.close()
    fk.close()

#乱数から元の値を割り出しpythonの乱数の初期値として与える
def dec_flag():
    keys = []
    fk = open("sample.key", "rb")
    for i in xrange(624):
        kd = fk.read(4)
        keys.append(unpack('<L', kd)[0])
    mt_state = tuple([untemper(x) for x in keys] + [0])
    random.setstate((3, mt_state, None))
    fk.close() 
    
    size = os.path.getsize('./encrypt.cpp')
    #疑似的にencrypt.cppを暗号化する処理を入れる
    #もとの暗号化したところでは同じ乱数の中でencrypt.cpp=>flag_dec.jpgと暗号化したため
    #最初の乱数を使用する必要がある。
    fp = open('encrypt.cpp', 'rb')
    fe = open('encrypt_dumy.enc', 'wb')
    
    while True:
        pd = fp.read(4)
        if pd == "":
            break
        key = random.getrandbits(32)
        fe.write(pack('<L', key ^ unpack('<L', pd)[0]))
    fp.close()
    fe.close()
    
    #実際のフラグを復号
    fe = open('flag.enc', 'rb')
    fp = open('flag_dec.jpg', 'wb')
    ed = fe.read(4)
    blocks = unpack('<L', ed)[0]
    while True:
        ed = fe.read(4)
        if ed == "":
            break
        fp.write(pack('<L', random.getrandbits(32) ^ unpack('<L', ed)[0]))
    fp.close()
    fe.close()

#乱数から元の値を逆演算する関数群
def untemper(x):
    x = reverseBitshiftRightXor(x, 18)
    x = reverseBitshiftLeftXor(x, 15, 0xefc60000)
    x = reverseBitshiftLeftXor(x, 7, 0x9d2c5680)
    x = reverseBitshiftRightXor(x, 11)
    return x

def reverseBitshiftRightXor(x, shift):
    i = 1
    temp = x
    while i * shift < 32:
        z = temp >> shift
        temp = x ^ z
        i += 1
    return y

def reverseBitshiftLeftXor(x, shift, mask):
    i = 1
    temp = x
    while i * shift < 32:
        z = temp << shift
        temp = x ^ (z & mask)
        i += 1
    return y

makekey()
dec_flag()
