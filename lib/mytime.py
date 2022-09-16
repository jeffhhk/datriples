import time

def mytime(fn):
    t0=time.time()
    ret = fn()
    dt=time.time()-t0
    return {"dt":dt, "value":ret}
