---
tag: GRPMAV
kind: theorem
slug: k-means-np-hardness
name: NP-hardness of k-means
aliases:
- k-means is NP-hard
- NP-hardness of minimum sum-of-squares clustering
area: machine-learning/clustering
level: advanced
summary: "Optimal k-means is NP-hard for k = 2 when d is part of the input, and in the plane when k is part of the input; it is also APX-hard in high dimension."
prereqs: [k-means-problem, np-hard]
see_also: [k-means-problem, k-means, k-means-plus-plus-guarantee, sparsest-cut-problem, polynomial-time-reduction, apx, ptas, k-center-hardness]
sources:
  - paper: doi:10.1007/s10994-009-5103-0
    title: Daniel Aloise, Amit Deshpande, Pierre Hansen and Preyas Popat, NP-hardness of Euclidean sum-of-squares clustering, Machine Learning 75(2), 2009, pages 245 to 248
    locator: the reduction from densest cut for k = 2, and the remark that the earlier proof of Drineas and others is not valid
  - paper: "Sanjoy Dasgupta, The hardness of k-means clustering, Technical Report CS2008-0916, University of California, San Diego, 2008"
    locator: NP-hardness for k = 2 in general dimension
  - paper: doi:10.1016/j.tcs.2010.05.034
    title: Meena Mahajan, Prajakta Nimbhorkar and Kasturi Varadarajan, The planar k-means problem is NP-hard, Theoretical Computer Science 442, 2012, pages 13 to 21
    locator: the reduction from planar 3-SAT for points in the plane with k part of the input
  - paper: doi:10.4230/LIPIcs.SOCG.2015.754
    title: Pranjal Awasthi, Moses Charikar, Ravishankar Krishnaswamy and Ali Kemal Sinop, The hardness of approximation of Euclidean k-means, 31st International Symposium on Computational Geometry (SoCG), LIPIcs 34, 2015, pages 754 to 767
    locator: the APX-hardness by a reduction from vertex cover on triangle-free graphs, with d = Omega(log n)
  - paper: "Mary Inaba, Naoki Katoh and Hiroshi Imai, Applications of weighted Voronoi diagrams and randomization to variance-based k-clustering, Proceedings of the 10th ACM Symposium on Computational Geometry, 1994, pages 332 to 339"
    locator: the exact algorithm in time n^O(kd) for fixed k and d
  - paper: "Bodo Manthey and Heiko Röglin, Smoothed analysis of the k-means method and related problems, survey, arXiv:1602.08254"
    locator: the overview of the complexity results for k-means
---

The NP-hardness of k-means is a family of results: finding the optimal solution of the [k-means problem](/k-means-problem/) is [NP-hard](/np-hard/) when the number of clusters is $k = 2$ but the dimension $d$ is part of the input, and also when the points lie in the plane but $k$ is part of the input. Dasgupta (2008) and Aloise, Deshpande, Hansen and Popat (2009) proved the first case, and Mahajan, Nimbhorkar and Varadarajan (2012) the second. When both $k$ and $d$ are fixed, or when $d = 1$, the problem is polynomial. In high dimension even a $(1 + \varepsilon)$ approximation is NP-hard for some constant $\varepsilon > 0$ (Awasthi, Charikar, Krishnaswamy and Sinop, 2015).

## Statement

The decision version of k-means asks: given points $x_1, \ldots, x_n \in \mathbb{Q}^d$, an integer $k$ and a number $M$, is there a partition of the points into $k$ clusters with $\sum_j \sum_{x \in P_j} \|x - \mu(P_j)\|^2 \le M$, where $\mu(P)$ is the mean of $P$? The input size counts all $n d$ coordinates.

| case | complexity | source |
|---|---|---|
| $d = 1$, any $k$ | polynomial, $O(k n^2)$ or better | dynamic program (Wang and Song, 2011) |
| $k$ and $d$ fixed | polynomial, $n^{O(kd)}$ | Inaba, Katoh and Imai (1994) |
| $k = 2$, $d$ part of the input | NP-complete | Dasgupta (2008); Aloise, Deshpande, Hansen and Popat (2009) |
| $d = 2$, $k$ part of the input | NP-complete | Mahajan, Nimbhorkar and Varadarajan (2012) |
| $k$ and $d$ part of the input | APX-hard: no $(1+\varepsilon)$ approximation for some $\varepsilon > 0$ unless P = NP | Awasthi, Charikar, Krishnaswamy and Sinop (2015) |

