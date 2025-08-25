# Price Update App

## Overview
The Price Update App is a Python application designed to track item listings from a trading site. It provides users with an intuitive interface to view all item listings, as well as those that have experienced price increases or decreases.

## Features
- **All Listings Tab**: Displays all item listings with their selling and calculated buying prices.
- **Price Increases Tab**: Shows listings that have experienced price increases.
- **Price Decreases Tab**: Displays listings that have experienced price decreases.

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd price-update-app
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
To run the application, execute the following command:
```
python src/main.py
```

## File Structure
```
lootfarm-price-updater
├── src
│   ├── main.py                # Entry point of the application
│   ├── tabs
│   │   ├── all_listings.py    # Displays all item listings
│   │   ├── price_increases.py  # Displays items with price increases
│   │   └── price_decreases.py  # Displays items with price decreases
│   └── utils
│       └── price_calculator.py # Contains price calculation logic
├── requirements.txt            # Lists project dependencies
└── README.md                   # Project documentation
```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.