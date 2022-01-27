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
	dag.Node("start-node").Modify(func(data []byte) ([]byte, error) {
		//time1 := time.Now()
		//log.Println("Before monolith: ", string(time1.Format("15:04:05.000000000")))
		time1 := time.Since(start)
		log.Println("Before monolith: ", time1)
		return data, nil
	}).Apply("monolith").Modify(func(data []byte) ([]byte, error) {
		log.Println("Monolith result: ", string(data))
		time2 := time.Since(start)
		log.Println("After monolith: ", time2)
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
		log.Println("Version4b took: ", elapsed2)
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