**Theorem A ($k = 2$).** The decision version of k-means with $k = 2$ is NP-complete when $d$ is part of the input. This holds even for points with coordinates in $\{-1, 0, 1\}$.

**Theorem B (the plane).** The decision version of k-means for points in $\mathbb{R}^2$ is NP-complete when $k$ is part of the input.

**Theorem C (approximation).** There is a constant $\varepsilon > 0$ such that it is NP-hard to approximate the k-means cost within a factor $1 + \varepsilon$, when $k$ and $d = \Omega(\log n)$ are part of the input.

The problem is in NP in all cases: a partition is a certificate, and its cost is a rational number that is computed exactly in polynomial time.

## In plain words

The k-means problem asks for the best way to split points into a given number of groups, with the least total squared distance to the group averages. The theorem says that there is no fast exact method for it in general, unless a large class of hard problems is also easy. This is already true when you only want two groups but the points have many features. It is also true when the points lie on a flat sheet but you want many groups. Only when both the number of groups and the number of features stay small is there a method that is fast in theory, and even that one is too slow for real use. So practical methods, such as Lloyd's algorithm, do not promise the best answer.

## Proof

**Proof of Theorem A (Aloise, Deshpande, Hansen and Popat).** The reduction is from the densest cut problem: given a graph $G = (V, E)$ and a number $M$, is there a cut $(S, T)$ of $V$ into two non-empty parts with $\frac{|E(S, T)|}{|S| \, |T|} \ge M$? Here $E(S, T)$ is the set of edges with one end in $S$ and one in $T$.

*Densest cut is NP-hard.* Let $\bar G$ be the complement of $G$. For each cut, $|E_{\bar G}(S, T)| = |S||T| - |E_G(S, T)|$, so the density of a cut in $\bar G$ is 1 minus its density in $G$. So a densest cut of $G$ is a sparsest cut of $\bar G$ with the ratio $|E(S,T)| / (|S||T|)$, and the uniform [sparsest cut problem](/sparsest-cut-problem/) is NP-hard (Matula and Shahrokhi, 1990).

*The points.* Let $n = |V|$ and $m = |E|$. Fix an orientation of each edge. For each vertex $v$ make a point $x_v \in \mathbb{R}^m$: its coordinate for the edge $e$ is $+1$ if $v$ is the tail of $e$, $-1$ if $v$ is the head of $e$, and 0 otherwise. Then $\|x_v\|^2 = \deg(v)$.

*The cost of one cluster.* For a set $S$ of vertices, the cost of $S$ is
$$\sum_{v \in S} \|x_v - \mu(S)\|^2 = \sum_{v \in S} \|x_v\|^2 - \frac{1}{|S|} \Big\| \sum_{v \in S} x_v \Big\|^2 .$$
In the sum $\sum_{v \in S} x_v$, an edge with both ends in $S$ gives $+1 - 1 = 0$, an edge with one end in $S$ gives $\pm 1$, and an edge with no end in $S$ gives 0. So $\|\sum_{v \in S} x_v\|^2 = |E(S, T)|$, where $T = V \setminus S$. The cost of $S$ is $\deg(S) - |E(S, T)| / |S|$, with $\deg(S) = \sum_{v \in S} \deg(v)$.

*The cost of a 2-clustering.* Add the costs of $S$ and $T$, and use $\deg(S) + \deg(T) = 2m$:
$$\phi(S, T) = 2m - |E(S, T)| \Big( \frac{1}{|S|} + \frac{1}{|T|} \Big) = 2m - n \cdot \frac{|E(S, T)|}{|S| \, |T|} .$$
So $G$ has a cut of density at least $M$ exactly when the points have a 2-clustering of cost at most $2m - nM$. The points have $n$ rows of $m$ coordinates in $\{-1, 0, 1\}$, so the reduction runs in polynomial time. We may assume $M > 0$, because for $M \le 0$ the answer is yes for each graph with at least two vertices. A clustering with one empty part has cost $2m > 2m - nM$, so each clustering of cost at most $2m - nM$ has two non-empty parts and is a cut. $\square$

The dimension of the points is $m$, the number of edges, so the proof needs $d$ to grow with the input. This is the reason why Theorem A says nothing about fixed $d$.

