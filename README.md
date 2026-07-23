# res-map

Functional Resistome Profiler for Metagenomic Reads.

`res-map` translates and aligns metagenomic FASTQ reads against a protein database via `diamond blastx` and outputs mapped read counts and normalized CPM abundances.

---

# PART 1: INSTALLATION & SETUP

### Step 1: Install `res-map`
Install res-map directly from GitHub using `pip3` in your Linux/WSL environment:

```bash
pip3 install git+https://github.com/Resistome-lab/res-map.git

```
Note: If res-map returns command not found after installation, add Python's user binary path to your environment:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

Step 2: Install perequisites

res-map requires DIAMOND to perform read alignments. Install it via Conda:
```bash
conda install -c bioconda diamond
```

# PART 2: HOW TO USE IT

### Step 1: Prepare your `DIAMOND` database
If you don't already have a .dmnd database file (such as CARD resistance proteins), index your reference FASTA file using `DIAMOND`:

```bash
diamond makeblastdb --in card_proteins.fasta -d card_db
```
This command generates your reference database file: card_db.dmnd.

### Step 2: Run `res-map` on your metagenomic reads
To profile a sample FASTQ file (.fastq or compressed .fastq.gz), pass your input reads and `DIAMOND` database to `res-map`:
```bash
res-map --input sample.fastq.gz --db card_db.dmnd --outdir results_sample1 --threads 8
```
You can change the options and file names according to your settings.

###Step 3: look for the output files
`res-map` automatically creates two output files inside your specified output directory (`--outdir`):
1) `resmap_summary.tsv`: Quantified target summary sorted by mapped read abundance:
a) `Target_Gene_ID`: Matched reference protein/gene header.
b) `Mapped_Reads`: Count of unique reads mapped to the target.
c) `Avg_Identity`: Mean alignment identity percentage ($\ge 80\%$).
d) `Avg_Alignment_Length`: Mean alignment length in amino acids.
e) `CPM`: Counts Per Million total sequencing reads.

2) `alignments.m8`: Unfiltered tabular alignment output generated directly by `DIAMOND` (`--outfmt 6`).