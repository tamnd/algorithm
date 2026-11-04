---
tag: K5P9KD
kind: data-structure
slug: wavelet-tree
name: Wavelet tree
aliases:
- Grossi-Gupta-Vitter wavelet tree
- wavelet tree over an alphabet
area: data-structures/succinct-structures
level: advanced
summary: A balanced binary tree over the alphabet with a bit vector per node, giving access, rank and select on sequences in compressed space.
model: word-ram
complexity:
  vars: {n: the length of the sequence, σ: the alphabet size}
  time: {access: O(log σ), rank: O(log σ), select: O(log σ), quantile: O(log σ), build: O(n log σ)}
  space: {total: "n log σ + o(n log σ) + O(σ log n)"}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 2003
  people: [Roberto Grossi, Ankur Gupta, Jeffrey Scott Vitter]
  note: Grossi, Gupta and Vitter introduced the wavelet tree at SODA 2003 as a part of a text index in high-order entropy space.
prereqs: [static-sequence, rank-select-dictionary]
see_also: [wavelet-matrix, fm-index, range-kth-smallest-query, rrr-bitvector, compressed-data-structure, document-listing, huffman-coding, burrows-wheeler-transform]
sources:
  - paper: Roberto Grossi, Ankur Gupta and Jeffrey Scott Vitter, High-order entropy-compressed text indexes, Fourteenth Annual ACM-SIAM Symposium on Discrete Algorithms (SODA 2003), 841-850
    locator: the wavelet tree, a balanced tree over the alphabet with a bit vector at each node, and its use for rank on the Burrows-Wheeler transform
  - paper: doi:10.1016/j.jda.2013.07.004
    title: Gonzalo Navarro, Wavelet trees for all, Journal of Discrete Algorithms 25, 2014, 2-20
    locator: Sections 2 and 3 (the structure, access, rank and select, and the view as a grid of points with range quantile and counting)
  - book: isbn:9781107152380
    title: Gonzalo Navarro, Compact Data Structures, A Practical Approach, Cambridge University Press, 2016
    locator: Chapter 6, Section 6.2 (Wavelet Trees), and Section 6.4.4 (Range Quantile Queries)
---

A wavelet tree stores a static sequence $S[0 \ldots n-1]$ over an alphabet of $\sigma$ symbols as a balanced binary tree over the alphabet, with a bit vector at each node, in $n \lceil \lg \sigma \rceil + o(n \lg \sigma) + O(\sigma \lg n)$ bits. The root splits the alphabet into a lower and an upper half and marks each position of $S$ with 0 or 1 by the half its symbol falls in; each child does the same for the subsequence of its half. With [rank and select](/rank-select-dictionary/) on the bit vectors, it answers access, rank and select of the [static sequence](/static-sequence/) type in $O(\lg \sigma)$ time, and range queries such as the $k$-th smallest symbol of a range in the same time. Grossi, Gupta and Vitter introduced it in 2003. It is the main component of the [FM-index](/fm-index/), and with [RRR](/rrr-bitvector/) bit vectors its space becomes $n H_0(S) + o(n \lg \sigma)$.

## In plain words

Take a string of letters from a to z. Write a 0 under each letter from the first half of the alphabet and a 1 under each letter from the second half. That row of bits is the top of the tree.

Then take only the letters marked 0, keep their order, and do the same with the first half of the alphabet split again; do the same with the letters marked 1. Keep splitting until each part has a single letter.

To read the letter at some place, read its bit at the top, then use a count of bits to find where that letter went in the next row down, and keep going. Each step down halves the possible letters, so after about five steps for 26 letters, only one is left.

## The abstract type

The structure stores a static string $S$ over $\Sigma = \{0, \ldots, \sigma - 1\}$ and answers the queries of the [static sequence](/static-sequence/) type: `access(i)`, `rank(c, i)`, the number of $c$ in $S[0 \ldots i-1]$, and `select(c, j)`, the position of the $j$-th $c$, for $j \ge 1$. It also answers `quantile(l, r, k)`, the $k$-th smallest symbol of $S[l \ldots r-1]$ for $1 \le k \le r - l$, which is the [range k-th smallest query](/range-kth-smallest-query/).

