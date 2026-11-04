---
tag: VSD7FB
kind: data-structure
slug: sparse-table
name: Sparse table
aliases:
- sparse table RMQ
area: data-structures/range-query-structures
level: core
summary: Precomputed table of power-of-two range aggregates giving O(1) queries for idempotent operations.
implements: [range-query-structure]
prereqs: [range-query-problem, idempotent-operation, asymptotic-notation]
see_also: [range-minimum-query, disjoint-sparse-table, sqrt-tree, segment-tree, fischer-heun-rmq, bender-farach-colton-rmq, range-gcd-query, binary-lifting]
sources:
  - paper: "Michael A. Bender and Martin Farach-Colton, The LCA problem revisited, LATIN 2000: Theoretical Informatics, Lecture Notes in Computer Science 1776, Springer, 2000"
    locator: the Sparse Table (ST) algorithm for RMQ, with O(n log n) preprocessing and O(1) query
  - url: https://cp-algorithms.com/data_structures/sparse-table.html
    title: cp-algorithms, Sparse Table
    locator: sections Precomputation, Range Sum Queries, Range Minimum Queries (RMQ), Similar data structures supporting more types of queries
  - url: https://cses.fi/book/book.pdf
    title: Antti Laaksonen, Competitive Programmer's Handbook
    locator: Section 9.1 (Static array queries), Minimum queries
  - paper: doi:10.1137/090779759
    title: "Johannes Fischer and Volker Heun, Space-Efficient Preprocessing Schemes for Range Minimum Queries on Static Arrays, SIAM Journal on Computing 40(2) (2011), 465-492"
    locator: the sparse table as the base of the block decomposition, and the O(n) and 2n + o(n) bit schemes
---

A sparse table is a static structure that stores, for each index $i$ and each $k$ with $i + 2^k \le n$, the aggregate $A[i] \oplus \cdots \oplus A[i + 2^k - 1]$ of the range of length $2^k$ that starts at $i$. It builds in $O(n \log n)$ time and space. For an [idempotent](/idempotent-operation/) operation such as min, max, gcd, bitwise and or bitwise or, it answers each [range query](/range-query-problem/) in $O(1)$ time with one application of $\oplus$, by covering the query range with two ranges of the same power-of-two length that may overlap. For any associative operation it answers in $O(\log n)$ time with disjoint ranges. It is the usual answer to the static [range minimum query](/range-minimum-query/) when $O(n \log n)$ memory is acceptable.

## In plain words

For each position of a list, write down the smallest item of the next 1 item, of the next 2 items, of the next 4 items, of the next 8 items, and so on, as long as the stretch stays inside the list. Each new row is quick to fill, because a stretch of 8 is two stretches of 4 that you already have.

To find the smallest item of any stretch, take the largest power of two that fits in it. Look up the stretch of that length that starts at the left end, and the one that ends at the right end. Together they cover the whole stretch, and they may overlap in the middle. For the smallest item, an overlap does no harm, since seeing an item twice does not change the smallest. So two lookups and one comparison give the answer.

## The abstract type

A sparse table implements the static part of the [range query structure](/range-query-structure/): `build(A)` and `query(l, r)`, with no updates. The fast query needs $(S, \oplus)$ to be a *band*: $\oplus$ is associative and idempotent, so $x \oplus x = x$ for each $x$. It does not need commutativity or an identity. For a general semigroup, such as $+$, the table still answers by a sum of disjoint parts in $O(\log n)$ time.

## Representation

Let $n \ge 1$ and $K = \lfloor \lg n \rfloor$. The table has a row $ST[k]$ for each $0 \le k \le K$, with the cells $ST[k][i]$ for $0 \le i \le n - 2^k$. A table $LG[1 \ldots n]$ holds $LG[m] = \lfloor \lg m \rfloor$.

**Invariant (T).** For each $0 \le k \le K$ and $0 \le i \le n - 2^k$: $ST[k][i] = A[i] \oplus A[i+1] \oplus \cdots \oplus A[i + 2^k - 1]$.

The table has $\sum_{k=0}^{K} (n - 2^k + 1) = (K + 1)(n + 1) - 2^{K+1} + 1$ cells, which is at most $n(K + 1)$ for $n \ge 2$. For $n = 8$ this is 21 cells, and for $n = 10^6$ it is 18951445 cells.

## Operations

