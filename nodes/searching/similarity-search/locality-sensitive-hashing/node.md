---
tag: XTR0CK
kind: algorithm
slug: locality-sensitive-hashing
name: Locality-sensitive hashing
aliases:
- LSH
area: searching/similarity-search
level: core
summary: Approximate nearest neighbor search by hashing points into buckets with an LSH family and checking only colliding points.
solves: [approximate-nearest-neighbor-search]
model: real-ram
complexity:
  vars: {n: the number of points, d: the time to compute one distance, τ: the time to evaluate one hash function, k: the number of functions in a key, L: the number of tables, ρ: the exponent ln(1/p1)/ln(1/p2)}
  time: {build: O(n L k τ), query: O(L k τ + L d)}
  space: {total: O(n L)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: false, comparison: false, recursive: false}
history:
  year: 1998
  people: [Piotr Indyk, Rajeev Motwani]
  note: Indyk and Motwani introduced locality-sensitive families and the hashing scheme for approximate nearest neighbors at STOC 1998; Gionis, Indyk and Motwani gave the practical version for the Hamming space in 1999.
prereqs: [locality-sensitive-hash-family, lsh-amplification, c-approximate-nearest-neighbor]
see_also: [approximate-nearest-neighbor-search, bit-sampling-lsh, minhash, random-hyperplane-lsh, e2lsh, multi-probe-lsh, lsh-forest, markov-inequality]
sources:
  - paper: doi:10.1145/276698.276876
    title: Piotr Indyk and Rajeev Motwani, Approximate nearest neighbors, towards removing the curse of dimensionality, Proceedings of the 30th ACM Symposium on Theory of Computing (STOC), 1998
    locator: pages 604 to 613 (locality-sensitive families, and the hashing scheme with n^(1+1/c) space and n^(1/c) query time for the Hamming cube)
  - paper: doi:10.4086/toc.2012.v008a014
    title: Sariel Har-Peled, Piotr Indyk and Rajeev Motwani, Approximate nearest neighbor, towards removing the curse of dimensionality, Theory of Computing 8, 2012
    locator: Section 3 (the LSH data structure, the choice of k and L, and the proof that it answers the randomized (c, r)-near neighbor problem with constant probability)
  - paper: doi:10.1145/1327452.1327494
    title: Alexandr Andoni and Piotr Indyk, Near-optimal hashing algorithms for approximate nearest neighbor in high dimensions, Communications of the ACM 51(1), 2008
    locator: pages 117 to 122 (the algorithm with k concatenated functions and L tables, the stop after a bounded number of points, the constant success probability, and the history of the exponents)
  - url: https://www.vldb.org/conf/1999/P49.pdf
    title: Aristides Gionis, Piotr Indyk and Rajeev Motwani, Similarity search in high dimensions via hashing, Proceedings of the 25th VLDB Conference, 1999
    locator: pages 518 to 529 (LSH for the Hamming space with bit sampling, and experiments against tree indexes)
  - paper: doi:10.1145/509907.509965
    title: Moses S. Charikar, Similarity estimation techniques from rounding algorithms, STOC 2002
    locator: Section 3 (the random hyperplane family)
  - paper: doi:10.1145/997817.997857
    title: Mayur Datar, Nicole Immorlica, Piotr Indyk and Vahab S. Mirrokni, Locality-sensitive hashing scheme based on p-stable distributions, Proceedings of the 20th ACM Symposium on Computational Geometry (SoCG), 2004
    locator: pages 253 to 262 (the family of quantized projections for ℓp)
  - book: isbn:9781107077232
    title: Jure Leskovec, Anand Rajaraman and Jeffrey D. Ullman, Mining of Massive Datasets, second edition, Cambridge University Press, 2014
    locator: Chapter 3, Sections 3.4 to 3.7 (LSH with banding, the theory of locality-sensitive functions, and the families for other distances)
---

Locality-sensitive hashing (LSH) solves the [$(c, r)$-near neighbor](/c-approximate-nearest-neighbor/) problem by hashing the $n$ points into $L$ hash tables with keys made of $k$ functions of a [locality-sensitive hash family](/locality-sensitive-hash-family/), and by checking only the points that share a bucket with the query. With $k = \lceil \log_{1/p_2} n \rceil$ and $L = \lceil n^\rho / p_1 \rceil$, a query evaluates $O(n^\rho \log n)$ hash functions and computes at most $3L$ distances, and it finds a point within $c r$ with probability at least $2/3 - 1/e \approx 0.30$ whenever a point within $r$ exists. Here $\rho = \ln(1/p_1)/\ln(1/p_2) < 1$, for example $\rho \le 1/c$ for the Hamming distance. Indyk and Motwani introduced it in 1998, and it was the first method with a query time sublinear in $n$ and polynomial in the dimension for [approximate nearest neighbor search](/approximate-nearest-neighbor-search/).

## In plain words

Put each point into buckets with a special kind of hash: points that are close to each other tend to get the same bucket, and points far apart tend to get different buckets. Then, to find a point close to a query, hash the query and look only in its bucket.

