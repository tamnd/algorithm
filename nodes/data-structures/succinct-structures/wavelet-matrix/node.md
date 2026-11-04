---
tag: 1R9K6G
kind: data-structure
slug: wavelet-matrix
name: Wavelet matrix
aliases:
- Claude-Navarro wavelet matrix
- levelwise wavelet tree
area: data-structures/succinct-structures
level: advanced
summary: A level-wise variant of the wavelet tree that stores one bit vector per level and avoids pointers.
model: word-ram
complexity:
  vars: {n: the length of the sequence, σ: the alphabet size}
  time: {access: O(log σ), rank: O(log σ), select: O(log σ), quantile: O(log σ), build: O(n log σ)}
  space: {total: "n log σ + o(n log σ)"}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 2012
  people: [Francisco Claude, Gonzalo Navarro, Alberto Ordóñez]
  note: Claude and Navarro presented the wavelet matrix at SPIRE 2012, and the journal version with Ordóñez appeared in Information Systems in 2015.
prereqs: [wavelet-tree]
see_also: [static-sequence, rank-select-dictionary, range-kth-smallest-query, fm-index, compressed-data-structure, radix-sort, document-listing, succinct-data-structures]
sources:
  - paper: doi:10.1007/978-3-642-34109-0_18
    title: Francisco Claude and Gonzalo Navarro, The wavelet matrix, String Processing and Information Retrieval (SPIRE 2012), LNCS 7608, 167-179
    locator: the definition of the levels, the counts z of zeros, and the access, rank and select algorithms
  - paper: doi:10.1016/j.is.2014.06.002
    title: Francisco Claude, Gonzalo Navarro and Alberto Ordóñez, The wavelet matrix, an efficient wavelet tree for large alphabets, Information Systems 47, 2015, 15-32
    locator: the wavelet matrix, its compressed variants, and the experimental comparison with pointerless wavelet trees
  - book: isbn:9781107152380
    title: Gonzalo Navarro, Compact Data Structures, A Practical Approach, Cambridge University Press, 2016
    locator: Chapter 6, Section 6.2.5 (Wavelet Matrices)
---

A wavelet matrix stores a static sequence $S[0 \ldots n-1]$ over $\sigma$ symbols as $L = \lceil \lg \sigma \rceil$ bit vectors of $n$ bits each, one for each bit of the symbols, and answers access, rank and select of the [static sequence](/static-sequence/) type in $O(\lg \sigma)$ time, in $n \lceil \lg \sigma \rceil + o(n \lg \sigma)$ bits with no pointers. Level $\ell$ holds bit $\ell$ of each symbol, counted from the most significant, with the symbols reordered so that, after each level, all the symbols with a 0 in that bit come before all the symbols with a 1, as in one pass of an LSD [radix sort](/radix-sort/) run from the top bit. A position moves down by one rank and one addition, and the tree shape of the [wavelet tree](/wavelet-tree/) disappears. Claude and Navarro introduced it in 2012; for large alphabets it is faster and smaller than the wavelet tree.

## In plain words

Write each letter in binary, all with the same number of bits. The first row of the matrix holds the first bit of each letter, in the order of the string. Then reorder the letters: those whose first bit is 0 go first, in their old order, and then those whose first bit is 1. The second row holds the second bit of each letter in this new order. Reorder again by the second bit, and so on.

To follow a letter down the rows, you need to know where it moved. If its bit is 0, its new place is the count of 0s before it. If its bit is 1, its new place is the count of all 0s in the row plus the count of 1s before it. With this, you can read a letter, count its copies before a place, or find its tenth copy.

## The abstract type

The structure answers the queries of the [static sequence](/static-sequence/) type: `access(i)`, `rank(c, i)`, the number of $c$ in $S[0 \ldots i-1]$, and `select(c, j)`, the position of the $j$-th $c$, for $j \ge 1$. It also answers `quantile(l, r, k)`, the $k$-th smallest symbol of $S[l \ldots r-1]$, the [range k-th smallest query](/range-kth-smallest-query/). Symbols are integers in $[0, 2^L)$ with $L = \max(1, \lceil \lg \sigma \rceil)$, and bit $\ell$ of $c$, written $c_\ell$, is bit $L - 1 - \ell$ of its binary form.

## Representation

Let $S_0 = S$. For each level $\ell = 0, \ldots, L-1$:

- $B_\ell[i] = (S_\ell[i])_\ell$, a bit vector of $n$ bits with rank and select;
- $z_\ell$ is the number of 0s of $B_\ell$;
- $S_{\ell+1}$ is $S_\ell$ stably reordered: first the symbols with $B_\ell[i] = 0$, then those with $B_\ell[i] = 1$, each group in its order in $S_\ell$.

Only the $B_\ell$ and the $z_\ell$ are stored. The $S_\ell$ are not. The invariant is that $B_\ell$ and $z_\ell$ are as defined; the structure is static.

The reordering moves a position $i$ of level $\ell$ to the position

