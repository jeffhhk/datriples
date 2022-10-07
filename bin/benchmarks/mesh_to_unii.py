
import os
import sys

adirProj=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(adirProj)

from lib.resource.altname_paths import *
from lib.diskgenmem import *
from lib.resource.fetch_mesh_to_unii import *
from lib.mytime import *

dmem = make_dmem()

mesh_to_unii = dmem.cache(lambda: gather_mesh_unii(), relf_mesh_to_unii)

mesh_to_only_unii = DictMem(lambda:
        ((meshid_find(x["mesh"]), x) for x in
            mesh_to_unii()))()

print(mytime(lambda: sum(1 for _ in mesh_to_only_unii.keys())))
#print(mytime(lambda: mesh_to_only_unii.keys()))
