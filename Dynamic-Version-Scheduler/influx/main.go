package main

import (
	"encoding/json"
	"fmt"
	"os"
	"strconv"
	"strings"

	client "github.com/influxdata/influxdb1-client/v2"
	"k8s.io/klog"
)

var isMoving bool = true

/*var NodesToCores = map[string][]int{
	"oracle-ikube-w01": {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15},
	"oracle-ikube-w02": {40, 41, 42, 43, 44, 45, 46, 47},
	"oracle-ikube-w03": {0, 1, 2, 3, 4, 5, 6, 7},
	"oracle-ikube-w04": {0, 1, 2, 3, 4, 5, 6, 7},
}*/
var NodesToCores = map[string][]int{
	"davinci": {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15},
	"davinci2": {40, 41, 42, 43, 44, 45, 46, 47},
	"coroni": {0, 1, 2, 3, 4, 5, 6, 7},
	"liono": {0, 1, 2, 3, 4, 5, 6, 7},
}


type scorerInput struct {
	metricName string
	metrics    map[string]float64
}

type Config struct {
	Server struct {
		Port string `yaml:"port"`
		Host string `yaml:"host"`
	} `yaml:"server"`
	Database struct {
		Type     string `yaml:"type"`
		Name     string `yaml:"name"`
		Username string `yaml:"username"`
		Password string `yaml:"password"`
	} `yaml:"database"`
	MonitoringSpecs struct {
		TimeInterval float32 `yaml:"interval"`
	} `yaml:"monitoring"`
}

func connectToInfluxDB(host, port string) (client.Client, error) {
	c, err := client.NewHTTPClient(client.HTTPConfig{
		Addr: "http://" + host + ":" + port + "",
	})
	if err != nil {
		klog.V(1).Infof("Error while connecting to InfluxDB: %v ", err.Error())
		return nil, err
	}
	klog.V(1).Infof("Connected Successfully to InfluxDB")
	return c, nil

}

func customScoreInfluxDB(metrics []string, uuid string, socket,
	numberOfRows int, c client.Client) (map[string]float64, error) {

	// calculate the number of rows needed
	// i.e. 20sec / 0.5s interval => 40rows
	//numberOfRows := int(float32(time) / cfg.MonitoringSpecs.TimeInterval)
	// merge all the required columns
	columns := strings.Join(metrics, ", ")
	// build the coommand
	var command strings.Builder
	fmt.Fprintf(&command, "SELECT %s from socket_metrics where uuid = '%s' and socket_id='%d' order by time desc limit %d", columns, uuid, socket, numberOfRows)
	//klog.V(1).V(1).Infof("%s", command.String())
	//q := client.NewQuery("select ipc from system_metrics", "evolve", "")
	// fmt.Println(command.String())
	q := client.NewQuery(command.String(), "evolve", "")
	response, err := c.Query(q)
	if err != nil {
		klog.V(1).Infof("Error while executing the query: %v", err.Error())
		return nil, err
	}

	// Calculate the average for the metrics provided
	if isMoving {
		return calculateWeightedAverage(response, numberOfRows, len(metrics))
	}
	return calculateWeightedAverage(response, numberOfRows, len(metrics))

}
func calculateWeightedAverage(response *client.Response,
	numberOfRows, numberOfMetrics int) (map[string]float64, error) {
	// initialize the metrics map with a constant size
	metrics := make(map[string]float64, numberOfMetrics)
	// fmt.Printf("%v", response)
	rows := response.Results[0].Series[0]
	for i := 1; i < len(rows.Columns); i++ {
		for j := 0; j < numberOfRows; j++ {
			// fmt.Println(rows.Values[j][i])
			val, err := rows.Values[j][i].(json.Number).Float64()
			if err != nil {
				klog.V(1).Infof("Error while calculating %v", rows.Columns[i])
				return nil, err
			}
			metrics[rows.Columns[i]] += val * float64(numberOfRows-j)
		}
		metrics[rows.Columns[i]] = metrics[rows.Columns[i]] / float64((numberOfRows * (numberOfRows + 1) / 2))
		//klog.V(1).Infof("%v : %v", rows.Columns[i], metrics[rows.Columns[i]])
	}
	// TODO better handling for the returning errors
	return metrics, nil
}

func calculateAverage(response *client.Response,
	numberOfRows, numberOfMetrics int) (map[string]float64, error) {
	// initialize the metrics map with a constant size
	metrics := make(map[string]float64, numberOfMetrics)
	rows := response.Results[0].Series[0]
	for i := 1; i < len(rows.Columns); i++ {
		for j := 0; j < numberOfRows; j++ {
			val, err := rows.Values[j][i].(json.Number).Float64()
			if err != nil {
				klog.V(1).Infof("Error while calculating %v", rows.Columns[i])
				return nil, err
			}
			metrics[rows.Columns[i]] += val
		}
		metrics[rows.Columns[i]] = metrics[rows.Columns[i]] / float64(numberOfRows)
		//klog.V(1).Infof("%v : %v", rows.Columns[i], metrics[rows.Columns[i]])
	}
	// TODO better handling for the returning errors
	return metrics, nil
}

