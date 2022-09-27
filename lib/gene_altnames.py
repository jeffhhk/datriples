import subprocess
from tqdm import tqdm

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

cidGeneid=2
cidName=3

def parse_gene_altnames_raw(relf):
    proc=subprocess.Popen(['zcat',relf],
        stdout=subprocess.PIPE,
        encoding='utf-8')
    for line in proc.stdout:
        yield line.rstrip("\n").split("\t")

def parse_gene_altnames(relf):
    it = parse_gene_altnames_raw(relf)
    it.__next__()               # TSV header
    for row in it:
        geneid=row[cidGeneid]
        name=row[cidName]
        yield (geneid, name)

def __count(T,k):
#    k=(geneid,name)
    if k not in T:
        T[k]=1
    else:
        num = T[k]
        T[k] = num+1

def __add_multi_disjoint(T,k,v):
    if k not in T:
        T[k]=[v]
    else:
        vs = T[k]
        vs.append(v)
        T[k]=vs

# Group the data by geneid.  Report the results as a generator of (k,v) pairs so that they can
# be cached with DiskgenMem.
def gather_pubtator_gene_altnames(relf, fn_normalize):
    h1={}
    for (geneid, name) in tqdm(parse_gene_altnames(relf)):
        __count(h1, (geneid, fn_normalize(name)))
    print("starting pass 2")
    h2={}
    for ((geneid, name),num) in tqdm(h1.items()):
        __add_multi_disjoint(h2, geneid, (name,num))
    print("starting pass 3")
    for (geneid, vs) in sorted(h2.items()):
        yield (geneid, sorted(vs))


