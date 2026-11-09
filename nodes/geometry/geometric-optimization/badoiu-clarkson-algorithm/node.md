---
tag: NMY7GA
kind: algorithm
slug: badoiu-clarkson-algorithm
name: Badoiu-Clarkson algorithm
aliases:
- Badoiu-Clarkson core-set algorithm
- Bădoiu-Clarkson algorithm
- Badoiu-Clarkson iteration
- farthest-point iteration for the minimum enclosing ball
area: geometry/geometric-optimization
level: advanced
summary: Iterative (1+ε)-approximation of the minimum enclosing ball in any dimension. Each step moves the center toward the farthest point; ⌈1/ε²⌉ steps suffice, whatever n and d are.
solves: [minimum-enclosing-ball]
model: real-ram
complexity:
  vars: {n: the number of points, d: the dimension, k: "the number of centers, ⌈1/ε²⌉ for a (1+ε)-approximation"}
  time: {worst: O(k n d)}
  space: {extra: O(k + d)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 2003
  people: [Mihai Bădoiu, Kenneth L. Clarkson]
  note: Bădoiu and Clarkson gave the farthest-point iteration with step 1/(i+1), its bound r/sqrt(i) on the distance to the optimal center, and core sets of size O(1/ε).
prereqs: [minimum-enclosing-ball, coreset]
see_also: [minimum-enclosing-circle, welzls-algorithm, clarksons-algorithm, khachiyans-algorithm, minimum-volume-enclosing-ellipsoid, lp-type-problem, geometric-median, weiszfelds-algorithm]
sources:
  - paper: "Mihai Bădoiu and Kenneth L. Clarkson, Smaller core-sets for balls, Proceedings of the 14th ACM-SIAM Symposium on Discrete Algorithms (SODA), 2003, pages 801 to 802"
    locator: the iteration c_(i+1) = c_i + (p_i − c_i)/(i + 1) with p_i the farthest point, the bound |c_i − c*| ≤ r*/sqrt(i), and a core set of size O(1/ε)
  - paper: "Mihai Bădoiu and Kenneth L. Clarkson, Optimal core-sets for balls, Computational Geometry: Theory and Applications 40(1), 2008"
    locator: every point set has an ε-core-set of size ⌈1/ε⌉, this is tight in the worst case, and an algorithm finds one of size at most 2/ε
  - paper: "Mihai Bădoiu, Sariel Har-Peled and Piotr Indyk, Approximate clustering via core-sets, Proceedings of the 34th ACM Symposium on Theory of Computing (STOC), 2002"
    locator: core sets of size O(1/ε²) for the minimum enclosing ball, independent of n and d, and their use for k-center clustering
  - paper: "Kenneth L. Clarkson, Coresets, sparse greedy approximation, and the Frank-Wolfe algorithm, ACM Transactions on Algorithms 6(4), 2010"
    locator: the minimum enclosing ball as a concave maximization over the simplex, and the Bădoiu-Clarkson iteration as a Frank-Wolfe method with step 1/(i+1)
  - paper: "Piyush Kumar, Joseph S. B. Mitchell and E. Alper Yıldırım, Approximate minimum enclosing balls in high dimensions using core-sets, ACM Journal of Experimental Algorithmics 8, 2003"
    locator: core sets of size O(1/ε) computed with second-order cone programming, and experiments in high dimension
---

The Bădoiu-Clarkson algorithm computes an approximate [minimum enclosing ball](/minimum-enclosing-ball/) of $n$ points in $\mathbb{R}^d$. It starts with the center at an input point. In step $i$ it finds the input point farthest from the current center and moves the center toward it by the fraction $1/(i + 1)$ of the distance. After the step that gives the $k$-th center, that center is at distance at most $r^*/\sqrt{k}$ from the optimal center, where $r^*$ is the optimal radius. So $k = \lceil 1/\varepsilon^2 \rceil$ centers give a ball of radius at most $(1 + \varepsilon) r^*$, in $O(nd/\varepsilon^2)$ time. The number of steps depends neither on $n$ nor on $d$. The farthest points that the algorithm picks form a [core set](/coreset/): a set of $O(1/\varepsilon^2)$ input points whose own smallest ball, slightly enlarged, holds all the input. Bădoiu and Clarkson also proved that core sets of size $\lceil 1/\varepsilon \rceil$ always exist.

## In plain words

You want the smallest ball around a cloud of points in many dimensions, where exact methods are too slow.

Put a center on any point. Find the point farthest from the center and walk toward it, but only part of the way: half the way the first time, a third the second time, a quarter the third time, and so on. The far points pull the center toward the middle of the cloud, and the shrinking steps make the center settle down.

After 100 steps the center is close enough to the true center that a ball around it, just large enough to hold every point, is at most 10 percent larger than the best ball. This holds for any number of points in any number of dimensions. The points that pulled the center are a small set that already shows the shape of the whole cloud.

## The problem

Notation: $P = \{p_1, \dots, p_n\}$ is the input, a nonempty set of points in $\mathbb{R}^d$; $|x - y|$ is the Euclidean distance. The minimum enclosing ball $B^* = B(c^*, r^*)$ is the smallest closed ball that contains $P$; it is unique. Given $\varepsilon > 0$, a $(1 + \varepsilon)$-approximation is a ball $B(c, R)$ that contains $P$ with $R \le (1 + \varepsilon) r^*$. The measure is the radius in the Euclidean norm; the volume of the ball is then within the factor $(1 + \varepsilon)^d$.

No general position is assumed. Duplicate points, points in a lower-dimensional flat and many points on one sphere are all allowed. The implementation takes integer or rational coordinates and computes every center exactly with rationals, because after $i$ steps the center is the average of $i$ input points.

## The algorithm

```pseudo id=main
BADOIU-CLARKSON(P, k)               ▷ returns the center c_k, its radius and the chosen points
L1  c₁ ← p₁                          ▷ any input point
L2  for i ← 1 to k − 1 do
L3      q_i ← a point of P farthest from c_i
L4      c_{i+1} ← c_i + (q_i − c_i) / (i + 1)
L5  return c_k, max over p in P of |p − c_k|, and {p₁, q₁, …, q_{k−1}, q_k}
```

Here $q_k$ is the point farthest from $c_k$, found while computing the radius on L5. By induction on L4, $c_{i+1} = (i\,c_i + q_i)/(i + 1)$, so

$$c_k = \frac{p_1 + q_1 + \dots + q_{k-1}}{k},$$

the average of the start point and the first $k - 1$ farthest points. With $k = \lceil 1/\varepsilon^2 \rceil$, the ball $B(c_k, \max_{p} |p - c_k|)$ is a $(1 + \varepsilon)$-approximation.

## Example

Take $P = \{(0, 0), (10, 0), (0, 6), (4, 8), (9, 7), (5, 3)\}$. The exact minimum enclosing disk has center $c^* = (5, 3)$ and $r^{*2} = 34$, so $r^* \approx 5.831$; the points $(0, 0)$, $(10, 0)$ and $(0, 6)$ lie on its circle. Ties for the farthest point go to the first point in the list.

| $k$ | center $c_k$ | farthest point $q_k$ | $\max_p \lvert p - c_k \rvert^2$ | radius | $\lvert c_k - c^* \rvert^2$ | bound $r^{*2}/k$ |
|---|---|---|---|---|---|---|
| 1 | $(0, 0)$ | $(9, 7)$ | $130$ | $11.402$ | $34$ | $34$ |
| 2 | $(9/2, 7/2)$ | $(10, 0)$ | $85/2$ | $6.519$ | $1/2$ | $17$ |
| 3 | $(19/3, 7/3)$ | $(0, 6)$ | $482/9$ | $7.318$ | $20/9$ | $11.33$ |
| 4 | $(19/4, 13/4)$ | $(10, 0)$ | $305/8$ | $6.175$ | $1/8$ | $8.5$ |
| 5 | $(29/5, 13/5)$ | $(0, 6)$ | $226/5$ | $6.723$ | $4/5$ | $6.8$ |
| 6 | $(29/6, 19/6)$ | $(10, 0)$ | $661/18$ | $6.060$ | $1/18$ | $5.67$ |

At $k = 4$ the center is $(0 + 9 + 10 + 0, 0 + 7 + 0 + 6)/4 = (19/4, 13/4)$, the average of the first four chosen points, and the radius is within $6.175/5.831 \approx 1.059$ of the optimum. The guarantee for $k = 4$ is $1 + 1/\sqrt{4} = 1.5$. The radius does not decrease monotonically: the center swings between the far corners while it closes in on $c^*$. In practice one keeps the best center seen so far.

## Correctness

The full proof is in [proofs/correctness](proofs/correctness.md). Write $\delta_i = |c_i - c^*|$.

**Lemma 1 (a far point exists).** For every point $c$, some $p \in P$ has $|p - c|^2 \ge r^{*2} + |c - c^*|^2$. The optimal center $c^*$ lies in the convex hull of the points of $P$ on the sphere of $B^*$; if every such point $p$ had $\langle p - c^*, c - c^* \rangle > 0$, the convex combination that gives $c^*$ would give $0 > 0$. A point with $\langle p - c^*, c - c^* \rangle \le 0$ satisfies the claim by the law of cosines.

**Lemma 2 (one step).** $\delta_{i+1}^2 \le (i^2 \delta_i^2 + r^{*2})/(i + 1)^2$. Write $u = c_i - c^*$ and $v = q_i - c_i$. Since $q_i \in B^*$, $|u + v|^2 \le r^{*2}$, so $2\langle u, v \rangle \le r^{*2} - |u|^2 - |v|^2$. Since $q_i$ is the farthest point, Lemma 1 gives $|v|^2 \ge r^{*2} + |u|^2$. Expand $\delta_{i+1}^2 = |u + v/(i + 1)|^2$ and use both inequalities.

**Theorem.** $\delta_k^2 \le r^{*2}/k$ for every $k \ge 1$, and every point of $P$ is within $(1 + 1/\sqrt{k})\, r^*$ of $c_k$. Put $e_i = i^2 \delta_i^2$. Lemma 2 says $e_{i+1} \le e_i + r^{*2}$, and $e_1 = \delta_1^2 \le r^{*2}$ because $c_1 = p_1 \in B^*$. So $e_k \le k\, r^{*2}$. Every point $p$ has $|p - c_k| \le |p - c^*| + \delta_k \le r^* + r^*/\sqrt{k}$.

**Core set.** Let $S$ be the chosen points returned on L5, with smallest ball $B(c_S, r_S)$. The argument above uses only that each $q_i$ lies in the optimal ball and is at least as far from $c_i$ as every point of the set. Both hold for $S$ in place of $P$, so $|c_k - c_S| \le r_S/\sqrt{k}$ and $|q_k - c_k| \le (1 + 1/\sqrt{k})\, r_S$. Since $q_k$ is the farthest point of $P$ from $c_k$, every point of $P$ lies within $(1 + 2/\sqrt{k})\, r_S$ of $c_S$. So $S$, with $k + 1$ points, is a $2/\sqrt{k}$-core set.

## Complexity

- **Time.** Each of the $k$ farthest-point searches (on L3 and L5) computes $n$ distances in $d$ coordinates, $O(nd)$. Step L4 costs $O(d)$. Total $O(knd)$, which is $O(nd/\varepsilon^2)$ for $k = \lceil 1/\varepsilon^2 \rceil$. The time is linear in the input size $nd$ for fixed $\varepsilon$.
- **Space.** $O(d)$ for the center and $O(k)$ for the indices of the chosen points, besides the input.
- **Exact arithmetic.** The center $c_i$ is a sum of $i$ input points divided by $i$, so with integer input of absolute value at most $M$ its coordinates are fractions with denominator $i$ and numerators below $iM$; squared distances compare exactly at little extra cost.
- **Convergence rate.** The bound $\delta_k \le r^*/\sqrt{k}$ is sublinear: halving $\varepsilon$ takes four times the steps. Faster methods trade simplicity for a better dependence on $\varepsilon$ (see Variants).

## Properties

- **Independent of $n$ and $d$.** The number of steps for a given $\varepsilon$ is the same in any dimension and for any number of points, which is why the method suits high dimension, where exact algorithms such as [Welzl's](/welzls-algorithm/) take time exponential in $d$.
- **Deterministic and simple.** Only distance computations; no linear algebra and no linear programming.
- **Few passes.** Each step is one pass over the data; the algorithm keeps only the current center.
- **Not monotone.** The radius $\max_p |p - c_i|$ can go up from one step to the next; the guarantee is for the center after $k$ steps, and the best center seen is at least as good.
- **A Frank-Wolfe method.** The squared radius problem has the dual $\max_{\lambda} \sum_j \lambda_j |p_j|^2 - |\sum_j \lambda_j p_j|^2$ over the probability simplex, with $c = \sum_j \lambda_j p_j$. A Frank-Wolfe step moves $\lambda$ toward the vertex of the farthest point, and with step size $1/(i + 1)$ it is exactly L4 (Clarkson 2010).

## Variants and improvements

- **Core sets of size $O(1/\varepsilon)$.** Keep a set $S$; compute the exact smallest ball of $S$, add the farthest point of $P$ from its center, and stop when that point is within $(1 + \varepsilon)$ times the radius. Bădoiu and Clarkson showed that a method of this kind finds a core set of size at most $2/\varepsilon$, and that every point set has an $\varepsilon$-core set of size $\lceil 1/\varepsilon \rceil$, which is tight in the worst case; the vertices of a regular simplex show that $\Omega(1/\varepsilon)$ points can be needed (see [core set](/coreset/)). The exact ball of $S$ is a problem on $O(1/\varepsilon)$ points, solved by second-order cone programming (Kumar, Mitchell and Yıldırım 2003).
- **Line search.** Choosing the step on L4 to minimize the radius along the segment, or using away steps, as in Yıldırım (2008), gives faster convergence in practice and linear convergence in some settings.
- **Faster first-order methods.** Accelerated gradient methods on a smoothed form of the problem improve the dependence on $\varepsilon$ from $1/\varepsilon^2$ to about $1/\sqrt{\varepsilon}$ passes, at the cost of a more complex step.
- **Streaming.** With one pass and $O(d)$ memory, a simple rule that grows the ball just enough to cover each new point outside it gives a $3/2$-approximation (Zarrabi-Zadeh and Chan 2006), and later analyses give better constants; the iteration here needs $k$ passes.
- **k-center clustering.** Core sets of size independent of $n$ and $d$ give $(1 + \varepsilon)$-approximations for the $k$-center problem with $k$ balls in time $2^{O((k \log k)/\varepsilon^2)} dn$ (Bădoiu, Har-Peled and Indyk 2002).
- **Ellipsoids.** For the [minimum volume enclosing ellipsoid](/minimum-volume-enclosing-ellipsoid/), [Khachiyan's algorithm](/khachiyans-algorithm/) is the analogous farthest-point method, with the farthest point measured in the norm of the current ellipsoid.

## When to use it

- **High dimension.** For $d$ in the tens or thousands and moderate accuracy, a few hundred passes over the data give a ball within a few percent of the optimum.
- **A quick bound.** Ten steps give a ball within a factor $1 + 1/\sqrt{10} \approx 1.32$ and a certificate: the lower bound $r^* \ge |c_k - q_k| / (1 + 1/\sqrt{k})$.
- **Not in the plane.** For $d = 2$ or $3$ the exact answer by [Welzl's algorithm](/welzls-algorithm/) takes expected $O(n)$ time and is simpler to trust.
- **Not for high accuracy.** For $\varepsilon = 10^{-6}$ the $10^{12}$ steps are too many; use the core-set method with an exact solver, or second-order cone programming.

## Pitfalls

- **Step size.** The proof needs the step $1/(i + 1)$, counted from $i = 1$ at the start point. A constant step, such as moving half way every time, does not converge to $c^*$.
- **Off by one.** $k = \lceil 1/\varepsilon^2 \rceil$ is the number of centers, so the loop runs $k - 1$ times. Running only $1/\varepsilon^2 - 1$ steps when $1/\varepsilon^2$ is not an integer misses the bound.
- **Reporting the last radius.** The bound is on the radius at $c_k$; the radius at an earlier center may be smaller, and it is safe to report the minimum over all centers, but not a value at a center that was not checked against all points.
- **Floating point.** In floating point the farthest point may be misidentified when distances nearly tie; this only changes which point pulls, and Lemma 1 still holds approximately, but the exact bound $\delta_k^2 \le r^{*2}/k$ then holds only up to rounding. The implementation uses rationals.
- **Volume versus radius.** A $(1 + \varepsilon)$ bound on the radius is a $(1 + \varepsilon)^d$ bound on the volume, which is large in high dimension.

## Implementations

## History

Bădoiu, Har-Peled and Indyk (STOC 2002) showed that the minimum enclosing ball has core sets whose size depends only on $\varepsilon$, of size $O(1/\varepsilon^2)$, and used them for clustering in high dimension. Bădoiu and Clarkson (SODA 2003) gave the simple farthest-point iteration with step $1/(i + 1)$ and its analysis, and core sets of size $O(1/\varepsilon)$; their journal paper (2008) proved that $\lceil 1/\varepsilon \rceil$ points always suffice and that this is tight. Kumar, Mitchell and Yıldırım (2003) made the core-set method practical with second-order cone programming. Clarkson (2010) and Yıldırım (2008) placed the iteration in the Frank-Wolfe framework of sparse greedy approximation over the simplex, which also explains its connection to [Khachiyan's algorithm](/khachiyans-algorithm/) for ellipsoids.

## References
