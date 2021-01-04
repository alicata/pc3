import pywavefront
import numpy as np
import glob


class Mesh:
    def __init__(self):
        self.name = "mesh"
        self.path = ""
        self.verts = [] 
        self.faces = []
        self.normals = [] 
        self.vertex_format = None 

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
        scene = pywavefront.Wavefront(
            filepath,
            create_materials=True,
            collect_faces=True,
        )
        """
        print("Faces:", scene.mesh_list[0].faces)
        print("Vertices:", scene.vertices)
        print("Format:", scene.mesh_list[0].materials[0].vertex_format)
        print("Vertices:", scene.mesh_list[0].materials[0].vertices)
        """
        mesh = Mesh()
        mesh.verts = list() #scene.vertices
        for v in scene.vertices:
            mesh.verts.append(np.array(v))
        mesh.faces = scene.mesh_list[0].faces
        mesh.vertex_format = scene.mesh_list[0].materials[0].vertex_format
        mesh.make_normals()
        mesh.path = filepath
        print(mesh)
        return mesh

class MeshCollider:
    def __init__(self, mesh):
        self.mesh = mesh

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

