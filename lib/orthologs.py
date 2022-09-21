import os
import sys
import subprocess
from .hmap import *
from collections import namedtuple

# https://ftp.ncbi.nih.gov/gene/DATA/gene_orthologs.gz

# zcat ~/Downloads/gene_orthologs.gz | head
#     #tax_id     GeneID  relationship    Other_tax_id    Other_GeneID
#     7955        30037   Ortholog        7830    119955596
#     7955        30037   Ortholog        7897    102366554
#     7955        30037   Ortholog        7936    118206824
#     7955        30037   Ortholog        7994    103038481
#     7955        30037   Ortholog        7998    108255935
#     7955        30037   Ortholog        8005    113577924
#     7955        30037   Ortholog        8010    105014395
#     7955        30037   Ortholog        8049    115554508
#     7955        30037   Ortholog        8078    105915626

# zcat ~/Downloads/gene_orthologs.gz | perl -ne 'chomp($_); @F=split(/\t/,$_,-1); $s=$F[0]; $o=$F[3]; print "$s\n$o\n";' | tsv-summarize --group-by 1 --count | sort -n -r -k2,2 | less

#     9606    5976738
#     7955    802861
#     75352   19671
#     1606681 19255
#     90988   19008
#     42514   18836
#     42526   18743
#     7994    18687
#     8005    18183
#     9598    17762
#     310915  17747
#     9597    17666
#     29144   17621
#     9601    17587
#     9544    17578

class Orth(namedtuple('Orth', ['taxid1', 'geneid1', 'rel', 'taxid2', 'geneid2'])):
    @classmethod
    def hdrsExt(cls):
        return ["#tax_id", "GeneID","relationship", "Other_tax_id", "Other_GeneID"]
    @classmethod
    def makeExt(cls, hmap, F):
        return cls._make([F[hmap[i]] for i in range(0,len(hmap))])


def parse_orth_raw(relf):
    proc=subprocess.Popen(['zcat',relf],
        stdout=subprocess.PIPE,
        encoding='utf-8')
    for line in proc.stdout:
        yield line.rstrip("\n").split("\t")

def parse_orth(relf):
    it = parse_orth_raw(relf)
    hdrsF=it.__next__()                      # TSV header
    hmap = hmap_build(Orth.hdrsExt(),hdrsF)
    for F in it:
        yield Orth.makeExt(hmap, F)

def parse_orth2(relf):
    it = parse_orth_raw(relf)
    hdrsF=it.__next__()                      # TSV header
    hmap = hmap_build(Orth.hdrsExt(),hdrsF)
    for F in it:
        yield [F[hmap[i]] for i in range(0,len(hmap))]

def parse_orth3(relf):
    it = parse_orth_raw(relf)
    hdrsF=it.__next__()                      # TSV header
    hmap = hmap_build(Orth.hdrsExt(),hdrsF)
    for F in it:
        G=[]
        for i in range(0,len(hmap)):
            G.append(F[hmap[i]])
        yield G

def parse_orth4(relf):
    it = parse_orth_raw(relf)
    hdrsF=it.__next__()                      # TSV header
    hmap = hmap_build(Orth.hdrsExt(),hdrsF)
    for F in it:
        G=[None]*len(hmap)
        for i in range(0,len(hmap)):
            G.append(F[hmap[i]])
        yield G

def filter_orth(relf):
    for orth in parse_orth(relf):
        if orth.rel == "Ortholog":
            yield orth

taxid_human = 9606

def gather_human_orthologs(relf):
    sttaxid_human=str(taxid_human)
    for orth in filter_orth(relf):
        if orth.taxid1 == sttaxid_human and orth.taxid2 != sttaxid_human:
            yield orth
        elif orth.taxid2 == sttaxid_human and orth.taxid1 != sttaxid_human:
            yield Orth(orth.taxid2, orth.geneid2, orth.rel, orth.taxid1, orth.geneid1)




