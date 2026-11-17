---
tag: 1P4EX1
kind: algorithm
slug: selective-alignment
name: Selective alignment
aliases:
- quasi-mapping
- Salmon mapping
area: biology/transcriptomics
level: advanced
summary: 'Map reads to transcripts by chaining exact matches, aligning the read around the best chains only, and keeping scores above a threshold, with decoys to catch reads from elsewhere.'
solves: [transcript-abundance-estimation]
model: word-ram
complexity:
  vars: {L: the read length, k: the k-mer length, h: the number of k-mer hits of the read, c: the number of candidates that pass the chain filter, b: the band}
  time: {worst: O(L·k + h^2 + c·L·(L+b))}
  space: {extra: O(h + L·(L+b))}
properties: {deterministic: true, exact: false, online: true, recursive: false}
history:
  year: 2020
  people: [Avi Srivastava, Laraib Malik, Hirak Sarkar, Mohsen Zakeri, Fatemeh Almodaresi, Charlotte Soneson, Michael I. Love, Carl Kingsford, Rob Patro]
  note: Salmon replaced quasi-mapping by mapping with a real alignment score for each candidate, a post-chaining filter, and decoy sequences from the genome that take reads away from transcripts they do not belong to.
prereqs: [pseudoalignment, read-mapping, seed-chaining, semi-global-alignment]
see_also: [em-isoform-quantification, minimap2, colinear-chaining, kmer-index, minimizer, fm-index, mapping-quality, spliced-read-alignment]
sources:
  - paper: doi:10.1186/s13059-020-02151-8
    title: Avi Srivastava, Laraib Malik, Hirak Sarkar, Mohsen Zakeri, Fatemeh Almodaresi, Charlotte Soneson, Michael I. Love, Carl Kingsford and Rob Patro, Alignment and mapping methodology influence transcript abundance estimation, Genome Biology 21 (2020)
    locator: Article 239, Materials and methods (the sections on selective alignment and on decoy sequences)
  - paper: doi:10.1093/bioinformatics/btw277
    title: Avi Srivastava, Hirak Sarkar, Nitish Gupta and Rob Patro, RapMap, a rapid, sensitive and accurate tool for mapping RNA-seq reads to transcriptomes, Bioinformatics 32(12) (2016)
    locator: pp. i192 to i200 (quasi-mapping)
  - paper: doi:10.1093/bioinformatics/bty292
    title: Fatemeh Almodaresi, Hirak Sarkar, Avi Srivastava and Rob Patro, A space and time-efficient index for the compacted colored de Bruijn graph, Bioinformatics 34(13) (2018)
    locator: pp. i169 to i177 (the pufferfish index)
  - paper: doi:10.1038/nmeth.4197
    title: Rob Patro, Geet Duggal, Michael I. Love, Rafael A. Irizarry and Carl Kingsford, Salmon provides fast and bias-aware quantification of transcript expression, Nature Methods 14(4) (2017)
    locator: pp. 417 to 419 (the quantification that uses the mappings)
  - paper: doi:10.1093/bioinformatics/bty191
    title: Heng Li, Minimap2, pairwise alignment for nucleotide sequences, Bioinformatics 34(18) (2018)
    locator: pp. 3094 to 3100 (the chaining score)
---

Selective alignment maps RNA-seq reads to a transcriptome in two steps. First it finds exact matches of the read in an index and chains them, as in [minimap2](/minimap2/), to find candidate places. Then it computes a real alignment score at each candidate whose chain is close to the best one, and keeps only the places whose score is at least a fixed fraction of the best possible score. Srivastava and colleagues (2020) built it into Salmon, on the pufferfish index, to replace quasi-mapping, which accepted places from exact matches alone. The index can also hold *decoys*, genome regions that look like transcripts. A read whose best score on a decoy is strictly greater than its best score on a transcript is dropped, so that reads from introns or other non-transcript regions do not inflate the [abundance](/transcript-abundance-estimation/) of a transcript.