## Representation

Each node $v$ covers a range of symbols $[a_v, b_v)$; the root covers $[0, \sigma)$. A node with $b_v - a_v = 1$ is a leaf. An inner node has the midpoint $m_v = \lfloor (a_v + b_v)/2 \rfloor$, a left child covering $[a_v, m_v)$ and a right child covering $[m_v, b_v)$.

Let $S_v$ be the subsequence of $S$ of the symbols in $[a_v, b_v)$, in their order in $S$; $S_{\text{root}} = S$. An inner node stores the bit vector $B_v$ of length $|S_v|$ with $B_v[i] = 1$ if $S_v[i] \ge m_v$ and 0 otherwise, with a rank and select index. The sequences $S_v$ are not stored. The tree has $\sigma - 1$ inner nodes and height $\lceil \lg \sigma \rceil$, and each level holds at most $n$ bits. The invariant is that $B_v$ is as defined for each $v$; the structure is static.

## Operations

```pseudo id=main
ACCESS(i)                                    ▷ 0 ≤ i < n
L1  v ← root, a ← 0, b ← σ
L2  while b − a > 1 do
L3      m ← ⌊(a + b) / 2⌋
L4      if B_v[i] = 0 then i ← RANK0_v(i), v ← left(v), b ← m
L5      else i ← RANK1_v(i), v ← right(v), a ← m
L6  return a

RANK(c, i)                                   ▷ 0 ≤ i ≤ n
L7  v ← root, a ← 0, b ← σ
L8  while b − a > 1 do
L9      m ← ⌊(a + b) / 2⌋
L10     if c < m then i ← RANK0_v(i), v ← left(v), b ← m
L11     else i ← RANK1_v(i), v ← right(v), a ← m
L12 return i

SELECT(v, a, b, c, j)                        ▷ called as SELECT(root, 0, σ, c, j), 1 ≤ j ≤ n_c
L13 if b − a = 1 then return j − 1                 ▷ the position in the leaf
L14 m ← ⌊(a + b) / 2⌋
L15 if c < m then return SELECT0_v(SELECT(left(v), a, m, c, j) + 1)
L16 else return SELECT1_v(SELECT(right(v), m, b, c, j) + 1)

QUANTILE(l, r, k)                            ▷ the k-th smallest of S[l .. r − 1], 1 ≤ k ≤ r − l
L17 v ← root, a ← 0, b ← σ
L18 while b − a > 1 do
L19     m ← ⌊(a + b) / 2⌋, z ← RANK0_v(r) − RANK0_v(l)
L20     if k ≤ z then l ← RANK0_v(l), r ← RANK0_v(r), v ← left(v), b ← m
L21     else k ← k − z, l ← RANK1_v(l), r ← RANK1_v(r), v ← right(v), a ← m
L22 return a
```

**Moving down.** The key fact is the mapping between a node and its children: if $S_v[i]$ goes to the left child, its position there is $\text{rank}_0(B_v, i)$, the number of 0s before it in $B_v$; if it goes to the right, its position is $\text{rank}_1(B_v, i)$. Lines L4 and L5 apply this to follow one position down. Lines L10 and L11 apply it to a prefix length: the prefix $S_v[0 \ldots i-1]$ maps to a prefix of the child that holds the symbols of that prefix in the child's half.

**Moving up.** Select goes the other way. In a leaf all symbols are equal to $c$, so the $j$-th $c$ is at position $j - 1$. Position $p$ of the left child of $v$ is the $(p+1)$-th 0 of $B_v$, so line L15 maps it up with $\text{select}_0$; line L16 does the same with $\text{select}_1$.

