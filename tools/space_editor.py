import transform.projection
import numpy as np


def make_grid(n, z_in_front_negative=True): 
    """Grid of n x n blocks (1/2x1/2 unit each)"""

    dim_count = n + 1
    x_val = np.linspace(-n/4, n/4, dim_count)
    z_val = np.linspace(0, n/2, dim_count)

    """camera view (eye) space requirs negative z in front.
       sometimes W=V, sometimes W[z] = -V[z]
    """
    if z_in_front_negative:
        z_val = -z_val

    x_coord = np.meshgrid(x_val, z_val)[0].flatten()
    z_coord = np.meshgrid(x_val, z_val)[1].flatten()
    
    y0 = np.ones(dim_count*dim_count)*0
    y1 = np.ones(dim_count*dim_count)*1

    base = np.array(list(zip(x_coord, y0, z_coord)))
    top = np.array(list(zip(x_coord, y1, z_coord)))
    grid = np.concatenate((base, top), axis=0)

    return grid

def edit(n):
    grid =  make_grid(n, z_in_front_negative=False)
    screen_size = np.array([320,240])

    [print(p) for p in grid]
    



    
if __name__=="__main__":
    edit(5)
