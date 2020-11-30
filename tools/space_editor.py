import numpy as np
import cv2 
import transform.projection
import pix.render


def make_grid(n, z_in_front_negative=True): 
    """Grid of n x n blocks (1/2x1/2 unit each)"""

    dim_count = n + 1
    x_val = np.linspace(-n/4, n/4, dim_count)
    z_val = np.linspace(1, 1 + n/2, dim_count)

    """camera view (eye) space requirs negative z in front.
       sometimes W=V, sometimes W[z] = -V[z]
    """
    if z_in_front_negative:
        z_val = -z_val

    x_coord = np.meshgrid(x_val, z_val)[0].flatten()
    z_coord = np.meshgrid(x_val, z_val)[1].flatten()
    
    y0 = np.ones(dim_count*dim_count)*-0.25
    y1 = np.ones(dim_count*dim_count)*0.25

    base = np.array(list(zip(x_coord, y0, z_coord)))
    top = np.array(list(zip(x_coord, y1, z_coord)))
    grid = np.concatenate((base, top), axis=0)

    return grid

def edit(n):
    grid =  make_grid(n, z_in_front_negative=True)
    screen_size = [640, 480]
    W, H = screen_size

    [print(p) for p in grid]

    frame_buffer = np.zeros((H, W), dtype=np.uint8)
    frustum = transform.projection.Frustum()
    frustum.from_intrinsics(focal_length=0.01, fov_h=90, fov_v=60, max_distance=10)
    P = frustum.perspective_matrix()

    """world and eye space are same, make grid points homogeneous"""
    vertex_position_eye = np.insert(grid, 3, values=1, axis=1)
    vertex_position_clip = vertex_position_eye @ P
    ndc_x = vertex_position_clip[:,0] / -vertex_position_eye[:, 2]
    ndc_y = vertex_position_clip[:,1] / -vertex_position_eye[:, 2]
    ndc_z = vertex_position_clip[:,2] / -vertex_position_eye[:, 2]

    """ NDC to screen coordinates """
    screen_x = (ndc_x + 1)/2 * W
    screen_y = H * (1 - (ndc_y + 1)/2)
    pixel_points = np.vstack([screen_x, screen_y]).T
    pixel_points = pixel_points[pixel_points[:,0]<W] 
    pixel_points= pixel_points[pixel_points[:,0]>=0] 
    pixel_points = pixel_points[pixel_points[:,1]<H] 
    pixel_points= pixel_points[pixel_points[:,1]>=0] 
    
    pix.render.points(frame_buffer, pixel_points)   
    cv2.imshow('projection - clip space', frame_buffer)
    cv2.waitKey(0)
    



    
if __name__=="__main__":
    edit(5)