$$\text{down}_\ell(i) = \begin{cases} \text{rank}_0(B_\ell, i) & \text{if } B_\ell[i] = 0, \\ z_\ell + \text{rank}_1(B_\ell, i) & \text{if } B_\ell[i] = 1 \end{cases}$$

of level $\ell + 1$. All the operations follow from this map.

## Operations

```pseudo id=main
ACCESS(i)                                    ▷ 0 ≤ i < n
L1  c ← 0
L2  for ℓ ← 0 to L − 1 do
L3      if B_ℓ[i] = 0 then c ← 2c, i ← RANK0_ℓ(i)
L4      else c ← 2c + 1, i ← z_ℓ + RANK1_ℓ(i)
L5  return c

RANK(c, i)                                   ▷ 0 ≤ i ≤ n
L6  p ← 0
L7  for ℓ ← 0 to L − 1 do
L8      if c_ℓ = 0 then p ← RANK0_ℓ(p), i ← RANK0_ℓ(i)
L9      else p ← z_ℓ + RANK1_ℓ(p), i ← z_ℓ + RANK1_ℓ(i)
L10 return i − p

SELECT(c, j)                                 ▷ 1 ≤ j ≤ n_c
L11 p ← the value of p after lines L6 to L9
L12 q ← p + j − 1                                  ▷ the position at the bottom
L13 for ℓ ← L − 1 downto 0 do
L14     if c_ℓ = 0 then q ← SELECT0_ℓ(q + 1)
L15     else q ← SELECT1_ℓ(q − z_ℓ + 1)
L16 return q

QUANTILE(l, r, k)                            ▷ 1 ≤ k ≤ r − l
L17 c ← 0
L18 for ℓ ← 0 to L − 1 do
L19     t ← RANK0_ℓ(r) − RANK0_ℓ(l)
L20     if k ≤ t then c ← 2c, l ← RANK0_ℓ(l), r ← RANK0_ℓ(r)
L21     else c ← 2c + 1, k ← k − t, l ← z_ℓ + RANK1_ℓ(l), r ← z_ℓ + RANK1_ℓ(r)
L22 return c
```

**Access.** Lines L3 and L4 apply $\text{down}_\ell$ to follow the symbol of position $i$ and read one bit of it at each level.

**Rank.** At level $\ell$, the symbols that agree with $c$ on bits $0, \ldots, \ell - 1$ occupy one contiguous block of $S_\ell$, and $p$ is the start of that block. The copies of $c$ in $S[0 \ldots i_0 - 1]$, followed down, are the first ones of that block, up to position $i$. Line L8 or L9 maps both ends down; at the bottom the block holds only copies of $c$, and $i - p$ counts those that came from before $i_0$.

**Select.** At the bottom, the copies of $c$ are at positions $p, p+1, \ldots$ in their order in $S$, so the $j$-th is at $q = p + j - 1$. Lines L14 and L15 invert $\text{down}_\ell$: a position $q$ below a 0 is the $(q+1)$-th 0 of $B_\ell$, and a position $q \ge z_\ell$ below a 1 is the $(q - z_\ell + 1)$-th 1.

**Quantile.** As in the wavelet tree, $t$ counts the symbols of the current range that have a 0 in the current bit; they are the smaller ones. The range moves down by the same map as $p$ and $i$.

**Build.** Each level is one stable partition of $n$ symbols by one bit, so the build is $O(n \lg \sigma)$ time and $O(n \lg \sigma)$ bits of working space, or $O(n)$ words.

## Example

Take $S = $ abracadabra coded as $a = 0$, $b = 1$, $c = 2$, $d = 3$, $r = 4$, so $\sigma = 5$ and $L = 3$; in binary $a = 000$, $b = 001$, $c = 010$, $d = 011$, $r = 100$.

| level $\ell$ | $S_\ell$ | $B_\ell$ | $z_\ell$ |
|---|---|---|---|
| 0 | 0 1 4 0 2 0 3 0 1 4 0 | 00100000010 | 9 |
| 1 | 0 1 0 2 0 3 0 1 0 4 4 | 00010100000 | 9 |
| 2 | 0 1 0 0 0 1 0 4 4 2 3 | 01000100001 | 8 |

The three bit vectors take $3 \cdot 11 = 33$ bits, which is $n \lceil \lg \sigma \rceil$; the wavelet tree of the same string uses 25 bits but needs pointers.

