package function

import (
	//"fmt"
	//"encoding/json"
	faasflow "github.com/faasflow/lib/openfaas"
	"log"
	"strconv"
	"time"
)

// Define provide definition of the workflow
func Define(flow *faasflow.Workflow, context *faasflow.Context) (err error) {
	dag := flow.Dag()
	start := time.Now()
	dag.Node("start-node").Apply("monolith").Modify(func(data []byte) ([]byte, error) {
		log.Println("Monolith result: ", string(data))
		return data, nil
	})
	dag.Node("final-node").Modify(func(data []byte) ([]byte, error) {
		result := ""
		result = result + string(data)
		elapsed := time.Since(start)
		elapsedFloat := float64(elapsed)
		elapsedStr := strconv.FormatFloat(elapsedFloat, 'g', -1, 64)
		result = result + " TotalTime=" + elapsedStr
		log.Println("End data: ", result)
		return []byte(result), nil
	}).Apply("outputer").Modify(func(data []byte) ([]byte, error) {
		elapsed2 := time.Since(start)
		log.Println("Version4 took: ", elapsed2)
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
