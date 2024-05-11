#!/bin/bash
DOCKER_USER='skovida'
DOCKER_IMAGE='nvdiffrec'
DOCKER_TAG='v1'
FULL_IMAGE="$DOCKER_USER/$DOCKER_IMAGE:$DOCKER_TAG"
NVDIFFREC_PATH="$1"
DATASET_PATH="$2"

if [ -z "$NVDIFFREC_PATH" ]; then
	echo 'no nvdiffrec path provided as arg 1, exiting...'
	exit 1
fi
if [ -z "$DATASET_PATH" ]; then
	echo 'no dataset path provided as arg 2, exiting...'
	exit 1
fi

if [ ! -d "$NVDIFFREC_PATH" ]; then
	echo "$NVDIFFREC_PATH is not a dir!"
	exit 1
fi
if [ ! -d "$DATASET_PATH" ]; then
	echo "$DATASET_PATH is not a dir!"
	exit 1
fi

echo "Running container with dataset in /dataset."
echo -e "\tPrepend this to the dataset path"
docker run --gpus device=0 -it -v "$DATASET_PATH":/dataset -v "$NVDIFFREC_PATH":/nvdiffrec -w=/nvdiffrec -v /raid:/raid "$FULL_IMAGE" bash
