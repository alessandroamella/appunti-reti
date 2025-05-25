#!/bin/bash

# Initialize variables
DARK_MODE=false
TEX_FILE=""

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
  --dark)
    DARK_MODE=true
    shift
    ;;
  --*)
    echo "Unknown option $1"
    exit 1
    ;;
  *)
    if [ -z "$TEX_FILE" ]; then
      TEX_FILE="$1"
    else
      echo "Error: Multiple input files specified"
      exit 1
    fi
    shift
    ;;
  esac
done

# Check if a file was provided
if [ -z "$TEX_FILE" ]; then
  echo "Usage: $0 [--dark] <latex-file>"
  echo "Example: $0 document.tex"
  echo "         $0 --dark document.tex"
  exit 1
fi

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

# Prepare the generate_preamble command
PREAMBLE_CMD="./generate_preamble.sh"
if [ "$DARK_MODE" = true ]; then
  PREAMBLE_CMD="$PREAMBLE_CMD --dark"
fi

echo "Watching $TEX_FILE for changes..."
nodemon --ext tex --watch "$TEX_FILE" --exec "$PREAMBLE_CMD && pdflatex -shell-escape \"$TEX_FILE\""
