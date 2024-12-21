# Makefile to build the crypto-pricing-plugin

# Name of the plugin executable
PLUGIN_NAME = cryptopricingplugin

# Path to Go source code
SRC_FILES = main.go cryptocurrencies.go

# Go build command
build:
	go build -o $(PLUGIN_NAME) $(SRC_FILES)

# Clean up generated files
clean:
	rm -f $(PLUGIN_NAME)