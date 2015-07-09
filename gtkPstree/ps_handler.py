from gi.repository import Gtk, Gdk, Pango

# Our modules
from dialog.about import AboutDialog
from dialog.pid import PidDialog

class Handler:
    def __init__(self, pstree):
        self.pstree = pstree
        self.aboutDialog = AboutDialog()
        self.show_about_dialog = self.aboutDialog.about_dialog
        self.pidDialog = PidDialog()
        self.show_pid_dialog = self.pidDialog.pid_dialog

    def onDeleteWindow(self, *args):
        self.pstree.timer.stop()
        Gtk.main_quit(*args)

    def onMotionNotify(self, widget, event):
        if event.is_hint:
            self.pstree.area.x = int(event.x)
            self.pstree.area.y = int(event.y)

    def onButtonPressed(self, widget, *args):
        print("Location: (%d, %d)" % (self.pstree.area.x, self.pstree.area.y))
        self.pstree.locate_pid()

    def onKeyPressed(self, widget, event):
        try:
            print("Key Press!", widget, chr(event.keyval))
            if chr(event.keyval).upper() == 'Q':
                self.onExitActivate(self)
        except:
            pass

    def onWindowState(self, widget, event):
        # print("{:016b}".format(event.new_window_state))
        if event.new_window_state & Gdk.EventMask.EXPOSURE_MASK:
            self.pstree.exposed = False
        else:
            self.pstree.exposed = True

    def onExitActivate(self, *args):
        self.pstree.timer.stop()
        Gtk.main_quit()

    def onResize(self, scroll, cr):
        width = scroll.get_allocated_width()
        # height = scroll.get_allocated_height()
        # scroll.set_size_request(width, height)
        self.pstree.width = width
        # print("Resize:", scroll, cr, width, height)
        # self.pstree.area = self.pstree.builder.get_object('canvas')
        # self.pstree.area.modify_bg(Gtk.StateType.NORMAL, pstree.bg)
