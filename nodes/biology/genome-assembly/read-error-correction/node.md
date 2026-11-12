---
tag: R4AMXT
kind: problem
slug: read-error-correction
name: Read error correction
aliases:
- sequencing error correction
area: biology/genome-assembly
level: core
summary: Find and fix the sequencing errors in reads, using the other reads. The usual method trusts k-mers that occur often and edits each read until all its k-mers are trusted.
prereqs: [kmer-spectrum, hamming-distance]
see_also: [kmer-spectrum, kmer-counting, de-bruijn-graph, hamming-distance, edit-distance, tip-removal, bubble-popping, consensus-sequence-calling]
sources:
  - paper: doi:10.1073/pnas.171285098
    title: Pavel A. Pevzner, Haixu Tang and Michael S. Waterman, An Eulerian path approach to DNA fragment assembly, PNAS 98(17) (2001)
    locator: pp. 9748 to 9753 (solid and weak l-tuples, the Spectral Alignment Problem and the Error Correction Problem, and the results on the N. meningitidis data)
  - paper: doi:10.1186/gb-2010-11-11-r116
    title: David R. Kelley, Michael C. Schatz and Steven L. Salzberg, Quake, quality-aware detection and correction of sequencing errors, Genome Biology 11(11) (2010)
    locator: Article R116 (q-mer counts, the trusted k-mer cutoff, the likelihood-ordered search, and the survey of other correction methods)
  - book: isbn:9781107078536
    title: Veli Mäkinen, Djamal Belazzougui, Fabio Cunial and Alexandru I. Tomescu, Genome-Scale Algorithm Design, Cambridge University Press (2015)
    locator: Chapter 13, Fragment assembly
---

Read error correction is the problem of finding and fixing the sequencing errors in a set of reads before they are used. It works because of redundancy: at coverage $c$, each base of the genome is read about $c$ times, and an error in one read disagrees with the other copies. The common method is spectrum based. A [k-mer](/kmer/) that occurs many times in the reads is *solid* (trusted); one that occurs once or twice is *weak* and probably holds an error. Each read is then changed by as few edits as possible so that all of its k-mers are solid. Pevzner, Tang and Waterman stated this as the Spectral Alignment Problem in 2001, and Quake added base quality values to choose the most likely correction.

## In plain words

Imagine fifty people copy the same letter by hand, each copying a different random part of it, and each makes a few spelling mistakes. To fix one copy, look at its words. A word that many other copies also contain is probably right. A word that no other copy contains is probably a mistake.

Now find the smallest change that makes every word of the copy a common word. If one letter is wrong, all the words that contain that letter look strange, and the letter they share is the one to fix. Try the other letters in that place and keep the one that turns all the strange words into common words. If no small change works, cut off the bad end of the copy or throw it away.

## Definition

Let $R = \{r_1, \ldots, r_N\}$ be reads, each a copy of a substring of a genome $S$ (or of its reverse complement) with some errors. Let $\text{count}(x)$ be the number of occurrences of the k-mer $x$ in $R$, from [k-mer counting](/kmer-counting/), and fix a threshold $M$.

- A k-mer $x$ is **solid** if $\text{count}(x) > M$ and **weak** otherwise. Let $T$ be the set of solid k-mers.
- A string is a **$T$-string** if all of its k-mers are in $T$.

**Spectral Alignment Problem** (Pevzner, Tang and Waterman). Given a read $s$ and the set $T$, find a $T$-string $s'$ at minimum distance from $s$. With substitution errors only, the distance is the [Hamming distance](/hamming-distance/); with insertions and deletions too, it is the [edit distance](/edit-distance/).

**Error Correction Problem** (same paper). Given $R$, an integer $\Delta$ and $k$, make at most $\Delta$ corrections in each read so that the number of distinct k-mers of the corrected reads is as small as possible. Errors add k-mers, so fewer distinct k-mers means fewer errors left.

**Maximum likelihood version** (Quake). Given $R$ with a quality value for each base, find for each read the set of substitutions with the highest probability, under the error model of the machine, such that the corrected read is a $T$-string. If no such set is found within limits, trim the read or discard it.

The true goal, the reads with no errors, is not observable. The versions above are proxies, and they fail where the proxy is wrong: in low-coverage regions, in repeats, and at sites where the sample itself varies.

## Variants

- **Error type.** Short reads have mostly substitutions; Quake gives 0.5% to 2.5% for Illumina reads of that time. Long single-molecule reads have more errors, mostly insertions and deletions, and need alignment-based correction.
- **Spectrum based.** Use k-mer counts only, as above.
- **Suffix tree based.** Count the substrings of all lengths with a [generalized suffix tree](/generalized-suffix-tree/) of the reads and correct the rare branches, as in SHREC.
- **Alignment based.** Align each read with its overlapping reads and call a [consensus](/consensus-sequence-calling/) column by column. This handles insertions and deletions and is the usual method for long reads.
- **Graph based.** Build the [de Bruijn graph](/de-bruijn-graph/) and remove the structures that errors create: short dead ends ([tips](/tip-removal/)) and short parallel paths ([bubbles](/bubble-popping/)). Velvet does this inside assembly.
- **Hybrid.** Correct long reads with accurate short reads mapped to them.
- **Uneven coverage.** In RNA-Seq, metagenomics and ChIP-Seq the coverage varies over orders of magnitude, so a single count threshold fails. Quake states that its method does not suit these data.

## Examples

**One error in a toy data set.** Let the genome be

$$S = \texttt{TTTCCTCATGCAATTCAAAACCATGTCCGTAATGTAGGCG}$$

