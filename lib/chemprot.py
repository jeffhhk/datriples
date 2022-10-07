import sys
import json
import os
from collections import namedtuple

class Doc(namedtuple('Doc', [
    'id',
    'title',
    'txt'
])):
    pass

class Ent(namedtuple('Ent', [
    'docid',     # 1322047
    'entid',     # T1
    'classid',  # CHEMICAL
    'ich_start', # 1138
    'ich_stop'   # 1179
])):
    pass

class Rel(namedtuple('Rel', [
    'docid',     # 1322047
    'relid',     # auto-incremented
    'classid',   # CPR:3
    'relfoo',    # Y
    'classname', # ACTIVATOR
    'entid1',    # Arg1:T12
    'entid2'     # Arg2:T17
])):
    pass



def mkdirp_for(rfile):
    os.makedirs(os.path.dirname(rfile), exist_ok=True)

class Chemprot(object):
    def __init__(self) -> None:
        self._abstracts={}             # docid => {id:, title:, txt:}
        self._entities={}  # docid => list({docid:, entid:, classid:, ich_start:, ich_stop:})
        self._rels={}                  # docid => list({docid:, relid:, relclass:, relfoo:, classname:, entid_1: entid_2:})

    def add_abstract(self,abstract):
        docid=abstract.id
        self._abstracts[docid]=abstract

    def add_entity(self,entity):
        docid=entity.docid
        v=[]
        if docid in self._entities:
            v=self._entities[docid]
        v.append(entity)
        self._entities[docid]=v
    
    def add_rel(self,rel):
        docid=rel.docid
        v=[]
        if docid in self._rels:
            v=self._rels[docid]
        v.append(rel)
        self._rels[docid]=v

    def get_rels(self,docid):
        return [] if docid not in self._rels else self._rels[docid]

    def get_entities(self,docid):
        return [] if docid not in self._entities else self._entities[docid]

    def load(self, rfile_abstracts, rfile_entities, rfile_rel):
        rfile_abstracts = rfile_abstracts
        rfile_entities = rfile_entities
        rfile_rel = rfile_rel
        with open(rfile_abstracts) as f:
            for X0 in f:
                X1=X0.rstrip()
                X = X1.split("\t")
                docid = int(X[0])
                title = X[1]
                txt = X[2]
                if docid in self._abstracts:
                    raise "Found duplicate abstract id={}".format(docid)
                self.add_abstract(Doc(
                    docid,
                    title,
                    txt
                ))
        with open(rfile_entities) as f:
            for X in f:
                X=X.rstrip()
                X = X.split("\t")
                docid = int(X[0])
                entid = X[1]
                classid = X[2]
                ich_start = int(X[3])
                ich_stop = int(X[4])
                self.add_entity(Ent(
                    docid,
                    entid,
                    classid,
                    ich_start,
                    ich_stop
                ))
        with open(rfile_rel) as f:
            docidPrev=None
            relid=0
            for X in f:
                X=X.rstrip()
                X = X.split("\t")
                docid = int(X[0])
                relclass = X[1]
                relfoo = X[2]
                classname = X[3]
                entid_1 = X[4][5:]
                entid_2 = X[5][5:]
                if docid!=docidPrev:
                    relid=0
                relid += 1
                self.add_rel(Rel(
                    int(docid),
                    relid,
                    relclass,
                    relfoo,
                    classname,
                    entid_1,
                    entid_2
                ))
                docidPrev=docid

    # Export data for brat labeling tool
    def export1(self):
        fnOutTxt="ChemProt_Corpus/chemprot_brat.txt"
        fnOutAnn="ChemProt_Corpus/chemprot_brat.ann"
        mkdirp_for(fnOutTxt)
        with open(fnOutTxt,"w") as f:
            for docid in sorted(self._abstracts.keys()):
                abstract=self._abstracts[docid]
                f.write(abstract.title)
                f.write("\n")
                f.write(abstract.txt)
                f.write("\n")
        mkdirp_for(fnOutAnn)
        with open(fnOutAnn,"w") as f:
            for docid in sorted(self._abstracts.keys()):
                for entity in sorted(self._entities[docid], key=lambda e:e["ich_start"]):
                    abstract=self._abstracts[docid]
                    ich=abstract["ich"]
                    ich_start=ich+entity["ich_start"]
                    ich_stop= ich+entity["ich_stop"]
                    personid_bogus="NTL"
                    e=[
                        entity["entid"],
                        entity["classid"],
                        str(ich_start),
                        str(ich_stop),
                        personid_bogus
                    ]
                    f.write("\t".join(e))
                    f.write("\n")
            # TODO: emit relations



