#!/usr/bin/perl

# read author keyphrases
my $testpapername = shift;
#print "testpapername=".$testpapername.":\n";exit;

my $predictsize = 0;
my $goldsize = 0;
my $correct = 0;

my %CANDIDATE = ();
open(FILE, $testpapername) or die $!;
while(my $line = <FILE>){
  chomp($line);
  my ($papername, $keystr) = split(/ : /, $line);
  $CANDIDATE{$papername} = $keystr;
  my @set = split(/\,/, $keystr);
  $predictsize += scalar(@set);
}

my ($participant, $answerformat) = split(/\./, $testpapername);
#print $participant."\t".$answerformat."\n";exit;

open(FILE, "test.reader.stem.final");
my @goldset = <FILE>;
close(FILE);

foreach my $oneline (@goldset){
  chomp($oneline);
  my ($papername, $keystr) = split(/ : /, $oneline);
  my @answerset = split(/\,/, $keystr);
  $recallsize += scalar(@answerset);

  # get keyphrases of a paper in candidiates
  my $tmpcandidate = $CANDIDATE{$papername};
  my @candidateset = split(/,/, $tmpcandidate);

  foreach my $one (@candidateset){ # totally 15 candidates
    foreach my $two (@answerset){
      if($one eq $two){
        $correct++;
      }
    }
  }
}

print "No. of user assigned keyphrases = ".$predictsize."\n";
print "No. of gold-standard keyphrases = ".$recallsize."\n";
print "No. of overlaps between user keyphrases and gold-standard keyphrases = ".$correct."\n";

my $tmpPrecision = ($correct*100)/$predictsize;
my $tmpRecall = ($correct*100)/$recallsize;
my $Precision = sprintf("%.2f", $tmpPrecision);
my $Recall = sprintf("%.2f", $tmpRecall);

my $tmpFscore = 0;
if($Precision + $Recall > 0){
  $tmpFscore = 2*($Precision * $Recall) / ($Precision + $Recall);
}
my $Fscore = sprintf("%.2f", $tmpFscore);

print "==================================================================\n";
print "[Participant] #_of_right answrs, Precision, Recall, Fscore\n";
print "[".$participant."]\t".$correct."\t".$Precision."\%\t".$Recall."\%\t".$Fscore."\%\n";


