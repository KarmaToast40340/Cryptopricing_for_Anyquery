package main

import (
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/julien040/anyquery/rpc"
)

type cryptoValueTable struct{}

type cryptoValueCursor struct {
	// Add any fields necessary for managing state
}

// Define the schema and columns to expose in Anyquery
func cryptoValueTableCreator(args rpc.TableCreatorArgs) (rpc.Table, *rpc.DatabaseSchema, error) {
	return &cryptoValueTable{}, &rpc.DatabaseSchema{
		HandlesInsert: false,
		HandlesUpdate: true, // Now handling updates
		HandlesDelete: false,
		HandleOffset:  false,
		Columns: []rpc.DatabaseSchemaColumn{
			{Name: "Currency", Type: rpc.ColumnTypeString},
			{Name: "Value", Type: rpc.ColumnTypeFloat},
		},
	}, nil
}

// Close handles cleanup if necessary
func (t *cryptoValueTable) Close() error {
	return nil
}

// CreateReader returns a cursor to handle data reading
func (t *cryptoValueTable) CreateReader() rpc.ReaderInterface {
	return &cryptoValueCursor{}
}

// Delete handles row deletions (not supported in this implementation)
func (t *cryptoValueTable) Delete(row []interface{}) error {
	return fmt.Errorf("delete operation not supported")
}

// Insert handles row insertions (not supported in this implementation)
func (t *cryptoValueTable) Insert(rows [][]interface{}) error {
	return fmt.Errorf("insert operation not supported")
}

// Update handles row updates (now supports single-row update)
func (t *cryptoValueTable) Update(newRows [][]interface{}) error {
	// Handle updates (this is just a placeholder)
	fmt.Println("Rows updated:", newRows)
	return nil
}

// Query fetches rows based on constraints (e.g., crypto names and prices)
func (c *cryptoValueCursor) Query(constraints rpc.QueryConstraint) ([][]interface{}, bool, error) {
	// Fetch the live crypto prices
	prices := getCryptoPrices() // Replace with your API call logic
	rows := [][]interface{}{}

	// Iterate through the data and format it for Anyquery
	for cryptoName, price := range prices {
		rows = append(rows, []interface{}{cryptoName, price})
	}

	// Return the rows, with `true` indicating no more data to fetch
	return rows, true, nil
}

// Function to fetch live prices from an API
func getCryptoPrices() map[string]float64 {
	// Example for CoinGecko
	resp, err := http.Get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,hedera-hashgraph,tezos,ripple,canto,ethereum,solana,usd-coin,elrond-erd-2,crypto-com-chain,euro-coin,cosmos,polkadot,orion-protocol,cardano,jito-governance-token,lukso-token-2,the-graph,polygon-ecosystem-token,matic-network,lumia&vs_currencies=eur")
	if err != nil {
		fmt.Println("Error fetching data:", err)
		return nil
	}
	defer resp.Body.Close()

	var result map[string]map[string]float64
	json.NewDecoder(resp.Body).Decode(&result)

	prices := map[string]float64{
		"XTZ":   result["tezos"]["eur"],
		"XRP":   result["ripple"]["eur"],
		"CANTO": result["canto"]["eur"],
		"HBAR":  result["hedera-hashgraph"]["eur"],
		"EGLD":  result["elrond-erd-2"]["eur"],
		"BTC":   result["bitcoin"]["eur"],
		"ETH":   result["ethereum"]["eur"],
		"SOL":   result["solana"]["eur"],
		"USD":   result["usd-coin"]["eur"],
		"USDC":  result["usd-coin"]["eur"],
		"CRO":   result["crypto-com-chain"]["eur"],
		"EUR":   result["euro-coin"]["eur"],
		"ATOM":  result["cosmos"]["eur"],
		"DOT":   result["polkadot"]["eur"],
		"ORN":   result["orion-protocol"]["eur"],
		"ADA":   result["cardano"]["eur"],
		"JTO":   result["jito-governance-token"]["eur"],
		"LYX":   result["lukso-token-2"]["eur"],
		"GRT":   result["the-graph"]["eur"],
		"POL":   result["polygon-ecosystem-token"]["eur"],
		"MATIC": result["matic-network"]["eur"],
		"LUMIA": result["lumia"]["eur"],
	}
	return prices
}
