
# TODO:
#     fetch_mesh_to_only_unii()

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

def organize_altnames_by_unii():
    pass

def parse_chemprot():
    pass

def augment_chemprot():
    pass

def compile_relevant_pmis():
    pass

