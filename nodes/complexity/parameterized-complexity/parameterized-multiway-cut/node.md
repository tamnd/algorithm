---
tag: 7G9N4C
kind: problem
slug: parameterized-multiway-cut
name: Parameterized multiway cut
aliases:
- k-multiway cut
area: complexity/parameterized-complexity
level: advanced
summary: "Delete at most k edges or vertices so that no two of the t given terminals stay connected. FPT in k, in O*(4^k) by important separators and O*(2^k) for the vertex version; NP-hard for t = 3."
prereqs: [multiway-cut-problem, fixed-parameter-tractable, important-separators]
see_also: [parameterized-multicut, multiway-cut-problem, important-separators, randomized-contractions, isolating-cuts, parameterized-vertex-cover, kernel-lower-bounds, parameterized-reduction]
sources:
  - book: isbn:9783319212746
    title: Marek Cygan, Fedor V. Fomin, Lukasz Kowalik, Daniel Lokshtanov, Daniel Marx, Marcin Pilipczuk, Michal Pilipczuk and Saket Saurabh, Parameterized Algorithms, Springer, 2015
    locator: Chapter 8, Finding cuts and separators (important cuts and the O*(4^k) algorithm for edge multiway cut)
  - paper: doi:10.1016/j.tcs.2005.10.007
    title: "Daniel Marx, Parameterized graph separation problems, Theoretical Computer Science 351(3), 394-406 (2006)"
    locator: node multiway cut is FPT parameterized by the cut size
  - paper: doi:10.1007/s00453-007-9130-6
    title: "Jianer Chen, Yang Liu and Songjian Lu, An improved parameterized algorithm for the minimum node multiway cut problem, Algorithmica 55(1), 1-13 (2009)"
    locator: node multiway cut in O*(4^k)
  - paper: doi:10.1145/2462896.2462899
    title: "Marek Cygan, Marcin Pilipczuk, Michal Pilipczuk and Jakub Onufry Wojtaszczyk, On multiway cut parameterized above lower bounds, ACM Transactions on Computation Theory 5(1), article 3 (2013)"
    locator: node multiway cut in O*(2^k), and FPT above the LP lower bound (conference version IPEC 2011)
  - paper: doi:10.1137/S0097539792225297
    title: "Elias Dahlhaus, David S. Johnson, Christos H. Papadimitriou, Paul D. Seymour and Mihalis Yannakakis, The complexity of multiterminal cuts, SIAM Journal on Computing 23(4), 864-894 (1994)"
    locator: NP-hardness of edge multiway cut for every fixed number t of terminals with t at least 3
  - paper: doi:10.1145/3390887
    title: "Stefan Kratsch and Magnus Wahlström, Representative sets and irrelevant vertices: new tools for kernelization, Journal of the ACM 67(3), article 16 (2020)"
    locator: randomized kernel with O(k^(t+1)) vertices for multiway cut with t terminals (conference version FOCS 2012)
  - paper: doi:10.1137/12086217X
    title: "Rajesh Chitnis, MohammadTaghi Hajiaghayi and Daniel Marx, Fixed-parameter tractability of directed multiway cut parameterized by the size of the cutset, SIAM Journal on Computing 42(4), 1674-1696 (2013)"
    locator: directed multiway cut is FPT in the cut size
  - paper: doi:10.1145/2594439
    title: "Marek Cygan, Stefan Kratsch, Marcin Pilipczuk, Michal Pilipczuk and Magnus Wahlström, Clique cover and graph separation: new incompressibility results, ACM Transactions on Computation Theory 6(2), article 6 (2014)"
    locator: no polynomial kernel for directed edge or vertex multiway cut, even with two terminals, unless NP is a subset of coNP/poly
---

Parameterized multiway cut is the [multiway cut problem](/multiway-cut-problem/) in its decision form, with the size $k$ of the cut as the [parameter](/parameter/). The input has $t$ terminals, and $t$ is not the parameter: the problem is NP-hard already for $t = 3$, but for every $t$ it is [fixed-parameter tractable](/fixed-parameter-tractable/) in $k$. Marx proved this in 2006 with [important separators](/important-separators/). The best known bounds are $O^\ast(4^k)$ for the edge version and $O^\ast(2^k)$ for the vertex version, where $O^\ast$ hides factors polynomial in the input size. This page gives the parameterized view; the multiway cut page has the optimization problem and its approximation algorithms.

