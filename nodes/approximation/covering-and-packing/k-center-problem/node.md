---
tag: R4VG79
kind: problem
slug: k-center-problem
name: k-center problem
aliases:
- metric k-center
- minimax clustering
- minimax facility location
- p-center problem
area: approximation/covering-and-packing
level: advanced
summary: Choose k centers minimizing the maximum distance from any point to its nearest center.
prereqs: [metric-space, triangle-inequality, approximation-ratio, dominating-set]
see_also: [gonzalez-k-center, k-center-inapproximability, k-center-hardness, dominating-set, k-median-problem, facility-location-problem, clustering-problem, minimum-enclosing-ball]
sources:
  - paper: "W.-L. Hsu and G. L. Nemhauser, Easy and hard bottleneck location problems, Discrete Applied Mathematics 1(3), 1979, pp. 209-215"
    title: Hsu and Nemhauser 1979
    locator: the theorem that metric k-center has no ratio 2 - epsilon unless P = NP, by a reduction from dominating set
  - paper: "T. F. Gonzalez, Clustering to minimize the maximum intercluster distance, Theoretical Computer Science 38, 1985, pp. 293-306"
    title: Gonzalez 1985
    locator: the farthest-first algorithm and its ratio 2
  - paper: "D. S. Hochbaum and D. B. Shmoys, A best possible heuristic for the k-center problem, Mathematics of Operations Research 10(2), 1985, pp. 180-184"
    title: Hochbaum and Shmoys 1985
    locator: the threshold algorithm with ratio 2
  - paper: "D. S. Hochbaum and D. B. Shmoys, A unified approach to approximation algorithms for bottleneck problems, Journal of the ACM 33(3), 1986, pp. 533-550"
    title: Hochbaum and Shmoys 1986
    locator: the bottleneck method, the square of a threshold graph, and the ratio 3 for k-supplier
  - paper: "O. Kariv and S. L. Hakimi, An algorithmic approach to network location problems. I: The p-centers, SIAM Journal on Applied Mathematics 37(3), 1979, pp. 513-538"
    title: Kariv and Hakimi 1979
    locator: the NP-hardness of the p-center problem and the polynomial algorithms on trees
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 2.2 (the k-center problem)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 5 (k-center)
---

The $k$-center problem gives $n$ points in a metric space and an integer $k$, and asks for $k$ of the points as centers so that the largest distance from a point to its nearest center is as small as possible. It is NP-hard, and two simple algorithms give ratio 2: the farthest-first traversal of [Gonzalez](/gonzalez-k-center/) (1985) and the threshold method of Hochbaum and Shmoys (1985). This is best possible: no polynomial-time algorithm has ratio $2 - \varepsilon$ unless P = NP (Hsu and Nemhauser 1979). Without the triangle inequality no ratio at all is possible.

## In plain words

A city wants to build $k$ fire stations at some of its sites. Each site is served by the station closest to it. The city wants the worst case to be good: the longest trip from any site to its station should be as short as possible.

A simple rule picks any site first. Then it picks again and again the site that is farthest from all stations so far, until there are $k$ stations. The longest trip is then at most twice the best possible. The reason is that if the rule must stop with a long trip left, it has found many sites that are all far from each other, and no plan with $k$ stations can serve all of them well.

## Definition

The input is a finite set $V$ of $n$ points with a distance $d : V \times V \to \mathbb{R}_{\ge 0}$ that is a [metric](/metric-space/): $d(u, u) = 0$, $d(u, v) = d(v, u)$, and the [triangle inequality](/triangle-inequality/) $d(u, w) \le d(u, v) + d(v, w)$ holds. Also given is an integer $k$ with $1 \le k \le n$. For a set $C \subseteq V$ of centers, the *radius* is

$$r(C) = \max_{v \in V}\ \min_{c \in C} d(v, c).$$

The goal is a set $C$ with $|C| \le k$ and $r(C)$ as small as possible; $\mathrm{OPT}$ is the least radius. Each point goes to its nearest center, so a choice of centers fixes $k$ clusters. $\mathrm{OPT}$ is one of the $\binom{n}{2}$ distances $d(u, v)$, so there are only $O(n^2)$ candidate values.

