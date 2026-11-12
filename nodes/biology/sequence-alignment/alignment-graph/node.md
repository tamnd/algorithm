---
tag: ECTZ11
kind: concept
slug: alignment-graph
name: Alignment graph (edit graph)
aliases:
- edit graph
- alignment grid
area: biology/sequence-alignment
level: core
summary: A grid DAG on the pairs of prefix lengths whose corner-to-corner paths are the global alignments of two sequences, so the best alignment is a heaviest path.
prereqs: [alignment-score, dag-longest-path]
see_also: [pairwise-sequence-alignment, needleman-wunsch, smith-waterman, hirschberg-algorithm, dot-matrix-plot, counting-lattice-paths, gotoh-algorithm, sequence-to-graph-alignment]
sources:
  - book: isbn:9780521585194
    title: Dan Gusfield, Algorithms on Strings, Trees, and Sequences, Cambridge University Press, 1997
    locator: Chapter 11, the section on edit graphs (the weighted grid graph and the correspondence of its paths with alignments)
  - book: isbn:9780262101066
    title: Neil C. Jones and Pavel A. Pevzner, An Introduction to Bioinformatics Algorithms, MIT Press, 2004
    locator: Chapter 6, the Manhattan tourist problem and Section 6.4 (alignments as paths in the alignment grid)
  - paper: "Eugene W. Myers, An O(ND) difference algorithm and its variations, Algorithmica 1(2), 1986, 251-266"
    locator: the edit graph of two strings, in which a shortest path gives the edit script
  - paper: "Cyril Banderier and Sylviane Schwer, Why Delannoy numbers?, Journal of Statistical Planning and Inference 135(1), 2005, 40-54"
    locator: the definition of the Delannoy numbers and their closed forms
---

