"""
PC Viewer

Usage:
------
Mouse: 
    Drag with left button to rotate around pivot (thick small axes), 
    with right button to translate and the wheel to zoom.

Keyboard: 
    [p]     Pause
    [r]     Reset View
    [z]     Toggle point scaling
    [c]     Toggle color source
    [s]     Save PNG (./out.png)
    [e]     Export points to ply (./out.ply)
    [q\ESC] Quit
"""

import math
import time
import cv2
import numpy as np
import collections


Intrinsics = collections.namedtuple('Intrinsics', 'width height ppx ppy fx fy model coeffs')

class AppState:

    def __init__(self, *args, **kwargs):
        self.WIN_NAME = 'Debug'
        self.pitch, self.yaw = math.radians(-10), math.radians(-15)
        self.translation = np.array([0, 0, -1], dtype=np.float32)
        self.distance = 2
        self.prev_mouse = 0, 0
        self.mouse_btns = [False, False, False]
        self.window_size = (1,1)
        self.paused = False
        self.color = False 
        self.intrinsics = {}

    def reset(self):
        self.pitch, self.yaw, self.distance = 0, 0, 2
        self.translation[:] = 0, 0, -1

    @property
    def rotation(self):
        Rx, _ = cv2.Rodrigues((self.pitch, 0, 0))
        Ry, _ = cv2.Rodrigues((0, self.yaw, 0))
        return np.dot(Ry, Rx).astype(np.float32)

    @property
    def pivot(self):
        return self.translation + np.array((0, 0, self.distance), dtype=np.float32)


class Device:

    def __init__(self):
        import pyrealsense2 as rs
        self.rs = rs
        pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        pipeline.start(config)
        profile = pipeline.get_active_profile()
        depth_profile = rs.video_stream_profile(profile.get_stream(rs.stream.depth))
        depth_intrinsics = depth_profile.get_intrinsics()
        w, h = depth_intrinsics.width, depth_intrinsics.height

        # Processing blocks
        pc = rs.pointcloud()
        colorizer = rs.colorizer()

        self.pipeline = pipeline
        self.intrinsics = {'depth' : depth_intrinsics}
        self.colorizer = colorizer
        self.pc = pc
    
    def depth_size(self):
        w = self.intrinsics['depth'].width
        h = self.intrinsics['depth'].height
        return (w, h)

    def export(self, path):
        pass 

    def deproject(self, u, v, depth):
        """Deprojection takes a 2D pixel location on a stream's images, as well as a depth, 
           specified in meters, and maps it to a 3D point location
        """
        intrinsics = self.intrinsics['depth']
        p = self.rs.rs2_deproject_pixel_to_point(intrinsics, [u, v], depth)
        return p
        
    def stop(self):
        self.pipeline.stop()

    def get_pc_array(self, color=False): 
        """Read vertex, tc, and texture arrays."""

        verts = np.array([])
        texcoords = np.array([])
        if self.pipeline is not None:
            frames = self.pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()

            depth_intrinsics = self.rs.video_stream_profile(
                depth_frame.profile).get_intrinsics()

            w, h = depth_intrinsics.width, depth_intrinsics.height
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())
            depth_colormap = np.asanyarray(
                self.colorizer.colorize(depth_frame).get_data())
            if color:
                mapped_frame, color_source = color_frame, color_image
            else:
                mapped_frame, color_source = depth_frame, depth_colormap

            points = self.pc.calculate(depth_frame)
            self.pc.map_to(mapped_frame)

            # Pointcloud data to arrays
            v, t = points.get_vertices(), points.get_texture_coordinates()
            verts = np.asanyarray(v).view(np.float32).reshape(-1, 3)  # xyz
            texcoords = np.asanyarray(t).view(np.float32).reshape(-1, 2)  # uv
        return verts, texcoords, color_source

