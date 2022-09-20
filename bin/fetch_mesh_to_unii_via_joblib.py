
import os
import sys

adirProj=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(adirProj)

from lib.fetch_mesh_to_unii_via_joblib import *
from lib.pipeline_altnames import *
from lib.mytime import *

#print("fetch_mesh_to_unii: {}".format(mytime(lambda: sum(1 for _ in fetch_mesh_to_unii()))))

i=0
for res in fetch_mesh_to_only_unii():
    i+=1
    #if (i % 5000) == 0:
    print(res)
