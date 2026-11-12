---
tag: 879EXX
kind: algorithm
slug: karlin-klein-oveis-gharan-algorithm
name: Karlin-Klein-Oveis Gharan algorithm
aliases:
- KKO algorithm
- (3/2 - epsilon) metric TSP algorithm
- max entropy algorithm for TSP
area: approximation/tsp-approximation
level: research
summary: Sample a max entropy spanning tree with the marginals of the subtour LP, then fix the parity as Christofides does. KKO proved an expected ratio of 3/2 minus 10^(-36) for metric TSP.
solves: [metric-tsp]
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: poly(n)}
  space: {extra: poly(n)}
properties: {deterministic: false, recursive: false, online: false}
history:
  year: 2020
  people: [Anna R. Karlin, Nathan Klein, Shayan Oveis Gharan]
  note: The paper was posted in 2020 and published at STOC 2021; the bound with respect to the subtour LP followed at FOCS 2022.
prereqs: [metric-tsp, christofides-algorithm, subtour-elimination-lp, spanning-tree-polytope, matrix-tree-theorem, minimum-weight-perfect-matching]
see_also: [christofides-algorithm, asadpour-atsp-algorithm, held-karp-bound, subtour-elimination-lp, uniform-spanning-tree-sampling, randomized-rounding, metric-tsp-inapproximability, integrality-gap]
sources:
  - paper: doi:10.1145/3406325.3451009
    title: Anna R. Karlin, Nathan Klein and Shayan Oveis Gharan, A (slightly) improved approximation algorithm for metric TSP, STOC 2021
    locator: pages 32 to 45 (Algorithm 1, the max entropy algorithm, and the main theorem with epsilon above 10^(-36))
  - title: Anna R. Karlin, Nathan Klein and Shayan Oveis Gharan, A (slightly) improved bound on the integrality gap of the subtour LP for TSP, FOCS 2022
    locator: pages 832 to 843 (the expected cost of the max entropy algorithm against the subtour LP)
  - title: Shayan Oveis Gharan, Amin Saberi and Mohit Singh, A randomized rounding approach to the traveling salesman problem, FOCS 2011
    locator: the max entropy algorithm for graphic TSP and its ratio 3/2 minus a constant
  - paper: doi:10.1287/opre.2017.1603
    title: Arash Asadpour, Michel X. Goemans, Aleksander Mądry, Shayan Oveis Gharan and Amin Saberi, An O(log n/log log n)-approximation algorithm for the asymmetric traveling salesman problem, Operations Research 65(4), 2017
    locator: pages 1043 to 1061 (the maximum entropy distribution of spanning trees with given marginals, and how to compute and sample it)
  - title: Laurence A. Wolsey, Heuristic analysis, linear programming and branch and bound, Mathematical Programming Study 13, 1980
    locator: pages 121 to 134 (the matching costs at most half of the subtour LP)
  - title: Jack Edmonds and Ellis L. Johnson, Matching, Euler tours and the Chinese postman, Mathematical Programming 5, 1973
    locator: pages 88 to 124 (the polyhedron of T-joins)
---

