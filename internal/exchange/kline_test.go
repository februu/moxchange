package exchange

import (
	"testing"

	"github.com/shopspring/decimal"
)

func TestNewKline(t *testing.T) {
	tests := []struct {
		open  decimal.Decimal
		high  decimal.Decimal
		low   decimal.Decimal
		close decimal.Decimal
		valid bool
	}{
		{decimal.NewFromInt(100), decimal.NewFromInt(200), decimal.NewFromInt(50), decimal.NewFromInt(80), true},
		{decimal.NewFromInt(100), decimal.NewFromInt(-100), decimal.NewFromInt(50), decimal.NewFromInt(80), false},  // negative high
		{decimal.NewFromInt(100), decimal.NewFromInt(100), decimal.NewFromInt(120), decimal.NewFromInt(100), false}, // low > high
		{decimal.NewFromInt(300), decimal.NewFromInt(200), decimal.NewFromInt(50), decimal.NewFromInt(80), false},   // open > high
		{decimal.NewFromInt(20), decimal.NewFromInt(200), decimal.NewFromInt(50), decimal.NewFromInt(80), false},    // open < low
		{decimal.NewFromInt(100), decimal.NewFromInt(200), decimal.NewFromInt(50), decimal.NewFromInt(300), false},  // close > high
		{decimal.NewFromInt(100), decimal.NewFromInt(200), decimal.NewFromInt(50), decimal.NewFromInt(20), false},   // close < low
	}

	for _, tt := range tests {
		kline, err := NewKline("", tt.open, tt.high, tt.low, tt.close, decimal.NewFromInt(1))
		if err != nil {
			if tt.valid {
				t.Errorf("NewKline() error = %v, want nil", err)
			}
			continue
		}
		if !tt.valid {
			t.Errorf("NewKline() = %v, want error", kline)
		}
	}
}

func TestNewKlineFromCSV(t *testing.T) {
	tests := []struct {
		values []string
		valid  bool
	}{
		{[]string{"1775253816", "100", "200", "50", "80", "70"}, true},
		{[]string{"2026-04-03T22:03:36+00:00", "100", "200", "50", "80"}, false},                    // no volume
		{[]string{"100", "200", "50", "80", "70"}, false},                                           // no timestamp
		{[]string{"Friday, 03-Apr-26 22:03:36 UTC", "100.5235.35", "200", "50", "80", "70"}, false}, // invalid open
		{[]string{"03-04-2026", "100", "42f4", "50", "80", "70"}, false},                            // invalid high
		{[]string{"03-04-2026 22:03", "100", "200", "%f44", "80", "70"}, false},                     // invalid low
		{[]string{"04-03-2026 22:03:36", "100", "200", "50", "34943b", "70"}, false},                // invalid close
		{[]string{"04-03-2026 22:03:36", "100", "200", "50", "80", "-32-"}, false},                  // invalid volume
	}

	for _, tt := range tests {
		kline, err := NewKlineFromCSV(tt.values)
		if err != nil {
			if tt.valid {
				t.Errorf("NewKline() error = %v, want nil", err)
			}
			continue
		}
		if !tt.valid {
			t.Errorf("NewKline() = %v, want error", kline)
		}
	}
}

func TestKlineContains(t *testing.T) {
	kline, err := NewKline("", decimal.NewFromInt(100), decimal.NewFromInt(200), decimal.NewFromInt(50), decimal.NewFromInt(80), decimal.NewFromInt(1))
	if err != nil {
		t.Errorf("NewKline() error = %v, want nil", err)
	}
	if !kline.Contains(decimal.NewFromInt(70.0)) {
		t.Errorf("kline.Contains() = false, want true")
	}
}

func TestKlineIsBullish(t *testing.T) {
	kline, err := NewKline("", decimal.NewFromInt(100), decimal.NewFromInt(200), decimal.NewFromInt(50), decimal.NewFromInt(80), decimal.NewFromInt(1))
	if err != nil {
		t.Errorf("NewKline() error = %v, want nil", err)
	}
	if kline.IsBullish() {
		t.Errorf("kline.IsBullish() = true, want false")
	}
}

func TestKlineIsBearish(t *testing.T) {
	kline, err := NewKline("", decimal.NewFromInt(100), decimal.NewFromInt(200), decimal.NewFromInt(50), decimal.NewFromInt(80), decimal.NewFromInt(1))
	if err != nil {
		t.Errorf("NewKline() error = %v, want nil", err)
	}
	if !kline.IsBearish() {
		t.Errorf("kline.IsBearish() = false, want true")
	}
}
