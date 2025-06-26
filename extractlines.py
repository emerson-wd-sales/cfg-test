#!/usr/bin/env python3

import sys
import re
import pprint
from collections import defaultdict

def extract_file_line_map(diff_file_path, simplify_paths=False):
    file_line_map = defaultdict(set)
    current_file = None

    # Regex to match and remove '/tmp/git-blob-*/' prefix
    tmp_blob_prefix = re.compile(r"^.*/git-blob-[^/]+/")

    file_header_re = re.compile(r"^.+ -> (.+)$")
    line_number_re = re.compile(r"^(\d+):")

    with open(diff_file_path, 'r') as f:
        for line in f:
            line = line.rstrip()

            match = file_header_re.match(line)
            if match:
                full_path = match.group(1)

                # remove /tmp/git-blob-*/ prefix
                if simplify_paths:
                    current_file = tmp_blob_prefix.sub('', full_path)
                else:
                    current_file = full_path
                continue

            if line.startswith("=") or line.startswith("---") or line.startswith("+++"):
                continue

            match = line_number_re.match(line)
            if match and current_file:
                line_number = int(match.group(1))
                file_line_map[current_file].add(line_number)

    return dict(file_line_map)

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <diffsitter_output.txt>")
        sys.exit(1)

    diff_path = sys.argv[1]
    global file_changes 
    file_changes = extract_file_line_map(diff_path)

    # Pretty-print the dictionary
    for filename, lines in file_changes.items():
        print(f"{filename}: {sorted(lines)}")

def save_dict_as_python_file(data, output_path):
    with open(output_path, 'w') as f:
        f.write("# Auto-generated file with file-to-lines mapping\n")
        f.write("file_line_map = ")
        pprint.pprint(data, stream=f)

if __name__ == "__main__":
    main()
    save_dict_as_python_file(file_changes, "pycparser-cc/file_line_map.py")