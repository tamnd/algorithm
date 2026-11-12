---
tag: 7B82N7
kind: problem
slug: consensus-sequence-calling
name: Consensus sequence calling
aliases:
- assembly polishing
- consensus calling
area: biology/genome-assembly
level: core
summary: "Compute the sequence of a contig from the reads placed on it: the most likely base, or gap, in each column of their alignment. Polishing repeats this on a draft assembly."
prereqs: [consensus-sequence, overlap-layout-consensus, read-mapping]
see_also: [partial-order-alignment, overlap-detection, hybrid-assembly, read-error-correction, assembly-quality-assessment, sequencing-coverage, multiple-sequence-alignment]
sources:
  - paper: doi:10.1007/BF01188580
    title: John D. Kececioglu and Eugene W. Myers, Combinatorial algorithms for DNA sequence assembly, Algorithmica 13(1/2), 1995
    locator: pp. 7 to 51, the consensus phase as a multiple alignment of the reads of a layout
  - paper: doi:10.1093/bioinformatics/18.3.452
    title: Christopher Lee, Catherine Grasso and Mark F. Sharlow, Multiple sequence alignment using partial order graphs, Bioinformatics 18(3), 2002
    locator: pp. 452 to 464, partial-order alignment of sequences to a graph
  - paper: "Christopher Lee, Generating consensus sequences from partial order multiple sequence alignment graphs, Bioinformatics 19(8), 2003"
    title: Lee 2003
    locator: pp. 999 to 1008, consensus paths through a partial-order alignment graph
  - paper: doi:10.1101/gr.214270.116
    title: Robert Vaser, Ivan Sović, Niranjan Nagarajan and Mile Šikić, Fast and accurate de novo genome assembly from long uncorrected reads, Genome Research 27(5), 2017
    locator: pp. 737 to 746, Racon, consensus of a draft by partial-order alignment of the mapped reads in windows
  - paper: doi:10.1371/journal.pone.0112963
    title: Bruce J. Walker et al., Pilon, an integrated tool for comprehensive microbial variant detection and genome assembly improvement, PLoS ONE 9(11), 2014
    locator: article e112963, polishing of a draft assembly with aligned short reads
  - paper: doi:10.1016/s0304-3975(97)00240-5
    title: Colin de la Higuera and Francisco Casacuberta, Topology of strings, median string is NP-complete, Theoretical Computer Science 230(1-2), 2000
    locator: pp. 39 to 48, NP-completeness of the median string under the edit distance
---

Consensus sequence calling is the problem of computing the sequence of a contig from the reads that an assembler placed on it, by choosing in each column of their alignment the most likely base or a gap. It is the last step of [overlap-layout-consensus](/overlap-layout-consensus/) assembly. When the reads are aligned again to a finished draft and the draft is corrected, the same problem is called polishing. This page treats consensus in assembly; the general notion of one string that sums up a set of sequences is the [consensus sequence](/consensus-sequence/).

## In plain words

Several copies of the same passage were typed by careless typists, and each copy has a few typing errors at different places. To get the passage back, put the copies one under the other, so that the same words are in the same columns. Then, in each column, take the letter that most copies agree on.

Errors at different places are voted away, because at each place most copies are right. Two problems remain. If a typist adds or drops a letter, the copies no longer line up, and you must first find the right alignment. If all typists tend to make the same error at the same place, the vote keeps the error.

## Definition

**Model.** The genome is a string of length $G$, sequenced by $N$ reads of length about $L$, so the mean coverage is $c = NL/G$ and a column has about $c$ reads. In the substitution model each base of read $i$ is wrong with probability $p_i$, independently, and a wrong base is one of the other three bases with equal probability. The Phred quality of a base with error probability $p$ is $q = -10 \log_{10} p$. Real reads also have insertions and deletions; long reads have them more often than substitutions.

**Consensus with a fixed alignment.** Input: a multiple alignment of the reads of one contig, as a matrix whose columns hold bases and gap symbols, and optional base qualities. Output: for each column, one symbol, base or gap, and the contig is the sequence of the chosen bases. The objective is the most likely contig under the error model.

**Consensus with an unknown alignment.** Input: the reads of a contig and their approximate positions from the layout or from [read mapping](/read-mapping/). Output: a sequence $S$ that maximizes the likelihood of the reads, or, in the simplest form, minimizes the sum of the edit distances from $S$ to the read segments. In this form the alignment and the consensus are found together.

**Polishing.** Input: a draft contig $D$ and reads, possibly from another technology. Output: a corrected contig, computed by aligning the reads to $D$ and calling the consensus of the alignment, often repeated a few times.

## Variants

- **Majority vote.** Choose the most frequent symbol of each column, gaps included. This is the maximum-likelihood choice when all reads have the same error rate; see the derivation below.
- **Quality-weighted vote.** With different error rates, give read $i$ the weight $w_i = \log \frac{3(1 - p_i)}{p_i}$ and choose the base with the largest sum of weights.
- **Graph consensus.** Align the reads into a [partial-order alignment](/partial-order-alignment/) graph and output the heaviest path, as in Racon. The graph keeps the alternative indel placements apart without forcing one row layout.
- **Short-read polishing.** Align accurate short reads to a long-read draft and correct substitutions and small indels, as in Pilon. This is the consensus step of many [hybrid assemblies](/hybrid-assembly/).
- **Diploid consensus.** In a diploid genome a column can have two true bases, one for each haplotype. A haploid vote then picks one of them, or the error rate is overestimated at heterozygous sites.

