#!/bin/bash

echo "Determining whether the strings '01101' and '01101' are equivalent with One-tape and Two-tape TMs."
echo "The machines should accept since these are identical."
echo ""
echo "One-tape TM:"
python3 main.py <<EOF
one_tape
test_identical
01101#01101
n
EOF

echo ""
echo "Two-Tape TM:"
python3 main.py <<EOF
two_tape
01101
01101
n
EOF