*Ratio convention.* This is a minimization problem. An algorithm has ratio $\rho \ge 1$ if $r(C) \le \rho\,\mathrm{OPT}$ on every input. The algorithms below use the following lower bound on $\mathrm{OPT}$.

*Lemma (packing bound).* If there are $k + 1$ points in $V$ with pairwise distances more than $2r$, then $\mathrm{OPT} > r$. *Proof.* Take any $C$ with $|C| \le k$. By the pigeonhole principle, two of the $k + 1$ points, $u$ and $v$, have the same nearest center $c$. Then $2r < d(u, v) \le d(u, c) + d(c, v) \le 2\,r(C)$, so $r(C) > r$. $\square$

## Variants

- **k-supplier.** The centers must come from a set $F$ of suppliers, and only the points of another set $U$ must be served. Ratio 3 is possible (Hochbaum and Shmoys 1986), and $3 - \varepsilon$ is NP-hard.
- **Weighted k-center.** Centers have costs, and the total cost is bounded; ratio 3 is possible (Hochbaum and Shmoys 1986).
- **Centers anywhere.** In a Euclidean space the centers may be any points of the space. For $k = 1$ this is the [minimum enclosing ball](/minimum-enclosing-ball/), and in the plane the [minimum enclosing circle](/minimum-enclosing-circle/).
- **Euclidean k-center.** Points in the plane with the Euclidean distance. The problem stays NP-hard, and ratio below about 1.822 is NP-hard (Feder and Greene 1988).
- **Asymmetric k-center.** The distance need not be symmetric. The best ratio is $O(\log^* n)$ (Panigrahy and Vishwanathan 1998), and this is best possible up to a constant factor (Chuzhoy, Guha, Halperin, Khanna, Kortsarz, Krauthgamer and Naor 2005).
- **Capacitated k-center.** Each center may serve at most $L$ points; constant ratios are known.
- **k-center with outliers.** Up to $z$ points may stay unserved; ratio 3 by Charikar, Khuller, Mount and Narasimhan (2001).
- **Graphs and trees.** The points are the vertices of a graph with shortest-path distances. On trees the problem is solvable in polynomial time (Kariv and Hakimi 1979); for $k = 1$ see the [tree center](/tree-center/).
- **Other objectives.** Minimizing the sum of distances is the [k-median problem](/k-median-problem/), and the sum of squared distances is the [k-means problem](/k-means-problem/).

## Examples

Take the six points $0, 1, 2, 10, 11, 12$ on a line with $d(u, v) = |u - v|$, and $k = 2$. The centers $\{1, 11\}$ have radius 1, and radius 0 would need six centers, so $\mathrm{OPT} = 1$.

*Farthest-first.* Start with the point 0. The farthest point is 12. Now each point has distance at most 2 to $\{0, 12\}$, and the points 2 and 10 have distance exactly 2. So the algorithm returns radius $2 = 2\,\mathrm{OPT}$.

*Threshold.* Try $r = 1$, the smallest positive distance. Pick the point 0 and drop all points within $2r = 2$ of it: 1 and 2. Pick 10 and drop 11 and 12. The picks $\{0, 10\}$ are at most $k$, so the method stops with radius at most $2r = 2$.

## Known algorithms

