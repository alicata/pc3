import numpy as np
import os
import cv2
import os
import itertools as it
import glob
import time

from pyrr import Matrix44
import moderngl
import moderngl_window as mglw



def depth_to_xyz(depth8):
    """Convert depth image coordinate system to opengl cs."""
    h, w = depth.shape[0:2]
    x = np.tile(np.arange(w), w)
    y = np.repeat(np.arange(h), h)
    z = depth8.flatten()
    return x, y, z

def xyz_to_gl(x,y,z, dim):
    """Convert point cloud in top-left z-pos-away to gl:
        gl: x positive-to-right, y bottom-up, z-positive-towards cam.
    """
    w, h, z_max = dim 
    x = w - (x + w/2)
    y = h - y - h/2
    z = -(z_max/2 -z)
    return x, y, z

class Dataset:
    def __init(self, dataset_name='default'):
        self.name = dataset_name    

    def load_point_data(self, filepath='data/depth8.png'):
        """Load depth8 image (rs cs) to opengl cordinate system"""
        depth8 = cv2.imread(filepath)[:,:,0]
            
        depth8 = cv2.resize(depth8, (256, 256), interpolation=cv2.INTER_NEAREST)
        h, w = depth8.shape
        d = 1

        x = np.tile(np.arange(w), w).flatten()
        y = np.repeat(np.arange(h), h).flatten()
        z = depth8.flatten() * 1.0

        min_z, max_z = 0, 255 
        x = x[z>min_z]
        y = y[z>min_z]
        z = z[z>min_z]

        x, y, z = xyz_to_gl(x,y,z, [w, h, 255]) 
        pts = np.dstack([x, y, z])
        #pts = pts[0][z < 0]
        return pts, w*h, (w, h, d)

    def gen_point_data(self):
        w, h, d = 256, 256, 256
        num_samples = w*h
        x = (np.tile(np.arange(w), w)) 
        y = (np.repeat(np.arange(h), h))
        z = np.random.randint(0, 255, d*d) 

        x, y, z = xyz_to_gl(x,y,z) 
        coordinates = np.dstack([x, y, z])

        return coordinates, w*h, (w, h, d)


class Window(mglw.WindowConfig):
    gl_version = (3, 3)
    title = "pc3"
    window_size = (2*640, 2*480)
    aspect_ratio = window_size[0] / window_size[1]
    resizable = True
    samples = 4

    resource_dir = os.path.normpath(os.path.join(__file__, '../data'))
    print('res dir: ', resource_dir)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def run(cls):
        mglw.run_window_config(cls)


class Camera:
    def __init__(self, win_size):
        self.aspect_ratio = win_size[0] / win_size[1]
        self.win = win_size
        self.reset()

    def reset(self):
        self.fov = 90.0
        self.cam_center = np.array([0, 0, -300])
        self.cam_pos = self.cam_center + np.array([0.0, 0.0, 0.0])
        self.cam_target = [0, 0, 0]
        self.cam_up = [0, 1, 0]
        self.stepper = [0, 0, 0]
        self.op = {}
        self.op['proj'] = 'ortho'
        self.op['layer'] = 'free'
        self.op['modulation'] = 'none'
        self.op['scale']= 0.25 
        self.op['fps'] = 30
    
    def orbit(self, t):
        """Make camera orbit around a path."""
        angle = 1.05 * t*np.pi/2 
        r = 130 #t #self.win[0]/8 #max(self.win[0], self.win[1]) / 2
        pos = np.array([np.cos(angle)*r,  1 , np.sin(angle)*r])
        self.cam_pos =  (pos - 0*self.cam_center)

    def disparity_shift(self, t):
        if self.op['layer'] in  ["free"]:
            shift = float(int(t*20) % 8)
            val = np.array([0, 1, 2, 1, 0, -1, -2, -1])
            shift = val[int(shift)] * 0.5
            self.cam_pos[0] += shift 
            self.cam_target[0] += shift
        elif self.op['layer'] in ["orbit"]:
            shift = float(int(t*100) % 3 - 1)
            shift *= 1
            self.cam_pos[1] += shift
            self.cam_target[1] += shift/2

    def step(self, t):
        """Step through motion trajectory."""
        if self.op['layer'] == "free":
            for dim in range(3):
                self.cam_center[dim] += self.stepper[dim]
            self.cam_pos = self.cam_center
        elif self.op['layer'] == "orbit":
            self.orbit(t) 
        if self.op['modulation'] == "disparity":
            self.disparity_shift(t)

    def axis_slide(self, axis, deltas):
        """Slide along one or more axis."""
        ax = {'z' : 2, 'y' : 1, 'x' : 0}
        for a, d in zip(axis, deltas):
            self.stepper[ax[a]] =d

    def update_pose(self, t):
        self.step(t)

        self.lookat = Matrix44.look_at(self.cam_pos, self.cam_target, self.cam_up)
        if self.op['proj'] == 'perp':
            self.proj = Matrix44.perspective_projection(self.fov, self.aspect_ratio, 0.1, 5000.0)
        else: 
            a=1024*self.op['scale']
            self.proj = Matrix44.orthogonal_projection(-a, a, -a, a, -a*4, a*4) 
        return self.mvp()

    def mvp(self):
        return self.proj * self.lookat

