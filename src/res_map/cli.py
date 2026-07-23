#!/usr/bin/env python3
"""
res-map: Streamlined Resistome Profiler
Aligns FASTQ (.fastq or .fastq.gz) reads against a DIAMOND protein database
and outputs mapped gene counts and CPM abundances.
"""

import sys
import os
import argparse
import subprocess
import gzip
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser(
        description="res-map: Map metagenomic FASTQ reads against a protein database using DIAMOND."
    )
    parser.add_argument(
        "-i", "--input", required=True, help="Path to input FASTQ file (.fastq or .fastq.gz)"
    )
    parser.add_argument(
        "-d", "--db", required=True, help="Path to DIAMOND database (.dmnd)"
    )
    parser.add_argument(
        "-o", "--outdir", default="resmap_output", help="Output directory [Default: resmap_output]"
    )
    parser.add_argument(
        "-t", "--threads", type=int, default=4, help="Number of CPU threads [Default: 4]"
    )
    parser.add_argument(
        "--id", "--identity", dest="identity", type=float, default=80.0,
        help="Minimum sequence identity percentage [Default: 80]"
    )
    parser.add_argument(
        "--cov", "--coverage", dest="coverage", type=float, default=75.0,
        help="Minimum query coverage percentage [Default: 75]"
    )
    return parser.parse_args()

def count_fastq_reads(fastq_path):
    """Counts total reads in raw or gzipped FASTQ file."""
    print(f"[INFO] Counting total reads in {fastq_path}...")
    read_count = 0
    open_fn = gzip.open if fastq_path.endswith('.gz') else open
    
    try:
        with open_fn(fastq_path, 'rt', encoding='utf-8', errors='ignore') as f:
            for line_idx, _ in enumerate(f):
                if line_idx % 4 == 0:
                    read_count += 1
    except Exception as e:
        sys.exit(f"[ERROR] Failed to read FASTQ file: {e}")
        
    print(f"[INFO] Total reads detected: {read_count:,}")
    return read_count

def run_diamond_alignment(fastq, db, out_m8, threads, identity, coverage):
    """Aligns reads using DIAMOND blastx."""
    print(f"[INFO] Aligning reads against {db} using DIAMOND (Identity: {identity}%, Coverage: {coverage}%)...")
    cmd = [
        "diamond", "blastx",
        "--db", db,
        "--query", fastq,
        "--out", out_m8,
        "--outfmt", "6", "qseqid", "sseqid", "pident", "length", "evalue", "bitscore",
        "--id", str(identity),          
        "--query-cover", str(coverage),  
        "--threads", str(threads),
        "--max-target-seqs", "1"
    ]
    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        sys.exit("[ERROR] 'diamond' executable not found in PATH. Please ensure DIAMOND is installed.")
    except subprocess.CalledProcessError as e:
        sys.exit(f"[ERROR] DIAMOND alignment failed: {e}")

def process_alignments(m8_file, total_reads):
    """Parses alignment results and calculates counts & CPM."""
    print("[INFO] Processing alignments and calculating abundances...")
    
    if not os.path.exists(m8_file) or os.path.getsize(m8_file) == 0:
        print("[WARN] No alignments found in output.")
        return pd.DataFrame()

    align_df = pd.read_csv(
        m8_file, sep="\t", 
        names=["qseqid", "sseqid", "pident", "length", "evalue", "bitscore"]
    )

    if align_df.empty:
        return pd.DataFrame()

    # Aggregate unique mapped reads per target gene/protein
    gene_summary = align_df.groupby('sseqid').agg(
        Mapped_Reads=('qseqid', 'nunique'),
        Avg_Identity=('pident', 'mean'),
        Avg_Alignment_Length=('length', 'mean')
    ).reset_index()

    gene_summary.rename(columns={'sseqid': 'Target_Gene_ID'}, inplace=True)

    # Calculate CPM (Counts Per Million total reads)
    if total_reads > 0:
        gene_summary['CPM'] = (gene_summary['Mapped_Reads'] / total_reads) * 1e6
    else:
        gene_summary['CPM'] = 0.0

    return gene_summary.sort_values(by='Mapped_Reads', ascending=False)

def main():
    args = parse_args()
    os.makedirs(args.outdir, exist_ok=True)

    m8_out = os.path.join(args.outdir, "alignments.m8")
    report_out = os.path.join(args.outdir, "resmap_summary.tsv")

    total_reads = count_fastq_reads(args.input)
    run_diamond_alignment(args.input, args.db, m8_out, args.threads, args.identity, args.coverage)
    
    res_df = process_alignments(m8_out, total_reads)

    if not res_df.empty:
        res_df.to_csv(report_out, sep="\t", index=False)
        print(f"[SUCCESS] Results saved to: {report_out}")
    else:
        print("[INFO] Pipeline finished. No resistance targets were detected above threshold.")

if __name__ == "__main__":
    main()
