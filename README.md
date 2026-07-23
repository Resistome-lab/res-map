# res-map

Functional Resistome Profiler for Metagenomic Reads.

`res-map` maps raw or compressed metagenomic FASTQ reads directly against a DIAMOND protein database (such as CARD) and outputs quantified gene abundances (mapped read counts and CPM).

---

## 🛠️ Prerequisites

Before using `res-map`, ensure **DIAMOND** is installed and accessible in your system `PATH`:

```bash
# Example Conda installation
conda install -c bioconda diamond

Installation

Install res-map directly from GitHub using pip3:

pip3 install git+[https://github.com/Resistome-lab/res-map.git](https://github.com/Resistome-lab/res-map.git)


To profile a sample FASTQ file against an indexed DIAMOND database (.dmnd):

res-map -i sample.fastq.gz -d card_db.dmnd -o results -t 8

=============================================
Command Line Options
Parameter	Short	Required	Default	Description
--input	-i	Yes	—	Path to input sequencing reads (.fastq or .fastq.gz).
--db	-d	Yes	—	Path to pre-indexed DIAMOND protein database (.dmnd).
--outdir	-o	No	resmap_output	Directory where output files will be saved.
--threads	-t	No	4	Number of CPU cores to assign to DIAMOND alignment.

Output Files

res-map automatically generates two files inside your specified --outdir:

    resmap_summary.tsv: Tabular report containing quantified targets sorted by abundance:

        Target_Gene_ID: Target protein/gene identifier matched.

        Mapped_Reads: Number of unique reads mapped to the gene.

        Avg_Identity: Mean alignment identity percentage (≥80%).

        Avg_Alignment_Length: Mean alignment length in amino acids.

        CPM: Counts Per Million total sequencing reads.

    alignments.m8: Unfiltered tabular alignment results from DIAMOND (--outfmt 6).