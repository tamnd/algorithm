---
tag: RBM9RY
kind: data-structure
slug: sqrt-tree
name: Sqrt tree
aliases:
- two-level sqrt structure
area: data-structures/range-query-structures
level: research
summary: Static structure answering associative range queries in O(1) with O(n log log n) space.
implements: [range-query-structure]
prereqs: [square-root-decomposition, sparse-table, associative-operator]
see_also: [disjoint-sparse-table, sparse-table, segment-tree, range-minimum-query, range-query-structure, square-root-decomposition, monoid, fischer-heun-rmq]
sources:
  - url: https://cp-algorithms.com/data_structures/sqrt-tree.html
    title: cp-algorithms, Sqrt Tree
    locator: sections Building sqrt decomposition, Building a tree, Optimizing the query, the layers with block size about the square root of the segment and the choice of layer from the highest bit of l xor r
  - paper: "Andrew C. Yao, Space-time tradeoff for answering range queries (extended abstract), Proceedings of the 14th Annual ACM Symposium on Theory of Computing (STOC 1982), 128-136"
    locator: the trade-off between the number of stored products and the number of combines per query for static semigroup range queries
  - paper: "Noga Alon and Baruch Schieber, Optimal preprocessing for answering on-line product queries, Technical Report 71/87, Tel Aviv University, 1987"
    locator: the bound of O(n log log n) stored products for queries with a constant number of combines, and the inverse Ackermann trade-off
---

A sqrt tree is a static structure for range products $A[l] \oplus \cdots \oplus A[r]$ under any [associative](/associative-operator/) operation $\oplus$. It answers each query with at most two applications of $\oplus$, after $O(n \log \log n)$ preprocessing time and space. It applies [square-root decomposition](/square-root-decomposition/) recursively: a segment of $2^k$ items is cut into blocks of about $2^{k/2}$ items, with prefix products, suffix products and a table of the products of all runs of whole blocks, and each block is again a segment of the next layer. The highest bit in which $l$ and $r$ differ names the one layer that answers the query.

## In plain words

You have a fixed list and a way to combine two items that may care about the order, such as gluing two strings together. You want to combine a whole stretch of the list, many times, in very few steps.

Cut the list into blocks. For each block, write down the combined value of every start piece and every end piece of the block. For each run of whole blocks, write down its combined value too. A stretch that crosses some block borders is then an end piece of one block, a run of whole blocks and a start piece of another block: three stored values and two steps.

A stretch that lies inside one block needs the same trick inside that block, with smaller blocks. A few layers of this are enough, because the size of the blocks shrinks to its square root at each layer.

## The abstract type

The structure implements a static [range query structure](/range-query-structure/): it is built from an array $A[0 \ldots n-1]$ over a semigroup $(S, \oplus)$ and then answers $\mathrm{query}(l, r) = A[l] \oplus \cdots \oplus A[r]$ for $0 \le l \le r \le n - 1$. It uses neither an identity, nor an inverse, nor commutativity, nor idempotence. The cost measure is the number of applications of $\oplus$ per query, besides $O(1)$ word operations.

## Representation

Let $K = \lceil \lg n \rceil$, so that the indices fit in $K$ bits. The layers are numbered $j = 0, 1, \ldots$ with the exponents

$$k_0 = K, \qquad b_j = \lceil k_j / 2 \rceil, \qquad k_{j+1} = b_j,$$

and the list stops before the first $k_j < 2$. In layer $j$, a *segment* is a range of indices $[s 2^{k_j}, (s + 1) 2^{k_j} - 1]$, and it is cut into $m_j = 2^{k_j - b_j}$ *blocks* of $2^{b_j}$ indices, the blocks $[p 2^{b_j}, (p + 1) 2^{b_j} - 1]$. Every range is clipped to $[0, n - 1]$. Layer $j$ stores three tables:

- $\mathit{PRE}_j[i]$, the product from the start of the block of $i$ to $i$;
- $\mathit{SUF}_j[i]$, the product from $i$ to the end of its block;
- $\mathit{BTW}_j[p, q]$, for blocks $p \le q$ of the same segment, the product of the blocks $p$ to $q$.

A table $\mathit{LAYER}[h]$ gives, for each bit position $1 \le h < K$, the layer $j$ with $b_j \le h < k_j$. The intervals $[b_j, k_j)$ are disjoint and their union is $[1, K)$, because $k_{j+1} = b_j$ and the last layer has $k_j = 2$, so $b_j = 1$ for it: a layer with $k_j = 3$ has $b_j = 2$ and is followed by a layer with $k = 2$. Bit position 0 needs no layer.

