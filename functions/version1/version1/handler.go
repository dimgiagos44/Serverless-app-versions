package function

import (
	//"fmt"
	"encoding/json"
	faasflow "github.com/faasflow/lib/openfaas"
	"log"
)

// Define provide definition of the workflow
func Define(flow *faasflow.Workflow, context *faasflow.Context) (err error) {
	/*dag := flow.Dag()
	dag.Node("start-node").Apply("framer")
	dag.Node("after-start-node").Modify(func(data []byte) ([]byte, error) {
		str := string(data) + " hello!"
		log.Print(str)
		return []byte(str), nil
	})
	dag.Edge("start-node", "after-start-node")
	return nil*/
	dag := flow.Dag()
	dag.Node("start-node").Apply("framer").Modify(func(data []byte) ([]byte, error) {
		str := string(data)
		log.Print("Start-node: ", str)
		return data, nil
	})
	foreachDag := dag.ForEachBranch(
		"F",
		func(data []byte) map[string][]byte {
			//for each returned key in the hashmap a new branch will be executed
			//this function executes in the runtime of foreach F
			type FramerResponse struct {
				OutputBucket  string   `json:"output_bucket"`
				FrameNames    []string `json:"frame_names"`
				FrameNumber   int      `json:"frame_number"`
				RequestStatus bool     `json:"request_status"`
			}
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
			//aggregate all dynamic branches results
			type FaceDetectorResponse struct {
				FaceExists bool   `json:"faceExists"`
				Key        string `json:"key"`
			}
			type FaceDetectorResults struct {
				Results []FaceDetectorResponse
			}
			var responses []FaceDetectorResponse
			var results2 FaceDetectorResults
			for _, data := range results {
				var resp FaceDetectorResponse
				json.Unmarshal(data, &resp)
				responses = append(responses, resp)
			}
			results2.Results = responses
			results3, _ := json.Marshal(results2)
			return results3, nil
		}),
	)
	foreachDag.Node("foreach-node1").Apply("facedetector").Modify(func(data []byte) ([]byte, error) {
		log.Print("Result from facedetector: ", string(data))
		return data, nil
	})
	dag.Node("second-node").Modify(func(data []byte) ([]byte, error) {
		log.Print("Invoking second-node")
		log.Print(string(data))
		return data, nil
	})
	foreachDag2 := dag.ForEachBranch(
		"F2",
		func(data []byte) map[string][]byte {
			//for each returned key in the hashmap a new branch will be executed
			//this function executes in the runtime of foreach F
			type FaceDetectorResponse struct {
				FaceExists bool   `json:"faceExists"`
				Key        string `json:"key"`
			}
			type FaceDetectorResults struct {
				Results []FaceDetectorResponse
			}
			var data2 FaceDetectorResults
			json.Unmarshal(data, &data2)
			results := make(map[string][]byte)
			for _, item := range data2.Results {
				str := `{"input-bucket": "image-output", "key": "` + item.Key + `"}`
				results[item.Key] = []byte(str)
			}
			return results
		},
		faasflow.Aggregator(func(results map[string][]byte) ([]byte, error) {
			//aggregate all dynamic branches results
			result := ""
			for option, data := range results {
				result = result + " " + option + "=" + string(data)
			}
			return []byte(result), nil
		}),
	)
	foreachDag2.Node("foreach-node2").Apply("mobilenet").Modify(func(data []byte) ([]byte, error) {
		log.Print("foreach-node2 = ", string(data))
		return data, nil
	})
	dag.Node("final-node").Modify(func(data []byte) ([]byte, error) {
		log.Print("FINAL DATA = ", string(data))
		return data, nil
	})
	dag.Edge("start-node", "F")
	dag.Edge("F", "second-node")
	dag.Edge("second-node", "F2")
	dag.Edge("F2", "final-node")
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
