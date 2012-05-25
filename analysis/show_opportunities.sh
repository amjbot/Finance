#!/bin/bash

cat daily_report.txt | grep NEGLECTED | grep LARGE | less
#cat daily_report.txt | egrep 'LARGE|MEDIUM' | grep growing | less
#cat daily_report.txt | grep -v SMALL | grep growing | less


