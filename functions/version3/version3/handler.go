package function

import (
	//"fmt"
	"encoding/json"
	faasflow "github.com/faasflow/lib/openfaas"
	"log"
	"strconv"
	"time"
)

type FramerResponse struct {
	OutputBucket  string   `json:"output_bucket"`
	FrameNames    []string `json:"frame_names"`
	FrameNumber   int      `json:"frame_number"`
	RequestStatus bool     `json:"request_status"`
}

type Output struct {
	Preds  []string `json:"predictions"`
	Bucket string   `json:"bucket"`
	KeyKey string   `json:"key"`
	FaceEx string   `json:"faceExists"`
}

type OutputWrapper struct {
	Data []Output
}

// Define provide definition of the workflow
func Define(flow *faasflow.Workflow, context *faasflow.Context) (err error) {
	dag := flow.Dag()
	start := time.Now()
	dag.Node("start-node").Modify(func(data []byte) ([]byte, error) {
		//time1 := time.Now()
		time1 := time.Since(start)
		//log.Println("Before Framer: ", string(time1.Format("15:04:05.000000000")))
		log.Println("Before framer: ", time1)
		return data, nil
	}).Apply("framer").Modify(func(data []byte) ([]byte, error) {
		log.Println("Framer Result: ", string(data))
		//time2 := time.Now()
		time2 := time.Since(start)
		log.Println("After framer: ", time2)
		//log.Println("After Framer: ", string(time2.Format("15:04:05.000000000")))
		return data, nil
	})
	foreachDag := dag.ForEachBranch(
		"F",
		func(data []byte) map[string][]byte {
			var data2 FramerResponse
			json.Unmarshal(data, &data2)
			results := make(map[string][]byte)
			for i := 0; i < len(data2.FrameNames); i++ {
				str := `{"input-bucket": "image-output", "key": "` + data2.FrameNames[i] + `"}`
				results[data2.FrameNames[i]] = []byte(str)
			}
			return results
		},
		faasflow.Aggregator(func(results map[string][]byte) ([]byte, error) {
			var results2 OutputWrapper
			for _, data := range results {
				var output Output
				json.Unmarshal(data, &output)
				results2.Data = append(results2.Data, output)
			}
			results2Byte, _ := json.Marshal(results2)
			log.Println("Aggregated results after biginference: ", string(results2Byte))
			time3 := time.Since(start)
			log.Println("After biginference: ", time3)
			return results2Byte, nil
		}),
	)
	foreachDag.Node("foreach-node1").Apply("biginference").Modify(func(data []byte) ([]byte, error) {
		return data, nil
	})
	dag.Node("final-node", faasflow.Aggregator(func(results map[string][]byte) ([]byte, error) {
		result := ""
		for _, data := range results {
			result = result + string(data)
		}
		elapsed := time.Since(start)
		elapsedFloat := float64(elapsed)
		elapsedStr := strconv.FormatFloat(elapsedFloat, 'g', -1, 64)
		result = result + " TotalTime=" + elapsedStr
		//time3 := time.Now()
		//log.Println("After biginference: ", string(time3.Format("15:04:05.000000000")))
		return []byte(result), nil
	})).Modify(func(data []byte) ([]byte, error) {
		log.Println("Invoking Final Node")
		log.Println("End data: ", string(data))
		return data, nil
	}).Apply("outputer").Modify(func(data []byte) ([]byte, error) {
		elapsed2 := time.Since(start)
		log.Println("Version3 took: ", elapsed2)
		return data, nil
	})
	dag.Edge("start-node", "F")
	dag.Edge("F", "final-node")
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
