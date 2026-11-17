---
tag: YWMA4M
kind: algorithm
slug: maximal-mappable-prefix-alignment
name: Maximal mappable prefix alignment
aliases:
- STAR alignment algorithm
area: biology/transcriptomics
level: advanced
summary: 'Align an RNA-seq read by finding, with a suffix array, its longest prefix that occurs in the genome, repeating on the rest of the read, and stitching the seeds across introns.'
solves: [spliced-read-alignment]
model: word-ram
complexity:
  vars: {L: the read length, n: the genome length, D: the number of seed diagonals}
  time: {worst: O(L^2·log n + L·D^2)}
  space: {extra: O(L·D)}
properties: {deterministic: true, exact: false, online: true, recursive: false}
history:
  year: 2013
  people: [Alexander Dobin, Carrie A. Davis, Felix Schlesinger, Jorg Drenkow, Chris Zaleski, Sonali Jha, Philippe Batut, Mark Chaisson, Thomas R. Gingeras]
  note: STAR found splice junctions without a junction database by searching maximal mappable prefixes in an uncompressed suffix array of the genome, and stitching the seeds with a dynamic program.
prereqs: [spliced-read-alignment, suffix-array, maximal-exact-match]
see_also: [binary-search, lcp-array, suffix-array-construction, seed-and-extend, smith-waterman, fm-index, sam-alignment-format, selective-alignment]
sources:
  - paper: doi:10.1093/bioinformatics/bts635
    title: Alexander Dobin, Carrie A. Davis, Felix Schlesinger, Jorg Drenkow, Chris Zaleski, Sonali Jha, Philippe Batut, Mark Chaisson and Thomas R. Gingeras, STAR, ultrafast universal RNA-seq aligner, Bioinformatics 29(1) (2013)
    locator: pp. 15 to 21, Sections 2.1 (seed search) and 2.2 (clustering, stitching and scoring), Section 3.3 (speed and memory), Figure 1
  - paper: doi:10.1137/0222058
    title: Udi Manber and Gene Myers, Suffix arrays, a new method for on-line string searches, SIAM Journal on Computing 22(5) (1993)
    locator: pp. 935 to 948 (the suffix array and the search by binary search)
  - paper: doi:10.1093/bioinformatics/btp120
    title: Cole Trapnell, Lior Pachter and Steven L. Salzberg, TopHat, discovering splice junctions with RNA-Seq, Bioinformatics 25(9) (2009)
    locator: pp. 1105 to 1111 (the earlier approach, with unspliced mapping first)
---

Maximal mappable prefix alignment is the seed search of the STAR aligner of Dobin and colleagues (2013) for [spliced read alignment](/spliced-read-alignment/). From the start of a read, it finds the *maximal mappable prefix* (MMP): the longest prefix of the read that occurs exactly somewhere in the genome. It finds it by binary search in a [suffix array](/suffix-array/) of the genome. If the read crosses a splice junction, the MMP stops at the end of the exon or a few bases after it, so the search starts again on the rest of the read and finds the next exon. A mismatch also stops the MMP, and the search goes on after it. Then a dynamic program stitches the seeds into one alignment with introns, mismatches and soft-clipped ends. No list of known junctions is needed. The method is a heuristic: it finds exact unspliced reads with certainty, but a spliced read with a very short overhang into an exon is often soft-clipped instead.

## In plain words

Sort every suffix of the genome, so that any piece of text can be looked up like a word in a dictionary.

To place a read, look up the read. The dictionary tells you how far the read matches before it stops fitting anywhere. If the read came from two exons glued together, the match stops near the place where the first exon ends. Note where the match is, skip one letter, and look up the rest of the read in the same way. The rest fits at the start of the next exon, further along the genome.

At the end, put the pieces together. Choose the cut point between them so that the gap starts and ends with the letters that real introns usually have, and count the matches and the differences.

## The problem

The input is a genome $G$ of length $n$ with its suffix array, and a read $R$ of length $L$ from an RNA molecule. The task is a spliced alignment: blocks of the read aligned to the genome in order, with long gaps in the genome between them for the introns, as on the [spliced read alignment](/spliced-read-alignment/) page. The output is a position and a CIGAR string with M, N and S operations, as in the [SAM format](/sam-alignment-format/), or *unmapped*.

The algorithm reduces the task to exact matching. The *diagonal* of a match is its genome position minus its read position. An alignment with mismatches and introns stays on one diagonal inside each block, and moves to a larger diagonal at each intron. So if the seeds give the right diagonals, the stitching only has to choose where to change diagonal.

