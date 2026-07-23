# res-map

Functional Resistome Profiler for Metagenomic Reads.

`res-map` translates and aligns metagenomic FASTQ reads against a protein database via `diamond blastx` and outputs mapped read counts and normalized CPM abundances.

---

# 📦 PART 1: INSTALLATION & SETUP

### Step 1: Install `res-map`
Install or update the package directly from GitHub using `pip3` in your Linux/WSL environment:

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


