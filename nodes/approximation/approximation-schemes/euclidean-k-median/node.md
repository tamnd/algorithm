---
tag: 3ZK1AD
kind: problem
slug: euclidean-k-median
name: Euclidean k-median problem
aliases:
- Euclidean k-median
- geometric k-median
- multi-source Weber problem
area: approximation/approximation-schemes
level: advanced
summary: Choose k centers among points in Euclidean space to minimize the sum of distances from each point to its nearest center.
prereqs: [k-median-problem, metric-space, geometric-median, np-hard]
see_also: [arora-euclidean-k-median-ptas, portal-based-dissection, k-means, k-center-problem, facility-location-problem, coreset, fermat-point, k-median-inapproximability]
sources:
  - paper: "N. Megiddo and K. J. Supowit, On the complexity of some common geometric location problems, SIAM Journal on Computing 13(1), 1984, pp. 182-196"
    title: Megiddo and Supowit 1984
    locator: the NP-hardness of the planar k-median and k-center problems
  - paper: doi:10.1145/276698.276718
    title: S. Arora, P. Raghavan and S. Rao, Approximation schemes for Euclidean k-medians and related problems, STOC 1998, pp. 106-113
    locator: the approximation scheme in the plane and the quasi-polynomial scheme in fixed dimension
  - paper: "V. Guruswami and P. Indyk, Embeddings and non-approximability of geometric problems, SODA 2003, pp. 537-538"
    title: Guruswami and Indyk 2003
    locator: no approximation scheme for k-median in dimension Θ(log n) unless P = NP
  - paper: "C. Bajaj, The algebraic degree of geometric optimization problems, Discrete and Computational Geometry 3, 1988, pp. 177-191"
    title: Bajaj 1988
    locator: the Fermat-Weber point is not computable by radicals in general
  - paper: "S. Har-Peled and S. Mazumdar, On coresets for k-means and k-median clustering, STOC 2004, pp. 291-300"
    title: Har-Peled and Mazumdar 2004
    locator: coresets of small size for k-median in fixed dimension
---

The Euclidean $k$-median problem asks for $k$ centres in $\mathbb{R}^d$ that minimize the total distance from the input points to their nearest centres. It is the [$k$-median problem](/k-median-problem/) in the Euclidean [metric](/metric-space/), and for $k = 1$ it is the problem of the [geometric median](/geometric-median/), also called the Fermat-Weber point. The problem is [NP-hard](/np-hard/) in the plane when $k$ is part of the input (Megiddo and Supowit 1984). In fixed dimension it has approximation schemes, the first by Arora, Raghavan and Rao (1998) with [portal-based dissection](/portal-based-dissection/); in dimension $\Theta(\log n)$ it has none unless P = NP.

## In plain words

A town wants to open a few clinics. Each household walks to the nearest clinic, and the town wants the total walking distance to be as small as possible. The clinics can stand anywhere on the map.

With one clinic the best place is a kind of middle point of all the homes, but there is no simple formula for it. With many clinics, the hard part is to decide which homes share a clinic. On a single straight road the homes split into runs of neighbours, and each run puts its clinic at its middle home, so the problem is easy. On a map it is hard. Good answers are still possible: we can come as close to the best as we like, in a time that grows quickly as we ask for more precision.

## Definition

**Input.** A set $P$ of $n$ points in $\mathbb{R}^d$ and an integer $k \ge 1$.

**Output.** A set $C$ of at most $k$ centres in $\mathbb{R}^d$.

**Goal.** Minimize
$$\mathrm{cost}(C) = \sum_{p \in P} \min_{c \in C} \lVert p - c \rVert,$$
with $\lVert \cdot \rVert$ the Euclidean norm. The least value is $\mathrm{OPT}$. The centres split $P$ into *clusters*: each point belongs to the cluster of its nearest centre.

*Ratio convention.* This is a minimization problem. An algorithm has ratio $\rho \ge 1$ if $\mathrm{ALG} \le \rho \cdot \mathrm{OPT}$ on every instance. An approximation scheme has ratio $1 + \varepsilon$ for each fixed $\varepsilon > 0$.

| symbol | meaning |
|---|---|
| $n$, $d$, $k$ | the number of points, the dimension, and the number of centres |
| $P$, $C$ | the input points and the chosen centres |
| $\mathrm{OPT}$, $\mathrm{ALG}$ | the optimal cost and the cost of an algorithm |

## Variants

- **Continuous and discrete.** In the continuous form, as above, the centres can be anywhere. In the discrete form they must be chosen from a given candidate set, often $P$ itself. Choosing them from $P$ loses at most a factor 2 (see Reductions).
- **One centre.** For $k = 1$ the cost is convex, and the optimum is the geometric median. For three points it is the [Fermat point](/fermat-point/). In general the optimum cannot be written with radicals (Bajaj 1988), so exact algorithms compute it only to a given precision, for example by Weiszfeld's iteration or by convex optimization.
- **Points on a line.** For $d = 1$ the clusters of an optimal solution are runs of the sorted points, and each run has its centre at a median point. A dynamic program over the runs is exact in $O(k n^2)$ time.
- **Weights and outliers.** Points may have weights, which multiply their distances, or the solution may ignore up to $z$ points.
- **Other objectives.** The sum of squared distances gives [$k$-means](/k-means/), the largest distance gives the [$k$-center problem](/k-center-problem/), and an opening cost for each centre in place of the bound $k$ gives the [facility location problem](/facility-location-problem/).

