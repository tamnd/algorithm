---
tag: WJ5KV3
kind: data-structure
slug: bitset-adjacency-matrix
name: Bitset adjacency matrix
aliases:
- bit matrix graph
area: graphs/graph-representation
level: core
summary: Adjacency matrix stored as one bit per entry, using word-parallel operations.
implements: [graph]
prereqs: [adjacency-matrix, bit-vector, bitwise-operations]
see_also: [adjacency-matrix, bit-set, bit-parallelism, population-count, triangle-counting, maximum-clique, transitive-closure, four-russians-method]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.1 (Representations of graphs), the remark that an unweighted adjacency matrix needs only one bit per entry
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.1.3 (Bitwise tricks and techniques), the extraction of the lowest set bit, sideways addition (population count) and the representation of sets by bits of words
  - paper: "Pablo San Segundo, Diego Rodriguez-Losada and Agustin Jimenez, An exact bit-parallel algorithm for the maximum clique problem, Computers and Operations Research 38(2), 2011"
    locator: pages 571 to 581, the bitset encoding of the adjacency matrix and the word-parallel set operations in branch and bound
---

A bitset adjacency matrix is an [adjacency matrix](/adjacency-matrix/) in which each row is a [bit vector](/bit-vector/) packed into machine words of $w$ bits, so the whole graph on $n$ vertices takes $n \lceil n/w \rceil$ words. It keeps the $O(1)$ [adjacency query](/adjacency-query/), edge insertion and edge deletion of the plain matrix, and it adds whole-row operations that run $w$ bits at a time: the neighbourhood of $u$ intersected with that of $v$, the degree by [population count](/population-count/), and the union of rows, each in $O(n/w)$ word operations. With $w = 64$ this is a 64-fold gain in space and often in time, and it is the base of fast exact algorithms for [maximum clique](/maximum-clique/), [triangle counting](/triangle-counting/) on dense graphs and [transitive closure](/transitive-closure/).

## In plain words

Take the table of the adjacency matrix, where each cell is a yes or a no. A yes or a no is one bit, and a computer word holds 64 bits. So pack each row of the table into words, 64 cells per word.

Now the table is 64 times smaller. Reading one cell still takes one step: find the word, then pick out the bit. The real gain is with whole rows. To find the common neighbours of two vertices, put their two rows side by side and combine them word by word with AND. One AND handles 64 vertices at once. Counting the 1s of a word is also a single instruction on most machines.

## The abstract type

The structure implements the [graph](/graph/) type over $V = \{0, \ldots, n-1\}$, with `adjacent`, `neighbors`, `add-edge`, `remove-edge`, `add-vertex`, `degree` and `edges`. It stores a [directed graph](/directed-graph/), with self-loops allowed, or a simple [undirected graph](/undirected-graph/). It does not store weights or parallel edges; for those, use a plain [adjacency matrix](/adjacency-matrix/) with numbers in the cells. It also offers the set operations of a [bit set](/bit-set/) on rows: `common(G, u, v)`, the number of vertices adjacent to both $u$ and $v$, and similar AND, OR and AND-NOT combinations.

## Representation

Fix the word size $w$ and let $W = \lceil n/w \rceil$. The structure has $n$, a flag that says whether the graph is directed, and $n$ rows $R[0], \ldots, R[n-1]$, each an array of $W$ words. Cell $(u, v)$ of the matrix is bit $v \bmod w$ of the word $R[u][\lfloor v/w \rfloor]$, where bit 0 is the least significant bit. So the row of $u$ is the set $N^+(u)$ of the out-neighbours of $u$, encoded as a bit vector of length $n$.

**Invariant (B).**

- (B1) The *padding bits*, the bits of the last word of each row at positions $v \ge n$, are 0.
- (B2) If the graph is undirected, bit $v$ of row $u$ equals bit $u$ of row $v$, and bit $u$ of row $u$ is 0.

