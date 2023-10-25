import tkinter as tk
from file_manager.storage import Storage


class GUI:
    def __init__(self):
        self.storage = Storage()
        self.root = tk.Tk()

        self.root.geometry("600x400")

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=1)

        # Configure scrollbar
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

        label = tk.Label(self.helper_frame, text="Label")
        label.pack()
        del_button = tk.Button(
            self.helper_frame, text="Delete", command=lambda: label.destroy()
        )
        del_button.pack()

        self.root.mainloop()

    def cd(self):
        pass

    def update_storables_in_frame(self):

        for storable in self.storage.current_dir_components:
            label = tk.Label(self.helper_frame, text=storable.get_name())
            label.pack()
