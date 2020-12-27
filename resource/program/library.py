import numpy as np
import os
import itertools as it
import time

from pyrr import Matrix44
import moderngl
import moderngl_window as mglw
from moderngl_window import geometry

class VertexProgram:
    def __init__(self):
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
        self.shader = {}
        self.shader['mvp'] = {}
        self.shader['mvp']['offset'] = vertex_shader

class FragmentProgram:

    def __init__(self):
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

        f_shader_illuminated='''
            #version 330

            uniform vec3 Light;

            in vec3 v_vert;
            in vec3 v_norm;

            out vec4 f_color;

            void main() {
                float lum = clamp(dot(normalize(Light - v_vert), normalize(v_norm)), 0.0, 1.0) * 0.7 + 0.3;
                f_color = vec4(lum, 1.0, lum, 1.0);
            }
        '''

        dark_to_bright ='''
            #version 330
            uniform vec3 Light;

            in vec3 v_vert;
            in vec3 v_norm;

            out vec4 f_color;
            float g = (v_vert.z+128)/255.0;

            void main() {
                float lum = clamp(dot(normalize(Light - v_vert), normalize(v_norm)), 0.0, 1.0);
                f_color = vec4(g, g, g, 1.0);
            }
        '''

        self.shader = {
            'modulated' : f_shader_modulated,
            'dark_to_bright' : dark_to_bright,
            'illuminated' : f_shader_illuminated,
            'mody' : f_shader_modulated_y,
            'firepit' : f_shader_firepit
        }
    