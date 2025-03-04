#!/bin/bash

./ghidra/*/support/analyzeHeadless ./projects decompile -import $1 -deleteProject -overwrite -postScript decompile.py