package exchange

import (
	"fmt"

	"github.com/shopspring/decimal"
)

type Side string

const (
	SideBuy  Side = "buy"
	SideSell Side = "sell"
)

type OrderType string

const (
	OrderTypeLimit  OrderType = "limit"
	OrderTypeMarket OrderType = "market"
)

// Order represents an order on an exchange.
type Order struct {
	Timestamp   int64
	AccountID   string
	Type        OrderType
	Side        Side
	Price       decimal.Decimal
	Quantity    decimal.Decimal
	StopLevel   decimal.Decimal
	ProfitLevel decimal.Decimal
}

// Validate validates the order against the current kline and account.
// Before calling this, if the order is a market order, its price should be set to the current kline close.
func (o *Order) Validate(currentKline Kline, account Account) error {

	if o.Side != SideBuy && o.Side != SideSell {
		return fmt.Errorf("invalid side: %s", o.Side)
	}
	if o.Type != OrderTypeLimit && o.Type != OrderTypeMarket {
		return fmt.Errorf("invalid order type: %s", o.Type)
	}

	if o.AccountID != account.ID {
		return fmt.Errorf("order account ID does not match account ID")
	}

	if o.Type == OrderTypeLimit && o.Price.LessThanOrEqual(decimal.NewFromInt(0)) {
		return fmt.Errorf("price must be greater than 0")
	}

	if o.Quantity.LessThanOrEqual(decimal.NewFromInt(0)) {
		return fmt.Errorf("quantity must be greater than 0")
	}

	switch o.Side {
	case SideBuy:
		if o.Type == OrderTypeLimit && o.Price.GreaterThanOrEqual(currentKline.Close) {
			return fmt.Errorf("price must be less than current close for buy limit orders")
		}
		if !o.StopLevel.IsZero() && o.StopLevel.GreaterThanOrEqual(o.Price) {
			return fmt.Errorf("stop level must be less than price for buy orders")
		}
		if !o.ProfitLevel.IsZero() && o.ProfitLevel.LessThanOrEqual(o.Price) {
			return fmt.Errorf("profit level must be greater than price for buy orders")
		}
	case SideSell:
		if o.Type == OrderTypeLimit && o.Price.LessThanOrEqual(currentKline.Close) {
			return fmt.Errorf("price must be greater than current close for sell limit orders")
		}
		if !o.StopLevel.IsZero() && o.StopLevel.LessThanOrEqual(o.Price) {
			return fmt.Errorf("stop level must be greater than price for sell orders")
		}
		if !o.ProfitLevel.IsZero() && o.ProfitLevel.GreaterThanOrEqual(o.Price) {
			return fmt.Errorf("profit level must be less than price for sell orders")
		}
	}

	return nil
}
