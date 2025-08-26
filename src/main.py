
import requests
import time
import json
import os
from tkinter import Tk
from tkinter.ttk import Notebook
from tabs.all_listings import AllListingsTab
from tabs.price_increases import PriceIncreasesTab
from tabs.price_decreases import PriceDecreasesTab
INCREASES_FILE = "increases.json"
DECREASES_FILE = "decreases.json"

PRICE_URL = "https://loot.farm/fullpriceTF2.json"
UPDATE_INTERVAL_MS = 60_000  # 60 seconds


def fetch_price_data():
    try:
        response = requests.get(PRICE_URL)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Failed to fetch price data: {e}")
        return []

def build_price_map(data):
    return {item["name"]: item["price"] for item in data}

def main():
    root = Tk()
    root.title("Price Update Application")


    # Universal search bar
    import tkinter as tk
    search_var = tk.StringVar()
    search_frame = tk.Frame(root)
    search_frame.pack(fill="x", padx=8, pady=4)
    tk.Label(search_frame, text="Search:").pack(side="left")
    search_entry = tk.Entry(search_frame, textvariable=search_var)
    search_entry.pack(side="left", padx=4)

    # Auto-refresh ticker (custom toggle switch)
    ticker_var = tk.BooleanVar(value=True)
    ticker_frame = tk.Frame(root)
    ticker_frame.pack(fill="x", padx=8, pady=2)
    ticker_label = tk.Label(ticker_frame, text="Auto Refresh", font=("Segoe UI", 10, "bold"))
    ticker_label.pack(side="left", padx=(0, 8))
    ticker_canvas = tk.Canvas(ticker_frame, width=50, height=28, highlightthickness=0, bg=ticker_frame.cget("bg"))
    ticker_canvas.pack(side="left")

    def draw_ticker():
        ticker_canvas.delete("all")
        if ticker_var.get():
            # ON: blue background, circle right
            ticker_canvas.create_rectangle(2, 6, 48, 22, fill="#4a90e2", outline="#4a90e2", width=2, tags="bg")
            ticker_canvas.create_oval(26, 4, 46, 24, fill="#fff", outline="#4a90e2", width=2, tags="knob")
        else:
            # OFF: gray background, circle left
            ticker_canvas.create_rectangle(2, 6, 48, 22, fill="#ccc", outline="#ccc", width=2, tags="bg")
            ticker_canvas.create_oval(4, 4, 24, 24, fill="#fff", outline="#ccc", width=2, tags="knob")

    def toggle_ticker(event=None):
        ticker_var.set(not ticker_var.get())
        draw_ticker()

    ticker_canvas.bind("<Button-1>",(toggle_ticker))
    draw_ticker()

    notebook = Notebook(root)

    # Load increases and decreases from JSON files if they exist
    def load_json_dict(filename):
        if os.path.exists(filename):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return {k: v for k, v in data.items()}
            except Exception:
                return {}
        return {}

    app_state = {
        "prev_data": [],
        "curr_data": fetch_price_data(),
        "increases": load_json_dict(INCREASES_FILE),
        "decreases": load_json_dict(DECREASES_FILE)
    }

    all_listings_tab = AllListingsTab(notebook, app_state["curr_data"], search_var)
    price_increases_tab = PriceIncreasesTab(notebook, app_state["curr_data"], [], search_var)
    price_decreases_tab = PriceDecreasesTab(notebook, app_state["curr_data"], [], search_var)

    notebook.add(all_listings_tab, text='All Listings')
    notebook.add(price_increases_tab, text='Price Increases')
    notebook.add(price_decreases_tab, text='Price Decreases')
    notebook.pack(expand=True, fill='both')


    def save_json_dict(filename, data):
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def update_data():
        if ticker_var.get():
            new_data = fetch_price_data()
            if new_data:
                prev_map = build_price_map(app_state["curr_data"])
                curr_map = build_price_map(new_data)

                # Track if there are new changes
                increases_changed = False
                decreases_changed = False

                # Handle increases
                for name, new_price in curr_map.items():
                    old_price = prev_map.get(name)
                    if old_price is not None:
                        # Price increased
                        if new_price > old_price:
                            if (name not in app_state["increases"]) or (app_state["increases"][name]["old"] != old_price or app_state["increases"][name]["new"] != new_price):
                                increases_changed = True
                            app_state["increases"][name] = {
                                "old": old_price,
                                "new": new_price
                            }
                            if name in app_state["decreases"]:
                                del app_state["decreases"][name]
                                decreases_changed = True
                        # Price decreased
                        elif new_price < old_price:
                            if name in app_state["increases"]:
                                del app_state["increases"][name]
                                increases_changed = True
                            if (name not in app_state["decreases"]) or (app_state["decreases"][name]["old"] != old_price or app_state["decreases"][name]["new"] != new_price):
                                decreases_changed = True
                            app_state["decreases"][name] = {
                                "old": old_price,
                                "new": new_price
                            }

                # If there are new changes, save to JSON files
                if increases_changed:
                    save_json_dict(INCREASES_FILE, app_state["increases"])
                if decreases_changed:
                    save_json_dict(DECREASES_FILE, app_state["decreases"])

                # Prepare lists for tabs
                increases_list = [
                    {
                        "name": name,
                        "old": v["old"],
                        "new": v["new"],
                        "change": v["new"] - v["old"]
                    }
                    for name, v in app_state["increases"].items()
                ]
                decreases_list = [
                    {
                        "name": name,
                        "old": v["old"],
                        "new": v["new"],
                        "change": v["new"] - v["old"]
                    }
                    for name, v in app_state["decreases"].items()
                ]

                app_state["prev_data"] = app_state["curr_data"]
                app_state["curr_data"] = new_data

                all_listings_tab.update_data(app_state["curr_data"])
                price_increases_tab.update_data(increases_list)
                price_decreases_tab.update_data(decreases_list)
        root.after(UPDATE_INTERVAL_MS, update_data)

    root.after(UPDATE_INTERVAL_MS, update_data)
    root.mainloop()

if __name__ == "__main__":
    main()