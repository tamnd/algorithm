---
tag: QXKQRZ
kind: data-structure
slug: overlap-graph
name: Overlap graph
area: biology/genome-assembly
level: core
summary: Directed graph with one vertex per read and an arc, weighted by the overlap length, for each suffix-prefix overlap of at least a minimum length.
prereqs: [directed-graph, adjacency-list, overlap, shotgun-sequencing]
see_also: [overlap-detection, overlap-layout-consensus, string-graph, shortest-common-superstring, greedy-shortest-common-superstring, hamiltonian-path-problem, de-bruijn-graph, generalized-suffix-tree]
sources:
  - paper: doi:10.1007/BF01188580
    title: John D. Kececioglu and Eugene W. Myers, Combinatorial algorithms for DNA sequence assembly, Algorithmica 13(1/2), 1995
    locator: pp. 7 to 51, the overlap graph of fragments and the layout as a path through it
  - paper: doi:10.1126/science.287.5461.2196
    title: Eugene W. Myers et al., A whole-genome assembly of Drosophila, Science 287(5461), 2000
    locator: pp. 2196 to 2204, the overlapper and the overlap graph of the Celera assembler
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Section 7.10 (all-pairs suffix-prefix matching) and Chapter 16 (fragment assembly and the shortest superstring)
  - paper: "Dan Gusfield, Gad M. Landau and Baruch Schieber, An efficient algorithm for the all pairs suffix-prefix problem, Information Processing Letters 41(4), 1992"
    locator: pp. 181 to 185, all longest suffix-prefix overlaps in O(n + m^2) time
  - book: isbn:9780990374602
    title: Phillip Compeau and Pavel Pevzner, Bioinformatics Algorithms, An Active Learning Approach, Volume 1, second edition
    locator: Chapter 3, the overlap graph and genome reconstruction as a Hamiltonian path
---

The overlap graph of a set of sequencing reads is the directed graph with one vertex for each read and an arc from read $a$ to read $b$ when a suffix of $a$ equals a prefix of $b$ over at least a minimum length $\ell$; the arc stores the length of the longest such [overlap](/overlap/). A layout of the reads along the genome is a path in this graph, and the string that the path spells is a candidate genome. It is the central structure of [overlap-layout-consensus](/overlap-layout-consensus/) assembly, and its maximum-weight Hamiltonian paths give the shortest common superstrings. Its size grows with the coverage, so assemblers usually reduce it to a [string graph](/string-graph/).

## In plain words

Write each short piece of text on a card and lay all the cards on a table. Draw an arrow from one card to another when the end of the first card spells the same letters as the start of the second, over a long enough stretch. Write on the arrow how many letters they share.

Two cards cut from neighbouring places of the long text are joined by such an arrow, because they share the part of the text where they overlap. To rebuild the text, you walk along the arrows from card to card, and on each step you add only the new letters of the next card. A walk that visits every card once spells the whole text, if the arrows are true. Arrows can also be false, when two different places of the text spell the same letters.

## The abstract type

**Model.** The genome is a string $x$ of length $G$. The input is a list of $m$ reads $r_0, \ldots, r_{m-1}$, nonempty strings over an alphabet (DNA uses $\{A, C, G, T\}$), of total length $n$ and maximum length $L$. In the assembly model there are $N = m$ reads of length about $L$ and the coverage is $c = NL/G$. This page treats exact overlaps; with sequencing errors the arcs come from approximate matches, see [overlap detection](/overlap-detection/).

For reads $a \ne b$, $\mathrm{ov}(a, b)$ is the length of the longest string that is a proper suffix of $a$ and a proper prefix of $b$. For a minimum overlap $\ell \ge 1$, the overlap graph is
$$ O_\ell = (V, E), \quad V = \{0, \ldots, m - 1\}, \quad E = \{ (i, j) : i \ne j, \ \mathrm{ov}(r_i, r_j) \ge \ell \}, \quad w(i, j) = \mathrm{ov}(r_i, r_j). $$
It is a [directed graph](/directed-graph/) without self-loops and with at most one arc for each ordered pair. Some texts use the complete graph ($\ell = 0$), where every ordered pair has an arc of weight $\mathrm{ov} \ge 0$.

The structure supports:

- BUILD$(r, \ell)$: construct the graph from the reads;
- WEIGHT$(i, j)$: the weight of the arc, or 0 if there is none;
- OUT$(i)$ and IN$(j)$: the arcs that leave $i$ or enter $j$, with their weights;
- SPELL$(i_0, \ldots, i_t)$: the string spelled by a path of arcs.

The spelled string of a path is $r_{i_0}$ followed, for each $q \ge 1$, by $r_{i_q}$ without its first $w(i_{q-1}, i_q)$ letters. It contains every read on the path and has length $\sum_q |r_{i_q}| - \sum_{q \ge 1} w(i_{q-1}, i_q)$.

