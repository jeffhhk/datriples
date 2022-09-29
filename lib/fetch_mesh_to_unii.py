import os
import sys
import re
import requests
from tqdm import tqdm

adirProj=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(adirProj)

from lib.altname_paths import *
from lib.diskgenmem import *

# class SparqlResult():
#     def __init__(self, value) -> None:
#         self.

def sparql_query(url, prefix, query):
    params = {'query': prefix + query, 'format': 'JSON', 'limit': 1000, 'offset': 0}
    r = requests.get(url, params=params)
    t = tqdm()
    while True:
        t.update(1)
        params['offset'] += 1000
        r = requests.get(url, params=params).json()['results']['bindings']
        if not r:
            break
        for x in r:
            yield x
        # if params['offset']>10000:
        #     break

def rdf_fd(x,fd):
    if x is None or fd not in x:
        return None
    return x[fd]

def val_rdf_fd(x,fd):
    v = rdf_fd(x,fd)
    if v is None or "value" not in v:
        return None
    return v["value"]

def fetch_mesh_unii_raw():
    # inspired by:
    #     https://github.com/stuppie/semmed-biolink/blob/master/05-xrefs.ipynb
    # query
    #     https://id.nlm.nih.gov/mesh/query?query=PREFIX+rdf%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23%3E%0D%0APREFIX+rdfs%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%0D%0APREFIX+xsd%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%23%3E%0D%0APREFIX+owl%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23%3E%0D%0APREFIX+meshv%3A+%3Chttp%3A%2F%2Fid.nlm.nih.gov%2Fmesh%2Fvocab%23%3E%0D%0APREFIX+mesh%3A+%3Chttp%3A%2F%2Fid.nlm.nih.gov%2Fmesh%2F%3E%0D%0APREFIX+mesh2022%3A+%3Chttp%3A%2F%2Fid.nlm.nih.gov%2Fmesh%2F2022%2F%3E%0D%0APREFIX+mesh2021%3A+%3Chttp%3A%2F%2Fid.nlm.nih.gov%2Fmesh%2F2021%2F%3E%0D%0APREFIX+mesh2020%3A+%3Chttp%3A%2F%2Fid.nlm.nih.gov%2Fmesh%2F2020%2F%3E%0D%0A%0D%0ASELECT+distinct+%3Fmesh+%3FmeshLabel+%3Fr+%3Frr%0D%0AFROM+%3Chttp%3A%2F%2Fid.nlm.nih.gov%2Fmesh%3E+WHERE+%7B%0D%0A++%3Fmesh+meshv%3Aactive+1+.%0D%0A++%3Fmesh+meshv%3ApreferredMappedTo+%3Fp+.%0D%0A++%3Fp+meshv%3AtreeNumber+%3FtreeNum+.%0D%0A++FILTER%28STRSTARTS%28STR%28%3FtreeNum%29%2C+%22http%3A%2F%2Fid.nlm.nih.gov%2Fmesh%2FD%22%29%29+.%0D%0A++%3Fmesh+rdfs%3Alabel+%3FmeshLabel+.%0D%0A++%3Fmesh+meshv%3ApreferredConcept+%5Bmeshv%3AregistryNumber+%3Fr%5D+.%0D%0A++OPTIONAL+%7B%3Fmesh+meshv%3ApreferredConcept+%5Bmeshv%3ArelatedRegistryNumber+%3Frr%5D%7D%0D%0A%7D+limit+50%0D%0A&format=HTML&year=current&limit=50&offset=0#lodestart-sparql-results

    # regex columns ?r and ?rr to look like a UNII

    # collect all matching (meshid, UNII) pairs

    #     NTH: include max one meshLabel
    URL = "http://id.nlm.nih.gov/mesh/sparql"
    PREFIX = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX meshv: <http://id.nlm.nih.gov/mesh/vocab#>
    PREFIX mesh: <http://id.nlm.nih.gov/mesh/>
    """

    query = """
    SELECT distinct ?mesh ?meshLabel ?r ?rr
    FROM <http://id.nlm.nih.gov/mesh> WHERE {
        ?mesh meshv:active 1 .
        ?mesh meshv:preferredMappedTo ?p .
        ?p meshv:treeNumber ?treeNum .
        FILTER(STRSTARTS(STR(?treeNum), "http://id.nlm.nih.gov/mesh/D")) .
        ?mesh rdfs:label ?meshLabel .
        ?mesh meshv:preferredConcept [meshv:registryNumber ?r] .
        OPTIONAL {?mesh meshv:preferredConcept [meshv:relatedRegistryNumber ?rr]}
    }
    """

    # example: {'mesh': {'type': 'uri', 'value': 'http://id.nlm.nih.gov/mesh/C408080'}, 
    #           'meshLabel': {'type': 'literal', 'xml:lang': 'en', 'value': 'fumaryl chloride'}, 
    #           'r': {'type': 'literal', 'value': 'B95L4812RG'}, 
    #           'rr': {'type': 'literal', 'value': '627-63-4 (fumaryl chloride)'}}

    return sparql_query(URL, PREFIX, query)

re_unii = re.compile('^[0-9A-Z]{10}$')

def is_unii(st):
    if not st:
        return False
    m = re_unii.match(st)
    return m[0] if m else None

re_mesh = re.compile('([0-9A-Z]+)$')

def meshid_find(st):
    if not st:
        return False
    m = re_mesh.search(st)
    return m[1] if m else None

def filter_mesh_to_only_unii(mesh_to_unii):
    for res in mesh_to_unii:
        r = val_rdf_fd(res,"r")
        rr = val_rdf_fd(res,"rr")
        if is_unii(r) or is_unii(rr):
            yield {
                "mesh": val_rdf_fd(res, "mesh"),
                "meshLabel": rdf_fd(res, "meshLabel"),
                "r": r if is_unii(r) else None,
                "rr": rr if is_unii(rr) else None
            }

def gather_mesh_unii():
    return filter_mesh_to_only_unii(fetch_mesh_unii_raw())