## In plain words

A network has a few special points, the terminals. You want to cut it so that no two terminals can reach each other, and you may remove at most $k$ links (or, in the other version, at most $k$ ordinary points). The number of terminals can be large; what must be small is the number of things you remove.

The search works one terminal at a time. Around a terminal, many small cuts would separate it from the rest. It is enough to try the cuts that are pushed as far away from the terminal as possible, and there are at most $4^k$ of those. So the work grows with $k$, and only polynomially with the size of the network.

## Definition

**Edge multiway cut.**

- Instance: an undirected graph $G$, a set $T = \{t_1, \ldots, t_t\}$ of terminal vertices, and an integer $k \ge 0$.
- Parameter: $k$.
- Question: is there a set $S$ of at most $k$ edges such that each connected component of $G - S$ contains at most one terminal?

**Node multiway cut.** The same, but $S$ is a set of at most $k$ vertices of $V(G) \setminus T$, and $G - S$ deletes them. A variant with *deletable terminals* allows $S$ to contain terminals.

The graph is given by adjacency lists, and the input size is $n + m$ for $n$ vertices and $m$ edges. We write $t = |T|$ for the number of terminals, which is not bounded by the parameter.

## Variants

- **Parameter $t$.** For every fixed $t \ge 3$ the edge version is NP-hard (Dahlhaus, Johnson, Papadimitriou, Seymour and Yannakakis). So with $t$ as the only parameter the problem is para-NP-hard: no $f(t)\,n^{O(1)}$ and no $n^{f(t)}$ algorithm exists unless P = NP. For $t = 2$ it is a minimum $s$-$t$ cut, solvable by one maximum flow.
- **Parameter $k + t$.** Since the problem is FPT in $k$ alone, adding $t$ to the parameter gives nothing new for the running time, but it does matter for kernels (see Bounds).
- **Above a lower bound.** Let $\ell$ be the value of the LP relaxation of node multiway cut. Cygan, Pilipczuk, Pilipczuk and Wojtaszczyk showed that the vertex version is FPT in $k - \ell$, which can be much smaller than $k$.
- **Directed multiway cut.** Delete at most $k$ arcs or vertices so that no terminal reaches another. Chitnis, Hajiaghayi and Marx proved that it is FPT in $k$, with shadow removal on top of important separators.
- **Weighted.** With integer weights at least 1 and a bound $k$ on the total weight, an edge of weight $w$ can be replaced by $w$ parallel edges. With real weights and $k$ the number of deleted edges, the important separator bound does not apply; [randomized contractions](/randomized-contractions/) handle such variants.
- **Multiway cut-uncut.** Also given an equivalence relation on $T$: terminals in the same class must stay connected, and terminals in different classes must be separated. Chitnis, Cygan, Hajiaghayi, Pilipczuk and Pilipczuk solved the vertex version in $2^{O(k^2 \log k)} n^4 \log n$ time with randomized contractions.
- **Multicut.** Instead of separating every pair of terminals, separate given pairs. Multiway cut is the special case with all $\binom{t}{2}$ pairs. See [parameterized multicut](/parameterized-multicut/).

## Examples

Take the $3 \times 3$ grid with vertices $(i, j)$, $0 \le i, j \le 2$, and 12 edges, with terminals $(0, 0)$, $(0, 2)$ and $(2, 2)$. A scratch script solved both versions by brute force.

- The least edge multiway cut has 4 edges, and there are 7 optimal solutions. One of them cuts the two edges at $(0, 0)$ and the two edges at $(2, 2)$.
- The least node multiway cut has 3 vertices, and there are 2 optimal solutions, $\{(0, 1), (1, 0), (1, 2)\}$ and $\{(0, 1), (1, 2), (2, 1)\}$. Deleting vertices is stronger here: a middle vertex of degree 3 or 4 removes all its edges at once.
- The important $((0, 0), \{(0, 2), (2, 2)\})$-cuts of size at most 4 have sizes 2, 3 and 4. The size 3 cut is the three horizontal edges between columns 1 and 2. The search over important cuts answers YES for $k = 4$ on its first leaf and NO for $k = 3$ after 2 leaves.

