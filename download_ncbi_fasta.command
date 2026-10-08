#!/bin/bash
set -euo pipefail

PROJECT_DIR="$HOME/fasta-reader"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

fetch_fasta() {
    local db="$1"
    local accession="$2"
    local filename="$3"
    local url="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=${db}&id=${accession}&rettype=fasta&retmode=text"
    echo "Downloading ${filename} (${accession})..."
    if ! curl --fail --location --silent --show-error --retry 3 --connect-timeout 15 --max-time 90 "$url" -o "${filename}.tmp"; then
        rm -f "${filename}.tmp"
        echo "Download failed: ${filename}. Check internet connection and try again."
        return 1
    fi
    if ! grep -q '^>' "${filename}.tmp"; then
        echo "Unexpected response from NCBI; not saving ${filename}."
        rm -f "${filename}.tmp"
        return 1
    fi
    mv "${filename}.tmp" "$filename"
    echo "Saved: $PROJECT_DIR/$filename"
}

fetch_fasta nuccore NM_000546.6 tp53_mrna.fasta
fetch_fasta protein NP_000537.3 tp53_protein.fasta
fetch_fasta nuccore NC_012920.1 mitochondrion_human.fasta
cat tp53_mrna.fasta mitochondrion_human.fasta > multiple_sequences.fasta

echo
echo "All done. Four FASTA files are in $PROJECT_DIR"
echo "Run: cd ~/fasta-reader && python3 main.py"
echo "Enter a filename, for example tp53_protein.fasta"
