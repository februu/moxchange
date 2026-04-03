package exchange

import (
	"fmt"

	"github.com/shopspring/decimal"
)

// Kline represents a single candle.
type Kline struct {
	Timestamp string
	Open      decimal.Decimal
	High      decimal.Decimal
	Low       decimal.Decimal
	Close     decimal.Decimal
	Volume    decimal.Decimal
}

func NewKline(timestamp string, open, high, low, close, volume decimal.Decimal) (Kline, error) {

	if !open.IsPositive() || !high.IsPositive() || !low.IsPositive() || !close.IsPositive() {
		return Kline{}, fmt.Errorf("invalid kline: open=%s high=%s low=%s close=%s volume=%s, ohlc values must be positive", open, high, low, close, volume)
	}

	if high.LessThan(low) {
		return Kline{}, fmt.Errorf("invalid kline: high=%s low=%s, high must be greater than low", high, low)
	}

	if open.GreaterThan(high) || open.LessThan(close) {
		return Kline{}, fmt.Errorf("invalid kline: open=%s high=%s low=%s close=%s, open must be less than high and greater than close", open, high, low, close)
	}

	if close.GreaterThan(high) || close.LessThan(low) {
		return Kline{}, fmt.Errorf("invalid kline: close=%s high=%s low=%s, close must be less than high and greater than low", close, high, low)
	}

	return Kline{
		Timestamp: timestamp,
		Open:      open,
		High:      high,
		Low:       low,
		Close:     close,
		Volume:    volume,
	}, nil
}

func NewKlineFromCSV(row []string) (Kline, error) {
	if len(row) < 6 {
		return Kline{}, fmt.Errorf("invalid row length: got %d", len(row))
	}

	open, err := decimal.NewFromString(row[1])
	if err != nil {
		return Kline{}, fmt.Errorf("invalid open '%s': %w", row[1], err)
	}

	high, err := decimal.NewFromString(row[2])
	if err != nil {
		return Kline{}, fmt.Errorf("invalid high '%s': %w", row[2], err)
	}

	low, err := decimal.NewFromString(row[3])
	if err != nil {
		return Kline{}, fmt.Errorf("invalid low '%s': %w", row[3], err)
	}

	close, err := decimal.NewFromString(row[4])
	if err != nil {
		return Kline{}, fmt.Errorf("invalid close '%s': %w", row[4], err)
	}

	volume, err := decimal.NewFromString(row[5])
	if err != nil {
		return Kline{}, fmt.Errorf("invalid volume '%s': %w", row[5], err)
	}

	return NewKline(row[0], open, high, low, close, volume)
}

func (k *Kline) Contains(price decimal.Decimal) bool {
	return price.GreaterThanOrEqual(k.Low) && price.LessThanOrEqual(k.High)
}

func (k *Kline) IsBullish() bool {
	return k.Close.GreaterThan(k.Open)
}

func (k *Kline) IsBearish() bool {
	return k.Close.LessThan(k.Open)
}
