#!/bin/bash

#
# Convenient bash file to use the awk file with hardcoded input parameter (the dictionary)
#

/usr/bin/awk -f find-undefined.awk -- dictionary.md
