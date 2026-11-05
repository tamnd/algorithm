---
tag: M16F3Q
kind: data-structure
slug: succinct-graph-representation
name: Succinct graph representation
aliases:
- succinct graphs
area: graphs/graph-representation
level: research
summary: Graph encoding close to the information-theoretic minimum while supporting fast queries.
implements: [graph]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of arcs, s: the number of arcs in the bucket of the query}
  time: {adjacent: O(1 + s), degree: O(1 + s), neighbor: O(1 + s)}
  space: {total: "m log(n^2 / m) + 2 m + o(m)"}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [graph, adjacency-matrix, elias-fano-encoding, rank-select-dictionary]
see_also: [succinct-data-structures, elias-fano-encoding, bit-vector, webgraph-compression, compressed-sparse-row, ordinal-tree, planar-graph, wavelet-tree]
sources:
  - book: isbn:9781107152380
    title: Gonzalo Navarro, Compact Data Structures, Cambridge University Press, 2016
    locator: Chapter 9 (Graphs), the information-theoretic bound for general graphs, adjacency lists on bit vectors, and the representations of planar graphs and web graphs
  - paper: doi:10.1109/SFCS.1989.63533
    title: Guy Jacobson, Space-efficient static trees and graphs, FOCS 1989
    locator: pages 549 to 554, rank and select on bit vectors and the O(n)-bit encodings of trees and planar graphs
---

A succinct graph representation stores a [graph](/graph/) in a number of bits close to the information-theoretic minimum, and still answers queries such as adjacency, degree and the $i$-th neighbour fast, without decompressing. A directed graph with $n$ vertices and $m$ arcs is one of $\binom{n^2}{m}$ graphs, so any encoding needs $\log_2 \binom{n^2}{m} \approx m \log_2(n^2/m) + 1.44m$ bits in the worst case. This page builds one structure that meets this bound up to $O(m)$ bits: the [Elias-Fano encoding](/elias-fano-encoding/) of the positions of the 1s of the [adjacency matrix](/adjacency-matrix/), queried by rank and select on a [bit vector](/bit-vector/). It uses about $m(2 + \log_2(n^2/m))$ bits, against $n^2$ bits for the matrix and $m \lceil \log_2 n \rceil$ bits plus pointers for an adjacency array.

## In plain words

Write the adjacency matrix row after row as one long line of $n^2$ cells, and keep only the numbers of the cells that hold an arc. These numbers are sorted, so store them by their differences: split each number into a high part and a few low bits, write the low bits as they are, and write the high parts as a short line of marks that counts how many numbers fall in each bucket. To ask whether $u$ points to $v$, look up the cell number $un + v$ in this list. The neighbours of $u$ are the numbers between $un$ and $un + n$, and the degree is how many there are.

## The abstract type

A static directed [graph](/graph/) on $0, \ldots, n - 1$ without parallel arcs; an undirected graph stores each edge as two arcs. It supports `build(n, arcs)`, `adjacent(G, u, v)`, `degree(G, u)` (the out-degree) and `neighbor(G, u, i)`, the $i$-th smallest out-neighbour. Updates are not supported.

## Representation

Let $p_0 < p_1 < \cdots < p_{m-1}$ be the numbers $un + v$ of the arcs $(u, v)$, in the universe $[0, n^2)$, and let $l = \lfloor \log_2(n^2 / m) \rfloor$ (and $l = 0$ when $m = 0$). The fields are:

- `low[i]`, the $l$ low bits of $p_i$, packed in $ml$ bits.
- `high`, a bit vector of length $m + \lfloor n^2 / 2^l \rfloor + 1$ with a 1 at position $\lfloor p_i / 2^l \rfloor + i$ for each $i$, and 0 elsewhere.
- A rank and select index on `high`, of $o(\text{length})$ bits in theory, that gives `select1(i)`, the position of the $i$-th 1, and `select0(j)`, the position of the $j$-th 0, both counted from 0.

