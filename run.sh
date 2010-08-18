#!/bin/bash
DEPS=deps
HADOOP=$HADOOP_HOME/bin/hadoop
LOG=dumbo.log
LOC_INPUT=text
DFS_INPUT=dfs_${LOC_INPUT}
LOC_OUTPUT=3134434.out
DFS_OUTPUT=dfs_${LOC_OUTPUT}

# Argument Handling
args=`getopt l $*`
eval set -- $args
if [ $1 == '--' ]; then
    DISTRIB=1
fi

echo -n "Running in "
if [ $DISTRIB ]; then echo -n "DISTRIBUTED"; else echo -n "LOCAL"; fi
echo " mode"

# Remove previous run if it exists
echo "Removing previous results..."
if [ $DISTRIB ]; then
    $HADOOP fs -rmr $DFS_OUTPUT > /dev/null 2> /dev/null
fi
rm $LOC_OUTPUT 2> /dev/null

# Move input files to DFS
# NOTE: Would have issues if there are files in one folder that aren't
# in the other, but for now it's okay
if [ $DISTRIB ]; then
    RESULT=$($HADOOP fs -ls $DFS_INPUT 2> /dev/null)
    if [ ${#RESULT} -eq 0 ]; then 
        echo "Moving input files to HDFS..."
        $HADOOP fs -moveFromLocal $LOC_INPUT $DFS_INPUT
    else
        echo "Input files are already on HDFS..."
    fi
fi

if [ $DISTRIB ]; then
    INPUT=$DFS_INPUT
    OUTPUT=$DFS_OUTPUT
    DIST_ARGS="-hadoop $HADOOP_HOME -file mycorpus.py"
else
    INPUT=$LOC_INPUT
    OUTPUT=$LOC_OUTPUT
fi

# Run the MapReduce program via Dumbo
echo "Beginning Dumbo Program..."
dumbo start keyphrase.py \
    $DIST_ARGS \
    -libegg $DEPS/nltk-2.0b9-py2.6.egg \
    -libegg $DEPS/PyYAML.egg \
    -addpath yes \
    -input $INPUT/* \
    -output $OUTPUT \
    -inputformat text \
    -outputformat text \
    > /dev/null \
    2> diagnostics

# Wait for Hadoop to finish before continuing
wait

# Get Output from DFS
if [ $DISTRIB ]; then
    echo "Collecting output from HDFS..."
    $HADOOP_HOME/bin/hadoop fs -cat $DFS_OUTPUT/part-* > $LOC_OUTPUT
fi

# Format for use with performance tester
#echo "Reformatting output..."
./format.pl $LOC_OUTPUT > $LOC_OUTPUT.formatted
mv $LOC_OUTPUT.formatted $LOC_OUTPUT

# Sort the output for easier manual inspection
sort -n $LOC_OUTPUT > $LOC_OUTPUT.sorted
mv $LOC_OUTPUT.sorted $LOC_OUTPUT

# Assess the performance
./performance.pl $LOC_OUTPUT

