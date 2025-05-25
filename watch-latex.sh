#!/bin/bash

if [ $# -eq 0 ]; then
  echo "Usage: $0 <latex-file>"
  echo "Example: $0 document.tex"
  exit 1
fi

# Get the input file
TEX_FILE="$1"

# Check if file exists
if [ ! -f "$TEX_FILE" ]; then
  echo "Error: File '$TEX_FILE' not found!"
  exit 1
fi

# Check if file ends with .tex
if [[ ! "$TEX_FILE" =~ \.tex$ ]]; then
  echo "Error: File must be a .tex file!"
  exit 1
fi

echo "Watching $TEX_FILE for changes..."
nodemon --ext tex --watch "$TEX_FILE" --exec "pdflatex -shell-escape \"$TEX_FILE\""
