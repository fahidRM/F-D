package config

import (
	"log"

	"github.com/joho/godotenv"
)

func LoadEnv() {
	err := godotenv.Load()
	if err != nil {
		log.Println("⚠️ Warning: .env file not found, using environment values instead.\n")
	} else {
		log.Println("🔑 .env file loaded successfully\n")
	}
}
