#!/bin/bash
HELP="Command line script for executing the available workflow versions.

./exec.sh <number> <times> <eraser1> <eraser2>

Options:
    <number>    Number of version to be executed
    <times>     How many times the workflow is gonna be executed
    <eraser1>   Delete frames that were just created - yes or no
    <eraser2>   Delete results from current execution - yes or no
    
    e.g         ./exec.sh version1 10 yes yes
    e.g         ./exec.sh 1 10 no no
    e.g         ./exec.sh version2 15 yes no"

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

if [ $3 != 'yes' ] && [ $3 != 'no' ] && [ $4 != 'yes' ] && [ $4 != 'no' ]
then 
    echo "$BAD_USAGE"
	exit -1
fi

start=$(date +'%s')
number=$1
times=$2
URL1="https://github.com/intel-iot-devkit/sample-videos/raw/master/head-pose-face-detection-female.mp4"

case $number in
            version1|1)

            echo 
            echo -e "\u2699 Executing version1 ..."
            echo 

            for ((i=0;i<${times};i++))
            do 
                curl -X POST http://localhost:8080/function/version1 -d '{"output_bucket": "image-output", "url": "'"$URL1"'", "seconds": 15, "lower_limit": 0, "upper_limit": "full"}'
                sleep 4
            done
            ;;

            version2|2)

            echo 
            echo -e "\u2699 Executing version2 ..."
            echo 

            for ((i=0;i<${times};i++))
            do 
                curl -X POST http://localhost:8080/function/version2 -d '{"output_bucket": "image-output", "url": "'"$URL1"'", "seconds": 15, "lower_limit": 0, "upper_limit": "full"}'
                sleep 7.2
            done
            ;;

            version3|3)

            echo 
            echo -e "\u2699 Executing version3 ..."
            echo 

            for ((i=0;i<${times};i++))
            do 
                curl -X POST http://localhost:8080/function/version3 -d '{"output_bucket": "image-output", "url": "'"$URL1"'", "seconds": 15, "lower_limit": 0, "upper_limit": "full"}'
                sleep 4
            done
            ;;

            version4|4)

            echo 
            echo -e "\u2699 Executing version4 ..."
            echo 

            for ((i=0;i<${times};i++))
            do 
                curl -X POST http://localhost:8080/function/version4 -d '{"output_bucket": "image-output", "url": "'"$URL1"'", "seconds": 15, "lower_limit": 0, "upper_limit": "full"}'
                sleep 4
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

if [ $3 == 'yes' ]
then
    echo -e "\U1F6AE Deleting the frames ..."
    source ../test/virtualenv/bin/activate
    python3 ../test/eraser.py 10
elif [ $3 == 'no' ]
then
    echo -e "\u270D  Saving the frames ..."
else
    echo "$BAD_USAGE"
	exit -1
fi 

if [ $4 == 'yes' ]
then
    echo -e "\U1F6AE Deleting the results ..."
    source ../test/virtualenv/bin/activate
    python3 ../test/eraser2.py 10
elif [ $4 == 'no' ]
then
    echo -e "\u270D  Saving the results ..."
else 
    echo "$BAD_USAGE"
	exit -1
fi 



