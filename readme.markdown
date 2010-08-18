Search Technology Assignment: Key Phrase Extraction
===================================================

Author: Alex Bowe

Email:  bowe.alexander@gmail.com

Obtaining
---------

To clone this repository:

	$ git clone http://github.com/alexbowe/keyphrase.git
	
This will create a directory `keyphrase` in your working directory. Note that this won't allow you to submit changes to the master repository.

Running
-------

You must have [Hadoop](http://hadoop.apache.org/) and [Dumbo](http://klbostee.github.com/dumbo/) installed. Just type:

    ./run.sh

This will copy the contents of the text folder to HDFS, and the results will be reformatted according to the assignment requirements and output to 3134434.out.

Dependencies
------------

**PROVIDED**:

 * [NLTK](www.nltk.org)
 * [PyYAML](www.pyyaml.org)

**NOT PROVIDED**:

 * [Hadoop](http://hadoop.apache.org/)
 * [Dumbo](http://klbostee.github.com/dumbo/)
 * [Perl](www.perl.org)
 * [Python](www.python.org)
 * [Java](www.java.com)

License
-------

Anyone can use my work however they wish.

The `performance.pl` and `porter.pl` scripts, `test.reader.stem.final`, the test data located in `test` and the assignment pdf files were all provided by the lecturer for the course. Please ask me if you need to use them, and I'll forward the request on.

NLTK is distributed under the [Apache License Version 2.0](http://www.apache.org/licenses/LICENSE-2.0). PyYAML is distributed under the [MIT License](http://www.opensource.org/licenses/mit-license.php).
