import InfiniteGlass
import Xlib.X
import Xlib.Xcursorfont
import Xlib.keysymdef.miscellany
import Xlib.ext.xinput
import os.path
import pkg_resources
import yaml
import json
import sys
from . import mode

def main2(*arg, **kw):
    mode.load_config()

    with InfiniteGlass.Display() as display:

        # extension_info = display.query_extension('XInputExtension')
        # xinput_major = extension_info.major_opcode
        version_info = display.xinput_query_version()
        print('Found XInput version %u.%u' % (
            version_info.major_version,
            version_info.minor_version,
        ))

        font = display.open_font('cursor')
        display.input_cursor = font.create_glyph_cursor(
            font, Xlib.Xcursorfont.box_spiral, Xlib.Xcursorfont.box_spiral + 1,
            (65535, 65535, 65535), (0, 0, 0))

        display.animate_window = -1
        @display.root.require("IG_ANIMATE")
        def animate_window(root, win):
            display.animate_window = win
            
        # Do not allow setting the input focus to None as that makes our keygrabs break...
        @display.root.on()
        def FocusIn(win, event):
            if event.detail == Xlib.X.NotifyDetailNone:
                display.root.set_input_focus(Xlib.X.RevertToNone, Xlib.X.CurrentTime)
            
        @display.root.on(mask="SubstructureNotifyMask", client_type="IG_INPUT_ACTION")
        def ClientMessage(win, event):
            win, atom = event.parse("WINDOW", "ATOM")
            action = json.loads(win[atom])
            InfiniteGlass.DEBUG("message", "RECEIVED INPUT ACTION %s" % (action,)); sys.stderr.flush()
            display.input_stack[-1].action(None, action, None)
            
        @display.eventhandlers.append
        def handle(event):
            if display.animate_window == -1:
                return False
            return mode.handle_event(display, event)

        mode.push_by_name(display, "base_mode")

        display.root.xinput_select_events([
            (Xlib.ext.xinput.AllDevices, Xlib.ext.xinput.RawMotionMask),
        ])

        InfiniteGlass.DEBUG("init", "Input handler started\n")

    
def main(*arg, **kw):
    print("XYZZYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", os.getcwd())
    import cProfile
    cProfile.runctx('main2()', globals(), locals(), "glass-input.prof")
