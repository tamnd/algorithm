---
tag: 6QAKRR
kind: data-structure
slug: string-graph
name: String graph
aliases:
- Myers string graph
area: biology/genome-assembly
level: advanced
summary: "Overlap graph of the non-contained reads without its transitive edges. Every walk spells the same strings as before, but there are about c times fewer edges."
prereqs: [overlap-graph, transitive-reduction]
see_also: [overlap-detection, overlap-layout-consensus, unitig, assembly-graph-simplification, de-bruijn-graph, genome-repeat, fm-index, minimap2]
sources:
  - paper: doi:10.1093/bioinformatics/bti1114
    title: Eugene W. Myers, The fragment assembly string graph, Bioinformatics 21(suppl 2), 2005
    locator: pp. ii79 to ii85; Section 2 (contained reads, transitive edges, chain collapsing, bidirected edges) and Section 3 with Fig. 4 (the transitive reduction algorithm and its time bounds)
  - paper: doi:10.1007/BF01188580
    title: John D. Kececioglu and Eugene W. Myers, Combinatorial algorithms for DNA sequence assembly, Algorithmica 13(1/2), 1995
    locator: pp. 7 to 51, the bidirected overlap graph for reads from both strands
  - paper: doi:10.1093/bioinformatics/btq217
    title: Jared T. Simpson and Richard Durbin, Efficient construction of an assembly string graph using the FM-index, Bioinformatics 26(12), 2010
    locator: pp. i367 to i373, overlaps and irreducible overlaps found directly with the FM-index
  - paper: doi:10.1093/bioinformatics/btw152
    title: Heng Li, Minimap and miniasm, fast mapping and de novo assembly for noisy long sequences, Bioinformatics 32(14), 2016
    locator: pp. 2103 to 2110, miniasm builds and simplifies a string graph from raw long-read overlaps
---

The string graph of a set of sequencing reads is the [overlap graph](/overlap-graph/) of the reads that are not contained in other reads, with every transitive edge removed. An edge from $u$ to $x$ is transitive when a third read $w$ lies between them, so that the path $u \to w \to x$ spells the same string as the edge. Myers (2005) introduced it to make overlap-based assembly scale. The reduction keeps every string that a walk can spell and removes about a factor $c$ of the edges, where $c$ is the coverage.

## In plain words

Lay the pieces of a long text on a table in the order in which they occur. In the overlap graph, an arrow goes from each piece to every later piece that shares letters with it. With deep coverage, each piece has arrows to many later pieces, and most of these arrows give no new information. The arrow to the piece after next is not necessary, because you can go through the next piece and read the same letters.

The string graph removes all such shortcut arrows. It also removes every piece that is fully inside a longer piece, because the longer piece already gives its letters. In a region of the text that occurs only once, what remains is a single chain from each piece to the next. Branches stay only where the text has a repeat that the pieces cannot bridge.

## The abstract type

**Model.** The genome is a string of length $G$, and the input is $N$ reads of length about $L$, with coverage $c = NL/G$. Write $m$ for the number of reads after the removal of duplicate and contained reads, and $n$ for their total length. The reads are exact substrings of one strand of the genome; the variants below describe errors and the two strands. The minimum overlap is $\ell \ge 1$.

A read is contained if it is a substring of a longer read. For two different reads $u$ and $x$, an overlap edge $(u, x, d)$ exists when $1 \le d \le |u| - \ell$ and the suffix of $u$ that starts at offset $d$ is a proper prefix of $x$. If $u$ starts at position 0, then $x$ starts at position $d$, and the overlap has length $|u| - d \ge \ell$. Unlike the overlap graph page, a pair of reads can have several edges, one for each overlap length, because a periodic read can overlap another read in more than one way.

The edge $(v, x, D)$ is **transitive** if there are edges $(v, w, a)$ and $(w, x, D - a)$; the read $w$ then starts and ends between $v$ and $x$. The string graph keeps the vertices that are not contained and the edges that are not transitive, which are called irreducible.