- **Farthest-first traversal (Gonzalez 1985).** Pick any first center; then $k - 1$ times add the point farthest from the current centers. Ratio 2 in $O(nk)$ time. See [Gonzalez's algorithm](/gonzalez-k-center/) for the proof and the tight example.
- **Threshold method (Hochbaum and Shmoys 1985).** Sort the distinct distances $r_1 < r_2 < \cdots$. For a guess $r$, let $G_r$ be the graph on $V$ with an edge $uv$ when $d(u, v) \le r$. Take a maximal independent set $I$ of the square $G_r^2$, where $u$ and $v$ are adjacent when $d(u, v) \le 2r$ through at most two edges; greedily, pick an unmarked point, put it in $I$ and mark all points within distance $2r$. If $|I| \le k$, return $I$; otherwise try a larger $r$.
  *Theorem.* The method returns centers of radius at most $2\,\mathrm{OPT}$. *Proof.* The points of $I$ have pairwise distances more than $2r$, so if $r \ge \mathrm{OPT}$, the packing bound gives $|I| \le k$, and the guess succeeds. A guess that succeeds gives radius at most $2r$, because every point was marked by a pick within distance $2r$. So the first guess in increasing order that succeeds is at most $\mathrm{OPT}$, which is itself a candidate. $\square$ A binary search over the sorted distances also works with the invariant "the lower end fails and the upper end succeeds": a failed guess is less than $\mathrm{OPT}$, so the final upper end is at most $\mathrm{OPT}$. The time is $O(n^2 \log n)$.
- **Dominating set view.** $\mathrm{OPT} \le r$ exactly when $G_r$ has a [dominating set](/dominating-set/) of size at most $k$. The threshold method replaces this NP-hard test by the easy test on $G_r^2$, at the cost of the factor 2.
- **Exact methods.** Try all $\binom nk$ center sets in $O(n^{k+1} k)$ time, or solve a set cover integer program for each candidate radius. For fixed $k$ in a Euclidean space of fixed dimension, there are faster exact and $(1 + \varepsilon)$ methods.

## Bounds

| claim | statement | source |
|---|---|---|
| lower bound used | $k + 1$ points pairwise more than $2r$ apart force $\mathrm{OPT} > r$ | proved above |
| farthest-first | ratio 2, $O(nk)$ time | Gonzalez 1985 |
| threshold method | ratio 2 | Hochbaum and Shmoys 1985 |
| hardness | no ratio $2 - \varepsilon$ unless P = NP | Hsu and Nemhauser 1979; see [k-center inapproximability](/k-center-inapproximability/) |
| no triangle inequality | no ratio $\alpha(n)$ for any $\alpha$ computable in polynomial time, unless P = NP | same reduction |
| k-supplier | ratio 3, and $3 - \varepsilon$ is NP-hard | Hochbaum and Shmoys 1986 |
| asymmetric | $\Theta(\log^* n)$ | Panigrahy and Vishwanathan 1998; Chuzhoy et al. 2005 |

## Reductions

- **From dominating set (Hsu and Nemhauser 1979).** Given a graph $H = (V, E)$ and $k$, set $d(u, v) = 1$ for $uv \in E$ and $d(u, v) = 2$ for other pairs $u \ne v$. Any distance with values in $\{1, 2\}$ off the diagonal satisfies the triangle inequality, because $d(u, w) \le 2 \le d(u, v) + d(v, w)$. A set $C$ of $k$ centers has radius 1 exactly when each vertex outside $C$ has a neighbor in $C$, that is, when $C$ is a dominating set; otherwise its radius is 2. So $\mathrm{OPT} = 1$ if $H$ has a dominating set of size $k$, and $\mathrm{OPT} = 2$ if not. An algorithm with ratio $2 - \varepsilon$ returns radius below 2, hence radius 1, exactly on the yes-instances, so it decides [dominating set](/dominating-set/), which is NP-complete. See [k-center hardness](/k-center-hardness/).
- **Without the triangle inequality.** Use the distance $\alpha(n) + 1$ in place of 2 for non-edges. The gap is then $\alpha(n) + 1$, so no ratio $\alpha(n)$ is possible unless P = NP.
- **To set cover.** For a guess $r$, the balls $\{ v : d(v, c) \le r \}$ for $c \in V$ form a [set cover](/set-cover/) instance, and $\mathrm{OPT} \le r$ exactly when $k$ balls cover $V$.
- **Bottleneck problems.** $k$-center is a bottleneck problem: the objective is a largest distance, so the answer is one of the input distances, and the threshold graphs $G_r$ turn it into a sequence of graph questions. The same method treats [bottleneck TSP](/bottleneck-tsp/) and other bottleneck problems.

## Applications

- **Facility location with a worst-case goal.** Placing fire stations, hospitals, warehouses or servers so that the longest response time is small.
- **Clustering.** Splitting data into $k$ groups of small diameter; farthest-first traversal is also a common way to choose diverse seeds for [k-means](/k-means-problem/) and to build hierarchical clusterings.
- **Summaries and coresets.** Choosing $k$ representatives so that every item is close to one of them, for example in image collections or in streaming data.
- **Network design.** Choosing $k$ hubs in a network to minimize the largest distance to a hub.

## References