var results map[string]float64

/*var NameToUuid = map[string]string{
	"oracle-ikube-w01": "9b1b13e5-3eeb-4927-b2b8-9ee3784d89f5",
	"oracle-ikube-w02": "9b1b13e5-3eeb-4927-b2b8-9ee3784d89f5",
	"oracle-ikube-w03": "644b8bc9-4ca9-486b-bbb6-3bda87b8b661",
	"oracle-ikube-w04": "ea9ec204-1e47-4665-b3c7-ccd965a6aeff",
}*/
var NameToUuid = map[string]string{
	"davinci": "9b1b13e5-3eeb-4927-b2b8-9ee3784d89f5",
	"davinci2": "9b1b13e5-3eeb-4927-b2b8-9ee3784d89f5",
	"coroni": "644b8bc9-4ca9-486b-bbb6-3bda87b8b661",
	"liono": "ea9ec204-1e47-4665-b3c7-ccd965a6aeff",
}


// var NameToSocket = map[string]int{
// 	"oracle-ikube-w02": 0,
// 	"oracle-ikube-w03": 0,
// 	"oracle-ikube-w04": "ea9ec204-1e47-4665-b3c7-ccd965a6aeff",
// }
func calculateScore(si scorerInput,
	logicFn func(scorerInput) float64) float64 {

	res := logicFn(si)
	//klog.V(1).Infof("Has score (in float) %v\n", res)

	return res
}
func customScoreFn(si scorerInput) float64 {
	return si.metrics["ipc"] / (si.metrics["mem_read"] + si.metrics["mem_write"])
}

func queryInfluxDbCores(metrics []string, uuid string, socket,
	numberOfRows int, c client.Client, cores []int) (*client.Response, error) {

	// calculate the number of rows needed
	// i.e. 20sec / 0.2s interval => 100rows
	//numberOfRows := int(float32(time) / cfg.MonitoringSpecs.TimeInterval)
	// EDIT
	// This time we will fetch data for multiple cores
	// so we will need more rows, proportional to the core number
	// merge all the required columns
	columns := strings.Join(metrics, ", ")

	// build the cores part of the command
	var coresPart strings.Builder
	fmt.Fprintf(&coresPart, "core_id='%d'", cores[0])
	for i := 1; i < len(cores); i++ {
		fmt.Fprintf(&coresPart, " or core_id='%d'", cores[i])
	}

	// build the coommand
	var command strings.Builder
	fmt.Fprintf(&command, "SELECT %s from core_metrics where uuid = '%s' and socket_id='%d' and (%s) order by time desc limit %d", columns, uuid, socket, coresPart.String(), numberOfRows*len(cores))
	//klog.V(1).Infof("The query is: %v", command.String())
	// fmt.Println(command.String())
	q := client.NewQuery(command.String(), "evolve", "")
	response, err := c.Query(q)
	if err != nil {
		klog.V(1).Infof("Error while executing the query: %v", err.Error())
		return nil, err
	}
	// Calculate the average for the metrics provided
	return response, nil
}

func calculateWeightedAverageCores(response *client.Response,
	numberOfRows, numberOfMetrics, numberOfCores int) (map[string]float64, error) {
	// initialize the metrics map with a constant size
	metrics := make(map[string]float64, numberOfMetrics)
	rows := response.Results[0].Series[0]
	for i := 1; i < len(rows.Columns); i++ {
		//klog.V(1).Infof("Name of column %v : %v\nrange of values: %v\nnumber of rows: %v\nnumber of cores %v\n", i, rows.Columns[i], len(rows.Values), numberOfRows, numberOfCores)
		for j := 0; j < numberOfRows; j++ {
			avg := 0.0
			for k := 0; k < numberOfCores; k++ {
				val, err := rows.Values[j*numberOfCores+k][i].(json.Number).Float64()
				if err != nil {
					klog.V(1).Infof("Error while calculating %v", rows.Columns[i])
					return nil, err
				}
				//metrics[rows.Columns[i]] += val * float64(numberOfRows-j)
				avg += val / float64(numberOfCores)
			}
			metrics[rows.Columns[i]] += avg * float64(numberOfRows-j)
		}
		metrics[rows.Columns[i]] = metrics[rows.Columns[i]] / float64((numberOfRows * (numberOfRows + 1) / 2))
		//klog.V(1).Infof("%v : %v", rows.Columns[i], metrics[rows.Columns[i]])
	}
	// TODO better handling for the returning errors
	return metrics, nil
}

