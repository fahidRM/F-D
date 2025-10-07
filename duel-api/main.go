// main.go
package main

import (
	"duel-api/pkg/config"
	"duel-api/pkg/routes"
	"duel-api/platform/database"
	"github.com/gofiber/fiber/v3"
	"log"
)

func main() {
	config.LoadEnv()
	config.ConnectDatabase()
	database.Setup(config.DB)
	app := fiber.New()

	routes.SetRoutes(app)

	log.Fatal(app.Listen(":3030"))
}