## Known algorithms

- **Marx (2006).** Node multiway cut is FPT in $k$; this was the first use of [important separators](/important-separators/).
- **Chen, Liu and Lu (2009).** Node multiway cut in $O^\ast(4^k)$, from the bound of $4^k$ on the number of important separators of size at most $k$.
- **Edge version by the pushing lemma.** Some optimal solution contains an important $(t_i, T \setminus \{t_i\})$-cut for any terminal $t_i$, which gives a search tree with $4^k$ leaves and time $O(4^k k^3 (n + m))$. The proof is on the important separators page.
- **Cygan, Pilipczuk, Pilipczuk and Wojtaszczyk (2013).** Node multiway cut in $O^\ast(2^k)$, by branching with the LP lower bound as a measure. The edge version reduces to it (see Reductions), so the same bound holds for edges.
- **Directed graphs.** FPT in $k$ (Chitnis, Hajiaghayi and Marx 2013).

## Bounds

- **Classical complexity.** NP-complete for every fixed $t \ge 3$ in the edge version, under polynomial-time many-one reductions (Dahlhaus et al.).
- **Lower bound in time.** Node multiway cut has no $2^{o(k)} n^{O(1)}$ algorithm unless the exponential time hypothesis (ETH) fails. This follows from the reduction from vertex cover below, which keeps $k$ and increases the size only linearly; vertex cover has no such algorithm under ETH. See [strong exponential time hypothesis](/strong-exponential-time-hypothesis/) for ETH.
- **Kernels.** Kratsch and Wahlström gave a randomized polynomial kernel with $O(k^{t + 1})$ vertices, which is polynomial when $t$ is a constant. For directed edge or vertex multiway cut there is no polynomial kernel in $k$, even with $t = 2$, unless NP is a subset of coNP/poly (Cygan, Kratsch, Pilipczuk, Pilipczuk and Wahlström). See [kernel lower bounds](/kernel-lower-bounds/).

## Reductions

- **From vertex cover to node multiway cut.** Given a graph $H$, add for each vertex $v$ a new terminal $t_v$ joined only to $v$, and keep $k$. A vertex cover $C$ of $H$ is a node multiway cut: after deleting $C$, every remaining vertex $v$ has no neighbor in $H$, so its component is $\{v, t_v\}$. Conversely, a node multiway cut $S$ must hit each path $t_u, u, v, t_v$ for an edge $uv$, and it contains no terminal, so it contains $u$ or $v$; thus $S$ is a vertex cover. This is a parameterized reduction with $k' = k$, in linear time. The scratch script checked it on a triangle with a pendant edge (both optima are 2) and on 60 random graphs with at most 6 vertices (seed 11); all agreed.
- **From edge to node multiway cut.** Subdivide every edge by a new deletable vertex, and replace each non-terminal vertex $v$ of $G$ by $k + 1$ copies with the same neighbors. Deleting a subdivision vertex is deleting an edge, and deleting all copies of a vertex costs more than $k$. So the two instances have the same answer, with $k' = k$ and size $O(k (n + m))$.
- **To multicut.** Multiway cut with $t$ terminals is multicut with all $\binom{t}{2}$ terminal pairs, with the same $k$.
- **Minimum $s$-$t$ cut.** The case $t = 2$ is the [minimum cut problem](/min-cut-problem/), in polynomial time by the [max-flow min-cut theorem](/max-flow-min-cut-theorem/).

## Applications

The pushing lemma for multiway cut is the model for many cut algorithms. The same reasoning appears in the compression step of [directed feedback vertex set](/directed-feedback-vertex-set/) and in multicut. The variant above the LP bound is a tool in its own right: Cygan, Pilipczuk, Pilipczuk and Wojtaszczyk use it to solve almost 2-SAT and vertex cover above the size of a maximum matching in $O^\ast(4^k)$, where $k$ is the excess over the lower bound. Edge multiway cut with a few terminals also models image segmentation with a few labels, where the approximation view of the [multiway cut problem](/multiway-cut-problem/) is more common.

## References
