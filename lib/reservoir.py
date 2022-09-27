import random

# Adapted from:
#   https://en.wikipedia.org/wiki/Reservoir_sampling#Simple_algorithm
# Modified so that the first $k

def reservoir(xs,k,rand=random.Random()):
    i=0
    sample=[None]*k
    for x in xs: 
        j = rand.randrange(0,i+1)
        if i > 0 and i < k:
            sample[i]=sample[j]
        if j < k:
            sample[j] = x
        i+=1
    return sample

