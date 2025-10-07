package models

import (
	"github.com/google/uuid"
	"gorm.io/gorm"
	"time"
)

type AdvocacyCampaignOutcome struct {
	gorm.Model

	ID                   uuid.UUID `gorm:"->;primaryKey;type:uuid;default:uuid_generate_v4()" json:"id"`
	UserID               uuid.UUID `json:"<-;type_uuid;default:uuid_generate_v4(); not null" json:"user_id"`
	Name                 string    `gorm:"<-;type:varchar(255);default null;not null" json:"name"`
	Email                string    `gorm:"<-;type:varchar(255);default null;not null" json:"email"`
	InstagramHandle      string    `gorm:"<-;type:varchar(35);default null;not null" json:"instagram_handle"`
	TiktokHandle         string    `gorm:"<-;type:varchar(35);default null;not null" json:"tiktok_handle"`
	JoinedAt             time.Time `gorm:"<-;default:null;not null" json:"joined_at"`
	ProgramID            uuid.UUID `gorm:"<-;type:uuid;default: null" json:"program_id"`
	Brand                string    `gorm:"<-;type:varchar(255);default null;not null" json:"brand"`
	TaskID               uuid.UUID `gorm:"<-;type:uuid;default:null" json:"task_id"`
	Platform             string    `gorm:"<-;type:varchar(255);default null;" json:"platform"`
	PostUrl              string    `gorm:"<-;type:text;default null;" json:"post_url"`
	Likes                int       `gorm:"<-;type:int;default 0;not null" json:"likes"`
	Comments             int       `gorm:"<-;type:int;default 0;not null" json:"comments"`
	Shares               int       `gorm:"<-;type:int;default 0;not null" json:"shares"`
	Reach                int       `gorm:"<-;type:int;default 0;not null" json:"reach"`
	TotalSalesAttributed float64   `gorm:"<-;type:float;default 0;not null" json:"total_sales_attributed"`
	CreatedAt            time.Time `json:"-"`
	UpdatedAt            time.Time `json:"-"`
}
