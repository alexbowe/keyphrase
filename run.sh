#!/bin/bash
DEPS=deps
INPUT_DIR=$1

rm $2
dumbo start keyphrase.py \
    -libegg $DEPS/nltk-2.0b9-py2.6.egg \
    -libegg $DEPS/PyYAML.egg \
    -addpath yes \
    -input $INPUT_DIR/* \
    -output $2 \
    2> dumbo.log
cat $2
    