**Proof idea of Theorem B (Mahajan, Nimbhorkar and Varadarajan).** The reduction is from planar 3-SAT, the case of [3-SAT](/3-sat/) in which the graph of variables and clauses is a [planar graph](/planar-graph/). Each variable becomes a cycle of points in the plane, drawn along the planar embedding. A cycle of $2r$ points has exactly two optimal ways to be covered by $r$ clusters of two consecutive points, and these two ways encode true and false. Each clause becomes a point placed near the three cycles of its variables, at a place where it can join a pair of the cycle at low extra cost only if the pair is in the state that satisfies the literal. The number of clusters $k$ is the total number of pairs. The formula is satisfiable exactly when the cost can reach a threshold $M$. The paper fixes the distances so that all coordinates are rational with polynomial size, and shows that no other kind of clustering reaches $M$. $\square$

**Proof idea of Theorem C (Awasthi, Charikar, Krishnaswamy and Sinop).** The reduction is from [vertex cover](/vertex-cover/) on triangle-free graphs, which is hard to approximate within some constant. Each edge of the graph becomes a point, the sum of the two unit vectors of its end vertices. A cluster of edges that share a vertex (a star) is cheap, and a cluster that contains edges with no common vertex is expensive; in a triangle-free graph the cheap clusters are exactly the stars. So a clustering into $k$ cheap clusters is a vertex cover of size $k$, and a gap in the size of the vertex cover becomes a constant factor gap in the k-means cost. The points live in a space whose dimension is the number of vertices, so $d$ grows with the input; the paper states the result for $d = \Omega(\log n)$. $\square$

## Consequences

- **No exact polynomial algorithm.** Unless P = NP, no algorithm solves k-means exactly in time polynomial in $n$, $d$ and $k$. This is why the [k-means algorithm](/k-means/) and its variants are heuristics.
- **No PTAS in high dimension.** By Theorem C, unless P = NP there is no [PTAS](/ptas/) when $k$ and $d$ are both part of the input. Constant factor algorithms exist, for example local search with $9 + \varepsilon$ (Kanungo and others, 2004).
- **Approximation schemes for fixed parameters.** For fixed $k$ there are $(1+\varepsilon)$ approximations in time linear in $n d$ for fixed $\varepsilon$ (Kumar, Sabharwal and Sen, 2010). For fixed $d$ local search gives a PTAS (Friggstad, Rezapour and Salavatipour, and Cohen-Addad, Klein and Mathieu, both 2016). So Theorems A and B are about exact solutions; they do not forbid good approximations in these cases.
- **Seeding with a guarantee.** The [k-means++ guarantee](/k-means-plus-plus-guarantee/) gives an expected $O(\log k)$ factor in time $O(nkd)$.
- **Related problems.** The [k-median problem](/k-median-problem/) and the [k-center problem](/k-center-problem/) are NP-hard too, by other reductions; see [k-center hardness](/k-center-hardness/).

## Tightness

- **Theorem A needs high dimension.** For fixed $d$ and fixed $k$ the problem is polynomial (time $n^{O(kd)}$). So the dimension must grow with the input in any proof for $k = 2$.
- **Theorem B needs many clusters.** For $d = 2$ and fixed $k$ the problem is again polynomial, so $k$ must grow.
- **One dimension is easy.** For $d = 1$ the optimal clusters are intervals of the sorted points, and a dynamic program solves the problem for every $k$; see the [k-means problem](/k-means-problem/).
- **The constant in Theorem C is small.** The proof gives a tiny $\varepsilon$; Lee, Schmidt and Wright (2017) obtained a factor about $1.0013$. The best known polynomial time approximation factors are larger than 5, so the gap is wide.

## History

Drineas, Frieze, Kannan, Vempala and Vinay stated the NP-hardness for $k = 2$ in 2004, but Aloise, Deshpande, Hansen and Popat showed that their proof was not valid. Dasgupta gave a proof for $k = 2$ in a 2008 technical report, and Aloise, Deshpande, Hansen and Popat gave the short proof by densest cut in 2009. Mahajan, Nimbhorkar and Varadarajan proved the planar case at WALCOM 2009, with the journal version in 2012. Awasthi, Charikar, Krishnaswamy and Sinop proved the APX-hardness in 2015. The polynomial algorithm for fixed $k$ and $d$ is due to Inaba, Katoh and Imai (1994).

## References
