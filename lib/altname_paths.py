
import os
import sys

from lib.diskgenmem import *

"""
To obtain a cached resource, two things are required:

    1) The function that can regenerate the resource
    2) The path at which the resource might be cached.

Each absf_ definition here corresponds to exactly one definition elsewhere in the code for regenerating its resource.  All
parameters must be bound to fully determine a path.

All other modules are free to freely reference these identifiers so long as they are properly associated with regeneration.
"""

adirProj=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(adirProj)

def make_dmem():
    return DiskgenMem(os.path.join(adirProj, "cache", "managed", "derived"))

def absf_external(relf):
    return os.path.join(adirProj, "cache", "external", relf)

absf_gene2pubtatorcentral = absf_external("gene2pubtatorcentral_2022-09-15.gz")
absf_human_orthologs = absf_external("gene_orthologs_2022-09-09.gz")

# dervied data
relf_pubtator_gene_altnames = "pubtator_gene_altnames.gz"
relf_mesh_to_unii = "mesh_to_unii.gz"
