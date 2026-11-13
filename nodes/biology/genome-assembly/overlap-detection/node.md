---
tag: HAG4HA
kind: problem
slug: overlap-detection
name: Overlap detection
aliases:
- read overlap computation
area: biology/genome-assembly
level: core
summary: "Find all pairs of reads in which a suffix of one read matches a prefix of the other over at least a minimum length, exactly or with a bounded error rate."
prereqs: [overlap, shotgun-sequencing, semi-global-alignment]
see_also: [overlap-graph, string-graph, overlap-layout-consensus, generalized-suffix-tree, minimizer, minimap2, minhash, seed-and-extend]
sources:
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Section 7.10, the all-pairs suffix-prefix problem solved with a generalized suffix tree in O(n + m^2) time
  - paper: "Dan Gusfield, Gad M. Landau and Baruch Schieber, An efficient algorithm for the all pairs suffix-prefix problem, Information Processing Letters 41(4), 1992"
    title: Gusfield, Landau and Schieber 1992
    locator: pp. 181 to 185, all longest suffix-prefix overlaps in O(n + m^2) time
  - paper: doi:10.1126/science.287.5461.2196
    title: Eugene W. Myers et al., A whole-genome assembly of Drosophila, Science 287(5461), 2000
    locator: pp. 2196 to 2204, the overlapper of the Celera assembler
  - paper: doi:10.1093/bioinformatics/btq217
    title: Jared T. Simpson and Richard Durbin, Efficient construction of an assembly string graph using the FM-index, Bioinformatics 26(12), 2010
    locator: pp. i367 to i373, all exact overlaps in O(n + P) time with the FM-index, where n is the total read length and P the number of overlaps
  - paper: doi:10.1038/nbt.3238
    title: Konstantin Berlin, Sergey Koren et al., Assembling large genomes with single-molecule sequencing and locality-sensitive hashing, Nature Biotechnology 33(6), 2015
    locator: pp. 623 to 630, MHAP, overlap candidates of noisy long reads from MinHash sketches of their k-mer sets
  - paper: doi:10.1093/bioinformatics/btw152
    title: Heng Li, Minimap and miniasm, fast mapping and de novo assembly for noisy long sequences, Bioinformatics 32(14), 2016
    locator: pp. 2103 to 2110, all-versus-all overlaps from chained minimizer hits without base-level alignment
  - paper: doi:10.1093/bioinformatics/bty191
    title: Heng Li, Minimap2, pairwise alignment for nucleotide sequences, Bioinformatics 34(18), 2018
    locator: pp. 3094 to 3100, the read-overlap presets for long reads
---

Overlap detection is the problem of finding all pairs of sequencing reads in which the end of one read matches the start of the other over at least a minimum length. In the exact form the match has no errors; in the form used for real reads it is an alignment with an error rate below a bound. Its output is the edge set of the [overlap graph](/overlap-graph/), and it is the first and usually the most expensive step of [overlap-layout-consensus](/overlap-layout-consensus/) assembly.

## In plain words

You have many short pieces of a long text and you want to know which pieces follow each other. Two pieces follow each other when the last letters of one are the first letters of the other, over a stretch that is long enough not to be chance.

Comparing every piece with every other piece takes too long when there are millions of pieces. So the fast methods first look for short words that two pieces have in common. Only pairs that share enough words go on to a full comparison. With reading errors, the shared stretch is not exactly the same in the two pieces, and the comparison must allow a few differences. The fast methods are filters: they can miss a true pair, and they can let a false pair through.

## Definition

**Model.** The genome is a string of length $G$ over $\{A, C, G, T\}$. A sequencer gives $N$ reads of length about $L$, so the coverage is $c = NL/G$. Write $m$ for the number of reads and $n$ for their total length. In the exact model the reads are substrings of the genome. In the error model each base of a read is substituted independently with probability $p$; real long reads also have insertions and deletions, which the edit-distance form below covers. Reads come from both strands, so a read can also overlap the reverse complement of another read.

**Exact overlap detection.** Input: reads $r_0, \ldots, r_{m-1}$ and a minimum length $\ell \ge 1$. Output: every ordered pair $(i, j)$ with $i \ne j$ and $\mathrm{ov}(r_i, r_j) \ge \ell$, with the value $\mathrm{ov}(r_i, r_j)$, the length of the longest proper suffix of $r_i$ that is a proper prefix of $r_j$. This is the all-pairs suffix-prefix problem with a threshold.