The alignment graph of two sequences $x$ and $y$ of lengths $m$ and $n$ is a directed acyclic grid. Its vertices are the pairs $(i, j)$ with $0 \le i \le m$ and $0 \le j \le n$, and it has a diagonal, a vertical and a horizontal edge into each vertex, one for each kind of alignment column. Each path from the corner $(0, 0)$ to the corner $(m, n)$ is one global alignment, and the weight of the path is the [alignment score](/alignment-score/). So an optimal alignment is a heaviest path, and every dynamic program of this area, from [Needleman-Wunsch](/needleman-wunsch/) to [Hirschberg's algorithm](/hirschberg-algorithm/), is a [longest path in a DAG](/dag-longest-path/) on this graph. In the unit-cost setting the same graph is called the edit graph, and the shortest path gives the [edit distance](/edit-distance/).

## In plain words

Draw a grid of streets. One sequence is written along the top, one letter between each pair of north-south streets, and the other is written down the side. You start at the top left corner and must reach the bottom right corner, and you may only go right, down, or diagonally down and right.

A diagonal step uses one letter of each sequence: it puts them in the same column. A step down uses a letter of the side sequence alone, against a gap. A step right does the same for the top sequence. So each route from corner to corner is one way to line up the two sequences, and each way to line them up is one route. Put the score of each column on its street. Then the best alignment is the route with the largest total.

## The idea

### The graph

**Model.** The input is $x = x_1 \cdots x_m$ and $y = y_1 \cdots y_n$ over an alphabet $\Sigma$, a substitution score $s$, and a linear gap penalty $d$ per gap symbol. The graph $G(x, y)$ has

- the vertices $(i, j)$ for $0 \le i \le m$ and $0 \le j \le n$, so $(m + 1)(n + 1)$ vertices;
- a diagonal edge $(i - 1, j - 1) \to (i, j)$ of weight $s(x_i, y_j)$, for the column $(x_i, y_j)$;
- a vertical edge $(i - 1, j) \to (i, j)$ of weight $-d$, for the column $(x_i, -)$;
- a horizontal edge $(i, j - 1) \to (i, j)$ of weight $-d$, for the column $(-, y_j)$.

It has $mn$ diagonal, $m(n + 1)$ vertical and $(m + 1)n$ horizontal edges, so $3mn + m + n$ edges. Each edge increases $i + j$, so the graph has no cycle, and the row-major order of the vertices is a [topological order](/topological-sort/).

The vertex $(i, j)$ stands for the state "the first $i$ letters of $x$ and the first $j$ letters of $y$ are aligned". So a path from $(0, 0)$ to $(i, j)$ is an alignment of the prefixes $x_1 \cdots x_i$ and $y_1 \cdots y_j$.

### Paths are alignments

**Claim.** The paths from $(0, 0)$ to $(m, n)$ correspond one to one to the global alignments of $x$ and $y$, and the weight of a path is the score of its alignment.

*Proof.* Map a path to the sequence of the columns of its edges. A path to $(m, n)$ has $i$ and $j$ go up from 0 to $m$ and $n$. The edges that increase $i$ put $x_1, \ldots, x_m$ in order in the top row, and the edges that increase $j$ put $y_1, \ldots, y_n$ in order in the bottom row. No edge gives the column $(-, -)$. So the result is an alignment. In the other direction, read the columns of an alignment from left to right; each column is the edge from the current vertex to the next one. The two maps are inverse to each other. The weight of the path is the sum of the column scores, which is $S(A)$ for a linear gap penalty. $\square$

So the best global score is the weight of a heaviest path from $(0, 0)$ to $(m, n)$. With $F(i, j)$ the heaviest weight of a path from $(0, 0)$ to $(i, j)$, the DAG longest-path rule, "the best of the incoming edges", is the Needleman-Wunsch recurrence.

### The number of alignments

Let $D(m, n)$ be the number of paths from $(0, 0)$ to $(m, n)$, that is the number of global alignments. The last edge is one of three, so

$$D(m, n) = D(m - 1, n - 1) + D(m - 1, n) + D(m, n - 1), \qquad D(i, 0) = D(0, j) = 1.$$

These are the *Delannoy numbers*. A closed form: an alignment with $k$ pair columns has $m - k$ deletion and $n - k$ insertion columns, $m + n - k$ columns in all, and every order of these column types gives exactly one alignment. So

$$D(m, n) = \sum_{k = 0}^{\min(m, n)} \frac{(m + n - k)!}{k! \,(m - k)! \,(n - k)!} = \sum_{k = 0}^{\min(m, n)} \binom{m}{k} \binom{n}{k} 2^k.$$

The second form is a known identity of the same numbers. For $m = n$ they grow like $(3 + 2\sqrt{2})^n / \sqrt{n}$, up to a constant factor, and $3 + 2\sqrt{2} \approx 5.83$. Some authors count fewer alignments, because they treat a deletion next to an insertion, $(a, -)(-, b)$, as the same as $(-, b)(a, -)$; the graph counts them as two paths.

### Other forms on the same graph

- **[Local alignment](/local-alignment/).** Add a source with an edge of weight 0 to every vertex, and an edge of weight 0 from every vertex to a sink. A heaviest source-to-sink path is a best alignment of a substring of $x$ with a substring of $y$. The 0 in the [Smith-Waterman](/smith-waterman/) recurrence is the edge from the source.
- **[Semi-global alignment](/semi-global-alignment/).** Give weight 0 to the edges of the first column or the first row, which lets the path start anywhere on the left or top border, and add free edges from the last row or column to the sink.
- **Affine gaps.** A gap opening costs more than a gap extension, so a vertex must know whether the path arrives in a gap. Three copies of the grid, one for each kind of last column, make the graph of the [Gotoh algorithm](/gotoh-algorithm/).
- **Edit distance and LCS.** With costs instead of scores, the shortest path gives the [edit distance](/edit-distance/). In the edit graph of Myers (1986), a diagonal edge exists only where $x_i = y_j$; the path with the most diagonal edges gives a [longest common subsequence](/longest-common-subsequence/).
- **Linear space.** Every corner-to-corner path crosses the middle row $i = \lfloor m/2 \rfloor$. The heaviest path through a vertex $(i, j)$ weighs $F(i, j) + B(i, j)$, where $B$ is the heaviest path from $(i, j)$ to $(m, n)$. [Hirschberg's algorithm](/hirschberg-algorithm/) finds the best crossing vertex and recurses on the two halves.
- **Bands and seeds.** A [banded alignment](/banded-alignment/) keeps only the vertices near the main diagonal. A [dot matrix plot](/dot-matrix-plot/) marks the diagonal edges between equal letters, which are the cheap steps of a good path.
- **Graphs of sequences.** If one sequence is replaced by a graph, the product of that graph with a path is again a DAG, or a graph with cycles that needs more care: [sequence-to-graph alignment](/sequence-to-graph-alignment/).

## Examples

**A small graph.** Take $x = $ AC and $y = $ A, with the toy scheme $s(a, a) = +2$, $s(a, b) = -1$, $d = 2$. The graph has $3 \times 2 = 6$ vertices and $3 \cdot 2 + 2 + 1 = 9$ edges. There are $D(2, 1) = 5$ paths from $(0, 0)$ to $(2, 1)$:

| path | alignment | score |
|---|---|---|
| $(0,0) \to (1,1) \to (2,1)$ | `AC` over `A-` | $2 - 2 = 0$ |
| $(0,0) \to (1,0) \to (2,1)$ | `AC` over `-A` | $-2 - 1 = -3$ |
| $(0,0) \to (1,0) \to (2,0) \to (2,1)$ | `AC-` over `--A` | $-6$ |
| $(0,0) \to (1,0) \to (1,1) \to (2,1)$ | `A-C` over `-A-` | $-6$ |
| $(0,0) \to (0,1) \to (1,1) \to (2,1)$ | `-AC` over `A--` | $-6$ |

The heaviest path takes the diagonal edge A to A first, with weight 0.

**The number of alignments.** The table gives $D(m, n)$ for small lengths. The value 1683 for $m = n = 5$ is the number of alignments of ACGTC and AGTAC, of which the [Needleman-Wunsch](/needleman-wunsch/) page finds the best one.

| $m \backslash n$ | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| 0 | 1 | 1 | 1 | 1 | 1 | 1 |
| 1 | 1 | 3 | 5 | 7 | 9 | 11 |
| 2 | 1 | 5 | 13 | 25 | 41 | 61 |
| 3 | 1 | 7 | 25 | 63 | 129 | 231 |
| 4 | 1 | 9 | 41 | 129 | 321 | 681 |
| 5 | 1 | 11 | 61 | 231 | 681 | 1683 |

Each entry is the sum of the entries to the left, above, and above-left, for example $D(3, 2) = D(2, 1) + D(2, 2) + D(3, 1) = 5 + 13 + 7 = 25$. Further, $D(10, 10) = 8097453$, and $D(100, 100)$ has 76 decimal digits. To try every alignment is out of the question, but the graph has only $(m + 1)(n + 1)$ vertices, so a longest-path computation takes $\Theta(mn)$ time.

## Where it is used

- [Needleman-Wunsch](/needleman-wunsch/), [Smith-Waterman](/smith-waterman/) and the [semi-global DP](/semi-global-dp/) are longest-path computations on this graph, each with its own start and end vertices.
- [Hirschberg's algorithm](/hirschberg-algorithm/) uses the forward and backward path weights through the middle row.
- The [Gotoh algorithm](/gotoh-algorithm/) uses a three-layer version for affine gaps.
- [Banded alignment](/banded-alignment/) and [X-drop extension](/x-drop-extension/) explore only a part of the graph.
- [Colinear chaining](/colinear-chaining/) chains exact matches, which are diagonal runs of the graph, before an alignment fills the gaps between them.
- The [Myers bit-parallel algorithm](/myers-bit-parallel-algorithm/) and the $O(ND)$ algorithm of Myers work on the unit-cost edit graph.

## References
