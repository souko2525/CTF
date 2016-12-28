# -*- coding: utf-8 -*-

#i文字ずらしたときのシーザー暗号を解読する

#各アルファベットの出現頻度
general_frequency = [0.08167, 0.01492, 0.02782, 0.04253, 0.12702, 0.02228, 0.02015, 0.06094, 0.06966, 0.00153, 0.00772, 0.04025, 0.02406, 0.06749, 0.07507, 0.01929, 0.00095, 0.05987, 0.06327, 0.09056, 0.02758, 0.00978, 0.02360, 0.00150, 0.01974, 0.00074]

# ある文章のアルファベットの出現頻度とgeneral_frequencyを乗算して出現頻度が一致したときの値
pmatch = 0.065

#ある文章のアルファベットの出現頻度をリストで返す
def freqanalysis(text):
    l = [0] * 26
    for i in xrange(len(text)):
        if 'A' <= text[i] and text[i] <= 'Z':
            c = ord(text[i]) - ord('A')
            l[c] = l[c] + 1
        elif 'a' <= text[i] and text[i] <= 'z':
            c = ord(text[i]) - ord('a')
            l[c] = l[c] + 1
        else:
            continue
    s = float(sum(l))
    l = [float(n)/s for n in l]
    return l

#アルファベットをi文字シフトしたときの文字を返す。アルファベット以外はそのまま
def shift(c, i):
    if 'A' <= c and c <= 'Z':
        return chr((ord(c) - ord('A') + i) % 26 + ord('A'))
    if 'a' <= c and c <= 'z':
        return chr((ord(c) - ord('a') + i) % 26 + ord('a'))
    return c

#出現頻度との一致具合を計算する
def freq(text, i):
    plain = [shift(n, i)  for n in text]
    fr = freqanalysis(plain)
    ret = 0
    for j in xrange(26):
        ret += general_frequency[j] * fr[j]
    return ret

#0~25文字ずらしたとき最も出現頻度が近いものを返す。
def findkeyletter(text):
    freqs = [abs(pmatch - freq(text, n)) for n in xrange(26)]
    return freqs.index(min(freqs))

with open('ciphertext') as fh:
    ciphertext = fh.read()

key = findkeyletter(ciphertext)
plain = [shift(n, key)  for n in ciphertext]
print "".join(plain)