## Representation

Each vertex keeps two hash maps, from out-neighbour to weight and from in-neighbour to weight, which is an [adjacency list](/adjacency-list/) with constant expected lookup time. The reads themselves are stored once. Large assemblers also store, for each arc, the offset of the second read relative to the first and the strands of the two reads, because DNA has two strands; this page uses one strand.

## Operations

BUILD works on the reads sorted as strings. For every read $i$ and every overlap length $k$ from long to short, it takes the suffix $u$ of length $k$ and finds, by binary search, the block of sorted reads that start with $u$. The first $k$ at which a read $j$ appears is the longest overlap from $i$ to $j$.

```pseudo id=main
BUILD-OVERLAP-GRAPH(r[0 .. m − 1], ℓ)
L1  P ← the read indices sorted by read string
L2  for i ← 0 to m − 1 do
L3      for k ← |r_i| − 1 down to ℓ do
L4          u ← the suffix of r_i of length k
L5          [lo, hi) ← the positions of P whose reads start with u, by two binary searches
L6          for each j = P[p] with lo ≤ p < hi, j ≠ i, |r_j| > k and no arc (i, j) yet do
L7              add the arc (i, j) with weight k to out[i] and to in[j]
```

The test $|r_j| > k$ in line L6 makes the overlap a proper prefix of $r_j$; line L3 starts at $|r_i| - 1$, so it is a proper suffix of $r_i$. A read contained in another read gets no arc of full length for that reason.

```pseudo id=spell
SPELL(i_0, …, i_t)
S1  T ← r[i_0]
S2  for q ← 1 to t do
S3      if (i_{q−1}, i_q) is not an arc then error
S4      T ← T · r[i_q][w(i_{q−1}, i_q) ..]
S5  return T
```

## Example

The genome is $x =$ `TACGGATCATGCATT`, with $G = 15$. Its repeats are short: `CAT` occurs at positions 7 and 11, and `AT` and `CA` occur at two or more places. Five reads of length 7 start at positions 0, 2, 4, 6 and 8:

| $i$ | read | start |
|---|---|---|
| 0 | `TACGGAT` | 0 |
| 1 | `CGGATCA` | 2 |
| 2 | `GATCATG` | 4 |
| 3 | `TCATGCA` | 6 |
| 4 | `ATGCATT` | 8 |

With $\ell = 2$ the graph has 8 arcs:

| arc | weight | why |
|---|---|---|
| $0 \to 1$, $1 \to 2$, $2 \to 3$, $3 \to 4$ | 5 | neighbours in $x$, 2 positions apart |
| $0 \to 2$, $1 \to 3$, $2 \to 4$ | 3 | 4 positions apart |
| $0 \to 4$ | 2 | false: `AT` ends read 0 at position 5 and starts read 4 at position 8 |

The path $0 \to 1 \to 2 \to 3 \to 4$ spells $35 - 20 = 15$ letters, the genome. The path $0 \to 2 \to 4$ skips two reads and spells the same 15 letters, because its arcs are the transitive arcs of the first path. The path $0 \to 4$ follows the false arc and spells `TACGGATGCATT`, which is not a substring of $x$. With $\ell = 3$ the false arc goes away and 7 arcs remain; with $\ell = 4$ only the four arcs of weight 5 remain; with $\ell = 1$ there are 12 arcs.

## Correctness

The proof file shows three facts. Sorted strings that start with a given $u$ form one block, and the two binary searches of line L5 find it. A read $j$ appears in the block of the suffix of length $k$ exactly when that suffix is a prefix of $r_j$, and line L6 keeps it only when the match is proper on both sides. Since $k$ goes down, the first $k$ at which $j$ is added is the largest such $k$, which is $\mathrm{ov}(r_i, r_j)$, and no arc is added when this value is below $\ell$. Line L7 writes each arc into both maps. For SPELL, each removed prefix of $r_{i_q}$ equals the end of the text written so far, so the text contains every read of the path.

## Complexity

Let $m$ be the number of reads, $n$ their total length, $L$ the longest read and $E$ the number of arcs. Let $P$ be the number of triples $(i, j, k)$ with $i \ne j$, $k \ge \ell$ and a proper suffix-prefix match of length $k$ from $r_i$ to $r_j$; then $E \le P$. The bounds are worst case on the word RAM, with expected constant time for a hash map access.

| operation | time | space |
|---|---|---|
| BUILD, sorting (line L1) | $O(L \cdot m \log m)$ | $O(m)$ |
| BUILD, lines L2 to L7 | $O(n \cdot L \log m + P)$ | $O(n + E)$ |
| WEIGHT | $O(1)$ expected | |
| OUT$(i)$, IN$(j)$ | $O(\deg)$, or $O(\deg \log \deg)$ sorted | |
| SPELL of a path | $O$(length of the result $+ t$) | $O$(result) |

