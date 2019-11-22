# Index-LArestaurant

This project loads the LA Restaurants & Market Health data set (available at Kaggle: https://www.kaggle.com/cityofLA/la-restaurant-market-health-data) into Firebase and creates an inverted index for restaurant names to facilitate the searching of LA restaurants.

(1) Loading data & creating index

"load.py" is a Python script that converts the data from a csv file (restaurants.csv) into the JSON format and load the dataset into Firebase. At the same time, it creates an inverted index in the same Firebase database for the facility_name column. The index stores, for each unique word in the name, the serial_number of restaurant whose name contains the word. The words are delimited by white spaces and obtained after removing punctuation charaters.

The index looks like the following:
	{"index": {
		"habitat": [DAJ00E07B, …],
		"coffee": [DAJ00E07B, …],
		"shop": [DAJ00E07B, …],
		…
	}

Execution format: python load.py restaurants.csv

(2) Searching

"search.py" is a Python script takes a a string of keywords (separated by white space) and returns names and scores of restaurants whose name contains one or more keywords in the list. The search is executed using the data stored in my Firebase database. The search case-insensitive and punctuations are removed (i.e. "coffee& SH-OP" is the same as "coffee shop").

Execution format: python search.py “coffee shop”
