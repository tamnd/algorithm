---
tag: D62R54
kind: data-structure
slug: jacobson-rank
name: Jacobson's rank structure
aliases:
- Jacobson rank dictionary
area: data-structures/succinct-structures
level: advanced
summary: Jacobson's 1989 n + o(n)-bit structure answering rank in O(1) time, the first succinct rank index.
model: word-ram
complexity:
  vars: {n: the number of bits}
  time: {build: O(n), rank: O(1), select: O(log n)}
  space: {total: n + O(n log log n / log n)}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 1989
  people: [Guy Jacobson]
  note: Jacobson gave the two-level rank directory in his FOCS 1989 paper and his Carnegie Mellon thesis, as the base of succinct trees and graphs.
prereqs: [rank-select-problem, bit-vector, four-russians-method]
see_also: [rank-select-dictionary, fully-indexable-dictionary, rrr-bitvector, succinct-data-structures, population-count, louds-tree, patrascu-succinct-lower-bound]
sources:
  - paper: doi:10.1109/SFCS.1989.63533
    title: Guy Jacobson, Space-efficient static trees and graphs, 30th Annual Symposium on Foundations of Computer Science (FOCS 1989), 549-554
    locator: the rank directory of superblocks and blocks with a lookup table, and its use for level-order trees
  - book: isbn:9781107152380
    title: Gonzalo Navarro, Compact Data Structures, A Practical Approach, Cambridge University Press, 2016
    locator: Chapter 4, Section 4.2 (Rank), Subsections 4.2.1 (Sparse Sampling) and 4.2.2 (Constant Time)
  - paper: doi:10.1007/978-3-540-68552-4_12
    title: Sebastiano Vigna, Broadword implementation of rank/select queries, 7th Workshop on Experimental Algorithms (WEA 2008), Lecture Notes in Computer Science 5038, 154-168
    locator: the rank9 layout, a two-level directory with 64-bit blocks and population count
  - paper: doi:10.1016/j.tcs.2007.07.041
    title: Alexander Golynski, Optimal lower bounds for rank and select indexes, Theoretical Computer Science 387(3), 2007, 348-359
    locator: the main theorem, which shows that an index of Θ(n lg lg n / lg n) bits is optimal when the bit vector is stored in plain form
---

Jacobson's rank structure adds an index of $O(n \lg \lg n / \lg n) = o(n)$ bits to a [bit vector](/bit-vector/) of $n$ bits, so that $\text{rank}_1(i)$, the number of 1s before position $i$, takes $O(1)$ time on the [word RAM](/word-ram/). It stores the rank at the start of each *superblock* of about $\lg^2 n$ bits, the rank relative to its superblock at the start of each *block* of about $\frac12 \lg n$ bits, and a table of the ranks inside all possible blocks. Guy Jacobson gave it in 1989, and it was the first succinct index for the [rank and select problem](/rank-select-problem/). Select follows by binary search in $O(\lg n)$ time; constant-time select is on the page [rank/select dictionary](/rank-select-dictionary/).

## In plain words

Counting the 1s before a place in a long row of bits is slow if you start from the left each time. Writing the answer for each place would be fast, but it would take far more memory than the bits.

The trick is to write the answer only at a few places. Every few hundred bits, you write the full count so far. Every few bits inside that stretch, you write a small count from the start of the stretch, which needs only a few bits since it is small. For the last few bits, you look the answer up in a small table that lists, for each possible short pattern of bits, how many 1s it has before each position. There are few short patterns, so the table is small. Each question is then three lookups and two additions.

## The abstract type

The structure answers $\text{rank}_1$ and $\text{rank}_0$ on a static bit vector, and $\text{access}$ and $\text{select}$ through rank. It is a solution of the [rank and select problem](/rank-select-problem/) that is fast for rank only. The operations are `build(B)`, `access(i)`, `rank1(i)` for $0 \le i \le n$, `rank0(i)` $= i - $ `rank1(i)`, and `select1(j)` for $1 \le j \le m$, where $m$ is the number of 1s.

