import tkinter as tk
from tkinter import messagebox
from file_manager.storage import Storage
from file_manager.exceptions import StorableNameAlreadyExists, StorableNameNotAvailable
from file_manager.data_types.storable import (
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

        self._current_row = len(self.storage.current_dir_components)

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
            label="Document",
            command=lambda: self.show_storable_name_popup_menu("document"),
        )

        self.sort_by_menu = tk.Menu(self.root, tearoff=False)
        self.sort_by_menu.add_command(label="Name")

        self.popup_menu.add_cascade(label="Create", menu=self.create_storable_menu)
        self.popup_menu.add_cascade(label="Sort by", menu=self.sort_by_menu)

        self.popup_storable_name_window = None

        self.root.bind("<Button-3>", self.show_popup_menu)

        self.nav_button_frame = tk.Frame(self.root)
        self.nav_button_frame.pack(side=tk.TOP, padx=10, pady=5)
        prev_button = tk.Button(
            self.nav_button_frame,
            text="Previous",
            command=self.on_click_previous_button,
        )
        prev_button.pack(side=tk.LEFT)

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

        enter_button = tk.Button(
            self.popup_storable_name_window,
            text="Enter",
            command=lambda: [
                self.add_storable(inputtext.get(1.0, "end-1c"), storable_type),
                self.popup_storable_name_window.destroy(),
            ],
        )
        enter_button.pack()

    def on_click_storable(
        self, storable_instance: StorableComponent, storable_type: str
    ):
        if storable_type == "directory":
            self.storage.current_dir = storable_instance
            self.update_storables_in_frame()
        elif storable_type == "file":
            pass
        elif storable_type == "document":
            pass

    def _place_storable_button(self, storable_button: SButton):
        storable_button.grid(row=self._current_row, column=0, columnspan=4)
        storable_type_label = tk.Label(
            self.helper_frame, text=storable_button.storable_type
        )
        storable_type_label.grid(row=self._current_row, column=5, columnspan=4)

        self._current_row += 1

    def add_storable(self, name: str, storable_type: str):
        storable_button = None
        storable_instance = None
        try:
            storable_instance = self.storable_factory.get_storable(storable_type, name)

            self.storage.current_dir.add(storable_instance)

            storable_button = SButton(
                self.helper_frame,
                storable_type,
                storable_instance,
                text=name,
                width=10,
                height=1,
                command=lambda: self.on_click_storable(
                    storable_instance, storable_type
                ),
            )
            self._place_storable_button(storable_button)

        except (StorableNameAlreadyExists, StorableNameNotAvailable) as e:
            messagebox.showwarning(
                title="Storable creation warning",
                icon=messagebox.WARNING,
                message=f"{str(e)}",
            )

    def update_storables_in_frame(self):
        for child in self.helper_frame.winfo_children():
            child.destroy()

        self._current_row = len(self.storage.current_dir_components)
        for storable in self.storage.current_dir_components:
            storable_button = SButton(
                self.helper_frame,
                storable.storable_type,
                storable,
                text=storable.get_name(),
                width=10,
                height=1,
                command=lambda s=storable, t=storable.storable_type:
                self.on_click_storable(
                    s, t
                ),
            )
            self._place_storable_button(storable_button)

    def on_click_previous_button(self):
        if not self.storage.current_dir.parent_directory:
            return
        self.storage.current_dir = self.storage.current_dir.parent_directory

        self.update_storables_in_frame()
