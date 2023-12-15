
# BTCUSDT Indicator

An crypto indicator using k-nearest neighbor to check for buy and sell signals.

### Main Functionality

1. Retrieve past crypto data using the Binance api

2. Check the knn accuracy based on the past crypto data

3. Setting up a discord bot that runs the indicator

  

## Set-Up

1. Clone the Repo:

	````
	git clone https://github.com/lshadoyan/GPA-Optimizer.git
	````

2. Install requirements:

	````
	pip install -r requirements.txt
	````

### Discord Bot Set-Up

1. Create a new Discord bot through the Developer Portal:

		https://discord.com/developers/applications
2. Modify text permissions to allow sending messages and imbedding links
3. Create a .env file and copy the `bot token` into the file while setting it equal to `BOT_TOKEN` 
	```` 
	BOT_TOKEN=
	````
4. Add the bot to a Discord Channel 

### Binance Set-Up
1. Create an public and secret API key 
2. In the .env file add two separate variables for the public and secret keys and copy them into the file
	```` 
	API_KEY=
	````
	````
	SECRET_KEY=
	````

## Commands
Specify usage using commands provided below:
#### Evaluates the ML model
````
python main.py -s knn_evaluation
````
#### Outputs historical data
````
python main.py -s historical_data
````
#### Starts the Indicator and Discord bot
````
python main.py -s indicator
````
**Note:** It is not recommended, but `-s` can be replaced by `-c` for a less robust KNN model