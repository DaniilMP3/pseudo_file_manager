import tkinter as tk
from tkinter import messagebox
from file_manager.storage import Storage
from file_manager.exceptions import StorableNameAlreadyExists
from file_manager.data_types.storable import (
    Directory,
    StorableComponent,
)
from file_manager.storable_factory import StorableFactory


class SButton(tk.Button):
    def __init__(
        self,
        master: tk.Widget,
        storable_type: str,
        storable_instance: StorableComponent,
        *args,
        **kwargs,
    ):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.storable_type = storable_type
        self.storable_instance = storable_instance


class GUI:
    def __init__(self):
        self.storage = Storage()
        self.storable_factory = StorableFactory()
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
        self.create_storable_menu.add_command(
            label="Directory",
            command=lambda: self.show_storable_name_popup_menu("directory"),
        )
        self.create_storable_menu.add_command(
            label="File", command=lambda: self.show_storable_name_popup_menu("file")
        )
        self.create_storable_menu.add_command(
            label="Document",
            command=lambda: self.show_storable_name_popup_menu("document"),
        )

        self.sort_by_menu = tk.Menu(self.root, tearoff=False)
        self.sort_by_menu.add_command(label="Name")

        self.popup_menu.add_cascade(label="Create", menu=self.create_storable_menu)
        self.popup_menu.add_cascade(label="Sort by", menu=self.sort_by_menu)

        self.popup_storable_name_window = None

        self.root.bind("<Button-3>", self.show_popup_menu)

        test_dir = SButton(
            self.helper_frame, "directory", Directory("test_dir"), text="test_dir"
        )
        test_dir.pack()

        del_button = tk.Button(
            self.helper_frame, text="Delete", command=test_dir.destroy
        )
        del_button.pack()

        self.root.mainloop()

    def show_popup_menu(self, e):
        self.popup_menu.tk_popup(e.x_root, e.y_root)

    def show_storable_name_popup_menu(self, storable_type: str):
        self.popup_storable_name_window = tk.Toplevel(self.root)
        self.popup_storable_name_window.title("Choose storable name")
        self.popup_storable_name_window.geometry("250x150")

        storable_name_helper_label = tk.Label(
            self.popup_storable_name_window, text="Enter storable name:"
        )
        storable_name_helper_label.pack()
        inputtext = tk.Text(self.popup_storable_name_window, height=1, width=10)
        inputtext.pack()

        tk.Button(self.popup_storable_name_window, text="Enter")

    def create_storable(self):
        pass

    def on_click_storable(self):
        pass

    def _on_click_directory(self):
        pass

    def add_storable(self, name: str, storable_type: str):
        storable_button = None
        storable_instance = None
        try:
            storable_instance = self.storable_factory.get_storable(storable_type, name)

            self.storage.current_dir.add(storable_instance)
            storable_button = SButton(
                self.helper_frame, storable_type, storable_instance
            )
            storable_button.pack()

        except StorableNameAlreadyExists as e:
            messagebox.Message(self.root, icon=messagebox.WARNING, message=f"{str(e)}")

    def update_storables_in_frame(self):
        for storable in self.storage.current_dir_components:
            label = tk.Label(self.helper_frame, text=storable.get_name())
            label.pack()
