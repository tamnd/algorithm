---
tag: PZGBBJ
kind: algorithm
slug: bit-sampling-lsh
name: Bit-sampling LSH
aliases:
- Hamming LSH
- Indyk-Motwani LSH
area: searching/similarity-search
level: core
summary: LSH for Hamming distance that hashes on randomly chosen bit positions.
solves: [approximate-nearest-neighbor-search]
model: real-ram
complexity:
  vars: {n: the number of points, d: the number of bits of a point, k: the number of sampled bits in a key, L: the number of tables, c: the approximation factor}
  time: {build: O(n L k), query: O(L k + L d)}
  space: {total: O(n L + n d)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: false, comparison: false, recursive: false}
history:
  year: 1998
  people: [Piotr Indyk, Rajeev Motwani]
  note: Indyk and Motwani gave bit sampling as the first locality-sensitive family, for the Hamming cube, at STOC 1998; Gionis, Indyk and Motwani tested it on real data in 1999.
prereqs: [hamming-distance, locality-sensitive-hashing]
see_also: [locality-sensitive-hash-family, lsh-amplification, simhash, minhash, multi-probe-lsh, approximate-nearest-neighbor-search, brute-force-nearest-neighbor-search]
sources:
  - paper: doi:10.1145/276698.276876
    title: Piotr Indyk and Rajeev Motwani, Approximate nearest neighbors, towards removing the curse of dimensionality, Proceedings of the 30th ACM Symposium on Theory of Computing (STOC), 1998
    locator: pages 604 to 613 (the bit-sampling family for the Hamming cube and the exponent 1/c)
  - paper: doi:10.4086/toc.2012.v008a014
    title: Sariel Har-Peled, Piotr Indyk and Rajeev Motwani, Approximate nearest neighbor, towards removing the curse of dimensionality, Theory of Computing 8, 2012
    locator: Section 3 (the LSH data structure and the bit-sampling family for the Hamming distance)
  - url: https://www.vldb.org/conf/1999/P49.pdf
    title: Aristides Gionis, Piotr Indyk and Rajeev Motwani, Similarity search in high dimensions via hashing, Proceedings of the 25th VLDB Conference, 1999
    locator: pages 518 to 529 (bit sampling on unary-coded vectors, and experiments)
  - book: isbn:9781107077232
    title: Jure Leskovec, Anand Rajaraman and Jeffrey D. Ullman, Mining of Massive Datasets, second edition, Cambridge University Press, 2014
    locator: Chapter 3, Section 3.7 (LSH families for the Hamming distance)
---

Bit-sampling LSH is [locality-sensitive hashing](/locality-sensitive-hashing/) for the [Hamming distance](/hamming-distance/) on strings of $d$ bits: each hash function returns the bit of a point at one random position. Two strings at Hamming distance $H$ agree on a random position with probability exactly $1 - H/d$, so the family is $(r, cr, 1 - r/d, 1 - cr/d)$-sensitive with exponent $\rho \le 1/c$. With $L = O(n^{1/c})$ tables, a query computes $O(n^{1/c})$ distances and finds a point within $cr$ with probability at least $2/3 - 1/e > 0.29$ when a point within $r$ exists. Indyk and Motwani gave it in 1998 as the first [locality-sensitive hash family](/locality-sensitive-hash-family/).

## In plain words

Each data item is a row of bits. To hash a row, look at a few bit places picked at random and write down the bits there. Two rows that differ in few places will usually show the same bits at the picked places, so they get the same bucket. Two rows that differ in many places will usually show some different bit.

Build several tables, each with its own random places. To answer a query, look up its bucket in each table and check the rows found there, one by one, until one is close enough or a fixed number of rows has been checked.

## The problem

The input is a set $P$ of $n$ strings in $\{0, 1\}^d$ under the Hamming distance $H$, a radius $r \ge 0$ and a factor $c > 1$ with $c r < d$. A query $q$ must get a string within $c r$ if some string is within $r$, and must never get a string beyond $c r$. This is the randomized $(c, r)$-near neighbor problem of [c-approximate nearest neighbor](/c-approximate-nearest-neighbor/); a search over radii turns it into [approximate nearest neighbor search](/approximate-nearest-neighbor-search/).

## The algorithm