## The algorithm

Positions are 1-based in the text and 0-based in the code.

```pseudo id=main
MMP-ALIGN(read R of length L, genome G with suffix array SA, seed length s_min, place limit n_max, fraction τ)
L1  Δ ← an empty set of diagonals; i ← 1
L2  while i ≤ L do
L3      (ℓ, P) ← the length of the longest prefix of R[i..L] that occurs in G, and the set of its positions, by binary search in SA
L4      if ℓ ≥ s_min and |P| ≤ n_max then add p - i to Δ for each p in P
L5      i ← i + ℓ + 1
L6  A ← STITCH(R, G, Δ), the best alignment that puts each read base on a diagonal of Δ
L7  if A exists and score(A) ≥ τ·L then return A
L8  return unmapped
```

Line L3 is the MMP search. The suffixes that share the longest prefix with $R[i..L]$ are next to the place where $R[i..L]$ would be inserted in the sorted order, so one binary search and two comparisons give $\ell$, and two more binary searches give the block of the suffix array whose suffixes start with this prefix, that is, all its places. Line L4 keeps a seed only if it is long enough to be meaningful and maps to few places; STAR also limits the number of places of its anchors. Line L5 skips the base after the MMP, which is a mismatch, or the first base after the end of the match on the next exon. The stitching realigns this base.

STITCH is a dynamic program over the read positions $x$ and the diagonals $d$ of $\Delta$. The value $F(x, d)$ is the best score of an alignment that ends with base $x$ on $d$. It adds $+1$ for a match or $-1$ for a mismatch to the best of three cases: start here (soft-clip all bases before), stay on $d$ from base $x - 1$, or come from a smaller diagonal $d'$ with $d - d'$ between the minimum and maximum intron length, minus the intron penalty. The penalty is 2 if the intron starts with GT and ends with AG (or CT and AC, the same motif on the other strand), and 8 otherwise. The best cell over all $x$ and $d$ gives the end, the bases after it are soft-clipped, and the back pointers give the CIGAR.

The code chooses these scores; STAR has its own scoring options, which the paper does not list. The code leaves out the search from the read end in the reverse direction, the extra start points, the clustering of seeds into windows around anchors, insertions and deletions in the stitching, the reverse strand of the read, read pairs, chimeric reads and the report of several alignments. The code builds the suffix array by sorting the suffixes, which is simple but slow; see [suffix array construction](/suffix-array-construction/).

## Example

The genome has 42 bases: CCCT, an exon CGATTCAAAT at positions 5 to 14, an intron GTGGCCGGGAGTAG at 15 to 28, an exon GACGGCAGCA at 29 to 38, and GAGA. The read is $R = \texttt{ATTCAAATGACGGCAG}$: the last 8 bases of the first exon and the first 8 of the second. Use $s_{\min} = 5$, $n_{\max} = 10$, introns of 10 to 1000 bases and $\tau = 0.66$.

| step | start $i$ | MMP | $\ell$ | places | diagonal |
|---|---|---|---|---|---|
| 1 | 1 | ATTCAAATG | 9 | 7 | 6 |
| 2 | 11 | CGGCAG | 6 | 31 | 20 |

The first MMP runs one base past the exon: the G at read position 9 also matches the G of the intron start GT. Line L5 then skips read position 10, and the second MMP is the rest of the read, at genome position 31 in the second exon. The search ends, and $\Delta = \{6, 20\}$, which differ by the intron length 14.

The stitching has two cut points with 16 matches. A cut after read base 8 makes the intron positions 15 to 28, GTGGCCGGGAGTAG, with the motif GT and AG, so the score is $16 - 2 = 14$. A cut after base 9 makes the intron positions 16 to 29, TGGCCGGGAGTAGG, with the motif TG and GG, so the score is $16 - 8 = 8$. Other cut points have a mismatch and a non-canonical motif. The result is position 7 with the CIGAR 8M14N8M and the score 14, which is at least $0.66 \cdot 16$. With only the first seed, the best alignment would be 9M7S with the score 9: the read could not cross the intron. The test file checks all of this, with the 0-based positions 6 and 30.

## Correctness

[The proof](proofs/correctness.md) shows four theorems. The MMP search returns the true maximal mappable prefix and all its places, because the longest common prefix with a string is reached at its neighbors in the sorted order and the suffixes with a given prefix form one block. The stitching is optimal among all alignments whose bases lie on the diagonals of $\Delta$, by the usual induction over the read positions. A read that occurs once in the genome with no error is returned with the full score, its position and the CIGAR $L$M. And an exact read across one intron gets a score at least $L$ minus the intron penalty, if the first MMP lies on the true first diagonal and both seeds are at least $s_{\min}$ long and map to few enough places. That the result is then the true alignment is not a theorem: the junction can often move by a base with the same matches, and the motif penalty decides.

