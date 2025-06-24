#!/bin/bash
set -e  # Exit immediately if any command fails

# Check for two arguments (commit hashes or refs)
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <commit1> <commit2>"
    exit 1
fi

# Run git difftool and save to file
git difftool "$1" "$2" > changedlines.txt

# Extract line changes
python3 extractlines.py changedlines.txt

# Change directory to pycparser-cc
cd pycparser-cc || { echo "pycparser-cc directory not found"; exit 1; }

# Run the analysis
python3 run.py
