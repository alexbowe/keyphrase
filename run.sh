#!/bin/bash
DEPS=deps
HADOOP=$HADOOP_HOME/bin/hadoop
LOG=dumbo.log
INPUT=text
DFS_INPUT=dfs_text
OUTPUT=3134434.out
DFS_OUTPUT=output

# Remove previous run if it exists
echo "Removing previous results..."
$HADOOP fs -rmr $DFS_OUTPUT
rm $OUTPUT

# Move input files to DFS
# NOTE: Would have issues if there are files in one folder that aren't
# in the other, but for now it's okay
echo "Checking if input files are on HDFS..."
RESULT=$($HADOOP fs -ls $DFS_INPUT)
if [ ${#RESULT} -eq 0 ]; then 
    echo "Moving input files to HDFS..."
    $HADOOP fs -put $INPUT/ $DFS_INPUT
else
    echo "Input files already on HDFS; no need to move them."
fi

# Run the MapReduce program via Dumbo
echo "Beginning Dumbo Program..."
dumbo start keyphrase.py \
    -hadoop $HADOOP_HOME \
    -libegg $DEPS/nltk-2.0b9-py2.6.egg \
    -libegg $DEPS/PyYAML.egg \
    -addpath yes \
    -input $DFS_INPUT/* \
    -output $DFS_OUTPUT \
    -inputformat text \
    -outputformat text

# Wait for Hadoop to finish before continuing
wait

# Get Output from DFS
echo "Collecting output from HDFS..."
$HADOOP_HOME/bin/hadoop fs -cat $DFS_OUTPUT/part-* > $OUTPUT

# Format for use with performance tester
echo "Reformatting output..."
./format.pl $OUTPUT

# Sort the output for easier manual inspection
sort -n $OUTPUT > $OUTPUT.sorted
mv $OUTPUT.sorted $OUTPUT

# Assess the performance
./performance.pl $OUTPUT