($G = 40$, with 36 distinct 5-mers and no repeated 5-mer). Take one read of length 10 at each of the 31 positions, and $k = 5$. The read at position 12 should be ATTCAAAACC, but the machine reads $s = \texttt{ATTCCAAACC}$: the base at position 4 of the read is C instead of A.

| k-mer of $s$ | ATTCC | TTCCA | TCCAA | CCAAA | CAAAC | AAACC |
|---|---|---|---|---|---|---|
| start | 0 | 1 | 2 | 3 | 4 | 5 |
| count | 1 | 1 | 1 | 1 | 1 | 6 |

With $M = 1$, the first five k-mers are weak and the last is solid.

1. **Locate.** The weak k-mers start at 0 to 4, so they cover positions $[0, 4], [1, 5], \ldots, [4, 8]$ of the read. An error at one position that explains all of them must lie in every window. The intersection is position 4.
2. **Correct.** Try the three other bases at position 4. Only A makes all six k-mers solid. A search over all corrections with at most two substitutions confirms that this one substitution is the unique smallest correction.

**A pitfall in the same data.** The spectrum of the toy data is $h(1) = 7$, $h(2) = 2$, $h(3) = 2$, $h(4) = 2$, $h(5) = 7$, $h(6) = 21$. Of the seven k-mers with count 1, five are the error k-mers above, but two are true: the first and last 5-mers of the genome are inside only one read each, because of the genome ends. A corrector with $M = 1$ would try to "fix" them. Low coverage makes true k-mers look like errors.

**The spectral alignment as a shortest path.** For substitutions only, the Spectral Alignment Problem has a dynamic program. Let $d(i, t)$ be the least number of substitutions that turn $s[0 \ldots i]$ into a string that ends with the solid k-mer $t$ and has only solid k-mers. Then $d(k - 1, t)$ is the Hamming distance between $t$ and $s[0 \ldots k-1]$, and

$$d(i, t) = [\,t[k-1] \ne s[i]\,] + \min_{b \in \Sigma,\ b\,t[0 \ldots k-2] \in T} d(i - 1, b\,t[0 \ldots k-2]).$$

The answer is $\min_t d(n - 1, t)$ for a read of length $n$. Each state has at most four predecessors, so the time is $O(n\,|T|)$. In practice only k-mers near the read are tried, since $|T|$ is about the genome size.

## Known algorithms

- **EULER's spectral alignment** (Pevzner, Tang and Waterman). Choose $M$, mark solid and weak tuples, and correct reads so that they become $T$-strings with few changes. On Sanger reads of *Neisseria meningitidis* (53,263 reads at about $9.7\times$ coverage, with 255,631 errors, about 1.2% of the bases), a greedy method removed 86.5% of the errors and the EULER method 97.7%. The corrected reads had about 0.11 errors each.
- **Quake** (Kelley, Schatz and Salzberg). Count *q-mers*: each k-mer occurrence adds the probability that all its bases are right, from the quality values, not 1. Fit the histogram of these counts to choose the cutoff between trusted and untrusted k-mers. For a read with untrusted k-mers, find the region that all of them cover and that no trusted k-mer covers, and try corrections in that region in order of decreasing likelihood, using the quality values and the rates at which the machine confuses each pair of bases. Accept the most likely correction that makes all k-mers trusted; trim or discard the read if none is found.
- **Other early methods.** Quake surveys SHREC (suffix tree), the corrector of SOAPdenovo, and the error removal of Velvet (tips and bubbles in the assembly graph).

## Bounds

- **Localization.** A single substitution at position $p$ of a read changes the k-mers that start at $\max(0, p - k + 1)$ to $\min(p, n - k)$, up to $k$ of them. If they all become weak and no other k-mer does, the intersection of their windows is exactly $\{p\}$ when $p$ is at least $k-1$ bases from both ends; near the ends the intersection is wider.
- **Search size.** With $d$ errors in a region of $w$ positions, there are $\binom{w}{d} 3^d$ candidate corrections. Quake searches them in order of likelihood and gives up on reads that need too many, which keeps the work bounded.
- **Coverage.** At coverage $c$ with read length $L$, a genome k-mer has mean count about $c (L - k + 1)(1 - e)^k / L$ (see [k-mer spectrum](/kmer-spectrum/)). When this is low, the count distributions of true and error k-mers overlap, and no threshold separates them.
- **Repeats and variation.** A true k-mer that is rare, such as one from a minor allele, a low-coverage region or a rare transcript, looks like an error. A correction toward a similar k-mer from another repeat copy turns a true difference into an error.

## Reductions

- **Spectral alignment to paths in the de Bruijn graph.** A $T$-string of length $n$ is a walk of $n - k + 1$ edges in the [de Bruijn graph](/de-bruijn-graph/) of $T$, one edge for each k-mer. The Spectral Alignment Problem with substitutions is a minimum-cost walk of that length. The first edge costs its Hamming distance to the first $k$ bases of the read, and each later edge costs 1 if its last base differs from the read at that position. This is the dynamic program above.
- **Consensus.** Alignment-based correction reduces to computing a [consensus](/consensus-sequence-calling/) of a [multiple alignment](/multiple-sequence-alignment/) of overlapping reads.
- **From counting.** All spectrum methods need [k-mer counting](/kmer-counting/) first.

## Applications

- Before [de Bruijn assembly](/de-bruijn-assembly/): each error adds up to $k$ false k-mers to the graph, so correcting errors first makes the graph smaller and simpler.
- Before overlap-based assembly of long reads, to raise the identity of overlaps.
- Before k-mer based analyses such as genome size estimation, where error k-mers would inflate counts.
- Before [read mapping](/read-mapping/) in some pipelines, to reduce false mismatches.

## References
