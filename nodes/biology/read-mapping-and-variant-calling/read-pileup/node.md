---
tag: 3YBHSY
kind: definition
slug: read-pileup
name: Read pileup
aliases:
- pileup format
area: biology/read-mapping-and-variant-calling
level: intro
summary: For each reference position, the bases, qualities and strands of all mapped reads that cover it. It is the column view of an alignment and the input of per-site variant callers.
prereqs: [sam-alignment-format, phred-quality-score]
see_also: [sequencing-coverage, genotype-likelihood, bayesian-genotype-calling, variant-calling-problem, mapping-quality, duplicate-read-marking, base-quality-score-recalibration, interval-tree]
sources:
  - paper: doi:10.1093/bioinformatics/btp352
    title: Heng Li, Bob Handsaker, Alec Wysoker, Tim Fennell, Jue Ruan, Nils Homer, Gabor Marth, Goncalo Abecasis, Richard Durbin and 1000 Genome Project Data Processing Subgroup, The Sequence Alignment/Map format and SAMtools, Bioinformatics 25(16), 2009
    locator: pp. 2078 to 2079 (the pileup output of SAMtools)
  - url: https://www.htslib.org/doc/samtools-mpileup.html
    title: samtools mpileup manual page, samtools 1.25
    locator: the sections on the pileup format and on the options --min-BQ, --max-depth and the default read filters
  - paper: doi:10.1093/bioinformatics/btr509
    title: Heng Li, A statistical framework for SNP calling, mutation discovery, association mapping and population genetical parameter estimation from sequencing data, Bioinformatics 27(21), 2011
    locator: Section 2 (the per-site data that the likelihoods use)
---

A read pileup turns the read-by-read view of an alignment into a position-by-position view. For each position of the reference it lists every mapped read that covers the position, with the base that the read has there, its quality and its strand. A variant caller that works one site at a time, such as [Bayesian genotype calling](/bayesian-genotype-calling/), reads its data from the pileup column of the site. The `samtools mpileup` command writes pileups as text, and that layout is often called the pileup format.

## Definition

Positions are 1-based in this page, as in [SAM](/sam-alignment-format/) and in the pileup format. Fix a set of alignment records, each with a reference name, a leftmost position POS, a CIGAR string, a strand, a mapping quality, a sequence and base qualities.

**Pileup column.** The pileup column at reference position $j$ is the list, in the order of the read start positions, of one entry for each record that passes the read filters and whose alignment covers $j$:

- if a read base is aligned to $j$ (by an M, = or X operation), the entry is $(b, Q, s, m, k)$: the base $b$, its quality $Q$, the strand $s$, the [mapping quality](/mapping-quality/) $m$ of the read, and the position $k$ of the base in the read;
- if $j$ lies in a deletion (D) of the read, the entry marks a deleted base;
- if $j$ lies in a skipped region (N), the read does not count as covering $j$ for variant calling, though `mpileup` shows it with its own mark.

Inserted bases (I) are not aligned to any reference position. The pileup attaches an insertion to the column of the reference base before it.

**Depth.** The depth $d_j$ is the number of entries of column $j$. Averaged over the positions, the depth is the [coverage](/sequencing-coverage/) $c = N L / G$ for $N$ reads of length $L$ on a genome of length $G$, minus the reads and bases that the filters remove.

**Filters.** A pileup is always taken after filters, and the result depends on them. The defaults of `samtools mpileup` drop unmapped, secondary, QC-failed and duplicate records, drop bases with quality below 13 (`--min-BQ`), and stop at a depth of 8000 reads per file (`--max-depth`). A caller often also drops reads with a low mapping quality. These are the tool's defaults, not part of the definition.

**Text format.** `samtools mpileup` writes one line per position with at least these columns: reference name, position, reference base, depth, read bases and base qualities. In the read bases column:

| symbol | meaning |
|---|---|
| `.` and `,` | a match to the reference on the forward and on the reverse strand |
| `ACGTN` and `acgtn` | a mismatch on the forward and on the reverse strand |
| `*` | a deleted base (`#` for the reverse strand with the option `--reverse-del`) |
| `>` and `<` | a reference skip (N) |
| `^` and one character | the start of a read, followed by its mapping quality as the ASCII code MAPQ + 33 |
| `$` | the end of a read |
| `+3ACG` | an insertion of the 3 bases ACG after this position |
| `-2CA` | a deletion of the 2 reference bases CA that follow this position |

The base qualities column has one character, $Q + 33$, for each base or deletion of the read bases column.

**Construction.** In a file sorted by position, a pileup is made by a sweep: keep the list of reads that are active at the current position, add the reads whose POS is reached, walk each active read's CIGAR string one position forward, and drop the reads whose alignment has ended. With $R$ records and $B$ aligned bases in total, the sweep takes $O(R + B)$ time plus the output, and its memory is the largest depth.

## Examples and non-examples

The SAM specification has an example with the reference `AGCATGTTAGATAAGATAGCTGTGCTAGTAGGCAGTCAGCGCCAT` and four forward-strand reads, all with mapping quality 30: r001 at 7 with CIGAR 8M2I4M1D3M, r002 at 9 with 3S6M1P1I4M, r003 at 9 with 5S6M, and r004 at 16 with 6M14N5M. Its records have no base qualities, so the quality column is left out here.

| pos | ref | depth | read bases | what happens |
|---|---|---|---|---|
| 14 | A | 3 | `.+2AG.+1G.$` | r001 and r002 match and each has an insertion after this base; r003 matches and ends |
| 16 | A | 3 | `..^?.` | r001 and r002 match; r004 starts here with MAPQ 30 (code 63, `?`) and matches |
| 18 | A | 3 | `.-1G.$.` | r001 matches and deletes the next reference base G; r002 matches and ends; r004 matches |
| 19 | G | 2 | `*.` | r001 has the deleted base; r004 matches |

At position 14, r003's six aligned bases AGCTAA cover 9 to 14 and r002's bases AGATAA cover 9 to 14 too, so all three reads end their first block of aligned bases there, and the two insertions sit between 14 and 15.

**A column for a genotype call.** Take a column at a site with reference base A whose read bases are `..,GgG` with qualities 30, 30, 20, 30, 20, 10. The caller reads three A and three G, with those qualities; strand does not enter the simple error model. This is the example of [genotype likelihood](/genotype-likelihood/), which gives PL 56, 0, 76.

**Non-example: depth is not coverage of one read.** A depth of 30 at a position does not mean 30 different DNA fragments. Without [duplicate marking](/duplicate-read-marking/), copies of one fragment made in PCR count as separate reads, and the two mates of a short fragment can both cover the same position. Callers that count each base as independent evidence then trust the column too much.

**Non-example: a pileup is not a multiple alignment.** Each read is aligned to the reference on its own. Two reads with the same indel can have it at different places in a repeat, so the pileup shows two different events. Local realignment, or callers that assemble the reads of a region again, fix this.

## Related definitions

- **Coverage and depth.** The mean depth over the genome is the [sequencing coverage](/sequencing-coverage/), and the share of positions with depth 0 follows the [Lander-Waterman model](/lander-waterman-model/) for uniform reads.
- **Genotype likelihood.** A function of one pileup column; see [genotype likelihood](/genotype-likelihood/).
- **Interval queries.** Getting the reads that overlap one region from an indexed file is an interval query; an [interval tree](/interval-tree/) answers the same question in memory.
- **Base and mapping qualities.** The two quality columns of the format use the [Phred scale](/phred-quality-score/); see also [mapping quality](/mapping-quality/).

## References
