# -*- coding: utf-8 -*-
""" TODO PLACEHOLDER module docstring """

# amit tennie kell: egy ablak egy textbox-szal és egy legördülő listával.
# a textboxba-másoljuk az elem forráskódját, a listából kiválasztjuk az
# osztályt. A program elmenti egy YAML fájlba min a kettőt.
import re
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Element():
    """
    represents the elements of the page abtracized to be used by the crawler 
    Fields:
    HTMLtag: the type of the element, eg. <a>, <div>, etc.
    HTMLclasses[]: a vector of classnames assocated with the element
    CrawlerClass: the class of the element, determined by the user
    """
    def __init__(self, _HTMLtag, _HTMLClasses, _CrawlerClass):
        self.HTMLtag = _HTMLtag
        self.TMLClasses = _HTMLClasses

class DLMWindow(Gtk.Window):
    """Class to implement the GUI of the SheetPy application"""

    def create_searchbox(self):
        """ Creating the search Dialog Box """
        self.search_dialog.action_area.pack_start(self.search_button, True,
                                                  True, 0)
        self.search_dialog.add(self.search_button)
        self.search_dialog.action_area.pack_start(self.entry, True, True, 0)
        self.search_button.connect("clicked", self.search)

    def create_addbox(self):
        """ Creating the search Dialog Box """
        self.addbox_buttons = []
        i = 0
        for name in enumerate(["DOM element", "HTML classes", "AI classes"]):
            self.addbox_buttons.append(Gtk.Entry())
            self.addbox_buttons[i].set_text(str(name))

        self.add_button.connect("clicked", self.add_element)

    def __init__(self):
        """intializes the GUI elements and the thread"""

        Gtk.Window.__init__(self, title="Learning Set Manager")
        self.set_border_width(10)
        self.set_default_size(900, 500)

        # Searchbox elements
        self.search_dialog = Gtk.Dialog(title="Search", parent=self, flags=0)
        self.search_button = Gtk.Button("Search")
        self.entry = Gtk.Entry()

        # Addbox elements
        self.add_dialog = Gtk.Dialog(title="Add task", parent=self, flags=0)
        self.add_button = Gtk.Button("Add")

        self.create_addbox()

        # Creating the ListStore model
        self.tasklist = Gtk.ListStore(str, str, str)
        self.current_filter = None

        # Creating the filter, feeding it with the tasklist model
        self.filter = self.tasklist.filter_new()

        # setting the filter function, note that we're not using the
        self.filter.set_visible_func(self.filter_func)

        # creating the treeview, making it use the filter
        # as a model, and adding the columns
        self.treeview = Gtk.TreeView.new_with_model(self.filter)

        for i, column_title in enumerate(["HTML tag", "HTML Classes", "Crawler Class"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            column.set_resizable(True)
            if i == 2 or i == 5:
                column.set_fixed_width(300)
            self.treeview.append_column(column)
            # scroll.connect_after('size-allocate', resize_wrap, treeview,
            #                     column, render)

        # Setting up the self.grid in which the elements are to be positionned
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(False)
        self.add(self.grid)

        self.buttons = list()
        for rule in ["List all", "Search",
                     "Delete", "Add element"]:
            button = Gtk.Button(rule)

            self.buttons.append(button)
            if rule == "List all":
                button.connect("clicked", self.on_all_clicked)
            elif rule == "Search":
                button.connect("clicked", self.on_search_clicked)
            elif rule == "Delete":
                button.connect("clicked", self.on_delete_clicked)
            elif rule == "Add element":
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

    def search(self, widget):
        """ intialize a filter method """
        param = self.entry.get_text()
        param_re = re.compile(param)
        print(param)
        self.current_filter = param_re
        self.filter.refilter()

    def on_delete_clicked(self, widget):
        """ starts a deletion method """
        pass

    def on_all_clicked(self, widget):
        """starts a pysheet function to list all rows of the sheet"""
        self.current_filter = None
        self.filter.refilter()

    def on_add_clicked(self, widget):
        """ opens Addbox dialog """
        self.add_dialog.show_all()

    def on_search_clicked(self, widget):
        """ opens Searchbox dialog """
        pass

    def add_element(self):
        """adds a HTML tag - HTML class - AI class trio to the list"""
        values = []
        values_re = []
        i = 0
        for entry in self.addbox_buttons:
            values.append(entry.get_text())
            values_re.append(re.compile(values[i]))

    def filter_func(self, model, iter, data):
        """Tests if the element in the row matches the filter"""
        if self.current_filter is None or self.current_filter == "None":
            return True
        else:
            return self.current_filter.search(model[iter][3])

PW = DLMWindow()
PW.connect("delete-event", Gtk.main_quit)
PW.show_all()
Gtk.main()
