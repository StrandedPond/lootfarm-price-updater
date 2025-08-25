import tkinter as tk
from tkinter import ttk

class PriceIncreasesTab(ttk.Frame):
    def __init__(self, parent, curr_data, prev_data):
        super().__init__(parent)
        self.tree = ttk.Treeview(self, columns=("Name", "Old Price", "New Price", "Change"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Old Price", text="Old Price")
        self.tree.heading("New Price", text="New Price")
        self.tree.heading("Change", text="Change")
        self.tree.pack(expand=True, fill="both")
        self.update_data(curr_data, prev_data)

    def update_data(self, curr_data, prev_data):
        self.tree.delete(*self.tree.get_children())
        prev_prices = {item["name"]: item["price"] for item in prev_data}
        for item in curr_data:
            name = item.get("name", "")
            new_price = item.get("price", 0)
            old_price = prev_prices.get(name)
            if old_price is not None and new_price > old_price:
                self.tree.insert(
                    "", "end",
                    values=(
                        name,
                        f"{old_price/100:.2f}",
                        f"{new_price/100:.2f}",
                        f"+{(new_price-old_price)/100:.2f}"
                    )
                )