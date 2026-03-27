package exchange

import "github.com/shopspring/decimal"

type Position struct {
	ID            uint64
	AccountID     string
	Side          Side
	Quantity      decimal.Decimal
	EntryPrice    decimal.Decimal
	MarkPrice     decimal.Decimal
	RealizedPnL   decimal.Decimal
	UnrealizedPnL decimal.Decimal
	Fees          decimal.Decimal
	MarginUsed    decimal.Decimal // initial margin locked for this position
	Leverage      decimal.Decimal // per-position leverage if supported
	StopLevel     decimal.Decimal
	TakeProfit    decimal.Decimal
	Status        string // open/closed/liquidated
	OpenedAt      string
	ClosedAt      string
}