**Quantile.** At each node, $z$ is the number of symbols of the current range that go to the left half. If the $k$-th smallest is among them, line L20 follows the range to the left child; otherwise line L21 skips the $z$ smaller symbols and goes right.

**Build.** Level by level, stably partition each $S_v$ into its two halves while writing $B_v$, then build the rank and select indexes. The time is $O(n \lg \sigma)$.

## Example

Take $S = $ abracadabra, coded as $a = 0$, $b = 1$, $c = 2$, $d = 3$, $r = 4$, so $S = 0\,1\,4\,0\,2\,0\,3\,0\,1\,4\,0$ with $n = 11$ and $\sigma = 5$.

| node | range | $S_v$ | $m_v$ | $B_v$ |
|---|---|---|---|---|
| root | $[0, 5)$ | a b r a c a d a b r a | 2 | 00101010010 |
| left | $[0, 2)$ | a b a a a b a | 1 | 0100010 |
| right | $[2, 5)$ | r c d r | 3 | 1011 |
| right, right | $[3, 5)$ | r d r | 4 | 101 |

The leaves are $a$, $b$, $c$, $d$ and $r$. The bit vectors hold $11 + 7 + 4 + 3 = 25$ bits, at most $n \lceil \lg 5 \rceil = 33$.

- ACCESS$(4)$: at the root $B[4] = 1$, so $i = \text{rank}_1(4) = 1$ and we go right. There $B[1] = 0$, so $i = \text{rank}_0(1) = 0$ and we go left, to the leaf $[2, 3)$. The answer is $2 = c$.
- RANK$(a, 7)$: $a < 2$, so $i = \text{rank}_0(7) = 4$ in the root; then $a < 1$, so $i = \text{rank}_0(4) = 3$ in the left node. The answer is 3.
- SELECT$(a, 4)$: in the leaf $a$, the position is 3. In the left node, the 4th 0 of 0100010 is at 4. In the root, the 5th 0 of 00101010010 is at 7. The answer is 7.
- QUANTILE$(2, 9, 4)$: $S[2 \ldots 8] = $ r a c a d a b, whose sorted order is a a a b c d r, so the answer must be $b$. At the root, $z = \text{rank}_0(9) - \text{rank}_0(2) = 6 - 2 = 4 \ge 4$, so we go left with $l = 2$, $r = 6$. There, $z = \text{rank}_0(6) - \text{rank}_0(2) = 4 - 1 = 3 < 4$, so $k = 1$ and we go right to the leaf $b$.

## Correctness

The proof rests on one lemma: for an inner node $v$ and $0 \le i \le |S_v|$, the symbols of $S_v[0 \ldots i-1]$ that are less than $m_v$ form the prefix of length $\text{rank}_0(B_v, i)$ of the left child's sequence, and those that are at least $m_v$ form the prefix of length $\text{rank}_1(B_v, i)$ of the right child's sequence. This holds because each child sequence keeps the order of $S_v$. Access, rank and quantile then keep an invariant about the current node and position, and select inverts the lemma. The full proof is in [the proof of correctness](proofs/correctness.md).

## Complexity

| operation | time, worst case |
|---|---|
| build | $O(n \lg \sigma)$ |
| access, rank, quantile | $O(\lg \sigma)$: one or two ranks on each of $\lceil \lg \sigma \rceil$ levels |
| select | $O(\lg \sigma)$: one select on each level |

**Space.** The bit vectors of each level sum to at most $n$ bits, and there are $\lceil \lg \sigma \rceil$ levels, so they take at most $n \lceil \lg \sigma \rceil$ bits; their rank and select indexes add $o(n \lg \sigma)$. The tree shape and the $\sigma - 1$ pointers take $O(\sigma \lg n)$ bits; the shape is implicit in the balanced split, and the [wavelet matrix](/wavelet-matrix/) removes the pointers.

