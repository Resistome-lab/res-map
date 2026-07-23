#!/usr/bin/env python3
import sys
import os
import argparse
import subprocess
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser(description="res-map: Map metagenomic reads to AMR databases and quantify gene abundance.")
    parser.add_argument("-i", "--input", required=True, help="Input FASTQ file")
    parser.add_argument("-d", "--db", required=True, help="Path to DIAMOND AMR protein database (.dmnd)")
    parser.add_argument("-m", "--mapping-info", required=True, help="TSV mapping file")
    parser.add_argument("-o", "--outdir", default="resmap_output", help="Output directory")
    parser.add_argument("-t", "--threads", type=int, default=4, help="Number of CPU threads")
    return parser.parse_args()

def main():
    args = parse_args()
    print("[INFO] res-map CLI executing...")

if __name__ == "__main__":
    main()
