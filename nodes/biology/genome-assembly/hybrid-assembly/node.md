---
tag: PQY156
kind: concept
slug: hybrid-assembly
name: Hybrid assembly
aliases:
- hybrid sequencing assembly
area: biology/genome-assembly
level: advanced
summary: "Genome assembly from two kinds of reads together, usually long error-prone reads that span repeats and short accurate reads that fix the bases."
prereqs: [overlap-layout-consensus, de-bruijn-assembly, consensus-sequence-calling]
see_also: [repeat-resolution, read-error-correction, read-mapping, string-graph, scaffolding, genome-repeat, reference-guided-assembly, assembly-quality-assessment]
sources:
  - paper: doi:10.1038/nbt.2280
    title: Sergey Koren et al., Hybrid error correction and de novo assembly of single-molecule sequencing reads, Nature Biotechnology 30(7), 2012
    locator: pp. 693 to 700, PBcR, correction of long reads with short reads before an OLC assembly
  - paper: doi:10.1093/bioinformatics/btv688
    title: Dmitry Antipov, Anton Korobeynikov, Jeffrey S. McLean and Pavel A. Pevzner, hybridSPAdes, an algorithm for hybrid assembly of short and long reads, Bioinformatics 32(7), 2016
    locator: pp. 1009 to 1015, alignment of long reads to the short-read assembly graph to resolve repeats and close gaps
  - paper: doi:10.1371/journal.pcbi.1005595
    title: Ryan R. Wick, Louise M. Judd, Claire L. Gorrie and Kathryn E. Holt, Unicycler, resolving bacterial genome assemblies from short and long sequencing reads, PLoS Computational Biology 13(6), 2017
    locator: article e1005595, a short-read assembly graph whose repeats are bridged with long reads
  - paper: doi:10.1371/journal.pone.0112963
    title: Bruce J. Walker et al., Pilon, an integrated tool for comprehensive microbial variant detection and genome assembly improvement, PLoS ONE 9(11), 2014
    locator: article e112963, polishing of a draft assembly with aligned short reads
  - paper: doi:10.1101/gr.214270.116
    title: Robert Vaser, Ivan Sović, Niranjan Nagarajan and Mile Šikić, Fast and accurate de novo genome assembly from long uncorrected reads, Genome Research 27(5), 2017
    locator: pp. 737 to 746, consensus polishing of a long-read draft
---

Hybrid assembly is genome assembly from two or more kinds of sequencing reads together, most often long reads with a high error rate and short reads with a low error rate. The long reads span repeats and so give the order of the genome; the short reads give the exact bases. It is a family of workflows, not one algorithm: each workflow chains standard steps such as read mapping, consensus calling and graph assembly in a different order.

## In plain words

Two people copy a long book. The first person copies whole pages at a time but makes many small spelling errors. The second person copies only single lines but almost never makes an error. From the lines alone you cannot tell the order of the pages, because many lines appear on several pages. From the pages alone you get the order, but the text is full of errors.

So you use both. You can fix the spelling of each page with the lines first and then put the pages in order. Or you can put the lines together into short passages and then use the pages to see which passage follows which. Or you can put the pages in order first and fix the spelling at the end.

## The idea

**Model.** The genome has length $G$. There are $N_s$ short reads of length $L_s$, with coverage $c_s = N_s L_s / G$ and mostly substitution errors at a low rate $p_s$, and $N_\ell$ long reads of length $L_\ell$, with coverage $c_\ell = N_\ell L_\ell / G$ and insertion, deletion and substitution errors at a higher rate $p_\ell$. The graph is a [de Bruijn graph](/de-bruijn-assembly/) of the short reads or an overlap or [string graph](/string-graph/) of the long reads. A repeat of length $R$ can be resolved only by reads that cover it and some unique sequence on both sides, so short reads with $L_s < R$ cannot resolve it, and long reads can when $L_\ell > R$.

There are three main orders of the steps. In each one, the algorithmic parts are standard problems with their own pages; what makes the method hybrid is the order and the choice of which read type does which step.

1. **Correct, then assemble.** Map the short reads to each long read and replace the long read by the [consensus](/consensus-sequence-calling/) of the short reads on it. Then assemble the corrected long reads with [overlap-layout-consensus](/overlap-layout-consensus/). PBcR (Koren et al. 2012) works this way. The algorithmic parts are [read mapping](/read-mapping/) and consensus; the result depends on coverage by short reads, and a long-read region without short-read coverage stays uncorrected or is lost.
2. **Assemble short, then bridge with long.** Assemble the short reads into a de Bruijn graph and simplify it. Then align each long read to the graph, as a path through its edges, and use the paths to choose the right exits at each repeat and to close gaps. hybridSPAdes and Unicycler work this way. The algorithmic parts are alignment of a read to a graph and [repeat resolution](/repeat-resolution/) by read paths.
3. **Assemble long, then polish.** Assemble the long reads with an OLC or string graph assembler, polish the draft with long reads, for example with Racon, and then polish it with short reads, for example with Pilon. The algorithmic parts are the long-read assembly and consensus with a fixed alignment.

A fourth order uses the long reads only as links to [scaffold](/scaffolding/) the contigs of a short-read assembly, without using their bases.

**What each read type limits.** The contiguity is limited by the long reads: their length against the repeats, and their coverage, through the [Lander-Waterman](/lander-waterman-model/) gaps. The base accuracy is limited by the short reads, and in regions where short reads do not map uniquely, such as long low-complexity repeats, the polish has no effect. All the bounds that the tools give for their results are observed on test genomes, not proved.

## Examples

**Which repeats can be bridged.** Take long reads of length $L_\ell = 10$ kb at coverage $c_\ell = 10$ on a bacterial genome, so read starts form a Poisson process of rate $c_\ell / L_\ell = 0.001$ per base. To bridge a repeat of length $R$, a read must cover it with at least 500 bases of unique sequence on each side, so it must start in a window of $L_\ell - R - 1000$ bases. The number of such reads is Poisson with mean $0.001 \cdot (L_\ell - R - 1000)$, and the probability that the repeat stays unbridged is the probability of zero:

| $R$ | mean bridging reads | probability unbridged |
|---|---|---|
| 3 kb | 6 | 0.0025 |
| 5 kb | 4 | 0.018 |
| 7 kb | 2 | 0.135 |
| 9 kb or more | 0 | 1 |

Short reads of 150 bases give 0 bridging reads for every repeat longer than about 150 bases. A hybrid assembly in the second order thus resolves the repeats up to about 5 to 7 kb in this setting and leaves the longer ones as branches of the graph.

**Base accuracy after polishing.** If the long reads have $p_\ell = 0.1$, a majority vote of 5 long reads with independent errors is wrong at a given base with probability up to 0.00856, which is quality 20.7, by the calculation on the [consensus calling](/consensus-sequence-calling/) page. Errors of long reads are often not independent, for example in runs of one base. Short reads with a much lower error rate and independent errors bring the vote error far below that, which is why the last polish in the third order uses short reads.

## Where it is used

- Bacterial genomes: moderate long-read coverage plus short reads often give one contig for each chromosome and plasmid, as Unicycler reports on its test genomes.
- Older long-read data with high error rates, where short-read correction or polishing was needed to reach usable base accuracy.
- Large genomes where long-read coverage is low for cost reasons, so that long reads give the layout and cheaper short reads give the depth.
- Finishing: long reads that close the gaps between short-read contigs, as a form of [gap filling](/gap-filling/).
- Less often with accurate long reads, which give both contiguity and base accuracy by themselves; then short reads serve mainly for [quality assessment](/assembly-quality-assessment/), for example for the $k$-mer QV.

## References
