#!/bin/bash
for line in `cat portfolio.txt`; do
    cat daily_report.txt | grep "$line"
done
