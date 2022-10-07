import re
import subprocess
from tqdm import tqdm
from lib.re_sub import *

from lib.sessionize import *

# zcat /data/gene2pubtatorcentral_2022-09-15.gz | pv | ~/bin/reservoir.pl 20
#     34456932	Gene	838452	PYL9|RCAR1	GNormPlus
#     10074924	Gene	2099	estrogen receptor	GNormPlus
#     29545832	Gene	2064	HER2	GNormPlus
#     21985955	Gene	3630	insulin	GNormPlus
#     32582168	Gene	12519	CD80	GNormPlus
#     29109483	Gene	4780	Nrf2	GNormPlus
#     29436792	Gene	960	CD44	GNormPlus
#     15828049	Gene	1548		CTD
#     31548609	Gene	153129	SLC38A9	GNormPlus
#     11781232	Gene	16183	IL-2	GNormPlus
#     20195532	Gene	5293	PI3Kdelta	GNormPlus
#     35227297	Gene	1788	DNMT3A	GNormPlus
#     25379667	Gene	3558	interleukin-2|IL-2|Lymphokine	GNormPlus
#     18724357	Gene	15977	IFN-beta	GNormPlus
#     19953087	Gene	8463		gene2pubmed|BioGRID
#     21285873	Gene	24410	NR2B	GNormPlus|gene2pubmed
#     30602081	Gene	5562	AMPK	GNormPlus
#     24618901	Gene	43791	Lgl	GNormPlus
#     33767656	Gene	26047	Caspr2|contactin-associated protein-like 2	GNormPlus
#     32327174	Gene	238	ALK	GNormPlus
#     27125264	Gene	93896	GLP-2	GNormPlus

# zcat /data/gene2pubtatorcentral_2022-09-15.gz | pv | wc -l
#     2.72GiB 0:00:13 [ 209MiB/s] [                             <=>                                                                           ]
#         67 078 503

# - how many unique gene alternative names are there?
#     zcat /data/gene2pubtatorcentral_2022-09-15.gz | pv | perl -ne 'chomp($_); @F=split(/\t/,$_,-1); $st0=$F[3]; $st1=uc($st0); $st1 =~ s/[^a-zA-Z0-9]+/ /g; print "$st1\n";' | time tsv-summarize --group-by 1 --count | wc -l
#         3331273

# - how many unique genes?
#     zcat /data/gene2pubtatorcentral_2022-09-15.gz | cut -f3 | time tsv-summarize --group-by 1 --count | wc -l
#         875987

cidPmid=0
cidGeneid=2
cidNames=3

def parse_gene_altnames_raw(relf):
    proc=subprocess.Popen(['zcat',relf],
        stdout=subprocess.PIPE,
        encoding='utf-8')
    for line in proc.stdout:
        yield line.rstrip("\n").split("\t")

def does_row_contain_single_gene(row):
    geneid=row[cidGeneid]
    return (
        geneid != "None"                  # phrase is a gene, but gene ID is not detected   (1 in 1212 rows).  Example:
            # 35660018	Gene	None	O-linked beta-N-acetylglucosamine transferase|Myb	GNormPlus
        and not geneid.__contains__(";")  # phrase is constructed to include multiple genes (1.2% of rows).  Examples:
            # ['28555004', 'Gene', '3065;3066;8841', 'Histone deacetylases 1, 2 and 3', 'GNormPlus']
            # ['30666004', 'Gene', '3605;112744', 'interleukin-17A and -17F', 'GNormPlus']
    )


# Deduplicate so that counts become counts of separate articles
def sess_dedupe(sess):
    h={}
    for row in sess:
        if does_row_contain_single_gene(row):
            geneid=row[cidGeneid]
            geneid=int(geneid)
            names=row[cidNames].split("|")
            for name in names:
                if (geneid, name) not in h:
                    h[(geneid,name)] = True
    return h.keys()
        # except:
        #     print("offending row: {}".format(row))

def parse_gene_altnames(relf):
    for sess in sessionize_rows(lambda: parse_gene_altnames_raw(relf), cidPmid):
        sess2 = sess_dedupe(sess)
        for geneid_name in sess2:
            yield geneid_name

re_name=re.compile(r"[^\(\)a-zA-Z0-9]+")

def normalize_pubtator_gene_altname(name):
    #return re_name.sub(name.upper(),r" ")
    #print("name={}".format(name))
    #return re.sub(re_name, name, " ")  # name=NFKB1\2  => re.error: invalid group reference
    #return re_name.sub(name, " ")      # name=NFKB1\2  => re.error: invalid group reference
    return sub_all_plain_string(re_name, name, " ").rstrip().lstrip()

# Group the data by geneid.  Report the results as a generator of (k,v) pairs so that they can
# be cached with DiskgenMem.
def gather_pubtator_gene_altnames(relf, fn_normalize):
    hgm = HistogramNamesByKey(parse_gene_altnames(relf), fn_normalize)
    for (geneid, vs) in hgm.get():
        yield (geneid,vs)


