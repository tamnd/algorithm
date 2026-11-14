---
tag: VACAVK
kind: algorithm
slug: spectral-partitioning
name: Spectral partitioning
aliases:
- spectral bisection
- Fiedler vector partitioning
area: cad/partitioning-floorplanning-and-placement
level: core
summary: Splits a graph by the signs or the median of the eigenvector of the second smallest Laplacian eigenvalue, the Fiedler vector, as in Hall and in Pothen and coauthors.
solves: [graph-partitioning-problem]
model: real-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, t: the number of power iteration steps}
  time: {worst: Θ(t (n + m) + n log n), average: Θ(t (n + m) + n log n), best: Θ(n + m + n log n)}
  space: {extra: Θ(n + m)}
properties: {deterministic: false, recursive: false, exact: false}
history:
  year: 1970
  people: [Kenneth M. Hall, Miroslav Fiedler, Alex Pothen, Horst D. Simon, Kang-Pu Liou, Lars Hagen, Andrew B. Kahng]
  note: Hall placed the vertices of a graph by Laplacian eigenvectors in 1970, Fiedler studied the second eigenvector in 1973 and 1975, and Pothen, Simon and Liou made the median split a standard bisection method in 1990.
prereqs: [laplacian-matrix, graph-partitioning-problem, power-iteration, rayleigh-quotient]
see_also: [ratio-cut, laplacian-matrix, spectral-clustering, kernighan-lin, fiduccia-mattheyses, multilevel-graph-partitioning, lanczos-algorithm, clique-net-model]
sources:
  - paper: doi:10.1287/mnsc.17.3.219
    title: Kenneth M. Hall, An r-dimensional quadratic placement algorithm, Management Science 17(3), 219 to 229, 1970
    locator: the placement of the vertices by the eigenvectors of the smallest nonzero eigenvalues of the Laplacian, under a norm constraint
  - paper: "Miroslav Fiedler, Algebraic connectivity of graphs, Czechoslovak Mathematical Journal 23(98), 298 to 305, 1973"
    locator: the second smallest Laplacian eigenvalue as the algebraic connectivity, positive exactly for connected graphs
  - paper: "Miroslav Fiedler, A property of eigenvectors of nonnegative symmetric matrices and its application to graph theory, Czechoslovak Mathematical Journal 25(100), 619 to 633, 1975"
    locator: the theorem that the vertices with entries of the Fiedler vector at least (or at most) a threshold on the right side of zero induce a connected subgraph
  - paper: doi:10.1137/0611030
    title: Alex Pothen, Horst D. Simon and Kang-Pu Liou, Partitioning sparse matrices with eigenvectors of graphs, SIAM Journal on Matrix Analysis and Applications 11(3), 430 to 452, 1990
    locator: spectral bisection by the median of the Fiedler vector, computed by the Lanczos method, and the vertex separators found from it
  - paper: doi:10.1109/43.159993
    title: Lars Hagen and Andrew B. Kahng, New spectral methods for ratio cut partitioning and clustering, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 11(9), 1074 to 1085, 1992
    locator: the bound of the minimum ratio cut by the second eigenvalue over n, and the EIG1 sweep over the sorted eigenvector
  - paper: doi:10.1137/S0895479896312262
    title: Stephen Guattery and Gary L. Miller, On the quality of spectral separators, SIAM Journal on Matrix Analysis and Applications 19(3), 701 to 719, 1998
    locator: the roach graph, a family with bisections of constant width on which the median split of the Fiedler vector cuts a linear number of edges
  - paper: doi:10.1016/j.laa.2006.07.020
    title: Daniel A. Spielman and Shang-Hua Teng, Spectral partitioning works, planar graphs and finite element meshes, Linear Algebra and its Applications 421(2 to 3), 284 to 305, 2007
    locator: the bound on the Fiedler value of bounded degree planar graphs and well-shaped meshes, and the cut ratio of the sweep that follows from it
  - book: isbn:9783030964146
    title: Andrew B. Kahng, Jens Lienig, Igor L. Markov and Jin Hu, VLSI Physical Design, From Graph Partitioning to Timing Closure, second edition, Springer, 2022
    locator: Chapter 2, Netlist and System Partitioning (general locator)
