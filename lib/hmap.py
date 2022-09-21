def _find_hdr(hdr, hdrsFound):
    for j in range(0,len(hdrsFound)):
        if hdr==hdrsFound[j]:
            return j
    return None

"""
hmap_build: build an integer header map to find a list of subscribed columns among a list of found columns.

Example:

    hmap_build(["orange","watermelon"],["apple","watermelon","orange","bananna"])

    returns: [2,1]
"""

def hmap_build(hdrsSub, hdrsFound):
    hmap=[]
    for i in range(0,len(hdrsSub)):
        k=_find_hdr(hdrsSub[i], hdrsFound)
        if k is None:
            raise Exception("could not find requested header: {}".format(hdrsSub[i]))
        hmap.append(k)
    return hmap

