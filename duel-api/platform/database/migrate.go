package database

import (
	"duel-api/app/models"
	"gorm.io/gorm"
	"log"
)

func Setup(db *gorm.DB) {
	runPreMigrationsTasks(db)
	runMigrations(db)
	runPostMigrationsTasks(db)
}

func runPreMigrationsTasks(db *gorm.DB) {
	db.Exec("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")
}
func runMigrations(db *gorm.DB) {

	err := db.AutoMigrate(
		&models.AdvocacyCampaignOutcome{},
	)

	if err != nil {
		log.Fatalf("❌ Failed to migrate: %v", err)
	}

	log.Println("✅ Migrations completed!")

}

func runPostMigrationsTasks(db *gorm.DB) {
	print("qq")
}
