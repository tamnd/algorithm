---
tag: XGWQ3Q
kind: data-structure
slug: elias-fano-encoding
name: Elias-Fano encoding
aliases:
- Elias-Fano representation
- Elias-Fano coding
area: data-structures/succinct-structures
level: advanced
summary: A succinct representation of a monotone integer sequence that supports access and successor queries.
model: word-ram
complexity:
  vars: {n: the number of elements, u: the universe size, s: the number of elements in the bucket of the query}
  time: {access: O(1), next_geq: O(1 + s), build: O(n + u / 2^(log(u / n)))}
  space: {total: "n log(u / n) + 2 n + o(n)"}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 1974
  people: [Peter Elias, Robert M. Fano]
  note: Fano described the split into high and low bits in a 1971 MIT memo, and Elias published it in the Journal of the ACM in 1974; Vigna revived it for inverted indexes in 2013.
prereqs: [unary-coding, rank-select-dictionary]
see_also: [sd-array, fully-indexable-dictionary, predecessor-problem, inverted-index, rrr-bitvector, elias-gamma-coding, succinct-data-structures, prefix-sums]
sources:
  - paper: doi:10.1145/321812.321820
    title: Peter Elias, Efficient storage and retrieval by content and address of static files, Journal of the ACM 21(2), 1974, 246-260
    locator: the representation of a sorted list by its high bits in unary and its low bits in binary, and the bound of about 2 + lg(u/n) bits for each element
  - book: isbn:9781107152380
    title: Gonzalo Navarro, Compact Data Structures, A Practical Approach, Cambridge University Press, 2016
    locator: Chapter 3, Section 3.4.3 (Elias-Fano Codes), and Chapter 4, Section 4.4 (Very Sparse Bitvectors)
  - paper: doi:10.1145/2433396.2433409
    title: Sebastiano Vigna, Quasi-succinct indices, Sixth ACM International Conference on Web Search and Data Mining (WSDM 2013), 83-92
    locator: Section 3 (the Elias-Fano representation of monotone sequences, with skipping by forward pointers into the upper bits)
---

Elias-Fano encoding stores a nondecreasing sequence $x_0 \le x_1 \le \cdots \le x_{n-1}$ of integers from $\{0, \ldots, u-1\}$ in at most $n \lceil \lg(u/n) \rceil + 2n$ bits, and with a select index of $o(n)$ bits it returns any $x_i$ in $O(1)$ time on the [word RAM](/word-ram/) and the first element $\ge x$ in time proportional to one bucket. Each $x_i$ is split into $\ell = \lfloor \lg(u/n) \rfloor$ low bits, stored in plain form, and the remaining high bits, stored as gaps in [unary](/unary-coding/) in a bit vector of about $2n$ bits. The space is within 2 bits for each element of the [information-theoretic minimum](/information-theoretic-bound/) $\lg \binom{u}{n} \approx n \lg(u/n) + 1.44 n$. Fano and Elias described it in the 1970s; it is now the standard code for posting lists of [inverted indexes](/inverted-index/). The bit-vector interface built on it is the [SD-array](/sd-array/).

## In plain words

Take a sorted list of numbers. Each number is split into a top part and a bottom part. The bottom parts are written down as they are, all with the same small width. The top parts change slowly along the list, because the list is sorted, so they are written as a row of bits that says how many numbers have each top part: a 1 for each number, and a 0 each time the top part goes up by one.

To read the tenth number, find the tenth 1 in that row. The count of 0s before it is the top part, and the bottom part is the tenth entry of the plain list.

To find the first number that is at least some value, use its top part to jump to the right place in the row, then check the few numbers that share that top part.

## The abstract type

The structure stores a static nondecreasing sequence $X = x_0, \ldots, x_{n-1}$ with $0 \le x_i < u$ and answers:

- `access(i)`: return $x_i$, for $0 \le i < n$;
- `next_geq(x)`: return the smallest $i$ with $x_i \ge x$, or $n$ if there is none, for $0 \le x < u$.

From these, the [predecessor and successor queries](/predecessor-problem/) follow: the successor of $x$ is $x_i$ for $i = $ `next_geq`$(x)$, and the number of elements less than $x$ is that same $i$. When the $x_i$ are the positions of the 1s of a bit vector, `access` is $\text{select}_1$ and `next_geq` is $\text{rank}_1$, which is the [SD-array](/sd-array/).

## Representation

Let $\ell = \lfloor \lg(u/n) \rfloor$ if $u \ge n$, and $\ell = 0$ otherwise. For each $i$, write $x_i = h_i 2^\ell + l_i$ with $0 \le l_i < 2^\ell$; $h_i$ is the *high part* and $l_i$ the *low part*.

