---
tag: PZD3RH
kind: data-structure
slug: sd-array
name: SD-array
aliases:
- sdarray
- sparse bit vector
- sd-vector
area: data-structures/succinct-structures
level: advanced
summary: A compressed bit vector built on Elias-Fano coding that is efficient for sparse bit vectors.
model: word-ram
complexity:
  vars: {n: the length of the bit vector, m: the number of 1s}
  time: {select1: O(1), rank: O(1 + log(n / m)), access: O(1 + log(n / m)), select0: O(log n log(n / m)), build: O(n)}
  space: {total: "m log(n / m) + 2 m + o(m)"}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 2007
  people: [Daisuke Okanohara, Kunihiko Sadakane]
  note: Okanohara and Sadakane named the sdarray in their 2007 paper on practical rank/select dictionaries, as an Elias-Fano code of the positions of the 1s with select on its upper bits.
prereqs: [elias-fano-encoding]
see_also: [rrr-bitvector, rank-select-dictionary, fully-indexable-dictionary, bit-vector, rank-select-problem, binary-search, succinct-data-structures, compressed-data-structure]
sources:
  - paper: doi:10.1137/1.9781611972870.6
    title: Daisuke Okanohara and Kunihiko Sadakane, Practical entropy-compressed rank/select dictionary, Workshop on Algorithm Engineering and Experiments (ALENEX 2007), 60-70
    locator: the sdarray, the Elias-Fano split of the positions of the 1s into high bits with select and low bits, and its rank and select
  - book: isbn:9781107152380
    title: Gonzalo Navarro, Compact Data Structures, A Practical Approach, Cambridge University Press, 2016
    locator: Chapter 4, Section 4.4 (Very Sparse Bitvectors), Subsections 4.4.1 (Constant-Time Select) and 4.4.2 (Solving Rank)
  - paper: doi:10.1145/321812.321820
    title: Peter Elias, Efficient storage and retrieval by content and address of static files, Journal of the ACM 21(2), 1974, 246-260
    locator: the high and low bit representation of a sorted list that the SD-array stores
---

The SD-array is a bit vector $B$ of $n$ bits with $m$ ones, stored as the [Elias-Fano code](/elias-fano-encoding/) of the positions of its 1s, in $m \lfloor \lg(n/m) \rfloor + 2m + o(m)$ bits, with $\text{select}_1$ in $O(1)$ time and $\text{rank}$ and access in $O(\lg(n/m))$ time on the [word RAM](/word-ram/). The space depends on $m$ and only logarithmically on $n$, so for a vector with very few 1s it is far below the $n$ bits of a plain [bit vector](/bit-vector/) and below the $o(n)$ redundancy of an [RRR bit vector](/rrr-bitvector/). Okanohara and Sadakane introduced it under the name sdarray in 2007. This page is about the bit-vector queries; the encoding of the sequence and its successor search are on the Elias-Fano page.

## In plain words

Some rows of bits are almost all 0s: one 1 in a thousand, say. Storing every bit wastes space, so store only the places of the 1s, as a sorted list of numbers, packed with the Elias-Fano method.

Then the questions about the row become questions about the list. The place of the tenth 1 is the tenth number in the list. The number of 1s before some place is the number of list entries below it, which is found by jumping to the right part of the list and looking at a few entries there. Whether a given bit is 1 is whether its place appears in the list.

## The abstract type

The structure answers the queries of the [rank and select problem](/rank-select-problem/) on a static bit vector: `build(B)`, `access(i)` for $0 \le i < n$, `rank1(i)` and `rank0(i)` for $0 \le i \le n$, `select1(j)` for $1 \le j \le m$ and `select0(j)` for $1 \le j \le n - m$. The rank counts the bits before position $i$, and select returns a 0-based position. It is meant for $m \ll n$; for a vector with few 0s, store the complement.

## Representation

Let $p_0 < p_1 < \cdots < p_{m-1}$ be the positions of the 1s, and let $\ell = \lfloor \lg(n/m) \rfloor$ if $m \ge 1$. The SD-array is the Elias-Fano code of this sequence with universe $n$:

- $Lo[j] = p_j \bmod 2^\ell$, in $m \ell$ bits;
- $H$, a bit vector of $m + \lfloor (n-1)/2^\ell \rfloor + 1$ bits with $H[\lfloor p_j / 2^\ell \rfloor + j] = 1$;
- a select index for the 1s and the 0s of $H$.

