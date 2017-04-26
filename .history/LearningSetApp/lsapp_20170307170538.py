# -*- coding: utf-8 -*-
""" TODO PLACEHOLDER module docstring """

# amit tennie kell: egy ablak egy textbox-szal és egy legördülő listával.
# a textboxba-másoljuk az elem forráskódját, a listából kiválasztjuk az
# osztályt. A program elmenti egy YAML fájlba min a kettőt.

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class DLMWindow(Gtk.Window):
    """Class to implement the GUI of the SheetPy application"""

    def create_addbox(self):
        # Creating the search Dialog Box
        self.add_dialog = Gtk.Dialog(title="Add task", parent=self, flags=0)
        self.add_button = Gtk.Button("Add")
        self.add_dialog.action_area.pack_start(self.search_button, True,
                                               True, 0)
        self.search_dialog.add(self.add_button)

        # self.temakor = Gtk.Entry()
        # self.prioritas = Gtk.Entry()
        # self.leiras = Gtk.Entry()
        # self.felelosok = Gtk.Entry()
        # self.hatarido = Gtk.Entry()
        # self.megjegyzes = Gtk.Entry()
        # self.hatarido = Gtk.Entry()
        # self.ellenorizni = Gtk.Entry()
        # self.nyomtatas = Gtk.Entry()

        self.addbox_buttons = []
        i = 0
        for name in enumerate(["Témakör", "Pri.", "Feladat leírása",
                                          "Felelős(ök)", "Határidő",
                                          "Megjegyzés", "Státusz",
                                          "Ellenőrizni", "Nyomtatás"]):
            self.addbox_buttons.append(Gtk.Entry())
            self.addbox_buttons[i].set_text(str(name))
            self.add_dialog.action_area.pack_start(self.addbox_buttons[i],
                                                   True, True, 0)

        self.add_button.connect("clicked", self.add_task)

    def __init__(self):
        """intializes the GUI elements and the thread"""

        Gtk.Window.__init__(self, title="Hello World")
        self.set_border_width(10)
        self.set_default_size(900, 500)

        self.handler = SheetPy.sheet_handler()

        gthread = threading.Thread(target=self.run_pythread, args=(self))
        gthread.start()

        self.create_searchbox()
        self.create_addbox()

        # Creating the ListStore model
        self.tasklist = Gtk.ListStore(str, str, str, str,
                                      str, str, str, str, str)
        self.current_filter = None

        # Creating the filter, feeding it with the tasklist model
        self.filter = self.tasklist.filter_new()

        # setting the filter function, note that we're not using the
        self.filter.set_visible_func(self.filter_func)

        # creating the treeview, making it use the filter
        # as a model, and adding the columns
        self.treeview = Gtk.TreeView.new_with_model(self.filter)

        for i, column_title in enumerate(["Témakör", "Pri.", "Feladat leírása",
                                          "Felelős(ök)", "Határidő",
                                          "Megjegyzés", "Státusz",
                                          "Ellenőrizni", "Nyomtatás"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            column.set_resizable(True)
            if i == 2 or i == 5:
                column.set_fixed_width(300)
            self.treeview.append_column(column)
            scroll.connect_after('size-allocate', resize_wrap, treeview,
                                 column, render)

        # Setting up the self.grid in which the elements are to be positionned
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(False)
        self.add(self.grid)

        self.buttons = list()
        for rule in ["Refresh Spreadsheet", "Find own tasks",
                     "List all", "Search", "Delete", "Add task"]:
            button = Gtk.Button(rule)

            self.buttons.append(button)
            if rule == "Find own tasks":
                button.connect("clicked", self.on_own_clicked)
            elif rule == "List all":
                button.connect("clicked", self.on_all_clicked)
            elif rule == "Refresh Spreadsheet":
                button.connect("clicked", self.on_refresh_clicked)
            elif rule == "Search":
                button.connect("clicked", self.on_search_clicked)
            elif rule == "Delete":
                button.connect("clicked", self.on_delete_clicked)
            elif rule == "Add task":
                button.connect("clicked", self.on_add_clicked)

        # setting up the layout, putting the treeview in a scrollwindow,
        # and the buttons in a row
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 0, 8, 10)
        self.grid.attach_next_to(self.buttons[0], self.scrollable_treelist,
                                 Gtk.PositionType.BOTTOM, 1, 1)
        for i, button in enumerate(self.buttons[1:]):
            self.grid.attach_next_to(button, self.buttons[i],
                                     Gtk.PositionType.RIGHT, 1, 1)

        self.scrollable_treelist.add(self.treeview)

        self.show_all()
        if gthread.isAlive():
            gthread.join()
        for line in self.handler.tasks:
            self.tasklist.append(line)
