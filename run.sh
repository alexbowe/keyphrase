#!/bin/bash
DEPS=deps
INPUT_DIR=text #$1
LOG=dumbo.log
OUT=3134434.out #$2

# Remove previous run if it exists
rm $OUT

# Run the MapReduce program
dumbo start keyphrase.py \
    -libegg $DEPS/nltk-2.0b9-py2.6.egg \
    -libegg $DEPS/PyYAML.egg \
    -addpath yes \
    -input $INPUT_DIR/* \
    -output $OUT \
    2> $LOG

# Format for use with performance tester
./format.pl $OUT

# Assess the performance
./performance.pl $OUT