```pseudo id=main
BIT-SAMPLING-BUILD(P, d, k, L)
L1  for j ← 1 to L do
L2      draw positions i_{j,1}, …, i_{j,k} independently and uniformly from {0, …, d−1}
L3      T_j ← a hash table that stores each x ∈ P under the key (x[i_{j,1}], …, x[i_{j,k}])

BIT-SAMPLING-QUERY(q, c, r)
L4  count ← 0
L5  for j ← 1 to L, and for each x in the bucket of (q[i_{j,1}], …, q[i_{j,k}]) in T_j do
L6      count ← count + 1; if H(q, x) ≤ c r then return x
L7      if count ≥ 3L then return none
L8  return none
```

Line L2 draws the positions with replacement, so the $k$ functions of a key are independent. The key of line L3 is the string of $k$ sampled bits, which fits in one machine word when $k \le 64$. Line L6 computes $H(q, x)$ as the number of ones in $q \oplus x$, which takes $O(d / w)$ word operations with a popcount instruction on $w$-bit words. Line L7 is the stop rule of [locality-sensitive hashing](/locality-sensitive-hashing/): at most $3L$ distances per query.

**The parameters.** With $p_1 = 1 - r/d$ and $p_2 = 1 - cr/d$, set $k = \lceil \ln n / \ln(1/p_2) \rceil$ and $L = \lceil n^\rho / p_1 \rceil$, where $\rho = \ln(1/p_1)/\ln(1/p_2)$.

## Example

Take the six strings of 8 bits of the [LSH page](/locality-sensitive-hashing/), with positions numbered 0 to 7 from the left, the query $q = 10110001$, $c = 2$, $k = 3$ and $L = 2$. The draws are the positions $(0, 2, 5)$ for table 1 and $(4, 6, 7)$ for table 2.

| $i$ | $P[i]$ | $H(q, P[i])$ | key 1: bits 0, 2, 5 | key 2: bits 4, 6, 7 |
|---|---|---|---|---|
| 0 | 00010111 | 4 | 001 | 011 |
| 1 | 11100000 | 3 | 110 | 000 |
| 2 | 11010010 | 4 | 100 | 010 |
| 3 | 01011011 | 5 | 000 | 111 |
| 4 | 00111100 | 4 | 011 | 100 |
| 5 | 10110100 | 2 | 111 | 000 |
| $q$ | 10110001 | | 110 | 001 |

The bucket of $q$ in table 1 holds only point 1, and its bucket in table 2 is empty.

- With $r = 2$, so $cr = 4$: the query checks point 1 (count 1, $H = 3 \le 4$) and returns it. Point 5 at distance 2 is the true nearest neighbor, but the query is correct, since $3 \le cr$.
- With $r = 1$, so $cr = 2$: point 1 fails the test, table 2 gives nothing, and the query returns none. This is correct, since no string is within $r = 1$. Point 5 at distance 2 would be a valid answer here, but it did not collide with $q$; the guarantee only covers points within $r$.

## Correctness

A returned string passed the test of line L6, so it is within $c r$. The rest of the proof is the bit-sampling lemma below plus the theorem of [locality-sensitive hashing](/locality-sensitive-hashing/).

**Lemma 1 (collision probability).** For a uniform random position $i$ and strings $x, y \in \{0,1\}^d$, $\Pr[x[i] = y[i]] = 1 - H(x, y)/d$. So the family $\{x \mapsto x[i]\}$ is $(r, cr, 1 - r/d, 1 - cr/d)$-sensitive.

*Proof.* Exactly $d - H(x, y)$ of the $d$ positions have equal bits. The probability is decreasing in $H$, which gives the two bounds of the definition.

**Lemma 2 (exponent).** If $c \ge 1$ and $0 < cr < d$, then $\rho = \dfrac{\ln(1 - r/d)}{\ln(1 - cr/d)} \le \dfrac{1}{c}$.

*Proof.* Let $x = r/d$, so $0 < cx < 1$. By Bernoulli's inequality $(1 - x)^c \ge 1 - cx$ for $c \ge 1$ and $x \le 1$. Take logarithms: $c \ln(1 - x) \ge \ln(1 - cx)$. Both logarithms are negative, so dividing by $c \ln(1 - cx) < 0$ reverses the order and gives $\ln(1-x)/\ln(1-cx) \le 1/c$.

**Theorem.** With $k$ and $L$ as above and a fixed query $q$ that has a string within $r$, BIT-SAMPLING-QUERY returns a string within $c r$ with probability at least $2/3 - 1/e > 0.29$ over the draws of line L2.

