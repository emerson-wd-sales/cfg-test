import sys
import re
from collections import defaultdict

def parse_cflow_graph(file_path):
    graph = defaultdict(set)
    locations = {}
    stack = []

    with open(file_path) as f:
        # print("file path is "+str(f))
        for line in f:
            # print("line is "+str(line))
            stripped = line.lstrip()
            # print("stripped line is "+str(stripped))
            if not stripped or '(' not in stripped: # blank, cflow bug, not a function (?)
                continue

            indent = len(line) - len(stripped)
            level = indent // 4 # 4-space indent
            # print ("level is "+str(level))

            match = re.match(r'.*?([a-zA-Z_][a-zA-Z0-9_]*)\s*\(.*<(.+?)>', stripped)
            if not match:
                continue

            func, full_sig = match.groups()

            # Extract just the file path after " at " and before ">"
            if " at " in full_sig:
                location = full_sig.split(" at ")[-1]
                filename = location.split(":")[0].strip()
            else:
                raise "error extracting function location"

            locations[func] = filename


            if level < len(stack):
                stack = stack[:level]

            if stack:
                parent = stack[-1]
                graph[parent].add(func)

            if len(stack) <= level:
                stack.append(func)
            else:
                stack[level] = func

    return graph, locations

def load_changed_functions(path):
    changed = set()
    with open(path) as f:
        for line in f:
            if line.strip():
                changed.add(line.strip())
    return changed

def is_library_function(func, locations):
    print("locations are " + str(locations))
    filename = locations.get(func, "")
    return "/" in filename

def analyze(reverse_graph, forward_graph, locations, changed_funcs):
    result = set()

    for func in changed_funcs:
        print("analising" + func)
        ftype = "library" if is_library_function(func, locations) else "nonlib"
        print(func + " is " + ftype)
        direct_callers = reverse_graph.get(func, set())

        if ftype == "nonlib":
            result.update(direct_callers)
        elif ftype == "library":
            result.update(direct_callers)
            for caller in direct_callers:
                result.update(forward_graph.get(caller, set()))
            result.update(forward_graph.get(func, set()))
        else:
            raise ValueError(f"Unknown function type for {func}")

    return result

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python analyze_callers.py <reverse_callgraph.txt> <forward_callgraph.txt> <changed_funcs.txt>")
        sys.exit(1)

    reverse_path = sys.argv[1]
    forward_path = sys.argv[2]
    changed_path = sys.argv[3]

    reverse_graph, reverse_locations = parse_cflow_graph(reverse_path)
    forward_graph, forward_locations = parse_cflow_graph(forward_path)

    changed_funcs = load_changed_functions(changed_path)

    # merge location maps (they should be consistent)
    locations = {**forward_locations, **reverse_locations}

    affected = analyze(reverse_graph, forward_graph, locations, changed_funcs)

    print("Affected functions:")
    for f in sorted(affected):
        print(f)
