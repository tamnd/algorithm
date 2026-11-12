---
tag: M5J6FC
kind: algorithm
slug: bwa
name: BWA
aliases:
- BWA
- BWA-MEM
- Burrows-Wheeler Aligner
- BWA-backtrack
area: biology/sequence-alignment
level: advanced
summary: A family of read mappers on the FM-index. BWA-backtrack searches for reads within a few edits and prunes with a lower bound; BWA-MEM seeds with super-maximal exact matches and extends them.
solves: [read-mapping]
model: word-ram
complexity:
  vars: {n: the length of the reference, m: the length of the read, z: the number of differences allowed, o: the number of hits}
  time: {worst: O(m (16m)^z + o)}
  space: {extra: O(n)}
properties: {deterministic: false, exact: false, online: false, recursive: true}
history:
  year: 2009
  people: [Heng Li, Richard Durbin]
  note: BWA-backtrack (2009) mapped short reads with gaps on an FM-index; BWA-SW (2010) and BWA-MEM (2013) added long reads and local alignment.
prereqs: [fm-index, read-mapping, maximal-exact-match]
see_also: [bowtie, minimap2, burrows-wheeler-transform, k-differences-problem, seed-chaining, smith-waterman, matching-statistics, sellers-algorithm]
sources:
  - paper: doi:10.1093/bioinformatics/btp324
    title: Heng Li and Richard Durbin, Fast and accurate short read alignment with Burrows-Wheeler transform, Bioinformatics 25(14), 2009
    locator: pages 1754 to 1760, Section 2.4 (exact matching by backward search), Section 2.5 (inexact matching by bounded traversal and backtracking, the procedures InexRecur and CalculateD) and Section 2.7 (the heuristics, maximum differences and mapping quality)
  - paper: doi:10.1093/bioinformatics/btp698
    title: Heng Li and Richard Durbin, Fast and accurate long-read alignment with Burrows-Wheeler transform, Bioinformatics 26(5), 2010
    locator: pages 589 to 595, BWA-SW (dynamic programming between the prefix trie of the reference and the query)
  - paper: doi:10.1093/bioinformatics/bts280
    title: Heng Li, Exploring single-sample SNP and INDEL calling with whole-genome de novo assembly, Bioinformatics 28(14), 2012
    locator: pages 1838 to 1844, the FMD-index and the algorithm for super-maximal exact matches
  - paper: arxiv:1303.3997
    title: Heng Li, Aligning sequence reads, clone sequences and assembly contigs with BWA-MEM, 2013
    locator: Section 2 (SMEM seeds, reseeding, chaining, banded extension and the choice of the primary alignment)
---

BWA, the Burrows-Wheeler Aligner by Heng Li and Richard Durbin, is a family of [read mappers](/read-mapping/) that search an [FM-index](/fm-index/) of the reference genome. The first algorithm, *BWA-backtrack* (2009), finds the places where a short read matches within a few differences (mismatches, insertions and deletions) by a backtracking search over the index. It prunes the search with an array $D$, a lower bound on the differences that each prefix of the read needs, computed with a second FM-index of the reversed genome. The later *BWA-MEM* (2013) seeds with [super-maximal exact matches](/maximal-exact-match/) (SMEMs), chains them and extends them with dynamic programming, which suits reads of 70 bases and longer. All BWA programs are heuristics in their default settings: they limit the search, keep the best hits, and break ties between equal hits at random.

## In plain words

An FM-index can tell, one letter at a time, which places of the genome end a word: read the word backwards, and the set of places shrinks with each letter. BWA-backtrack uses this to look up a read. When the read has an error, the set becomes empty, so the search goes back and tries a different letter, an extra letter, or a missing letter.

That search can try far too many options. So, before it starts, BWA reads the read from left to right and cuts it into pieces that do not occur anywhere in the genome. Each such piece must contain at least one error. If the search has used up its errors and still has more such pieces to go, it stops at once. For longer reads, BWA-MEM instead finds the longest exact pieces that the read shares with the genome, and builds an alignment around them.

## The problem

**Input.** A reference $X$ of length $n$ over $\{A, C, G, T\}$, a read $W$ of length $m$, and a bound $z$ on the number of differences. In the paper the read is aligned in full and the gaps have open and extension costs; this page uses unit costs for the core search.

**Output.** The suffix array intervals of the strings $v$ that occur in $X$ and have an alignment to $W$ with at most $z$ differences. Each interval gives the positions of $v$ in $X$. The program reports the best hits, with a mapping quality.

This is the [k-differences problem](/k-differences-problem/) for a read against an indexed text. BWA-backtrack is exhaustive within $z$ differences when its limits are off. In practice it uses a seed with a smaller bound and stops early.

## The algorithm

