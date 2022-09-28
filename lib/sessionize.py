
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