- ACCESS$(4)$: at level 0, $B_0[4] = 0$, so $i = \text{rank}_0(4) = 3$. At level 1, $B_1[3] = 1$, so $c = 01$ and $i = 9 + \text{rank}_1(3) = 9$. At level 2, $B_2[9] = 0$, so $c = 010 = 2$, which is $c$.
- RANK$(a, 7)$: $a = 000$, so $p$ stays 0 and $i$ becomes $\text{rank}_0(7) = 6$, then $\text{rank}_0(6) = 4$, then $\text{rank}_0(4) = 3$. The answer is $3 - 0 = 3$.
- RANK$(r, 10)$: $r = 100$. At level 0, $p = 9 + \text{rank}_1(0) = 9$ and $i = 9 + \text{rank}_1(10) = 11$. At level 1, $p = \text{rank}_0(9) = 7$ and $i = \text{rank}_0(11) = 9$. At level 2, $p = \text{rank}_0(7) = 5$ and $i = \text{rank}_0(9) = 7$. The answer is $7 - 5 = 2$: the $r$s at positions 2 and 9.
- SELECT$(a, 4)$: $p = 0$, so $q = 3$. Going up: the 4th 0 of $B_2$ is at 4, the 5th 0 of $B_1$ is at 6, and the 7th 0 of $B_0$ is at 7. The answer is 7.

## Correctness

The proof uses two facts. First, $\text{down}_\ell$ maps position $i$ of $S_\ell$ to the position of the same symbol occurrence in $S_{\ell+1}$, by the definition of the stable reordering. Second, by induction on $\ell$, $S_\ell$ is sorted by the first $\ell$ bits of the symbols, with ties in their order in $S$; so the symbols that share a prefix of $\ell$ bits form a contiguous block of $S_\ell$, in the order of $S$. Access follows the first fact; rank and select use the block of $c$ at each level. The full proof is in [the proof of correctness](proofs/correctness.md).

## Complexity

| operation | time, worst case |
|---|---|
| build | $O(n \lg \sigma)$ |
| access | $O(\lg \sigma)$: one access and one rank for each level |
| rank, quantile | $O(\lg \sigma)$: two ranks for each level |
| select | $O(\lg \sigma)$: $L$ ranks down and $L$ selects up |

**Space.** $L$ bit vectors of $n$ bits, $n \lceil \lg \sigma \rceil$ bits, with their rank and select indexes, $o(n \lg \sigma)$ bits, and $L$ counts $z_\ell$ of $\lg n$ bits. There are no pointers and no tree shape, which saves the $O(\sigma \lg n)$ bits of a pointer-based [wavelet tree](/wavelet-tree/). For $\sigma$ close to $n$, this is the difference between about $n \lg n$ bits and about $2 n \lg n$.

## Variants

- **Compressed levels.** With [RRR](/rrr-bitvector/) bit vectors at each level, the space becomes $n H_0(S) + o(n \lg \sigma)$; each node of the wavelet tree is a contiguous piece of one level, in a different order, so the compressed sizes add up to the zero-order entropy as for the wavelet tree, up to the blocks that straddle two nodes.
- **Huffman-shaped wavelet matrix.** Claude, Navarro and Ordóñez use canonical Huffman codes that can be laid out by levels, which gives $n (H_0(S) + 1)$ bits for the bit vectors and $O(1 + H_0)$ average access time.
- **Range queries.** Counting the points $(i, S[i])$ in a rectangle, reporting them, and listing the distinct values of a range work as on the wavelet tree, by keeping the two ends of a range at each level.
- **Small alphabets.** For $\sigma = 2^L$ small, a [wavelet tree](/wavelet-tree/) with one bit vector per level and implicit node boundaries is the same size and slightly simpler.

## When to use it

Use a wavelet matrix for a static sequence over a large alphabet, such as an array of integers or the document array of a collection, when you need access, rank, select or range quantiles in about $n \lceil \lg \sigma \rceil$ bits. It is the usual choice in practice for $\sigma$ more than a few thousand, and a good default for range quantile queries on integer arrays. For small alphabets and compressed space, a Huffman-shaped [wavelet tree](/wavelet-tree/) with [RRR](/rrr-bitvector/) bit vectors is a little smaller.

## Pitfalls

- **Bit order.** Level 0 must hold the most significant bit, so that the order of the levels is the order of the symbols; quantile depends on this.
- **Forgetting $z_\ell$.** A position under a 1 moves to $z_\ell + \text{rank}_1$, not to $\text{rank}_1$. Without the offset, the 1s of a level overwrite the 0s.
- **Select needs the start of the block.** SELECT must first run the descent of RANK to find $p$, and then add $j - 1$; starting the ascent from $j - 1$ alone is wrong for every symbol but the smallest.
- **Symbols outside $[0, \sigma)$.** With $L = \lceil \lg \sigma \rceil$, the values $\sigma, \ldots, 2^L - 1$ are valid bit patterns that do not occur; RANK returns 0 for them, but SELECT must check $j \le \text{RANK}(c, n)$.
- **$\sigma = 1$.** Then $\lceil \lg \sigma \rceil = 0$; use $L = 1$ so that each operation has one level.

## Implementations

## History

Claude and Navarro presented the wavelet matrix at SPIRE 2012 as a levelwise layout of the wavelet tree in which each level is reordered by the bit of the previous level, which removes the pointers and the per-node offsets of earlier pointerless wavelet trees. The journal version, with Ordóñez, appeared in Information Systems in 2015 and added Huffman-shaped and compressed variants, with experiments that showed it faster than the wavelet tree for large alphabets.

## References