## Representation

Let $n \ge 1$ and $\ell = \max(1, \lceil \lg n \rceil)$. The structure fixes the block length $b = \max(1, \lfloor \ell / 2 \rfloor)$, the number $s = 2b$ of blocks in a superblock, and the superblock length $L = sb$, which is $\Theta(\lg^2 n)$. Block $k$ covers the positions $kb$ to $kb + b - 1$, for $0 \le k \le K = \lfloor n/b \rfloor$; positions of $n$ or more read as 0. The fields are:

- $X[0 \ldots K]$: the bits of block $k$ as a $b$-bit number, with $B[kb + t]$ as bit $t$. This is the bit vector itself, in $n + O(b)$ bits.
- $RS[0 \ldots \lfloor K/s \rfloor]$: $RS[q] = \text{rank}_1(qL)$, one number of $\lceil \lg(n+1) \rceil$ bits for each superblock.
- $RB[0 \ldots K]$: $RB[k] = \text{rank}_1(kb) - RS[\lfloor k/s \rfloor]$, the rank relative to the superblock. It is less than $L$, so it fits in $\lceil \lg L \rceil = O(\lg \lg n)$ bits.
- $T[x][r]$ for $0 \le x < 2^b$ and $0 \le r \le b$: the number of 1s among the $r$ lowest bits of $x$.

These equations are the invariant. The structure is static, so BUILD sets them once.

## Operations

```pseudo id=main
BUILD(B[0 .. n − 1])
L1  b ← max(1, ⌊⌈lg n⌉ / 2⌋), s ← 2b, K ← ⌊n / b⌋   ▷ block length and blocks per superblock
L2  for x ← 0 to 2^b − 1 and r ← 0 to b do T[x][r] ← the number of 1s in the r low bits of x
L3  c ← 0                                        ▷ c = rank1(kb) at the top of each step
L4  for k ← 0 to K do
L5      if k mod s = 0 then RS[k / s] ← c
L6      RB[k] ← c − RS[⌊k / s⌋]
L7      X[k] ← B[kb .. kb + b − 1] as a number, bit t = B[kb + t], 0 past n − 1
L8      c ← c + T[X[k]][b]

RANK1(i)                                         ▷ 0 ≤ i ≤ n
L9  k ← ⌊i / b⌋
L10 return RS[⌊k / s⌋] + RB[k] + T[X[k]][i mod b]

SELECT1(j)                                       ▷ 1 ≤ j ≤ m
L11 lo ← 0, hi ← n − 1
L12 while lo < hi do
L13     mid ← ⌊(lo + hi) / 2⌋
L14     if RANK1(mid + 1) ≥ j then hi ← mid else lo ← mid + 1
L15 return lo
```

**Build.** Line L2 fills the table for each pattern of $b$ bits. The loop of line L4 walks the blocks from left to right and keeps $c = \text{rank}_1(kb)$. At the first block of a superblock, line L5 writes the full count. Line L6 writes the count relative to the superblock. Line L8 adds the 1s of the block, read from the table with $r = b$. The time is $O(2^b b + n/b + n) = O(n)$, since $2^b \le 2^{\lg n / 2 + 1} = O(\sqrt{n})$.

**Rank.** Position $i$ lies in block $k = \lfloor i/b \rfloor$, which lies in superblock $\lfloor k/s \rfloor$. The 1s before $i$ are the 1s before the superblock, those between the start of the superblock and the start of the block, and those among the first $i \bmod b$ bits of the block. Line L10 reads one value for each part. This is three table reads and two additions, $O(1)$ time. For $i = n$ with $b \mid n$, the index $k = K$ points at the extra empty block, which is why the loops run to $K$.

**Access.** $B[i]$ is bit $i \bmod b$ of $X[\lfloor i/b \rfloor]$, or $\text{rank}_1(i+1) - \text{rank}_1(i)$.