- **Low bits.** An array $Lo[0 \ldots n-1]$ of $\ell$-bit fields, $Lo[i] = l_i$, packed in $n \ell$ bits.
- **High bits.** A bit vector $H$ of $n + \lfloor (u-1) / 2^\ell \rfloor + 1$ bits with $H[h_i + i] = 1$ for each $i$ and 0 elsewhere. Read from the left, $H$ is the [unary code](/unary-coding/) of the gaps $h_0, h_1 - h_0, h_2 - h_1, \ldots$: before the $(i+1)$-th 1 there are exactly $h_i$ zeros.
- **Select index.** $\text{select}_1$ and $\text{select}_0$ on $H$, as in the [rank/select dictionary](/rank-select-dictionary/), in $o(n)$ bits.

The *bucket* $h$ is the run of 1s of $H$ between the $h$-th and the $(h+1)$-th 0; it holds the elements with high part $h$. The invariant is that $H$ and $Lo$ are as defined; the structure is static.

## Operations

```pseudo id=main
BUILD(x[0 .. n − 1], u)                      ▷ nondecreasing, 0 ≤ x[i] < u
L1  ℓ ← ⌊lg(u / n)⌋ if u ≥ n else 0
L2  for i ← 0 to n − 1 do
L3      Lo[i] ← x[i] mod 2^ℓ
L4      H[⌊x[i] / 2^ℓ⌋ + i] ← 1                ▷ all other bits of H are 0

ACCESS(i)                                    ▷ 0 ≤ i < n
L5  return (SELECT1_H(i + 1) − i) · 2^ℓ + Lo[i]

NEXT-GEQ(x)                                  ▷ 0 ≤ x < u
L6  h ← ⌊x / 2^ℓ⌋
L7  p ← 0 if h = 0 else SELECT0_H(h) + 1         ▷ the start of bucket h in H
L8  i ← p − h                                    ▷ the number of elements with high part < h
L9  while i < n and ACCESS(i) < x do i ← i + 1
L10 return i
```

**Build.** Lines L2 to L4 fill $Lo$ and set one bit of $H$ for each element, in $O(n)$ time after $H$ is cleared, and then the select index of $H$ is built in time linear in its length.

**Access.** The $(i+1)$-th 1 of $H$ is at position $h_i + i$, so line L5 recovers $h_i$ by subtracting $i$ and appends the low bits. One select and one read: $O(1)$.

**Next-geq.** Every element with high part less than $h$ is less than $x$, and every element with high part greater than $h$ is greater than $x$. Line L7 finds the start of bucket $h$, the position just after the $h$-th 0, and line L8 counts the 1s before it. Line L9 then walks inside bucket $h$; it stops at the first element $\ge x$, or after the bucket, where the next element has a higher high part and so is $> x$. The time is $O(1 + s)$ for a bucket of $s$ elements. The number of buckets is at least $u / 2^\ell \ge n$, so the average bucket holds at most one element; a binary search over the low bits inside the bucket gives $O(1 + \lg s)$ in the worst case.

## Example

Take $X = 3, 4, 7, 13, 14, 15, 21, 43$ with $u = 64$ and $n = 8$. Then $\ell = \lfloor \lg 8 \rfloor = 3$.

| $i$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| $x_i$ | 3 | 4 | 7 | 13 | 14 | 15 | 21 | 43 |
| $h_i = \lfloor x_i / 8 \rfloor$ | 0 | 0 | 0 | 1 | 1 | 1 | 2 | 5 |
| $l_i = x_i \bmod 8$ | 3 | 4 | 7 | 5 | 6 | 7 | 5 | 3 |
| $h_i + i$ | 0 | 1 | 2 | 4 | 5 | 6 | 8 | 12 |

$H$ has $8 + \lfloor 63/8 \rfloor + 1 = 16$ bits, $H = 1110\,1110\,1000\,1000$, with the 0s at 3, 7, 9, 10, 11, 13, 14, 15. The buckets are $\{3, 4, 7\}$, $\{13, 14, 15\}$, $\{21\}$, empty, empty, $\{43\}$, empty, empty. The low bits take $8 \cdot 3 = 24$ bits, so the total is 40 bits, while 8 plain 6-bit numbers take 48 and $\lg \binom{64}{8} \approx 32.0$.

- ACCESS$(6)$: SELECT1$_H(7) = 8$, so $h_6 = 8 - 6 = 2$, and $x_6 = 2 \cdot 8 + 5 = 21$.
- ACCESS$(7)$: SELECT1$_H(8) = 12$, $h_7 = 5$, $x_7 = 40 + 3 = 43$.
- NEXT-GEQ$(14)$: $h = 1$, SELECT0$_H(1) = 3$, so $p = 4$ and $i = 3$. ACCESS$(3) = 13 < 14$, then ACCESS$(4) = 14$, so the answer is $4$.
- NEXT-GEQ$(30)$: $h = 3$, SELECT0$_H(3) = 9$, $p = 10$, $i = 7$. ACCESS$(7) = 43 \ge 30$, so the answer is 7: bucket 3 is empty and the walk stops at once.

## Correctness

