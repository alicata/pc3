import numpy as np


def domain_range_swap_yz(i, max_range=255):
    """Given an frame swap one domain dimension with range."""
    if i is None:
        return None

    h, w = i.shape[0:2]
    x = np.tile(i[0,:], h).flatten()
    y = np.repeat(i[0,:], w).flatten()
    z = i[:,:,0]

    j = np.zeros((max_range+1, w, 3), np.uint8)
    
    for n in range(w*h):
        xx = n % w
        yy = n // w
         
        zz = max_range-z[yy,xx]

        if j[zz,xx][0] < yy:
            j[zz,xx]=(yy,yy,yy)
    return j