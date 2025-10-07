package controllers

import (
	"duel-api/app/dtos"
	"duel-api/pkg/config"
	"github.com/gofiber/fiber/v3"
	"github.com/google/uuid"
	"strconv"
	"strings"
)

func GetOverview(c fiber.Ctx) error {

	var overviewStats dtos.OverviewStats

	config.DB.Raw(`SELECT COUNT(DISTINCT program_id) FROM advocacy_campaign_outcomes`).Scan(&overviewStats.ProgramsCount)
	config.DB.Raw(`SELECT COUNT(DISTINCT task_id) FROM advocacy_campaign_outcomes`).Scan(&overviewStats.ActivitiesCount)
	config.DB.Raw(`SELECT COUNT(DISTINCT platform) FROM advocacy_campaign_outcomes`).Scan(&overviewStats.PlatformsCount)
	config.DB.Raw(`SELECT COUNT(DISTINCT brand) FROM advocacy_campaign_outcomes`).Scan(&overviewStats.BrandsCount)
	config.DB.Raw(`SELECT SUM(comments) FROM advocacy_campaign_outcomes`).Scan(&overviewStats.TotalComments)
	config.DB.Raw(`SELECT SUM(likes) FROM advocacy_campaign_outcomes`).Scan(&overviewStats.TotalLikes)
	config.DB.Raw(`SELECT SUM(reach) FROM advocacy_campaign_outcomes`).Scan(&overviewStats.TotalReach)
	config.DB.Raw(`SELECT SUM(shares) FROM advocacy_campaign_outcomes`).Scan(&overviewStats.TotalShares)
	config.DB.Raw(`SELECT SUM(total_sales_attributed) FROM advocacy_campaign_outcomes`).Scan(&overviewStats.TotalSalesAttributed)

	return c.JSON(overviewStats)

}

func ListAdvocates(c fiber.Ctx) error {
	pageStr := c.Query("page", "1")
	limitStr := c.Query("limit", "10")
	page, _ := strconv.Atoi(pageStr)
	limit, _ := strconv.Atoi(limitStr)
	offset := (page - 1) * limit

	var advocates []dtos.AdvocateOverview
	query := `
        SELECT DISTINCT id, name, email, instagram_handle, tiktok_handle
        FROM advocacy_campaign_outcomes
        ORDER BY name DESC
        LIMIT ? OFFSET ?
    `
	if err := config.DB.Raw(query, limit, offset).Scan(&advocates).Error; err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": "Failed to fetch advocates",
		})
	}

	var total int64
	countQuery := `
        SELECT COUNT(DISTINCT id)
        FROM advocacy_campaign_outcomes
    `
	if err := config.DB.Raw(countQuery).Scan(&total).Error; err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": "Failed to count advocates",
		})
	}

	return c.JSON(fiber.Map{
		"data":  advocates,
		"page":  page,
		"limit": limit,
		"total": total,
	})
}

func ListPlatforms(c fiber.Ctx) error {
	var platforms []dtos.PlatformOverview
	query := `
        SELECT DISTINCT  platform
        FROM advocacy_campaign_outcomes
    `
	if err := config.DB.Raw(query).Scan(&platforms).Error; err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": "Failed to fetch platforms",
		})
	}
	return c.JSON(platforms)
}

func ListPrograms(c fiber.Ctx) error {
	pageStr := c.Query("page", "1")
	limitStr := c.Query("limit", "10")
	page, _ := strconv.Atoi(pageStr)
	limit, _ := strconv.Atoi(limitStr)
	if page < 1 {
		page = 1
	}
	if limit < 1 {
		limit = 10
	}
	offset := (page - 1) * limit

	var programs []dtos.ProgramOverview
	query := `
        SELECT DISTINCT program_id, brand
        FROM advocacy_campaign_outcomes
        LIMIT ? OFFSET ?
    `
	if err := config.DB.Raw(query, limit, offset).Scan(&programs).Error; err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": "Failed to fetch programs",
		})
	}

	var total int64
	countQuery := `
        SELECT COUNT(DISTINCT program_id)
        FROM advocacy_campaign_outcomes
    `
	if err := config.DB.Raw(countQuery).Scan(&total).Error; err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": "Failed to count programs",
		})
	}

	return c.JSON(fiber.Map{
		"data":  programs,
		"page":  page,
		"limit": limit,
		"total": total,
	})
}

func GetProgramStats(c fiber.Ctx) error {
	programID, _ := uuid.Parse(c.Params("programId"))
	if programID == uuid.Nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid Program",
		})
	}
	var programStats []dtos.ProgramStats
	programQuery := `
        SELECT
            program_id,
            brand,
            SUM(likes) AS total_likes,
            SUM(comments) AS total_comments,
            SUM(reach) AS total_reach,
            SUM(shares) AS total_shares,
            SUM(total_sales_attributed) AS total_sales_attributed
        FROM advocacy_campaign_outcomes
        WHERE program_id = ?
        GROUP BY program_id, brand
    `
	if err := config.DB.Raw(programQuery, programID.String()).Scan(&programStats).Error; err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": "Failed to fetch program stats",
		})
	}

	// Per-activity stats
	var activityStats []dtos.ProgramActivityStats
	activityQuery := `
        SELECT
            program_id,
            brand,
            task_id AS activity_id,
            SUM(likes) AS total_likes,
            SUM(comments) AS total_comments,
            SUM(reach) AS total_reach,
            SUM(shares) AS total_shares,
            SUM(total_sales_attributed) AS total_sales_attributed
        FROM advocacy_campaign_outcomes
        WHERE program_id = ?
        GROUP BY program_id, brand, task_id
    `
	if err := config.DB.Raw(activityQuery, programID.String()).Scan(&activityStats).Error; err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": "Failed to fetch activity stats",
		})
	}

	return c.JSON(fiber.Map{
		"program_stats":  programStats,
		"activity_stats": activityStats,
	})
}

