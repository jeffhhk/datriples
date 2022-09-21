
# TODO:
#     fetch_mesh_to_only_unii()

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

# TODO:
#     gather_human_orthologs()

def gather_pubtator_gene_altnames():
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