**Invariant.** Read `high` from the left: the run of 1s before the $h$-th 0 lists, in order, the elements with high part $h$. So the number of 0s before the 1 of element $i$ is $\lfloor p_i / 2^l \rfloor$, and $p_i = ((\texttt{select1}(i) - i) \cdot 2^l) + \texttt{low}[i]$.

## Operations

```pseudo id=main
ACCESS(G, i)                             ▷ the i-th smallest position
L1  return ((select1(high, i) − i) · 2^l) + low[i]

RANK(G, x)                               ▷ the number of positions < x
L2  h ← ⌊x / 2^l⌋
L3  q ← (if h > 0 then select0(high, h − 1) + 1 else 0)    ▷ start of bucket h
L4  k ← q − h                            ▷ elements in buckets < h
L5  while high[q] = 1 and low[k] < x mod 2^l do
L6      k ← k + 1; q ← q + 1
L7  return k

ADJACENT(G, u, v)
L8  p ← u · n + v
L9  k ← RANK(G, p)
L10 return k < m and ACCESS(G, k) = p

DEGREE(G, u)
L11 return RANK(G, (u + 1) · n) − RANK(G, u · n)

NEIGHBOR(G, u, i)
L12 return ACCESS(G, RANK(G, u · n) + i) − u · n
```

**Access.** Line L1 recovers the high part as the number of 0s before the 1 of element $i$.

**Rank.** Line L3 finds where the bucket of $x$ starts, line L4 counts the 1s before it, and lines L5 and L6 step over the elements of the bucket that are still below $x$. The loop runs at most $s$ times, where $s$ is the size of the bucket; since there are about $m$ buckets for $m$ elements, $s$ is $O(1)$ on average.

**Adjacent, degree, neighbor.** All reduce to one or two ranks and one access. The neighbours of $u$ are the positions in $[un, un + n)$, already sorted.

## Example

Take $n = 4$ and the arcs $(0,1), (0,2), (1,2), (2,0), (2,3), (3,3)$. The positions are $1, 2, 6, 8, 11, 15$, so $m = 6$, $l = \lfloor \log_2(16/6) \rfloor = 1$, the low bits are $1, 0, 0, 0, 1, 1$ and the high parts are $0, 1, 3, 4, 5, 7$.

| field | value |
|---|---|
| `low` | 1 0 0 0 1 1 |
| `high` (positions 0 to 14) | 1 0 1 0 0 1 0 1 0 1 0 0 1 0 0 |
| size | $6 \cdot 1 + 15 = 21$ bits |

- ADJACENT$(2, 3)$: $p = 11$, $h = 5$. The 0 of index 4 is at position 8, so $q = 9$ and $k = 4$. $\texttt{high}[9] = 1$ but $\texttt{low}[4] = 1$ is not below $11 \bmod 2 = 1$, so RANK returns 4. ACCESS$(4) = (9 - 4) \cdot 2 + 1 = 11$, so the answer is true.
- DEGREE$(2)$ = RANK$(12)$ − RANK$(8)$ = $5 - 3 = 2$, and NEIGHBOR$(2, 0)$ = ACCESS$(3) - 8 = 0$.

This tiny graph is denser than the regime the structure is for: $\log_2 \binom{16}{6} \approx 13$ bits is the minimum and the plain matrix uses 16. For $n = 200$ and $m = 1000$ random arcs, $l = 5$ and the structure uses 7,251 bits, against 40,000 for the matrix, 8,000 for the bare neighbour array of 8-bit entries, and the bound of about 6,740.

## Correctness

The invariant holds after `build` by construction: the 1 of element $i$ is at $\lfloor p_i / 2^l \rfloor + i$, and these positions increase strictly with $i$ because the $p_i$ do. ACCESS inverts this, RANK counts the elements of the buckets below $\lfloor x / 2^l \rfloor$ and then the elements of the bucket of $x$ with smaller low bits, and the other operations follow from the order $p = un + v$. The full proof is in `proofs/correctness.md`.

## Complexity

The model is the [word RAM](/word-ram/) with words of $\Theta(\log n)$ bits.

