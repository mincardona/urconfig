#!/usr/bin/perl

use strict;
use warnings;

#
# https://perlmaven.com/trim
#

sub ltrim {
    my $s = shift;
    $s =~ s/^\s+//;
    return $s;
}

sub rtrim {
    my $s = shift;
    $s =~ s/\s+$//;
    return $s;
}

sub trim {
    my $s = shift;
    $s =~ s/^\s+|\s+$//g;
    return $s;
}

my $titleRegex = qr/[A-Za-z0-9_\-\.]+/;
my $keyRegex = qr/[A-Za-z0-9_\-]+/;
my $blankRegex = qr/^\s*$/;

# parseUrCfgLines(line0, line1, line2...)
# returns ($hashReference, $errorLinesCount)
sub parseUrCfgLines {
    my @lines = @_;

    my %sectionHash;
    my $currentSection = "";
    $sectionHash{$currentSection} = {};

    my $errCount = 0;
    my $lineNo   = 1;

    foreach my $line (@lines) {
        # check for k=v
        if ($line =~ /^\s*(${keyRegex})\s*=(.*)$/) {
            my ($k, $v) = ($1, trim($2));
            $sectionHash{$currentSection}{$k} = $v;

        # check for header line
        } elsif ($line =~ /^\s*\[\s*(${titleRegex})\s*\]\s*$/) {
            my $title = $1;
            if (!exists $sectionHash{$title}) {
                $sectionHash{$title} = {};
            }
            $currentSection = $title;

        # check for comment
        } elsif ($line =~ /^\s*#(.*)$/) {
            my $commentText = trim($1);

        # check for blank line
        } elsif ($line =~ /${blankRegex}/) {
            # excludes blank lines from being caught as
            # errors in the else clause

        # unable to interpret line
        } else {
            print STDERR "UrConfig syntax error on line $lineNo\n";
            $errCount++;
        }

        $lineNo++;
    }

    return (\%sectionHash, $errCount);
}

# printUrCfgHash($cfgHash, $ostream)
# serializes cfgHash to ostream
sub printUrCfgHash {
    my ($cfgHash, $ostream) = @_;
    # iterate through each section
    foreach my $title (sort keys %{$cfgHash}) {
        my $kvPairs = $cfgHash->{$title};
        # don't print the "empty section" if it has no contents
        next if ($title eq "" && (keys %{$kvPairs} < 1));
        print $ostream "[$title]\n";
        # iterate through each k-v pair in the section
        foreach my $key (sort keys %{$kvPairs}) {
            my $value = $kvPairs->{$key};
            print $ostream "$key=$value\n";
        }
        print $ostream "\n";    # print a blank line after each section
    }
}

# queries a cfgHash for a value reference
# two ways to call:
# - provide a hash reference, a section title, and a key
# - provide a hash reference and a query string
# returns a *reference* to the value string, or undef if it was not found (also prints an error message to STDERR)
sub getUrCfg {
    my $hash = shift;
    my $title = "";
    my $key = "";
    # hash, title, key
    if (scalar(@_) == 3) {
        $title = shift;
        $key = shift;
    # hash, query
    } else {
        my $keystr = shift;
        if ($keystr =~ /^\s*\[\s*(${titleRegex})\s*\]\s*\.?\s*(${keyRegex})\s*$/) {
            ($title, $key) = ($1, $2);
        } elsif ($keystr =~ /^\s*(${titleRegex})\s*\.\s*(${keyRegex})\s*/) {
            ($title, $key) = ($1, $2);
        } else {
            print STDERR "Bad query string\n";
            return undef;
        }
    }
    return \($hash->{$title}->{$key});
}

#-----------main section-----------#

my @lines = ();
while (my $line = <STDIN>) {
    push @lines, $line;
}

# could use
# `my ($urResult, $errCount) = ...`
# or
# `my ($urResult) = ...`
my ($urResult, $errCount) = parseUrCfgLines(@lines);

printUrCfgHash($urResult, *STDOUT);
