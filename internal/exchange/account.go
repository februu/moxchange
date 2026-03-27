package exchange

import "github.com/shopspring/decimal"

type Account struct {
	ID              string
	Balance         decimal.Decimal // cash balance
	Equity          decimal.Decimal // balance + unrealizedPnL
	MarginUsed      decimal.Decimal // initial margin locked
	MarginFree      decimal.Decimal // equity - marginUsed
	RealizedPnL     decimal.Decimal
	UnrealizedPnL   decimal.Decimal
	PositionHistory []Position
}
