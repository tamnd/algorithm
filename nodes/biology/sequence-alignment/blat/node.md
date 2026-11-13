---
tag: 6CXMHF
kind: algorithm
slug: blat
name: BLAT
aliases:
- BLAST-like alignment tool
area: biology/sequence-alignment
level: advanced
summary: Kent's 2002 aligner for mRNA and proteins against a genome. It indexes the non-overlapping K-mers of the genome, looks up every K-mer of the query, and clumps the hits.
solves: [local-alignment]
model: word-ram
complexity:
  vars: {n: the length of the database, m: the length of the query, k: the tile size, h: the number of hits}
  time: {worst: O(n + m k + h log h)}
  space: {extra: O(n / k + h)}
properties: {deterministic: true, exact: false, online: false, recursive: false}
history:
  year: 2002
  people: [W. James Kent]
  note: Written to align mRNA, ESTs and mouse proteins to the draft human genome at the University of California, Santa Cruz.
prereqs: [kmer-index, local-alignment]
see_also: [blast, seed-and-extend, minimap2, spaced-seed, read-mapping, kmer, x-drop-extension, bwa]
sources:
  - paper: doi:10.1101/gr.229202
    title: W. James Kent, BLAT, the BLAST-like alignment tool, Genome Research 12(4), 2002
    locator: pages 656 to 664, Methods (Searching With Single Perfect Matches, Single Almost Perfect Matches and Multiple Perfect Matches; Selecting Initial Match Criteria; Clumping Hits and Identifying Homologous Regions; Alignment Stage; Stitching and Filling In), Table 3 and Discussion
  - paper: doi:10.1101/gr.194201
    title: Zemin Ning, Anthony J. Cox and James C. Mullikin, SSAHA, a fast search method for large DNA databases, Genome Research 11(10), 2001
    locator: pages 1725 to 1729, the hash table of non-overlapping k-tuples of the database
  - paper: doi:10.1016/0022-2836(81)90087-5
    title: Temple F. Smith and Michael S. Waterman, Identification of common molecular subsequences, Journal of Molecular Biology 147(1), 1981
    locator: pages 195 to 197, the local alignment recurrence that the alignment stage of BLAT approximates
---

BLAT, the BLAST-like alignment tool by W. James Kent (2002), finds the regions of a large genome that are similar to a query, such as an mRNA or a protein. Like [BLAST](/blast/) it is a [seed-and-extend](/seed-and-extend/) method, but it turns BLAST's design around. BLAST indexes the query and scans the database. BLAT builds a [K-mer index](/kmer-index/) of the database, the genome, and keeps it in memory. It stores only the *non-overlapping* K-mers, the tiles at positions $0, K, 2K, \ldots$, which makes the index $K$ times smaller. It then looks up *every* overlapping K-mer of the query, groups the hits by diagonal, and aligns the regions with enough hits. The paper reports that BLAT is 500 times faster than the tools of that time for mRNA/DNA alignments and about 50 times faster than TBLASTX for translated searches.

## In plain words

Cut the genome into short pieces that do not overlap, all of the same length, and record where each piece is. To search for a query, take every piece of the query that starts at any position, and look it up. Each hit says "this part of the query may come from that part of the genome".

A real match leaves several hits in a line: the same shift between the query and the genome. A chance hit stands alone. BLAT keeps the hits that line up with others, groups the nearby ones, and then aligns the query to each group in full. Because the query pieces start at every position, a long enough match always contains at least one whole genome piece.

## The problem

**Input.** A database $T$ of length $n$, such as a genome, prepared once, and a query $Q$ of length $m$, such as an mRNA. The letters are bases or, in the translated mode, amino acids.

**Output.** The regions of $T$ that are similar to parts of $Q$, each with an alignment. For an mRNA the alignment follows the exons and skips the introns.

This is a [local alignment](/local-alignment/) problem, but BLAT does not compute an optimal local alignment. It targets close similarity: mRNA against its own genome, at 95% identity or better, and proteins between related species.

## The algorithm

**The index.** For each tile, the K-mer $T[t \ldots t+K-1]$ with $t$ a multiple of $K$, store $t$ in the list of that K-mer. Tiles that occur too often, usually repeats, are dropped, and so are tiles with unknown bases.