A walk $v_0 \to v_1 \to \cdots \to v_t$ with offsets $d_1, \ldots, d_t$ spells the string
$$ v_0[0..d_1) \cdot v_1[0..d_2) \cdots v_{t-1}[0..d_t) \cdot v_t . $$
Myers labels each edge with the letters of the second read beyond the end of the first one; the first read followed by these labels gives the same string.

The structure supports:

- BUILD$(r, \ell)$: construct the graph from the reads;
- OUT$(v)$: the irreducible edges out of $v$, by increasing offset;
- SPELL$(v_0, \text{steps})$: the string spelled by a walk;
- CONTAINED: the list of removed reads, which later steps place on the edges.

## Representation

Each vertex keeps its out-edges as a list of pairs (offset, head), sorted by offset. The sort order matters: the reduction reads the edges of a vertex from short to long and stops early. The reads are stored once. During the build, a hash map holds one mark for each pair (head, offset) out of the current vertex, with the states in play and eliminated. Production assemblers use the bidirected form, in which a vertex is a read with two ends, so that a read can occur on either strand.

## Operations

BUILD first computes all overlap edges, here with the prefix function of $x \, \# \, u$ for each pair, which gives all suffix-prefix matches in $O(|u| + |x|)$ time. Then it removes the transitive edges with Myers' algorithm. For each vertex $v$ it marks the heads of all edges out of $v$. It goes through the edges $(v, w, a)$ by increasing $a$, and for each edge out of $w$ that ends no further than the longest edge out of $v$, it eliminates the matching mark. An edge whose mark is already eliminated does not need to be expanded, because an earlier read covers the same edges. That skip is exact only when $v$ has at most one edge to each read; the code below turns it off otherwise.

```pseudo id=main
STRING-GRAPH(r[0 .. N − 1], ℓ)
L1  remove repeated reads and every read that is a substring of a longer read
L2  add (u, x, d) for each u ≠ x and 1 ≤ d ≤ |u| − ℓ with u[d ..] a proper prefix of x; sort each list by d
L3  for each read v do
L4      mark (w, a) inplay for each edge (v, w, a); longest ← the largest a; skip ← v has at most one edge to each read
L5      for each edge (v, w, a) by increasing a do
L6          if (w, a) is inplay or skip is false then
L7              for each edge (w, x, b) by increasing b while a + b ≤ longest do
L8                  if (x, a + b) is inplay then mark (x, a + b) eliminated
L9      keep the edges (v, w, a) whose mark is inplay; clear all marks
```

```pseudo id=spell
SPELL(v, steps)
S1  T ← empty string
S2  for each (d, x) in steps do
S3      if (v, x, d) is not an overlap edge then error
S4      T ← T · v[0 .. d); v ← x
S5  return T · v
```

After the reduction, assemblers collapse each chain of vertices with in-degree and out-degree one into one composite edge, whose label is the string of the chain. These chains are the [unitigs](/unitig/) of the graph.

## Example

The genome is `TACGGATCATGCATT`, with $G = 15$, and there are six reads:

| read | string | start |
|---|---|---|
| 0 | `TACGGAT` | 0 |
| 1 | `CGGATCA` | 2 |
| | `GGATC` | 3, contained in read 1 |
| 2 | `GATCATG` | 4 |
| 3 | `TCATGCA` | 6 |
| 4 | `ATGCATT` | 8 |

Line L1 removes `GGATC`, and five reads of length 7 remain. With $\ell = 2$, line L2 finds 8 edges:

| edge $(u, x, d)$ | overlap | status |
|---|---|---|
| $(0, 1, 2)$, $(1, 2, 2)$, $(2, 3, 2)$, $(3, 4, 2)$ | 5 | irreducible |
| $(0, 2, 4)$ | 3 | transitive through read 1, since $2 + 2 = 4$ |
| $(1, 3, 4)$ | 3 | transitive through read 2 |
| $(2, 4, 4)$ | 3 | transitive through read 3 |
| $(0, 4, 5)$ | 2 | irreducible and false: `AT` ends read 0 and starts read 4 by chance |