**Approximate overlap detection.** Input: the reads, $\ell$, and a maximum error rate $\varepsilon$. Output: every ordered pair $(i, j)$ for which some suffix $s$ of $r_i$ and some prefix $t$ of $r_j$ with $|s|, |t| \ge \ell$ have edit distance at most $\varepsilon \cdot \max(|s|, |t|)$, together with such an alignment. This is a [semi-global alignment](/semi-global-alignment/), with free gaps at the start of $r_i$ and at the end of $r_j$. Pairs in which one read aligns fully inside the other are containments, and are reported separately.

## Variants

- **Longest overlap only, or all overlaps.** The [overlap graph](/overlap-graph/) needs the longest overlap for each pair. The [string graph](/string-graph/) can use every overlap length, because periodic reads can overlap in more than one way.
- **Both strands.** Compare each read with the reverse complements of the other reads too, and record the strand of each overlap.
- **Candidates only.** Tools such as minimap report a pair with the approximate positions of the overlap, from chained seed hits, but no base-level alignment. The later steps then work with these approximate overlaps.
- **Irreducible overlaps only.** For string graph assembly it is enough to find the overlaps that are not transitive, which SGA does directly.
- **Containment detection.** Report the reads that align fully inside a longer read; assemblers remove them before the layout.

## Examples

**Exact.** The genome is `TACGGATCATGCATT` and the reads are `TACGGAT`, `CGGATCA`, `GATCATG`, `TCATGCA` and `ATGCATT`, numbered 0 to 4. With $\ell = 2$ the output has 8 pairs:

| pair | overlap | pair | overlap |
|---|---|---|---|
| $(0, 1)$ | 5 | $(1, 3)$ | 3 |
| $(0, 2)$ | 3 | $(2, 3)$ | 5 |
| $(0, 4)$ | 2, by chance | $(2, 4)$ | 3 |
| $(1, 2)$ | 5 | $(3, 4)$ | 5 |

**One error.** Change read 1 to `CGGTTCA`, with a substitution at its fourth base. The exact overlaps $(0, 1)$ and $(1, 2)$ of length 5 are lost, because each now has one mismatch. With $\ell = 3$ and at most one mismatch in five bases, the approximate form finds them again, with one mismatch each, and the output is the 7 true pairs. The chance pair $(0, 4)$ is gone because its overlap is shorter than 3.

**A $k$-mer filter.** Keep a pair as a candidate when the two reads share a $k$-mer. With $k = 3$, the reads with the error give exactly 7 candidate pairs, for example $(0, 1)$ through `CGG` and $(1, 2)$ through `TCA`, and these are the 7 true pairs. With $k = 4$ only the pairs $(2, 3)$ and $(3, 4)$ share a $k$-mer, and 5 true pairs are lost. A long $k$ makes fewer chance candidates but misses overlaps that are short or have errors.

**Shared $k$-mers in noisy long reads.** Two reads overlap over $o$ bases, with independent substitutions at rate $p$ in each read. A $k$-mer of the overlap is exact in both reads with probability $(1 - p)^{2k}$, so the expected number of shared $k$-mers is $(o - k + 1)(1 - p)^{2k}$. For $o = 2000$:

| $p$ | $k = 12$ | $k = 16$ | $k = 21$ |
|---|---|---|---|
| 0.01 | 1563 | 1439 | 1298 |
| 0.05 | 581 | 385 | 230 |
| 0.15 | 40 | 11 | 2 |

At an error rate of 15 percent, most $k$-mers of the overlap are destroyed, so tools for such reads use short $k$ and decide on the number of hits, not on one hit.

## Known algorithms

