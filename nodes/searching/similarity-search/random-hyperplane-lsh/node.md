---
tag: 7MZBA9
kind: algorithm
slug: random-hyperplane-lsh
name: Random hyperplane LSH
aliases:
- sign random projections
- SimHash-style LSH for angles
area: searching/similarity-search
level: core
summary: LSH for angular distance that hashes each vector by the signs of its dot products with random hyperplanes.
model: real-ram
complexity:
  vars: {n: the number of vectors, d: the dimension, k: the bits per table, L: the number of tables, ρ: the exponent ln(1/p1)/ln(1/p2)}
  time: {build: O(n d k L), query: O(d k L) expected}
  space: {total: O(n L + d k L)}
properties: {deterministic: false, online: true}
history:
  year: 2002
  people: [Moses Charikar]
  note: Charikar turned the random hyperplane rounding of Goemans and Williamson into a locality-sensitive hash family for the angle between vectors in 2002.
prereqs: [locality-sensitive-hashing, cosine-similarity, markov-inequality]
see_also: [locality-sensitive-hash-family, locality-sensitive-hashing, simhash, lsh-amplification, multi-probe-lsh, cosine-similarity, bit-sampling-lsh, maximum-inner-product-search]
sources:
  - paper: doi:10.1145/509907.509965
    title: Moses S. Charikar, Similarity estimation techniques from rounding algorithms, Proceedings of the 34th ACM Symposium on Theory of Computing (STOC), 2002
    locator: pages 380 to 388 (Section 3, the random hyperplane hash family with collision probability 1 − θ/π)
  - paper: doi:10.1145/227683.227684
    title: Michel X. Goemans and David P. Williamson, Improved approximation algorithms for maximum cut and satisfiability problems using semidefinite programming, Journal of the ACM 42(6), 1995
    locator: pages 1115 to 1145 (the lemma that a random hyperplane separates two unit vectors with probability equal to their angle divided by π)
  - paper: doi:10.1145/276698.276876
    title: Piotr Indyk and Rajeev Motwani, Approximate nearest neighbors, towards removing the curse of dimensionality, Proceedings of the 30th ACM Symposium on Theory of Computing (STOC), 1998
    locator: pages 604 to 613 (locality-sensitive families, the scheme of L tables of k concatenated hashes, and its analysis by Markov's inequality)
  - book: isbn:9781107077232
    title: Jure Leskovec, Anand Rajaraman and Jeffrey D. Ullman, Mining of Massive Datasets, second edition, Cambridge University Press, 2014
    locator: Chapter 3, Section 3.7.2, Random Hyperplanes and the Cosine Distance, and Section 3.6, The Theory of Locality-Sensitive Functions
---

Random hyperplane LSH hashes a vector $x \in \mathbb{R}^d$ to one bit, the sign of $r \cdot x$ for a random Gaussian vector $r$; two vectors at angle $\theta$ get the same bit with probability exactly $1 - \theta/\pi$. It is the [locality-sensitive hash family](/locality-sensitive-hash-family/) for the angle, and so for [cosine similarity](/cosine-similarity/). With $L$ hash tables keyed by $k$ such bits, it solves the approximate near neighbor problem for angles: if some stored vector is within angle $\theta_1$ of the query, it returns a vector within angle $\theta_2 > \theta_1$ with probability at least $1 - 1/e - 1/3 \approx 0.2988$, after $O(n^{\rho})$ distance evaluations, where $\rho = \ln(1/p_1)/\ln(1/p_2) < 1$. Charikar introduced the family in 2002, from the rounding step of the Goemans-Williamson algorithm for maximum cut.

## In plain words

Draw a random flat cut through the origin. Every vector lies on one side of it. Write 1 for one side and 0 for the other. Two vectors that point in almost the same direction are rarely split by a random cut. Two vectors that point in very different directions are split often. The chance of a split is exactly the angle between them divided by half a turn.

Use several cuts and write down all the bits. This code names a bucket. Vectors with the same code go into the same bucket, and similar vectors are likely to share a bucket. To find vectors like a query, compute the code of the query and look only in its bucket. A similar vector can still be cut away by bad luck, so keep several tables with different random cuts, and look in the bucket of the query in each.

## The problem

The data set is a set $P$ of $n$ nonzero vectors in $\mathbb{R}^d$. The angle between nonzero vectors is $\theta(x, y) = \arccos\big(x \cdot y / (\lVert x \rVert \lVert y \rVert)\big) \in [0, \pi]$. For two angles $0 < \theta_1 < \theta_2 < \pi$, the **$(\theta_1, \theta_2)$-near neighbor** problem asks for a structure that, for a query $q$, does this: if some $p \in P$ has $\theta(q, p) \le \theta_1$, return some $x \in P$ with $\theta(q, x) \le \theta_2$. If no point is within $\theta_2$, return "none". In the other cases either answer is allowed. This is the approximate near neighbor problem of [locality-sensitive hashing](/locality-sensitive-hashing/) for the angle, which is a metric on directions.

## The algorithm

```pseudo id=main
HASH(x, R)                                 ▷ R = (r1, ..., rk), vectors of R^d
L1  return the bit string (b1, ..., bk) with bi = 1 if ri · x ≥ 0, else 0

BUILD(P, k, L)
L2  for ℓ ← 1 to L do
L3      Rℓ ← k vectors with independent N(0, 1) coordinates
L4      for each x in P do append x to the bucket Tℓ[HASH(x, Rℓ)]

QUERY(q, θ2)
L5  c ← 0
L6  for ℓ ← 1 to L do
L7      for each x in Tℓ[HASH(q, Rℓ)] do
L8          if θ(q, x) ≤ θ2 then return x
L9          c ← c + 1
L10         if c ≥ 3L then return none
L11 return none
```

HASH makes a key of $k$ bits, one per hyperplane: the hyperplane is the set of vectors orthogonal to $r_i$, and the bit tells the side. BUILD makes $L$ tables, each with its own independent hyperplanes, and stores each vector in one bucket per table. QUERY looks in the bucket of $q$ in each table. Every vector it rejects in line L8 is farther than $\theta_2$; line L10 stops after $3L$ of them, which bounds the time of a query. The parameters are $p_1 = 1 - \theta_1/\pi$, $p_2 = 1 - \theta_2/\pi$, $\rho = \ln(1/p_1)/\ln(1/p_2)$, $k = \lceil \log_{1/p_2} n \rceil$ and $L = \lceil n^{\rho}/p_1 \rceil$.

## Example

In the plane, take the four hyperplanes with normals $r_1 = (0.5, 1)$, $r_2 = (-1, 0.3)$, $r_3 = (0.2, -1)$ and $r_4 = (1, -0.4)$, and four vectors.

| vector | $r_1 \cdot x$ | $r_2 \cdot x$ | $r_3 \cdot x$ | $r_4 \cdot x$ | key |
|---|---|---|---|---|---|
| $x = (1, 0)$ | 0.5 | $-1$ | 0.2 | 1 | 1011 |
| $y = (1, 1)$ | 1.5 | $-0.7$ | $-0.8$ | 0.6 | 1001 |
| $w = (0.9, 0.3)$ | 0.75 | $-0.81$ | $-0.12$ | 0.78 | 1001 |
| $z = (-1, 0.2)$ | $-0.3$ | 1.06 | $-0.4$ | $-1.08$ | 0100 |

The angles and the probabilities $1 - \theta/\pi$ that one random bit agrees are:

| pair | angle in degrees | one bit agrees | the 4 bits above agree |
|---|---|---|---|
| $x, w$ | 18.43 | 0.8976 | 3 of 4 |
| $w, y$ | 26.57 | 0.8524 | 4 of 4 |
| $x, y$ | 45 | 0.75 | 3 of 4 |
| $x, z$ | 168.69 | 0.0628 | 0 of 4 |

With $k = 4$, the keys put $y$ and $w$ in the same bucket, $x$ alone, and $z$ alone. A query near $x$ misses $w$ in this table, because $r_3$ cuts between them; the other $L - 1$ tables give $w$ more chances.

For a realistic size, let $n = 10^6$, $\theta_1 = 30^\circ$ and $\theta_2 = 60^\circ$. Then $p_1 = 5/6$, $p_2 = 2/3$, $\rho = \ln 1.2 / \ln 1.5 \approx 0.4497$, $k = \lceil 34.07 \rceil = 35$ and $L = \lceil n^{\rho}/p_1 \rceil = 599$ tables. A query computes $35 \times 599$ dot products for the keys and at most $3 \times 599 + 1$ angles, instead of $10^6$.

## Correctness

**Lemma (Goemans and Williamson; Charikar).** For nonzero $x, y \in \mathbb{R}^d$ and a vector $r$ with independent $N(0, 1)$ coordinates, $\Pr[\operatorname{sign}(r \cdot x) = \operatorname{sign}(r \cdot y)] = 1 - \theta(x, y)/\pi$.

The reason: only the projection of $r$ onto the plane of $x$ and $y$ matters, its direction is uniform on the circle because the Gaussian is invariant under rotations, and the signs differ exactly when the line orthogonal to that direction passes between $x$ and $y$, which happens on two arcs of total angle $2\theta$ out of $2\pi$.

**Theorem.** With the parameters above, if some $p^* \in P$ has $\theta(q, p^*) \le \theta_1$, QUERY returns a vector within angle $\theta_2$ of $q$ with probability at least $1 - 1/e - 1/3$. Every vector that QUERY returns is within $\theta_2$.

The proof bounds two bad events. The chance that $p^*$ shares no bucket with $q$ is at most $(1 - p_1^k)^L \le 1/e$, because $p_1^k \ge p_1 n^{-\rho}$. The expected number of far vectors (angle above $\theta_2$) in the buckets of $q$ is at most $L \cdot n p_2^k \le L$, so by [Markov's inequality](/markov-inequality/) there are $3L$ or more of them with probability at most $1/3$. Outside both events, QUERY reaches $p^*$, or another vector within $\theta_2$, before line L10 stops it. The full proof is below. Independent repetitions raise the success probability: $t$ independent copies of the structure fail together with probability at most $(1/e + 1/3)^t$.

## Complexity

The model is the [real RAM](/real-ram/) with a source of Gaussian random numbers, and a hash table lookup in $O(1)$ expected time.

- **Build.** Line L3 draws $dkL$ numbers. Line L4 computes $kL$ dot products for each vector, $O(dk)$ time per table: $O(ndkL)$ in total. With the parameters above, this is $O(d\, n^{1 + \rho} \log n)$, since $kL = O(n^{\rho} \log n)$ for fixed $\theta_1$ and $\theta_2$.
- **Query.** $L$ keys at $O(dk)$ each, plus at most $3L + 1$ angle computations at $O(d)$ each: $O(dkL) = O(d\, n^{\rho} \log n)$, worst case for the number of angles and expected for the lookups.
- **Space.** $L$ references per vector and the $dkL$ hyperplane coordinates: $O(nL + dkL) = O(n^{1+\rho} + d\, n^{\rho} \log n)$.

The exponent satisfies $\rho < 1$ because $p_1 > p_2$. For $\theta_2 = c\,\theta_1$ with small angles, $\ln(1/p) \approx \theta/\pi$, so $\rho \approx 1/c$.

## Properties

- **Randomized, one-sided error.** A returned vector is always within $\theta_2$; the error is a miss, with probability at most $1/e + 1/3$ per query.
- **Scale invariant.** HASH depends only on the direction of $x$: $x$ and $2x$ get the same key. Normalizing the data is not needed.
- **Online.** A vector is inserted by hashing it into the $L$ tables, without a rebuild, as long as $n$ stays within a constant factor of the value used to choose $k$ and $L$.
- **Compact keys.** A key of $k$ bits fits a machine word for $k \le 64$.

## Variants and improvements

- **Similarity estimation.** Without tables, the fraction of agreeing bits among $k$ independent hyperplanes estimates $1 - \theta/\pi$, so $\theta$ and $\cos\theta$, as [MinHash](/minhash/) estimates the Jaccard similarity. [SimHash](/simhash/) applies this to weighted feature sets of documents.
- **Multi-probe.** [Multi-probe LSH](/multi-probe-lsh/) also looks in buckets whose key differs from the query key in a few bits, starting with the bits whose dot product $r_i \cdot q$ is closest to 0. It needs far fewer tables.
- **Fast projections.** Replace the dense Gaussian matrix by a structured one, such as a randomized Hadamard transform, to compute $k$ bits in $O(d \log d)$ time.
- **Better families.** Cross-polytope LSH and other spherical families reach a smaller $\rho$ for the same angles; for the Euclidean distance, [E2LSH](/e2lsh/) uses projections onto random lines cut into intervals.
- **Inner products.** After an asymmetric transformation that gives all data vectors the same norm, the angle family also serves [maximum inner product search](/maximum-inner-product-search/).

## When to use it

Use random hyperplane LSH for cosine similarity or angles between dense vectors, when an answer with a probabilistic guarantee is enough and the dimension is too high for a [k-d tree](/kd-tree/). For sets with Jaccard similarity use [MinHash](/minhash/); for Hamming distance use [bit sampling](/bit-sampling-lsh/); for the Euclidean distance between unnormalized vectors use [E2LSH](/e2lsh/). In practice, for in-memory search with a high recall, graph indexes such as [HNSW](/hnsw/) are often faster, but they have no guarantee.

## Pitfalls

- **The zero vector.** Line L1 maps $0$ to the all-ones key, and the angle is undefined. Remove or treat zero vectors before line L4.
- **Uniform instead of Gaussian.** Coordinates drawn uniformly from $[-1, 1]$ give a direction that is not uniform on the sphere, and the collision probability is no longer $1 - \theta/\pi$. Line L3 must use a rotation-invariant distribution, such as independent Gaussians.
- **One set of hyperplanes for all tables.** Reusing the same $R$ in all tables makes all $L$ tries fail together. Each table needs fresh hyperplanes.
- **No stop rule.** Without line L10 a query can scan a huge bucket of far vectors, for example when the data has many near-duplicates of a vector far from $q$. The stop after $3L$ rejected vectors is what makes the query time sublinear in the worst case.
- **The wrong distance in line L8.** Testing $1 - \cos\theta \le 1 - \cos\theta_2$ is the same test as $\theta \le \theta_2$, but mixing angles in degrees and radians, or comparing the cosine with the angle, is a common bug.

## Implementations

## History

Goemans and Williamson used a random hyperplane to round the vectors of a semidefinite program for maximum cut, and proved that it separates two unit vectors with probability $\theta/\pi$; their paper appeared in the Journal of the ACM in 1995. Indyk and Motwani defined locality-sensitive families and the scheme of $L$ tables of $k$ concatenated hashes in 1998. Charikar observed in 2002 that the rounding step is a locality-sensitive hash family for the angle, and used it to estimate similarities from short sketches.

## References
