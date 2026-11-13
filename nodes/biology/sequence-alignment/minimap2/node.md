---
tag: 5DG5E4
kind: algorithm
slug: minimap2
name: Minimap2
area: biology/sequence-alignment
level: research
summary: A heuristic mapper for long and short DNA reads. It looks up minimizer seeds in a hash table, chains them with a gap-aware dynamic program, and aligns the gaps with affine-gap DP.
solves: [read-mapping]
model: word-ram
complexity:
  vars: {n: the length of the reference, m: the length of the query, a: the number of anchors, h: the number of predecessors tried per anchor, w: the minimizer window, b: the band width of the base-level alignment}
  time: {average: O(m + a log a + h a + m b)}
  space: {extra: O(n/w + a)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2018
  people: [Heng Li]
  note: Minimap2 grew out of minimap (2016), which found overlaps between long reads with minimizers but did not align them.
prereqs: [minimizer, seed-chaining]
see_also: [colinear-chaining, kmer-index, read-mapping, affine-gap-alignment, banded-alignment, x-drop-extension, overlap-detection, bwa]
sources:
  - paper: doi:10.1093/bioinformatics/bty191
    title: Heng Li, Minimap2, pairwise alignment for nucleotide sequences, Bioinformatics 34(18), 2018
    locator: pages 3094 to 3100, Section 2.1 (indexing, the chaining recurrence, backtracking, primary chains and mapping quality) and Section 2.2 (alignment with 2-piece affine gaps and the Z-drop rule)
  - paper: arxiv:1708.01492
    title: Heng Li, Minimap2, versatile pairwise alignment for nucleotide sequences, preprint, 2017
    locator: Sections 2.1.1 to 2.1.3 (the chaining score, the heuristic with h = 50 predecessors and its average O(hN) time)
  - paper: doi:10.1093/bioinformatics/btw152
    title: Heng Li, Minimap and miniasm, fast mapping and de novo assembly for noisy long sequences, Bioinformatics 32(14), 2016
    locator: pages 2103 to 2110, the minimizer sketch with an invertible hash and the clustering of minimizer hits
  - paper: doi:10.1093/bioinformatics/bth408
    title: Michael Roberts, Wayne Hayes, Brian R. Hunt, Stephen M. Mount and James A. Yorke, Reducing storage requirements for biological sequence comparison, Bioinformatics 20(18), 2004
    locator: pages 3363 to 3369, (w,k)-minimizers
---

Minimap2 is a [read mapper](/read-mapping/) and pairwise aligner for DNA, written by Heng Li and published in 2018. It finds where a query, from a short read to a whole assembled chromosome, lies in a reference, and it handles the high error rates of long single-molecule reads. It works in three steps: it looks up the [minimizers](/minimizer/) of the query in a hash table of the minimizers of the reference, it [chains](/seed-chaining/) the resulting hits with a dynamic program that charges for gaps, and it fills the gaps between the anchors of a chain with [affine-gap](/affine-gap-alignment/) dynamic programming. Every step is a heuristic: the sketch can miss a region with no exact match of $w + k - 1$ bases, the chaining tries only $h$ predecessors per anchor, and the alignment stops early by the Z-drop rule. So minimap2 can miss the best alignment; what it gains is speed on genomes and reads of any length.

## In plain words

Minimap2 does not compare every letter of a read with every letter of the genome. First it picks a small set of short words from the genome, one from each stretch of a few words, and stores where each one occurs. It picks the same kind of words from the read, and looks them up. Each match says "this place in the read may be that place in the genome".

Most true matches line up along one diagonal: their order and spacing agree in the read and in the genome. Minimap2 finds the best such line of matches, and it charges a small penalty where the spacing changes, which is where the read has an extra or a missing piece. Only then does it run a full letter-by-letter alignment, and only in the short gaps between the matches it kept.

## The problem

**Input.** A reference $R$ of length $n$ over $\{A, C, G, T\}$, which may be many sequences, and a query $Q$ of length $m$. Parameters: the k-mer length $k$, the window $w$, the maximum gap $G$, the number $h$ of predecessors tried, and the scores of the alignment.

**Output.** A list of mappings of $Q$: for each, a strand, a reference interval, a query interval, a mapping quality, and, if asked, a base-level alignment with a score. One mapping is *primary* for each part of the query, and others are *secondary*.

The model behind the output is a scored local alignment of $Q$ against $R$ with affine gaps. Minimap2 does not guarantee the best such alignment; it reports the alignments that its seeds and chains lead to.

## The algorithm

**Index.** Minimap2 computes the minimizer sketch of $R$: for each window of $w$ consecutive k-mers, the k-mer with the smallest hash. The hash is an invertible integer function of the 2-bit code of the *canonical* k-mer, the smaller of the k-mer and its reverse complement, so that both strands select the same positions. A hash table maps each minimizer hash to the list of its positions and strands. In expectation the index keeps about $2n/(w+1)$ positions; see [minimizer](/minimizer/).

**Anchors.** For each minimizer of $Q$ and each position in the table with the same hash, minimap2 makes an *anchor* $(x, y, w)$: the reference interval $[x - w + 1, x]$ matches the query interval $[y - w + 1, y]$, where here $w$ is the seed length. Anchors on the two relative strands are kept apart; for the opposite strand, $y$ is measured on the reverse complement of $Q$. The anchors are sorted by $x$. Minimizers that occur too often in the reference are skipped.

**Chaining.** The best score of a chain that ends at anchor $i$ is

$$f(i) = \max\Bigl\{\ \max_{i > j \ge 1}\bigl\{f(j) + \alpha(j, i) - \beta(j, i)\bigr\},\ w_i\ \Bigr\},$$

with $\alpha(j, i) = \min\{y_i - y_j,\ x_i - x_j,\ w_i\}$, the new bases matched by anchor $i$, and $\beta(j, i)$ the gap cost: infinite if $y_j \ge y_i$ or if either gap exceeds $G$, and otherwise $\gamma_c(\ell) = 0.01 \cdot \bar{w} \cdot |\ell| + 0.5 \log_2 |\ell|$ for $\ell = (y_i - y_j) - (x_i - x_j) \ne 0$, with $\gamma_c(0) = 0$ and $\bar{w}$ the average seed length. This is the score of the [seed chaining](/seed-chaining/) problem. Computed in full it takes $O(a^2)$ time for $a$ anchors. Minimap2 instead tries the predecessors $j = i - 1, i - 2, \ldots$ and stops when it has not found a better score after $h$ tries; the paper uses $h = 50$.

```pseudo id=main
MINIMAP2-MAP(Q)                           ▷ index of R built in advance
L1  for each minimizer (hash v, end position q, strand s) of Q do
L2      for each (position r, strand s') in TABLE[v] do add the anchor (r, q, k) to the list of strand s ⊕ s'
L3  sort the anchors of each strand by x
L4  for i ← 1 to a do                    ▷ a anchors on one strand
L5      f(i) ← w_i; P(i) ← NIL; misses ← 0
L6      for j ← i − 1 down to 1, while x_i − x_j ≤ G and misses < h do
L7          if f(j) + α(j, i) − β(j, i) > f(i) then f(i) ← f(j) + α(j, i) − β(j, i); P(i) ← j; misses ← 0
L8          else misses ← misses + 1
L9      end
L10 take the anchors in decreasing order of f; from each unused one, follow P back to a used anchor or to NIL
L11 keep the chains of high score; a chain is secondary if half of the shorter chain lies on the query interval of a better chain
L12 for each primary chain, align the gaps between consecutive anchors and the two ends with 2-piece affine gaps, stop by Z-drop
L13 return the alignments, with mapping qualities
```

Lines L1 to L3 build the anchors, lines L4 to L9 are the chaining dynamic program with the limit $h$, line L10 is the backtracking, and lines L11 to L13 select and align. The mapping quality of a primary chain is

$$\mathrm{mapQ} = 40 \cdot (1 - f_2 / f_1) \cdot \min\{1, c/10\} \cdot \log f_1,$$

where $f_1$ is the chaining score of the chain, $f_2$ the score of the best secondary chain that overlaps it, and $c$ the number of anchors on the chain.

**Alignment.** The gaps between anchors are aligned with a 2-piece affine gap cost $\gamma_a(\ell) = \min\{q + |\ell| e,\ \tilde{q} + |\ell| \tilde{e}\}$, where the second piece has a larger open cost and a smaller extension cost, so that one long gap is cheaper than several short ones. The dynamic program uses the difference formulation of Suzuki and Kasahara with SIMD instructions. An extension stops when the score drops more than $Z$ below the best score seen, plus a term for the length difference; this is the *Z-drop* rule, a variant of [X-drop extension](/x-drop-extension/), and it also splits an alignment at a large inversion or a misjoin.

## Example

Take a random reference $R$ of 60 bases and a query $Q$ of 38 bases that copies $R[10 \ldots 29]$ and then $R[32 \ldots 49]$, so that $Q$ misses the two bases $R[30 \ldots 31]$. With $k = 5$ and $w = 4$, the sketch of $R$ has 22 minimizers and that of $Q$ has 13. They give these anchors on the forward strand, sorted by $x$ (all with seed length 5), and the chaining scores with the integer gap cost of the implementation:

| $(x, y)$ | (14, 4) | (17, 7) | (19, 9) | (19, 24) | (23, 13) | (24, 14) | (28, 18) | (38, 26) | (41, 29) | (44, 32) | (47, 35) | (49, 37) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| $y - x$ | $-10$ | $-10$ | $-10$ | $5$ | $-10$ | $-10$ | $-10$ | $-12$ | $-12$ | $-12$ | $-12$ | $-12$ |
| $f$ | 5 | 8 | 10 | 9 | 14 | 15 | 19 | 24 | 27 | 30 | 33 | 35 |

The anchor $(19, 24)$ is a chance hit 15 diagonals away; it starts no good chain, and no later anchor uses it. All the others form one chain with score 35. The diagonal moves from $-10$ to $-12$ between $(28, 18)$ and $(38, 26)$: the reference gap is 10 and the query gap is 8, which is the deletion of two bases. The mapping is on the forward strand, starting at reference position $14 - 4 = 10$. In the full tool the base-level alignment of the gap between these two anchors would place the deletion exactly.

## Correctness

Minimap2 is a heuristic, so the claims are about its parts, not about finding the best alignment.

- **The sketch.** For each window of $w$ consecutive k-mers, the sketch holds the k-mer of smallest hash (leftmost on ties). The sliding-window minimum keeps a deque of positions with increasing hashes, so its head is the minimum of the current window. Two sequences that share $w + k - 1$ bases share a minimizer, by the shared-window property of [minimizers](/minimizer/), and so do a sequence and the reverse complement of the other, because the hash is taken on canonical k-mers.
- **The exact chaining.** With $h \ge a$ and no limit from $G$, lines L4 to L9 evaluate every $j < i$, so $f(i)$ is the maximum of the recurrence. Since the anchors are sorted by $x$, each $f(j)$ is final before it is used. By induction, $f(i)$ is the largest score of a chain that ends at $i$.
- **The heuristic chaining.** With a smaller $h$, each $f(i)$ is a maximum over a subset of the predecessors of values that are, by induction, no larger than the exact ones. So the heuristic score is never above the exact score, and it is equal when the best predecessor of each anchor on the best chain is among the tries.

The proofs file gives these arguments in full.

## Complexity

| step | cost |
|---|---|
| index of $R$ | $O(n)$ expected time with a hash table; about $2n/(w+1)$ positions |
| sketch of $Q$ | $O(m)$ time with a sliding-window minimum |
| anchors | $O(a)$ time to make, $O(a \log a)$ to sort |
| chaining | $O(h a)$ on average, as the paper states; $O(a^2)$ in the worst case of the exact version |
| alignment | proportional to the area of the bands in the gaps, about $O(m \cdot b)$ for a band of width $b$ |

The number of anchors $a$ depends on the repeats of the genome; dropping the most frequent minimizers keeps it under control. The time per read does not depend on $n$, apart from the hash table lookups and the number of hits.

## Properties

- **Heuristic.** It can miss a true alignment (no shared minimizer, a chain cut by the limit $h$, an alignment stopped by Z-drop) and it does not prove the best score.
- **Deterministic.** The same input and parameters give the same output.
- **Strand-symmetric.** Canonical k-mers make the sketches of a sequence and of its reverse complement select the same positions.
- **Local.** It reports local alignments, possibly several per query, and splits a query that spans a rearrangement into several alignments.

## Variants and improvements

- **Presets.** The same program maps short reads, noisy long reads, accurate long reads and assemblies, with different $k$, $w$, scores and chaining parameters for each.
- **Spliced alignment.** For RNA reads, the alignment step allows long gaps that follow splice signals, with a cost model that favors the canonical GT and AG ends of introns.
- **Paired-end reads.** Short read pairs are chained and paired with a distance constraint.
- **Overlaps only.** Without the base-level step, it finds the [overlaps](/overlap-detection/) between long reads, as minimap did, for assembly.
- **Other chaining.** The exact [colinear chaining](/colinear-chaining/) with range-maximum queries gives a worst-case $O(a \log a)$ bound for gap costs that fit it; the $h$ limit is the choice of the original program.

## When to use it

Use minimap2 to map long reads or assembled contigs to a reference, to compare two assemblies, or to find overlaps between long reads. It also maps short reads, though short-read aligners such as [BWA](/bwa/)-MEM and Bowtie 2 were designed for them. Do not use it when you need a guarantee that every alignment within a given distance is found; use an exact method, such as [approximate string matching](/approximate-string-matching/) with an index and verification, for that.

## Pitfalls

- **Repeats.** Minimizers that occur too often are dropped, so a read inside a long, highly repeated region may get no anchors or a mapping quality of 0. Check the mapping quality before trusting a placement.
- **Short or divergent matches.** A region shares a minimizer only when it has an exact match of $w + k - 1$ bases. Very divergent sequences, such as distant species, can be missed.
- **Parameters.** The defaults of each preset are tuned for one kind of data. Using the long-read preset on short reads, or the reverse, lowers accuracy.
- **Secondary and supplementary alignments.** A query can have one primary alignment and several other records. Counting all records as reads counts some reads twice.

## Implementations

## History

Roberts et al. (2004) introduced minimizers to reduce the storage of sequence comparison. Li's minimap (2016) used minimizer sketches and clustering of hits to find overlaps between noisy long reads quickly, with the miniasm assembler on top. Minimap2 (preprint 2017, journal 2018) added the chaining recurrence with gap costs, the base-level alignment with 2-piece affine gaps and SIMD, spliced alignment, and short-read support, and it became a standard mapper for long reads.

## References
