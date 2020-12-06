import numpy as np
import os
import itertools as it
import time

from pyrr import Matrix44
import moderngl
import moderngl_window as mglw
from moderngl_window import geometry


class ProgramAssembler:
    def __init__(self, ctx, loader):
        self.ctx = ctx
        self.load_program(loader)
        self.set_program_inputs()
        self.create_vertex_data()

    def load_program(self, loader):
        self.loader = loader
        self.prog = self.ctx.program(
            vertex_shader=self.load_vertex_shader(),
            fragment_shader=self.load_fragment_shader("mody"),
        )

    def set_program_inputs(self):
        # buffer format needed by shader and used to create vbo
        self.vertex_buffer_format = '3f/i'
        self.vertex_buffer_name = 'in_move'

        # uniform names
        self.mvp = self.prog['Mvp']
        self.light = self.prog['Light']
  
    def create_vertex_data(self):
        self.scene = self.loader.load_scene('cube.obj')
        self.vao = self.scene.root_nodes[0].mesh.vao

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

    
class Effect:
    def __init__(self, assembley, max_samples=320*240):
        self.name = "pointcloud"
        self.program_assembley = assembley
        self.max_samples = max_samples

    def init(self):
        self.vao_wrapper = self.program_assembley.vao
        self.init_dynamic_data()

    def init_dynamic_data(self):
        assembley = self.program_assembley

        # Add a new buffer into the VAO wrapper in the scene.
        # This is simply a collection of named buffers that is auto mapped
        # to attributes in the vertex shader with the same name.
        self.vbo = assembley.ctx.buffer(reserve=12 * self.max_samples, dynamic=True)

        self.vao_wrapper.buffer(self.vbo, assembley.vertex_buffer_format, assembley.vertex_buffer_name)
        # Create the actual vao instance (auto mapping in action)
        self.vao = self.vao_wrapper.instance(assembley.prog)

    def render(self, mvp_matrix, data=None, max_count=None):
        """Render with updated data, and transforming eye space to clip with MVP
           
           input:
               mvp : model view projection matrix (from model/world to clip)
               data : 3d point data with [0, N, 3] shape

        """
        self.program_assembley.mvp.write(mvp_matrix.astype('f4').tobytes())
        self.program_assembley.light.value = (1.0, 1.0, 1.0)

        points = data
        if points is not None:
            if max_count is None:
                max_count = len(points[0])
            self.vbo.clear()
            self.vbo.write(points.astype('f4').tobytes())
            self.vao.render(instances=max_count)





