import os
import sys
import itertools
import re

adirProj=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(adirProj)

from lib.chemprot import Chemprot

def run_main():
    rfileA=os.path.join(adirProj, "status_quo/chemprot_test_gs/chemprot_test_abstracts_gs.tsv")
    rfileE=os.path.join(adirProj, "status_quo/chemprot_test_gs/chemprot_test_entities_gs.tsv")
    rfileR=os.path.join(adirProj, "status_quo/chemprot_test_gs/chemprot_test_relations_gs.tsv")
    cp=Chemprot()
    cp.load(rfileA, rfileE, rfileR)
    cp.export2("/dev/stdout")

if __name__ == '__main__':
    run_main()
