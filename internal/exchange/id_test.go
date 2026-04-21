package exchange

import "testing"

func TestNextID(t *testing.T) {
	ids := make(map[uint64]bool, 1000000)
	for i := 0; i < 1000000; i++ {
		id := nextID()
		if ids[id] {
			t.Errorf("Duplicate ID generated: %d", id)
		}
		ids[id] = true
	}
}
