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
			result := ""
			for option, data := range results {
				result = result + " " + option + "=" + string(data)
			}
			return []byte(result), nil
		}),
	)
	foreachDag.Node("node1").Apply("facedetector").Modify(func(data []byte) ([]byte, error) {
		log.Print("Invoking node1 for-each")
		return data, nil
	})
	dag.Node("end-node").Modify(func(data []byte) ([]byte, error) {
		log.Print("Invoking End-Node")
		log.Print(string(data))
		return data, nil
	})
	dag.Edge("start-node", "F")
	dag.Edge("F", "end-node")
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