func calculateAverageCores(response *client.Response,
	numberOfRows, numberOfMetrics, numberOfCores int) (map[string]float64, error) {
	// initialize the metrics map with a constant size
	metrics := make(map[string]float64, numberOfMetrics)
	rows := response.Results[0].Series[0]
	for i := 1; i < len(rows.Columns); i++ {
		//klog.V(1).Infof("Name of column %v : %v\nrange of values: %v\nnumber of rows: %v\nnumber of cores %v\n", i, rows.Columns[i], len(rows.Values), numberOfRows, numberOfCores)
		for j := 0; j < numberOfRows; j++ {
			avg := 0.0
			for k := 0; k < numberOfCores; k++ {
				val, err := rows.Values[j*numberOfCores+k][i].(json.Number).Float64()
				if err != nil {
					klog.V(1).Infof("Error while calculating %v", rows.Columns[i])
					return nil, err
				}
				//metrics[rows.Columns[i]] += val * float64(numberOfRows-j)
				avg += val / float64(numberOfCores)
			}
			metrics[rows.Columns[i]] += avg
		}
		metrics[rows.Columns[i]] = metrics[rows.Columns[i]] / float64(numberOfRows)
		//klog.V(1).Infof("%v : %v", rows.Columns[i], metrics[rows.Columns[i]])
	}
	// TODO better handling for the returning errors
	return metrics, nil
}

func main() {
	// InfluxDB 
	c, err := connectToInfluxDB("192.168.1.216", "8086")
	if err != nil {
		//return 0, err
		fmt.Println("Error occurred")
	}
	// close the connection in the end of execution
	defer c.Close()

	// query the last 'time' seconds
	TimeInterval := 1
	var numberOfRows int
	moving := os.Args[2]
	monitoredNode := os.Args[3]
	if moving == "average" {
		isMoving = false
	}

	if time, err := strconv.Atoi(os.Args[1]); err == nil {
		// calculate the rows of data needed for this interval
		numberOfRows = int(float32(time) / float32(TimeInterval))
	} else {
		klog.V(1).Infof("Something is wrong with the INPUT")
		return
	}

    // nodes := []string{"oracle-ikube-w02", "oracle-ikube-w03", "oracle-ikube-w04"}
	nodes := []string{monitoredNode}
	for _, node := range nodes {
		results, err = customScoreInfluxDB([]string{"ipc", "mem_read", "mem_write", "l3m", "l2m", "procnrg", "dramnrg", "qpi0", "qpi1"}, NameToUuid[node], 0, numberOfRows, c)
		if err != nil {
			// fmt.Printf()
			klog.V(1).Infof("Error in querying or calculating average for the custom score in the first stage: %v", err.Error())
			return
		}
		klog.V(1).Infof("Node: %v, Calculating score...", node)
		res := calculateScore(scorerInput{metrics: results}, customScoreFn)
		klog.V(1).Infof("Node: %v, Finished calculating", node)

		// Check the core availability

		// Return the metrics of those cores
		metrics := []string{"c1res", "c0res", "ipc", "l3m", "l2m"} // check the c0res and ipc
		r, err := queryInfluxDbCores(metrics, NameToUuid[node], 0, numberOfRows, c, NodesToCores[node])
		if err != nil {
			klog.V(1).Infof("Error in querying or calculating core availability in the first stage: %v", err.Error())
		}

		// Calculate the average of those metrics
		var average map[string]float64
		if isMoving {
			average, err = calculateWeightedAverageCores(r, numberOfRows, len(metrics), len(NodesToCores[node]))
			if err != nil {
				klog.V(1).Infof("Error defining core availability")
			}
		} else {
			average, err = calculateAverageCores(r, numberOfRows, len(metrics), len(NodesToCores[node]))
			if err != nil {
				klog.V(1).Infof("Error defining core availability")
			}
		}

		// fmt.Println("Node,Score,IPC,Reads,Writes")
		// fmt.Printf("Node: %v, Score: %v, IPC: %v, Reads: %v, Writes: %v, CPU: %v", node, res, results["ipc"], results["mem_read"], results["mem_write"], 1-average["c0res"])
		// fmt.Printf("%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v,%v", node, res, results["ipc"], results["mem_read"], results["mem_write"], results["l3m"], results["l2m"], results["dramnrg"], results["procnrg"], results["l3occ"], results["qpi1"], results["qpi0"], average["l2m"], average["l3m"], average["c0res"], average["c1res"], 1-average["c0res"]-average["c1res"], average["ipc"], average["ipc"]/(results["mem_read"]+results["mem_write"]))
		fmt.Printf("Node: %v, Score: %v, IPC: %v, Reads: %v, Writes: %v, l3m: %v, l2m: %v, dramnrg: %v, procnrg: %v, l3occ: %v, qpi1: %v, qpi0: %v, average_l2m: %v, average_l3m: %v, average_c0res: %v, average_c1res: %v, average_not_c0res_c1res: %v, %v,%v\n", node, res, results["ipc"], results["mem_read"], results["mem_write"], results["l3m"], results["l2m"], results["dramnrg"], results["procnrg"], results["l3occ"], results["qpi1"], results["qpi0"], average["l2m"], average["l3m"], average["c0res"], average["c1res"], 1-average["c0res"]-average["c1res"], average["ipc"], average["ipc"]/(results["mem_read"]+results["mem_write"]))

	}

}