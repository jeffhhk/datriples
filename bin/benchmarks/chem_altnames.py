
import os
import sys
import itertools
import re

adirProj=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(adirProj)

from lib.resource.altname_paths import *
from lib.diskgenmem import *
from lib.resource.chem_altnames import *
from lib.mytime import *
from lib.re_sub import sub_all_plain_string
from lib.reservoir import reservoir
import random


dmem = make_dmem()
pubtator_chem_altnames = DictMem(lambda:
    dmem.cache(
        lambda: gather_pubtator_chem_altnames(absf_chemical2pubtatorcentral, lambda n:n),
        relf_pubtator_chem_altnames)())

def main():
    i=0
    #for row in parse_chem_altnames_raw(absf_chemical2pubtatorcentral):
    # for row in parse_chem_altnames(absf_chemical2pubtatorcentral):
    #     print(row)
    #     i+=1
    #     if i>=100:
    #         break
    tmp=mytime(lambda: sum(1 for _ in pubtator_chem_altnames().keys()))

    print("pubtator_chem_altnames={}".format(tmp))

    for (k,v) in reservoir(pubtator_chem_altnames().items(), 20, random.Random(123)):
        print("{} => {}".format(k,v))

if __name__ == '__main__':
    main()
