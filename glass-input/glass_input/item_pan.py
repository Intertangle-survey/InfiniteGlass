from . import mode

class ItemPanMode(mode.Mode):
    def enter(self):
        mode.Mode.enter(self)
        if not self.window or self.window == self.display.root:
            mode.pop(self.display)
            mode.push_by_name(self.display, "pan", first_event=self.first_event, last_event=self.last_event)
            return True
        return True

    def pan(self, event, x=None, y=None):
        if x is None and y is None:
            self.x += event["XK_Right"] - event["XK_Left"]
            self.y += event["XK_Down"] - event["XK_Up"]
        else:
            self.x += x
            self.y += y

        space_orig = mode.view_to_space(self.orig_view, self.orig_size, 0, 0)
        space = mode.view_to_space(self.orig_view, self.orig_size, self.x, self.y)

        coords = list(self.orig_window_coords)
        coords[0] = self.orig_window_coords[0] + (space[0] - space_orig[0])
        coords[1] = self.orig_window_coords[1] + (space[1] - space_orig[1])

        self.window["IG_COORDS"] = coords

    def pan_mouse(self, event):
        space_orig = mode.view_to_space(self.orig_view, self.orig_size, self.first_event.root_x, self.first_event.root_y)
        space = mode.view_to_space(self.orig_view, self.orig_size, event.root_x, event.root_y)

        coords = list(self.orig_window_coords)
        coords[0] = self.orig_window_coords[0] + (space[0] - space_orig[0])
        coords[1] = self.orig_window_coords[1] + (space[1] - space_orig[1])

        self.window["IG_COORDS"] = coords
