import os
from xml.sax.saxutils import escape
import itertools

def mkdirp_for(rfile):
    os.makedirs(os.path.dirname(rfile), exist_ok=True)

class NerreXml():
    def __init__(self) -> None:
        pass

    def _events(self, this, docid):
        ich_start={}
        ich_stop={}
        for ent in this.get_entities(docid):
            ich_start[ent["entid"]]=ent["ich_start"]
            ich_stop[ent["entid"]]=ent["ich_stop"]
        # mnemonic: tb: "tiebreaker" - encourage rel/ent tags to be well-formed when possible
        return itertools.chain(
            ({"ich":e["ich_start"], "end":"start", "tb":2, "type":"ent", "e":e} for e in this.get_entities(docid)),
            ({"ich":e["ich_stop"], "end":"stop", "tb":3, "type":"ent", "e":e} for e in this.get_entities(docid)),
            ({"ich":ich_start[e["entid_1"]], "end":"start", "tb":1, "type":"rel", "e":e} for e in this.get_rels(docid)),
            ({"ich":ich_stop[e["entid_1"]], "end":"stop", "tb":4, "type":"rel", "e":e} for e in this.get_rels(docid)),
            ({"ich":ich_start[e["entid_2"]], "end":"start", "tb":1, "type":"rel", "e":e} for e in this.get_rels(docid)),
            ({"ich":ich_stop[e["entid_2"]], "end":"stop", "tb":4, "type":"rel", "e":e} for e in this.get_rels(docid))
            )

    # Export xml-shaped data for 3 stage triple extraction
    def write(self, this, rfileOut):
        mkdirp_for(rfileOut)
        with open(rfileOut,"w") as f:
            f.write("<xml>\n")
            for docid in sorted(this._abstracts.keys()):
                abstract=this._abstracts[docid]
                f.write("<doc docid=\"{}\">".format(docid))
                f.write("<title>{}</title>".format(escape(abstract["title"])))
                f.write("<text>")
                txt=abstract["title"]+"\t"+abstract["txt"]
                evs=sorted(
                    self._events(this,docid),
                    key=lambda entity: (entity["ich"], entity["tb"]))
                ichL=0
                for ev in evs:
                    ichR=ev["ich"]
                    n=ev["type"]
                    # TODO?: ev["e"]["classid"]
                    f.write(escape(txt[ichL:ichR]))
                    stSlash="/" if ev["end"]=="stop" else ""
                    stId=ev["e"]["relid"] if ev["type"]=="rel" else ev["e"]["entid"]
                    stClass=ev["e"]["relclass"] if ev["type"]=="rel" else ev["e"]["classid"]
                    f.write("<{}{} {}id=\"{}\" class=\"{}\">".format(stSlash, n, n, stId, stClass))
                    ichL=ichR
                f.write(escape(txt[ichL:]))
                f.write("</text></doc>\n")
            f.write("</xml>\n")