Bucket $h$ of $H$ holds the 1s of $B$ in positions $h 2^\ell$ to $(h+1) 2^\ell - 1$. Because the positions are distinct, a bucket holds at most $2^\ell \le n/m$ elements, and its low parts are strictly increasing. The invariant is that these fields encode the positions of the 1s; the structure is static.

## Operations

```pseudo id=main
SELECT1(j)                                   ▷ 1 ≤ j ≤ m
L1  return (SELECT1_H(j) − (j − 1)) · 2^ℓ + Lo[j − 1]

RANK1(i)                                     ▷ 0 ≤ i ≤ n
L2  if i = n then return m
L3  h ← ⌊i / 2^ℓ⌋, l ← i mod 2^ℓ
L4  p ← 0 if h = 0 else SELECT0_H(h) + 1          ▷ the start of bucket h
L5  s ← SELECT0_H(h + 1) − p                      ▷ the size of bucket h
L6  r ← p − h                                     ▷ the 1s in earlier buckets
L7  return r + |{t < s : Lo[r + t] < l}|          ▷ by binary search on Lo[r .. r + s − 1]

ACCESS(i)                                    ▷ 0 ≤ i < n
L8  r ← RANK1(i)
L9  return 1 if r < m and SELECT1(r + 1) = i else 0

SELECT0(j)                                   ▷ 1 ≤ j ≤ n − m
L10 return the least q with (q + 1) − RANK1(q + 1) ≥ j      ▷ binary search over q
```

**Select.** The $j$-th 1 of $B$ is the element $p_{j-1}$ of the sequence, and line L1 is the ACCESS of [Elias-Fano](/elias-fano-encoding/). One select on $H$: $O(1)$.

**Rank.** The 1s of $B$ before position $i$ are those in buckets less than $h$, counted by line L6, and those in bucket $h$ with a low part less than $l$, counted by line L7. Since $i < n$, $h \le \lfloor (n-1)/2^\ell \rfloor$, so the $(h+1)$-th 0 of $H$ exists and line L5 is defined. The bucket has $s \le 2^\ell$ elements, so the binary search takes $O(1 + \ell) = O(1 + \lg(n/m))$ steps. Then $\text{rank}_0(i) = i - \text{rank}_1(i)$.

**Access.** $B[i] = 1$ exactly when the next 1 at or after $i$ is at $i$. Line L8 finds how many 1s precede $i$, and line L9 checks whether the next one is at $i$.

**Select of the 0s.** The 0s are not stored, so $\text{select}_0$ is a binary search over $q$ on the nondecreasing function $\text{rank}_0(q + 1)$, in $O(\lg n)$ rank queries. When $\text{select}_0$ matters, store a second SD-array, or use a [rank/select dictionary](/rank-select-dictionary/).

## Example

Take $n = 64$ and the 1s at $3, 4, 7, 13, 14, 15, 21, 43$, so $m = 8$ and $\ell = \lfloor \lg 8 \rfloor = 3$. This is the sequence of the example on the [Elias-Fano](/elias-fano-encoding/) page, so $Lo = [3, 4, 7, 5, 6, 7, 5, 3]$ and $H = 1110\,1110\,1000\,1000$, with the 0s of $H$ at 3, 7, 9, 10, 11, 13, 14, 15. The SD-array takes $24 + 16 = 40$ bits, plus the select index, where the plain vector takes 64.

- SELECT1$(7)$: SELECT1$_H(7) = 8$, so $(8 - 6) \cdot 8 + Lo[6] = 16 + 5 = 21$.
- RANK1$(14)$: $h = 1$, $l = 6$. Bucket 1 starts at $p = 3 + 1 = 4$ and ends before the 0 at 7, so $s = 3$, and $r = 4 - 1 = 3$. In $Lo[3..5] = [5, 6, 7]$, one value is less than 6. The answer is $3 + 1 = 4$: the 1s at 3, 4, 7 and 13.
- RANK1$(40)$: $h = 5$, $l = 0$. The 5th 0 of $H$ is at 11, so $p = 12$, and the 6th 0 is at 13, so $s = 1$; $r = 12 - 5 = 7$. No low part is below 0, and the answer is 7.
- ACCESS$(21)$: RANK1$(21) = 6$ and SELECT1$(7) = 21$, so $B[21] = 1$. ACCESS$(22)$: RANK1$(22) = 7$ and SELECT1$(8) = 43 \ne 22$, so $B[22] = 0$.
- SELECT0$(10)$: the 0s of $B$ are at $0, 1, 2, 5, 6, 8, 9, 10, 11, 12, 16, \ldots$, and the least $q$ with $\text{rank}_0(q + 1) \ge 10$ is $q = 12$.

