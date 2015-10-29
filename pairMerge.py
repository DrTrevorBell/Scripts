# Copyright (C) 2015 University of the Witwatersrand, Johannesburg, South Africa
# Author: Dr Trevor G. Bell, TrevorGrahamBell@gmail.com

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

#!/usr/bin/python

# This is an example script to demonstrate the use of the EMBOSS
# "merger" program. It makes use of the "climb" library to process
# the FASTA file. It requires a forward and reverse input file in
# FASTA format and writes out a FASTA file with an extension of "OUT"

# Usage:
#   $ python paired.py ForwardFile.fasta ReverseFile.fasta

# Caveats:
# 1. If the input sequences do not contain sufficient overlapping regions,
#    the resulting output ("merged") sequence will likely be meaningless.
# 2. The script processes sequences from the two input files in order (as pairs),
#    without checking the FASTA IDs. The input files must therefore contain
#    the same number of sequences in matching order.
# 3. The "subprocess" command includes a check to ensure that the script is
#    not run in a Win32 machine. This can be modified, however, to exeute
#    the appropriate command under that operating system.
# 4. The "climb" library is required.
# 5. The EMBOSS suite of programs is required,as the "merger" program is used.

import climb                    # Available from https://github.com/DrTrevorBell
import sys
import subprocess

Forward = climb.Sequence()
Reverse = climb.Sequence()

Forward.load(sys.argv[1])       # Command-line parameter specifying forward file
Reverse.load(sys.argv[2])       # Command-line parameter specifying reverse file

# Loop over each sequence in the forward file and write out each forward
# sequence and each reverse sequence, in turn, to a temporary file.
# The temporary forward and reverse files are then merged with the EMBOSS "merge" program
for i in range(Forward.seqCount()):
    fTemp = open('fTemp.fasta', 'w')
    rTemp = open('rTemp.fasta', 'w')
    fTemp.write('>%s\n%s\n' % (Forward.seq[i]['id'], Forward.seq[i]['seq']))
    rTemp.write('>%s\n%s\n' % (Reverse.seq[i]['id'], Reverse.seq[i]['seq']))
    fTemp.close()
    rTemp.close()

    command = 'merger -bsequence rTemp.fasta -asequence fTemp.fasta -auto -outfile "%s.OUT" -outseq "%s.fasta"' % (Forward.seq[i]['id'][:24], Forward.seq[i]['id'][:24])
    return_code = subprocess.call(command, shell=(sys.platform != "win32"))

# end for