**Hits.** For each position $i$ of the query, look up $Q[i \ldots i+K-1]$; each tile position $t$ in its list gives a hit $(i, t)$ on the *diagonal* $t - i$. Kent describes three ways to accept hits:

- *single perfect hits*: every hit counts;
- *near-perfect hits*: a query K-mer may differ from the tile in one letter, which needs $K(A-1)+1$ lookups for an alphabet of $A$ letters;
- *multiple perfect hits*: a hit counts only if $N$ perfect hits lie on the same diagonal within $W$ letters of each other.

The defaults in the paper are two perfect hits with $K = 11$ for DNA, and one perfect hit with $K = 5$ for proteins in the stand-alone program.

**Clumps.** BLAT sorts the accepted hits by diagonal and joins hits that are close in diagonal and in position into clumps. Each clump, padded on both sides, is a candidate region.

```pseudo id=main
BLAT-SEARCH(T, Q, K, N, W, g)
L1  for t ← 0, K, 2K, … while t + K ≤ n do
L2      append t to index[T[t .. t+K−1]]
L3  remove the lists of overused tiles
L4  for i ← 0 to m − K do
L5      for each t in index[Q[i .. i+K−1]] do
L6          add the hit (i, t) to H
L7  bucket the hits of H by the diagonal t − i
L8  sort each bucket by i
L9  for each bucket, slide a window of W query letters over it do
L10     if the window holds at least N hits then
L11         keep these hits
L12 sort the kept hits by diagonal
L13 for each kept hit, and each later hit at most g diagonals away do
L14     join the two into one clump if their query positions differ by at most g
L15 return the bounding region of each clump
```

**Alignment stage.** For DNA, BLAT extends the hits of a clump into gapless blocks, fills the gaps between blocks by searching again with smaller K-mers, allows a few mismatches and small gaps, and slides a large gap until its ends match the GT and AG of an intron. For proteins it extends hits into ungapped segments and links them with dynamic programming. Blocks are stitched together across clumps with a gap cost of a constant plus the logarithm of the gap length.

## Example

Let $K = 4$, $N = 2$, $W = 10$ and $g = 10$, and let the database be

$T = \texttt{GCTAAAGACAATTACATAACATACACGTCAGCACGAAACT}$ ($n = 40$).

The tiles are at $0, 4, 8, \ldots, 36$: GCTA, AAGA, CAAT, TACA, TAAC, ATAC, ACGT, CAGC, ACGA, AACT. The query is $T[9 \ldots 30]$ with the C at database position 19 changed to A:

$Q = \texttt{AATTACATAAAATACACGTCAG}$ ($m = 22$).

| query position $i$ | query K-mer | tile position $t$ | diagonal $t - i$ |
|---|---|---|---|
| 3 | TACA | 12 | 9 |
| 11 | ATAC | 20 | 9 |
| 12 | TACA | 12 | 0 |
| 15 | ACGT | 24 | 9 |

The tile TAAC at 16 gives no hit: its copy in the query, TAAA at $i = 7$, holds the changed base. Three hits lie on diagonal 9, the true shift between $Q$ and $T$, and pairs of them lie within 10 letters, so they are kept. The hit at $(12, 12)$ is alone on diagonal 0, a chance match of the repeated word TACA, and is dropped. The three kept hits form one clump, with query positions 3 to 15 and tile positions 12 to 24, and the alignment stage then aligns $Q$ to $T$ around positions 9 to 30. With $g = 5$ the hit at $i = 3$ would form a clump of its own, since its neighbour on the diagonal is 8 letters away.

## Correctness

The search stage is exact for what it defines: the index holds every tile, the lookups return every hit, and the filters keep exactly the hits with $N$ partners in the window. The proofs file shows this, and the tests compare each stage with a naive scan.

What makes the design work is a guarantee about tiles. Let $Q$ and $T$ share an exact match of length $H$. The tiles of $T$ inside the match start at multiples of $K$ in an interval of $H - K + 1$ positions, and any $K$ consecutive integers hold a multiple of $K$, so the match holds at least $\lfloor (H+1)/K \rfloor - 1$ whole tiles. Since the query K-mers start at every position, each of these tiles gives a hit. So BLAT with single perfect hits finds every exact match of length $2K - 1$ or more, and with $N$ hits every exact match of length $(N+1)K - 1$ or more.

