from gi.repository import Gtk

class AboutDialog:
    """Dialog for showing overal information about this program"""

    def about_dialog(self, widget):
        about_dialog = Gtk.AboutDialog()

        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_name("About gtkPstree")
        about_dialog.set_program_name("gtkPstree")
        about_dialog.set_copyright("(c) 2015 Rocky Bernstein")
        about_dialog.set_version("1.0")
        about_dialog.set_comments("Real-time process tree animation")
        about_dialog.set_authors(["Rocky Bernstein"])
        about_dialog.set_website("http://github.com/rocky/pygtk3-pstree")

        about_dialog.run()
        about_dialog.destroy()
