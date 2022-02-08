#!/bin/bash
HELP="Command line script for executing the available workflow versions.

./exec.sh <version> <url> --times=<times> <eraser1> <eraser2> --sleep=<sleep>s (<result>)

Options:
    <version>   Version to be executed
    <url>       Input video selection - url1 or url2 or url3
    <times>     How many times the workflow is gonna be executed
    <eraser1>   Delete frames that were just created - yes or no
    <eraser2>   Delete results from current execution - yes or no
    <sleep>     sleep duration between invocations - e.g 10 => 10 seconds
    <result>    If given --no-result, then no result will be displayed. If not, result will appear
    
    e.g         ./exec.sh version1 url1 --times=10 yes yes --sleep=10s --step=5s
    e.g         ./exec.sh version1 url2 --times=10 no no --sleep=10s --step=10s --no-result
    e.g         ./exec.sh version2 url1 --times=15 yes no --sleep=15s --step=5s"

BAD_USAGE="./exec.sh: Incorrect usage.
Try './exec.sh -h' or './exec.sh --help' for further information."
    
echo "============================"
echo "=== ML Workflow Execution =="
echo "============================"

if [ $1 == '-h' ] || [ $1 == '--help' ]
then 
    echo "$HELP"
    exit 0
fi

if [ $4 != 'yes' ] && [ $4 != 'no' ] && [ $5 != 'yes' ] && [ $5 != 'no' ]
then 
    echo "$BAD_USAGE"
	exit -1
fi

start=$(date +'%s')
number=$1

times=$3
arrTimes=(${times//=/ })
times=${arrTimes[1]}

URL=$2

sleep=$6
arrSleep=(${sleep//=/ })
arrSleep2=(${arrSleep[1]//s/ })
sleep=${arrSleep2[0]}

step=$7
arrStep=(${step//=/ })
arrStep2=(${arrStep[1]//s/ })
step=${arrStep2[0]}


URL1="https://github.com/intel-iot-devkit/sample-videos/raw/master/head-pose-face-detection-female.mp4" #duration 2m 15s
#URL1="https://im3.ezgif.com/tmp/ezgif-3-b56610b863.mp4"
URL2="https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master/bottle-detection.mp4" #duration 40s
URL3="https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master/head-pose-face-detection-male.mp4" #duration 2m 14s
URL4="https://im3.ezgif.com/tmp/ezgif-3-f0dedbb69f.mp4" #0-280 (1 frame / 15sec)
URL5="https://im3.ezgif.com/tmp/ezgif-3-955cc84064.mp4" #0-500 (1 frame / 15sec)
URL6="https://im3.ezgif.com/tmp/ezgif-3-955cc84064.mp4" #0-400 (1 frame / 10sec)
URL7="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4" #0-500 (1 frame / 5 sec)
URL8="https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4"

case $2 in 
        url1|1)

        URL=${URL1}
        ;;

        url2|2)

        URL=${URL2}
        ;;

        url3|3)
        URL=${URL3}
        ;;

        url4|4)
        URL=${URL4}
        ;;

        url5|5)
        URL=${URL5}
        ;;

        url6|6)
        URL=${URL6}
        ;;

        url7|7)
        URL=${URL7}
        ;;

        url8|8)
        URL=${URL8}
        ;;

        *)
		echo "$BAD_USAGE"
		exit -1
		;;
esac

echo 
echo -e "\u2699 Executing "$number" ..."
echo 

for ((i=0;i<${times};i++));
    do 
        curl http://localhost:8080/function/"$number" -d '{"output_bucket": "image-output", "url": "'"$URL"'", "seconds": '"$step"', "lower_limit": 0, "upper_limit": "full"}'
        #sleep 4.5
        sleep ${sleep}
    done



#echo -e "\u231B Average time of instance execution: $(python3 ./scripts/reader2.py 6 ${times})"
echo 

if [ $# == 8 ]
then
    if [ $8 == '--no-result' ]
    then 
        echo "No result displayed."
        echo 
    fi
else 
    echo "Result of execution: "
    python3 ./scripts/reader.py 1
    echo
fi

if [ $4 == 'yes' ]
then
    echo -e "\U1F6AE Deleting the frames ..."
    python3 ./scripts/eraser.py 10
elif [ $4 == 'no' ]
then
    echo -e "\u270D  Saving the frames ..."
else
    echo "$BAD_USAGE"
	exit -1
fi 

if [ $5 == 'yes' ]
then
    echo -e "\U1F6AE Deleting the results ..."
    python3 ./scripts/eraser2.py 10
elif [ $5 == 'no' ]
then
    echo -e "\u270D  Saving the results ..."
else 
    echo "$BAD_USAGE"
	exit -1
fi 


echo -e "\u2705 Script took $(($(date +'%s') - $start)) seconds to complete!"
echo 



