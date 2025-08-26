import tkinter as tk
from tkinter import ttk

class AllListingsTab(ttk.Frame):
    def __init__(self, parent, price_data, search_var):
        super().__init__(parent)
        self.price_data = price_data
        self.sort_column = "Name"
        self.sort_reverse = False
        self.search_var = search_var
        self.search_var.trace_add("write", lambda *args: self.refresh_tree())

        # Style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#4a90e2", foreground="white")
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=28, background="#f5f7fa", fieldbackground="#f5f7fa")
        style.map("Treeview", background=[("selected", "#b3d1ff")])
        style.configure("Full.Treeview", background="#ffe5e5")  # Light red for full rows

        # Frame for treeview and scrollbar
        tree_frame = ttk.Frame(self)
        tree_frame.pack(expand=True, fill="both", padx=8, pady=(0,8))

        self.tree = ttk.Treeview(
            tree_frame,
            columns=("Name", "Sell Price", "Buy Price", "Rate", "Have", "Max"),
            show="headings"
        )
        self.tree.heading("Name", text="Name", command=lambda: self.sort_by("Name"))
        self.tree.heading("Sell Price", text="Sell Price", command=lambda: self.sort_by("Sell Price"))
        self.tree.heading("Buy Price", text="Buy Price")
        self.tree.heading("Rate", text="Rate", command=lambda: self.sort_by("Rate"))
        self.tree.heading("Have", text="Have", command=lambda: self.sort_by("Have"))
        self.tree.heading("Max", text="Max", command=lambda: self.sort_by("Max"))
        self.tree.column("Name", width=220)
        self.tree.column("Sell Price", width=90, anchor="center")
        self.tree.column("Buy Price", width=90, anchor="center")
        self.tree.column("Rate", width=90, anchor="center")
        self.tree.column("Have", width=60, anchor="center")
        self.tree.column("Max", width=60, anchor="center")

        # Add vertical scrollbar
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(side="left", expand=True, fill="both")

        # Tag for full rows
        self.tree.tag_configure("full", background="#ffe5e5")

        self.update_data(price_data)

    def sort_by(self, column):
        # Map column names to item keys
        col_map = {
            "Name": lambda item: item.get("name", ""),
            "Sell Price": lambda item: item.get("price", 0),
            "Rate": lambda item: item.get("rate", 0),
            "Have": lambda item: item.get("have", 0),
            "Max": lambda item: item.get("max", 0)
        }
        if self.sort_column == column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_column = column
            self.sort_reverse = False

        key_func = col_map.get(column, lambda item: item.get("name", ""))
        self.price_data.sort(key=key_func, reverse=self.sort_reverse)
        self.update_data(self.price_data)

    def update_data(self, price_data):
        self.price_data = price_data
        self.displayed_data = self.price_data  # For search/filter
        self.refresh_tree()

    def refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        filter_text = self.search_var.get().lower()
        count = 0
        for item in self.price_data:
            name = item.get("name", "")
            if filter_text and filter_text not in name.lower():
                continue
            sell_price = item.get("price", 0) / 100
            buy_price = round(sell_price * 0.97, 2)
            rate = item.get("rate", 0) / 100
            have = item.get("have", 0)
            max_ = item.get("max", 0)
            tags = ("full",) if have >= max_ and max_ > 0 else ()
            self.tree.insert(
                "", "end",
                values=(name, f"{sell_price:.2f}", f"{buy_price:.2f}", f"{rate:.2f}", have, max_),
                tags=tags
            )
            count += 1
            if count >= 100:
                break

    def on_search(self, event=None):
        self.refresh_tree()
