<p align="center"><img src="OzonPrices.png" alt="Logo" width="256"></p>

# ❗ Attention❗ 
Ozon has increased the level of security on its website, causing this bot to no longer function. Since this application was a university project, I do not plan to attempt to fix it. In short: THE BOT DOES NOT WORK

## Shorn description
A Telegram bot that allows tracking price changes for products on Ozon. Search by name `@ozonWatcherBot`

## Installation
> Python 3.10+ is required for the application to work
- Clone the repository into your environment
	```shell
	git clone https://github.com/Nytrock/OzonPricesBot.git
	```
- Install all the required modules and libraries
	```
	    pip install -r requirements.txt
	```
- Create a `.env` file based on the `.env.example` file.
- To run the application on Windows, use
	```
	    python main.py
	```
- MacOS и Linux:
	```
	    python3 main.py
	```

## Application structure


The bot is primarily written using `aiogram_dialog`, with elements of standard `aiogram`. Users can search for products by SKU or name, view product information, and add products to their watchlist.

The parser is built using the `curl_cffi` and `BeautifulSoup4` libraries. If a user requests a product that is not in the database, the parser retrieves the product information and adds it to the database. Interaction with the database is handled through `SQLAlchemy`.

Price tracking is implemented with the `APScheduler` library. Every 6 hours, the system scans all products in the database and checks for price changes. 
If a change is detected, it is recorded in the database, and users with the product in their favorites receive a notification about the price change based on their settings.
