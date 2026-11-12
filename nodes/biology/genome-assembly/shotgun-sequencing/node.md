---
tag: HZVJC3
kind: concept
slug: shotgun-sequencing
name: Shotgun sequencing
aliases:
- whole-genome shotgun sequencing
area: biology/genome-assembly
level: intro
summary: Break many copies of a genome into random fragments, read a short stretch of each, and rebuild the genome from the overlaps of the reads by computer.
prereqs: []
see_also: [genome-assembly-problem, sequencing-coverage, lander-waterman-model, paired-end-reads, genome-repeat, read-error-correction, overlap-layout-consensus, de-bruijn-assembly]
sources:
  - paper: doi:10.1093/nar/6.7.2601
    title: Rodger Staden, A strategy of DNA sequencing employing computer programs, Nucleic Acids Research 6(7) (1979)
    locator: pp. 2601 to 2610
  - paper: doi:10.1016/0022-2836(82)90546-0
    title: F. Sanger, A. R. Coulson, G. F. Hong, D. F. Hill and G. B. Petersen, Nucleotide sequence of bacteriophage lambda DNA, Journal of Molecular Biology 162(4) (1982)
    locator: pp. 729 to 773
  - paper: doi:10.1016/0888-7543(88)90007-9
    title: Eric S. Lander and Michael S. Waterman, Genomic mapping by fingerprinting random clones, a mathematical analysis, Genomics 2(3) (1988)
    locator: pp. 231 to 239, Section 2 (the remark that the results also apply to shotgun sequencing, p. 232)
  - paper: doi:10.1126/science.7542800
    title: Robert D. Fleischmann et al., Whole-genome random sequencing and assembly of Haemophilus influenzae Rd, Science 269(5223) (1995)
    locator: pp. 496 to 512
  - paper: doi:10.1101/gr.7.5.401
    title: James L. Weber and Eugene W. Myers, Human whole-genome shotgun sequencing, Genome Research 7(5) (1997)
    locator: pp. 401 to 409
  - book: isbn:9780990374602
    title: Phillip Compeau and Pavel Pevzner, Bioinformatics Algorithms, An Active Learning Approach, Volume I, second edition
    locator: Chapter 3, How do we assemble genomes?
---

Shotgun sequencing reads a long DNA molecule by breaking many copies of it into random fragments, reading a short stretch (a *read*) from each fragment, and putting the reads back together by computer. The sequencer cannot read a whole chromosome from end to end, but it can read millions of short pieces at once. The price is a computational task, the [genome assembly problem](/genome-assembly-problem/): find the genome from the reads, without knowing where each read came from. How much of the genome the reads cover is the subject of [sequencing coverage](/sequencing-coverage/) and the [Lander-Waterman model](/lander-waterman-model/).

## In plain words

Take a hundred copies of the same newspaper and run them all through a shredder. Each strip of paper shows a few words. Nobody tells you where a strip came from. You can still rebuild the page: two strips that end and start with the same words were probably next to each other. With enough copies, the strips overlap everywhere, and you can chain them from the first word of the page to the last.

Shotgun sequencing does this with DNA. The machine reads short strips from random places on many copies of the genome. A computer then finds the overlaps and joins the strips. Two things make the work hard. The machine makes some reading mistakes. And a genome repeats some long passages many times, so two strips can match by accident: they look the same, but come from different places.

## The idea

### The data

Let the genome be a string $S$ of length $G$ over the alphabet $\{A, C, G, T\}$. DNA has two strands. The second strand is the *reverse complement* $\overline{S}$: reverse $S$ and swap $A \leftrightarrow T$ and $C \leftrightarrow G$. A shotgun experiment produces $N$ reads $r_1, \ldots, r_N$, each of length about $L$. Read $r_i$ is a noisy copy of either $S[p_i \ldots p_i + L - 1]$ or its reverse complement, for a start position $p_i$ and a strand that the experiment does not record. Three facts define the setting:

- **The positions are random and unknown.** The fragments come from random breaks in the DNA. The standard model takes the start positions as independent and uniform on $[0, G - L]$. This is the model of [Lander and Waterman](/lander-waterman-model/).
- **The strand is unknown.** A read is equally likely to come from either strand. So an assembler compares each read with the other reads and with their reverse complements.
- **The reads have errors.** Each read differs from the genome in a small fraction of its bases. The error model depends on the machine. Sanger and Illumina reads have mostly substitutions. Single-molecule long reads have more insertions and deletions.

