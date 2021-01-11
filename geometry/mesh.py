import pywavefront
import numpy as np
import glob
from utils.path import * 


def load_wavefront_scene(scene_filepath):
    """Load scene in wavefront obj file
       see https://github.com/pywavefront/PyWavefront
    """
    scene = pywavefront.Wavefront(scene_filepath, create_materials=True, collect_faces=True)
    faces = list()
    faces.append(scene.mesh_list[0].faces)

    # format size for each interleaved vertex format
    elems_per_vertex = {}
    elems_per_vertex['C3F_N3F_V3F'] = 9

    # vertex offest where each attribute is found
    pos = 6
    nor = 3
    col = 0

    # groups of vertices and normals (usually only 1)
    verts = list()
    norms = list()
    for name, material in scene.materials.items():
        # Contains the vertex format (string) such as "T2F_N3F_V3F"
        # T2F, C3F, N3F and V3F may appear in this string
        material.vertex_format
        #number of bytes per vertex
        vert_size = elems_per_vertex[material.vertex_format]

        max_vertices = len(material.vertices)//vert_size
        vert = list()
        norm = list()
        for n in range(max_vertices):
            v = material.vertices[n*vert_size:(n*vert_size+vert_size)] 
            vert.append(np.array([v[pos+0], v[pos+1], v[pos+2]]))
            norm.append(np.array([v[nor+0], v[nor+1], v[nor+2]]))

        verts.append(np.array(vert).reshape(-1,3))
        norms.append(np.array(norm).reshape(-1,3))

        # Contains the vertex list of floats in the format described above
        material.vertices
        """
        # Material properties
        material.diffuse
        material.ambient
        material.texture
        """
        print("completed. ", name)
    return scene, verts[0], norms[0], faces[0]

class Mesh:
    def __init__(self):
        self.name = "mesh"
        self.path = ""
        self.scene = None
        self.verts = [] 
        self.faces = []
        self.normals = [] 
        self.vertex_format = '' 

    def __str__(self):
        v = [str(v) for v in self.verts]
        f = [str(f) for f in self.faces]
        n = [str(n) for n in self.normals]
        
        count = "{}:\nv f n : {} {} {}".format(self.path, len(v), len(f), len(n)) 
        return "# " + count + "\nvert:" + str(v) + "\nfaces:" + str(f) + "\nnormals:" + str(n)

    def make_normals(self):
        self.normals = []
        for face in self.faces:
            p0 = self.verts[face[0]]
            p1 = self.verts[face[1]]
            p2 = self.verts[face[2]]
            
            v0 = (p1 - p0)[0:3]
            v1 = (p2 - p0)[0:3]
            n = np.cross(v0, v1)
            self.normals.append(n)

class MeshLoader:
    def __init__(self):
        self.history = [] 

    def load(self, filepaths):
        if isinstance(filepaths, str):
            filepaths = glob.glob(filepaths)
        meshes = []
        for filepath in filepaths:
            print("loading {}".format(filepath))
            meshes.append(self.read_wavefront(filepath))
            self.history.append(filepath)
        return meshes

    def read_wavefront(self, filepath):
        """
        print("Faces:", scene.mesh_list[0].faces)
        print("Vertices:", scene.vertices)
        print("Format:", scene.mesh_list[0].materials[0].vertex_format)
        print("Vertices:", scene.mesh_list[0].materials[0].vertices)
        """
        scene, verts, norms, faces = load_wavefront_scene(filepath)
        mesh = Mesh()
        mesh.scene = scene
        mesh.verts = verts 
        mesh.faces = faces
        mesh.vertex_format = scene.mesh_list[0].materials[0].vertex_format
        mesh.make_normals()
        mesh.normals = norms
        mesh.path = filepath
        print(mesh)
        return mesh


class MeshCollider:
    def __init__(self, mesh):
        self.mesh = mesh

    def check_point(self, p):
        m = self.mesh
        return False
            

            

    def check(self, points):
        """
        TODO
        ======
        . only 1 point works with vbo write
        . shape and type that works with raw points is (1,N,3) float64
        . check when points are None is main render loop (does not draw zones)
        1) implement CPU collision check and return collision points
        2) either mark & color collision points for existing pointcloud in frag shader
        3) or write points in zone render vbo
        4) or explore particle system

        """
        points = np.array([np.array([0,0,0])])
        """
        x = np.array([1,2,3,4.0])
        y = np.array([2,3,4,5.0])
        z = np.array([3,4,5,6.0])
        #points = np.dstack([x,y,z]).astype(np.float64)
        """
        return points

