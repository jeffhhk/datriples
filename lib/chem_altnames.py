import re
import subprocess
from tqdm import tqdm
from lib.re_sub import *

from lib.sessionize import *

# zcat /data/chemical2pubtatorcentral_2022-08-05.gz | ~/bin/reservoir.pl 20
#     24735050	Chemical	MESH:D000975		MESH
#     3028076	Chemical	MESH:D007610		MESH
#     28296541	Chemical	MESH:D009821	oil	TaggerOne
#     17850067	Chemical	MESH:D014867	water	TaggerOne
#     33298524	Chemical	MESH:D013752	tetracycline	TaggerOne
#     31642774	Chemical	-	K318|methyl-lysine|K30|ROS|K316|K525|K253|Efm6	TaggerOne
#     25837679	Chemical	MESH:D012694	Ser	TaggerOne
#     34362742	Chemical	MESH:D017693	NaHCO3	TaggerOne
#     33933117	Chemical	MESH:D019788	18F-FDG	TaggerOne
#     22041936	Chemical	MESH:C008261	lead acetate	TaggerOne|MESH
#     28680580	Chemical	MESH:C104275	Tiglyl-carnitine	TaggerOne
#     15285795	Chemical	MESH:D017830	Triton X100	TaggerOne
#     26442122	Chemical	-	gallium aluminum arsenide	TaggerOne
#     11706197	Chemical	MESH:C029353	xyloglucan	TaggerOne
#     34066641	Chemical	MESH:D000241	adenosine|Adenosine	TaggerOne
#     25412678	Chemical	MESH:D000078330	Oxcarbazepine	TaggerOne
#     33253190	Chemical	-	PLH|Organic matter	TaggerOne
#     1369285	Chemical	MESH:C000874	deoxynybomycin	TaggerOne|MESH
#     18230773	Chemical	MESH:D005632		MESH
#     33464657	Chemical	MESH:D002264	carboxylic acid|Carboxylic acids|carboxylic acids	TaggerOne
#     18954864	Chemical	MESH:C029943	KOH	TaggerOne

# zcat /data/chemical2pubtatorcentral_2022-08-05.gz | pv | wc -l
#     116 676 386

cidPmid=0
cidChemid=2
cidNames=3

def parse_chem_altnames_raw(relf):
    proc=subprocess.Popen(['zcat',relf],
        stdout=subprocess.PIPE,
        encoding='utf-8')
    for line in proc.stdout:
        yield line.rstrip("\n").split("\t")

re_meshid = re.compile("MESH:([A-Z0-9]+)")

def chemid_find(row):
    """
        Handle:
            No URI detected (7% of rows)  Example:
                22927999	Chemical	-	lidocaine N-ethyl-bromide|QX|saline-QX-314|AP-18|cinn|CFA-QX-314|O2	TaggerOne
            Row includes ; folowed by a number.  Example:
                33694023	Chemical	MESH:D010100;0.2093579325156376	oxygen	TaggerOne
    """
    st=row[cidChemid]
    m=re_meshid.search(st)
    if m:
        return m[1]

# Deduplicate so that counts become counts of separate articles
def sess_dedupe(sess):
    h={}
    for row in sess:
        chemid=chemid_find(row)
        if chemid:
            names=row[cidNames].split("|")
            for name in names:
                if len(name)>0 and (chemid, name) not in h:
                    h[(chemid,name)] = True
    return h.keys()
        # except:
        #     print("offending row: {}".format(row))

def parse_chem_altnames(relf):
    for sess in sessionize_rows(lambda: parse_chem_altnames_raw(relf), cidPmid):
        sess2 = sess_dedupe(sess)
        for chemid_name in sess2:
            yield chemid_name

def gather_pubtator_chem_altnames(relf, fn_normalize):
    hgm = HistogramNamesByKey(parse_chem_altnames(relf), fn_normalize)
    for (chemid, vs) in hgm.get():
        yield (chemid,vs)