---

Spectral partitioning splits a graph into two parts by one eigenvector of its [Laplacian](/laplacian-matrix/): the eigenvector of the second smallest eigenvalue $\lambda_2$, called the Fiedler vector. Sort the vertices by their entries in this vector, then cut the sorted list at the median for a bisection, or at the best prefix for a [ratio cut](/ratio-cut/). The method is a relaxation of [graph bisection](/graph-partitioning-problem/): it solves the problem exactly when the entries may be any real numbers, and then rounds. It is a heuristic with no constant-factor guarantee, but $\lambda_2$ gives a lower bound that sometimes proves the result optimal.

## In plain words

Think of the vertices as beads and the edges as springs. Pull the beads apart along a line, but keep their center fixed and their total spread fixed. The springs pull linked beads together. In the position with the least spring energy, groups of beads with many springs between them stay close together, and groups with few springs between them drift apart.

That position is the Fiedler vector. So you sort the beads by their place on the line and cut the line in the middle. Beads on the same side are mostly linked to each other. The cut is often good, but it is not always the best, and on some graphs it is far from the best.

## The problem

The input is an undirected graph $G = (V, E)$ with $n \ge 2$ vertices $0, \ldots, n - 1$, $m$ edges and weights $w(u, v) > 0$. In *bisection mode* the output is a split $(A, B)$ with $|A| = \lfloor n/2 \rfloor$, and the goal, which the method does not always reach, is a small cut weight $\mathrm{cut}(A, B)$. This is the bisection case of the [graph partitioning problem](/graph-partitioning-problem/), which is NP-hard. In *ratio mode* the output is any split with both parts nonempty, and the goal is a small [ratio cut](/ratio-cut/) $\mathrm{cut}(A, B) / (|A| \, |B|)$.

For a netlist, a [hypergraph](/hypergraph/) with $n$ cells, $m$ nets and $P$ pins, first replace each net by a graph with the [clique net model](/clique-net-model/). A net of $p$ pins gives $\binom{p}{2}$ edges, so large nets make the graph dense. The cut of the graph then only approximates the number of cut nets, which is the true cost in [hypergraph partitioning](/hypergraph-partitioning/).

## The algorithm

Let $d(v)$ be the weighted degree of $v$ and $L = D - A$ the Laplacian, with eigenvalues $0 = \lambda_1 \le \lambda_2 \le \cdots \le \lambda_n$. The all-ones vector $\mathbf 1$ is an eigenvector of $\lambda_1$. The implementation finds the Fiedler vector by [power iteration](/power-iteration/) on $M = cI - L$ with $c = 2 \max_v d(v)$. The eigenvalues of $M$ are $c - \lambda_i \ge 0$, so after the component along $\mathbf 1$ is removed, the largest one is $c - \lambda_2$, and power iteration finds its eigenvector. The tolerance $\tau$ bounds the residual of the unit vector $x$.

```pseudo id=main
SPECTRAL-PARTITION(G, mode, τ)
L1  build L = D − A and set c ← 2 · max_v d(v)
L2  x ← a random vector; x ← x − mean(x) · 1; x ← x / ‖x‖
L3  loop
L4      ρ ← xᵀ L x                                  ▷ the Rayleigh quotient
L5      if ‖L x − ρ x‖ ≤ τ then leave the loop
L6      x ← (c I − L) x; x ← x − mean(x) · 1; x ← x / ‖x‖
L7  sort the vertices by x_v, ties by the vertex number
L8  if mode = bisection then return (the first ⌊n/2⌋ vertices, the rest)
L9  for k ← 1 to n − 1: R_k ← cut(first k, rest) / (k (n − k))
L10 return the split at the k with the least R_k
```

