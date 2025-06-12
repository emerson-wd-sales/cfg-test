# echo $1 $2
git diff -U0 $1 $2 -- '*.c'   | grep '^@@'   | sed -E 's/^@@.*\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\(.*/\1/' | uniq