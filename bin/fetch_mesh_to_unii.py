
import os
import sys

adirProj=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(adirProj)

from lib.pipeline_altnames import fetch_mesh_to_unii
from lib.pipeline_altnames import *
from lib.mytime import *

print("fetch_mesh_to_unii: {}".format(mytime(lambda: sum(1 for _ in fetch_mesh_to_unii()))))
