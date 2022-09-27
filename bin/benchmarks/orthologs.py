
import os
import sys
import itertools

adirProj=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(adirProj)

from lib.altname_paths import *
from lib.orthologs import *
from lib.mytime import *

def main():
    for orth in itertools.islice(gather_human_orthologs(absf_human_orthologs),5):
        print("orth={}".format(orth))
    print("parse_orth_raw: {}".format(mytime(lambda: sum(1 for _ in parse_orth_raw(absf_human_orthologs)))))
    print("parse_orth2: {}".format(mytime(lambda: sum(1 for _ in parse_orth2(absf_human_orthologs)))))
    print("parse_orth3: {}".format(mytime(lambda: sum(1 for _ in parse_orth3(absf_human_orthologs)))))
    print("parse_orth4: {}".format(mytime(lambda: sum(1 for _ in parse_orth4(absf_human_orthologs)))))
    print("parse_orth: {}".format(mytime(lambda: sum(1 for _ in parse_orth(absf_human_orthologs)))))
    print("filter_orth: {}".format(mytime(lambda: sum(1 for _ in filter_orth(absf_human_orthologs)))))
    print("gather_human_orthologs: {}".format(mytime(lambda: sum(1 for _ in gather_human_orthologs(absf_human_orthologs)))))

if __name__ == '__main__':
    main()