## Operations

```pseudo id=main
BUILD(A[0 .. n − 1])
L1  K ← ⌈lg n⌉; the layers j with k_0 = K, b_j = ⌈k_j / 2⌉, k_{j+1} = b_j, while k_j ≥ 2
L2  for each layer j and each h with b_j ≤ h < k_j do LAYER[h] ← j
    for each layer j and each block [s, e] of 2^{b_j} indices, clipped to n:
L3      PRE_j[s] ← A[s]; for i ← s + 1 to e do PRE_j[i] ← PRE_j[i − 1] ⊕ A[i]
L4      SUF_j[e] ← A[e]; for i ← e − 1 downto s do SUF_j[i] ← A[i] ⊕ SUF_j[i + 1]
    for each layer j, each segment, and each block p of the segment:
L5      acc ← SUF_j[p · 2^{b_j}]; BTW_j[p, p] ← acc       ▷ the product of block p
L6      for each later block q of the same segment do acc ← acc ⊕ SUF_j[q · 2^{b_j}]; BTW_j[p, q] ← acc

QUERY(l, r)                                               ▷ 0 ≤ l ≤ r ≤ n − 1
L7  if l = r then return A[l]
L8  h ← the highest bit of l xor r; if h = 0 then return A[l] ⊕ A[r]
L9  j ← LAYER[h]; p ← ⌊l / 2^{b_j}⌋; q ← ⌊r / 2^{b_j}⌋
L10 if q = p + 1 then return SUF_j[l] ⊕ PRE_j[r]
L11 return SUF_j[l] ⊕ BTW_j[p + 1, q − 1] ⊕ PRE_j[r]
```

**Choosing the layer** (lines L8 and L9). The indices $l$ and $r$ agree on all bits above $h$ and differ at bit $h$. So they lie in one aligned range of $2^{h+1}$ indices, which lies in one segment of layer $j$ since $h + 1 \le k_j$, and they lie in different blocks of it, since $h \ge b_j$. The query is then the end of the block of $l$, the whole blocks between, if any, and the start of the block of $r$.

**Two adjacent indices** (line L8). When $h = 0$, $r = l + 1$, and the answer is one application of $\oplus$ on the array itself.

## Example

Let $n = 16$, $\oplus = +$ and

$$A = [5, 2, 8, 1, 9, 3, 7, 4, 6, 0, 2, 5, 1, 8, 3, 7].$$

Then $K = 4$. Layer 0 has $k_0 = 4$ and $b_0 = 2$: one segment, the whole array, with 4 blocks of 4 items, whose sums are 16, 23, 13 and 19. Layer 1 has $k_1 = 2$ and $b_1 = 1$: segments of 4 items with 2 blocks of 2. So $\mathit{LAYER}[2] = \mathit{LAYER}[3] = 0$ and $\mathit{LAYER}[1] = 1$.

| query | $l \oplus r$ in bits | $h$ | layer | blocks $p, q$ | parts | answer |
|---|---|---|---|---|---|---|
| $(1, 14)$ | 1111 | 3 | 0 | 0, 3 | $\mathit{SUF}_0[1] = 11$, $\mathit{BTW}_0[1, 2] = 36$, $\mathit{PRE}_0[14] = 12$ | 59 |
| $(2, 7)$ | 0101 | 2 | 0 | 0, 1 | $\mathit{SUF}_0[2] = 9$, $\mathit{PRE}_0[7] = 23$ | 32 |
| $(5, 6)$ | 0011 | 1 | 1 | 2, 3 | $\mathit{SUF}_1[5] = 3$, $\mathit{PRE}_1[6] = 7$ | 10 |
| $(8, 9)$ | 0001 | 0 | none | none | $A[8] + A[9]$ | 6 |

The query $(1, 14)$ is the sum of all 16 items, 71, less $A[0] = 5$ and $A[15] = 7$, which is 59. The sum is not idempotent, and no item is counted twice.

## Correctness

The build fills each table by a left-to-right or right-to-left fold, so each entry is the product it names, by associativity. In a query, the choice of the layer puts $l$ and $r$ in different blocks of one segment, as shown above, so the ranges of $\mathit{SUF}_j[l]$, of $\mathit{BTW}_j[p + 1, q - 1]$ when $q > p + 1$, and of $\mathit{PRE}_j[r]$ are consecutive and cover $[l, r]$ exactly, in order. By associativity their product is the answer. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

