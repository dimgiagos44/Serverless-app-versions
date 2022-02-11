package function

import (
	//"fmt"
	"encoding/json"
	faasflow "github.com/faasflow/lib/openfaas"
	"log"
	"strconv"
	"sync"
	"sync/atomic"
	"time"
)

type Output struct {
	Preds  []string `json:"predictions"`
	Bucket string   `json:"bucket"`
	KeyKey string   `json:"key"`
}

type OutputWrapper struct {
	Data []Output
}

type FramerResponse struct {
	OutputBucket  string   `json:"output_bucket"`
	FrameNames    []string `json:"frame_names"`
	FrameNumber   int      `json:"frame_number"`
	RequestStatus bool     `json:"request_status"`
}

type FaceDetectorResponse struct {
	FaceExists bool   `json:"faceExists"`
	Key        string `json:"key"`
}

type FaceDetectorResults struct {
	Results []FaceDetectorResponse
}

type CondInput struct {
	InputBucket string `json:"input-bucket"`
	Key         string `json:"key"`
	FaceExists  string `json:"faceExists"`
}

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

var (
	nowFramer      time.Duration
	calcFramerOnce Once
)

func GetFramer(start time.Time) time.Duration {
	calcFramerOnce.Do(func() {
		nowFramer = time.Since(start)
	})
	return nowFramer
}

func resetFramer() {
	calcFramerOnce.Reset()
	return
}

var (
	nowFace      time.Duration
	calcFaceOnce Once
)

func GetFace(start time.Time) time.Duration {
	calcFaceOnce.Do(func() {
		nowFace = time.Since(start)
	})
	return nowFace
}

func resetFace() {
	calcFaceOnce.Reset()
	return
}

var (
	nowInf      time.Duration
	calcInfOnce Once
)

func GetInf(start time.Time) time.Duration {
	calcInfOnce.Do(func() {
		nowInf = time.Since(start)
	})
	return nowInf
}

func resetInf() {
	calcInfOnce.Reset()
	return
}

// Define provide definition of the workflow
func Define(flow *faasflow.Workflow, context *faasflow.Context) (err error) {
	dag := flow.Dag()
	start := GetTotal()
	dag.Node("start-node").Modify(func(data []byte) ([]byte, error) {
		return data, nil
	}).Apply("framer").Modify(func(data []byte) ([]byte, error) {
		log.Println("Framer Result: ", string(data))
		nowFramer := GetFramer(start)
		log.Println("AFTER-FRAMER: ", nowFramer)
		resetFramer()
		return data, nil
	})
	foreachDag := dag.ForEachBranch(
		"F",
		func(data []byte) map[string][]byte {
			//for each returned key in the hashmap a new branch will be executed
			//this function executes in the runtime of foreach F
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
			var responses []FaceDetectorResponse
			var results2 FaceDetectorResults
			for _, data := range results {
				var resp FaceDetectorResponse
				json.Unmarshal(data, &resp)
				responses = append(responses, resp)
			}
			results2.Results = responses
			results2Byte, _ := json.Marshal(results2)
			return results2Byte, nil
		}),
	)
	foreachDag.Node("foreach-node1").Apply("facedetector").Modify(func(data []byte) ([]byte, error) {
		//log.Print("Result from facedetector: ", string(data))
		return data, nil
	})
	dag.Node("second-node").Modify(func(data []byte) ([]byte, error) {
		log.Println("Facedetector results (Aggregated): ", string(data))
		nowFace := GetFace(start)
		log.Println("AFTER-FACE: ", nowFace)
		resetFace()
		return data, nil
	})
	foreachDag2 := dag.ForEachBranch(
		"F2",
		func(data []byte) map[string][]byte {
			//for each returned key in the hashmap a new branch will be executed
			//this function executes in the runtime of foreach F2
			var data2 FaceDetectorResults
			json.Unmarshal(data, &data2)
			results := make(map[string][]byte)
			for _, item := range data2.Results {
				str := `{"input-bucket": "image-output", "key": "` + item.Key + `", "faceExists": "` + strconv.FormatBool(item.FaceExists) + `"}`
				results[item.Key] = []byte(str)
			}
			return results
		},
		faasflow.Aggregator(func(results map[string][]byte) ([]byte, error) {
			//aggregate all dynamic branches results
			var results2 []OutputWrapper
			for _, data := range results {
				var output OutputWrapper
				json.Unmarshal(data, &output)
				results2 = append(results2, output)
			}
			results2Byte, _ := json.Marshal(results2)
			log.Println("Aggregated results after conditionals: ", string(results2Byte))
			nowInf := GetInf(start)
			log.Println("AFTER-INF: ", nowInf)
			resetInf()
			return results2Byte, nil
		}),
	)
	conditionalDags := foreachDag2.ConditionalBranch(
		"C",
		[]string{"true", "false"}, //possible conditions
		func(response []byte) []string {
			//function that determine the status
			var condInput CondInput
			json.Unmarshal(response, &condInput)
			return []string{condInput.FaceExists}
		},
		faasflow.Aggregator(func(results map[string][]byte) ([]byte, error) {
			// results can be aggregated accross the branches
			var results2 OutputWrapper
			for _, data := range results {
				var output Output
				json.Unmarshal(data, &output)
				results2.Data = append(results2.Data, output)
			}
			results2Byte, _ := json.Marshal(results2)
			log.Println("InferenceResult = ", string(results2Byte))
			return results2Byte, nil
		}),
	)
	conditionalDags["true"].Node("true-node").Apply("faceanalyzer").Modify(func(data []byte) ([]byte, error) {
		log.Println("trueFaceanalyzerNode: ", string(data))
		return data, nil
	})
	conditionalDags["false"].Node("false-node").Apply("mobilenet").Modify(func(data []byte) ([]byte, error) {
		log.Println("falseMobilenetNode: ", string(data))
		return data, nil
	})
	foreachDag2.Node("foreach-node2").Modify(func(data []byte) ([]byte, error) {
		return data, nil
	})
	foreachDag2.Edge("foreach-node2", "C")
	dag.Node("final-node", faasflow.Aggregator(func(results map[string][]byte) ([]byte, error) {
		result := ""
		for _, data := range results {
			result = result + string(data)
		}
		return []byte(result), nil
	})).Modify(func(data []byte) ([]byte, error) {
		log.Println("Invoking Final Node")
		log.Println("End data: ", string(data))
		return data, nil
	}).Apply("outputer").Modify(func(data []byte) ([]byte, error) {
		end := time.Since(start)
		reset()
		log.Println("Version1b took: ", end)
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