One such hash makes many mistakes. So a key is made from several hashes at once, which keeps out most far points, and several tables are built with different random keys, so that a close point lands with the query in at least one of them.

At query time, look through the query's buckets in all tables. Stop as soon as you find a point close enough, or when you have looked at a fixed number of points.

## The problem

The input is a set $P$ of $n$ points in a metric space $(M, \delta)$, a radius $r > 0$ and a factor $c > 1$, and an $(r, c r, p_1, p_2)$-sensitive family $\mathcal{H}$. A query $q$ must get a point of $P$ within $c r$ if some point is within $r$. The answer is never a point beyond $c r$. The method is randomized: the guarantee holds for each fixed query with a probability over the random functions chosen at build time. This is the randomized $(c, r)$-near neighbor problem; the [proposition on the definition page](/c-approximate-nearest-neighbor/) turns it into a $c(1+\varepsilon)$-approximate nearest neighbor search.

## The algorithm

```pseudo id=main
LSH-BUILD(P, ℋ, k, L)
L1  for j ← 1 to L do
L2      draw h_{j,1}, …, h_{j,k} independently from ℋ
L3      g_j(x) ← (h_{j,1}(x), …, h_{j,k}(x))
L4      T_j ← a hash table that stores each x ∈ P under the key g_j(x)

LSH-QUERY(q, c, r)
L5  count ← 0
L6  for j ← 1 to L do
L7      for each x in the bucket T_j[g_j(q)] do
L8          count ← count + 1
L9          if δ(q, x) ≤ c r then return x
L10         if count ≥ 3L then return none
L11 return none
```

Lines L1 to L4 are the AND and OR of [LSH amplification](/lsh-amplification/): a key is a tuple of $k$ values, and there are $L$ independent tables. Each table is an ordinary [hash table](/hash-table/) on the tuples, so a bucket is found in $O(k)$ expected time after the $k$ functions are evaluated.

A query walks the buckets of $q$ in the $L$ tables. Line L9 returns the first point within $c r$, so the answer is never far. Line L10 bounds the work: the query computes at most $3L$ distances, even if a bucket is large. Line L11 is reached when all buckets are exhausted.

**The parameters.** Set $k = \lceil \log_{1/p_2} n \rceil$ and $L = \lceil n^{\rho} / p_1 \rceil$. Then the expected number of far points in the bucket of $q$ is at most 1 for each table, and a near point shares a bucket with $q$ in some table with probability at least $1 - 1/e$.

## Example

Let $P$ be six strings of 8 bits under the [Hamming distance](/hamming-distance/), with the query $q = 10110001$, $r = 1$ and $c = 2$, so $c r = 2$. Bit sampling picks one bit position for each function. Here $k = 2$ and $L = 3$, and the draws are the positions $(0, 3)$, $(1, 6)$ and $(2, 7)$.

| $i$ | $P[i]$ | $H(q, P[i])$ | key 1: bits 0, 3 | key 2: bits 1, 6 | key 3: bits 2, 7 |
|---|---|---|---|---|---|
| 0 | 00010111 | 4 | 01 | 01 | 01 |
| 1 | 11100000 | 3 | 10 | 10 | 10 |
| 2 | 11010010 | 4 | 11 | 11 | 00 |
| 3 | 01011011 | 5 | 01 | 11 | 01 |
| 4 | 00111100 | 4 | 01 | 00 | 10 |
| 5 | 10110100 | 2 | 11 | 00 | 10 |
| $q$ | 10110001 | | 11 | 00 | 11 |

The query keys are 11, 00 and 11. The bucket of $q$ in table 1 is $[2, 5]$. The query checks point 2 (count 1, distance $4 > 2$), then point 5 (count 2, distance $2 \le 2$), and returns point 5. With $c r = 1$ instead, the query checks points 2 and 5 in table 1 and points 4 and 5 in table 2, finds the bucket of table 3 empty, and returns none after 4 distance computations; this is correct, since no point is within $r = 1$.

## Correctness

A returned point passed line L9, so it is within $c r$. In particular, if no point is within $c r$, the query returns none, which is correct. The other case needs probability.

**Theorem.** Let $\mathcal{H}$ be $(r, c r, p_1, p_2)$-sensitive with $0 < p_2 < p_1$, let $n \ge 1$, $k = \lceil \log_{1/p_2} n \rceil$ and $L = \lceil n^\rho / p_1 \rceil$. For each fixed $q$ such that some $p^* \in P$ has $\delta(q, p^*) \le r$, LSH-QUERY returns a point within $c r$ with probability at least $1 - 1/e - 1/3 > 0.29$ over the draws of line L2.

