#!/bin/sh

snakemake all
chacon verify -i bad_contract.yml