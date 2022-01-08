#!/bin/bash
HELP="Command line script for executing the available workflow versions.

./exec.sh <version> <url> <times> <eraser1> <eraser2> (<result>)

Options:
    <version>   Version to be executed
    <url>       Input video selection - url1 or url2 or url3
    <times>     How many times the workflow is gonna be executed
    <eraser1>   Delete frames that were just created - yes or no
    <eraser2>   Delete results from current execution - yes or no
    <result>    If given --no-result, then no result will be displayed. If not, result will appear
    
    e.g         ./exec.sh version1 url1 10 yes yes
    e.g         ./exec.sh 1 url2 10 no no --no-result
    e.g         ./exec.sh version2 url1 15 yes no"

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
URL=$2


URL1="https://github.com/intel-iot-devkit/sample-videos/raw/master/head-pose-face-detection-female.mp4" #duration 2m 15s
URL2="https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master/bottle-detection.mp4" #duration 40s
URL3="https://raw.githubusercontent.com/intel-iot-devkit/sample-videos/master/head-pose-face-detection-male.mp4" #duration 2m 14s


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

            for ((i=0;i<${times};i++))
            do 
                curl -X POST http://localhost:8080/function/version1 -d '{"output_bucket": "image-output", "url": "'"$URL"'", "seconds": 15, "lower_limit": 0, "upper_limit": "full"}'
                sleep 4
            done
            ;;

            version2|2)

            echo 
            echo -e "\u2699  Executing version2 ..."
            echo 

            for ((i=0;i<${times};i++))
            do 
                curl -X POST http://localhost:8080/function/version2 -d '{"output_bucket": "image-output", "url": "'"$URL"'", "seconds": 15, "lower_limit": 0, "upper_limit": "full"}'
                sleep 7
            done
            ;;

            version3|3)

            echo 
            echo -e "\u2699  Executing version3 ..."
            echo 

            for ((i=0;i<${times};i++))
            do 
                curl -X POST http://localhost:8080/function/version3 -d '{"output_bucket": "image-output", "url": "'"$URL"'", "seconds": 15, "lower_limit": 0, "upper_limit": "full"}'
                sleep 2.8
            done
            ;;

            version4|4)

            echo 
            echo -e "\u2699  Executing version4 ..."
            echo 

            for ((i=0;i<${times};i++))
            do 
                curl -X POST http://localhost:8080/function/version4 -d '{"output_bucket": "image-output", "url": "'"$URL"'", "seconds": 15, "lower_limit": 0, "upper_limit": "full"}'
                #sleep 0.5
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

echo -e "\u231B It took $(($(date +'%s') - $start)) seconds!"
echo 

if [ $# == 6 ]
then
    if [ $6 == '--no-result' ]
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