class DeviceSw:
    def __init__(self):
        """
        intrinsics: width: 640, height: 480, 
        ppx: 318.997, ppy: 238.437, fx: 380.299, fy: 380.299, 
        model: Brown Conrady, coeffs: [0, 0, 0, 0, 0]
        image plane size:  (640, 480)
        """
        depth_intrinsics = Intrinsics(width=640, height=480, ppx=318.9, ppy=238.4, fx=380.2, fy=380.2, model='None', coeffs=[0, 0, 0, 0, 0])
        self.intrinsics = {'depth' :  depth_intrinsics}

    def depth_size(self):
        w = self.intrinsics['depth'].width
        h = self.intrinsics['depth'].height
        return (w, h)

    def export(self, path):
        pass

    def deproject(self, u, v, depth):
        """Deprojection takes a 2D pixel location on a stream's images, as well as a depth, 
           specified in meters, and maps it to a 3D point location
        """
        p = (depth*u/380.0, depth*v/380.0, depth) 
        return p

    def stop(self):
        pass

    def get_pc_array(self, color=False):
        """
        v:  (76800, 3)
        t:  (76800, 2)
        r:  (240, 320, 3)

        v :x,y,z in meters z positive:
        [[-0.7571616  -0.8843999   1.447     ]
        [-0.7495518  -0.8843999   1.447     ]

        t : tex coords u, v in [0.0, 1.0] range:  
        [[0.12499998 0.0125    ]
        [0.128125   0.0125    ]

        rgb 8-bit channels
        """
        w, h = self.depth_size()

        sz = h*w
        # v [num, 3]: x and y in [-2.5 to 2.5] range, z in [0.0, 5.0]
        v = np.random.random((sz, 3))*2.5
        v[:,2] += 2.5

        # tex u, v coords [num, 2]: u,v in [0.0 to 1.0] range
        t = (np.random.random((sz, 2)) + 1.0) / 2.0       

        # texture is 8-bit channels rgb image: [h, w, 3]
        if color:
            rgb = np.random.randint(0, 255, (sz, 3), dtype=np.uint8)
        else:
            rgb = np.ones((h, w, 3), np.uint8)*255
        return v, t, rgb



state = AppState()

