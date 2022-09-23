
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

# TODO:
#     gather_pubtator_gene_altnames():

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

