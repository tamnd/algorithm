---
tag: K84C3G
kind: algorithm
slug: e2lsh
name: E2LSH
aliases:
- Euclidean LSH
area: searching/similarity-search
level: advanced
summary: LSH for Euclidean distance built from p-stable random projections quantized into buckets.
solves: [approximate-nearest-neighbor-search]
model: real-ram
complexity:
  vars: {n: the number of points, d: the dimension, k: the number of projections in a key, L: the number of tables, w: the bucket width, ρ: the exponent ln(1/p(r))/ln(1/p(cr))}
  time: {build: O(n L k d), query: O(L k d + L d)}
  space: {total: O(n L + n d + L k d)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: false, comparison: false, recursive: false}
history:
  year: 2004
  people: [Mayur Datar, Nicole Immorlica, Piotr Indyk, Vahab S. Mirrokni]
  note: Datar, Immorlica, Indyk and Mirrokni gave the family of quantized projections onto p-stable random vectors at SoCG 2004, the first LSH family that works directly in ℓ2 and ℓp; Andoni and Indyk released it as the E2LSH package.
prereqs: [locality-sensitive-hashing, p-stable-distribution]
see_also: [locality-sensitive-hash-family, lsh-amplification, euclidean-distance, johnson-lindenstrauss-lemma, random-hyperplane-lsh, multi-probe-lsh, bit-sampling-lsh, approximate-nearest-neighbor-search]
sources:
  - paper: doi:10.1145/997817.997857
    title: Mayur Datar, Nicole Immorlica, Piotr Indyk and Vahab S. Mirrokni, Locality-sensitive hashing scheme based on p-stable distributions, Proceedings of the 20th ACM Symposium on Computational Geometry (SoCG), 2004
    locator: pages 253 to 262 (the family h(v) = floor((a·v + b)/w), its collision probability as an integral over the density of |a·(x − y)|, and the numerical computation of ρ against c)
  - paper: doi:10.1145/1327452.1327494
    title: Alexandr Andoni and Piotr Indyk, Near-optimal hashing algorithms for approximate nearest neighbor in high dimensions, Communications of the ACM 51(1), 2008
    locator: pages 117 to 122 (the p-stable family in practice, and the ball-carving family with ρ = 1/c² + o(1))
  - paper: doi:10.4086/toc.2012.v008a014
    title: Sariel Har-Peled, Piotr Indyk and Rajeev Motwani, Approximate nearest neighbor, towards removing the curse of dimensionality, Theory of Computing 8, 2012
    locator: Section 3 (the LSH data structure and its success probability, used here with the p-stable family)
---

E2LSH is [locality-sensitive hashing](/locality-sensitive-hashing/) for the [Euclidean distance](/euclidean-distance/) in $\mathbb{R}^d$. Each hash function projects a point onto a random Gaussian direction $a$, shifts it by a random $b \in [0, w)$, and cuts the line into intervals of width $w$: $h(v) = \lfloor (a \cdot v + b)/w \rfloor$. Because the Gaussian is 2-[stable](/p-stable-distribution/), the collision probability of two points depends only on their distance $u$, and it decreases in $u$; for $w = 4$ and $c = 2$ the exponent is $\rho \approx 0.449 < 1/c$. With $L = O(n^\rho)$ tables, a query computes $O(n^{\rho} \log n)$ projections and at most $3L$ distances, and it finds a point within $cr$ with probability at least $2/3 - 1/e > 0.29$ when a point within $r$ exists. Datar, Immorlica, Indyk and Mirrokni introduced the family in 2004.

## In plain words

Pick a random direction and look at the shadow of every point on a line in that direction. Points that are close have shadows that are close. Cut the line into equal pieces, starting at a random offset, and use the number of the piece as the hash value. Close points usually land in the same piece; far points usually do not.

One piece number is a weak test, so a key is made from several directions at once, and several tables are built with different keys. A query checks the points that share its key in each table.

## The problem

The input is a set $P$ of $n$ points in $\mathbb{R}^d$, a radius $r > 0$ and a factor $c > 1$. A query $q$ must get a point within $cr$ if some point is within $r$, and must never get a point beyond $cr$. This is the randomized $(c, r)$-near neighbor problem of [c-approximate nearest neighbor](/c-approximate-nearest-neighbor/), the building block of [approximate nearest neighbor search](/approximate-nearest-neighbor-search/).

