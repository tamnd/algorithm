---
tag: NNNB37
kind: algorithm
slug: asymmetric-lsh
name: Asymmetric LSH
aliases:
- ALSH
- Simple-LSH
- L2-ALSH
- ALSH
area: searching/similarity-search
level: research
summary: Uses different transformations for data and queries to reduce maximum inner product search to LSH for angles.
solves: [maximum-inner-product-search]
model: real-ram
complexity:
  vars: {n: the number of points, d: the dimension, k: the number of hyperplanes in a key, L: the number of tables, C: the number of candidates of a query, ρ: the exponent ln(1/p1)/ln(1/p2)}
  time: {build: O(n L k d), query: O(L k d + C d)}
  space: {total: O(n L + n d + L k d)}
properties: {stable: false, in_place: false, adaptive: false, online: false, deterministic: false, comparison: false, recursive: false}
history:
  year: 2014
  people: [Anshumali Shrivastava, Ping Li, Behnam Neyshabur, Nathan Srebro]
  note: Shrivastava and Li showed in 2014 that no symmetric LSH family exists for inner products and gave the first asymmetric one, L2-ALSH, built on E2LSH; Neyshabur and Srebro gave the simpler transformation with random hyperplanes in 2015.
prereqs: [maximum-inner-product-search, locality-sensitive-hashing]
see_also: [random-hyperplane-lsh, e2lsh, locality-sensitive-hash-family, lsh-amplification, cosine-similarity, dot-product, approximate-nearest-neighbor-search, inverted-file-index]
sources:
  - url: https://arxiv.org/abs/1405.5869
    title: Anshumali Shrivastava and Ping Li, Asymmetric LSH (ALSH) for sublinear time maximum inner product search (MIPS), Advances in Neural Information Processing Systems 27 (NeurIPS), 2014
    locator: the definition of an asymmetric LSH family, the theorem that no symmetric LSH family exists for MIPS, and the maps P(x) = [x; |x|^2; ...; |x|^(2^m)], Q(q) = [q; 1/2; ...; 1/2] with |Q(q) − P(x)|^2 = 1 + m/4 − 2 q·x + |x|^(2^(m+1))
  - url: https://proceedings.mlr.press/v37/neyshabur15.html
    title: Behnam Neyshabur and Nathan Srebro, On symmetric and asymmetric LSHs for inner product search, Proceedings of the 32nd International Conference on Machine Learning (ICML), PMLR 37, 2015
    locator: the maps P(x) = [x; sqrt(1 − |x|^2)] and Q(q) = [q; 0] followed by random hyperplanes (Simple-LSH), and the comparison of its exponent with L2-ALSH
  - paper: doi:10.1145/509907.509965
    title: Moses S. Charikar, Similarity estimation techniques from rounding algorithms, Proceedings of the 34th ACM Symposium on Theory of Computing (STOC), 2002
    locator: pages 380 to 388 (Section 3, sketches from random hyperplanes, with collision probability 1 − θ/π for the angle θ between the vectors)
  - paper: doi:10.1145/276698.276876
    title: Piotr Indyk and Rajeev Motwani, Approximate nearest neighbors, towards removing the curse of dimensionality, Proceedings of the 30th ACM Symposium on Theory of Computing (STOC), 1998
    locator: pages 604 to 613 (the (r1, r2, p1, p2)-sensitive families and the construction with k concatenated hashes and L tables)
---

Asymmetric LSH (ALSH) reduces [maximum inner product search](/maximum-inner-product-search/) to [locality-sensitive hashing](/locality-sensitive-hashing/) by applying one map $P$ to the stored vectors and a different map $Q$ to the query, chosen so that a distance between $P(x)$ and $Q(q)$ is a decreasing function of the inner product $q \cdot x$. The asymmetry is needed: Shrivastava and Li proved that no hash family applied in the same way to both sides can be locality-sensitive for inner products. The simplest version, by Neyshabur and Srebro, scales the data into the unit ball, appends $\sqrt{1 - \|x\|^2}$ to each data vector and $0$ to the normalized query, and then uses [random hyperplanes](/random-hyperplane-lsh/); a point that beats the threshold $S$ is found with probability at least $1 - 1/e$ in time $O(n^{\rho})$ hash evaluations, with $\rho = \ln(1/p_1)/\ln(1/p_2) < 1$.

