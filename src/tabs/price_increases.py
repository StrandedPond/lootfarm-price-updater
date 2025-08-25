import tkinter as tk
from tkinter import ttk
import time

class PriceIncreasesTab(ttk.Frame):
    def __init__(self, parent, curr_data, increases_list):
        super().__init__(parent)
        self.increases_list = increases_list
        self.sort_column = "Name"
        self.sort_reverse = False

        # Frame for treeview and scrollbar
        tree_frame = ttk.Frame(self)
        tree_frame.pack(expand=True, fill="both")

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("Name", "Old Price", "New Price", "Have", "Max", "Change"),
            show="headings"
        )
        self.tree.heading("Name", text="Name", command=lambda: self.sort_by("Name"))
        self.tree.heading("Old Price", text="Old Price", command=lambda: self.sort_by("Old Price"))
        self.tree.heading("New Price", text="New Price", command=lambda: self.sort_by("New Price"))
        self.tree.heading("Have", text="Have", command=lambda: self.sort_by("Have"))
        self.tree.heading("Max", text="Max", command=lambda: self.sort_by("Max"))
        self.tree.heading("Change", text="Change", command=lambda: self.sort_by("Change"))
        self.tree.column("Have", width=60, anchor="center")
        self.tree.column("Max", width=60, anchor="center")

        # Add vertical scrollbar
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(side="left", expand=True, fill="both")

        # Tag for full rows
        self.tree.tag_configure("full", background="#ffe5e5")

        self.tree.bind("<Button-1>", self.on_tree_click)

        self.update_data(increases_list)

    def on_tree_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return
        col = self.tree.identify_column(event.x)
        if col != "#1":  # Name column is #1
            return
        row_id = self.tree.identify_row(event.y)
        if not row_id:
            return
        name = self.tree.item(row_id, "values")[0]
        self.clipboard_clear()
        self.clipboard_append(name)
        self.update()  # Ensures clipboard is set
    def __init__(self, parent, curr_data, increases_list):
        super().__init__(parent)
        self.increases_list = increases_list
        self.sort_column = "Name"
        self.sort_reverse = False

        # Frame for treeview and scrollbar
        tree_frame = ttk.Frame(self)
        tree_frame.pack(expand=True, fill="both")

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("Name", "Old Price", "New Price", "Have", "Max", "Change"),
            show="headings"
        )
        self.tree.heading("Name", text="Name", command=lambda: self.sort_by("Name"))
        self.tree.heading("Old Price", text="Old Price", command=lambda: self.sort_by("Old Price"))
        self.tree.heading("New Price", text="New Price", command=lambda: self.sort_by("New Price"))
        self.tree.heading("Have", text="Have", command=lambda: self.sort_by("Have"))
        self.tree.heading("Max", text="Max", command=lambda: self.sort_by("Max"))
        self.tree.heading("Change", text="Change", command=lambda: self.sort_by("Change"))
        self.tree.column("Have", width=60, anchor="center")
        self.tree.column("Max", width=60, anchor="center")

        # Add vertical scrollbar
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(side="left", expand=True, fill="both")

        # Tag for full rows
        self.tree.tag_configure("full", background="#ffe5e5")

        self.update_data(increases_list)

    def sort_by(self, column):
        col_map = {
            "Name": lambda item: item["name"],
            "Old Price": lambda item: item["old"],
            "New Price": lambda item: item["new"],
            "Have": lambda item: item.get("have", 0),
            "Max": lambda item: item.get("max", 0),
            "Change": lambda item: item["change"],
        }
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
            self.sort_reverse = False

        key_func = col_map.get(column, lambda item: item["name"])
        self.increases_list.sort(key=key_func, reverse=self.sort_reverse)
        self.refresh_tree()

    def update_data(self, increases_list):
        self.increases_list = increases_list
        self.refresh_tree()

    def refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        for item in self.increases_list:
            name = item["name"]
            old_price = item["old"] / 100
            new_price = item["new"] / 100
            change = (item["new"] - item["old"]) / 100
            have = item.get("have", 0)
            max_ = item.get("max", 0)
            tags = ("full",) if have >= max_ and max_ > 0 else ()
            self.tree.insert(
                "", "end",
                values=(name, f"{old_price:.2f}", f"{new_price:.2f}", have, max_, f"+{change:.2f}"),
                tags=tags
            )