#!/usr/bin/env python
from gi.repository import Gtk, Gdk
from bisect import bisect_left

# Stuff from this package
from opsys.loadavg import ReadLoadAvg
from ps_timer import TimerClass
from ps_handler import Handler
from draw import do_draw


def bisect_pids(pids, pid2node, y):
    """Return the index where to y offset *y* is in pid list *pids*,
    assuming pids are sorted by y offset.  The return value *i* is
    such that all *pid* in pids[:i] have pid2node[pid].PosInfo[-1] <
    *y*, and all *pid* in pids[i:] have pid2node[pid].PosInfo[-1] >=
    *y*.  So if *y* already appears in the list, i points just before
    the leftmost *y* already there.
    """
    lo, hi = 0, len(pids)
    while lo < hi:
        mid = (lo+hi) >> 1
        if pid2node[pids[mid]].PosInfo[-1] < y: lo = mid+1
        else: hi = mid
    return lo


class PSTreeWindow:

    def __init__(self, delay_in_secs=1, bg='#DA7', font='Sans 10'):
        self.debug = False
        self.delay_in_secs = delay_in_secs
        self.handler = Handler(self)
        self.builder = Gtk.Builder()
        self.builder.add_from_file("gnopstree.glade")
        self.builder.connect_signals(self.handler)

        # Levels contains a list of list of pids.  The top-level list
        # are pids at a given depth, 0, being root-level pids within a
        # level, pids are arranged as they are to appear left to
        # right. (We draw our tree with roots on the left and children
        # on the extreme right.
        self.levels = []

        self.bg = Gdk.color_parse(bg)
        self.font = font
        self.inter_level_space = 20

        self.init_canvas_area()

        self.window = self.builder.get_object("pstree top")
        self.status_bar = self.builder.get_object("statusBar")

        self.exposed = True
        self.update_status()
        self.window.show_all()
        self.timer = TimerClass(self.update_status, delay_in_secs)
        self.timer.start()
        return

    def init_canvas_area(self):
        self.width = 400
        self.scroll = self.builder.get_object('scolledwindow')
        self.scroll.set_size_request(self.width, 400)

        self.area = self.builder.get_object('canvas')
        self.area.modify_bg(Gtk.StateType.NORMAL, self.bg)
        self.area.set_events(Gdk.EventMask.BUTTON_PRESS_MASK
                             | Gdk.EventMask.KEY_PRESS_MASK
                             | Gdk.EventMask.POINTER_MOTION_HINT_MASK
                             | Gdk.EventMask.POINTER_MOTION_MASK
                             )
        self.fontHeight = 17
        self.area.connect("draw", self.draw_cb)

        # The number of pixels between a before a node name and the
        # line connecting it to its parent line, and after its parent
        # name.
        self.line_gap = 4

    def draw_cb(self, widget, cr):
        do_draw(self, cr)

    def locate_pid(self):
        level = bisect_left(self.levels_x, self.area.x) - 1
        print("Level found is %d" % level)
        if level >= len(self.levels) or level < 0: return None
        ary = self.levels[level]
        y = bisect_pids(ary, self.pid2node, self.area.y)-1
        if y >= len(ary) or len(ary) == 0: return None
        if y < 0: y = 0
        pid = ary[y]
        print("found y: %d, pid (%d) %s" % (y, pid, self.pid2node[pid]))
        self.handler.show_pid_dialog(pid, self.pid2node[pid])

    def update_status(self):
        l = ReadLoadAvg('/proc/loadavg')
        msg = (("%d processes, %d running."
                " LoadAvg: %g, %g, %g")
               % (l.ProcessTotal,
                  l.ProcessRunning,
                  l.Last1Min, l.Last5Min, l.Last15Min))
        self.status_bar.set_label(msg)
        # print(l)

if __name__ == '__main__':
    pstree = PSTreeWindow(2)
    Gtk.main()
