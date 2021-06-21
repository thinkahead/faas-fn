#!/usr/local/bin/perl
use bignum;
foreach my $line ( <STDIN> ) { chomp($line);print $line;if ($line=~/^$/) { last; } print(" ",bignum::bpi($line),"\n"); }