**Compressed space.** If each $B_v$ is an [RRR bit vector](/rrr-bitvector/), the sum of $\lg \binom{|B_v|}{\text{ones}}$ over all nodes telescopes to $n H_0(S)$, so the total is $n H_0(S) + o(n \lg \sigma)$, whatever the shape of the tree.

## Variants

- **Huffman shape.** Using the [Huffman](/huffman-coding/) tree of the symbol frequencies as the shape makes the total length of the bit vectors less than $n(H_0(S) + 1)$, and the average time of access $O(1 + H_0(S))$.
- **Wavelet matrix.** Concatenate the bit vectors of each level and reorder each level by the bit of the previous level; the [wavelet matrix](/wavelet-matrix/) has no pointers and is faster for large alphabets.
- **Multiary wavelet trees.** Nodes of arity $\rho$ with sequences over $\rho$ symbols give height $\lceil \log_\rho \sigma \rceil$ and $O(\lg \sigma / \lg \lg n)$ time with suitable sequence structures at the nodes.
- **Range counting and reporting.** Seen as a grid of the points $(i, S[i])$, the tree counts the points of a rectangle in $O(\lg \sigma)$ time and reports each in $O(\lg \sigma)$ more; this is how it solves 2D orthogonal range queries in $n \lg \sigma + o(n \lg \sigma)$ bits.
- **Distinct values and top-$k$.** Visiting all nonempty nodes of a range lists the distinct symbols of $S[l \ldots r-1]$, the core of [document listing](/document-listing/).
- **Dynamic wavelet trees.** With [dynamic bit vectors](/dynamic-bit-vector/) at the nodes, the tree supports insertion and deletion of symbols in $O(\lg \sigma \lg n)$ time.

## When to use it

Use a wavelet tree for a static sequence over a moderate alphabet when you need rank and select on all symbols in about the space of the sequence: the [Burrows-Wheeler transform](/burrows-wheeler-transform/) inside an [FM-index](/fm-index/), the document array in [document listing](/document-listing/), and range quantile or range counting on an array of integers. For very large alphabets, prefer the [wavelet matrix](/wavelet-matrix/). For a small alphabet and speed above all, one [bit vector](/rank-select-dictionary/) per symbol is faster.

## Pitfalls

- **Rank of a position, rank of a prefix.** Line L4 uses the bit at position $i$ to choose the child, while line L10 uses the symbol $c$; mixing them gives the wrong child when $S[i] \ne c$.
- **Off by one in select.** A position $p$ in a child is the $(p+1)$-th 0 or 1 of the parent, not the $p$-th. Lines L15 and L16 add 1.
- **Symbols that do not occur.** RANK$(c, i)$ for a symbol with no occurrences returns 0 and is fine, but SELECT$(c, j)$ with $j > n_c$ calls select beyond the last 0 or 1; check $j \le \text{RANK}(c, n)$ first.
- **Uneven splits.** With $m = \lfloor (a+b)/2 \rfloor$, the left half can be smaller by one; code that assumes $\sigma$ is a power of two must pad the alphabet, which adds empty nodes.
- **Pointer overhead for large $\sigma$.** For $\sigma$ close to $n$, the $O(\sigma \lg n)$ bits of pointers dominate; use the [wavelet matrix](/wavelet-matrix/) or a levelwise layout.

## Implementations

## History

Grossi, Gupta and Vitter introduced the wavelet tree at SODA 2003, inside a compressed text index of high-order entropy space, where it gives rank over the Burrows-Wheeler transform. Ferragina, Manzini, Mäkinen and Navarro used it in 2004 and 2007 to make the [FM-index](/fm-index/) work for large alphabets. Mäkinen and Navarro used it for 2D range searching in 2006, and Gagie, Puglisi and Turpin noted in 2009 its use for range quantile queries. Navarro's survey "Wavelet trees for all" (2014) collected its many applications. Claude, Navarro and Ordóñez gave the [wavelet matrix](/wavelet-matrix/) in 2012.

## References