The proof uses two events. $E_1$: $p^*$ shares a bucket with $q$ in some table; its probability is at least $1 - (1 - p_1^k)^L \ge 1 - 1/e$. $E_2$: fewer than $3L$ entries of the $L$ buckets of $q$ are points beyond $c r$; their expected number is at most $L \cdot n \cdot p_2^k \le L$, so by [Markov's inequality](/markov-inequality/) $E_2$ fails with probability at most $1/3$. When both hold, the scan meets a point within $c r$ before line L10 can stop it. The full proof is in `proofs/correctness.md`.

To lower the failure probability to $f$, build $\lceil \ln(1/f) / \ln(1/0.71) \rceil$ independent copies and query each; all copies fail with probability at most $0.71^{t} \le f$.

## Complexity

The model is the [real RAM](/real-ram/) with hash tables of $O(1)$ expected time per operation; $\tau$ is the time to evaluate one function of $\mathcal{H}$ and $d$ the time to compute $\delta$.

- **Build.** Each of the $n$ points gets $L$ keys of $k$ values: $O(n L k \tau)$ time, and $O(nL)$ expected time for the table operations.
- **Space.** Each table stores one entry per point: $O(nL)$ words besides the points. With the parameters above this is $O(n^{1+\rho} / p_1)$.
- **Query.** $Lk$ hash evaluations and at most $3L$ distance computations (line L10): $O(L k \tau + L d)$ time in the worst case over the draws. With the parameters above this is $O\big(\tfrac{n^\rho}{p_1} (\tau \log_{1/p_2} n + d)\big)$.
- **Example of the exponent.** For bit sampling in $\{0, 1\}^D$, $\tau = O(1)$ and $\rho \le 1/c$, so the query takes $O(n^{1/c}(\log n + D))$ time and the space is $O(n^{1 + 1/c} + nD)$. For $c = 2$ this is about $\sqrt n$ distance computations, against $n$ for a scan.

## Properties

- **One-sided error.** A returned point is always valid. The only error is a "none" when a near point exists.
- **Randomized, per query.** The bound holds for each fixed query. An adversary who sees the tables can choose queries that fail.
- **Static.** Inserting a point costs $L$ table insertions; deletion is the same. The parameters depend on $n$, so a large growth of $n$ calls for a rebuild.
- **Distance-agnostic.** The same code works for any distance that has a sensitive family; only line L2 changes.

## Variants and improvements

- **Families.** [Bit sampling](/bit-sampling-lsh/) for Hamming, [MinHash](/minhash/) for Jaccard, [random hyperplanes](/random-hyperplane-lsh/) for the angle, [E2LSH](/e2lsh/) for $\ell_2$ and $\ell_1$, and [asymmetric LSH](/asymmetric-lsh/) for inner products.
- **Multi-probe LSH.** [Multi-probe LSH](/multi-probe-lsh/) also checks buckets near the query's bucket, so that far fewer tables reach the same recall.
- **LSH forest.** [LSH forest](/lsh-forest/) replaces the fixed $k$ by prefix trees, which adapts to the distance of the nearest neighbor and handles many radii at once.
- **k nearest neighbors.** Collect all candidates of the $L$ buckets, compute their distances, and keep the $k$ best with a heap. This drops the bound of line L10 and is the usual use in practice.
- **Better exponents.** Data-independent families cannot beat $\rho = 1/c^2 - o(1)$ for $\ell_2$; data-dependent hashing, which first splits the data set into clusters, reaches smaller exponents.

## When to use it

Use LSH for high-dimensional data with a distance that has a good family, when you need a guarantee for each query or a method that is easy to analyze and to distribute over machines, as in near-duplicate detection with [MinHash](/minhash/). Its space of $n^{1+\rho}$ entries is its main cost. For in-memory vector search with a fixed data set, graph indexes such as [HNSW](/hnsw/) usually reach a higher recall at the same speed, with no guarantee. For low dimension, a [k-d tree](/kd-tree/) is exact and fast.

## Pitfalls

- **No stop rule.** Without line L10, one query can scan a huge bucket, for example when many points are near each other but far from $q$. The bound of $3L$ distances is what makes the query time sublinear in the worst case.
- **Reusing the functions.** Line L2 must draw new functions for each table. Tables built from the same functions are copies, and the probability of $E_1$ drops back to $p_1^k$.
- **Wrong $k$ for the data.** The proof needs $p_2^k \le 1/n$. If $k$ is too small, buckets fill with far points; if it is too large, near points rarely collide. Recompute $k$ and $L$ when $n$ changes by a large factor.
- **Treating "none" as "no near point".** "None" is a correct answer only with probability; with $L$ too small it is often wrong. For a decision with error $f$, use independent copies.

## Implementations

## History

Indyk and Motwani defined locality-sensitive families and gave this scheme in a paper at STOC 1998, with bit sampling for the Hamming cube and query time about $n^{1/c}$. Gionis, Indyk and Motwani gave the practical form for disk-based data in 1999. Charikar added the random hyperplane family in 2002, and Datar, Immorlica, Indyk and Mirrokni the $p$-stable family in 2004. Andoni and Indyk reached $\rho = 1/c^2 + o(1)$ for $\ell_2$ in 2006, and the journal version of the founding paper, with Har-Peled, appeared in 2012.

## References