The *coverage* is $c = NL/G$, the mean number of reads that contain a given base. The reads cover the genome with gaps when $c$ is small. The expected number of gaps is about $N e^{-c}$, which is the main result of the [Lander-Waterman model](/lander-waterman-model/).

### From reads to a genome

The computer does not know the positions $p_i$. It must infer the order of the reads from the reads themselves. Two reads that come from overlapping places share a string: a suffix of one equals a prefix of the other, up to errors. The classical method, [overlap-layout-consensus](/overlap-layout-consensus/), finds these overlaps, lays out the reads in a consistent order, and takes a consensus of the bases in each column. Short reads are often assembled with a [de Bruijn graph](/de-bruijn-graph/) of their [k-mers](/kmer/) instead; see [de Bruijn assembly](/de-bruijn-assembly/).

Repeats limit what any method can do. A [genome repeat](/genome-repeat/) longer than the reads makes reads from different copies look the same. Then the reads alone do not tell how the regions between the copies are joined. [Paired-end reads](/paired-end-reads/) help: they give two reads at a known distance, which can span a repeat. The result of an assembly is a set of [contigs](/contig/) (gap-free stretches), often ordered into [scaffolds](/scaffold/).

### Whole-genome and clone-by-clone shotgun

The first shotgun projects sequenced one clone of a few tens of kilobases at a time. For a large genome, the *hierarchical* or clone-by-clone method first breaks the genome into large clones, maps their order, and then shotgun sequences each clone. *Whole-genome shotgun* sequencing skips the map: it shreds the whole genome at once and relies on the assembler and on read pairs to put the pieces in order. Weber and Myers proposed this for the human genome in 1997. Today almost all genome projects use whole-genome shotgun data.

## Examples

**A toy genome.** Let $S = \texttt{CAGTTCGATGGC}$ ($G = 12$). Four reads of length $L = 5$ start at positions 0, 3, 5 and 7:

| read | start | sequence |
|---|---|---|
| $r_1$ | 0 | CAGTT |
| $r_2$ | 3 | TTCGA |
| $r_3$ | 5 | CGATG |
| $r_4$ | 7 | ATGGC |

The coverage is $c = 4 \cdot 5 / 12 \approx 1.67$. Without the positions, the overlaps give the order. The suffix TT of $r_1$ is a prefix of $r_2$ (overlap 2). The suffix CGA of $r_2$ is a prefix of $r_3$ (overlap 3). The suffix ATG of $r_3$ is a prefix of $r_4$ (overlap 3). Merging the reads along these overlaps gives CAGTT + CGA + TG + GC = CAGTTCGATGGC, which is $S$. If the read from position 4 came from the other strand, the machine would report ATCGA, the reverse complement of TCGAT. The assembler finds its place only after it reverse-complements the read.

**Historical genomes.** Sanger and colleagues sequenced the 48,502 base pairs of bacteriophage lambda in 1982 with a shotgun method. In 1995 Fleischmann and colleagues assembled the 1.83 million base pairs of the bacterium *Haemophilus influenzae* from whole-genome shotgun reads, the first complete genome of a free-living organism.

**A modern human run.** For a human genome, $G \approx 3.1 \times 10^9$. At coverage $c = 30$ with reads of $L = 150$ bases, the run has $N = cG/L = 6.2 \times 10^8$ reads.

## Where it is used

- Almost all de novo genome sequencing. The [genome assembly problem](/genome-assembly-problem/) is the computational half of the method.
- Resequencing. When a reference genome exists, the reads are placed by [read mapping](/read-mapping/) instead of assembly.
- The planning of a project. The [Lander-Waterman model](/lander-waterman-model/) and [sequencing coverage](/sequencing-coverage/) tell how many reads give how many gaps.
- The [k-mer spectrum](/kmer-spectrum/) of shotgun reads estimates the genome size and the error rate before any assembly.
- Read correction: [read error correction](/read-error-correction/) uses the redundancy of the reads to fix errors.

## References
