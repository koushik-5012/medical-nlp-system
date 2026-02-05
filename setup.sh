#!/bin/bash
set -e

echo "Installing spaCy models..."
python -m spacy download en_core_web_sm

echo "Models installed successfully!"