**Select.** By the identity $\text{select}_1(j) = \min\{p : \text{rank}_1(p+1) \ge j\}$, and since $\text{rank}_1(p+1)$ does not decrease in $p$, lines L11 to L15 are a [binary search](/binary-search/) for that least $p$. It calls RANK1 $\lceil \lg n \rceil$ times at most, so it takes $O(\lg n)$ time. A first binary search on $RS$ and then on $RB$ inside the superblock does the same work with fewer cache misses.

## Example

Let $B = 1011\,0010\,1100\,0111$, so $n = 16$ and $\lceil \lg n \rceil = 4$. Then $b = 2$, $s = 4$, $L = 8$ and $K = 8$. The blocks, with $B[2k]$ as bit 0, are:

| $k$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| bits $B[2k]\,B[2k+1]$ | 10 | 11 | 00 | 10 | 11 | 00 | 01 | 11 | (empty) |
| $X[k]$ | 1 | 3 | 0 | 1 | 3 | 0 | 2 | 3 | 0 |
| $\text{rank}_1(2k)$ | 0 | 1 | 3 | 3 | 4 | 6 | 6 | 7 | 9 |
| $RB[k]$ | 0 | 1 | 3 | 3 | 0 | 2 | 2 | 3 | 0 |

The superblock counts are $RS = [0, 4, 9]$, at positions 0, 8 and 16. The table for $b = 2$ has $T[2][1] = 0$, because the low bit of $2 = 10_2$ is 0, and $T[3][1] = 1$.

- RANK1$(13)$: $k = 6$, $RS[1] = 4$, $RB[6] = 2$, $T[X[6]][1] = T[2][1] = 0$. The result is $4 + 2 + 0 = 6$.
- RANK1$(16)$: $k = 8$, $RS[2] = 9$, $RB[8] = 0$, $T[0][0] = 0$. The result is 9.
- SELECT1$(5)$: the search tries $mid = 7$ ($\text{rank}_1(8) = 4 < 5$, so $lo = 8$), then $mid = 11$ ($\text{rank}_1(12) = 6 \ge 5$, $hi = 11$), $mid = 9$ ($\text{rank}_1(10) = 6$, $hi = 9$), $mid = 8$ ($\text{rank}_1(9) = 5$, $hi = 8$). It returns 8.

## Correctness

The invariant is the list of equations of the representation. BUILD makes them true by the loop invariant $c = \text{rank}_1(kb)$ of line L4. RANK1 is then correct because

$$\text{rank}_1(i) = \text{rank}_1(qL) + (\text{rank}_1(kb) - \text{rank}_1(qL)) + (\text{rank}_1(i) - \text{rank}_1(kb)),$$

with $k = \lfloor i/b \rfloor$ and $q = \lfloor k/s \rfloor$, and the three terms are $RS[q]$, $RB[k]$ and $T[X[k]][i \bmod b]$. SELECT1 is correct by the invariant of the binary search: the answer is always in $[lo, hi]$. The full proof is in [the proof of correctness](proofs/correctness.md).

## Complexity

| operation | time, worst case |
|---|---|
| build | $O(n)$ |
| rank | $O(1)$: three reads and two additions |
| access | $O(1)$ |
| select | $O(\lg n)$ by binary search over rank |

**Space.** With $\ell = \lceil \lg n \rceil$ and $b \approx \ell/2$:

- $RS$ has $n/L + 1$ entries of $\ell + 1$ bits, so $O(n / \lg n)$ bits.
- $RB$ has $n/b + 1$ entries of $\lceil \lg L \rceil = O(\lg \lg n)$ bits, so $O(n \lg \lg n / \lg n)$ bits. This term dominates.
- $T$ has $2^b (b + 1)$ entries of $\lceil \lg(b+1) \rceil$ bits, at most $2^{\ell/2} (\ell + 1) \lg(\ell + 1) = O(\sqrt{n} \lg n \lg \lg n)$ bits.

