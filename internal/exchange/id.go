package exchange

import "sync/atomic"

var idCounter uint64 = 1

// nextID returns the next unique ID.
func nextID() uint64 {
	return atomic.AddUint64(&idCounter, 1)
}