## The algorithm

```pseudo id=main
E2LSH-BUILD(P, k, L, w)
L1  for j ← 1 to L do
L2      for i ← 1 to k: draw a_{j,i} with d independent N(0, 1) entries, and b_{j,i} uniform in [0, w)
L3      T_j ← a hash table that stores each x ∈ P under g_j(x) = (⌊(a_{j,i} · x + b_{j,i})/w⌋ for i = 1..k)

E2LSH-QUERY(q, c, r)
L4  count ← 0
L5  for j ← 1 to L, and for each x in the bucket g_j(q) of T_j do
L6      count ← count + 1; if ‖q − x‖ ≤ c r then return x
L7      if count ≥ 3L then return none
L8  return none
```

Line L2 draws $kL$ independent functions. The key of line L3 is a tuple of $k$ integers, hashed again into an ordinary [hash table](/hash-table/). The query is the same as in [locality-sensitive hashing](/locality-sensitive-hashing/), with the stop rule of line L7.

**Collision probability.** For $\|x - y\| = u > 0$, let $t = w/u$ and let $\Phi$ be the standard normal distribution function. Then

$$p(u) = \Pr[h(x) = h(y)] = 1 - 2\Phi(-t) - \frac{2}{\sqrt{2\pi}\, t}\big(1 - e^{-t^2/2}\big).$$

It depends only on $w/u$. **The parameters.** Scale the data so that $r = 1$. With $p_1 = p(1)$ and $p_2 = p(c)$, set $k = \lceil \ln n / \ln(1/p_2) \rceil$ and $L = \lceil n^\rho / p_1 \rceil$ with $\rho = \ln(1/p_1)/\ln(1/p_2)$.

| $w$ | $p(1)$ | $p(2)$ | $\rho$ for $c = 2$ | $\rho$ for $c = 3$ |
|---|---|---|---|---|
| 1 | 0.3687 | 0.1954 | 0.6111 | 0.4922 |
| 2 | 0.6095 | 0.3687 | 0.4962 | 0.3639 |
| 4 | 0.8005 | 0.6095 | 0.4494 | 0.2907 |
| 8 | 0.9003 | 0.8005 | 0.4723 | 0.2966 |

For $c = 2$ the best width in the table is $w = 4$, with $\rho \approx 0.449$, against $1/c = 0.5$. With $n = 10^6$, $c = 2$ and $w = 4$, the formulas give $k = 28$ and $L = 622$.

## Example

Take $d = 1$, so that $a$ is a single Gaussian number and $h(v) = \lfloor (a v + b)/w \rfloor$, with $w = 4$. For the points $x = 0.0$ and $y = 1.5$ and the draw $a = 1.2$, $b = 2.5$: $a x + b = 2.5$ and $a y + b = 4.3$, so $h(x) = 0$ and $h(y) = 1$, and they do not collide. With $b = 0.5$ instead: $0.5$ and $2.3$, both in bucket 0, so they collide. For this $a$, the shadows are $|a| \cdot 1.5 = 1.8$ apart, and they collide for a fraction $1 - 1.8/4 = 0.55$ of the shifts $b$. Averaged over $a$, the collision probability at $u = 1.5$ is $p(1.5) \approx 0.70$.

## Correctness

A returned point passed the test of line L6, so it is within $cr$. The other direction is the LSH theorem applied to the following lemma.

**Lemma 1 (collision probability).** For $x, y \in \mathbb{R}^d$ with $\|x - y\| = u > 0$, $\Pr[h(x) = h(y)] = p(u)$ as above, and $p$ is strictly decreasing in $u$. So the family is $(r, cr, p(r), p(cr))$-sensitive for every $c > 1$.

*Proof sketch.* By 2-stability, $a \cdot x - a \cdot y = a \cdot (x - y)$ has the law of $u Z$ with $Z \sim N(0, 1)$. Given $s = |a \cdot (x - y)|$, the two shifted values collide exactly when no multiple of $w$ falls between them, which has probability $\max(0, 1 - s/w)$ over $b$. So $p(u) = \mathbb{E}[\max(0, 1 - u|Z|/w)]$, which is strictly decreasing in $u$, and integrating against the density of $|Z|$ gives the closed form.