| operation | time | space |
|---|---|---|
| build (from sorted positions) | $O(m + n^2 / 2^l) = O(m)$ | |
| access | $O(1)$ with constant-time select | |
| adjacent, degree, neighbor | $O(1 + s)$ | |
| all fields | | $ml + m + n^2/2^l + 1 \le m(2 + \log_2(n^2/m)) + 1$ bits |
| rank/select index | | $o(m + n^2 / 2^l)$ bits |

The bound $n^2 / 2^l \le 2m$ follows from $2^l > n^2 / (2m)$. With $\log_2 \binom{N}{m} \ge m \log_2(N/m)$, the structure uses at most $2m + o(m)$ bits more than the minimum. Listing all neighbours of $u$ takes $O(1 + d(u))$ by reading `high` sequentially instead of calling select for each one. The Python implementation uses a binary search over word counts for select, so its select costs $O(\log m)$.

## Variants

- **Adjacency lists on a bit vector.** Store the out-neighbours of all vertices in one array of $m \lceil \log_2 n \rceil$ bits, and the degrees as a unary bit vector $1 0^{d(0)} 1 0^{d(1)} \cdots$ with select. This uses $m \log n + O(n + m)$ bits, more than the bound when $m$ is large, but lists neighbours in $O(1)$ each.
- **Planar graphs.** A planar graph has at most $3n - 6$ edges, and $O(n)$ bits suffice: Turán gave an encoding of $12n$ bits, and Jacobson showed how to answer adjacency and degree fast in $O(n)$ bits through book embeddings written as [balanced parentheses](/balanced-parentheses/).
- **Trees.** A tree with $n$ nodes takes $2n + o(n)$ bits; see [ordinal trees](/ordinal-tree/) and [DFUDS](/dfuds/).
- **Graphs with structure.** Web and social graphs are far below the worst-case bound, because their arcs are local and their lists repeat; [WebGraph compression](/webgraph-compression/) and the $k^2$-tree exploit this, and a [wavelet tree](/wavelet-tree/) over the concatenated lists also gives in-neighbours.

## When to use it

Use a succinct representation when the graph is static, too large for memory in a usual form, and queried by random access: road networks, web crawls, knowledge graphs, genome graphs. If the graph changes often, use an [adjacency list](/adjacency-list/). If it is only scanned in order, a compressed stream such as [WebGraph](/webgraph-compression/) or a [compressed sparse row](/compressed-sparse-row/) array with gap coding is simpler and often smaller.

## Pitfalls

- **Forgetting the index.** Without the select directory, line L1 and line L3 scan `high` from the start and every query is linear. The directory is part of the structure.
- **The choice of $l$.** With $l$ too large, `low` wastes bits; with $l$ too small, `high` grows as $n^2/2^l$. Use $l = \lfloor \log_2(n^2/m) \rfloor$, as in the representation, and $l = 0$ for $m = 0$.
- **Overflow of $un + v$.** The universe is $n^2$, which needs $2 \log_2 n$ bits. For $n > 2^{32}$ it does not fit in a 64-bit word.
- **Calling a structure succinct.** Succinct means $\mathrm{OPT} + o(\mathrm{OPT})$ bits. This structure is compact, $\mathrm{OPT} + O(m)$, which for sparse graphs is the same order but not the same constant.

## Implementations

The Python class `SuccinctGraph` builds the Elias-Fano encoding from a list of arcs and gives `access`, `rank`, `adjacent`, `degree`, `neighbor`, `neighbors` and `bits`. Its `BitVector` packs 64-bit words with a cumulative count per word.

## History

Jacobson introduced rank and select on bit vectors in 1989 and used them for trees and planar graphs in $O(n)$ bits; Turán had already shown in 1984 that planar graphs can be encoded in $O(n)$ bits without queries. Munro and Raman, and later many others, made these structures succinct in the strict sense. For general graphs, Farzan and Munro gave a representation within $(1 + \varepsilon)$ of $\log_2 \binom{n^2}{m}$ with constant-time queries. Navarro's book collects these results in its chapter on graphs.

## References
