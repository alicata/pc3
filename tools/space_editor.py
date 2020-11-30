import numpy as np
import cv2 
import transform.projection


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
    grid =  make_grid(n, z_in_front_negative=True)
    screen_size = np.array([320,240])

    [print(p) for p in grid]

    frame_buffer = np.zeros(screen_size, dtype=np.uint8)
    frustum = transform.projection.Frustum()
    frustum.from_intrinsics(focal_length=0.01, fov_h=90, fov_v=60, max_distance=10)
    P = frustum.perspective_matrix()

    """world and eye space are same, make grid points homogeneous"""
    vertex_position_eye = np.insert(grid, 3, values=1, axis=1)
    vertex_position_clip = P * vertex_position_eye 
    vertex_position_ndc = grid / vertex_position_clip[:, 3]

    """ NDC to screen coordinates """
    W, H = screen_size
    vertex_position_scr = (vertex_position_ndc + 1)/2 * np.array([W, H, 1])
    vertex_position_scr[:,1] = H - vertex_position_scr[:,1]
    
    pixel_points = vertex_position_scr[:,0:2]

    pix.render.line(frame_buffer, pixel_points)   
    cv2.imshow('projection - clip space', frame_buffer)
    cv2.waitKey(0)
    



    
if __name__=="__main__":
    edit(5)