## In plain words

Recommendation systems store a vector for each item and compute a vector for each user. The best items for a user are the ones with the largest inner product with the user's vector. Searching all items is slow, and the usual fast tools find near vectors, not vectors with a large inner product. These are different: a long item vector can win the inner product even if it points a little away from the user.

The trick is to change the vectors before hashing. Every item vector gets one extra number, so that all item vectors have the same length. The user vector gets a 0 in that place. After this change, the item with the largest inner product is the item whose direction is closest to the user's direction, and ordinary hashing by direction can find it.

## The problem

Given vectors $X = \{x_1, \dots, x_n\} \subset \mathbb{R}^d$, preprocess them so that for a query $q \in \mathbb{R}^d$, $q \ne 0$, we find $\arg\max_i q \cdot x_i$. Scaling $q$ by a positive number does not change the answer.

The approximate form uses thresholds. Let $M = \max_i \|x_i\|$ and define the normalized inner product $s(q, x) = q \cdot x/(M \|q\|) \in [-1, 1]$. For $0 < S \le 1$ and $0 < c < 1$: if some $x$ has $s(q, x) \ge S$, return a point $x'$ with $s(q, x') \ge cS$. Our version returns the best candidate it sees, so if it sees a point with $s \ge S$ it returns one with $s \ge S$.

An **asymmetric** hash family is a distribution over pairs of functions $(h^P, h^Q)$ with: $\Pr[h^P(x) = h^Q(q)] \ge p_1$ when $s(q, x) \ge S$, and $\le p_2$ when $s(q, x) \le cS$, where $p_1 > p_2$. A symmetric family is the case $h^P = h^Q$.

## The algorithm

```pseudo id=main
PREPROCESS(X, k, L)
L1  M ← max over x ∈ X of ‖x‖
L2  P(x) ← (x/M, √(1 − ‖x‖²/M²)) for each x ∈ X              ▷ a unit vector in ℝ^(d+1)
L3  draw k·L vectors a_{j,i} ∈ ℝ^(d+1) with independent standard normal entries
L4  for j ← 1 to L: store each x in table T_j under g_j(P(x)) = (sign(a_{j,1}·P(x)), ..., sign(a_{j,k}·P(x)))

QUERY(q)
L5  Q(q) ← (q/‖q‖, 0)                                        ▷ a unit vector in ℝ^(d+1)
L6  C ← the union over j of the bucket T_j[g_j(Q(q))]
L7  return the x ∈ C with the largest q·x, or "none" if C is empty
```

Line L2 lifts every data vector onto the unit sphere of $\mathbb{R}^{d+1}$ without changing its first $d$ coordinates except for the common scale $1/M$. Line L5 puts the query on the same sphere with last coordinate 0. Then $P(x) \cdot Q(q) = q \cdot x/(M \|q\|) = s(q, x)$: the inner product of the original vectors has become the cosine of the angle between unit vectors. Lines L3, L4 and L6 are [random hyperplane LSH](/random-hyperplane-lsh/) for that angle, amplified with $k$ bits per key and $L$ tables as in [LSH amplification](/lsh-amplification/). Line L7 checks the candidates exactly.

**L2-ALSH.** The first construction, by Shrivastava and Li, scales the data so that $\|x\| \le U < 1$, normalizes the query, and uses

$$P(x) = (x, \|x\|^2, \|x\|^4, \dots, \|x\|^{2^m}), \qquad Q(q) = (q, \tfrac12, \dots, \tfrac12),$$

so that $\|Q(q) - P(x)\|^2 = 1 + m/4 - 2\, q \cdot x + \|x\|^{2^{m+1}}$. The last term is at most $U^{2^{m+1}}$, which tends to 0 fast as $m$ grows, so the Euclidean distance is almost a decreasing function of $q \cdot x$, and [E2LSH](/e2lsh/) applies. The identity holds because the sum $\sum_{i=1}^m (\tfrac12 - \|x\|^{2^i})^2$ telescopes: its cross terms $-\|x\|^{2^i}$ and squares $\|x\|^{2^{i+1}}$ cancel except for $-\|x\|^2$ and $+\|x\|^{2^{m+1}}$, and the $-\|x\|^2$ cancels the $\|x\|^2$ in $\|q - x\|^2$.

