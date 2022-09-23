
import os
import sys
import itertools
import re

adirProj=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(adirProj)

from lib.diskgenmem import *
from lib.gene_altnames import *
from lib.mytime import *
from lib.re_sub import sub_all_plain_string

re_name=re.compile(r"[^a-zA-Z0-9]+")

def normalize_name(name):
    #return re_name.sub(name.upper(),r" ")
    #print("name={}".format(name))
    #return re.sub(re_name, name, " ")  # name=NFKB1\2  => re.error: invalid group reference
    #return re_name.sub(name, " ")      # name=NFKB1\2  => re.error: invalid group reference
    return sub_all_plain_string(re_name, name, " ")

dmem = DiskgenMem(os.path.join(adirProj, "cache", "managed", "derived"))
pubtator_gene_altnames = DictMem(lambda:
    dmem.cache(
        lambda: gather_pubtator_gene_altnames(os.path.join(adirProj, "cache", "external", "gene2pubtatorcentral_2022-09-15.gz"), normalize_name),
        "pubtator_gene_altnames.gz")())

def main():
    tmp=mytime(lambda: sum(1 for _ in pubtator_gene_altnames().keys()))

    print("pubtator_gene_altnames={}".format(tmp))

    # TODO: print a random sample for spot checking, not the first rows
    for (k,v) in itertools.islice(pubtator_gene_altnames().items(), 10):
        print("{} => {}".format(k,v))

if __name__ == '__main__':
    main()
