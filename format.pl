#! /usr/bin/perl -i -p

# Remove single quotes
s/'//g;
# Replace tab with specified separator
s/\t/ : /;
# Extract file numbers
s/.*\/([0-9]+)\.txt/\1/;