Line L6 uses one product with $L$, which costs $O(n + m)$ with adjacency lists. Removing the mean in lines L2 and L6 keeps $x$ orthogonal to $\mathbf 1$, both in exact arithmetic and against the drift of rounding errors. Line L9 moves the vertices to the first part one at a time and updates the cut from the edges of the moved vertex, so the whole sweep costs $O(n + m)$.

The *sign split* is the other common rounding: put the vertices with $x_v < 0$ on one side. It does not control the sizes of the parts. In practice the eigenvector is computed by the [Lanczos method](/lanczos-algorithm/), which needs far fewer products than power iteration when $\lambda_2$ and $\lambda_3$ are close. Power iteration is used here because it is short and its stopping rule is easy to check.

## Example

Take the graph of the [graph partitioning](/graph-partitioning-problem/) page: two triangles $a, b, c$ and $d, e, f$, joined by the edges $cd$ and $be$, all of weight 1. The Laplacian has eigenvalues $0, 1, 3, 3, 4, 5$, and the Fiedler vector for $\lambda_2 = 1$ is

$$ x = \tfrac{1}{\sqrt{12}} (2, 1, 1, -1, -1, -2) \approx (0.577, 0.289, 0.289, -0.289, -0.289, -0.577) $$

in the order $a, \ldots, f$. Check at $a$ with the unscaled vector $(2, 1, 1, -1, -1, -2)$: $a$ has degree 2 and the neighbors $b, c$, so $(Lx)_a = 2 \cdot 2 - 1 - 1 = 2 = \lambda_2 \cdot 2$.

The largest degree is 3, so $c = 6$. Start from $e_a$, the unit vector at $a$, after line L2 removes its mean.

| step | $x$ (rounded) | $\rho$ | residual |
| --- | --- | --- | --- |
| 0 | $(0.913, -0.183, -0.183, -0.183, -0.183, -0.183)$ | 2.4 | 1.20 |
| 1 | $(0.866, 0, 0, -0.289, -0.289, -0.289)$ | 1.6667 | 1.03 |
| 2 | $(0.778, 0.130, 0.130, -0.324, -0.324, -0.389)$ | 1.2605 | 0.698 |
| 3 | $(0.704, 0.203, 0.203, -0.325, -0.325, -0.460)$ | 1.0948 | 0.432 |
| 5 | $(0.623, 0.262, 0.262, -0.307, -0.307, -0.534)$ | 1.0122 | 0.156 |
| 10 | | 1.0001 | $1.21 \cdot 10^{-2}$ |
| 20 | | 1.0000 | $7.31 \cdot 10^{-5}$ |
| 30 | | 1.0000 | $4.42 \cdot 10^{-7}$ |

The residual falls by a factor of about $3/5$ per step, which is $(c - \lambda_3)/(c - \lambda_2) = 3/5$. The sorted order $a, b, c, d, e, f$ is already right at step 2, long before the residual is small. Line L8 returns $\{a, b, c\} \mid \{d, e, f\}$ with cut 2. Every bisection has cut at least $n \lambda_2 / 4 = 1.5$, so at least 2, and this split is optimal. In ratio mode, line L9 finds $R_3 = 2/9$ as the least value, which is the minimum ratio cut; the bound of Hagen and Kahng gives only $\lambda_2 / n = 1/6$.

**A graph where the median fails.** The roach graph of Guattery and Miller has two paths of $2k$ vertices each, the upper and the lower path, with a rung between the $i$-th vertices of the two paths for $i = 1, \ldots, k$. The other $k$ vertices of each path form an "antenna". Guattery and Miller show that the Fiedler vector is odd under the swap of the two paths, so the median split puts the upper path on one side and the lower path on the other and cuts all $k$ rungs. The minimum bisection cuts each path in its middle, 2 edges. With the implementation (seed 1), $k = 3$ and $k = 4$ give cuts 3 and 4 against the optimum 2, checked by brute force, and $k = 8$ and $k = 12$ give cuts 8 and 12. The ratio sweep does better here: it cuts off one antenna with a single edge.

## Correctness

