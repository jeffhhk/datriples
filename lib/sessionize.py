from tqdm import tqdm

def sessionize_rows(itbl, cid):
    pmidPrev=None
    sess=[]
    it = itbl().__iter__()
    it.__next__()               # TSV header
    for row in it:
        pmid=row[cid]
        if pmid != pmidPrev and len(sess)>0:
            yield sess
            sess=[]
        pmidPrev=pmid
        sess.append(row)
    yield sess

class HistogramNamesByKey():
    def __init__(self, itbl, fn):
        self._itbl = itbl
        self._fn = fn
    def get(self):
        def __count(T,k):
            if k not in T:
                T[k]=1
            else:
                num = T[k]
                T[k] = num+1

        def __add_multi_disjoint(T,k,v):
            if k not in T:
                T[k]=[v]
            else:
                vs = T[k]
                vs.append(v)
                T[k]=vs

        h1={}
        for (geneid, name) in tqdm(self._itbl):
            nname = self._fn(name)
            if len(nname)>0:
                __count(h1, (geneid, self._fn(name)))
        print("starting pass 2")
        h2={}
        for ((geneid, name),num) in tqdm(h1.items()):
            __add_multi_disjoint(h2, geneid, (name,num))
        print("starting pass 3")
        for (geneid, vs) in sorted(h2.items()):
            yield (geneid, sorted(vs, key=lambda v:-v[1]))

