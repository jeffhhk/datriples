import unittest

import os
import sys
import shutil

adirProj=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(adirProj)

from lib.diskgenmem import *

class TestDiskgen(unittest.TestCase):
    def absf(self):
        return os.path.join(adirProj, "cache", "managed", "test")

    def drop_cache(self):
        if os.path.exists(self.absf()):
            shutil.rmtree(self.absf())

    def dmem(self):
        return DiskgenMem(self.absf())

    def million(self, dmem):
        return dmem.cache(lambda: range(0,1000000), "hello.gz")

    def test_one(self):
        self.drop_cache()
        dmem = self.dmem()
        #print("class={}".format(self.million(dmem).__class__))
        sum(1 for _ in self.million(dmem)())
        self.assertEqual(dmem._numRead, 1)
        self.assertEqual(dmem._numWrite, 1)
        sum(1 for _ in self.million(dmem)())
        self.assertEqual(dmem._numRead, 2)
        self.assertEqual(dmem._numWrite, 1)

    def millionkv(self, dmem):
        return dmem.cache(lambda: ((x, 1000000-x) for x in range(0,1000000)), "hellokv.gz")

    def test_kv(self):
        self.drop_cache()
        dmem = self.dmem()
        h = DictMem(lambda:
            self.millionkv(dmem)())()
        self.assertEqual(sum(1 for _ in h.keys()), 1000000)
        self.assertEqual(dmem._numRead, 1)
        self.assertEqual(dmem._numWrite, 1)
        h = DictMem(lambda:
            self.millionkv(dmem)())()
        self.assertEqual(sum(1 for _ in h.keys()), 1000000)
        self.assertEqual(dmem._numRead, 2)
        self.assertEqual(dmem._numWrite, 1)


if __name__ == '__main__':
    unittest.main()