## Examples

**A pileup.** Five reads cover the region `ACGTTAC`. Read 3 has a substitution, read 4 has an extra `T` and read 5 has lost a `T`:

| read | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| 1 | A | C | G | T | T | - | A | C |
| 2 | A | C | G | T | T | - | A | C |
| 3 | A | C | **C** | T | T | - | A | C |
| 4 | A | C | G | T | T | **T** | A | C |
| 5 | A | C | G | T | **-** | - | A | C |
| vote | A | C | G | T | T | - | A | C |

Column 3 has four `G` and one `C`, column 5 has four `T` and one gap, and column 6 has four gaps and one `T`. The consensus without gaps is `ACGTTAC`. The alignment places both indels at the end of the run `TT`; if read 4 put its extra `T` in the column before the run, the votes for the run would split across two columns. Consensus tools therefore align indels in runs in one fixed way, for example to the left.

**The vote is maximum likelihood.** In one column, let read $i$ show the symbol $s_i$. Under the substitution model, the likelihood of the true base $b$ is
$$ \prod_{i : s_i = b} (1 - p_i) \prod_{i : s_i \ne b} \frac{p_i}{3} . $$
Divide by $\prod_i p_i / 3$, which does not depend on $b$, and take logarithms: the best $b$ maximizes $\sum_{i : s_i = b} w_i$ with $w_i = \log \frac{3(1 - p_i)}{p_i}$. With equal $p_i$ all weights are equal, and the best base is the most frequent one. With qualities, two reads that show `A` at quality 10 ($p = 0.1$) have the weight $2 \log_{10} 27 \approx 2.86$, and one read that shows `C` at quality 30 ($p = 0.001$) has the weight $\log_{10} 2997 \approx 3.48$, so the call is `C`.

**How accurate is the vote.** Take a column with $c = 5$ reads and $p = 0.1$, and suppose all wrong reads show the same wrong base, which is the worst case. The vote is wrong when at least 3 reads are wrong:
$$ \sum_{j = 3}^{5} \binom{5}{j} p^j (1 - p)^{5 - j} = \frac{107}{12500} = 0.00856 , $$
which is quality 20.7. If the wrong bases are spread at random over the three other bases and ties are broken at random, the error is 0.00406, quality 23.9. For $p = 0.15$ the two values are 0.0266 and 0.0131. For odd $c$ and $p < 1/2$, the worst-case error is at most $(4p(1 - p))^{c/2}$ by the Chernoff bound, so it falls exponentially in the coverage while the errors stay independent.

## Known algorithms

- **Column vote over a layout.** Place the reads at the offsets of the layout, align them to each other or to a running consensus, and vote in each column. Given the alignment, the vote costs $O(n)$ for $n$ aligned symbols, worst case.
- **Iterative realignment.** Align each read to the current consensus with [banded alignment](/banded-alignment/), recompute the consensus, and repeat until it does not change. Each round costs $O(n \cdot b)$ for bandwidth $b$. This is a local search: it can stop at a consensus that is not the best.
- **Partial-order alignment.** Add the reads one by one to a graph by dynamic programming against the graph, at $O(|r| \cdot |V|)$ time for a read $r$ and a graph with $|V|$ nodes, then output the heaviest path. The result depends on the order of the reads, so it is a heuristic. Racon splits the draft into windows and runs POA in each window.
- **Short-read polishing.** Map short reads to the draft, collect the pileup of each position, and change the bases and small indels where the reads disagree with the draft with strong support. Pilon also finds local misassemblies from the read pairs. The decisions use thresholds, so this is a heuristic.

## Bounds

- **Fixed alignment.** The maximum-likelihood consensus under the substitution model is computed column by column in linear time, because the columns are independent given the alignment.
- **Unknown alignment.** The string that minimizes the sum of edit distances to a set of strings is the median string, and finding it is NP-hard (de la Higuera and Casacuberta 2000). So exact consensus with unknown alignment is NP-hard in general, and all practical methods fix an alignment first or use local search.
- **Coverage.** With independent errors, the error of a majority vote falls exponentially in $c$, as above. Errors that repeat at the same place in many reads, such as the length of long runs of one base in some technologies, are not independent, and more coverage does not remove them.

## Reductions

- **From multiple alignment.** Given a [multiple sequence alignment](/multiple-sequence-alignment/) of the reads, consensus is a vote per column; the hard part is the alignment.
- **To the median string.** Consensus with unknown alignment and unit edit costs is the median string problem on the read segments; see [consensus sequence](/consensus-sequence/).
- **From read mapping.** Polishing reduces to [read mapping](/read-mapping/) of all reads to the draft, followed by a consensus with a fixed alignment.

## Applications

- The consensus step of [overlap-layout-consensus](/overlap-layout-consensus/) assembly, which gives each contig its sequence.
- Polishing of long-read drafts with long reads (Racon) or with short reads (Pilon), and the last step of [hybrid assembly](/hybrid-assembly/).
- Self-correction of long reads, where the reads that overlap a read give the pileup; see [read error correction](/read-error-correction/).
- Measuring base accuracy: the disagreement between the reads and the consensus gives an estimate of the read error rate, and [assembly quality assessment](/assembly-quality-assessment/) uses consensus quality values.

## References