Rule (B1) matters because whole-row operations, such as the degree by population count, also count the padding bits. The space is $nW = n \lceil n/w \rceil$ words, which is $n^2/w + O(n)$, or $n^2$ bits plus at most $n(w - 1)$ padding bits.

## Operations

```pseudo id=main
NEW(n, directed)
L1  R[u] ← an array of W = ⌈n/w⌉ zero words, for each u

ADD-EDGE(G, u, v)                       ▷ for an undirected graph, u ≠ v
L2  R[u][⌊v/w⌋] ← R[u][⌊v/w⌋] OR 2^(v mod w)
L3  if not directed then R[v][⌊u/w⌋] ← R[v][⌊u/w⌋] OR 2^(u mod w)

REMOVE-EDGE(G, u, v)
L4  R[u][⌊v/w⌋] ← R[u][⌊v/w⌋] AND NOT 2^(v mod w)
L5  if not directed then R[v][⌊u/w⌋] ← R[v][⌊u/w⌋] AND NOT 2^(u mod w)

ADJACENT(G, u, v)
L6  return (R[u][⌊v/w⌋] shifted right by v mod w) AND 1 = 1

NEIGHBORS(G, u)                         ▷ in increasing order
L7  for j ← 0 to W − 1 do
L8      x ← R[u][j]
L9      while x ≠ 0 do
L10         output j·w + (the index of the lowest set bit of x)
L11         x ← x AND (x − 1)

DEGREE(G, u)
L12 return the sum over j of POPCOUNT(R[u][j])

COMMON(G, u, v)                         ▷ |N(u) ∩ N(v)|
L13 return the sum over j of POPCOUNT(R[u][j] AND R[v][j])

ADD-VERTEX(G)
L14 if n mod w = 0 then append a zero word to each row
L15 append a row of ⌈(n + 1)/w⌉ zero words; n ← n + 1; return n − 1
```

**Add-edge, remove-edge and adjacent** (lines L2 to L6) each touch one word, or two for an undirected graph, with a shift, an OR, an AND or a NOT. They take $O(1)$ time, as on the plain matrix. When $w$ is a power of two, $\lfloor v/w \rfloor$ and $v \bmod w$ are a shift and a mask.

**Neighbors** (lines L7 to L11) reads the $W$ words of the row, and inside each word it jumps from one set bit to the next: line L10 finds the [lowest set bit](/lowest-set-bit/) with a [trailing zero count](/trailing-zero-count/) instruction, and line L11 clears it. So it takes $O(W + d(u)) = O(n/w + d(u))$ time, against $\Theta(n)$ for the plain matrix. Zero words cost one test each.

**Degree and common** (lines L12 and L13) take $O(n/w)$ time with a [population count](/population-count/) instruction. COMMON gives the number of common neighbours, which is the number of triangles through the edge $\{u, v\}$ when $u$ and $v$ are adjacent. The same loop with OR, AND-NOT or a stored result row computes the union, the difference and the new row of a set operation, also in $O(n/w)$ time.

**Add-vertex** (lines L14 and L15) adds a zero row of $\lceil (n+1)/w \rceil$ words, and once in each $w$ additions, when $n$ reaches a multiple of $w$, one more word in each row. With rows kept as [dynamic arrays](/dynamic-array/), this costs $O(n)$ amortized time per row extension, so $O(n/w + 1)$ amortized per new vertex. If all rows live in one block of memory, each extension copies the block, in $\Theta(n^2/w)$ time.

## Example

Take $w = 4$, so that the words are short enough to show, and the undirected graph on $\{0, \ldots, 5\}$ with the edges $01, 02, 12, 13, 23, 34, 45$. Then $W = \lceil 6/4 \rceil = 2$ words per row. Words are written with bit 0 on the right, and the bits at positions 6 and 7 of the second word are padding.

