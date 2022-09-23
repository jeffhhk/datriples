
import os
import shutil
from lib.diskgen import *

class DiskgenMem:
    def __init__(self, absdStorage) -> None:
        self._absdStorage = absdStorage
        self._numRead = 0    # for automated test
        self._numWrite = 0   # for automated test
        os.makedirs(self._absdStorage, exist_ok=True)
    
    def cache(self, itbl, relf):
        absf = os.path.join(self._absdStorage, relf)
        if os.path.exists(absf):
            self._numRead += 1
            return lambda: Diskgen.read(absf)
        absfTmp = os.path.join(self._absdStorage, "{}.tmp".format(relf))
        if os.path.exists(absfTmp):
            os.remove(absfTmp)
        if not os.path.exists(os.path.dirname(absfTmp)):
            os.makedirs(os.path.dirname(absfTmp))
        self._numWrite += 1
        Diskgen.write(itbl(), absfTmp)
        shutil.move(absfTmp, absf)
        self._numRead += 1
        return lambda: Diskgen.read(absf)

class DictMem:
    def __init__(self, fn):
        self._fn = fn
        self._d = None
    def __call__(self):
        if not self._d:
            d = {}
            for (k,v) in self._fn():
                d[k]=v
            self._d=d
        return self._d
