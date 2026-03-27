package exchange

import (
	"fmt"

	"github.com/shopspring/decimal"
)

type DataSource interface {
	Next() ([]string, error)
}

type Exchange struct {
	dataSource   DataSource
	slippage     decimal.Decimal
	feeRate      decimal.Decimal
	Accounts     map[string]*Account
	ActiveOrders map[uint64]Order
	Positions    map[uint64]Position
	lastKline    Kline
}

func NewExchange(ds DataSource, slippage, feeRate decimal.Decimal) *Exchange {
	return &Exchange{
		dataSource:   ds,
		slippage:     slippage,
		feeRate:      feeRate,
		Accounts:     make(map[string]*Account),
		ActiveOrders: make(map[uint64]Order),
		lastKline:    Kline{},
	}
}

func (e *Exchange) Step() []error {
	var errors []error
	if _, err := e.nextKline(); err != nil {
		errors = append(errors, err)
		return errors
	}
	errors = append(errors, e.executeActiveOrders()...)
	errors = append(errors, e.updatePositions()...)
	errors = append(errors, e.updateAccounts()...)
	return errors
}

func (e *Exchange) nextKline() (Kline, error) {
	record, err := e.dataSource.Next()
	if err != nil {
		return Kline{}, err
	}
	kline, err := NewKlineFromCSV(record)
	if err != nil {
		return Kline{}, err
	}
	e.lastKline = kline
	return kline, nil
}

func (e *Exchange) PlaceOrder(order Order) (id uint64, err error) {
	if order.Type == OrderTypeMarket {
		order.Price = e.lastKline.Close
	}

	// FIXME: Validate doesnt make sense now. It checks for type validity but we assume that the type is correct in the check above.
	// Also, we pass the account using account ID which we should validate against the accounts slice in the exchange.
	if err := order.Validate(e.lastKline, *e.Accounts[order.AccountID]); err != nil {
		return 0, err
	}

	id = nextID()
	e.ActiveOrders[id] = order
	return id, nil
}

func (e *Exchange) GetOrder(id uint64, accountID string) (Order, error) {
	order, ok := e.ActiveOrders[id]
	if !ok {
		return Order{}, fmt.Errorf("order %d not found", id)
	}
	if order.AccountID != accountID {
		return Order{}, fmt.Errorf("order %d does not belong to account %s", id, accountID)
	}
	return order, nil
}

func (e *Exchange) CancelOrder(id uint64, accountID string) error {
	if _, ok := e.ActiveOrders[id]; !ok {
		return fmt.Errorf("order %d not found", id)
	}
	if e.ActiveOrders[id].AccountID != accountID {
		return fmt.Errorf("order %d does not belong to account %s", id, accountID)
	}
	delete(e.ActiveOrders, id)
	return nil
}

func (e *Exchange) GetPosition(id uint64, accountID string) (Position, error) {
	var pos Position
	pos, ok := e.Positions[id]
	if !ok {
		return Position{}, fmt.Errorf("position %d not found", id)
	}
	if pos.AccountID != accountID {
		return Position{}, fmt.Errorf("position %d does not belong to account %s", id, accountID)
	}
	return pos, nil
}

func (e *Exchange) ClosePosition(id uint64, accountID string) error {
	if _, ok := e.Positions[id]; !ok {
		return fmt.Errorf("position %d not found", id)
	}
	if e.Positions[id].AccountID != accountID {
		return fmt.Errorf("position %d does not belong to account %s", id, accountID)
	}
	// TODO: Close position
	delete(e.Positions, id)
	return nil
}

func (e *Exchange) executeActiveOrders() []error {
	errors := []error{}

	for id, order := range e.ActiveOrders {
		if !e.lastKline.Contains(order.Price) {
			continue
		}
		if err := e.executeOrder(order); err != nil {
			errors = append(errors, err)
		}
		delete(e.ActiveOrders, id)
	}

	return errors
}

func (e *Exchange) executeOrder(order Order) error {
	// TODO: Add checks
	position := Position{
		ID:            nextID(),
		AccountID:     order.AccountID,
		Side:          order.Side,
		Quantity:      order.Quantity,
		EntryPrice:    order.Price,
		MarkPrice:     e.lastKline.Close,
		RealizedPnL:   decimal.Zero,
		UnrealizedPnL: decimal.Zero,
		Fees:          decimal.Zero,
		MarginUsed:    decimal.Zero,
		Leverage:      decimal.Zero,
		StopLevel:     order.StopLevel,
		TakeProfit:    order.ProfitLevel,
		Status:        "open",
		OpenedAt:      e.lastKline.Timestamp,
		ClosedAt:      "",
	}

	e.Positions[position.ID] = position
	return nil
}

func (e *Exchange) updatePositions() []error {
	var errors []error
	for _, position := range e.Positions {
		// position.MarkPrice = e.lastKline.Close
		// TODO: Update position
		//
		if e.lastKline.Contains(position.StopLevel) {
			// Close position with loss
			position.Status = "closed"
			position.ClosedAt = e.lastKline.Timestamp
			e.Accounts[position.AccountID].PositionHistory = append(e.Accounts[position.AccountID].PositionHistory, position)
			delete(e.Positions, position.ID)
			continue
		}
		if e.lastKline.Contains(position.TakeProfit) {
			// Close position with profit
			position.Status = "closed"
			position.ClosedAt = e.lastKline.Timestamp
			e.Accounts[position.AccountID].PositionHistory = append(e.Accounts[position.AccountID].PositionHistory, position)
			delete(e.Positions, position.ID)
			continue
		}
		e.Positions[position.ID] = position
	}
	return errors
}

func (e *Exchange) updateAccounts() []error {
	var errors []error
	for _, account := range e.Accounts {
		// TODO: Update account
		account.Equity = account.Balance.Add(account.UnrealizedPnL)
	}
	return errors
}