| $u$ | $R[u][0]$, vertices 3 2 1 0 | $R[u][1]$, padding, padding, 5 4 | neighbours |
|---|---|---|---|
| 0 | 0110 | 0000 | 1, 2 |
| 1 | 1101 | 0000 | 0, 2, 3 |
| 2 | 1011 | 0000 | 0, 1, 3 |
| 3 | 0110 | 0001 | 1, 2, 4 |
| 4 | 1000 | 0010 | 3, 5 |
| 5 | 0000 | 0001 | 4 |

Now run these operations.

1. ADJACENT$(1, 3)$: word $R[1][0] = 1101$, shifted right by $3$, is $0001$, so the answer is yes.
2. NEIGHBORS$(3)$: word 0 is $0110$; the lowest set bit is bit 1, so output 1, and $0110 \text{ AND } 0101 = 0100$; then output 2, and the word becomes 0. Word 1 is $0001$, so output $4 + 0 = 4$. The output is $1, 2, 4$, after 2 word reads and 3 bit extractions.
3. DEGREE$(1)$: $\mathrm{popcount}(1101) + \mathrm{popcount}(0000) = 3$.
4. COMMON$(1, 2)$: $1101 \text{ AND } 1011 = 1001$, so the common neighbours are 0 and 3, and the count is 2. Since 1 and 2 are adjacent, the edge $\{1, 2\}$ is in the 2 triangles $\{0, 1, 2\}$ and $\{1, 2, 3\}$.
5. REMOVE-EDGE$(2, 3)$: $R[2][0]$ becomes $1011 \text{ AND } 0111 = 0011$, and $R[3][0]$ becomes $0110 \text{ AND } 1011 = 0010$.
6. ADD-VERTEX: $n = 6$ is not a multiple of 4, so the rows keep 2 words, and the new zero row $R[6]$ gets $\lceil 7/4 \rceil = 2$ words. It returns 6.

Summed over the 7 edges, COMMON gives $6 = 3 \times 2$ before step 5, because each of the 2 triangles is counted once for each of its 3 edges.

## Correctness

The structure stores the same bits as the plain [adjacency matrix](/adjacency-matrix/), with cell $(u, v)$ at a fixed bit of a fixed word, so the arguments of that page carry over to lines L2 to L6. The new points are the word operations. OR with $2^{v \bmod w}$ sets exactly bit $v \bmod w$, AND with its complement clears exactly that bit, and neither touches a padding bit, since $v < n$. In lines L9 to L11, $x \text{ AND } (x - 1)$ clears exactly the lowest set bit of $x \neq 0$, so the loop outputs each set bit of the word once, in increasing order, and stops after as many steps as there are set bits. By (B1), the population counts in lines L12 and L13 count only real vertices. Line L14 adds words of zeros, and line L15 a row of zeros, which keeps (B1) and (B2). The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

Times are in word operations on a [word RAM](/word-ram/) with $w$-bit words, $w \ge \log_2 n$, with POPCOUNT and the lowest set bit in $O(1)$ time.

| operation | time | plain matrix |
|---|---|---|
| new graph | $\Theta(n^2/w + n)$ | $\Theta(n^2)$ |
| adjacent, add-edge, remove-edge | $O(1)$ | $O(1)$ |
| neighbors$(u)$ | $O(n/w + d(u))$ | $\Theta(n)$ |
| degree$(u)$ | $O(n/w)$ | $\Theta(n)$ |
| common, union or difference of two rows | $O(n/w)$ | $\Theta(n)$ |
| add-vertex | $O(n/w + 1)$ amortized with dynamic rows | $\Theta(n^2)$ |
| complement | $\Theta(n^2/w)$ | $\Theta(n^2)$ |
| space | $n \lceil n/w \rceil$ words | $n^2$ cells |

**Whole-graph algorithms.** [BFS](/breadth-first-search/) on the bitset matrix takes $O(n^2/w + m)$ time: scanning each row with NEIGHBORS costs $O(n/w + d(u))$, and summing over all $u$ gives the bound. A bit-parallel BFS that keeps the unvisited set as a bitset and ANDs it with each row also takes $O(n^2/w)$. Counting the triangles of a graph by COMMON over all edges takes $O(mn/w)$ time. The [transitive closure](/transitive-closure/) by Warshall's method, which ORs row $k$ into each row $i$ with bit $k$ set, takes $O(n^3/w)$ time; the [four Russians method](/four-russians-method/) speeds up Boolean matrix products by a further $\log n$ factor.

