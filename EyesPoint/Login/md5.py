#!/usr/bin/env python
# coding=utf-8

import hashlib

def md5(str):
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()

if __name__ == '__main__':
    print(md5("1256"))