**Backward search.** Let $B$ be the [Burrows-Wheeler transform](/burrows-wheeler-transform/) of $X\$$, $C(a)$ the number of letters of $X$ smaller than $a$, and $O(a, i)$ the number of $a$ in $B[0 \ldots i]$. If the rows of the suffixes that start with $u$ form an interval, then the rows that start with $au$ form an interval computed from it in $O(1)$ time. The [FM-index](/fm-index/) page proves this; BWA uses it to extend a match one letter to the left.

**The lower bound $D$.** BWA scans $W$ from left to right and cuts it greedily into pieces that do not occur in $X$. $D(i)$ is the number of such pieces that end at or before position $i$. Any alignment of $W[0 \ldots i]$ to a substring of $X$ needs at least $D(i)$ differences, since each piece needs one. The test "is $W[j \ldots i]$ a substring of $X$?" grows the piece to the right, which is backward search on the FM-index of $X$ reversed.

**Bounded backtracking.** The search reads $W$ from right to left. A state is $(i, z, [sp, ep))$: the letters $W[i+1 \ldots m-1]$ are aligned, $z$ differences are left, and $[sp, ep)$ is the interval of the string $v$ built so far. From a state it can match or mismatch $W[i]$ with a letter $b$, treat $W[i]$ as an insertion (move on in $W$ but not in $X$), or insert a letter $b$ of $X$ that $W$ lacks (a deletion from $W$). A state with $z < D(i)$ is dropped.

```pseudo id=main
CALCULATE-D(W)                            ▷ uses the FM-index of reverse(X)
L1  z ← 0; j ← 0
L2  for i ← 0 to m − 1 do
L3      if W[j .. i] is not a substring of X then
L4          z ← z + 1
L5          j ← i + 1
L6      D(i) ← z

INEXACT-SEARCH(W, z)                      ▷ D(−1) = 0
L7  S ← stack with (m − 1, z, [0, n + 1))
L8  pop (i, z, [sp, ep)); if z < D(i) then drop it
L9  if i < 0 then report [sp, ep) and continue
L10 if z > 0 then push (i − 1, z − 1, [sp, ep))                  ▷ W[i] is an insertion
L11 for each b in {A, C, G, T} with [sp', ep') = backward step of b from [sp, ep) not empty do
L12     if z > 0 then push (i, z − 1, [sp', ep'))                ▷ b is deleted from W
L13     if b = W[i] then push (i − 1, z, [sp', ep'))             ▷ match
L14     else if z > 0 then push (i − 1, z − 1, [sp', ep'))      ▷ mismatch
```

The procedure repeats lines L8 to L14 until the stack is empty. The paper writes the search as a recursion, InexRecur, and implements it as a breadth-first search with a heap that takes the states with the fewest differences first, so that the best hits come out first and the search can stop early.

**BWA-MEM.** For longer reads, BWA-MEM uses the FMD-index, an FM-index of the reference and its reverse complement together, which allows a match to grow in both directions. For each query position it finds the SMEMs that cover it, the longest exact matches that no other match contains on the query. It re-seeds long SMEMs to find shorter seeds that a repeat may hide, groups the seeds into chains by position, drops weak chains, and extends each chain with banded affine-gap dynamic programming that stops when the score falls too far. The best extension becomes the primary alignment, and the score of the second best gives the mapping quality.

## Example

Let $X = \texttt{ACGTTACGGA}$ ($n = 10$) and $W = \texttt{ACGTAACGGT}$ ($m = 10$).

**The array $D$.** CALCULATE-D reads $W$ from the left. ACGT occurs in $X$, but ACGTA does not (only ACGTT does), so the first piece ends at $i = 4$ and $D(4) = 1$. The next piece starts at $i = 5$: ACGG occurs, ACGGT does not, so $D(9) = 2$:

| $i$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| $W[i]$ | A | C | G | T | A | A | C | G | G | T |
| $D(i)$ | 0 | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 2 |

**Search with $z = 1$.** The first state is $(9, 1, \ldots)$, and $1 < D(9) = 2$, so the search stops at once: there is no hit, and the bound proves it after 1 state. Without $D$ the search visits 34 states to reach the same answer.

**Search with $z = 2$.** Now the search finds two occurrences, both starting at position 0 of $X$. One is $X[0 \ldots 9]$ = ACGTTACGGA, with the mismatches A/T at read position 4 and T/A at position 9. The other is $X[0 \ldots 8]$ = ACGTTACGG, with the mismatch at position 4 and the last T of the read as an insertion. The search visits 104 states, against 132 without $D$.

**SMEMs.** For the query CATTACAGGATTAC against GATTACAGATTACC, the matching statistics are $2, 7, 6, 5, 4, 3, 2, 1, 6, 5, 4, 3, 2, 1$, and the SMEMs are the query intervals $[0, 2)$, $[1, 8)$ and $[8, 14)$, as on the [maximal exact match](/maximal-exact-match/) page. BWA-MEM drops the first one as too short and uses the other two as seeds.

## Correctness

