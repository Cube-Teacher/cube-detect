#!/bin/bash

# get current dir name whenever on any device
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

declare -i num=1

for file in "$DIR/img"/*
do 
    newname=${DIR}/img/${num}".jpg"
    mv $file ${newname}
    num+=1
done