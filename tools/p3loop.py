import cv2
import sys
import numpy as np
import json

import pywavefront


def xy2z(i):
    if i is None:
        return None

    h, w = i.shape[0:2]
    x = np.tile(i[0,:], h).flatten()
    y = np.repeat(i[0,:], w).flatten()
    z = i[:,:,0]
    j = np.zeros((256, w, 3), np.uint8)
    
    for n in range(w*h):
        xx = n % w
        yy = n // w
         
        zz = 255-z[yy,xx]

        #print(xx, yy, zz, w, h)
        if j[zz,xx][0] < yy:
            j[zz,xx]=(yy,yy,yy)
    return j
    

def draw_quad_meshes(i, s, meshes, id, order=[0,1]):

    for d, mesh in enumerate(meshes):
        #if d != id and id >= 0:
        #    continue
        col = [(0, 255, 0), (255, 255, 0), (255, 0, 0 )]
        b, g, r = col[d]
        colf = (b, g, r)
        colb = (b//2, g//2, r//2)
        v = mesh.verts[0:8]
        
        def line(n, m, c):
            o0 = order[0]
            o1 = order[1]
            if o0==0 and o1 ==1:
                p0 =  ( s*int(v[n][o0]), s*int(v[n][o1]) )
                p1 =  ( s*int(v[m][o0]), s*int(v[m][o1]) )
            elif o0==0 and o1 ==2:
                p0 =  ( s*int(v[n][o0]), s*255-s*int(v[n][o1]) )
                p1 =  ( s*int(v[m][o0]), s*255-s*int(v[m][o1]) )
            cv2.line(i, p0, p1, c)

        line(3, 7, colb) 
        line(0, 4, colb)  

        line(3, 0, colb)
        line(0, 1, colb)
        line(2, 3, colf)
        line(1, 2, colf)
 
        line(7, 4, colb)
        line(4, 5, colb)
        line(6, 7, colf)
        line(5, 6, colf)  
        
        line(1, 5, colf) 
        line(2, 6, colf)    
  

def draw_pixel_layer(data, i):
    """Draw a pixel space layer"""
    if i is None:
        return 

    h, w = i.shape[0:2]
    s = data['scale']
    id = data['id']

    r = data['ref']
    pixel_layer = data['ref'][str(id)]["pixel"]

    # layer 0, can be line, polygon

    col = [255,0,255]
    for poly in  pixel_layer["0"]:
        pts = [tuple(np.array(ll[0:2])*s) for ll in poly]
        print(pts)
        for n, p in enumerate(pts):
            
            p0 = pts[n]
            p1 = pts[(n+1)%len(p)]

            print(n, p0, p1)
            cv2.line(i, p0, p1, col, 2)

    # polygons
    a = 2
    col = (255//a,0//a,255//a)
    for poly in pixel_layer["1"]:
        pts = [tuple(np.array(ll[0:2])*s) for ll in poly]
        for n in range(len(pts)+1):
            p0 = pts[(n+0)%len(pts)]
            p1 = pts[(n+1)%len(pts)]
            cv2.line(i, p0, p1, col, 1)

def loop(data, file):
    s = data['scale']
    meshes = data['meshes']
    try:
        i = cv2.imread(file);
        if i is None:
            return

        h, w = i.shape[0:2]

        j = xy2z(i)
        hj, wj = j.shape[0:2]
        sj = s #int((w/wj)*s)
        j = cv2.resize(j, (wj*sj, hj*sj), interpolation=cv2.INTER_NEAREST)
        draw_quad_meshes(j, s, meshes, -1, order=[0, 2])
        j = cv2.resize(j, (w*s, h*s))
        
        i = cv2.resize(i, (w*s, h*s), interpolation=cv2.INTER_NEAREST)

        draw_pixel_layer(data, i)

        if data['blank_red']:  
            i[i.sum(axis=2)==0,2]=128

        draw_quad_meshes(i, s, meshes, -1, order=[0,1])

                
        cv2.imshow(file, np.hstack((i,j)))
        
        key = cv2.waitKey(100)

        if key == ord('r'):
            data['blank_red'] = not data['blank_red']

        if key == ord('s'):
            data['scale'] = ((data['scale'] + 1) % 4) + 1

        if key == ord('q'):
            exit(0)

        data['count'] += 1        


    except Exception as e:
        print(str(e))
        pass

def get_data_from_config(config, name, id_string):
    data = {'scale' : 2, 'blank_red' : False, 'meshes' : [], 'count' : 0}

    with open(config) as f:
        default = json.load(f)
        d = default[name][id_string]
        data['id'] = d['id']
        data['config'] = str(config)
        data['name'] = name
        data['ref'] = default['ref']
        data['mesh_filepaths'] = d['mesh_filepaths']
        #data['mask_filepaths'] = d.get('mask_paths')
    return data


def load_meshes(filepaths):
    meshes = list()
    class Mesh: pass
    for filepath in filepaths:
        print(filepath)
        scene = pywavefront.Wavefront(filepath)
        verts = scene.vertices
        
        mesh = Mesh()
        mesh.verts = verts
        meshes.append(mesh)
    return meshes


def main():
    file = sys.argv[1]

    try:
        config = sys.argv[2]
        name = sys.argv[3]
        id = sys.argv[4]
        print(file, config, name, id)
    except:
        print("usage: {} imagefile <layering.json> <config name> <viewpoint or instance id>")
        print("example: {} frame0020.png debug_reference.json room01 11")
        exit(0)

    data = get_data_from_config(config, name, id)

    data['meshes'] = load_meshes(data['mesh_filepaths'])

    while True:
        loop(data, file)

main()
     