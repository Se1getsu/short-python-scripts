# 【内容】
# 文字列のハッシュ化と誤り訂正を行うプログラムです。
# デフォルトでは SHA-256 の先頭 2 バイトを使用します。

import argparse
import getpass
import hashlib
import sys

# Options
parser = argparse.ArgumentParser(description='SHA-256 hash')
parser.add_argument(
    '-s', '--secret', action='store_true',
    help='hides input text'
)
parser.add_argument(
    '-l', '--length', type=int,
    default=2,
    help='hash length'
)
parser.add_argument(
    '--charset', type=str,
    default=''.join(chr(i) for i in range(0x21, 0x7E+1)),
    help='character set for error correction'
)
args = parser.parse_args()

HIDE_INPUT = args.secret
HASH_LENGTH = args.length
CHAR_SET = args.charset


# Functions
def highlighted(text, code=33):
    return f"\x1b[{code}m{text}\x1b[0m"

def hash(text):
    return hashlib.sha256(text.encode()).hexdigest()[:HASH_LENGTH]


# Calculate Hash
text = (input, getpass.getpass)[HIDE_INPUT]("text: ")
print("Hash:", hash(text))


# Error Correction
if HIDE_INPUT: sys.exit()
expected = ""
while not expected or len(expected) != HASH_LENGTH:
    expected = input("expected hash: ")

print("\nreplace(1)")
for point in range(len(text)):
    for c in CHAR_SET:
        s = text[:point] + c + text[point+1:]
        if s != text and hash(s) == expected:
            print(text[:point] + highlighted(c) + text[point+1:])

print("\ninsert(1)")
for point in range(len(text)+1):
    for c in CHAR_SET:
        s = text[:point] + c + text[point:]
        if hash(s) == expected:
            print(text[:point] + highlighted(c) + text[point:])

print("\nremove(1)")
for point in range(len(text)):
    s = text[:point] + text[point+1:]
    if s != text and hash(s) == expected:
        print(text[:point] + highlighted(text[point+1:]))

print("\ncompleted.")