The Karlin-Klein-Oveis Gharan algorithm is a randomized approximation algorithm for [metric TSP](/metric-tsp/) with an expected ratio of $\tfrac{3}{2} - \varepsilon$ for a constant $\varepsilon > 10^{-36}$. It is the first proved improvement on the ratio 3/2 of [Christofides' algorithm](/christofides-algorithm/) since 1976. It solves the [subtour elimination LP](/subtour-elimination-lp/), samples a random spanning tree whose edge probabilities follow the LP solution, and then adds a [minimum weight perfect matching](/minimum-weight-perfect-matching/) on the odd vertices and shortcuts, as Christofides does. This page proves the simpler bound $\mathbb{E}[\text{ALG}] \le \tfrac{3}{2} \cdot \text{LP}^*$ for the code on this page, and gives only an outline of the step from $\tfrac{3}{2}$ to $\tfrac{3}{2} - 10^{-36}$.

## In plain words

Christofides' method picks the cheapest tree that connects all the cities and then repairs the cities with an odd number of roads. That repair can cost half of the best trip, and for more than forty years nobody could prove a better bound.

This method picks the tree at random instead. First it solves a relaxed version of the problem, in which a trip can use a road in part. The answer says how much each road "wants" to be in the trip. The method then picks a random tree in which each road appears with about that chance, and otherwise the trees are as mixed as possible. Such a random tree is often already balanced, so the repair is cheaper on average. The gain proved so far is extremely small, but it showed that the old bound is not the limit.

## The problem

The input is a set $V$ of $n \ge 3$ vertices with costs $c(u, v) = c(v, u) \ge 0$ that satisfy the [triangle inequality](/triangle-inequality/). The output is a tour through all vertices. OPT is the least cost of a tour, ALG the cost of the output, and LP* the value of the subtour elimination LP, which is the [Held-Karp bound](/held-karp-bound/), with $\text{LP}^* \le \text{OPT}$. The algorithm is randomized, so the ratio $\rho$ here means $\mathbb{E}[\text{ALG}] \le \rho \cdot \text{OPT}$ on each instance, where the expectation is over the random choices of the algorithm.

## The algorithm

```pseudo id=main
MAX-ENTROPY-TOUR(V, c)
L1  x ← an optimal solution of the subtour elimination LP for (V, c)
L2  z ← (1 − 1/n) · x                     ▷ now z is a point of the spanning tree polytope
L3  λ ← weights on the support of x with Pr_λ[e ∈ T] = z_e for each edge e
L4  T ← a random spanning tree with Pr[T] proportional to the product of λ_e over e in T
L5  O ← the vertices of odd degree in T
L6  J ← a minimum weight perfect matching of the complete graph on O
L7  W ← an Euler circuit of the multigraph T + J
L8  H ← the vertices of W, each kept only at its first visit
L9  return H
```

Line L1 gives a point $x$ with $x(\delta(v)) = 2$ at each vertex and $x(\delta(S)) \ge 2$ for each cut. The sum of all $x_e$ is $n$, one more than the number of edges of a spanning tree, so line L2 scales $x$ down by the factor $1 - 1/n$. The scaled point $z$ is in the [spanning tree polytope](/spanning-tree-polytope/) of the support graph, in its relative interior.

Lines L3 and L4 are the random part. A distribution of the form $\Pr[T] \propto \prod_{e \in T} \lambda_e$ is called $\lambda$-uniform; for $\lambda = 1$ it is the [uniform spanning tree](/uniform-spanning-tree-sampling/). Among all distributions of spanning trees with the marginals $z$, the one of largest entropy is $\lambda$-uniform for some $\lambda$, and line L3 finds these weights. The weights solve a [convex optimization](/convex-optimization/) problem: minimize $\log \sum_T \exp(\gamma(T)) - \gamma \cdot z$ over $\gamma = \log \lambda$. Its gradient is the vector of marginals minus $z$, so its minimum is where the marginals are $z$. The code uses [Newton's method](/newton-method-for-systems/) on this function.

Lines L5 to L8 are the same as in Christofides' algorithm. Only the tree is different: a random tree that follows the LP, not a minimum spanning tree.

The algorithm of Karlin, Klein and Oveis Gharan differs from these lines in one detail. Instead of the scale factor of line L2, they split one vertex into two copies joined by an edge of cost 0, so that the LP solution itself gives the marginals. The form on this page, with the factor $1 - 1/n$, is the form of Asadpour et al. and of Oveis Gharan, Saberi and Singh. The proof outline of the ratio $\tfrac{3}{2} - 10^{-36}$ refers to the form of KKO.

## Example

Six vertices $A, \ldots, F$ with these costs. They are the instance of the [Held-Karp bound](/held-karp-bound/) page, and OPT $= 11$.

| | $A$ | $B$ | $C$ | $D$ | $E$ | $F$ |
|---|---|---|---|---|---|---|
| $A$ | 0 | 3 | 2 | 3 | 1 | 2 |
| $B$ | 3 | 0 | 2 | 2 | 2 | 1 |
| $C$ | 2 | 2 | 0 | 2 | 3 | 2 |
| $D$ | 3 | 2 | 2 | 0 | 3 | 3 |
| $E$ | 1 | 2 | 3 | 3 | 0 | 3 |
| $F$ | 2 | 1 | 2 | 3 | 3 | 0 |

One run with the seed 2021 in the code on this page:

| line | result |
|---|---|
| L1 | $x = 1$ on $AE$, $BF$, $CD$ and $x = 1/2$ on $AC$, $AF$, $BD$, $BE$, $CF$, $DE$; LP* $= 21/2$ |
| L2 | $z = 5/6$ on the three edges with $x = 1$ and $z = 5/12$ on the other six |
| L3 | $\lambda = 9/2$ on $AE$, $BF$, $CD$ and $\lambda = 1$ on the other six (weights are fixed only up to a common factor) |
| L4 | $T = \{AE, BE, BF, CD, DE\}$, of cost 9 and probability $3/64$ |
| L5 | the degrees are $A{:}1$, $B{:}2$, $C{:}1$, $D{:}2$, $E{:}3$, $F{:}1$, so $O = \{A, C, E, F\}$ |
| L6 | $J = \{AE, CF\}$, of cost 3; the edge $AE$ is now in $T + J$ two times |
| L7 | $W = A\,E\,B\,F\,C\,D\,E\,A$, of cost $9 + 3 = 12$ |
| L8 | $H = A\,E\,B\,F\,C\,D$, of cost 11, which is optimal |

The support of $x$ has 75 spanning trees. With the weights of line L3, the trees that hold one, two or three of the edges with $x = 1$ have the total probabilities $1/16$, $3/8$ and $9/16$. So each of these three edges is in $T$ with probability $\tfrac{1}{3}(1/16 + 2 \cdot 3/8 + 3 \cdot 9/16) = 5/6$, as line L3 asks. Over all 75 trees, exactly:

| quantity | value |
|---|---|
| $\mathbb{E}[c(T)]$ | $35/4 = (1 - 1/6) \cdot 21/2$ |
| $\mathbb{E}[c(J)]$ | $2651/864 \approx 3.07$, and $c(J) \le 5 \le \text{LP}^*/2$ for each tree |
| $\Pr[\text{ALG} = 11, 12, 13, 14]$ | $73/96$, $5/24$, $23/864$, $1/216$ |
| $\mathbb{E}[\text{ALG}]$ | $4871/432 \approx 11.28$, against the proved bound $35/4 + 21/4 = 14$ |

On this instance Christofides' algorithm gives 11 and the [double-tree algorithm](/double-tree-algorithm/) gives 14.

## Correctness

**Theorem (proved here).** For metric costs, the tour of MAX-ENTROPY-TOUR has

$$\mathbb{E}[\text{ALG}] \le \Big(1 - \frac{1}{n}\Big)\text{LP}^* + \frac{\text{LP}^*}{2} < \frac{3}{2}\,\text{LP}^* \le \frac{3}{2}\,\text{OPT}.$$

The proof uses the lower bound LP* in both parts.

1. **The tree.** Each edge $e$ is in $T$ with probability $z_e$, so by linearity $\mathbb{E}[c(T)] = c \cdot z = (1 - 1/n)\,\text{LP}^*$. Only the marginals are used here, not the entropy.
2. **The matching (Wolsey 1980).** For each spanning tree $T$, $c(J) \le \text{LP}^*/2$. Each cut $S$ with an odd number of vertices of $O$ has $x(\delta(S)) \ge 2$, so $x/2$ is in the polyhedron of the $O$-joins of Edmonds and Johnson. So some $O$-join costs at most $\text{LP}^*/2$, and by the triangle inequality it shortcuts to a perfect matching of $O$ of no larger cost.
3. **The tour.** The Euler circuit costs $c(T) + c(J)$ and the shortcut step does not add cost.

The full proof, and an outline of the KKO improvement, are in the proof file. The proof file marks the KKO part as an outline: it is cited, not proved.

**The KKO bound (cited).** Karlin, Klein and Oveis Gharan proved $\mathbb{E}[\text{ALG}] \le (\tfrac{3}{2} - \varepsilon)\,\text{OPT}$ for some $\varepsilon > 10^{-36}$ (STOC 2021), and then $\mathbb{E}[\text{ALG}] \le (\tfrac{3}{2} - \varepsilon)\,\text{LP}^*$ (FOCS 2022), which also shows that the [integrality gap](/integrality-gap/) of the subtour LP is below 3/2. The main idea is that the matching of step 2 can be paid with a vector cheaper than $x/2$: a cut that $T$ crosses an even number of times needs no matching edge, and max entropy trees, which are strongly Rayleigh, cross each near minimum cut an even number of times with a constant probability.

**Hardness.** No polynomial algorithm has a ratio below $123/122$ for metric TSP unless P = NP (Karpinski, Lampis and Schmied 2015; see [metric TSP inapproximability](/metric-tsp-inapproximability/)). The integrality gap of the subtour LP is at least $4/3$, so no analysis against LP* can give a ratio below $4/3$.

## Complexity

- **Line L1.** The subtour LP has exponentially many cut constraints, but it can be solved in polynomial time with the [ellipsoid method](/ellipsoid-method/) and a min cut [separation oracle](/separation-oracle/), or as one polynomial size LP with flow variables.
- **Line L3.** The weights are the optimum of a convex program. Asadpour et al. showed how to find $\lambda$ in polynomial time so that the marginals are within a factor $1 + \delta$ of $z$, with a running time polynomial in $n$ and $\log(1/\delta)$.
- **Line L4.** By the [matrix-tree theorem](/matrix-tree-theorem/), the total weight of the spanning trees is a [determinant](/determinant/). Decide the edges one at a time: the probability that $e$ is in $T$, given the choices so far, is a ratio of two such determinants. This takes $O(m)$ determinants of size $n$, for $m$ edges in the support.
- **Lines L5 to L8.** $O(n^3)$ for the matching with the [blossom algorithm](/edmonds-blossom/), and $O(n)$ for the rest.
- **Total.** Polynomial in $n$, in the [word RAM](/word-ram/) with exact or high precision numbers. The degree of the polynomial is large, and no one uses this algorithm for its speed.

The code on this page is for small instances only. It solves the LP exactly with fractions and adds cut constraints over all $2^{n-1}$ subsets, it lists all spanning trees of the support, and it computes the matching by a dynamic program over subsets. This is exponential, but it makes every number in the example exact and easy to check.

## Properties

- **Randomized, ratio in expectation.** The bound holds for the expected cost over the random tree, on each instance. One run can be worse; in the example the worst tree gives 14. Repeat the algorithm and keep the best tour to get the bound with high probability.
- **A bound against the LP.** The proved bound uses LP*, not OPT, so each run also gives the lower bound LP* for free.
- **Only the marginals matter for 3/2.** Any distribution of trees with marginals $z$ gives the bound of this page. The entropy, and the negative dependence that comes with it, matter only for the step below 3/2.
- **Derandomized.** Karlin, Klein and Oveis Gharan also gave a deterministic algorithm with a ratio below 3/2 (IPCO 2023); see [derandomization](/derandomization/) for the general idea.
- **The gain is tiny.** The proved $\varepsilon$ is about $10^{-36}$. In practice the tours are close to those of Christofides' algorithm.

## Variants and improvements

- **Graphic TSP.** Oveis Gharan, Saberi and Singh (2011) introduced the max entropy algorithm for graphic TSP, where the costs are shortest path lengths in an unweighted graph, and proved a ratio of $\tfrac{3}{2} - \varepsilon_0$ for a small constant. For graphic TSP, methods based on ear decompositions later gave 7/5 (Sebő and Vygen 2014).
- **ATSP.** The [Asadpour et al. algorithm](/asadpour-atsp-algorithm/) uses the same max entropy trees for the asymmetric problem and gets $O(\log n / \log\log n)$.
- **A better constant.** Later work improved the analysis of KKO and made $\varepsilon$ larger, but it is still extremely small; Gurvits, Klein and Leake reported about $10^{-34}$.
- **A limit of the method.** Jin, Klein and Williamson gave graphic instances on which the max entropy algorithm has an expected ratio of at least about 1.375. So the method alone cannot reach $4/3$.
- **Other trees.** Taking a uniform spanning tree of the support, or a minimum spanning tree, keeps line L5 and later lines but loses the link with the LP. The minimum spanning tree gives Christofides' algorithm.

## When to use it

Use this page to understand the best known ratio for metric TSP and the max entropy method of [randomized rounding](/randomized-rounding/) on spanning trees. Do not use it to get good tours in practice: [Christofides' algorithm](/christofides-algorithm/) gives almost the same guarantee at a much lower cost, and [Lin-Kernighan-Helsgaun](/lin-kernighan-helsgaun/) gives much better tours on most instances.

## Pitfalls

- **No scale factor in line L2.** The sum of the $x_e$ is $n$, but a spanning tree has $n - 1$ edges, so no distribution of trees has the marginals $x$. Without the factor $1 - 1/n$, or the vertex split of KKO, the fit of line L3 has no solution and Newton's method does not converge.
- **Uniform weights in line L3.** With $\lambda = 1$, the tree is uniform on the support, and its marginals are not $z$. In the example the edge $AE$ is then in $T$ with probability $3/5$, not $5/6$, and $\mathbb{E}[c(T)] = 28/3$, which is more than $(1 - 1/n)\,\text{LP}^* = 35/4$.
- **A single run in line L4.** The ratio is in expectation. A program that samples one tree and claims the bound for that tour is wrong; it must either repeat the run or report the bound as an expectation.
- **A simple graph in line L7.** If an edge of $J$ is also an edge of $T$, as $AE$ is in the example, the multigraph needs both copies. Otherwise two vertices have odd degree and the Euler circuit does not exist.
- **Costs that are not metric.** Step 2 of the proof and the shortcut of line L8 both need the triangle inequality. For a graph, use the shortest path costs.

## Implementations

## History

Max entropy distributions of spanning trees came to TSP through the ATSP algorithm of Asadpour, Goemans, Mądry, Oveis Gharan and Saberi (SODA 2010). Oveis Gharan, Saberi and Singh (FOCS 2011) used them for graphic TSP and beat 3/2 there by a small constant. Anna Karlin, Nathan Klein and Shayan Oveis Gharan posted the first improvement on 3/2 for general metric TSP in 2020; the paper won the best paper award at STOC 2021. Their FOCS 2022 paper moved the comparison from OPT to the subtour LP, and their IPCO 2023 paper gave a deterministic version. The bound 3/2 of Christofides (1976) and Serdyukov (1978) had stood for more than 40 years.

## References
