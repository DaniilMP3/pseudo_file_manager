import tkinter as tk
from tkinter import ttk
from file_manager.storage import Storage


class SButton(tk.Button):
    def __init__(self, master: tk.Widget, storable_type: str, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.storable_type = storable_type


class GUI:
    def __init__(self):
        self.storage = Storage()
        self.root = tk.Tk()

        self.root.geometry("600x400")

        # Configure scrollbar
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=1)

        self.canvas = tk.Canvas(self.main_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.scroll_bar = tk.Scrollbar(
            self.main_frame, orient=tk.VERTICAL, command=self.canvas.yview
        )
        self.scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scroll_bar.set)
        self.canvas.bind(
            "<Configure>",
            lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )
        self.canvas.bind(
            "<MouseWheel>",
            lambda e: self.canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"),
        )

        self.helper_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.helper_frame, anchor="nw")

        # Popup menu
        self.popup_menu = tk.Menu(self.root, tearoff=False)

        self.create_storable_menu = tk.Menu(self.root, tearoff=False)
        self.create_storable_menu.add_command(label='Directory')
        self.create_storable_menu.add_command(label='File')
        self.create_storable_menu.add_command(label='Document')

        self.sort_by_menu = tk.Menu(self.root, tearoff=False)
        self.sort_by_menu.add_command(label='Name')

        self.popup_menu.add_cascade(label='Create', menu=self.create_storable_menu)
        self.popup_menu.add_cascade(label='Sort by', menu=self.sort_by_menu)

        self.root.bind('<Button-3>', self.show_popup_menu)


        test_dir = SButton(self.helper_frame, 'directory', text='Directory1')
        test_dir.pack()

        del_button = tk.Button(
            self.helper_frame, text="Delete", command=lambda: test_dir.destroy()
        )
        del_button.pack()

        self.root.mainloop()

    def show_popup_menu(self, e):
        self.popup_menu.tk_popup(e.x_root, e.y_root)

    def create_storable(self):
        pass

    def on_click_storable(self):
        pass

    def _on_click_directory(self):
        pass

    def update_storables_in_frame(self):

        for storable in self.storage.current_dir_components:
            label = tk.Label(self.helper_frame, text=storable.get_name())
            label.pack()
