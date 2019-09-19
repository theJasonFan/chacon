#!/bin/sh

snakemake all
snakemake -D all > output/summary.tsv

chacon create -i output/summary.tsv -o output/contract.yml
chacon verify -i output/contract.yml