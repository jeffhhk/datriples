
import os
import sys
import itertools
import re

adirProj=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(adirProj)

from lib.resource.altname_paths import *
from lib.diskgenmem import *
from lib.resource.chem_altnames import *
from lib.resource.fetch_mesh_to_unii import *
from lib.mytime import *
from lib.re_sub import sub_all_plain_string
from lib.reservoir import reservoir
import random

dmem = make_dmem()

mesh_to_unii = dmem.cache(lambda: gather_mesh_unii(), relf_mesh_to_unii)

mesh_to_only_unii = DictMem(lambda:
        ((meshid_find(x["mesh"]), x) for x in
            mesh_to_unii()))()

pubtator_chem_altnames = DictMem(lambda:
    dmem.cache(
        lambda: gather_pubtator_chem_altnames(absf_chemical2pubtatorcentral, lambda n:n),
        relf_pubtator_chem_altnames)())


def mesh_chem_altnames():
    for (meshid,vs) in pubtator_chem_altnames().items():
        if meshid in mesh_to_only_unii:
            meshinfo = mesh_to_only_unii[meshid]
            unii = meshinfo["r"] if "r" in meshinfo else None
            unii2 = meshinfo["rr"] if "rr" in meshinfo else None
            yield (unii,unii2,meshid,vs)


def main():
    print("pubtator chemicals count={}".format(
        mytime(lambda: sum(1 for _ in pubtator_chem_altnames().keys()))))

    print("chemical meshids count={}".format(
        mytime(lambda: sum(1 for _ in mesh_to_only_unii.keys()))
    ))

    print("mesh_chem_altnames count={}".format(
        mytime(lambda: sum(1 for _ in mesh_chem_altnames()))))

    print("mesh_chem_altnames with any unii count={}".format(
        mytime(lambda: sum(1 for (unii,unii2,meshid,vs) in mesh_chem_altnames() if unii is not None or unii2 is not None))))

    print("mesh_chem_altnames with direct unii count={}".format(
        mytime(lambda: sum(1 for (unii,unii2,meshid,vs) in mesh_chem_altnames() if unii is not None))))

    for (unii,unii2,meshid,v) in reservoir(mesh_chem_altnames(), 20, random.Random(123)):
        print("{},{},{} => {}".format(unii,unii2,meshid,v))

if __name__ == '__main__':
    main()
