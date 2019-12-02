from pc3_gpu import PC3


class Viewer(PC3):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def key_event(self, key, action, modifiers):
        # Key presses
        if action == self.wnd.keys.ACTION_PRESS:
            if key == self.wnd.keys.SPACE:
                print("SPACE key was pressed")

            # Using modifiers (shift and ctrl)

            if key == self.wnd.keys.Z and modifiers.shift:
                print("Shift + Z was pressed")
                
            if key == self.wnd.keys.A:
                self.cam.axis_slide(['z'], [1])

            if key == self.wnd.keys.W:
                self.cam.axis_slide(['z'], [-1])

            if key == self.wnd.keys.I:
                print("cam_pos: " + str(self.cam.cam_pos))
                print("cam_tar: " + str(self.cam.cam_target))

            if key == self.wnd.keys.Z and modifiers.ctrl:
                print("ctrl + Z was pressed")

        # Key releases
        elif action == self.wnd.keys.ACTION_RELEASE:
            if key == self.wnd.keys.SPACE:
                print("SPACE key was released")
            if key == self.wnd.keys.A:
                self.cam.axis_slide(['z'], [0])

            if key == self.wnd.keys.W:
                self.cam.axis_slide(['z'], [0])

    def mouse_position_event(self, x, y):
        print("Mouse position:", x, y)

    def mouse_drag_event(self, x, y):
        print("Mouse drag:", x, y)

    def mouse_scroll_event(self, x_offset, y_offet):
        print("mouse_scroll_event", x_offset, y_offet)

    def mouse_press_event(self, x, y, button):
        print("Mouse button {} pressed at {}, {}".format(button, x, y))
        print("Mouse states:", dir(self.wnd))

    def mouse_release_event(self, x: int, y: int, button: int):
        print("Mouse button {} released at {}, {}".format(button, x, y))
        print("Mouse states:", dir(self.wnd))

def main():
    Viewer.run()

if __name__ == '__main__':
    main()