**The bound.** Let the greedy scan cut $W[0 \ldots i]$ into the pieces $W[j_1 \ldots i_1], W[j_2 \ldots i_2], \ldots$, each not a substring of $X$, with $D(i)$ of them. In any alignment of $W[0 \ldots i]$ to a substring $v$ of $X$, a piece with no difference inside its span would be copied letter by letter into $v$, and so would occur in $X$. So each piece has a difference inside its span. The spans are disjoint, so the alignment has at least $D(i)$ differences.

**The search.** Without pruning, the search enumerates every alignment of $W$ to a string $v$ with at most $z$ differences, from right to left, and the backward step keeps the interval of $v$ correct. Pruning drops only states that need more differences than they have left, by the bound. So the reported intervals are those of the strings $v$ within $z$ differences of $W$. The proofs file gives both arguments in full, and the implementation checks the end positions against [Sellers' algorithm](/sellers-algorithm/).

**The heuristics.** With seeds, a limit on the differences in the seed, a limit on the work, and early stopping after the best hits, BWA-backtrack can miss hits. BWA-MEM can miss an alignment whose seeds are all shorter than its minimum SMEM length.

## Complexity

| step | time | space |
|---|---|---|
| build the two FM-indexes | $O(n)$ with linear suffix sorting; BWA uses a method for large genomes | about $2n$ bits for each BWT, plus rank and suffix array samples |
| CALCULATE-D | $O(m)$ | $O(m)$ |
| exact match | $O(m)$ | $O(1)$ |
| search with $z$ differences | worst case $O(m (16m)^z)$ states, plus $O(o)$ to report | the stack or heap |

Each state that leads to a report is the end of a path of at most $m + z \le 2m$ steps with at most $z$ difference steps. The paths differ in where the differences are, at most $\binom{m+z}{z} \le (2m)^z$ choices, and in their kind, at most 8 choices for each (3 substitutions, 4 deletions, 1 insertion). This gives the bound above; it is exponential in $z$, which is why $z$ is kept small. In practice the bound $D$ removes most branches: on reads that do not occur, it often stops the search at the first state.

## Properties

- **Heuristic in practice, exhaustive in principle.** With the limits off, BWA-backtrack finds every hit within $z$ differences; the default settings trade this for speed.
- **Gapped.** Unlike [Bowtie](/bowtie/) 1, BWA-backtrack allows insertions and deletions in the search.
- **Random ties.** Among equally good hits, such as copies of a repeat, BWA reports one at random and gives it a mapping quality of 0.

## Variants and improvements

- **Seeding in BWA-backtrack.** The first bases of the read, 32 by default, form a seed with at most 2 differences; the rest of the read gets a larger bound. The maximum number of differences depends on the read length.
- **BWA-SW (2010).** For long reads with gaps, it runs [Smith-Waterman](/smith-waterman/)-style dynamic programming between a prefix trie of the reference, represented by the FM-index, and a directed acyclic word graph of the query, with heuristics that prune the trie.
- **BWA-MEM (2013).** SMEM seeds, re-seeding, chaining and banded extension. It handles reads from 70 bases to a few megabases, local alignments and chimeric reads, and is the variant in common use.
- **[Bowtie](/bowtie/).** Published the same year, also on an FM-index, but with mismatches only and double indexing instead of the bound $D$.
- **[Minimap2](/minimap2/).** For long noisy reads, minimizer seeds and chaining replace the FM-index search.

## When to use it

Use BWA-MEM to map short or medium Illumina reads to a reference genome for variant calling; it is accurate and reports a mapping quality. Use BWA-backtrack only for very short reads, under about 70 bases, where seeds of exact matches are too short to be useful. For long noisy reads, prefer [minimap2](/minimap2/).

## Pitfalls

- **Index of the wrong direction.** $D$ needs the index of the reversed reference, not of its reverse complement. The reverse complement is used for the other strand of the reads, which is a different step.
- **The insertion case.** An insertion in $W$ moves on in $W$ but keeps the interval. Forgetting this case, or applying it with no differences left, gives wrong results.
- **Duplicate reports.** Different alignments can reach the same interval; keep the reports in a set, or keep the best number of differences per interval.
- **Exponential search.** A large $z$ makes the search explode even with $D$. Use a seed, or switch to a seed-and-extend method.

## Implementations

## History

Burrows and Wheeler (1994) introduced their transform, and Ferragina and Manzini (2000) built the FM-index on it. When short-read sequencers arrived, Li and Durbin (2009) turned the index into BWA-backtrack, with the bound $D$ and a breadth-first search for gapped hits; Bowtie and SOAP2 appeared the same year. BWA-SW (2010) extended the approach to long reads. Li's FMD-index (2012) made bidirectional search on both strands possible, and BWA-MEM (2013) built on it with SMEM seeds. BWA-MEM became a standard mapper of short reads in genome sequencing pipelines.

## References