## Example

Take $X = \{(2, 0), (1, 1), (0, 3), (-1, -1)\}$ and $q = (1, 1)$. Then $M = 3$, $\|q\| = \sqrt 2$, and line L2 gives

| $x$ | $q \cdot x$ | $P(x)$ | $s(q, x)$ | angle | $1 - \theta/\pi$ | cosine of $q$ and $x$ |
|---|---|---|---|---|---|---|
| $(2, 0)$ | 2 | $(0.6667, 0, 0.7454)$ | 0.4714 | 61.87° | 0.6563 | 0.7071 |
| $(1, 1)$ | 2 | $(0.3333, 0.3333, 0.8819)$ | 0.4714 | 61.87° | 0.6563 | 1 |
| $(0, 3)$ | 3 | $(0, 1, 0)$ | 0.7071 | 45° | 0.75 | 0.7071 |
| $(-1, -1)$ | −2 | $(-0.3333, -0.3333, 0.8819)$ | −0.4714 | 118.13° | 0.3437 | −1 |

with $Q(q) = (0.7071, 0.7071, 0)$. The MIPS answer is $(0, 3)$, and after the maps it has the smallest angle to $Q(q)$ and the highest probability, 0.75, of agreeing with the query on one hyperplane bit. Plain angular LSH on the original vectors would favor $(1, 1)$, whose cosine with $q$ is 1, though its inner product is only 2. The extra coordinate $\sqrt{1 - \|x\|^2/M^2}$ tilts the shorter vectors away from the query's hyperplane $\{y : y_{d+1} = 0\}$.

**Parameters.** For $n = 10^6$, $S = 0.9$ and $c = 0.5$: $p_1 = 1 - \arccos(0.9)/\pi = 0.8564$ and $p_2 = 1 - \arccos(0.45)/\pi = 0.6486$, so $\rho = 0.3579$. The theorem below gives $k = \lceil \ln n/\ln(1/p_2) \rceil = 32$ and $L = \lceil n^\rho/p_1 \rceil = 165$ tables.

## Correctness

The proofs are in the proof file.

**Lemma 1 (the maps).** $\|P(x)\| = \|Q(q)\| = 1$ and $P(x) \cdot Q(q) = s(q, x)$.

**Lemma 2 (one bit).** For a standard normal $a$ and unit vectors $u, v$ at angle $\theta$, $\Pr[\operatorname{sign}(a \cdot u) = \operatorname{sign}(a \cdot v)] = 1 - \theta/\pi$. This is the random hyperplane lemma of Charikar, used in [random hyperplane LSH](/random-hyperplane-lsh/). So one bit of line L4 is an asymmetric family with $p_1 = 1 - \arccos(S)/\pi$ and $p_2 = 1 - \arccos(cS)/\pi$, and $p_1 > p_2$ because $\arccos$ is decreasing.

**Theorem (guarantee).** Model: real RAM with exact arithmetic and independent standard normal samples. Let $k = \lceil \ln n/\ln(1/p_2) \rceil$ and $L = \lceil n^\rho/p_1 \rceil$. If some $x^*$ has $s(q, x^*) \ge S$, QUERY returns a point $x'$ with $s(q, x') \ge S$ with probability at least $1 - 1/e$. The expected number of candidates with $s(q, x) \le cS$ is at most $L$.

**Theorem (no symmetric family; Shrivastava and Li).** Let the data and the queries both range over a set $D$ that contains a vector $x \neq 0$ with $\|x\|^2 \le cS$. Then for no $p_1 > p_2$ is there a symmetric family with $\Pr[h(x) = h(q)] \ge p_1$ when $q \cdot x \ge S$ and $\le p_2$ when $q \cdot x \le cS$. *Proof.* Take $q = x$. Then $q \cdot x = \|x\|^2 \le cS$, so the family needs $\Pr[h(x) = h(x)] \le p_2$. But $h(x) = h(x)$ always, so $p_2 \ge 1 \ge p_1$. $\square$ The same argument fails for an asymmetric family, since $h^P(x)$ and $h^Q(x)$ are different functions.

## Complexity

