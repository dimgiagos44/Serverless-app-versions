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
    
    e.g         ./exec.sh version1 url1 --times=10 yes yes --sleep=10s
    e.g         ./exec.sh 1 url2 --times=10 no no --sleep=10s --no-result
    e.g         ./exec.sh version2 url1 --times=15 yes no --sleep=15s"

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


URL1="https://github.com/intel-iot-devkit/sample-videos/raw/master/head-pose-face-detection-female.mp4" #duration 2m 15s
#URL1="https://im2.ezgif.com/tmp/ezgif-2-15cfa4b5f7.mp4"
URL2="https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master/bottle-detection.mp4" #duration 40s
URL3="https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master/head-pose-face-detection-male.mp4" #duration 2m 14s
URL4="https://im2.ezgif.com/tmp/ezgif-2-d17701bdc4.mp4"
URL5="https://im2.ezgif.com/tmp/ezgif-2-1087e7bdca.mp4"

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

        *)
		echo "$BAD_USAGE"
		exit -1
		;;
esac

case $number in
            version1|1)

            echo 
            echo -e "\u2699  Executing version1 ..."
            echo 

            for ((i=0;i<${times};i++));
            do 
                curl http://localhost:8080/function/version1 -d '{"output_bucket": "image-output", "url": "'"$URL"'", "seconds": 15, "lower_limit": 0, "upper_limit": "full"}'
                #sleep 4.5
                sleep ${sleep}
            done
            ;;

            version2|2)

            echo 
            echo -e "\u2699  Executing version2 ..."
            echo 

            for ((i=0;i<${times};i++));
            do 
                curl http://localhost:8080/function/version2 -d '{"output_bucket": "image-output", "url": "'"$URL"'", "seconds": 15, "lower_limit": 0, "upper_limit": "full"}'
                #sleep 7.2
                sleep ${sleep}
            done
            ;;

            version3|3)

            echo 
            echo -e "\u2699  Executing version3 ..."
            echo 

            for ((i=0;i<${times};i++));
            do 
                curl http://localhost:8080/function/version3 -d '{"output_bucket": "image-output", "url": "'"$URL"'", "seconds": 15, "lower_limit": 0, "upper_limit": "full"}'
                #sleep 5.8
                sleep ${sleep}
            done
            ;;

            version4|4)

            echo 
            echo -e "\u2699  Executing version4 ..."
            echo 

            for ((i=0;i<${times};i++))
            do 
                curl http://localhost:8080/function/version4 -d '{"output_bucket": "image-output", "url": "'"$URL"'", "seconds": 15, "lower_limit": 0, "upper_limit": "full"}'
                #sleep 1
                sleep ${sleep}
            done
            ;;

	        --help|-h)
            echo "$HELP"
            exit 0
            ;;

            *)
		    echo "$BAD_USAGE"
		    exit -1
		    ;;
esac

echo -e "\u231B Average time of instance execution: $(python3 ./scripts/reader2.py 6 ${times})"
echo 

if [ $# == 7 ]
then
    if [ $7 == '--no-result' ]
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