Each suffix in line L4 is a slice of up to $L$ letters, and each of the $O(\log m)$ comparisons of the binary searches reads up to $L$ letters. The suffix-tree method of Gusfield, Landau and Schieber finds all longest overlaps in $O(n + m^2)$ time, which is better when $L$ is large and the reads are few.

**Size.** In the worst case $E = m(m - 1)$: with all reads equal to `AAA…A`, every ordered pair overlaps. For shotgun data the expected size depends on the model. Assume reads of length $L$ with starts that form a Poisson process of rate $N/G$, a genome without repeats of length $\ell$ or more, and no errors. Then the reads that start within $L - \ell$ positions after a read are exactly its true out-neighbours, so the expected out-degree is about $(N/G)(L - \ell) = c(L - \ell)/L$, and $E \approx N c (L - \ell)/L$. The graph thus grows linearly in the coverage per read, and most of the arcs are transitive: in the example, the arcs of weight 3 add nothing that the arcs of weight 5 do not give. If instead the genome is a uniform random string over four letters, a fixed pair of reads from far apart has a chance overlap of length at least $\ell$ with probability at most $\sum_{k \ge \ell} 4^{-k} = \tfrac{4}{3} \cdot 4^{-\ell}$, which is why $\ell$ of about 20 or more removes almost all chance arcs between millions of reads.

## Variants

- **Overlap graph with all overlaps.** Some texts keep one arc for each matching length $k \ge \ell$, not only the longest. This multigraph is the input of the transitive reduction in the [string graph](/string-graph/).
- **Bidirected overlap graph.** For double-stranded DNA each read has two ends, and an arc joins ends, so that a read can be used in either orientation. This is the form in the Celera assembler and in Myers' string graph.
- **Approximate overlaps.** With sequencing errors, an arc carries an alignment of the overlap with an error rate, as in the output of [overlap detection](/overlap-detection/) tools.
- **Complete weighted graph.** With $\ell = 0$, a maximum-weight Hamiltonian path gives a [shortest common superstring](/shortest-common-superstring/) of a substring-free read set, by the merge formula on that page. Finding it is NP-hard; see the [NP-hardness theorem](/shortest-common-superstring-np-hard/).
- **Distance graph.** The weight $|r_i| - w(i, j)$ is the number of new letters, and the shortest superstring is then a minimum [asymmetric traveling salesman](/asymmetric-tsp/) path.
- **de Bruijn graph.** Take the distinct $k$-mers of the reads as the reads, and $\ell = k - 1$. This overlap graph is, apart from self-loops, the [line graph](/line-graph/) of the [de Bruijn graph](/de-bruijn-graph/) whose vertices are the $(k-1)$-mers and whose arcs are the $k$-mers. A Hamiltonian path in the first graph is an Eulerian path in the second, which can be found in linear time.

## When to use it

Use the overlap graph when the reads are long compared to the repeats and few compared to the genome length, for example for long reads of 10 to 100 kb at coverage 30, or for Sanger reads. It keeps the whole read sequence, so it handles repeats shorter than the reads. For short reads at high coverage, the number of arcs grows with the coverage and the cost of all-pairs overlaps grows faster, and a de Bruijn graph is cheaper.

## Pitfalls

- **Contained reads.** A read inside another read has no proper overlap of full length with it, but it has arcs to and from the neighbours of the longer read. These arcs add paths that spell the same text. Remove contained reads first, as the string graph does.
- **Self-loops and duplicates.** A read with a border, such as `ACGAC`, overlaps itself, and two equal reads overlap each other. Self-loops are excluded by $i \ne j$; duplicate reads should be collapsed before the build.
- **A minimum overlap that is too short.** Short overlaps match by chance and add false arcs, as the arc $0 \to 4$ above. Choose $\ell$ well above $\log_4 G$ for a genome of length $G$.
- **A minimum overlap that is too long.** If $\ell$ is above the true overlap of two neighbouring reads, the graph breaks into pieces at that place, and the layout has a gap.
- **Hamiltonian path as the goal.** The genome is a path through all reads only if there are no errors and no unresolved repeats. A maximum-weight Hamiltonian path is a shortest superstring, which collapses repeats; assemblers instead simplify the graph and output the unambiguous paths as contigs.
- **One strand.** Real reads come from both strands. Without reverse complements, half of the true overlaps are missing.

## Implementations

## History

Overlap-based fragment assembly predates the formal graph. Kececioglu and Myers (1995) gave a combinatorial treatment of the assembly problem with overlaps between fragments, and the Celera assembler, which assembled the Drosophila genome in 2000, was built around an overlapper and a graph of overlaps. Gusfield, Landau and Schieber (1992) gave the $O(n + m^2)$ algorithm for all longest suffix-prefix overlaps. Myers (2005) replaced the overlap graph with the string graph, which removes the transitive arcs and the contained reads.

## References
