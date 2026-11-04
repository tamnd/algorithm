---
tag: 5HH6N4
kind: data-structure
slug: disjoint-sparse-table
name: Disjoint sparse table
aliases:
- disjoint sparse table for associative operations
area: data-structures/range-query-structures
level: advanced
summary: O(n log n) table answering any associative range query in O(1) using divide and conquer.
implements: [range-query-structure]
model: word-ram
complexity:
  vars: {n: the length of the array; the time is per query, and the build takes O(n log n)}
  time: {worst: O(1)}
  space: {extra: Θ(n log n)}
prereqs: [sparse-table, monoid, bit-manipulation]
see_also: [idempotent-operation, segment-tree, sqrt-tree, range-minimum-query, prefix-sums, divide-and-conquer-paradigm, invertible-operation, matrix-exponentiation]
sources:
  - url: https://discuss.codechef.com/t/tutorial-disjoint-sparse-table/17404
    title: CodeChef Discuss, [Tutorial] Disjoint Sparse Table
    locator: the whole tutorial (the levels of blocks with products from the middle outward, and the level of a query from the highest set bit of x xor y)
  - url: https://cp-algorithms.com/data_structures/sparse-table.html
    title: cp-algorithms, Sparse Table
    locator: the last paragraph before Practice Problems (structures for any associative function, the Disjoint Sparse Table and the Sqrt Tree)
  - paper: doi:10.1145/800070.802185
    title: "Andrew C. Yao, Space-time tradeoff for answering range queries (extended abstract), Proceedings of the 14th Annual ACM Symposium on Theory of Computing (STOC 1982), 128-136"
    locator: the result on interval queries over a semigroup, with query time about the inverse Ackermann function of the space
---

A disjoint sparse table answers range queries $A[l] \cdot A[l+1] \cdots A[r]$ over any associative operation in $O(1)$ time with one operation, after $O(n \log n)$ preprocessing. It splits the array, padded to a power of two, into blocks of size $2^h$ on each level $h$, and stores for each position the product from that position to the middle of its block. Any query $[l, r]$ with $l \ne r$ crosses the middle of exactly one block, found from the highest set bit of $l \oplus r$, and its answer is the product of two stored values. Unlike the [sparse table](/sparse-table/), whose two ranges overlap, it needs neither an [idempotent](/idempotent-operation/) nor an [invertible](/invertible-operation/) operation, only a [monoid](/monoid/) or even a semigroup.

## In plain words

Think of a long ruler cut in half, then each half cut in half again, and so on. For every cut you write down running totals: going left from the cut, and going right from the cut, up to the end of the piece.

To answer "what is the total from mark $l$ to mark $r$?", find the first cut that falls between $l$ and $r$. Then the total is "from $l$ up to the cut" plus "from the cut up to $r$", and both are already written down. No piece is counted twice, so this works even for operations where counting twice would be wrong, such as sums or products of matrices.

## The abstract type

A static array $A[0 \ldots n-1]$ over a semigroup $(S, \cdot)$, that is, a set with an associative operation. The only operation after the build is

- $\textsc{query}(l, r)$ with $0 \le l \le r < n$: return $A[l] \cdot A[l+1] \cdots A[r]$, in this order.

No updates are supported. The operation need not be commutative: matrix products, string concatenation and composition of functions all work.

## Representation

Let $K = \lceil \lg n \rceil$ and $N = 2^K$; positions $n \ldots N - 1$ exist only as padding and are never read by a query. For each level $h = 1, \ldots, K$, the positions are cut into blocks $[b, b + 2^h)$ with $b$ a multiple of $2^h$, each with the middle $m = b + 2^{h-1}$. The table stores

$$ T[h][i] = \begin{cases} A[i] \cdot A[i+1] \cdots A[m - 1] & \text{if } b \le i < m, \\ A[m] \cdot A[m+1] \cdots A[i] & \text{if } m \le i < b + 2^h, \end{cases} $$

for $i < n$. Level 1 is the array itself, so the table often stores $A$ at level 0 and builds the levels from 2 on. The space is $n$ values per level, $n K$ in total.

The key fact is the **level of a query**: for $l < r$, let $h$ be the bit length of $l \oplus r$, that is, the position of its highest set bit plus one. Then $l$ and $r$ agree on all bits from $h$ upwards, so they lie in the same block of size $2^h$, and they differ in bit $h - 1$, so $l$ lies in the left half and $r$ in the right half. So $[l, r]$ contains the middle $m$ of that block, and $A[l \ldots r] = T[h][l] \cdot T[h][r]$.

## Operations

```pseudo id=main
QUERY(l, r)                                ▷ 0 ≤ l ≤ r < n
L1  if l = r then return A[l]
L2  h ← BITLENGTH(l xor r)                 ▷ one count-leading-zeros instruction
L3  return T[h][l] · T[h][r]
```

The build fills each level from the middles outward.

```pseudo id=build
BUILD(A, n)
L4  for h ← 1 to K do
L5      for b ← 0 to N − 1 step 2^h do
L6          m ← b + 2^(h−1)
L7          if m − 1 < n then T[h][m − 1] ← A[m − 1]
L8          for i ← m − 2 down to b do if i < n then T[h][i] ← A[i] · T[h][i + 1]
L9          if m < n then T[h][m] ← A[m]
L10         for i ← m + 1 to b + 2^h − 1 do if i < n then T[h][i] ← T[h][i − 1] · A[i]
```

The order of the factors matters: on the left half the new item goes on the left, and on the right half it goes on the right.

