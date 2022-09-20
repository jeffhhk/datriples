import os

from jobli2.joblib import Memory as DiskMemorize
from jobli2.joblib import Jlstream

import lib.fetch_mesh_to_unii

adirProj=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
adirJoblib=os.path.join(adirProj, "cache", "joblib")
dmem = DiskMemorize(adirJoblib)

def pass_stream():
    return Jlstream(lambda : (x for x in range(0,3)))

adirProj=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
adirJoblib=os.path.join(adirProj, "cache", "joblib")
dmem = DiskMemorize(adirJoblib)

def _fetch_mesh_to_unii():
    return Jlstream(lambda : lib.fetch_mesh_to_unii.run_fetch_mesh_to_unii())

fetch_mesh_to_unii = dmem.cache(_fetch_mesh_to_unii)

def jl_fetch_mesh_to_only_unii():
    return Jlstream(lambda: lib.fetch_mesh_to_unii.filter_mesh_to_only_unii(fetch_mesh_to_unii()))

fetch_mesh_to_only_unii = dmem.cache(jl_fetch_mesh_to_only_unii)