The [proof](proofs/correctness.md) shows the following. The first three items hold for every input; the last says how good the result is, and it is only a bound.

- **Valid output.** Line L8 returns parts of sizes $\lfloor n/2 \rfloor$ and $\lceil n/2 \rceil$, and line L10 returns two nonempty parts. The incremental cut of line L9 equals the cut of each prefix.
- **The relaxation.** Over real vectors $x \perp \mathbf 1$ with $x \ne 0$, the Rayleigh quotient $x^{\top} L x / x^{\top} x$ is least, with value $\lambda_2$, exactly at the eigenvectors of $\lambda_2$. For a bisection with $x_v = \pm 1$, $x^{\top} L x = 4 \, \mathrm{cut}$, so the method minimizes the relaxed cut and rounds.
- **Convergence.** With $c = 2 \max_v d(v)$, every eigenvalue of $cI - L$ is nonnegative. If the start has a nonzero component in the eigenspace of $\lambda_2$, which happens with probability 1 for a continuous random start, the residual after $k$ steps is at most $C \, q^k$ with $q = (c - \lambda')/(c - \lambda_2) < 1$, where $\lambda'$ is the least eigenvalue above $\lambda_2$ ($q = 0$ if there is none). So the loop of line L3 stops.
- **Lower bounds.** Every bisection has cut at least $n \lambda_2 / 4$, and every split has ratio cut at least $\lambda_2 / n$. If the returned cut meets the bound after rounding up, it is optimal. These bounds are for the unnormalized Laplacian and for $R = \mathrm{cut}/(|A| |B|)$; other normalizations give other constants.

## Complexity

Let $t$ be the number of power steps.

- **Time.** Line L1 takes $O(n + m)$. Each step of lines L4 to L6 takes $O(n + m)$. Line L7 takes $O(n \log n)$, and lines L8 to L10 take $O(n + m)$. The total is $\Theta(t (n + m) + n \log n)$.
- **Steps.** By the convergence bound, $t = O(\log(C/\tau) / \log(1/q))$. When the gap $\lambda' - \lambda_2$ is small compared with $c$, $q$ is close to 1 and $t$ is large. In the usual analysis, the number of Lanczos steps depends on the square root of the relative gap instead of the gap itself, so it needs far fewer products, which is why production codes use it.
- **Space.** The adjacency lists and a few vectors of length $n$ take $\Theta(n + m)$.
- **Netlists.** With the clique model, the graph of a netlist has up to $\sum_e \binom{|e|}{2}$ edges, which can be much more than $P$. A star model or a cap on net sizes keeps it at $O(P)$.

## Properties

Spectral partitioning is a heuristic for bisection and for the ratio cut. What is proved about it and what is only measured are kept apart below.

**What is proved.**

- The relaxation, the convergence of the power iteration and the two lower bounds above.
- Fiedler (1975): if $G$ is connected and $x$ is a Fiedler vector, then for every $r \ge 0$ the vertices with $x_v \ge -r$ induce a connected subgraph, and so do the vertices with $x_v \le r$. So both sides of the sign split with $x_v \ge 0$ and $x_v \le 0$ are connected. This page cites it and does not prove it.
- Spielman and Teng (2007): for planar graphs of bounded degree, $\lambda_2 = O(1/n)$, and a sweep of the Fiedler vector finds a split whose cut divided by the smaller part is $O(1/\sqrt n)$. Applied recursively, this gives balanced separators of size $O(\sqrt n)$, as the [planar separator theorem](/planar-separator-theorem/) does.
- No constant ratio: on the roach graphs of Guattery and Miller (1998), the median split cuts $\Theta(n)$ edges while the minimum bisection cuts 2. So spectral bisection has no constant approximation ratio.

**What is measured.** Pothen, Simon and Liou (1990) and Hagen and Kahng (1992) reported experiments on sparse matrices and on benchmark circuits, in their papers. The numbers below are from the implementation of this page, on small random graphs, and are not benchmark results. On 200 graphs $G(12, 0.3)$ with unit weights (generator `random.Random(2026)`, the solver of graph $t$ started from `random.Random(t)`), compared with brute force:

| method | optimal | mean of cut / optimum | worst |
| --- | --- | --- | --- |
| median split (bisection) | 107 of 200 | 1.151 | 2.333 |
| sweep (ratio cut) | 191 of 200 | 1.003 | 1.257 |

All runs converged to residual $10^{-10}$. The median split is often far from the best bisection on such small graphs, which is why it is followed by a [Kernighan-Lin](/kernighan-lin/) or [Fiduccia-Mattheyses](/fiduccia-mattheyses/) refinement in practice.

## Variants and improvements

- **EIG1 for ratio cut.** Hagen and Kahng's sweep, lines L9 and L10, picks the best of the $n - 1$ prefixes for the ratio cut instead of the median.
- **More eigenvectors.** Hall (1970) used the eigenvectors of $\lambda_2$ and $\lambda_3$ as $x$ and $y$ coordinates, a quadratic placement in the plane. Spectral $k$-way methods use $k$ eigenvectors, as in [spectral clustering](/spectral-clustering/) with $k$-means.
- **Normalized Laplacian.** Using $D^{-1/2} L D^{-1/2}$ relaxes the [normalized cut](/normalized-cut/) instead of the ratio cut.
- **Recursive bisection.** Bisect each part again to get $2^j$ parts. Each level needs a new eigenvector of the subgraph.
- **Refinement and multilevel use.** Refine the rounded split with local moves, or use a spectral split as the start at the coarsest level of a [multilevel partitioner](/multilevel-graph-partitioning/).

## When to use it

Use spectral partitioning when you need a global view of a graph that local moves do not have, for example as a starting split for refinement, or when a lower bound from $\lambda_2$ is useful. It works well on meshes and other graphs with geometric structure, as the result of Spielman and Teng explains. For large netlists, multilevel partitioners with FM refinement are faster and give smaller cuts, and they handle nets directly.

## Pitfalls

- **Forgetting to remove $\mathbf 1$.** Without the mean removal, power iteration on $cI - L$ converges to $\mathbf 1$, the eigenvector of $\lambda_1 = 0$, which carries no information.
- **A shift that is too small.** If $c < \lambda_n$, the eigenvalue $c - \lambda_n$ of $M$ is negative and can be larger in absolute value than $c - \lambda_2$. Then the iteration finds the wrong vector. $c = 2 \max_v d(v)$ is safe because $\lambda_n \le 2 \max_v d(v)$.
- **Stopping on $\rho$ alone.** $\rho$ converges about twice as fast as $x$, so $\rho$ can look exact while the order of the entries is still wrong. Stop on the residual.
- **A multiple $\lambda_2$.** If $\lambda_2 = \lambda_3$, any vector of the eigenspace is a Fiedler vector, and different starts give different splits.
- **Disconnected graphs.** Then $\lambda_2 = 0$, and the Fiedler vector can be any vector that is constant on each component, so a split with cut 0 exists, but the median split need not find it.
- **Wrong cost for netlists.** The cut of the clique graph is not the number of cut nets. Report the hypergraph cut of the final split, not the graph cut.

## Implementations

## History

Hall (1970) placed the vertices of a graph in $r$ dimensions by minimizing a quadratic sum of squared edge lengths, and found that the optimum is given by eigenvectors of the Laplacian. Donath and Hoffman (1973) used eigenvectors of graph matrices for partitioning. Fiedler (1973) named $\lambda_2$ the algebraic connectivity and in 1975 proved the connectivity property of its eigenvectors. Pothen, Simon and Liou (1990) made the median split of the Fiedler vector a standard tool for sparse matrix ordering and parallel computing. Hagen and Kahng (1992) linked $\lambda_2$ to the ratio cut of circuits and proposed the EIG1 sweep. Guattery and Miller (1998) showed that the method can fail badly, and Spielman and Teng (1996 at FOCS, 2007 in the journal) showed why it works on planar graphs and meshes.

## References