## Complexity

The word RAM, with read length $L$, genome length $n$ and $D$ diagonals in $\Delta$.

- **Seed search.** Each MMP search is a few binary searches of $O(\log n)$ steps, each step a comparison of up to $L$ letters, so $O(L \log n)$. There are at most $L$ searches, and usually only one per block, because each search moves $i$ past its match. The worst case is $O(L^2 \log n)$.
- **Stitching.** $L \cdot D$ cells, each looking at up to $D$ diagonals, so $O(L D^2)$ time and $O(L D)$ space. $D$ is at most $n_{\max}$ times the number of seeds.
- **Index.** The suffix array has $n$ entries and can be built in $O(n \log n)$ time or faster. STAR keeps it uncompressed, which makes the search fast and the memory large: the paper reports about 27 GB of RAM for the human genome, and less than 16 GB with a sparse suffix array, at a cost in speed. It reports about 550 million paired-end reads of 2 × 76 bases per hour on 12 threads. These are measurements.

## Properties

- **No junction database.** The seeds find new junctions as easily as known ones.
- **Heuristic.** Exact unspliced reads are found with certainty, and exact reads across one junction under the conditions of Theorem 4. Short overhangs and repeats can make it miss the true alignment.
- **Exact matching first.** All the work with mismatches and introns happens on the few diagonals that the seeds give, which is what makes the method fast.
- **Deterministic and online.** Each read is handled alone, so reads run in parallel.

## Variants and improvements

- **Search in both directions.** STAR runs the MMP search in both the forward and the reverse direction of the read, which gives a second set of seeds when the forward search misses a block.
- **Extra start points.** The search can start at points spread over the read, so that one error does not hide a whole block.
- **Windows around anchors.** STAR clusters the seeds into windows around anchors that map to few places; the window size sets the largest intron. Seeds of the two mates of a pair are stitched together, and a read that needs two windows is reported as chimeric.
- **Multimappers.** STAR reports all alignments whose score is within a set range below the best one.
- **Compressed indexes.** HISAT replaces the uncompressed suffix array with an [FM-index](/fm-index/) and small local indexes, which uses much less memory; see [spliced read alignment](/spliced-read-alignment/).
- **Reads to transcripts.** For quantification only, [selective alignment](/selective-alignment/) or pseudoalignment to a transcriptome avoids the genome and the introns.

## When to use it

Use it to align short RNA-seq reads to a genome when splice junctions must be found, including new ones, and when memory is available: an index of tens of gigabytes for a mammalian genome. When memory is short, an aligner with an FM-index is the better choice. For long reads with many errors, exact seeds of maximal length are too rare, and chaining of [minimizers](/minimizer/), as in minimap2, works better. For counts of known transcripts alone, a mapping to the transcriptome is faster.

## Pitfalls

- **Short overhangs.** When a read crosses a junction with only a few bases on one side, the second MMP is shorter than $s_{\min}$ and is dropped, and the short end is soft-clipped. In the tests, every read whose blocks all had at least 12 bases was placed exactly (183 of 183), but only 16 of 57 reads with a shorter block were, a measurement. A search from the other end of the read can find the short block from its other side.
- **Overshoot at the junction.** The MMP often runs a few bases past the end of the exon, because the start of the intron can match the start of the next exon by chance. The stitching must be free to move the cut point back, as in the example.
- **The junction is ambiguous.** When the end of an exon equals the end of the intron, several cut points have the same matches, and only the motif penalty chooses. Two non-canonical cut points with the same score are a tie, and the result depends on the order of the search.
- **Repeats.** An MMP in a repeat has many places. If it has more than $n_{\max}$, it gives no diagonal, and a read made mostly of repeats can be unmapped.
- **Memory.** The uncompressed suffix array of a large genome needs much RAM, as the measurements above show.

## Implementations

## History

Manber and Myers (1993) gave the suffix array and its search by binary search. Trapnell, Pachter and Salzberg (2009) found junctions in TopHat by first mapping reads without splicing and then looking for junctions between islands of coverage. Dobin and colleagues (2013) gave STAR, which searched maximal mappable prefixes in an uncompressed suffix array of the genome, so that the first exon and the next one were found by the same exact search, and stitched the seeds with a dynamic program. They traded memory for speed.

## References