Model: real RAM. Preprocessing computes $M$ in $O(nd)$, the maps in $O(nd)$, and $kL$ dot products of length $d + 1$ per point, $O(nLkd)$ in all, with $O(nL)$ table entries and $O(Lkd)$ for the hyperplanes. A query costs $O(Lkd)$ to hash and $O(Cd)$ to check the $C$ candidates. With the parameters of the theorem, $L = O(n^\rho)$, $k = O(\log n)$, and the expected number of candidates below $cS$ is at most $L$, so the expected query time is $O(n^\rho d \log n)$ for constant $S$ and $c$, plus the cost of candidates with $cS < s < S$, which the guarantee does not bound.

| $S$ | $c$ | $p_1$ | $p_2$ | $\rho$ | $k$ | $L$ ($n = 10^6$) |
|---|---|---|---|---|---|---|
| 0.5 | 0.5 | 0.6667 | 0.5804 | 0.7454 | 26 | 44490 |
| 0.8 | 0.5 | 0.7952 | 0.6310 | 0.4978 | 31 | 1220 |
| 0.9 | 0.5 | 0.8564 | 0.6486 | 0.3579 | 32 | 165 |
| 0.9 | 0.8 | 0.8564 | 0.7559 | 0.5537 | 50 | 2452 |

The exponent depends on $S$, a normalized inner product. If the best item has $s$ far below 1, which happens when $\|q\|$ is fixed and the norms of the data vary a lot, $\rho$ is close to 1 and the method gives little over a scan.

## Properties

- **Randomized, one-sided.** Every returned point has its true inner product checked at line L7; the error is only in missing the best point.
- **Exact candidates.** The answer is the exact best among the candidates, so more tables can only improve it.
- **Scale invariant.** Multiplying all data by a positive number, or the query by a positive number, changes nothing, since $M$ and $\|q\|$ absorb it.
- **Static.** A new point with norm above $M$ changes $M$ and therefore every $P(x)$; the index must be rebuilt, or $M$ chosen with room to spare.

## Variants and improvements

- **L2-ALSH** (above) with [E2LSH](/e2lsh/), and a variant with sign projections after a similar transformation, by Shrivastava and Li.
- **Norm ranges.** Split the data by norm into groups and build one index per group with its own $M$; this keeps $s$ large for the best item of each group and improves $\rho$ when the norms vary.
- **Graph and quantization methods.** In practice, MIPS is often served by [inverted file indexes](/inverted-file-index/) with quantization tuned for inner products, or by graph indexes run on the transformed vectors $P(x)$, which turns MIPS into nearest neighbor search on the sphere.
- **Exact reduction to nearest neighbor.** Since $\|Q(q) - P(x)\|^2 = 2 - 2 s(q, x)$ for the unit vectors of Lemma 1, the maps reduce exact MIPS to exact Euclidean nearest neighbor search in dimension $d + 1$, so any nearest neighbor index can be used.

## When to use it

- Maximum inner product search over item vectors from matrix factorization or two-tower models, when the best item has a large normalized inner product with the query.
- When an LSH or angular index already exists: the maps are a cheap preprocessing step.
- Prefer a scan for small $n$, and a quantization or graph index when tuned recall per unit of time matters more than a provable guarantee.

## Pitfalls

- **Using cosine LSH without the maps.** Angular hashing on the original vectors finds vectors in the right direction, not the largest inner product, as the example shows for $(1, 1)$ versus $(0, 3)$.
- **Rounding in the extra coordinate.** For $\|x\|$ very close to $M$, $1 - \|x\|^2/M^2$ can come out slightly negative in floating point; clamp it at 0 before the square root.
- **A large $M$ from one outlier.** One long vector makes $M$ large and all $s$ small, which drives $\rho$ toward 1. Handle outliers separately or split by norm.
- **Zero query.** $q = 0$ has no direction; every point is a maximizer, and line L5 divides by zero.

## Implementations

## History

Shrivastava and Li introduced asymmetric LSH in 2014: they proved that no symmetric LSH family exists for inner products and gave L2-ALSH, which appends powers of the norm and uses E2LSH. Neyshabur and Srebro in 2015 gave the simpler pair of maps with $\sqrt{1 - \|x\|^2}$ and 0 and random hyperplanes, and compared it with L2-ALSH.

## References