## Examples

**Points on a line.** Take the points $1, 2, 3, 10, 11, 20$.

| $k$ | clusters | centres | cost |
|---|---|---|---|
| 1 | $\{1, 2, 3, 10, 11, 20\}$ | 3 | $2 + 1 + 0 + 7 + 8 + 17 = 35$ |
| 2 | $\{1, 2, 3\}$, $\{10, 11, 20\}$ | 2, 11 | $2 + 10 = 12$ |
| 3 | $\{1, 2, 3\}$, $\{10, 11\}$, $\{20\}$ | 2, 10, 20 | $2 + 1 + 0 = 3$ |

For $k = 1$ any point between the third and the fourth point is also optimal; every median of the multiset is a minimizer.

**The triangle.** Take the corners of an equilateral triangle of side 1 and $k = 1$. The best centre is the centre of the triangle, at distance $1/\sqrt 3$ from each corner, with cost $\sqrt 3 \approx 1.732$. The best corner has cost 2. So the discrete form costs $2/\sqrt 3 \approx 1.155$ times more here.

## Known algorithms

| algorithm | ratio | setting | time |
|---|---|---|---|
| dynamic program over runs | exact | $d = 1$ | $O(k n^2)$ |
| trying all sets of $k$ input points | 2 | any $d$ | $O(n^{k+1} d)$ |
| local search with $p$ swaps | $3 + 2/p$ | any metric | polynomial for fixed $p$ |
| [Arora, Raghavan and Rao 1998](/arora-euclidean-k-median-ptas/) | $1 + \varepsilon$ | $d = 2$ | $n^{O(1/\varepsilon + 1)}$ |
| Arora, Raghavan and Rao 1998 | $1 + \varepsilon$ | fixed $d$ | $n^{O((\log n/\varepsilon)^{d-1})}$, quasi-polynomial |
| Kolliopoulos and Rao 1999 | $1 + \varepsilon$ | fixed $d$ | $2^{O((\log(1/\varepsilon)/\varepsilon)^{d-1})} n \log^{d+6} n$ |
| [coresets](/coreset/) and exhaustive search | $1 + \varepsilon$ | fixed $d$ and $k$ | linear in $n$ plus a term in $k$ and $\varepsilon$ |

**The dynamic program on a line.** Sort the points as $x_1 \le \cdots \le x_n$. On a line, the points nearest to one centre form an interval between two midpoints of consecutive centres, so the clusters of an optimal solution are runs. The best centre of the run $x_i, \ldots, x_j$ is its median, and its cost comes from prefix sums in $O(1)$. Let $F(c, j)$ be the best cost of $x_1, \ldots, x_j$ with $c$ runs. Then $F(c, j) = \min_{i < j} F(c - 1, i) + \mathrm{run}(i + 1, j)$, which gives $O(k n^2)$ time.

## Bounds

- **NP-hardness.** The problem is NP-hard in the plane when $k$ is part of the input, for both the continuous and the discrete form (Megiddo and Supowit 1984).
- **No scheme in high dimension.** For $d = \Theta(\log n)$ there is no approximation scheme unless P = NP (Guruswami and Indyk 2003). So the dependence on $d$ in the exponent of the schemes cannot be removed in general.
- **General metrics.** In an arbitrary metric, $k$-median has no ratio below $1 + 2/e$ unless P = NP; see [k-median inapproximability](/k-median-inapproximability/). The Euclidean structure is what allows approximation schemes.
- **Fixed $k$.** For fixed $k$ the discrete form is polynomial, since there are only $\binom{n}{k}$ sets of input points to try, and approximation schemes exist in any dimension.

## Reductions

**Input points as centres, at a factor 2.** Let $C$ be any solution and $c \in C$ a centre with cluster $Q$. Let $q^*$ be the point of $Q$ nearest to $c$. For every $p \in Q$, $\lVert p - q^* \rVert \le \lVert p - c \rVert + \lVert c - q^* \rVert \le 2 \lVert p - c \rVert$. So replacing each centre by the nearest point of its cluster at most doubles the cost, and the discrete form on $P$ has optimum at most $2\,\mathrm{OPT}$. The triangle example shows that some loss is unavoidable.

**To a polynomial candidate set.** For fixed $d$ and $\varepsilon$, a set of candidate centres of size polynomial in $n$, built from grids around the input points, contains $k$ centres of cost at most $(1 + \varepsilon)\,\mathrm{OPT}$. This turns the continuous form into the discrete one at a small loss, and the scheme of Arora, Raghavan and Rao uses such grids.

**From satisfiability.** Megiddo and Supowit prove NP-hardness by a reduction from a satisfiability problem, with gadgets of points whose optimal centres encode the truth values.

## Applications

- Facility location without opening costs: placing warehouses, clinics or base stations to minimize the total travel distance.
- Clustering that is robust to outliers: the sum of distances, unlike the sum of squares of $k$-means, gives a far point a linear rather than a quadratic weight.
- Compression of point sets, where each point is replaced by its centre and the total error is the sum of the distances.

## References