**Theorem.** With $k$ and $L$ as above, for each fixed $q$ that has a point within $r$, E2LSH-QUERY returns a point within $cr$ with probability at least $2/3 - 1/e > 0.29$ over the draws of line L2. The full proof is in `proofs/correctness.md`.

## Complexity

The model is the [real RAM](/real-ram/) with exact Gaussian samples and the floor function, and with hash tables of $O(1)$ expected time per operation.

- **Build.** $nLk$ projections of $O(d)$ time each: $O(nLkd)$.
- **Query.** $Lk$ projections, $O(Lkd)$, and at most $3L$ distances, $O(Ld)$. With the parameters above, $O(d \, n^{\rho} \log n / p_1)$ time for fixed $c$ and $w$.
- **Space.** $O(nL)$ table entries, $O(nd)$ for the points and $O(Lkd)$ for the projection vectors. With the parameters above, $O(n^{1 + \rho}/p_1 + nd)$.
- **Failure probability.** At most $1/3 + 1/e < 0.71$ per query and fixed $q$; $t$ independent copies give $0.71^t$.

## Properties

- **One-sided error.** A returned point is always within $cr$.
- **Data-independent.** The functions are drawn without looking at $P$.
- **Exponent.** $\rho$ depends on $w$ and $c$. As $w \to \infty$, $1 - p(u)$ is about $\sqrt{2/\pi} \, u/w$, so $\rho \to 1/c$; the best $w$ gives a value a little below $1/c$, as in the table. The ball-carving family of Andoni and Indyk reaches $\rho = 1/c^2 + o(1)$, which is optimal for LSH in $\ell_2$ (see [locality-sensitive hash family](/locality-sensitive-hash-family/)).
- **Other norms.** With entries from a $p$-stable law, the same scheme works for $\ell_p$, $0 < p \le 2$; the Cauchy law gives $\ell_1$.

## Variants and improvements

- **Multi-probe.** [Multi-probe LSH](/multi-probe-lsh/) also checks the buckets whose keys differ from $g_j(q)$ by $\pm 1$ in a few coordinates, chosen by how close $a \cdot q + b$ is to a bucket edge. It reaches the same recall with many fewer tables.
- **Dimension reduction first.** A [Johnson-Lindenstrauss](/johnson-lindenstrauss-lemma/) projection to $O(\log n / \varepsilon^2)$ dimensions makes each projection cheaper.
- **Angles.** For unit vectors and the angle, [random hyperplanes](/random-hyperplane-lsh/) give one bit per function, $\lfloor \cdot \rfloor$ replaced by a sign.
- **k nearest neighbors.** In practice the stop rule is dropped, all candidates of the $L$ buckets are ranked by distance, and the $k$ best are returned.

## When to use it

Use E2LSH for Euclidean data of high dimension when a per-query guarantee matters, when the index must be built fast without training, or when points arrive in a stream. It needs a known radius, or a ladder of structures for many radii. Its space is large, $n^{1 + \rho}$ entries, and in practice, at the same recall, graph indexes such as [HNSW](/hnsw/) and quantized indexes such as the [inverted file index](/inverted-file-index/) are usually faster and smaller.

## Pitfalls

- **Wrong scale.** The width $w$ is relative to $r$; after scaling the data so that $r = 1$, $w$ around 4 is a good start. A width far too small makes $p_1$ tiny; a width far too large lets far points collide.
- **Reusing projections.** Each of the $kL$ functions needs its own $a$ and $b$; shared projections break the independence that the proof uses.
- **Unbounded keys.** The integers of the key can be large; hash the tuple, do not use it as an array index.
- **Floating-point edges.** Points with $a \cdot x + b$ exactly on a multiple of $w$ go to one side by the floor; this has probability 0 for random draws, but data on a grid with a fixed $b$ can hit it.

## Implementations

## History

Datar, Immorlica, Indyk and Mirrokni gave the family at SoCG 2004, with the collision probability as an integral and the exponent computed numerically for $\ell_1$ and $\ell_2$. Before it, LSH for $\ell_2$ went through an embedding into the Hamming cube. Andoni and Indyk distributed an implementation named E2LSH, and in 2006 gave the ball-carving family with $\rho = 1/c^2 + o(1)$, surveyed in Communications of the ACM in 2008.

## References
