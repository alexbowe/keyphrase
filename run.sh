#!/bin/bash
DEPS=deps
INPUT_DIR=text #$1
LOG=dumbo.log
OUT=3134434.out #$2

# Remove previous run if it exists
$HADOOP_HOME/bin/hadoop fs -rmr $OUT 2> $LOG
rm $OUT 2> $LOG

# Move input files to DFS
$HADOOP_HOME/bin/hadoop fs -put $INPUT_DIR/ $INPUT_DIR

# Run the MapReduce program
dumbo start keyphrase.py \
    -hadoop $HADOOP_HOME \
    -libegg $DEPS/nltk-2.0b9-py2.6.egg \
    -libegg $DEPS/PyYAML.egg \
    -addpath yes \
    -input $INPUT_DIR/* \
    -output $OUT \
    -inputformat text \
    -outputformat text \
    2> $LOG

# Get Output from DFS
# $HADOOP_HOME/bin/hadoop fs -get $OUT/* $OUT

# Format for use with performance tester
# ./format.pl $OUT

# Sort the output for easier manual inspection
# sort -n $OUT > $OUT.sorted
# mv $OUT.sorted $OUT

# Assess the performance
#./performance.pl $OUT #> results
#cat results

# Track difference
#cat results | tail -1 >> perf
# Use awk here to calculate difference in %ges
#rm results
