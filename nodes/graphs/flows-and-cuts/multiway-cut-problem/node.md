---
tag: FW31D6
kind: problem
slug: multiway-cut-problem
name: Multiway cut problem
aliases:
- multiterminal cut
area: graphs/flows-and-cuts
level: advanced
summary: Find a minimum-weight edge set separating every pair of k given terminals.
prereqs: [min-cut-problem, np-hard, approximation-ratio, lp-relaxation]
see_also: [multicut-problem, isolating-cuts, multiway-cut-inapproximability, randomized-rounding, unique-games-conjecture, gomory-hu-tree, sparsest-cut-problem, image-segmentation-graph-cuts]
sources:
  - paper: doi:10.1137/S0097539792225297
    title: E. Dahlhaus, D. S. Johnson, C. H. Papadimitriou, P. D. Seymour and M. Yannakakis, The complexity of multiterminal cuts, SIAM Journal on Computing 23(4), 864 to 894 (1994)
    locator: the whole paper (NP-hardness and MAX SNP-hardness for k ≥ 3, the polynomial algorithm for planar graphs with fixed k, and the 2 − 2/k isolating cut heuristic)
  - paper: doi:10.1006/jcss.1999.1687
    title: Gruia Călinescu, Howard Karloff and Yuval Rabani, An improved approximation algorithm for MULTIWAY CUT, Journal of Computer and System Sciences 60(3), 564 to 574 (2000)
    locator: the whole paper (the simplex relaxation and its rounding with ratio 3/2 − 1/k)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms, Springer (2001)
    locator: Chapter 4, Multiway cut and k-cut (the isolating cut heuristic), and Chapter 19, Multiway cut (the LP relaxation and its rounding)
---

The multiway cut problem asks, in an undirected graph with nonnegative edge weights and $k$ terminals $t_1, \ldots, t_k$, for a set of edges of least total weight whose removal leaves no path between any two terminals. Equivalently, it asks for a partition of the vertices into $k$ parts, one terminal in each, with the least weight of edges between different parts. For $k = 2$ it is the [minimum $s$-$t$ cut](/min-cut-problem/), solvable by one maximum flow. For every fixed $k \ge 3$ it is [NP-hard](/np-hard/), and even hard to approximate within some constant, as shown by Dahlhaus, Johnson, Papadimitriou, Seymour and Yannakakis. Two classic approximations are the union of [isolating cuts](/isolating-cuts/), within $2 - 2/k$, and the rounding of a geometric LP relaxation by Călinescu, Karloff and Rabani, within $3/2 - 1/k$.

## In plain words

A network has several special points, say several data centers, and you want to cut links so that no two special points can reach each other any more, while paying as little as possible for the links you cut.

With two special points, this is the classic cheapest-cut problem, which is easy. With three or more it becomes hard: the cheap cut for one pair can be the wrong choice for the others. A simple rule works well, though: for each special point, find the cheapest way to cut it off from all the others, and use all these cuts except the most expensive one. This never costs more than about twice the best answer.

## Definition

**Input.** An undirected graph $G = (V, E)$ with weights $w : E \to \mathbb{R}_{\ge 0}$, real or integer, and a set $T = \{t_1, \ldots, t_k\}$ of $k \ge 2$ distinct terminals. Parallel edges add up and self-loops never matter. The graph has no direction, so there are no antiparallel pairs; the directed problem is a variant below.

**Output.** A set $F \subseteq E$ such that no two terminals are joined by a path in $G - F$, of least weight $w(F)$. Equivalently, a partition $V = V_1 \cup \cdots \cup V_k$ with $t_i \in V_i$ that minimizes the weight of the edges whose ends lie in different parts. *Proof of the equivalence.* For a partition, the edges between parts separate all terminals. For a feasible $F$, let $V_i$ be the component of $t_i$ in $G - F$ for $i \ge 2$, and put all other vertices into $V_1$; every edge between different parts leaves some component of $G - F$ or joins two of them, so it lies in $F$. $\square$

## Variants

- **Node multiway cut.** Remove vertices other than the terminals, with weights on vertices.
- **Directed multiway cut.** In a directed graph, remove edges so that no terminal reaches another. Each edge of an antiparallel pair is a separate edge with its own weight, and only edges leaving a part need to be cut.
- **Multicut.** Separate $k$ given pairs $(s_i, t_i)$ rather than all pairs of a terminal set: the [multicut problem](/multicut-problem/), which contains multiway cut as the case of all $\binom{k}{2}$ pairs.
- **$k$-cut.** No terminals; split the graph into $k$ nonempty parts at least cost. It is polynomial for fixed $k$ and NP-hard when $k$ is part of the input.
- **Labeling problems.** In vision, each pixel gets one of $k$ labels with costs for the labels and for neighbors with different labels; multiway cut is the special case without label costs, and the $\alpha$-expansion method of [graph cuts](/image-segmentation-graph-cuts/) solves such problems approximately with $s$-$t$ cuts.