This is the LSH theorem applied to the family of Lemma 1. The full proof is in `proofs/correctness.md`.

For $d = 64$ and $r = 4$, $\rho = 0.6556$ for $c = 1.5$, $0.4833$ for $c = 2$, and $0.3108$ for $c = 3$; each is below $1/c$.

## Complexity

The model is the [real RAM](/real-ram/) with hash tables of $O(1)$ expected time per operation, and with the strings stored as bit arrays.

- **Build.** $nLk$ bit reads and $nL$ table insertions: $O(nLk)$ expected time.
- **Space.** $O(nL)$ table entries plus $O(nd)$ bits for the strings. With the parameters above, $L = O(n^{1/c} / p_1)$, so the space is $O(n^{1 + 1/c} + nd)$ words when $r \le d/2$.
- **Query.** $Lk$ bit reads for the keys and at most $3L$ Hamming distances of $O(d)$ time each: $O(Lk + Ld) = O(n^{1/c}(\log n + d))$ time for constant $c$ and $r \le d/2$, against $O(nd)$ for a scan.
- **Failure probability.** At most $1/3 + 1/e < 0.71$ per query; $t$ independent copies reduce it to $0.71^t$.

## Properties

- **One-sided error.** A returned string is always within $cr$; the only error is a "none" when a string within $r$ exists.
- **Exact collision probability.** Lemma 1 holds with equality, so the ratio $\rho$ is known exactly, not only bounded.
- **Optimal for the Hamming cube up to constants.** O'Donnell, Wu and Zhou showed that every LSH family for the Hamming distance has $\rho \ge 1/c - o(1)$ (see [locality-sensitive hash family](/locality-sensitive-hash-family/)), so bit sampling is the best possible data-independent family there.
- **Dynamic.** Inserting or deleting a string costs $L$ table operations.

## Variants and improvements

- **Other metrics through embeddings.** Gionis, Indyk and Motwani map integer vectors in $\{0, \dots, C\}^d$ to $\{0,1\}^{Cd}$ by unary coding, which turns the $\ell_1$ distance into the Hamming distance; sampling a bit of the unary code is the same as testing whether one coordinate is at least a random threshold.
- **Banding.** In practice $k$ and $L$ are set from the S-curve $1 - (1 - p^k)^L$ of [LSH amplification](/lsh-amplification/), not from the worst-case formulas.
- **Multi-probe.** [Multi-probe LSH](/multi-probe-lsh/) also probes keys that differ from the query key in one or two bits, which cuts the number of tables.
- **SimHash.** For angles, [SimHash](/simhash/) first maps vectors to bit strings whose Hamming distance tracks the angle, and bit sampling then indexes those strings.

## When to use it

Use bit sampling for binary codes, fingerprints and sets coded as bit vectors when the near radius $r$ is a known fraction of $d$, for example near-duplicate fingerprints at distance at most 3 out of 64. When $r/d$ is very small, $p_1$ is close to 1 and few tables are needed. For Jaccard distance on sparse sets, use [MinHash](/minhash/): its collision probability depends on the sets and not on $d$, while bit sampling on indicator vectors sees almost only zeros.

## Pitfalls

- **Sampling without replacement.** Drawing the $k$ positions of a key without replacement changes the collision probability to a hypergeometric one; the analysis above then needs a new proof. It is usually a little better in practice, but do not reuse the formulas blindly.
- **Same positions in all tables.** Each table needs its own draw; equal positions make the tables copies.
- **Very sparse data.** If every string has few ones, two unrelated strings agree on most positions, so $p_2$ is close to 1 and $k$ must be very large.
- **Using $r$ near $d/c$.** As $cr \to d$, $p_2 \to 0$ and the formulas break; the method needs $cr < d$.

## Implementations

## History

Indyk and Motwani introduced locality-sensitive families at STOC 1998 and used bit sampling on the Hamming cube to get the first query time of about $n^{1/c}$ for the $(c, r)$-near neighbor problem, with space polynomial in $n$ and $d$. Gionis, Indyk and Motwani applied it to image and text data at VLDB 1999, with unary coding for $\ell_1$, and found it faster than tree indexes in high dimension. Har-Peled, Indyk and Motwani gave the full analysis in the journal version in 2012.

## References
