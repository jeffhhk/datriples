import re

# Workaround:
#
#    python -c 'import re; re.sub(r"[^a-zA-Z0-9]+", "NFKB1\\2", " ")'
#    ...
#    re.error: invalid group reference 2 at position 6
#
#
# No satisfactory answer found:
#   https://stackoverflow.com/questions/48703979/invalid-group-reference-when-using-re-sub
#   https://stackoverflow.com/questions/8441984/python-re-sub-ignore-backreferences-in-the-replacement-string
#   

def sub_all_plain_string(re_x, stSearch, stRep):
    ret=[]  # https://stackoverflow.com/questions/19926089/python-equivalent-of-java-stringbuffer
    i=0
    m = re_x.search(stSearch,i)
    if m is None:
        ret.append(stSearch)
    else:
        while True:
            stSkipped = stSearch[i:m.start()]
            if i>0:
                ret.append(stRep)
            ret.append(stSkipped)
            i=m.end()
            m = re_x.search(stSearch,i)
            if m is None:
                break
        stSkipped = stSearch[i:]
        ret.append(stRep)
        ret.append(stSkipped)
    return "".join(ret)

