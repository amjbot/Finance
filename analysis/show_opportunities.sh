#!/bin/bash

cat daily_report.txt | grep LARGE | grep growing | less
#cat daily_report.txt | grep -v SMALL | grep growing | less


