#!/bin/bash
cat food.csv \
    | awk 'BEGIN { FS = "," } ; { print $12 }' \
    | sort \
    | tr ":" "\n" \
    | sed 's/^\s*//' \
    | tr '[:upper:]' '[:lower:]' \
    | sort \
    | uniq -c \
    | sort -n -k 1
