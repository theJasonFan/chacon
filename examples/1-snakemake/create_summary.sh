#!/bin/sh

snakemake all
snakemake -D all > output/summary.tsv