## Variants

- **One bit vector for the whole matrix.** Store all $n^2$ bits in one array, row after row, without padding between rows. This saves up to $n(w-1)$ bits but makes row operations shift across word borders.
- **Triangular bits.** For an undirected graph, store only the $\binom{n}{2}$ bits above the diagonal. Then a row is no longer contiguous, which loses the word-parallel row operations.
- **SIMD rows.** With vector registers of 256 or 512 bits, the loops of lines L12 and L13 process several words per instruction.
- **Sparse rows.** When rows have long runs of zero words, a compressed bitmap such as a [roaring bitmap](/roaring-bitmap/) per row saves space and skips the zero words.
- **[Bitboards](/bitboard/).** Board games on $8 \times 8$ boards store the attack graph of each piece as 64-bit rows, one word per row.
- **Bipartite form.** For a [bipartite graph](/bipartite-graph/) with parts of sizes $p$ and $q$, store the $p \times q$ biadjacency matrix as $p$ rows of $\lceil q/w \rceil$ words.

## When to use it

Use a bitset adjacency matrix for a dense unweighted graph, or for a graph with up to a few tens of thousands of vertices on which the algorithm works with sets of neighbours: clique search, coloring heuristics such as [DSatur](/dsatur/), triangle counting, dominating sets, and closure computations. With $n = 10^4$ the matrix takes $10^8$ bits, which is 12.5 MB, small enough to keep in memory, while a plain matrix of bytes would take 100 MB. For a sparse graph with $n$ in the millions, $n^2/8$ bytes is too much, and an [adjacency list](/adjacency-list/) or a [compressed sparse row](/compressed-sparse-row/) array is the right choice.

## Pitfalls

- **Padding bits.** A complement row computed as NOT of each word sets the padding bits to 1, and then POPCOUNT counts vertices that do not exist. Mask the last word with $2^{n \bmod w} - 1$ after each NOT, when $n \bmod w \ne 0$.
- **The diagonal after a complement.** The complement of an undirected graph must also clear bit $u$ of row $u$, or each vertex becomes its own neighbour.
- **Shift widths.** In C and similar languages, shifting a 64-bit word by 64 or more bits is undefined. Compute $2^{v \bmod w}$ as `1 << (v % 64)` on an unsigned 64-bit one, not as a 32-bit `1 << v`.
- **Bit order.** The code and the drawings must agree on whether bit 0 is the least or most significant bit of a word. The lowest set bit trick of line L11 assumes bit 0 is the least significant.
- **Sparse graphs.** The $O(n/w)$ terms do not depend on $m$. For a sparse graph with large $n$, NEIGHBORS is still dominated by the $n/w$ zero words, and a list is faster.

## Implementations

The Python class keeps each row as a list of $W$ integers of $w$ bits, with $w$ a parameter that defaults to 64, so that the tests can use $w = 4$ as in the example. It uses `int.bit_count` for POPCOUNT and `(x & -x).bit_length() - 1` for the lowest set bit, and it follows the main block line by line. `check_invariant` tests (B1) and (B2).

## History

Packing the rows of a Boolean matrix into words is as old as binary computers; Knuth (Section 7.1.3) collects the word tricks used here, such as $x \text{ AND } (x - 1)$ and sideways addition. The bit-parallel speed-up of Boolean matrix products and transitive closure goes back to the method of Arlazarov, Dinic, Kronrod and Faradzev in 1970, the four Russians method. In exact search, the bitset matrix became the standard representation for maximum clique algorithms after the bit-parallel algorithm of San Segundo, Rodriguez-Losada and Jimenez in 2011.

## References