Since the $x_i$ are nondecreasing, so are the $h_i$, and the positions $h_i + i$ are strictly increasing; so the $(i+1)$-th 1 of $H$ is at $h_i + i$, with exactly $h_i$ zeros before it. This gives ACCESS. For NEXT-GEQ, the number of 1s before the $h$-th 0 is the number of elements with high part less than $h$, and the walk of line L9 stays in a part of $X$ where the answer must lie. The full proof is in [the proof of correctness](proofs/correctness.md).

## Complexity

| operation | time, worst case |
|---|---|
| build | $O(n + u / 2^\ell)$, which is $O(n)$ when $u \ge n$ |
| access | $O(1)$ |
| next_geq | $O(1 + s)$ for a bucket of $s$ elements; $O(1 + \lg s)$ with binary search |

**Space.** The low bits take $n \ell$ bits. $H$ has $n$ ones and $\lfloor (u-1)/2^\ell \rfloor + 1 \le u / 2^\ell + 1$ zeros. If $u \ge n$, then $2^\ell > u / (2n)$, so $u / 2^\ell < 2n$, and the total is less than $n \lfloor \lg(u/n) \rfloor + 3n + 1$ bits; with $\ell = \lceil \lg(u/n) \rceil$ the zeros number at most $n + 1$, which gives Elias's bound of $n \lceil \lg(u/n) \rceil + 2n + 1$. The select index on $H$ adds $o(n)$ bits. When $n$ is much smaller than $u$, $\lg \binom{u}{n}$ is about $n \lg(u/n) + n \lg e$, with $\lg e \approx 1.44$, so Elias-Fano is within about 2 bits for each element of the minimum.

## Variants

- **Choice of $\ell$.** Elias used $\lceil \lg(u/n) \rceil$; most practical codes use $\lfloor \lg(u/n) \rfloor$. Lowering $\ell$ by one saves $n$ low bits and adds at most about $u / 2^{\ell+1} \le n$ zeros to $H$, so the floor is never worse up to rounding.
- **Forward pointers and skips.** Vigna's quasi-succinct indices store, for every $q$-th 0 and every $q$-th 1 of $H$, its position, in place of a full select index; ACCESS and NEXT-GEQ jump to the nearest sample and scan. This is the form used in search engines.
- **Partitioned Elias-Fano.** Ottaviano and Venturini cut the sequence into chunks and choose for each chunk the best of Elias-Fano, a plain bit vector, or an implicit run, which adapts to clusters in the data.
- **Strictly increasing sequences.** For a set, $x_i - i$ is nondecreasing and smaller, so encoding $x_i - i$ with universe $u - n$ saves space; this is the multiset view.
- **Prefix sums.** A sequence of nonnegative integers $a_j$ is stored as the Elias-Fano code of its [prefix sums](/prefix-sums/), which gives any prefix sum in $O(1)$ time and any $a_j$ as a difference.
- **Bit vector interface.** The [SD-array](/sd-array/) uses the positions of the 1s as $X$ and adds $\text{rank}$ and $\text{select}_0$.

## When to use it

Use Elias-Fano for a static sorted list of integers that must stay compressed and still allow random access and skipping: posting lists in an [inverted index](/inverted-index/), the offsets of variable-length records, the adjacency lists of a large graph, or the pointers of a [LOUDS trie](/louds-trie/). It suits lists whose gaps are irregular. If the gaps are very small and regular, a [rank/select dictionary](/rank-select-dictionary/) on the characteristic vector is smaller; if only sequential decoding is needed, a gap code such as [Elias gamma](/elias-gamma-coding/) may be smaller.

## Pitfalls

- **$\ell$ when $u < n$.** For a multiset with more elements than the universe, $\lg(u/n)$ is negative; $\ell$ must be 0, and then $H$ has more 1s than 0s.
- **Size of $H$.** $H$ needs $n + \lfloor (u-1)/2^\ell \rfloor + 1$ bits, not $2n$; with the floor in $\ell$, the number of zeros can be up to almost $2n$.
- **The start of bucket 0.** SELECT0$_H(0)$ is not defined; bucket 0 starts at position 0, which line L7 handles as a special case.
- **Walking past the bucket.** The walk in line L9 may leave bucket $h$; this is correct, because the next element is then larger than $x$, but code that compares only low bits must stop at the end of the bucket, where the high part changes.
- **Duplicates.** A nondecreasing sequence may repeat values; ACCESS and NEXT-GEQ handle this, but a set interface must use the strictly increasing transform or report multiplicities.

## Implementations

## History

Robert Fano described the split of each key into a high part in unary and a low part in binary in a 1971 memo of MIT Project MAC on the number of bits needed for an associative memory. Peter Elias published the scheme and its analysis in the Journal of the ACM in 1974. The method was rediscovered several times and became central to succinct data structures through the sparse arrays of Okanohara and Sadakane (2007). Vigna's quasi-succinct indices (2013) made it the standard code for posting lists, and Ottaviano and Venturini's partitioned variant (2014) improved its compression on clustered data.

## References
