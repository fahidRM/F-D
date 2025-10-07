package dtos

type ProgramOverview struct {
	ProgramID string `json:"program_id"`
	Brand     string `json:"brand"`
}

type PlatformOverview struct {
	Platform string `json:"platform"`
}

type AdvocateOverview struct {
	ID              string `json:"id"`
	Name            string `json:"name"`
	Email           string `json:"email"`
	InstagramHandle string `json:"instagram_handle"`
	TiktokHandle    string `json:"tiktok_handle"`
}

type AdvocateRankOverview struct {
	UserID               string  `json:"user_id"`
	Name                 string  `json:"name"`
	Email                string  `json:"email"`
	InstagramHandle      string  `json:"instagram_handle"`
	TiktokHandle         string  `json:"tiktok_handle"`
	Likes                int64   `json:"likes"`
	Reach                int64   `json:"reach"`
	Comments             int64   `json:"comments"`
	Shares               int64   `json:"shares"`
	TotalSalesAttributed float64 `json:"total_sales_attributed"`
}

type PlatformStats struct {
	Platform             string  `json:"platform"`
	Activities           int64   `json:"activities"`
	TotalLikes           int64   `json:"total_likes"`
	TotalComments        int64   `json:"total_comments"`
	TotalReach           int64   `json:"total_reach"`
	TotalShares          int64   `json:"total_shares"`
	TotalSalesAttributed float64 `json:"total_sales_attributed"`
}

type ProgramStats struct {
	ProgramID            string  `json:"program_id"`
	Brand                string  `json:"brand"`
	TotalLikes           int64   `json:"total_likes"`
	TotalComments        int64   `json:"total_comments"`
	TotalReach           int64   `json:"total_reach"`
	TotalShares          int64   `json:"total_shares"`
	TotalSalesAttributed float64 `json:"total_sales_attributed"`
}

type ProgramActivityStats struct {
	ProgramID            string  `json:"program_id"`
	Brand                string  `json:"brand"`
	ActivityID           string  `json:"activity_id"`
	TotalLikes           int64   `json:"total_likes"`
	TotalComments        int64   `json:"total_comments"`
	TotalReach           int64   `json:"total_reach"`
	TotalShares          int64   `json:"total_shares"`
	TotalSalesAttributed float64 `json:"total_sales_attributed"`
}

type UserPlatformStats struct {
	Platform             string  `json:"platform"`
	TotalLikes           int64   `json:"total_likes"`
	TotalComments        int64   `json:"total_comments"`
	TotalReach           int64   `json:"total_reach"`
	TotalShares          int64   `json:"total_shares"`
	TotalSalesAttributed float64 `json:"total_sales_attributed"`
}

type UserProgramStats struct {
	ProgramID            string  `json:"program_id"`
	Brand                string  `json:"brand"`
	TotalLikes           int64   `json:"total_likes"`
	TotalComments        int64   `json:"total_comments"`
	TotalReach           int64   `json:"total_reach"`
	TotalShares          int64   `json:"total_shares"`
	TotalSalesAttributed float64 `json:"total_sales_attributed"`
}

type OverviewStats struct {
	ProgramsCount        int64   `json:"programs_count"`
	ActivitiesCount      int64   `json:"activities_count"`
	PlatformsCount       int64   `json:"platforms_count"`
	BrandsCount          int64   `json:"brands"`
	TotalComments        int64   `json:"total_comments"`
	TotalLikes           int64   `json:"total_likes"`
	TotalReach           int64   `json:"total_reach"`
	TotalShares          int64   `json:"total_shares"`
	TotalSalesAttributed float64 `json:"total_sales_attributed"`
}

type OverviewSums struct {
	Likes                int64   `json:"total_likes"`
	Reach                int64   `json:"total_reach"`
	Shares               int64   `json:"total_shares"`
	TotalSalesAttributed float64 `json:"total_sales_attributed"`
}
