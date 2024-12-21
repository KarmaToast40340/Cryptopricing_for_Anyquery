package main

import (
    "github.com/julien040/anyquery/rpc"
	"log"
)

// Fonction principale pour démarrer le plugin
func main() {
    // Enregistrer la table que tu as définie (crypto_value) 
    plugin := rpc.NewPlugin(cryptoValueTableCreator)

    // Démarrer le serveur du plugin
    if err := plugin.Serve(); err != nil {
        log.Fatalf("Erreur lors du démarrage du plugin : %v", err)
    }
}