**Query.** At most two applications of $\oplus$, and $O(1)$ word operations: one xor, one highest-bit operation, two shifts and the table reads. The highest bit is one machine instruction on most processors, or a lookup in a table of $2^K$ entries.

**Space and build time of one layer.** The tables $\mathit{PRE}_j$ and $\mathit{SUF}_j$ have $n$ entries each and take $n - 1$ applications of $\oplus$ each at most. A segment has $m_j = 2^{k_j - b_j}$ blocks, so $\mathit{BTW}_j$ has $m_j (m_j + 1)/2 \le m_j^2 = 2^{2(k_j - b_j)} \le 2^{k_j}$ entries per segment, because $2 b_j \ge k_j$. There are $\lceil n / 2^{k_j} \rceil$ segments, so $\mathit{BTW}_j$ has fewer than $n + 2^{k_j} \le n + 2^K < 3n$ entries, each made by one application of $\oplus$.

**Number of layers.** The exponent goes from $k_j$ to $\lceil k_j / 2 \rceil$, so after $t$ layers it is at most $K / 2^t + 1$ and drops below 2 after at most $\lceil \lg K \rceil + 1$ layers. So there are $O(\log \log n)$ layers, and the build takes $O(n \log \log n)$ time and space.

| operation | time | space |
|---|---|---|
| build | $O(n \log \log n)$ | $O(n \log \log n)$ |
| query | 2 applications of $\oplus$, $O(1)$ | |

**Optimality.** Yao and then Alon and Schieber studied this question for static semigroups, where the structure may store only products of ranges and a query may only combine stored products. With a constant number of combines per query, $\Theta(n \log \log n)$ stored products are needed and enough when the constant is 2, so the sqrt tree is optimal in that model up to a constant factor. With one combine, the [disjoint sparse table](/disjoint-sparse-table/) with $O(n \log n)$ products is the matching structure.

## Variants

- **Point updates.** Rebuild the parts of each layer that hold the changed item: one block of $\mathit{PRE}_j$ and $\mathit{SUF}_j$ and the $\mathit{BTW}_j$ of one segment. The top layer then costs $O(\sqrt n)$, and the lower layers cost less, so an update takes $O(\sqrt n)$ time.
- **Lazy range updates.** cp-algorithms describes range assignment with lazy tags on the blocks of the top layer, at $O(\sqrt n \log \log n)$ per update.
- **Disjoint sparse table.** Use blocks of size 2 at every level, that is, a layer for each bit; then one combine is enough, and the space is $O(n \log n)$.
- **The cp-algorithms form.** It builds the layers as a tree of explicit nodes with an extra index array to make the between tables smaller; the bounds are the same.
- **A combine count of 3.** Answering in three combines needs only $O(n \log^* n)$ stored products, by the results of Alon and Schieber, at the cost of a more complex scheme.

## When to use it

Use it when the array is static, the operation is associative but not idempotent, such as the sum modulo a number, string or matrix products, or the composition of functions, and the queries are many and must cost $O(1)$ combines. For an idempotent operation, a [sparse table](/sparse-table/) is simpler. For sums with an inverse, [prefix sums](/prefix-sums/) need only one subtraction. For an array with frequent updates, a [segment tree](/segment-tree/) is better.

## Pitfalls

- **The order of the combines.** For a non-commutative $\oplus$, line L11 must combine the suffix, the between part and the prefix in this order, and line L4 must build suffixes as $A[i] \oplus \mathit{SUF}_j[i + 1]$, not the other way.
- **Clipping to $n$.** When $n$ is not a power of two, the last block and the last segment are short. The tables must stop at $n - 1$, and the between table must have no entry for a block that does not exist.
- **The case $h = 0$.** With $r = l + 1$, no layer has blocks of one item, so the query must handle this case directly, as in line L8.
- **Layers chosen by the length.** The length $r - l + 1$ does not decide the layer: a range of length 2 may cross a block border of the top layer. The bit test on $l$ xor $r$ is what puts $l$ and $r$ in one segment.

## Implementations

The Python class `SqrtTree` follows the main block, with the layers in lists and the between tables in dictionaries keyed by the pair of block numbers. The tests count the applications of $\oplus$ in each query and compare queries with direct folds for sums, minimums, gcds and string concatenation, which is not commutative. The `check_invariant` method checks the layer plan and every stored product.

## History

The sqrt tree is a structure of the competitive programming community and is described on cp-algorithms. Its layers with blocks of about the square root of the segment are a practical form of the schemes of Yao and of Alon and Schieber, who found the trade-off between stored products and combines per query for static semigroups in the 1980s.

## References
