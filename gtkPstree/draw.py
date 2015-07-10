"""Things related to drawing the process tree"""
from gi.repository import Pango, PangoCairo
from arrange import arrange


def do_draw(self, cr, get_data_fn):

    if not self.exposed:
        if self.debug: print("Not exposed")
        return
    if self.debug: print("exposed")

    self.levels, self.pid2node = get_data_fn(self)

    max_x, max_y, self.levels_x = arrange(self.levels, self.pid2node,
                                          self.width, debug=self.debug)
    old_x, old_y = self.area.get_size_request()
    if old_x != max_x or old_y != max_y:
        self.area.set_size_request(max_x, max_y)

    if len(self.levels) == 0: return

    # cr.translate (10, 10)
    layout = PangoCairo.create_layout(cr)
    desc = Pango.font_description_from_string(self.font)
    layout.set_font_description(desc)

    x_offset = 0

    text_mid = self.fontHeight >> 1

    widths = {}

    for i, level in enumerate(self.levels):
        for pid in level:

            node = self.pid2node[pid]

            try:
                vrank, rank, x_offset, y_offset = node.PosInfo
            except:
                from trepan.api import debug; debug()

            # Draw line from process to parent
            if i > 0:
                layout.set_text('', -1)
                ppid = node.PPid
                parent = self.pid2node[ppid]

                pp_vrank, pp_i, pp_x, pp_y = parent.PosInfo
                pp_x += widths[ppid] + self.line_gap

                cr.move_to(x_offset - self.line_gap, y_offset + text_mid)
                cr.line_to(pp_x + self.line_gap, pp_y + text_mid)
                cr.set_source_rgba(0.0, 0.0, 0.0, 0.5)
                cr.stroke()
                pass

            # print(node.Name, node.PosInfo, node.State)
            PangoCairo.show_layout(cr, layout)

            cr.move_to(x_offset, y_offset)
            layout.set_text(node.Name, -1)

            text_width, text_height = layout.get_pixel_size()
            widths[pid] = text_width

            # layout and set process name
            if node.State[0] == 'R':
                cr.set_source_rgba(0.0, 1.0, 0.0, 1.0)
            elif node.State[0] == 'T':
                cr.set_source_rgba(1.0, 0.0, 0.0, 1.0)
            else:
                cr.set_source_rgba(0.0, 0.0, 0.0)

            if self.debug:
                print("xy(%d,%d), pid(%ld): %s" %
                      (node.PosInfo[2], node.PosInfo[3], node.Pid, node.Name))

            PangoCairo.show_layout(cr, layout)

            pass

    return