## Example

Take $A = [3, 1, 4, 1, 5, 9, 2, 6]$ with addition, so $n = N = 8$ and $K = 3$.

| level $h$ | blocks | $T[h][0 \ldots 7]$ |
|---|---|---|
| 1 | $[0,2), [2,4), [4,6), [6,8)$ | $3, 1, 4, 1, 5, 9, 2, 6$ |
| 2 | $[0,4), [4,8)$ | $4, 1, 4, 5, 14, 9, 2, 8$ |
| 3 | $[0,8)$ | $9, 6, 5, 1, 5, 14, 16, 22$ |

At level 2, the block $[4, 8)$ has the middle 6: $T[2][4] = A[4] + A[5] = 14$, $T[2][5] = 9$, $T[2][6] = 2$ and $T[2][7] = 2 + 6 = 8$.

- $\textsc{query}(2, 5)$: $2 \oplus 5 = 7$, bit length 3, so the answer is $T[3][2] + T[3][5] = 5 + 14 = 19 = 4 + 1 + 5 + 9$.
- $\textsc{query}(4, 7)$: $4 \oplus 7 = 3$, bit length 2, so $T[2][4] + T[2][7] = 14 + 8 = 22$.
- $\textsc{query}(1, 2)$: $1 \oplus 2 = 3$, so $T[2][1] + T[2][2] = 1 + 4 = 5$.
- $\textsc{query}(3, 3) = A[3] = 1$.

## Correctness

The build computes the definition of $T$ by induction from the middle outward: on the left half $T[h][i] = A[i] \cdot T[h][i+1]$, and on the right half $T[h][i] = T[h][i-1] \cdot A[i]$, which is the definition by associativity. For a query with $l < r$, the level fact above gives a block $[b, b + 2^h)$ with $b \le l < m \le r < b + 2^h$, so $T[h][l] = A[l] \cdots A[m-1]$ and $T[h][r] = A[m] \cdots A[r]$, and their product in this order is $A[l] \cdots A[r]$ by the split law of a semigroup. Positions at or above $n$ are never needed, because $r < n$. The [proof](proofs/correctness.md) gives the details.

## Complexity

A query is one comparison, one xor, one bit-length instruction, two table reads and one operation: $O(1)$ time on the word RAM, where the bit length of a word is one instruction (count leading zeros), or a table lookup. The build performs fewer than $n$ operations per level, so at most $n \lceil \lg n \rceil$ operations in total, and the table has $n \lceil \lg n \rceil$ entries, $\Theta(n \log n)$ space. Storing $A$ at level 0 and building from level 2 saves one level.

Compared with the [sparse table](/sparse-table/), the space and the build time are the same, and the query is one operation in both, but the disjoint table has no overlap and so allows any associative operation. Compared with a [segment tree](/segment-tree/), the query is $O(1)$ instead of $O(\log n)$, at the price of $\Theta(n \log n)$ space and no updates.

## Variants

- **Sqrt tree.** Levels with blocks of size $\sqrt{n}$, then $n^{1/4}$, and so on, give $O(n \log \log n)$ space and $O(1)$ queries, and allow updates in $O(\sqrt n)$; see the [sqrt tree](/sqrt-tree/).
- **More operations per query, less space.** Allowing $t$ operations per query reduces the space towards $O(n \lambda(t, n))$, where $\lambda(3, n) = O(\log \log n)$ and $\lambda(4, n) = O(\log^* n)$; this is the trade-off of Yao and of Alon and Schieber.
- **Blocks plus a table.** Cut the array into blocks of size $\lg n$, keep a disjoint sparse table over the block products, and prefix and suffix products inside each block. Queries that span a block boundary take $O(1)$; queries inside one block need a scan or a small table.
- **Two dimensions.** The same construction on both coordinates answers rectangle queries with three operations and $O(n m \log n \log m)$ space.

## When to use it

Use a disjoint sparse table for a static array with many queries over an associative operation that is neither idempotent nor invertible, such as products modulo a composite number, products of matrices, composition of linear functions, or concatenation of string hashes. For idempotent operations, the plain sparse table is simpler. For sums or xor, [prefix sums](/prefix-sums/) need only $n + 1$ values. If the array changes, use a segment tree.

## Pitfalls

- **The order of the factors.** For a non-commutative operation the left half must be built as $A[i] \cdot T[h][i+1]$ and the query must return $T[h][l] \cdot T[h][r]$, not the other order.
- **The case $l = r$.** Then $l \oplus r = 0$ and no level applies; return $A[l]$, or keep $A$ as level 0.
- **Padding.** Without padding to a power of two, blocks at the end are cut short. The table must still have the right middle for every block, which is easiest with $N = 2^K$ and with entries at positions $\ge n$ skipped.
- **The bit length of zero.** In C and C++, `__builtin_clz(0)` is undefined, which is one more reason to treat $l = r$ apart.
- **Memory.** For $n = 10^6$ and 8-byte values the table is about 160 MB. Trim it with blocks, or use a segment tree.

## Implementations

## History

The question of how many stored products a query needs, against how much space, was studied by Yao (1982) for interval queries over a semigroup, who found a trade-off through the inverse of Ackermann's function; Alon and Schieber (1987) gave matching constructions. Two stored values per query with $\Theta(n \log n)$ space is the first point of that trade-off. The name *disjoint sparse table* and the bit trick for the level come from competitive programming, where a 2017 CodeChef tutorial made the structure widely known.

## References