So the index is $O(n \lg \lg n / \lg n) = o(n)$ bits, and the total is $n + o(n)$ bits. Golynski proved that an index of $\Omega(n \lg \lg n / \lg n)$ bits is needed when $B$ is kept in plain form and a query reads $O(\lg n)$ bits of $B$, so this order of redundancy is optimal for such structures.

**The constants matter.** For $n = 2^{32}$, the parameters give $b = 16$ and $L = 512$. Then $RS$ costs $33/512 \approx 0.064$ bits for each bit of $B$ and $RB$ costs $9/16 \approx 0.56$, so the index is about 63% of $n$. Practical layouts use 64-bit blocks and a [population count](/population-count/) instruction in place of $T$: Vigna's rank9 uses 512-bit superblocks and packs the seven 9-bit relative counts of one superblock in one word, for an index of 25% of $n$.

## Variants

- **Rank9 and popcount layouts.** Blocks of one word, rank inside the block by POPCOUNT, and the relative counts interleaved with the absolute counts so that one query touches one or two cache lines.
- **Sparse sampling.** Keep only $RS$, with superblocks of $s$ words, and scan up to $s$ words with POPCOUNT. This uses $n \lg n / (sw)$ bits for $O(s)$ time.
- **Constant-time select.** Add the select index of Clark or of Munro: the [rank/select dictionary](/rank-select-dictionary/).
- **Compressed blocks.** Store each block as its number of 1s and an offset among the blocks with that many 1s: the [RRR bit vector](/rrr-bitvector/), which reaches $\lg \binom{n}{m} + o(n)$ bits.
- **Bit-probe form.** Jacobson stated his bounds in the bit-probe model, where a query is charged for each bit it reads. A rank query here reads $O(\lg n)$ bits.

## When to use it

Use this layout when rank is the main query and the bit vector is static: LOUDS trees, the occurrence counts of an [FM-index](/fm-index/), or a [bit vector](/bit-vector/) that marks the starts of items of variable length. In code, use the popcount form with 64-bit blocks, which is smaller and faster than the half-log blocks of the theory. If select is just as frequent, add a select index. If the bits are very sparse, an [SD-array](/sd-array/) is smaller.

## Pitfalls

- **The end of the vector.** RANK1$(n)$ reads block $\lfloor n/b \rfloor$, which does not exist when $b \mid n$ unless the build stores one extra block, as lines L4 to L8 do with $k$ up to $K$.
- **Inclusive or exclusive rank.** Line L10 uses $T[X[k]][i \bmod b]$, the bits below $i$. Using $T[X[k]][i \bmod b + 1]$ gives the inclusive rank and makes the binary search of line L14 off by one.
- **Superblocks that are not a multiple of the block.** If $L$ is not a multiple of $b$, a block can cross a superblock boundary and $RB[k]$ is no longer relative to one superblock. Line L1 sets $L = sb$.
- **Asymptotic parameters on real data.** With $b = \frac12 \lg n$ the index is over half the size of $B$ for $n = 2^{32}$, as computed above. The $o(n)$ bound is asymptotic.
- **Overflow of the relative counts.** $RB[k] < L$ needs $\lceil \lg L \rceil$ bits. A field of $\lceil \lg b \rceil$ bits is too small.

## Implementations

## History

Guy Jacobson introduced the structure in his 1989 FOCS paper "Space-efficient static trees and graphs" and in his doctoral thesis at Carnegie Mellon University. He used it to store trees in level order ([LOUDS](/louds-tree/)) and graphs of bounded page number in a linear number of bits, with navigation by rank and select. Clark, in his 1996 thesis at the University of Waterloo, and Munro, in his paper "Tables" of 1996, added constant-time select on the word RAM. Golynski showed in 2006 and 2007 that the redundancy $\Theta(n \lg \lg n / \lg n)$ is optimal when the bit vector is kept in plain form.

## References
