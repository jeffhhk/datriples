import os
import sys
import itertools
import re
import json
from tqdm import tqdm

adirProj=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(adirProj)

from lib.resource.altname_paths import *
from lib.diskgenmem import *
from lib.resource.gene_altnames import *
from lib.resource.orthologs import *
from lib.mytime import *
from lib.re_sub import sub_all_plain_string
from lib.reservoir import reservoir
import random

dmem = make_dmem()

pubtator_gene_altnames = DictMem(lambda: dmem.cache(lambda: gather_pubtator_gene_altnames(
            absf_gene2pubtatorcentral, 
            normalize_pubtator_gene_altname),
        relf_pubtator_gene_altnames)())

def __add_multi(h,k,v):
    if k not in h:
        h[k] = [v]
    else:
        vs = h[k]
        vs.append(v)
        h[k] = vs      # superstition

def __add_gene(h, geneid1, geneid2, taxid2):
    hpga = pubtator_gene_altnames()
    if geneid2 in hpga:
        frnames=sorted(hpga[geneid2], key=lambda x:-x[1])
        __add_multi(h, geneid1, {"taxid":taxid2, "geneid":geneid2, "frnames":frnames})

def gather_ortho_altnames():
    hpga = pubtator_gene_altnames()
    h={}
    # The upstream ortholog map is constructed to omit the trivial relation from each (taxid,gene) to itself, so we have to collect and process human genes separately.
    isHuman={}
    for orth in tqdm(gather_human_orthologs(absf_human_orthologs)):
        geneid1=orth.geneid1
        if not geneid1 in isHuman:
            isHuman[geneid1]=True
        __add_gene(h, geneid1, orth.geneid2, orth.taxid2)
    for geneid in isHuman.keys():
        __add_gene(h, geneid, geneid, taxid_human)
    for geneid1 in sorted(h.keys()):
        hs = h[geneid1]
        yield (geneid1, sorted(hs, key=lambda h:h["taxid"]))

ortho_altnames = DictMem(lambda: gather_ortho_altnames())

def main():
    print("gather_ortho_altnames={}".format(mytime(lambda: sum(1 for _ in ortho_altnames()))))
    for kv in reservoir(sorted(ortho_altnames().items(), key=lambda x: x[0]), 10, random.Random(124)):
        print("{}".format(json.dumps(kv)))

if __name__ == '__main__':
    main()