func GetPlatformStats(c fiber.Ctx) error {
	platform := c.Params("platform")
	if platform == "" {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid Platform",
		})
	}
	var stats []dtos.PlatformStats
	query := `
        SELECT
            platform,
            COUNT(DISTINCT task_id) AS activities,
            SUM(likes) AS total_likes,
            SUM(comments) AS total_comments,
            SUM(reach) AS total_reach,
            SUM(shares) AS total_shares,
            SUM(total_sales_attributed) AS total_sales_attributed
        FROM advocacy_campaign_outcomes
        WHERE platform = ?
        GROUP BY platform
        
    `
	if err := config.DB.Raw(query, platform).Scan(&stats).Error; err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": "Failed to fetch platform stats",
		})
	}

	return c.JSON(fiber.Map{
		"data": stats,
	})
}

func GetUserStats(c fiber.Ctx) error {
	userID, _ := uuid.Parse(c.Params("advocateId"))
	if userID == uuid.Nil {
		return c.Status(fiber.StatusBadRequest).JSON(fiber.Map{
			"error": "Invalid user ID",
		})
	}

	// Per-platform stats
	var platformStats []dtos.UserPlatformStats
	platformQuery := `
    SELECT
        platform,
        SUM(likes) AS total_likes,
        SUM(comments) AS total_comments,
        SUM(reach) AS total_reach,
        SUM(shares) AS total_shares,
        SUM(total_sales_attributed) AS total_sales_attributed
    FROM advocacy_campaign_outcomes
    WHERE user_id = ?
    GROUP BY platform
`
	if err := config.DB.Raw(platformQuery, userID.String()).Scan(&platformStats).Error; err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": "Failed to fetch user platform stats",
		})
	}

	// Per-program stats
	var programStats []dtos.UserProgramStats
	programQuery := `
    SELECT
        program_id,
        brand,
        SUM(likes) AS total_likes,
        SUM(comments) AS total_comments,
        SUM(reach) AS total_reach,
        SUM(shares) AS total_shares,
        SUM(total_sales_attributed) AS total_sales_attributed
    FROM advocacy_campaign_outcomes
    WHERE user_id = ?
    GROUP BY program_id, brand
`
	if err := config.DB.Raw(programQuery, userID.String()).Scan(&programStats).Error; err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": "Failed to fetch user program stats",
		})
	}

	return c.JSON(fiber.Map{
		"platform_stats": platformStats,
		"program_stats":  programStats,
	})
}

func RankAdvocates(c fiber.Ctx) error {
	sortBy := c.Query("sort_by", "total_sales_attributed")
	program := c.Query("program")
	activity := c.Query("activity")
	platform := c.Query("platform")

	pageStr := c.Query("page", "1")
	limitStr := c.Query("limit", "10")
	page, _ := strconv.Atoi(pageStr)
	limit, _ := strconv.Atoi(limitStr)
	if page < 1 {
		page = 1
	}
	if limit < 1 {
		limit = 10
	}
	offset := (page - 1) * limit

	allowedSort := map[string]bool{
		"likes": true, "reach": true, "comments": true, "shares": true, "total_sales_attributed": true,
	}
	if !allowedSort[sortBy] {
		sortBy = "total_sales_attributed"
	}

	var filters []string
	var args []interface{}
	if program != "" {
		filters = append(filters, "program_id = ?")
		args = append(args, program)
	}
	if activity != "" {
		filters = append(filters, "task_id = ?")
		args = append(args, activity)
	}
	if platform != "" {
		filters = append(filters, "platform = ?")
		args = append(args, platform)
	}
	whereClause := ""
	if len(filters) > 0 {
		whereClause = "WHERE " + strings.Join(filters, " AND ")
	}

	// Main query with pagination
	query := `
        SELECT user_id, name, email, instagram_handle, tiktok_handle,
            SUM(likes) AS likes,
            SUM(reach) AS reach,
            SUM(comments) AS comments,
            SUM(shares) AS shares,
            SUM(total_sales_attributed) AS total_sales_attributed
        FROM advocacy_campaign_outcomes
        ` + whereClause + `
        GROUP BY user_id, name, email, instagram_handle, tiktok_handle
        ORDER BY ` + sortBy + ` DESC
        LIMIT ? OFFSET ?
    `
	argsWithPagination := append(args, limit, offset)
	var ranked []dtos.AdvocateRankOverview
	if err := config.DB.Raw(query, argsWithPagination...).Scan(&ranked).Error; err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": "Failed to rank advocates",
		})
	}

	// Count total unique advocates for pagination
	countQuery := `
        SELECT COUNT(*) FROM (
            SELECT user_id
            FROM advocacy_campaign_outcomes
            ` + whereClause + `
            GROUP BY user_id
        ) AS sub
    `
	var total int64
	if err := config.DB.Raw(countQuery, args...).Scan(&total).Error; err != nil {
		return c.Status(fiber.StatusInternalServerError).JSON(fiber.Map{
			"error": "Failed to count advocates",
		})
	}

	return c.JSON(fiber.Map{
		"data":  ranked,
		"page":  page,
		"limit": limit,
		"total": total,
	})
}
