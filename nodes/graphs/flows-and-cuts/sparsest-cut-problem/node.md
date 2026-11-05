---
tag: 4CAH3A
kind: problem
slug: sparsest-cut-problem
name: Sparsest cut problem
aliases:
- uniform sparsest cut
- edge expansion problem
area: graphs/flows-and-cuts
level: research
summary: Minimize the ratio of cut capacity to the product of the sides' sizes.
prereqs: [min-cut-problem, multi-commodity-flow-problem, lp-relaxation, np-hard]
see_also: [multicut-problem, sparsest-cut-ugc-hardness, semidefinite-programming, cheeger-inequality, conductance, normalized-cut, integrality-gap, min-cut-max-flow-duality]
sources:
  - paper: doi:10.1145/331524.331526
    title: Tom Leighton and Satish Rao, Multicommodity max-flow min-cut theorems and their use in designing approximation algorithms, Journal of the ACM 46(6), 787 to 832 (1999)
    locator: the whole paper (the O(log n) approximation for uniform sparsest cut and the matching gap on expanders)
  - paper: doi:10.1007/BF01200757
    title: Nathan Linial, Eran London and Yuri Rabinovich, The geometry of graphs and some of its algorithmic applications, Combinatorica 15(2), 215 to 245 (1995)
    locator: the whole paper (rounding by embedding into l1, and the O(log k) flow-cut gap)
  - paper: doi:10.1137/S0097539794285983
    title: Yonatan Aumann and Yuval Rabani, An O(log k) approximate min-cut max-flow theorem and approximation algorithm, SIAM Journal on Computing 27(1), 291 to 301 (1998)
    locator: the whole paper (the O(log k) gap for general demands)
  - paper: doi:10.1145/1502793.1502794
    title: Sanjeev Arora, Satish Rao and Umesh Vazirani, Expander flows, geometric embeddings and graph partitioning, Journal of the ACM 56(2) (2009)
    locator: the whole paper (the O(sqrt(log n)) approximation by semidefinite programming)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms, Springer (2001)
    locator: Chapter 21, Sparsest cut
---

The sparsest cut problem asks, in an undirected graph with nonnegative edge weights, for a set $S$ of vertices that minimizes the weight of the edges leaving $S$ divided by $|S| \cdot |V \setminus S|$. A small ratio means a cut that is cheap for how evenly it splits the graph, the bottleneck that a balanced partition must cross. The general form puts a demand on each pair of vertices and divides by the demand that the cut separates. The problem is [NP-hard](/np-hard/). Its LP relaxation is the dual of a [multicommodity flow](/multi-commodity-flow-problem/) problem, and the gap between the two is $\Theta(\log n)$, which gives the $O(\log n)$ approximation of Leighton and Rao. Rounding through embeddings into $\ell_1$ extends it to $O(\log k)$ for $k$ demand pairs, and a [semidefinite](/semidefinite-programming/) relaxation gives $O(\sqrt{\log n})$ for the uniform case (Arora, Rao and Vazirani).

## In plain words

You want to split a network into two groups so that few links cross between them, but you do not want a lazy answer that chops off one lonely point. So you measure each split by the crossing links divided by how many pairs of points it separates. The best split cuts few links and still separates many pairs.

This finds the true bottleneck of a network: a narrow bridge between two large regions. It is hard to find exactly. Good approximate methods imagine sending a little traffic between every pair of points at once and see where the traffic jams: the jammed places mark a sparse cut, and the amount of traffic that fits gives a bound on how sparse any cut can be.

## Definition

**Input.** An undirected graph $G = (V, E)$ with $n \ge 2$ vertices and weights $w : E \to \mathbb{R}_{\ge 0}$, real or integer. Parallel edges add up; there is no direction, so there are no antiparallel pairs.

**Uniform sparsest cut.** Find $\emptyset \ne S \subsetneq V$ that minimizes

$$\phi(S) = \frac{w(\delta(S))}{|S| \cdot |V \setminus S|},$$

where $\delta(S)$ is the set of edges with exactly one end in $S$.

**General (non-uniform) sparsest cut.** Also given are demands $D : \binom{V}{2} \to \mathbb{R}_{\ge 0}$, and the denominator becomes $D(S) = \sum_{u \in S,\ v \notin S} D(u, v)$, the demand separated by $S$. Only sets with $D(S) > 0$ count. The uniform case has $D \equiv 1$. With $k$ pairs of positive demand, the guarantees below depend on $k$.

**Edge expansion.** The ratio $w(\delta(S)) / \min(|S|, |V \setminus S|)$ is within a factor of 2 of $n \cdot \phi(S)$, since $\frac{n}{2} \min(|S|, |V \setminus S|) \le |S| \cdot |V \setminus S| \le n \min(|S|, |V \setminus S|)$. So approximating one approximates the other within a factor of 2.

## Variants

