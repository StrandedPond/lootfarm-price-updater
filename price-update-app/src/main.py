import requests
from tkinter import Tk
from tkinter.ttk import Notebook
from tabs.all_listings import AllListingsTab
from tabs.price_increases import PriceIncreasesTab
from tabs.price_decreases import PriceDecreasesTab

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

def main():
    root = Tk()
    root.title("Price Update Application")

    notebook = Notebook(root)

    # Store previous and current price data for change detection
    app_state = {
        "prev_data": [],
        "curr_data": fetch_price_data()
    }

    all_listings_tab = AllListingsTab(notebook, app_state["curr_data"])
    price_increases_tab = PriceIncreasesTab(notebook, app_state["curr_data"], app_state["prev_data"])
    price_decreases_tab = PriceDecreasesTab(notebook, app_state["curr_data"], app_state["prev_data"])

    notebook.add(all_listings_tab, text='All Listings')
    notebook.add(price_increases_tab, text='Price Increases')
    notebook.add(price_decreases_tab, text='Price Decreases')
    notebook.pack(expand=True, fill='both')

    def update_data():
        new_data = fetch_price_data()
        if new_data:
            app_state["prev_data"] = app_state["curr_data"]
            app_state["curr_data"] = new_data

            all_listings_tab.update_data(app_state["curr_data"])
            price_increases_tab.update_data(app_state["curr_data"], app_state["prev_data"])
            price_decreases_tab.update_data(app_state["curr_data"], app_state["prev_data"])
        root.after(UPDATE_INTERVAL_MS, update_data)

    root.after(UPDATE_INTERVAL_MS, update_data)
    root.mainloop()

if __name__ == "__main__":
    main()