package routes

import (
	"duel-api/app/controllers"
	"github.com/gofiber/fiber/v3"
	"github.com/gofiber/fiber/v3/middleware/static"
)

func SetRoutes(app *fiber.App) {

	app.Get("/*", static.New("./public"))
	api := app.Group("/api")
	api.Get("advocates", controllers.ListAdvocates)
	api.Get("advocates/rank", controllers.RankAdvocates)
	api.Get("overview", controllers.GetOverview)
	api.Get("platforms", controllers.ListPlatforms)
	api.Get("programs", controllers.ListPrograms)
	api.Get("stats/programs/:programId<guid>", controllers.GetProgramStats)
	api.Get("stats/platform/:platform", controllers.GetPlatformStats)
	api.Get("stats/advocate/:advocateId<guid>", controllers.GetUserStats)
}