## In plain words

To place a read, first look for short words of the read that occur exactly in the transcripts. Words that fall in a row on the same transcript point to a place where the read may come from.

Next, check the best of these places with a real letter-by-letter comparison. Count the matches and charge for the differences. If the result is not good enough, throw the place away. This removes the places that only share a few words with the read.

Last, add to the index some pieces of the genome that are not transcripts but look like them. If the read fits one of these pieces better than any transcript, it probably came from there, so do not count it at all.

## The problem

The input is a set of targets, each a transcript or a decoy, and a read $R$ of length $L$. An *alignment* of $R$ (or of its reverse complement) to a target is a semiglobal alignment: all of the read against any substring of the target. With a match score $\mathrm{MATCH} > 0$ and negative scores for a mismatch and a gap, no alignment scores more than $\mathrm{MATCH} \cdot L$. An alignment is *valid* when its score is at least $\tau \cdot \mathrm{MATCH} \cdot L$. The output is the set of valid alignments on transcripts, or nothing if a decoy has a strictly better valid alignment. These alignments go to the [EM](/em-isoform-quantification/), which shares the read among its transcripts.

Aligning the read to every target is too slow. Selective alignment aligns only where the exact matches point, and only where their chain is good, which makes it a heuristic for the problem above.

## The algorithm

The anchors of the read on a target $t$ are the pairs $(x, y)$ with $q[x..x + k - 1] = t[y..y + k - 1]$. An anchor $j$ may follow $i$ in a chain when $x_i < x_j$, $y_i < y_j$ and their diagonals $y - x$ differ by $g_{ij} \le b$. A chain gets $k$ for its first anchor and $\min(x_j - x_i, y_j - y_i, k) - g_{ij}$ for each step. This is a simple form of the [chaining](/seed-chaining/) score of minimap2, with a linear gap cost, and CHAIN finds the best chain by dynamic programming over the anchors sorted by $y$.

```pseudo id=main
SELECTIVE-ALIGN(read R of length L, targets, decoy flags, k-mer index, band b, fractions τ' and τ)
L1  C ← an empty list of candidates
L2  for each strand s, with q = R or q = the reverse complement of R do
L3      for each target t that has a k-mer hit of q do
L4          add (CHAIN(the anchors of q on t), t, s) to C
L5  S ← the best chain score in C
L6  keep in C only the candidates with chain score at least τ'·S
L7  for each candidate, A ← the best semiglobal score of q in the window of t around its chain, widened by b on each side
L8  V ← the candidates with A ≥ τ·MATCH·L
L9  if the best score in V on a decoy is strictly greater than the best score in V on a transcript then return nothing
L10 return the candidates in V on transcripts
```

Lines L2 to L4 collect, for each strand and each target, the best chain of exact k-mer matches. Line L5 takes the best chain score of the read over all targets and strands. Line L6 is the post-chaining filter: a candidate whose chain is far below the best one is not aligned at all. Line L7 aligns the read in a window that covers the chain, extended to the read ends and by the band on both sides. Line L8 keeps the alignments whose score is at least the fraction $\tau$ of the top score. Line L9 is the decoy rule, and line L10 returns what is left, all of it, so a read that fits several transcripts equally well keeps all of them.

Salmon sets both fractions to 0.65 by default, as the paper states; the code uses the same values. The paper does not give the match, mismatch and gap scores in its text. The code uses 2, -4 and -4, with a linear gap cost. It leaves out the pufferfish index and its uni-MEMs (here a plain [k-mer index](/kmer-index/)), the limits of the chaining, affine gaps and the ksw2 library, soft-clipping, the alignment cache, read pairs and the quantification. Positions are 1-based in the text and 0-based in the code.

## Example