## Examples

**A triangle with a center.** The terminals $t_1, t_2, t_3$ are joined pairwise by edges of weight 1, and each is joined to a center $c$ by an edge of weight 2. Every solution cuts the three terminal edges, weight 3, and puts $c$ with one terminal, cutting the other two center edges, weight 4. So the optimum is 7. The isolating cut of each terminal is $\{t_i\}$, of weight 4 (the alternative $\{t_i, c\}$ has weight 6), and the union of two of them, say those of $t_1$ and $t_2$, has weight $1 + 1 + 1 + 2 + 2 = 7$, because the edge $t_1 t_2$ is shared; here the heuristic is optimal, while its guarantee $2 - 2/3 = 4/3$ would allow up to $28/3$.

**Two terminals.** With $k = 2$ the problem is the minimum $s$-$t$ cut, and the isolating cut heuristic returns one isolating cut, which is optimal.

**A zero-weight edge.** An edge of weight 0 can be cut for free, so it never changes the optimum.

**Terminals already separated.** If no path joins any two terminals, the empty set is optimal, of weight 0. If only some pairs are joined, only those need cutting.

## Known algorithms

| method | guarantee | notes |
|---|---|---|
| one minimum cut per pair, or $k = 2$ | exact for $k = 2$ | one maximum flow |
| isolating cut heuristic | $2 - 2/k$ | $k$ maximum flows, or $O(\log k)$ with [isolating cuts](/isolating-cuts/) |
| Călinescu-Karloff-Rabani rounding | $3/2 - 1/k$ | LP over the simplex, randomized rounding |
| later roundings of the same LP | about 1.3 | the LP's integrality gap is the limit under the unique games conjecture |
| planar graphs, fixed $k$ | exact | polynomial for each fixed $k$ |
| trees | exact | dynamic programming |
| parameterized by the cut size | exact | fixed-parameter tractable |

**The isolating cut heuristic.** For each $i$, let $C_i$ be a minimum cut that separates $t_i$ from the other terminals (merge them into one sink). Output the union of all $C_i$ except the heaviest. *Feasible:* for $i$ other than the dropped index $j$, $C_i$ cuts $t_i$ from every other terminal, so every pair of terminals has a member other than $t_j$ and is separated. *Ratio:* in an optimal partition, the edges leaving $V_i$ form an isolating cut for $t_i$, so $w(C_i) \le w(\delta(V_i))$, and $\sum_i w(\delta(V_i)) = 2\,\mathrm{OPT}$ because each cut edge leaves exactly two parts. Dropping the heaviest keeps at most a $(1 - 1/k)$ fraction of $\sum_i w(C_i)$, so the output weighs at most $(1 - 1/k) \cdot 2\,\mathrm{OPT} = (2 - 2/k)\,\mathrm{OPT}$. $\square$

**The CKR relaxation.** Give each vertex a point $x_v$ of the simplex $\{x \in \mathbb{R}^k_{\ge 0} : \sum_i x_i = 1\}$, with $x_{t_i} = e_i$, and minimize $\sum_{uv} w(uv) \cdot \frac12 \lVert x_u - x_v \rVert_1$. An integral solution puts each vertex at a corner, which is a partition, and then the objective is its cut weight. Călinescu, Karloff and Rabani round with a random threshold and a random order of the terminals and prove the ratio $3/2 - 1/k$.

## Bounds

For each fixed $k \ge 3$ the problem is NP-hard, and MAX SNP-hard, so it has no PTAS unless P = NP; see [multiway cut inapproximability](/multiway-cut-inapproximability/). In planar graphs it is NP-hard when $k$ is part of the input and polynomial for each fixed $k$. Under the [unique games conjecture](/unique-games-conjecture/), no polynomial algorithm beats the integrality gap of the CKR relaxation. Lower bound for any exact algorithm: $\Omega(n + m)$ to read the input.

## Reductions

- **Multiway cut to multicut**, with all pairs of terminals as the pairs.
- **$k = 2$ to max flow**, by the max-flow min-cut theorem.
- **Isolating cuts to max flow**, one flow per terminal, or $O(\log k)$ flows with the isolating cuts lemma.
- **NP-hardness for $k = 3$** is by a reduction from a cut problem in Dahlhaus et al.; the problem stays hard in planar graphs when $k$ grows with the input.

## Applications

- Partitioning a program or a circuit among $k$ processors with fixed placements, so that communication between processors is least.
- Labeling problems in computer vision, where terminals stand for labels.
- Clustering with $k$ given seed points.
- Network design and security, where several sites must be isolated from each other.

## References
