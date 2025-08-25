import requests
import time
from tkinter import Tk
from tkinter.ttk import Notebook
from tabs.all_listings import AllListingsTab
from tabs.price_increases import PriceIncreasesTab
from tabs.price_decreases import PriceDecreasesTab

PRICE_URL = "https://loot.farm/fullpriceTF2.json"
UPDATE_INTERVAL_MS = 60_000  # 60 seconds
DECAY_SECONDS = 15 * 60      # 15 minutes

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

    notebook = Notebook(root)

    # State for decay logic
    app_state = {
        "prev_data": [],
        "curr_data": fetch_price_data(),
        "increases": {},  # name: {"old": old_price, "new": new_price, "timestamp": t}
        "decreases": {}   # name: {"old": old_price, "new": new_price, "timestamp": t}
    }

    all_listings_tab = AllListingsTab(notebook, app_state["curr_data"])
    price_increases_tab = PriceIncreasesTab(notebook, app_state["curr_data"], [])
    price_decreases_tab = PriceDecreasesTab(notebook, app_state["curr_data"], [])

    notebook.add(all_listings_tab, text='All Listings')
    notebook.add(price_increases_tab, text='Price Increases')
    notebook.add(price_decreases_tab, text='Price Decreases')
    notebook.pack(expand=True, fill='both')

    def update_data():
        new_data = fetch_price_data()
        now = time.time()
        if new_data:
            prev_map = build_price_map(app_state["curr_data"])
            curr_map = build_price_map(new_data)

            # Handle increases
            for name, new_price in curr_map.items():
                old_price = prev_map.get(name)
                if old_price is not None:
                    # Price increased
                    if new_price > old_price:
                        # If already in increases, update and reset timer
                        app_state["increases"][name] = {
                            "old": old_price,
                            "new": new_price,
                            "timestamp": now
                        }
                        # Remove from decreases if present
                        if name in app_state["decreases"]:
                            del app_state["decreases"][name]
                    # Price decreased
                    elif new_price < old_price:
                        # Remove from increases if present and add to decreases
                        if name in app_state["increases"]:
                            del app_state["increases"][name]
                        app_state["decreases"][name] = {
                            "old": old_price,
                            "new": new_price,
                            "timestamp": now
                        }

            # Decay logic: remove entries older than 15 minutes
            app_state["increases"] = {
                k: v for k, v in app_state["increases"].items()
                if now - v["timestamp"] < DECAY_SECONDS
            }
            app_state["decreases"] = {
                k: v for k, v in app_state["decreases"].items()
                if now - v["timestamp"] < DECAY_SECONDS
            }

            # Prepare lists for tabs
            increases_list = [
                {
                    "name": name,
                    "old": v["old"],
                    "new": v["new"],
                    "change": v["new"] - v["old"],
                    "timestamp": v["timestamp"]
                }
                for name, v in app_state["increases"].items()
            ]
            decreases_list = [
                {
                    "name": name,
                    "old": v["old"],
                    "new": v["new"],
                    "change": v["new"] - v["old"],
                    "timestamp": v["timestamp"]
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