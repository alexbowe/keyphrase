#! /usr/bin/perl -p

# Remove single quotes (when dumbo is run locally)
s/^['"](.*)['"]\t+['"](.*)['"]$/\1\t\2/;

# Replace tab with specified separator
s/\t/ : /;

# Extract file numbers
s/.*\/([0-9]+)\.txt/\1/;

