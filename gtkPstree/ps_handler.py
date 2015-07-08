from gi.repository import Gtk, Pango
import subprocess
class Handler:
    def __init__(self, pstree):
        self.pstree = pstree
        self.font = 'Courier 10'
        self.font_desc = Pango.font_description_from_string(self.font)

    def onDeleteWindow(self, *args):
        self.pstree.timer.stop()
        Gtk.main_quit(*args)

    def onButtonPressed(self, *args):
        print("Button Press!", args)

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

    def onHideEvent(self, *args):
        print("Hide called!", args)

    def onExitActivate(self, *args):
        self.pstree.timer.stop()
        Gtk.main_quit()

    def onResize(self, scroll, cr):
        width = scroll.get_allocated_width()
        height = scroll.get_allocated_height()
        # scroll.set_size_request(width, height)
        self.pstree.width = width
        # print("Resize:", scroll, cr, width, height)
        # self.pstree.area = self.pstree.builder.get_object('canvas')
        # self.pstree.area.modify_bg(Gtk.StateType.NORMAL, pstree.bg)


    def show_about_dialog(self, widget):
        about_dialog = Gtk.AboutDialog()

        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_name("About gtkPstree")
        about_dialog.set_program_name("gtkPstree")
        about_dialog.set_copyright("(c) 2015 Rocky Bernstein")
        about_dialog.set_version("1.0")
        about_dialog.set_comments("Real-time process tree animation")
        about_dialog.set_authors(["Rocky Bernstein"])
        about_dialog.set_website("http://github.com/rocky/python-gtkPstree")

        about_dialog.run()
        about_dialog.destroy()

    def show_pid_dialog(self, pid, pidinfo):
        dialog = Gtk.MessageDialog()
        dialog.modify_font(self.font_desc)
        try:
            output = subprocess.check_output(['ps', '-o', 'args,cpu,wchan,pri', '-p',
                                              str(pid)])
            dialog.format_secondary_text(output)
        except:
            pass
        msg = ("<b>Process %d (from cached info)</b>\n" +
               "PPid RealUid # kids Depth State Name\n" +
               "%4d %7d %6d %5d %s %s") % (pid, pidinfo.PPid, pidinfo.RealUid,
                                          len(pidinfo.Children), pidinfo.Depth,
                                          pidinfo.State, pidinfo.Name)
        dialog.set_markup(msg)
        dialog.run()
        dialog.destroy()
