package function

import (
	//"fmt"
	//"encoding/json"
	faasflow "github.com/faasflow/lib/openfaas"
	"log"
	"sync"
	"sync/atomic"
	"time"
)

type Once struct {
	m    sync.Mutex
	done uint32
}

func (o *Once) Do(f func()) {
	if atomic.LoadUint32(&o.done) == 1 {
		return
	}
	// Slow-path.
	o.m.Lock()
	defer o.m.Unlock()
	if o.done == 0 {
		defer atomic.StoreUint32(&o.done, 1)
		f()
	}
}

func (o *Once) Reset() {
	o.m.Lock()
	defer o.m.Unlock()
	atomic.StoreUint32(&o.done, 0)
}

var (
	now           time.Time
	calcTotalOnce Once
)

func GetTotal() time.Time {
	// Init / calc total once:
	calcTotalOnce.Do(func() {
		log.Println("Fetching total...")
		// Do some heavy work, make HTTP calls, whatever you want:
		now = time.Now() // This will set total to 1 (once and for all)
	})

	// Here you can safely use total:
	return now
}

func reset() {
	calcTotalOnce.Reset()
	return
}

// Define provide definition of the workflow
func Define(flow *faasflow.Workflow, context *faasflow.Context) (err error) {
	dag := flow.Dag()
	start := GetTotal()
	dag.Node("start-node").Modify(func(data []byte) ([]byte, error) {
		return data, nil
	}).Apply("monolith").Modify(func(data []byte) ([]byte, error) {
		log.Println("Monolith result: ", string(data))
		return data, nil
	})
	dag.Node("final-node").Modify(func(data []byte) ([]byte, error) {
		result := ""
		result = result + string(data)
		log.Println("End data: ", result)
		return []byte(result), nil
	}).Apply("outputer").Modify(func(data []byte) ([]byte, error) {
		end := time.Since(start)
		reset()
		log.Println("Version4b took: ", end)
		return data, nil
	})
	dag.Edge("start-node", "final-node")
	return
}

// OverrideStateStore provides the override of the default StateStore
func OverrideStateStore() (faasflow.StateStore, error) {
	// NOTE: By default FaaS-Flow use consul as a state-store,
	//       This can be overridden with other synchronous KV store (e.g. ETCD)
	return nil, nil
}

// OverrideDataStore provides the override of the default DataStore
func OverrideDataStore() (faasflow.DataStore, error) {
	// NOTE: By default FaaS-Flow use minio as a data-store,
	//       This can be overridden with other synchronous KV store
	return nil, nil
}