- **Conductance.** Divide by the smaller total degree of the two sides instead of the smaller size; this is the [conductance](/conductance/) of a graph, tied to the second eigenvalue of the Laplacian by [Cheeger's inequality](/cheeger-inequality/).
- **Normalized cut.** Sum of the cut over the volume of each side, a clustering objective: [normalized cut](/normalized-cut/).
- **Balanced separator.** The cheapest cut whose sides each hold at least a fixed fraction of the vertices. Approximations for sparsest cut, applied repeatedly, give pseudo-approximations for it.
- **Directed sparsest cut.** Count only the edges from $S$ to $V \setminus S$; each edge of an antiparallel pair counts in its own direction. It is harder to approximate than the undirected problem.

## Examples

**Two triangles joined by a bridge.** The vertices $a, b, c$ form a triangle, $d, e, f$ form another, and the edge $c d$ joins them, all with weight 1. The set $S = \{a, b, c\}$ cuts one edge and separates $3 \cdot 3 = 9$ pairs, so $\phi(S) = \frac19$. The next best sets, such as $\{a, b\}$ or $\{a, b, c, d\}$, cut 2 edges and separate 8 pairs, ratio $\frac14$; a single vertex of degree 2 gives $\frac25$. So the sparsest cut is the bridge. A minimum cut, by contrast, would also accept the cut of weight 1 but does not care about balance; on a graph with a pendant vertex, minimum cut picks the pendant edge while sparsest cut may not.

**A cycle.** In the cycle $C_n$ with $n$ even, every cut crosses at least 2 edges, and two edges split it into arcs of $p$ and $n - p$ vertices, so the best is $p = n/2$ with $\phi = 2 / (n/2)^2 = 8 / n^2$.

**A zero-weight edge** contributes nothing to any cut; a graph whose only bridge has weight 0 has sparsest cut 0.

**Disconnected graph.** If $G$ is disconnected, a component $S$ gives $\phi(S) = 0$, which is optimal. In the general version, the answer is 0 exactly when some pair with positive demand lies in different components.

## Known algorithms

| method | ratio | notes |
|---|---|---|
| brute force | exact | $2^{n-1}$ sets |
| LP and metric rounding (Leighton-Rao) | $O(\log n)$ | uniform demands; the LP is maximum concurrent flow |
| embedding into $\ell_1$ (Linial-London-Rabinovich, Aumann-Rabani) | $O(\log k)$ | general demands with $k$ pairs; Bourgain's embedding |
| semidefinite programming (Arora-Rao-Vazirani) | $O(\sqrt{\log n})$ | uniform demands, the "expander flows" analysis |
| spectral partitioning | Cheeger bound | good for well-connected graphs, poor in the worst case |

**The LP and its rounding.** Every cut $S$ defines the *cut metric* $d_S(u, v) = [\,|\{u, v\} \cap S| = 1\,]$, and $\phi(S) = \sum_{uv \in E} w(uv)\, d_S(u, v) \big/ \sum_{u, v} D(u, v)\, d_S(u, v)$. Relaxing $d_S$ to an arbitrary metric $d$ gives

$$\lambda^{*} = \min_{d \text{ metric}} \frac{\sum_{uv \in E} w(uv)\, d(u, v)}{\sum_{u, v} D(u, v)\, d(u, v)},$$

which, after scaling the denominator to 1, is a linear program; its dual is the maximum concurrent flow with demands $D$. So $\lambda^{*} \le$ the sparsest cut. The minimum of the same ratio over metrics that embed into $\ell_1$ is exactly the sparsest cut, because every $\ell_1$ metric is a nonnegative sum of cut metrics and a ratio of sums is at least the smallest ratio of its terms. So any embedding of the LP metric into $\ell_1$ with distortion $\alpha$ yields a cut within factor $\alpha$; Bourgain's theorem gives $\alpha = O(\log n)$, and the version that only needs to preserve the $k$ demand pairs gives $O(\log k)$.

## Bounds

- **NP-hardness.** Uniform and general sparsest cut are NP-hard.
- **Flow-cut gap.** For uniform demands on constant-degree expanders, the sparsest cut is $\Omega(\log n)$ times the maximum concurrent flow, because most pairs are at distance $\Omega(\log n)$ and each unit of flow uses that many edges. So the LP gap is $\Theta(\log n)$, and $\Theta(\log k)$ in terms of the number of demand pairs.
- **Hardness of approximation.** Under the [unique games conjecture](/unique-games-conjecture/), the general version has no constant-factor approximation; see [sparsest cut hardness](/sparsest-cut-ugc-hardness/).
- **Lower bound.** Any exact method reads the input, $\Omega(n + m)$.

## Reductions

- **Sparsest cut LP to maximum concurrent flow**, by [LP duality](/lp-duality/); the cut condition of [multicommodity flow](/multi-commodity-flow-problem/) is that $\lambda \le \phi(S)$ for all $S$.
- **Edge expansion to uniform sparsest cut**, within a factor of 2 as above.
- **Balanced separator to sparsest cut**, by cutting sparse pieces off repeatedly until a balanced split appears.
- **Min-cut is not a special case.** For a single pair with demand 1, $D(S) = 1$ whenever $S$ separates the pair, and the problem becomes the [minimum $s$-$t$ cut](/min-cut-problem/), which is easy; the hardness comes from many demand pairs.

## Applications

- Divide-and-conquer on graphs: VLSI layout, minimum linear arrangement, and crossing number bounds, where Leighton and Rao's separator is the recursive step.
- Clustering and image segmentation through conductance and normalized cuts.
- Measuring expansion and mixing of networks and Markov chains.
- Finding bottlenecks in communication and road networks.

## References
