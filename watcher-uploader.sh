#!/bin/bash
echo "Ensure that you are running this with sudo due to read write priveleges imposed by the docker container"

FOLDER=${1:-data}
PREFIX=${2:-/synthea/}
S3_BUCKET=${3:-s3://kpi-datapipeline-dev}
COUNT=0
echo "PREFIX: $PREFIX"
echo "S3_BUCKET: $S3_BUCKET"
echo "FOLDER: $FOLDER"
inotifywait -m $FOLDER -e close_write --recursive |
  while read dir action file; do
    COUNT=$((COUNT + 1))
    #echo "The file '$file' appeared in directory '$dir' via '$action'"
    #call-local-sqs-consumer.sh "$dir/$file" &
    TARGET=$S3_BUCKET$PREFIX$file
    SOURCE=$dir$file
    echo $COUNT - $SOURCE "->" $TARGET
    aws s3 cp $SOURCE $TARGET
    sudo rm $SOURCE
  done