```pseudo id=main
BUILD(A[0 .. n − 1])
L1  LG[1] ← 0; for m ← 2 to n do LG[m] ← LG[⌊m/2⌋] + 1
L2  for i ← 0 to n − 1 do ST[0][i] ← A[i]
L3  for k ← 1 to LG[n] do
L4      for i ← 0 to n − 2^k do
L5          ST[k][i] ← ST[k − 1][i] ⊕ ST[k − 1][i + 2^(k−1)]

QUERY(l, r)                                   ▷ 0 ≤ l ≤ r < n, ⊕ idempotent
L6  k ← LG[r − l + 1]
L7  return ST[k][l] ⊕ ST[k][r − 2^k + 1]

QUERY-ANY(l, r)                               ▷ 0 ≤ l ≤ r < n, ⊕ associative
L8  res ← e
L9  for k ← LG[n] downto 0 do
L10     if l + 2^k − 1 ≤ r then res ← res ⊕ ST[k][l]; l ← l + 2^k
L11 return res
```

**Build** (lines L1 to L5) first fills the table of floors of logarithms by the rule $\lfloor \lg m \rfloor = \lfloor \lg \lfloor m/2 \rfloor \rfloor + 1$ for $m \ge 2$. Row 0 is the array. Row $k$ comes from row $k - 1$: the range of length $2^k$ at $i$ is the range of length $2^{k-1}$ at $i$ followed by the one at $i + 2^{k-1}$. Build applies $\oplus$ once per cell of the rows 1 to $K$, so $\sum_{k=1}^{K} (n - 2^k + 1)$ times, which is $\Theta(n \log n)$.

**Query** (lines L6 and L7) takes $k = \lfloor \lg(r - l + 1) \rfloor$, so $2^k \le r - l + 1 < 2^{k+1}$. The range $[l, l + 2^k - 1]$ starts at $l$ and the range $[r - 2^k + 1, r]$ ends at $r$. Both lie inside $[l, r]$, and since $2 \cdot 2^k > r - l + 1$, they cover it. The cost is two table reads and one $\oplus$.

**Query-any** (lines L8 to L11) covers $[l, r]$ by disjoint ranges whose lengths are the powers of two in the binary form of $r - l + 1$, from the largest down, and combines them from left to right. It needs no idempotence. The $e$ of line L8 stands for an empty result: the code starts with the first part instead, so no identity is needed. The cost is $O(\log n)$.

## Example

Let $A = [5, 2, 8, 1, 9, 3, 7, 4]$ and $\oplus = \min$. Then $n = 8$, $K = 3$ and $LG[1 \ldots 8] = [0, 1, 1, 2, 2, 2, 2, 3]$.

| row | length | cells $ST[k][0], ST[k][1], \ldots$ |
|---|---|---|
| $k = 0$ | 1 | 5, 2, 8, 1, 9, 3, 7, 4 |
| $k = 1$ | 2 | 2, 2, 1, 1, 3, 3, 4 |
| $k = 2$ | 4 | 1, 1, 1, 1, 3 |
| $k = 3$ | 8 | 1 |

For example $ST[2][4] = \min(ST[1][4], ST[1][6]) = \min(3, 4) = 3$, the minimum of $A[4 \ldots 7] = 9, 3, 7, 4$.

| query | length | $k$ | the two cells | answer |
|---|---|---|---|---|
| $(2, 6)$ | 5 | 2 | $ST[2][2] = 1$ for $[2, 5]$, $ST[2][3] = 1$ for $[3, 6]$ | 1 |
| $(5, 7)$ | 3 | 1 | $ST[1][5] = 3$ for $[5, 6]$, $ST[1][6] = 4$ for $[6, 7]$ | 3 |
| $(4, 4)$ | 1 | 0 | $ST[0][4] = 9$ twice | 9 |

With $\oplus = +$ on the same array, the overlap is counted twice: the fast query of $(1, 6)$ gives $ST[2][1] + ST[2][3] = 20 + 20 = 40$, while the true sum is 30. QUERY-ANY splits the length 6 as $4 + 2$ and returns $ST[2][1] + ST[1][5] = 20 + 10 = 30$.

## Correctness

Build sets each cell from two cells of the row before it, whose ranges are adjacent and together make its range, so (T) holds by induction on $k$. For QUERY, let $a = r - 2^k + 1$ and $b = l + 2^k - 1$, so the two cells hold $\Pi(l, b)$ and $\Pi(a, r)$ with $l \le a \le b + 1 \le r + 1$. Split them at the overlap $[a, b]$: the product is $\Pi(l, a - 1) \oplus \Pi(a, b) \oplus \Pi(a, b) \oplus \Pi(b + 1, r)$, and idempotence turns the middle pair into one $\Pi(a, b)$. So the answer is $\Pi(l, r)$, and commutativity is not used. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time | applications of $\oplus$ |
|---|---|---|
| build | $\Theta(n \log n)$ | $(K+1)(n+1) - 2^{K+1} + 1 - n$, with $K = \lfloor \lg n \rfloor$ |
| query, idempotent $\oplus$ | $O(1)$ worst case | 1 |
| query-any, associative $\oplus$ | $O(\log n)$ worst case | at most $K$ |
| update | not supported; a change of $A[i]$ changes up to $2^k$ cells of row $k$, up to $2n - 1$ cells in all, so a repair costs $\Theta(n)$ in the worst case | |
| space | $(K + 1)(n + 1) - 2^{K+1} + 1$ cells, plus $n$ for $LG$ | |