BLAT is a heuristic for alignment. A similar region with no long enough exact match, or whose only tiles were dropped as overused, gives no hits, and the alignment stage is not an optimal dynamic program.

## Complexity

| step | time | space |
|---|---|---|
| build the index | $O(n)$ | $O(n/K)$ positions plus the table |
| perfect hits | $O(m + h)$ with $O(K)$ hashing per K-mer, $O(mK)$ in all | $O(h)$ |
| near-perfect hits | $O(mK^2 A + h)$ | $O(h)$ |
| filter and clump | $O(h \log h)$ for the sorts, plus the pairs inside the clump distance | $O(h)$ |

Here $h$ is the number of hits. In a random genome, a query K-mer equals a given tile with probability $4^{-K}$, so the expected number of chance hits is

$$(m - K + 1) \cdot \frac{n}{K} \cdot 4^{-K}.$$

For a 500-base query against a genome of 3 billion bases, this is about 140,000 for $K = 10$, 32,000 for $K = 11$ and 7,300 for $K = 12$. The demand for $N = 2$ hits on one diagonal removes most of them. An index of overlapping K-mers would make both the index and the chance hits $K$ times larger. Kent reports about 0.9 GB of memory for the human genome index of DNA.

## Properties

- **Sensitivity.** If a gapless homologous region of length $H$ has each base the same with probability $M$, independently, it holds at least $\tau = \lfloor (H+1)/K \rfloor - 1$ whole tiles, and it gives a perfect hit with probability at least $1 - (1 - M^K)^{\tau}$. For $H = 100$ and $K = 11$, $\tau = 8$, and the bound is 0.95 at $M = 0.9$ but 0.51 at $M = 0.8$. This is why BLAT on DNA suits close matches, and why the paper notes that the method starts to break down below 90% identity.
- **Index in memory.** The index of the database is built once per run, or kept by a server, and every query uses it.
- **Spliced alignment.** For mRNA, the alignment stage places introns at GT and AG ends.

## Variants and improvements

- **Translated BLAT.** Both the query and the genome are translated in all reading frames, and the index holds amino acid tiles; this finds protein similarity between species.
- **Near-perfect hits.** One mismatch per tile finds more distant matches at the cost of $K(A-1)+1$ lookups per K-mer.
- **[BLAST](/blast/).** Indexes the query and scans the database, with words of all positions and extension by [X-drop](/x-drop-extension/). It is more sensitive for distant proteins and slower on a genome.
- **[Spaced seeds](/spaced-seed/).** PatternHunter and later tools use seeds with "don't care" positions, which are more sensitive than contiguous K-mers of the same weight.
- **[Minimap2](/minimap2/).** Indexes the database by minimizers instead of fixed tiles, which keeps the guarantee above for a window of $K$ K-mers but stores more positions, about $2/(K+1)$ per base against $1/K$ for tiles; the query then needs only its own minimizers looked up, and the hits are chained before alignment.

## When to use it

Use BLAT to place a transcript, EST or contig on its own genome, or a close relative, when the identity is high. It is the search behind the BLAT tool of the UCSC Genome Browser. Do not use it for distant homology; use [BLAST](/blast/) or a profile method. For millions of short reads, use a [read mapper](/read-mapping/) such as [BWA](/bwa/).

## Pitfalls

- **Matches shorter than $2K - 1$.** They can fall between tiles and give no hit at all, even with no mismatch.
- **Overused tiles.** Dropping repeated tiles saves time but hides matches that lie only in repeats.
- **Indexing the wrong side.** The non-overlapping tiles must be in the indexed database, and the overlapping K-mers on the side that is scanned. With non-overlapping K-mers on both sides, a match can hold no aligned pair at all.
- **Assuming optimal alignments.** BLAT's alignment stage stitches blocks with heuristics; for a scored optimal alignment of a candidate region, run [Smith-Waterman](/smith-waterman/) on it.

## Implementations

## History

Kent wrote BLAT to align mRNA and mouse proteins to the draft human genome assembled at the University of California, Santa Cruz in 2000 and 2001. The idea of indexing the database instead of the query goes back to SSAHA (Ning, Cox and Mullikin, 2001), which also stored non-overlapping K-mers of the database. BLAT added near-perfect and multiple-hit seeds, clumping and a spliced alignment stage, and became a standard tool of the UCSC Genome Browser.

## References
