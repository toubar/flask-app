#!/bin/bash

####
##   this is a bash script for building a docker image of the app.
##   1)removes current containers
##   2)removes images
##   3) builds a new image
##   4) runs a new container from the new image
####

# text color variables
green='\e[1;32m%s\e[0m\n'
red='\e[1;31m%s\e[0m\n'

DOCKER_IMAGE_NAME=flask_backend
DOCKER_CONTAINER_NAME=flask_backend

function remove_containers() {
  printf "$red" "----------------------------------------REMOVING CONTAINERS----------------------------------------"
  docker rm -f $containers
  printf "$green" "---------------------------------------------DONE------------------------------------------------"
}

function remove_images() {
  docker rmi $(docker images -aq $DOCKER_IMAGE_NAME)
  printf "$green" "----------------------------------------IMAGES REMOVED-------------------------------------------"
}

function build_image() {
  printf "$green" "--------------------------------------BUILDING NEW IMAGE-----------------------------------------"
  docker build -t $DOCKER_IMAGE_NAME:latest .
  printf "$green" "---------------------------------------------DONE------------------------------------------------"
}

function run_container() {
  printf "$green" "----------------------------------------RUNNING CONTAINER----------------------------------------"
  docker run -d --name $DOCKER_CONTAINER_NAME -p 5000:5000 --rm $DOCKER_IMAGE_NAME:latest
  printf "$green" "---------------------------------------CONTAINER IS RUNNING--------------------------------------"
}

# store list of container IDs
containers=$(docker ps -aqf "ancestor=$DOCKER_IMAGE_NAME")

# if containers is not empty, remove containers | Else -> proceed
if [ ! -z "$containers" ]; then
  printf "$green" "$DOCKER_IMAGE_NAME Docker containers(s) found. Deleting containers(s)...."
  remove_containers
else
  printf "$red" "No $DOCKER_IMAGE_NAME Docker containers(s) found."
  printf "$red" "---------------------------------------------------------------------------------------------------"
fi

# store list of Docker Image IDs
images=$(docker images | grep $DOCKER_IMAGE_NAME)

# if above command returned 0, then docker images were found -> delete them | Else -> proceed
if [ $? -eq 0 ]; then
  printf "$green" "$DOCKER_IMAGE_NAME Docker image(s) found. Deleting current image(s) and building a new image...."
  remove_images
else
  printf "$red" "No $DOCKER_IMAGE_NAME Docker image(s) found. Building one.."
fi

build_image
run_container

exit 0