The count of query-any is the number of 1 bits of $r - l + 1$ minus one, which is at most $K$. On the [word RAM](/word-ram/), $\lfloor \lg m \rfloor$ can also come from the position of the highest set bit of $m$ in $O(1)$ time, which removes the $LG$ table.

For range minimum, the space $O(n \log n)$ is not optimal. The [Bender-Farach-Colton](/bender-farach-colton-rmq/) and [Fischer-Heun](/fischer-heun-rmq/) schemes use a sparse table over blocks of $\Theta(\log n)$ items, which gives $O(n)$ preprocessing and $O(1)$ query.

## Variants

- **[Disjoint sparse table](/disjoint-sparse-table/).** For each level, store prefix and suffix aggregates inside blocks of size $2^k$ around their midpoints. Each query then uses two disjoint parts and one $\oplus$, for any associative operation, still in $O(n \log n)$ space.
- **Block decomposition.** Cut the array into blocks of $b$ items, build the sparse table on the $n / b$ block aggregates, and keep prefix and suffix aggregates in each block. With $b = \lceil \lg n \rceil$ the space is $O(n)$. A query inside one block needs its own method, which is where the RMQ schemes differ; see [range minimum query](/range-minimum-query/).
- **Two dimensions.** Store $ST[k][j][x][y]$ for the $2^k \times 2^j$ rectangles at $(x, y)$. A rectangle query with an idempotent operation reads four cells. The space is $O(nm \log n \log m)$.
- **[Binary lifting](/binary-lifting/).** The same doubling over the parent pointers of a tree gives the $2^k$-th ancestor of each node.
- **Memory layout.** Store the table as $ST[i][k]$ or as $ST[k][i]$. Row by row ($ST[k][i]$) makes the build loop read memory in order, which is faster in practice.

## When to use it

Use a sparse table for a static array with an idempotent operation and many queries: range minimum, maximum, gcd, and or, and the LCP queries of a [suffix array](/suffix-array/). It is short and its query is very fast. If memory is tight, use a [segment tree](/segment-tree/) ($O(\log n)$ query in $O(n)$ space) or a linear RMQ scheme. If the array changes, use a segment tree. For a static sum, use [prefix sums](/prefix-sums/), which need only $n + 1$ cells. For a static array and an operation that is associative but not idempotent, use a disjoint sparse table or a [sqrt tree](/sqrt-tree/).

## Pitfalls

- **A non-idempotent operation in the fast query.** For a sum, line L7 counts the overlap $[a, b]$ twice, as in the example where the answer 40 should be 30. Use QUERY-ANY, a disjoint sparse table or prefix sums.
- **The wrong second start.** The second cell of line L7 starts at $r - 2^k + 1$, not at $r - 2^k$ or at $l + 2^k$. With $l + 2^k$, the second range may run past $r$, or past the end of the row.
- **Floating-point logarithms.** Computing $k$ with a floating-point $\log_2$ can round up near a power of two: in double precision, $\log_2(2^{49} - 1)$ rounds to exactly 49.0, while $\lfloor \lg(2^{49} - 1) \rfloor = 48$. Use the table of line L1 or the bit length of the integer.
- **Rows that run past the end.** Row $k$ has only $n - 2^k + 1$ cells. A build loop that runs $i$ up to $n - 1$ in each row reads outside row $k - 1$.
- **Too much memory.** For $n = 10^6$ the table has about $1.9 \cdot 10^7$ cells. With 8-byte values this is about 150 MB, which can be too much. A block decomposition or a segment tree uses much less.

## Implementations

The Python class builds the table row by row with the $LG$ table of line L1. `query` is the $O(1)$ query of lines L6 and L7, and `query_any` is the disjoint query of lines L8 to L11, which starts from the first part instead of an identity.

## History

Bender and Farach-Colton presented the sparse table, under this name, in 2000, as the $O(n \log n)$ step of their simple linear-time solution of the range minimum and lowest common ancestor problems, which they offer as a simple alternative to the earlier optimal methods for these problems. Fischer and Heun used the sparse table over blocks in their space-optimal scheme of 2011.

## References