Take $A = \texttt{TTCCTAAGAA}$, $B = \texttt{ACGGATTAGG}$ and $C = \texttt{CCGGGTAACC}$. The transcripts are $t_1 = ABC$ and $t_2 = AC$, which skips the exon $B$. The decoy is $D = \texttt{GCAT}\,\texttt{TTCCTACGAACCGTGTAACC}\,\texttt{ACTT}$: a copy of $AC$ with two substitutions, at positions 7 and 14 of the copy, and 4 more bases at each end. Use $k = 5$, $b = 8$ and the fractions 0.65. The reads have $L = 20$, so the top score is 40, the validity threshold is $0.65 \cdot 40 = 26$, and a chain of the top score 20 keeps the candidates with a chain score of at least 13.

The read $r_1$ is the first 20 bases of $t_1$, that is $AB$.

| candidate | chain | passes L6 | alignment score | valid |
|---|---|---|---|---|
| $t_1$, forward | 20 | yes | 40 | yes |
| $t_2$, forward | 10 | no | | |
| $D$, forward | 6 | no | | |
| $t_1$, reverse | 10 | no | | |
| $t_2$, reverse | 5 | no | | |

The read $r_1$ maps to $t_1$ only, with score 40. On $t_2$ only the k-mers of $A$ match, and the chain stops where $B$ starts.

The read $r_2 = AC$ is $t_2$ itself.

| candidate | chain | passes L6 | alignment score | valid |
|---|---|---|---|---|
| $t_1$, forward | 10 | no | | |
| $t_2$, forward | 20 | yes | 40 | yes |
| $D$, forward | 18 | yes | 28 | yes |
| $t_1$, reverse | 5 | no | | |

On $t_1$ the k-mers of $A$ and of $C$ are on two diagonals 10 apart, more than the band, so the chain holds only $A$. The decoy alignment has two mismatches, so it scores $40 - 2 \cdot 6 = 28$. That is less than 40, so the read is kept and maps to $t_2$.

The read $r_3 = \texttt{TTCCTACGAACCGTGTAACC}$ comes from the decoy. On $t_1$ it has a chain of 6, which fails line L6. On $t_2$ it has a chain of 18 and a valid alignment of score 28. On $D$ it has a chain of 20 and a score of 40. The decoy score is strictly greater, so line L9 drops the read. Without the decoy in the index, the read would map to $t_2$ with score 28 and add to its count. The test file checks all three reads, the reverse complement of $r_1$, and the case without the decoy.

## Correctness

[The proof](proofs/correctness.md) shows four facts. The chain DP finds a chain of the best score, because a predecessor always comes earlier in the order by target position. Every returned alignment is real and has a score of at least $\tau \cdot \mathrm{MATCH} \cdot L$, and none is on a decoy. A chain scores at most $L$, and a chain of score $L$ means that the read occurs in the target with no error. So a read with no error always gets the top chain score, survives the filter, scores $\mathrm{MATCH} \cdot L$ in its window, and no decoy can beat it: it is always returned with its source. These are theorems. The filter of line L6 is a heuristic: for a read with errors, the true place can have a lower chain score than a false one and then is not aligned.

## Complexity

The word RAM, with read length $L$, k-mer length $k$, $h$ k-mer hits of the read, $c$ candidates after the chain filter and band $b$.

- **Index.** The plain k-mer index of the code takes $O(n k)$ time and $O(n)$ entries for targets of total length $n$. Pufferfish stores the compacted colored de Bruijn graph of the targets instead, with each k-mer found through its unitig.
- **Lookups.** $2(L - k + 1)$ lookups of $O(k)$ each, so $O(L k)$.
- **Chaining.** The DP compares each pair of anchors on a target, which is $O(h^2)$ in the worst case. Minimap2 limits the number of predecessors that it tries, which makes this close to linear in practice, a heuristic.
- **Alignment.** A window has length at most $L + 2b$ plus the span of the chain, which is $O(L + b)$ when the chain is on one diagonal band, so each candidate costs $O(L (L + b))$. This is the main cost, and it is why line L6 matters.