For $v = 0$, line L4 marks $(1, 2)$, $(2, 4)$ and $(4, 5)$ in play, with longest $= 5$. Line L5 takes $(1, 2)$; the edges out of read 1 are $(2, 2)$ and $(3, 4)$, and only the first has $2 + 2 \le 5$, so the mark $(2, 4)$ becomes eliminated. Then $(2, 4)$ is skipped, and $(4, 5)$ has no edge out of read 4 that is short enough. Line L9 keeps $(0, 1, 2)$ and $(0, 4, 5)$.

The string graph has 5 edges. The walk $0 \to 1 \to 2 \to 3 \to 4$ spells the genome, and the false edge $0 \to 4$ spells `TACGGATGCATT`. So the reduction removes redundant edges but not false ones: a branch caused by a short repeat stays in the graph. With $\ell = 3$ the false edge is not an overlap edge, and the string graph is the single chain of 4 edges. With $\ell = 4$ there are only the 4 chain edges from the start, and with $\ell = 1$ there are 13 overlap edges and 8 irreducible ones.

## Correctness

The [proof](proofs/correctness.md) shows three facts. First, every eliminated edge is transitive, because line L8 eliminates a mark only when it finds the two edges of a witness. Second, every transitive edge is eliminated. Take its witness $(w, a)$ with the smallest $a$. If the mark of $(w, a)$ were eliminated by an earlier read $w'$, then $w'$ starts before $w$ and ends after $v$, so it also overlaps $x$ by at least $\ell$ and is a witness with a smaller offset. This step needs $w' \ne x$, which the skip test ensures. Third, by strong induction on the offset, every overlap edge $(v, x, D)$ has a walk of irreducible edges from $v$ to $x$ with total offset $D$, and this walk spells the same string. So the string graph spells the same strings as the overlap graph.

## Complexity

Let $E$ be the number of overlap edges, $\Delta$ the largest out-degree, and $S$ the sum of $\deg(w)$ over the irreducible edges $(v, w)$, plus the sum over all edges out of vertices that have two edges to one read. The bounds in the first five rows are worst case.

| step | time | space |
|---|---|---|
| L1, containment by pairwise matching | $O(m \cdot n)$ | $O(n)$ |
| L2, all overlap edges and sorting | $O(m \cdot n + E \log E)$ | $O(n + E)$ |
| L3 to L9, reduction | $O(E + S)$, at most $O(E \Delta)$ | $O(\Delta)$ for the marks |
| OUT$(v)$ | $O(\deg v)$ | |
| SPELL | $O$(length of the result $+$ steps) | $O$(result) |
| reduction, Myers' random-sequence model | $O(E)$ expected | |

Myers states the bound as $O(\sum_v \mathrm{tr.deg}(v) \cdot \deg(v))$ in the worst case, where tr.deg is the out-degree after the reduction, against $O(E \Delta)$ for general [transitive reduction](/transitive-reduction/). The expected bound is his, "assuming all input sequences are equally likely", under which tr.deg$(v)$ is $O(1)$ on average. The same holds in the following simpler model. Read starts form a Poisson process of rate $N/G$, all reads have length $L$, there are no errors, and the genome has no repeat of length $\ell$ or more. Then each read has about $c(L - \ell)/L$ overlap edges, and at most one of them, the edge to the next read, is irreducible. So $S$ is about $N c$, which is $O(E)$, and the string graph has fewer than $N$ edges: about $c$ times fewer than the overlap graph, as Myers reports for real data.

The containment and overlap steps above are quadratic. Simpson and Durbin find all overlaps with an [FM-index](/fm-index/) in $O(n + P)$ time, where $P$ is the number of overlaps, and they find the irreducible edges directly in $O(n)$ time, without building the full overlap graph; these are their stated bounds for exact overlaps.