class PC3(Window):
    '''
    Point Cloud 
    '''
    title = "PC3 Visualizer"
    gl_version = (3, 4)

    def load_vertex_shader(self):
        vertex_shader='''
            #version 330

            uniform mat4 Mvp;

            in vec3 in_move;

            in vec3 in_position;
            in vec3 in_normal;

            out vec3 v_vert;
            out vec3 v_norm;

            void main() {
                float s = 1.0;
                gl_Position = Mvp * vec4(s*in_position + in_move, 1.0);
                v_vert = in_position + in_move;
                v_norm = in_normal;
            }
            '''
        return vertex_shader

    def load_fragment_shader(self, name):

        f_shader_firepit='''
            #version 330

            uniform vec3 Light;

            in vec3 v_vert;
            in vec3 v_norm;

            out vec4 f_color;

            void main() {
                float dist = length((v_vert - 0))/255.0;
                float lum = clamp(dot(normalize(Light - v_vert), normalize(v_norm)), 0.0, 1.0) * 0.3 + 0.7;

                //float proximity = 1.0 - length(v_vert) / 255.0;
                lum = 1.0;

                // front red back blue
                float b = clamp(dist * 1.3, 0.0, 1.0);
                float r = 1.0 - b;
                f_color = vec4(lum*r, 0.1, lum*b, 1.0);

            }
        '''

        f_shader_modulated_y='''
            #version 330

            uniform vec3 Light;

            in vec3 v_vert;
            in vec3 v_norm;

            out vec4 f_color;

            void main() {
                float lum = clamp(dot(normalize(Light - v_vert), normalize(v_norm)), 0.0, 1.0) * 0.7 + 0.3;
                float b = 1.0 - (-(v_vert.z))/255.0;
                b *= 0.5;
                float dy = 15.0;
                float g = (int(abs(v_vert.y))%int(dy))/dy;
                float r = 1.0 - b;

                f_color = vec4(r, g, b, 1.0);
            }
        '''

        f_shader_modulated='''
            #version 330

            uniform vec3 Light;

            in vec3 v_vert;
            in vec3 v_norm;

            out vec4 f_color;

            void main() {
                float lum = clamp(dot(normalize(Light - v_vert), normalize(v_norm)), 0.0, 1.0) * 0.7 + 0.3;
                //f_color = vec4(v_vert.z / 255.0, 0.0, 1.0 - v_vert.z / 255.0, 1.0);

                // center is red and lit
                //float b = (abs(v_vert.z*2)/255.0);
                //float r = 1.0 - b;

                // front red back blue
                float b = -(v_vert.z-128)/255.0;
                float r = 1.0 - b;
                f_color = vec4(lum*r, abs(sin(b*9.0)), 0.6*b, 1.0);
                //f_color = vec4(v_vert.z / 255.0, v_vert.z  / 255.0, v_vert.z / 255.0, 1.0);
            }
        '''
        fragment_shader = {
            'modulated' : f_shader_modulated,
            'mody' : f_shader_modulated_y,
            'firepit' : f_shader_firepit
        }
        return fragment_shader[name]


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.prog = self.ctx.program(
            vertex_shader=self.load_vertex_shader(),
            fragment_shader=self.load_fragment_shader("mody"),
        )

        self.off = {'x' : 0, 'y' : 0 ,'z' : 0}
        self.mvp = self.prog['Mvp']
        self.light = self.prog['Light']
        self.cam = Camera(PC3.window_size)
        self.time = dict.fromkeys({'render', 'render:load'}, 0)
        pattern = os.environ.get('PC3_FILEPATH', False)
        if pattern is False:
            print("specify input file in PC3_FILEPATH") 
            exit(0)
        self.filepath = it.cycle(glob.glob(pattern))

        self.points = None
        self.scene = self.load_scene('cube.obj')
        self.vao_wrapper = self.scene.root_nodes[0].mesh.vao

        ds = Dataset()
        self.points, self.num_samples, self.dim = ds.load_point_data(next(self.filepath))

        self.init_dynamic_data()


    def init_dynamic_data(self):
        # Add a new buffer into the VAO wrapper in the scene.
        # This is simply a collection of named buffers that is auto mapped
        # to attributes in the vertex shader with the same name.
        self.instance_data = self.ctx.buffer(reserve=12 * self.num_samples, dynamic=True)

        self.vao_wrapper.buffer(self.instance_data, '3f/i', 'in_move')
        # Create the actual vao instance (auto mapping in action)
        self.vao = self.vao_wrapper.instance(self.prog)

    def render(self, t, frame_time):
        self.ctx.clear(.05, .02, 0.3)

        self.ctx.enable(moderngl.DEPTH_TEST | moderngl.BLEND)
        self.ctx.blend_func = moderngl.ADDITIVE_BLENDING
        #self.ctx.blend_func = moderngl.PREMULTIPLIED_ALPHA
        #self.ctx.blend_func = moderngl.DEFAULT_BLENDING
        self.ctx.blend_equation = moderngl.FUNC_ADD
        self.ctx.blend_equation = moderngl.MAX

        # step through frames or change continous fps: 
        # fps = inf  : step frame
        # fps = 0    : pause
        # fps = 1    : 1 fps
        # fps = 30   : 30 fps
        if self.cam.op['fps'] == np.inf:
            self.cam.op['fps'] = 0
            update_frame = True
        elif self.cam.op['fps'] != 0 and (time.time()-self.time['render:load']) > (1/self.cam.op['fps']): 
            update_frame = True
        else:
            update_frame = False

        if update_frame is True:
            try:
                filepath = next(self.filepath)
                print(filepath)
                self.points, self.num_samples, self.dim = Dataset().load_point_data(filepath)
                self.time['render:load'] = time.time()
            except:
                pass

        mvp = self.cam.update_pose(t)
        self.mvp.write(mvp.astype('f4').tobytes())
        self.light.value = (1.0, 1.0, 1.0)
        if self.points is not None:
            self.instance_data.clear()
            self.instance_data.write(self.points.astype('f4').tobytes())
            self.vao.render(instances=self.num_samples)

        self.time['render'] = time.time()