## Properties

- **Heuristic.** It finds every place where the read occurs with no error (a theorem), but for reads with errors it can miss a place whose chain is weak.
- **Sound.** Every place it reports has a real alignment above the threshold. This is the difference from quasi-mapping and from [pseudoalignment](/pseudoalignment/), which accept a place on exact matches alone.
- **Multi-mapping.** All valid places are reported, not only the best, and the EM shares the read among them.
- **Deterministic and online.** Each read is handled alone, so reads can be streamed and run in parallel.

## Variants and improvements

- **Quasi-mapping.** RapMap (2016) found the transcripts and positions of a read from exact matches in an index, without an alignment score. Selective alignment adds the score.
- **Pseudoalignment.** Kallisto keeps only the set of transcripts, with no position or score; see [pseudoalignment](/pseudoalignment/).
- **The whole genome as a decoy.** Srivastava and colleagues also tested an index that holds the full genome as decoys, so that a read from any part of the genome can be caught, at the cost of a much larger index. Their smaller decoy set holds only the genome regions similar to transcripts, found with MashMap at a minimum identity of 80 percent with the exons masked.
- **An alignment cache.** Salmon keeps a cache per read of the target substrings it has already aligned to, so that the same window is not aligned twice.
- **Score only.** Salmon computes the alignment score and not the CIGAR, which is enough to decide validity.
- **Minimizers.** The exact matches can come from [minimizers](/minimizer/) instead of all k-mers, as in minimap2, or from maximal matches in an [FM-index](/fm-index/).

## When to use it

Use it to quantify known transcripts when the accuracy of the abundances matters more than a small factor in speed, in particular when the sample has many reads from introns, unannotated genes or repeats. Include decoys for such samples. When the transcriptome is complete and speed is all that matters, [pseudoalignment](/pseudoalignment/) is simpler. When new junctions or transcripts are expected, or the alignments themselves are needed, use [spliced alignment](/spliced-read-alignment/) to the genome. Srivastava and colleagues measured that quasi-mapping gave the lowest agreement with alignment-based estimates on experimental data, which is a measurement and not a proof.

## Pitfalls

- **No decoys, no protection.** Without decoys, a read from a region that is not a transcript maps to the most similar transcript if the score passes the threshold, as $r_3$ does in the example.
- **Ties keep the read.** The decoy rule needs a strictly greater decoy score. A read that fits a transcript and a decoy equally well is kept for the transcript.
- **The threshold is relative to the read length.** With $\tau = 0.65$, a short read tolerates fewer differences than a long one in absolute terms.
- **Reads that run off a transcript end.** Without soft-clipping, the overhanging bases are scored as gaps, and a correct read near an end can fall below the threshold. The code has no soft-clipping.
- **The chain filter can drop the truth.** With many errors, the chain of the true place can be weaker than the chain of a repeat. Lowering $\tau'$ aligns more candidates and costs time.
- **Band too small.** Indels shift the diagonal, and a band smaller than the indel splits the chain, as the exon skip splits the chain of $r_2$ on $t_1$.

## Implementations

## History

Patro, Mount and Kingsford (2014) quantified transcripts without alignment in Sailfish, from k-mer counts. Srivastava, Sarkar, Gupta and Patro (2016) introduced quasi-mapping in RapMap, which found the transcripts and positions of a read from exact matches in a generalized suffix array of the transcriptome, with a hash table from each k-mer to its suffix array interval, and computed no base-level alignment. Patro and colleagues (2017) used such mappings in Salmon. Almodaresi, Sarkar, Srivastava and Patro (2018) gave pufferfish, an index of the compacted colored de Bruijn graph. Srivastava and colleagues (2020) showed that mapping without an alignment score can distort abundance estimates, and gave selective alignment with chaining, a score threshold and decoys, on the pufferfish index.

## References