| method | output | cost | guarantee |
|---|---|---|---|
| prefix function of $r_j \, \# \, r_i$ for each pair | exact, all overlap lengths | $O(m \cdot n)$ | exact, worst case |
| generalized suffix tree (Gusfield, Landau and Schieber 1992) | exact, longest overlap of every pair | $O(n + m^2)$ | exact, worst case |
| FM-index (Simpson and Durbin 2010) | exact, all overlaps of length at least $\ell$ | $O(n + P)$, $P$ the number of overlaps | exact, stated bound |
| semi-global alignment of each pair | approximate | $O(L^2)$ per pair, $O(m^2 L^2)$ in total | exact for the edit model |
| $k$-mer seeds, then alignment (Celera overlapper) | approximate | depends on the seed hits | heuristic filter |
| MinHash sketches of $k$-mer sets (MHAP) | candidates with positions | close to linear in $n$, observed | heuristic, probabilistic |
| chained [minimizers](/minimizer/) (minimap, [minimap2](/minimap2/)) | candidates, optional alignment | close to linear in $n$, observed | heuristic |

The [generalized suffix tree](/generalized-suffix-tree/) method builds the tree of all reads and does one depth-first traversal. A node whose string is a whole suffix of $r_i$ gives a suffix-prefix match from $r_i$ to every read whose leaf is below the node. One stack per read keeps the deepest such node on the current path from the root, so at the leaf of the whole read $r_j$, the top of the stack of $r_i$ gives $\mathrm{ov}(r_i, r_j)$. The seed methods are versions of [seed and extend](/seed-and-extend/). [MinHash](/minhash/) estimates the Jaccard similarity of the $k$-mer sets of two reads from small sketches, and MHAP stores the sketches in hash tables so that similar reads collide; a pair that passes is then placed by the offsets of the shared $k$-mers.

## Bounds

- **Output size.** The output can have $m(m - 1)$ pairs, for example when all reads are equal to `AAA…A`. Any algorithm reads the input and writes the output, so $\Omega(n + \text{output})$ time is a lower bound, and $O(n + m^2)$ is optimal when every pair is reported.
- **Expected output under the coverage model.** With read starts as a Poisson process of rate $N/G$, equal lengths $L$ and no repeats of length $\ell$ or more, each read overlaps about $c(L - \ell)/L$ later reads, so there are about $N c (L - \ell)/L$ true pairs. This grows linearly in $N$ for fixed coverage.
- **Chance overlaps.** For two independent uniform random reads, an exact suffix-prefix match of length $k$ has probability $4^{-k}$, so a match of length at least $\ell$ has probability at most $\tfrac{4}{3} \cdot 4^{-\ell}$. Over all $m(m - 1)$ ordered pairs with $m = 10^6$, the expected number of chance overlaps is at most about 1242 for $\ell = 15$, 1.2 for $\ell = 20$ and 0.0012 for $\ell = 25$.
- **When a seed filter is exact.** If an overlap of length $o$ has at most $e$ edits, the edits split one of the two strings into at most $e + 1$ error-free pieces of total length at least $o - e$. If $o \ge (e + 1)k + e$, one piece has length at least $k$, and the two reads share an exact $k$-mer. So a filter that keeps every pair with a shared $k$-mer misses no such overlap; this is a worst-case guarantee. At $p = 0.15$ and $o = 2000$, the two reads differ at about $2p(1 - p)o \approx 510$ positions, so $e$ is about 510, and the guarantee needs $k \le 2$, which gives far too many candidates. Practical long-read overlappers therefore give no worst-case guarantee.

## Reductions

- **To the overlap graph and superstrings.** The exact output with $\ell = 1$ gives the weights of the [overlap graph](/overlap-graph/), and a maximum-weight Hamiltonian path in that graph gives a [shortest common superstring](/shortest-common-superstring/).
- **From read mapping.** Overlap detection is all-versus-all [read mapping](/read-mapping/): map every read to the set of all reads and keep the hits that run off the end of one read and the start of the other. Minimap2 does this with its overlap presets.
- **To alignment.** For one pair, the approximate problem is a semi-global alignment, and with an error bound it is a [banded alignment](/banded-alignment/) around the diagonal given by the seed hits.

## Applications

- The edge set of the [overlap graph](/overlap-graph/) and of the [string graph](/string-graph/) in [overlap-layout-consensus](/overlap-layout-consensus/) assembly.
- Self-correction of noisy long reads: the reads that overlap a read give a pileup from which [read error correction](/read-error-correction/) computes a corrected read.
- [Consensus calling](/consensus-sequence-calling/): the overlaps give the multiple alignment of the reads in a contig.
- Detection of contained reads before the layout.

## References
