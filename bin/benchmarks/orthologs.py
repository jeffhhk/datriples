
import os
import sys
import itertools

adirProj=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(adirProj)

from lib.orthologs import *
from lib.mytime import *

def main():
    absf = os.path.join(adirProj, "cache", "external", "gene_orthologs.gz")
    for orth in itertools.islice(gather_human_orthologs(absf),5):
        print("orth={}".format(orth))
    print("parse_orth_raw: {}".format(mytime(lambda: sum(1 for _ in parse_orth_raw(absf)))))
    print("parse_orth2: {}".format(mytime(lambda: sum(1 for _ in parse_orth2(absf)))))
    print("parse_orth3: {}".format(mytime(lambda: sum(1 for _ in parse_orth3(absf)))))
    print("parse_orth4: {}".format(mytime(lambda: sum(1 for _ in parse_orth4(absf)))))
    print("parse_orth: {}".format(mytime(lambda: sum(1 for _ in parse_orth(absf)))))
    print("filter_orth: {}".format(mytime(lambda: sum(1 for _ in filter_orth(absf)))))
    print("gather_human_orthologs: {}".format(mytime(lambda: sum(1 for _ in gather_human_orthologs(absf)))))

if __name__ == '__main__':
    main()