def mouse_cb(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:
        state.mouse_btns[0] = True

    if event == cv2.EVENT_LBUTTONUP:
        state.mouse_btns[0] = False

    if event == cv2.EVENT_RBUTTONDOWN:
        state.mouse_btns[1] = True

    if event == cv2.EVENT_RBUTTONUP:
        state.mouse_btns[1] = False

    if event == cv2.EVENT_MBUTTONDOWN:
        state.mouse_btns[2] = True

    if event == cv2.EVENT_MBUTTONUP:
        state.mouse_btns[2] = False

    if event == cv2.EVENT_MOUSEMOVE:

        w, h = state.window_size #out.shape[:2]
        dx, dy = x - state.prev_mouse[0], y - state.prev_mouse[1]

        if state.mouse_btns[0]:
            state.yaw += float(dx) / w * 2
            state.pitch -= float(dy) / h * 2

        elif state.mouse_btns[1]:
            dp = np.array((dx / w, dy / h, 0), dtype=np.float32)
            state.translation -= np.dot(state.rotation, dp)

        elif state.mouse_btns[2]:
            dz = math.sqrt(dx**2 + dy**2) * math.copysign(0.01, -dy)
            state.translation[2] += dz
            state.distance -= dz

    if event == cv2.EVENT_MOUSEWHEEL:
        dz = math.copysign(0.1, flags)
        state.translation[2] += dz
        state.distance -= dz

    state.prev_mouse = (x, y)



def project(out, v):
    """project 3d vector array to 2d"""
    h, w = out.shape[:2]
    view_aspect = float(h)/w

    # ignore divide by zero for invalid depth
    with np.errstate(divide='ignore', invalid='ignore'):
        proj = v[:, :-1] / v[:, -1, np.newaxis] * \
            (w*view_aspect, h) + (w/2.0, h/2.0)

    # near clipping
    znear = 0.03
    proj[v[:, 2] < znear] = np.nan
    return proj


def view(v):
    """apply view transformation on vector array"""
    return np.dot(v - state.pivot, state.rotation) + state.pivot - state.translation


def line3d(out, pt1, pt2, color=(0x80, 0x80, 0x80), thickness=1):
    """draw a 3d line from pt1 to pt2"""
    p0 = project(out, pt1.reshape(-1, 3))[0]
    p1 = project(out, pt2.reshape(-1, 3))[0]
    if np.isnan(p0).any() or np.isnan(p1).any():
        return
    p0 = tuple(p0.astype(int))
    p1 = tuple(p1.astype(int))
    rect = (0, 0, out.shape[1], out.shape[0])
    inside, p0, p1 = cv2.clipLine(rect, p0, p1)
    if inside:
        cv2.line(out, p0, p1, color, thickness, cv2.LINE_AA)


def grid(out, pos, rotation=np.eye(3), size=1, n=10, color=(0x80, 0x80, 0x80)):
    """draw a grid on xz plane"""
    pos = np.array(pos)
    s = size / float(n)
    s2 = 0.5 * size
    for i in range(0, n+1):
        x = -s2 + i*s
        line3d(out, view(pos + np.dot((x, 0, -s2), rotation)),
               view(pos + np.dot((x, 0, s2), rotation)), color)
    for i in range(0, n+1):
        z = -s2 + i*s
        line3d(out, view(pos + np.dot((-s2, 0, z), rotation)),
               view(pos + np.dot((s2, 0, z), rotation)), color)


def axes(out, pos, rotation=np.eye(3), size=0.075, thickness=2):
    """draw 3d axes"""
    line3d(out, pos, pos +
           np.dot((0, 0, size), rotation), (0xff, 0, 0), thickness)
    line3d(out, pos, pos +
           np.dot((0, size, 0), rotation), (0, 0xff, 0), thickness)
    line3d(out, pos, pos +
           np.dot((size, 0, 0), rotation), (0, 0, 0xff), thickness)


def frustum(out, dev, color=(0x40, 0x40, 0x40)):
    """draw camera's frustum"""
    orig = view([0, 0, 0])
    intrinsics = dev.intrinsics['depth']
    w, h = intrinsics.width, intrinsics.height

    for d in range(1, 6, 2):
        def get_point(x, y):
            p = dev.deproject(x, y, d)
            line3d(out, orig, view(p), color)
            return p

        top_left = get_point(0, 0)
        top_right = get_point(w, 0)
        bottom_right = get_point(w, h)
        bottom_left = get_point(0, h)

        line3d(out, view(top_left), view(top_right), color)
        line3d(out, view(top_right), view(bottom_right), color)
        line3d(out, view(bottom_right), view(bottom_left), color)
        line3d(out, view(bottom_left), view(top_left), color)


def pointcloud(out, verts, texcoords, color, painter=True):
    """draw point cloud with optional painter's algorithm"""
    if painter:
        # Painter's algo, sort points from back to front

        # get reverse sorted indices by z (in view-space)
        # https://gist.github.com/stevenvo/e3dad127598842459b68
        v = view(verts)
        s = v[:, 2].argsort()[::-1]
        proj = project(out, v[s])
    else:
        proj = project(out, view(verts))

    h, w = out.shape[:2]

    # proj now contains 2d image coordinates
    j, i = proj.astype(np.uint32).T

    # create a mask to ignore out-of-bound indices
    im = (i >= 0) & (i < h)
    jm = (j >= 0) & (j < w)
    m = im & jm

    cw, ch = color.shape[:2][::-1]
    if painter:
        # sort texcoord with same indices as above
        # texcoords are [0..1] and relative to top-left pixel corner,
        # multiply by size and add 0.5 to center
        v, u = (texcoords[s] * (cw, ch) + 0.5).astype(np.uint32).T
    else:
        v, u = (texcoords * (cw, ch) + 0.5).astype(np.uint32).T
    # clip texcoords to image
    np.clip(u, 0, ch-1, out=u)
    np.clip(v, 0, cw-1, out=v)

    # perform uv-mapping
    out[i[m], j[m]] = color[u[m], v[m]]


class Viewer:
    def __init__(self, dev):
        self.dev = dev 
        state.window_size = self.dev.depth_size()
        w, h = state.window_size
        cv2.namedWindow(state.WIN_NAME, cv2.WINDOW_AUTOSIZE)
        cv2.resizeWindow(state.WIN_NAME, w, h)
        cv2.setMouseCallback(state.WIN_NAME, mouse_cb)

    def update_frame(self, out):
        verts, texcoords, color_source = self.dev.get_pc_array()
        out.fill(0)
        grid(out, (0, 0.5, 1), size=1, n=10)
        frustum(out, self.dev)
        axes(out, view([0, 0, 0]), state.rotation, size=0.1, thickness=1)
        pointcloud(out, verts, texcoords, color_source)
        if any(state.mouse_btns):
            axes(out, view(state.pivot), state.rotation, thickness=4)

    def update_frame_with_ui(self, out):
            now = time.time()
            self.update_frame(out)
            dt = time.time() - now

            cv2.setWindowTitle(
                state.WIN_NAME, "Debug %dFPS (%.2fms) %s" %
                (1.0/dt, dt*1000, "PAUSED" if state.paused else ""))
            cv2.imshow(state.WIN_NAME, out)

    def run(self):
        h, w = self.dev.depth_size()
        out = np.empty((h, w, 3), dtype=np.uint8)
        while True:
            self.update_frame_with_ui(out)

            key = cv2.waitKey(30)
            if key == ord("r"):
                state.reset()
            if key == ord("p"):
                state.paused ^= True
            if key == ord("c"):
                state.color ^= True
            if key == ord("s"):
                cv2.imwrite('./out.png', out)
            if key == ord("e"):
                self.dev.export('./out.ply')
            if key in (27, ord("q")) or cv2.getWindowProperty(state.WIN_NAME, cv2.WND_PROP_AUTOSIZE) < 0:
                self.dev.stop()
                break

    def stop(self):
        self.dev.stop()


if __name__=="__main__":
    camera = DeviceSw()
    v = Viewer(camera)
    v.run()
    try:
        v.stop()
    except:
        print('cannot stop camera, maybe already stopped.')


