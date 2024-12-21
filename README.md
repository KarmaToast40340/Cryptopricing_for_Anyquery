# Crypto Pricing Plugin for Anyquery

This plugin integrates real-time cryptocurrency pricing data into Anyquery. It allows you to query the prices of selected cryptocurrencies and interact with the data in your SQL queries. The plugin fetches cryptocurrency prices from a public API (CoinGecko) and provides this data in a table format within Anyquery. You can use the table to perform further calculations, such as determining the total value of your crypto assets.

## Features

- Provides a table with real-time cryptocurrency prices for selected cryptocurrencies.
- Supports updates to the cryptocurrency prices.
- Allows querying of the cryptocurrency data with SQL in Anyquery.
- Prices are fetched from the CoinGecko API and include EUR values for a variety of cryptos.

## Prerequisites

Before using the plugin, you need to set up the following:

1. **Notion API Key**: This plugin also requires access to your Notion database to integrate cryptocurrency quantities.
2. **Notion Database ID**: The ID of the Notion database where your cryptocurrency transaction history is stored.

Both of these credentials should be placed in a `.env` file in the root directory of your project.

## Setup

### 1. Install Dependencies

First, ensure that you have Go installed and your Go environment is set up correctly. Then, install the required dependencies:

```bash
# Install Go dependencies
go get github.com/julien040/anyquery
```

### 2. Create the `.env` File

Create a `.env` file to store your Notion API credentials and database ID:

```bash
# .env
NOTION_API_KEY="your_notion_api_key"
NOTION_DATABASE_ID="your_notion_database_id"
```

Replace `"your_notion_api_key"` and `"your_notion_database_id"` with your actual credentials from Notion.

### 3. Plugin Configuration

The plugin uses the CoinGecko API to fetch cryptocurrency prices. By default, it fetches prices for the following cryptocurrencies in EUR:

- Bitcoin (BTC)
- Ethereum (ETH)
- Tezos (XTZ)
- Solana (SOL)
- Hedera Hashgraph (HBAR)
- Cardano (ADA)
- Polkadot (DOT)
- And several others...

The plugin uses this data to create a table in Anyquery, where each row contains the currency name (e.g., "BTC", "ETH") and its current price in EUR.

### 4. SQL Queries

The plugin supports SQL queries to interact with the cryptocurrency pricing data. For example, you can use the following query to retrieve the total value of your cryptocurrency assets:

```sql
SELECT 
    Currency, 
    Value AS Price_in_EUR
FROM 
    cryptopricingplugin_cryptoValueTable;
```

This query will return the latest prices of the supported cryptocurrencies.

## Running the Plugin in Anyquery

### 1. Start the Plugin in Development Mode

To run the plugin in development mode, use the following command:

```bash
anyquery plugin -dev
```

This will start the plugin in development mode, allowing you to test and interact with the plugin directly from Anyquery.

### 2. Querying the Data

Once the plugin is running, you can execute SQL queries to retrieve the crypto pricing data. For example:

```sql
SELECT 
    Currency, 
    Value AS Price_in_EUR
FROM 
    cryptopricingplugin_cryptoValueTable;
```

This will fetch the latest cryptocurrency prices in EUR.

### 3. Updating Prices

The plugin supports updating the cryptocurrency prices. Every time you query the table, the plugin will fetch the latest prices from the CoinGecko API. 

### 4. Calculate Total Asset Value

You can use a query like this to calculate the total value of your assets based on the quantities you hold (retrieved from Notion) and the real-time prices from the plugin:

```sql
SELECT 
    Currency, 
    Amount, 
    Value * Amount AS Total_Value_in_EUR
FROM 
    notion_database, cryptopricingplugin_cryptoValueTable
WHERE 
    notion_database.Currency = cryptopricingplugin_cryptoValueTable.Currency;
```

This query joins your Notion database with the cryptocurrency pricing table, calculates the total value of each asset, and returns the result.

## Plugin Operations

### Table Operations

- **Insert**: Not supported. The plugin does not support inserting rows into the table.
- **Update**: Supported. The table supports updating cryptocurrency prices with the latest values fetched from the CoinGecko API.
- **Delete**: Not supported. The plugin does not support deleting rows from the table.

### Schema

The `cryptopricingplugin_cryptoValueTable` contains two columns:

1. **Currency** (Type: String) – The name of the cryptocurrency (e.g., "BTC", "ETH").
2. **Value** (Type: Float) – The current price of the cryptocurrency in EUR.

## Troubleshooting

If you encounter any issues:

- Ensure that your `.env` file is properly configured with your Notion API key and database ID.
- Make sure your internet connection is active since the plugin fetches live data from the CoinGecko API.
- Verify that Anyquery is installed correctly and you're running the plugin in development mode with the `anyquery plugin -dev` command.

## License

This plugin is open-source. Feel free to fork, modify, and contribute to the project.
