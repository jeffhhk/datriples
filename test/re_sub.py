import unittest

import os
import sys
import re

adirProj=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(adirProj)

from lib.re_sub import *

class TestReSub(unittest.TestCase):
    def re_name(self):
        return re.compile(r"[^a-zA-Z0-9]+")

    def test_one(self):
        re_name=self.re_name()
        st ="elongation factor 1 alpha (EF-1alpha"
        stE="elongation factor 1 alpha EF 1alpha"
        stNorm = sub_all_plain_string(re_name, st, " ")
        self.assertEqual(stNorm, stE)

    def test_beg_stop(self):
        re_name=self.re_name()
        st ="!!elongation factor 1 alpha (EF-1alpha"
        stE=" elongation factor 1 alpha EF 1alpha"
        stNorm = sub_all_plain_string(re_name, st, " ")
        self.assertEqual(stNorm, stE)

    def test_end_stop(self):
        re_name=self.re_name()
        st ="elongation factor 1 alpha (EF-1alpha!!"
        stE="elongation factor 1 alpha EF 1alpha "
        stNorm = sub_all_plain_string(re_name, st, " ")
        self.assertEqual(stNorm, stE)

    def test_no_stop(self):
        re_name=self.re_name()
        st ="elongation"
        stE="elongation"
        stNorm = sub_all_plain_string(re_name, st, " ")
        self.assertEqual(stNorm, stE)


if __name__ == '__main__':
    unittest.main()