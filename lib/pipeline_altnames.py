import os
from jobli2.joblib import Memory as DiskMemorize
from jobli2.joblib import Jlstream

adirProj=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
adirJoblib=os.path.join(adirProj, "cache", "joblib")
dmem = DiskMemorize(adirJoblib)

def pass_stream():
    return Jlstream(lambda : (x for x in range(0,3)))

def _fetch_mesh_to_unii():
    # query
    #     https://id.nlm.nih.gov/mesh/query?query=PREFIX+rdf%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F1999%2F02%2F22-rdf-syntax-ns%23%3E%0D%0APREFIX+rdfs%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%0D%0APREFIX+xsd%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%23%3E%0D%0APREFIX+owl%3A+%3Chttp%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23%3E%0D%0APREFIX+meshv%3A+%3Chttp%3A%2F%2Fid.nlm.nih.gov%2Fmesh%2Fvocab%23%3E%0D%0APREFIX+mesh%3A+%3Chttp%3A%2F%2Fid.nlm.nih.gov%2Fmesh%2F%3E%0D%0APREFIX+mesh2022%3A+%3Chttp%3A%2F%2Fid.nlm.nih.gov%2Fmesh%2F2022%2F%3E%0D%0APREFIX+mesh2021%3A+%3Chttp%3A%2F%2Fid.nlm.nih.gov%2Fmesh%2F2021%2F%3E%0D%0APREFIX+mesh2020%3A+%3Chttp%3A%2F%2Fid.nlm.nih.gov%2Fmesh%2F2020%2F%3E%0D%0A%0D%0ASELECT+distinct+%3Fmesh+%3FmeshLabel+%3Fr+%3Frr%0D%0AFROM+%3Chttp%3A%2F%2Fid.nlm.nih.gov%2Fmesh%3E+WHERE+%7B%0D%0A++%3Fmesh+meshv%3Aactive+1+.%0D%0A++%3Fmesh+meshv%3ApreferredMappedTo+%3Fp+.%0D%0A++%3Fp+meshv%3AtreeNumber+%3FtreeNum+.%0D%0A++FILTER%28STRSTARTS%28STR%28%3FtreeNum%29%2C+%22http%3A%2F%2Fid.nlm.nih.gov%2Fmesh%2FD%22%29%29+.%0D%0A++%3Fmesh+rdfs%3Alabel+%3FmeshLabel+.%0D%0A++%3Fmesh+meshv%3ApreferredConcept+%5Bmeshv%3AregistryNumber+%3Fr%5D+.%0D%0A++OPTIONAL+%7B%3Fmesh+meshv%3ApreferredConcept+%5Bmeshv%3ArelatedRegistryNumber+%3Frr%5D%7D%0D%0A%7D+limit+50%0D%0A&format=HTML&year=current&limit=50&offset=0#lodestart-sparql-results

    # regex columns ?r and ?rr to look like a UNII

    # collect all matching (meshid, UNII) pairs

    #     NTH: include max one meshLabel
    return pass_stream()

fetch_mesh_to_unii = dmem.cache(_fetch_mesh_to_unii)

def gather_pubtator_chem_altnames():
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
    pass

def filter_on_whitelisted_meshid():
    pass

def gather_taxomy_names():
    # for debugging

    # /data$ curl https://ftp.ncbi.nih.gov/pub/taxonomy/taxdmp.zip -o taxdmp_2022-09-15.zip

    # unzip -p /data/taxdmp_2022-09-15.zip names.dmp | grep -w 9606
    #     1909	|	NCIMB 9606	|	NCIMB 9606 <type strain>	|	type material	|
    #     9606	|	Homo sapiens Linnaeus, 1758	|		|	authority	|
    #     9606	|	Homo sapiens	|		|	scientific name	|
    #     9606	|	human	|		|	genbank common name	|
    #     199339	|	CBS 9606	|	CBS 9606 <type material>	|	type material	|
    #     685789	|	Wu 9606-39	|	Wu 9606-39 <holotype>	|	type material	|
    #     1671882	|	UFRJ 9606	|	UFRJ 9606 <holotype>	|	type material	|
    #     2184181	|	9606	|	9606 <holotype>	|	type material	|
    #     2184181	|	Chen 9606	|	Chen 9606 <holotype>	|	type material	|
    #     2845822	|	Aquabacterium sp. CECT 9606	|		|	scientific name	|
    pass


def gather_human_orthologs():
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
    pass

def gather_pubtator_chem_altnames():
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
    pass

def organize_altnames_by_human_gene():
    pass

def organize_altnames_by_unii():
    pass

def parse_chemprot():
    pass

def augment_chemprot():
    pass

def compile_relevant_pmis():
    pass

