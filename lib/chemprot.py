import sys
import json
import os
from xml.sax.saxutils import escape
import itertools

def mkdirp_for(rfile):
    os.makedirs(os.path.dirname(rfile), exist_ok=True)

class Chemprot(object):
    def __init__(self) -> None:
        self._abstracts={}             # docid => {id:, title:, txt:}
        self._entities_by_abstract={}  # docid => list({docid:, entid:, ent_name:, ich_start:, ich_stop:})
        self._rels={}                  # docid => list({docid:, relid:, relclass:, relfoo:, rel_name:, entid_1: entid_2:})

    def add_abstract(self,abstract):
        docid=abstract["id"]
        self._abstracts[docid]=abstract

    def number_abstracts(self):
        ich = 0
        for k in sorted(self._abstracts.keys()):
            abstract=self._abstracts[k]
            abstract["ich"]=ich
            txt=abstract["txt"]
            ich += len(txt)+1   # 1 for size of EOL

    def add_entity(self,entity):
        docid=entity["docid"]
        v=[]
        if docid in self._entities_by_abstract:
            v=self._entities_by_abstract[docid]
        v.append(entity)
        self._entities_by_abstract[docid]=v
    
    def add_rel(self,rel):
        docid=rel["docid"]
        v=[]
        if docid in self._rels:
            v=self._rels[docid]
        v.append(rel)
        self._rels[docid]=v

    def get_rels(self,docid):
        return [] if docid not in self._rels else self._rels[docid]

    def get_entities(self,docid):
        return [] if docid not in self._entities_by_abstract else self._entities_by_abstract[docid]

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
                self.add_abstract({
                    "id":docid,
                    "title":title,
                    "txt":txt
                })
        self.number_abstracts()
        with open(rfile_entities) as f:
            for X in f:
                X=X.rstrip()
                X = X.split("\t")
                docid = int(X[0])
                entid = X[1]
                ent_name = X[2]
                ich_start = int(X[3])
                ich_stop = int(X[4])
                self.add_entity({
                    "docid":docid,
                    "entid":entid,
                    "ent_name":ent_name,
                    "ich_start":ich_start,
                    "ich_stop":ich_stop
                })
        with open(rfile_rel) as f:
            docidPrev=None
            relid=0
            for X in f:
                X=X.rstrip()
                X = X.split("\t")
                docid = int(X[0])
                relclass = X[1]
                relfoo = X[2]
                rel_name = X[3]
                entid_1 = X[4][5:]
                entid_2 = X[5][5:]
                if docid!=docidPrev:
                    relid=0
                relid += 1
                self.add_rel({
                    "docid":int(docid),
                    "relid":relid,
                    "relclass":relclass,
                    "relfoo":relfoo,
                    "rel_name":rel_name,
                    "entid_1":entid_1,
                    "entid_2":entid_2
                })
                docidPrev=docid

    # Export data for brat labeling tool
    def export1(self):
        fnOutTxt="ChemProt_Corpus/chemprot_brat.txt"
        fnOutAnn="ChemProt_Corpus/chemprot_brat.ann"
        mkdirp_for(fnOutTxt)
        with open(fnOutTxt,"w") as f:
            for docid in sorted(self._abstracts.keys()):
                abstract=self._abstracts[docid]
                f.write(abstract["title"])
                f.write("\n")
                f.write(abstract["txt"])
                f.write("\n")
        mkdirp_for(fnOutAnn)
        with open(fnOutAnn,"w") as f:
            for docid in sorted(self._abstracts.keys()):
                for entity in sorted(self._entities_by_abstract[docid], key=lambda e:e["ich_start"]):
                    abstract=self._abstracts[docid]
                    ich=abstract["ich"]
                    ich_start=ich+entity["ich_start"]
                    ich_stop= ich+entity["ich_stop"]
                    personid_bogus="NTL"
                    e=[
                        entity["entid"],
                        entity["ent_name"],
                        str(ich_start),
                        str(ich_stop),
                        personid_bogus
                    ]
                    f.write("\t".join(e))
                    f.write("\n")
            # TODO: emit relations

    def events(self, docid):
        ich_start={}
        ich_stop={}
        for ent in self.get_entities(docid):
            ich_start[ent["entid"]]=ent["ich_start"]
            ich_stop[ent["entid"]]=ent["ich_stop"]
        # mnemonic: tb: "tiebreaker" - encourage rel/ent tags to be well-formed when possible
        return itertools.chain(
            ({"ich":e["ich_start"], "end":"start", "tb":2, "type":"ent", "e":e} for e in self.get_entities(docid)),
            ({"ich":e["ich_stop"], "end":"stop", "tb":3, "type":"ent", "e":e} for e in self.get_entities(docid)),
            ({"ich":ich_start[e["entid_1"]], "end":"start", "tb":1, "type":"rel", "e":e} for e in self.get_rels(docid)),
            ({"ich":ich_stop[e["entid_1"]], "end":"stop", "tb":4, "type":"rel", "e":e} for e in self.get_rels(docid)),
            ({"ich":ich_start[e["entid_2"]], "end":"start", "tb":1, "type":"rel", "e":e} for e in self.get_rels(docid)),
            ({"ich":ich_stop[e["entid_2"]], "end":"stop", "tb":4, "type":"rel", "e":e} for e in self.get_rels(docid))
            )

    # Export xml-shaped data for 3 stage triple extraction
    def export2(self,rfileOut):
        mkdirp_for(rfileOut)
        with open(rfileOut,"w") as f:
            f.write("<xml>\n")
            for docid in sorted(self._abstracts.keys()):
                abstract=self._abstracts[docid]
                f.write("<doc docid=\"{}\">".format(docid))
                f.write("<title>{}</title>".format(escape(abstract["title"])))
                f.write("<text>")
                txt=abstract["title"]+"\t"+abstract["txt"]
                evs=sorted(
                    self.events(docid),
                    key=lambda entity: (entity["ich"], entity["tb"]))
                ichL=0
                for ev in evs:
                    ichR=ev["ich"]
                    n=ev["type"]
                    # TODO?: ev["e"]["ent_name"]
                    f.write(escape(txt[ichL:ichR]))
                    stSlash="/" if ev["end"]=="stop" else ""
                    stId=ev["e"]["relid"] if ev["type"]=="rel" else ev["e"]["entid"]
                    stClass=ev["e"]["relclass"] if ev["type"]=="rel" else ev["e"]["ent_name"]
                    f.write("<{}{} {}id=\"{}\" class=\"{}\">".format(stSlash, n, n, stId, stClass))
                    ichL=ichR
                f.write(escape(txt[ichL:]))
                f.write("</text></doc>\n")
            f.write("</xml>\n")

    # From BLUE_Benchmark/blue/bert/create_cdr_bert.py
    def _find_toks(self, sentences, start, end):
        toks = []
        for sentence in sentences:
            for ann in sentence.annotations:
                span = ann.total_span
                if start <= span.offset and span.offset + span.length <= end:
                    toks.append(ann)
                elif span.offset <= start and end <= span.offset + span.length:
                    toks.append(ann)
        return toks

    # # Export data formatted for run_bluebert_ner.py task_name=bc5cdr (BC5CDRProcessor)
    # # Ported from BLUE_Benchmark/blue/bert/create_cdr_bert.py
    #
    # from blue.ext.preprocessing import tokenize_text, print_ner_debug, write_bert_ner_file
    #
    # def export3(self,rfileOut):
    #     validate_mentions=None
    #     mkdirp_for(rfileOut)
    #     total_sentences = []

    #     for docid in tqdm.tqdm(sorted(self._abstracts.keys())):
    #         abstract=self._abstracts[docid]
    #         txt=abstract["title"]+"\t"+abstract["txt"]
    #         entities=sorted(
    #             (self._entities_by_abstract[docid] if docid in self._entities_by_abstract else []),
    #             key=lambda entity: entity["ich_start"])

    #         sents = tokenize_text(txt, docid)

    #         ichL=0
    #         for entity in entities:
    #             #if ann.type == entity_type:    # entity["ent_name"]
    #             anns = self._find_toks(sents, entity["ich_start"], entity["ich_stop"])
    #             if len(anns) == 0:
    #                 print(f'Cannot find {doc.pmid}: {ann}')
    #                 print_ner_debug(sents, ann.start, ann.end)
    #                 exit(1)
    #             has_first = False
    #             for ann in anns:
    #                 if not has_first:
    #                     ann.infons['NE_label'] = 'B'
    #                     has_first = True
    #                 else:
    #                     ann.infons['NE_label'] = 'I'

    #         total_sentences.extend(sents)

    #     cnt = write_bert_ner_file(rfileOut, total_sentences)
    #     if validate_mentions is not None and validate_mentions != cnt:
    #         print(f'Should have {validate_mentions}, but have {cnt} {entity_type} mentions')
    #     else:
    #         print(f'Have {cnt} mentions')

