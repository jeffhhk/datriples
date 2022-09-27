
import os
import sys
import itertools
import re

adirProj=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(adirProj)

from lib.altname_paths import *
from lib.diskgenmem import *
from lib.gene_altnames import *
from lib.mytime import *
from lib.re_sub import sub_all_plain_string
from lib.reservoir import reservoir
import random


dmem = make_dmem()
pubtator_gene_altnames = DictMem(lambda:
    dmem.cache(
        lambda: gather_pubtator_gene_altnames(absf_gene2pubtatorcentral, normalize_pubtator_gene_altname),
        absf_pubtator_gene_altnames)())

def main():
    tmp=mytime(lambda: sum(1 for _ in pubtator_gene_altnames().keys()))

    print("pubtator_gene_altnames={}".format(tmp))

    for (k,v) in reservoir(pubtator_gene_altnames().items(), 20, random.Random(123)):
        print("{} => {}".format(k,v))

if __name__ == '__main__':
    main()
