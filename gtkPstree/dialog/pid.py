from gi.repository import Gtk, Pango
import subprocess


class PidDialog:
    """Dialog for showing PID information when a process is clicked on"""

    DEFAULT_PS_CMD = ['ps', '-o', 'pcpu,wchan,pri,args', '-w', '-p']

    def __init__(self, ps_cmd=DEFAULT_PS_CMD):
        # ps comamnds and args without the final pid
        self.ps_cmd = ps_cmd
        self.font = 'Courier 10'
        self.font_desc = Pango.font_description_from_string(self.font)

    def pid_dialog(self, pid, pidinfo):
        dialog = Gtk.MessageDialog()
        dialog.modify_font(self.font_desc)
        try:
            output = subprocess.check_output(self.ps_cmd + [str(pid)])
            dialog.format_secondary_text(output)
        except:
            pass
        msg = ("<b>Process %d (from cached info)</b>\n" +
               "PPid RealUid # kids Depth State Name\n" +
               "%4d %7d %6d %5d %s %s") % (pid, pidinfo.PPid, pidinfo.RealUid,
                                          len(pidinfo.Children),
                                          pidinfo.Depth,
                                          pidinfo.State, pidinfo.Name)
        dialog.set_markup(msg)
        dialog.run()
        dialog.destroy()
