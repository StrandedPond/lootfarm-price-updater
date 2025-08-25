import tkinter as tk
from tkinter import ttk
import time

class PriceDecreasesTab(ttk.Frame):
    def __init__(self, parent, curr_data, decreases_list):
        super().__init__(parent)
        self.tree = ttk.Treeview(
            self,
            columns=("Name", "Old Price", "New Price", "Change", "Since"),
            show="headings"
        )
        self.tree.heading("Name", text="Name")
        self.tree.heading("Old Price", text="Old Price")
        self.tree.heading("New Price", text="New Price")
        self.tree.heading("Change", text="Change")
        self.tree.heading("Since", text="Since")
        self.tree.pack(expand=True, fill="both")
        self.update_data(decreases_list)

    def update_data(self, decreases_list):
        self.tree.delete(*self.tree.get_children())
        now = time.time()
        for item in decreases_list:
            name = item["name"]
            old_price = item["old"] / 100
            new_price = item["new"] / 100
            change = (item["new"] - item["old"]) / 100
            since = int(now - item["timestamp"])
            since_str = f"{since//60}m {since%60}s"
            self.tree.insert(
                "", "end",
                values=(name, f"{old_price:.2f}", f"{new_price:.2f}", f"{change:.2f}", since_str)
            )