**Observed size.** Myers reports that "typically 40% of the reads" are contained, and that the bidirected string graph after chain collapsing has "between two to three orders of magnitude fewer vertices and edges than the number of reads and overlaps". These are observations on the genomes in his paper, not bounds.

## Variants

- **Bidirected string graph.** Each read has a begin end and an end end, and an edge joins ends, so that a walk can use a read on either strand. Myers takes this form from Kececioglu and Myers (1995). A walk must enter and leave each read through opposite ends.
- **Approximate overlaps.** With sequencing errors, offsets shift by a few bases and transitivity can fail. Myers' algorithm adds a tolerance FUZZ of 10 bases to the test $a + b \le$ longest, and a second pass that lets the shortest edges out of each $w$ eliminate marks. This version is a heuristic: it can keep a transitive edge or remove an edge whose offsets do not match exactly.
- **One edge per pair.** If each pair of reads has only its longest overlap, marks can be kept per vertex, as in Myers' figure, and the skip is always exact.
- **Direct construction.** SGA (Simpson and Durbin 2010) builds the string graph from an FM-index of the reads and never stores the transitive edges.
- **Long noisy reads.** Miniasm (Li 2016) builds a string graph from approximate overlaps of raw long reads found by minimap, then removes tips and pops bubbles. It does not compute a consensus, so its output has the error rate of the reads.
- **de Bruijn graph.** A string graph of all $k$-mers with $\ell = k - 1$ has an edge for each pair of adjacent $k$-mers. A [de Bruijn graph](/de-bruijn-graph/) keeps the same information with the $(k-1)$-mers as vertices. The string graph uses the whole read instead of cutting it into $k$-mers, so it keeps repeats shorter than a read resolved.

## When to use it

Use a string graph for overlap-based assembly when the reads are long compared to the repeats, as for long reads of 10 kb or more. It replaces the overlap graph after [overlap detection](/overlap-detection/) and before the layout step of [overlap-layout-consensus](/overlap-layout-consensus/), and the [graph simplification](/assembly-graph-simplification/) steps operate on it. For short reads at high coverage, a de Bruijn graph usually needs less memory, unless the overlaps come from a compressed index as in SGA.

## Pitfalls

- **Contained reads must be removed first.** A contained read has edges to and from the neighbours of the longer read, and these edges are not transitive in the sense above. Myers keeps the contained reads aside and maps them back to the edges later, for coverage statistics.
- **The reduction does not remove false edges.** A chance overlap, as the edge $0 \to 4$ in the example, is irreducible when no read lies between its ends. Choose $\ell$ large enough, and remove such branches in later simplification steps.
- **Multi-edges and the skip.** Periodic reads can overlap in more than one way. With marks keyed by (head, offset), skipping eliminated edges can then keep a transitive edge: for the reads `BBBBAB`, `BBABB` and `BABBA` with $\ell = 1$, the edge from `BBBBAB` to `BBABB` with offset 5 goes through `BABBA`, whose own edge is eliminated only through `BBABB`. The code above disables the skip for such vertices.
- **Errors break exact transitivity.** An error in the read $w$ can hide the edge $w \to x$, so the shortcut $v \to x$ stays. Correct the reads first, see [read error correction](/read-error-correction/), or use the FUZZ rule.
- **A walk is not an assembly.** The graph spells every assembly that agrees with the reads. Choosing the walk across a repeat needs more data, such as coverage or [paired-end reads](/paired-end-reads/); see [repeat resolution](/repeat-resolution/).

## Implementations

## History

Kececioglu and Myers (1995) introduced the bidirected graph for fragment assembly with reads from both strands. Myers (2005) defined the string graph, gave the transitive reduction algorithm with its expected linear time, and described the chain collapsing and the estimate of how many times each composite edge occurs in the genome. Simpson and Durbin (2010) built the string graph directly from an FM-index in the SGA assembler, so that the overlap graph of short reads at high coverage never has to be stored. Li (2016) used the string graph in miniasm for noisy long reads, and later long-read assemblers also build string graphs.

## References