## Correctness

The fields are the Elias-Fano code of $p_0, \ldots, p_{m-1}$, so line L1 is the correct ACCESS of that code. In RANK1, the elements with high part less than $h$ are all less than $h 2^\ell \le i$, those with high part greater than $h$ are all at least $(h+1) 2^\ell > i$, and an element $h 2^\ell + Lo[t]$ of bucket $h$ is less than $i = h 2^\ell + l$ exactly when $Lo[t] < l$. ACCESS and SELECT0 follow from rank and select by their definitions. The full proof is in [the proof of correctness](proofs/correctness.md).

## Complexity

| operation | time, worst case |
|---|---|
| build | $O(n)$ from the plain vector, $O(m + n/2^\ell)$ from the list of 1s |
| select1 | $O(1)$ |
| rank, access | $O(1 + \lg(n/m))$ |
| select0 | $O(\lg n \cdot (1 + \lg(n/m)))$ |

**Space.** By the bound of [Elias-Fano](/elias-fano-encoding/) with $\ell = \lfloor \lg(n/m) \rfloor$, the low bits take $m \ell$ bits and $H$ fewer than $3m + 1$ bits; with $\ell = \lceil \lg(n/m) \rceil$ the total is at most $m \lceil \lg(n/m) \rceil + 2m + 1$. A select index on $H$ adds $o(m)$ bits. The minimum for a vector with $m$ ones is $\lg \binom{n}{m} \approx m \lg(n/m) + 1.44 m$ when $m \ll n$, so the SD-array is within about 2 bits for each 1 of the minimum, with no term that grows with $n$ beyond $\lg n$. The [RRR bit vector](/rrr-bitvector/) has redundancy $\Theta(n \lg \lg n / \lg n)$, so the SD-array is smaller roughly when $m \lg(n/m)$ is below $n \lg \lg n / \lg n$.

## Variants

- **Rank by scanning.** Okanohara and Sadakane, and Navarro, Section 4.4.2, compute rank by finding the end of bucket $h$ with select0 and scanning its low parts backward, which is fast because buckets are small on average.
- **Sampled select.** In place of a full select index on $H$, store every $q$-th position of a 1 and a 0 and scan from the sample, as in Vigna's forward pointers.
- **Both kinds of select.** Store an SD-array on $B$ and one on its complement, which doubles the space only when both kinds of bits are rare.
- **Hybrid.** Partitioned Elias-Fano and the hybrid bit vectors of practical libraries switch between an SD-array, a plain vector and RRR block by block.

## When to use it

Use an SD-array when a static bit vector has few 1s, roughly when fewer than one bit in ten is a 1, and the queries are mostly $\text{select}_1$ and rank: the sample marks of a [compressed suffix array](/compressed-suffix-array/), the document boundaries in [document listing](/document-listing/), or a sparse set given as a [fully indexable dictionary](/fully-indexable-dictionary/). For dense vectors use a [rank/select dictionary](/rank-select-dictionary/), and for vectors with runs or skew use the [RRR bit vector](/rrr-bitvector/).

## Pitfalls

- **Rank at $i = n$.** Line L2 is needed: for $i = n$, $h$ may exceed the last bucket, and the $(h+1)$-th 0 of $H$ does not exist.
- **Low bits are sorted only inside a bucket.** The binary search of line L7 must stay within $Lo[r .. r + s - 1]$; across buckets the low parts are not ordered.
- **$m = 0$.** Then $\lg(n/m)$ is undefined; set $\ell = 0$, return 0 for rank and 0 for access, and leave select1 undefined.
- **select0 is slow.** It is a binary search over rank, so code that uses $\text{select}_0$ heavily, such as tree navigation, should not use an SD-array for that vector.
- **Dense vectors.** For $m = n/2$, $\ell = 1$ and the SD-array uses about $1.5 n$ bits plus its index, worse than the plain vector.

## Implementations

## History

The split of a sorted list into high bits in unary and low bits in binary is due to Fano (1971) and Elias (1974). Okanohara and Sadakane presented four practical rank/select dictionaries at ALENEX 2007, among them the darray for dense vectors and the sdarray for sparse ones, which stores the Elias-Fano code of the positions of the 1s with select on its upper part. The name SD-array, or sd-vector, is used in later libraries for the same structure.

## References
