---
tag: G973MS
kind: problem
slug: generalized-steiner-network
name: Generalized Steiner network problem
aliases:
- GSNDP
- generalized Steiner network
- Steiner network problem
area: approximation/lp-rounding
level: advanced
summary: Buy edges so that each pair u, v has r(u, v) edge-disjoint paths; the cut LP with a weakly supermodular right side has a vertex with some value at least 1/2, which gives ratio 2.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(2^m n^2 m^2)}
prereqs: [survivable-network-design, lp-relaxation, extreme-point, menger-theorem, submodular-function]
see_also: [survivable-network-design, jain-iterative-rounding-network-design, iterative-rounding, steiner-forest, goemans-williamson-steiner-forest, separation-oracle, integrality-gap, extreme-point]
sources:
  - paper: doi:10.1007/s004930170004
    title: Kamal Jain, A factor 2 approximation algorithm for the generalized Steiner network problem, Combinatorica 21(1), 2001
    locator: the LP, weakly supermodular functions, and the theorem that a vertex has a value at least 1/2
  - paper: doi:10.1137/S0097539792236237
    title: Ajit Agrawal, Philip Klein and R. Ravi, When trees collide, an approximation algorithm for the generalized Steiner problem on networks, SIAM Journal on Computing 24(3), 1995
    locator: the version with multiple copies of edges
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 23 (Steiner network)
  - book: isbn:9781107007512
    title: Lap Chi Lau, R. Ravi and Mohit Singh, Iterative Methods in Combinatorial Optimization, Cambridge University Press, 2011
    locator: Chapter 10 (network design, the survivable network design problem)
---

The generalized Steiner network problem is the edge-connectivity form of [survivable network design](/survivable-network-design/), stated through its cut LP. A graph with edge costs and a requirement $r_{uv}$ for each pair of vertices are given, and the task is to buy a cheapest set of edges with $r_{uv}$ edge-disjoint paths between each pair $u, v$. The requirements become one function $f$ on vertex sets, and the problem becomes: cover each cut $\delta(S)$ at least $f(S)$ times. Jain (2001) proved that each vertex of the LP relaxation has an edge with value at least $1/2$. This gives the [iterative rounding algorithm](/jain-iterative-rounding-network-design/) with ratio 2, which is also the best known bound on the integrality gap. This page covers the problem as a covering problem with the function $f$, and the structure of its LP.

## In plain words

Each pair of sites needs a number of routes that share no link. Instead of looking at the routes, look at the walls: draw a line around any group of sites. If the line separates two sites that need 3 routes, at least 3 bought links must cross it. The network is good exactly when every such line is crossed enough times.

So the problem is: buy links to cross every wall enough times. Allow fractions of links, and you get a linear program. Its corner points always have some link that is at least half bought. Buy that link in full, and repeat. Each step at most doubles the price, which gives the factor 2.

## Definition

**Input.** An undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges, costs $c_e \ge 0$, and integer requirements $r_{uv} = r_{vu} \ge 0$ for the pairs of vertices.

**Output.** A set $F \subseteq E$ of least cost such that $(V, F)$ has $r_{uv}$ edge-disjoint paths between $u$ and $v$ for each pair. Each edge can be bought once.

**Requirement function.** For $S \subseteq V$, $f(S) = \max \{ r_{uv} : u \in S, \ v \notin S \}$, or 0 if there is no such pair. By [Menger's theorem](/menger-theorem/), $F$ is feasible exactly when $|F \cap \delta(S)| \ge f(S)$ for every $S$.

**The cut LP.**

$$\min \sum_{e \in E} c_e x_e \ \text{ s.t. } \ x(\delta(S)) \ge f(S) \text{ for all } S \subseteq V, \quad 0 \le x_e \le 1.$$

Here $x(\delta(S)) = \sum_{e \in \delta(S)} x_e$. The upper bound $x_e \le 1$ says that each edge is bought at most once.

**Weak supermodularity.** A function $f$ on the subsets of $V$ is *weakly supermodular* if $f(V) = 0$ and, for all $A, B \subseteq V$, at least one of these holds:

$$f(A) + f(B) \le f(A \cap B) + f(A \cup B), \qquad f(A) + f(B) \le f(A \setminus B) + f(B \setminus A).$$

The function $f$ of the requirements has this property. If $F$ is a set of edges already bought, the residual function $f(S) - d_F(S)$ has it too, with $d_F(S) = |F \cap \delta(S)|$. The reason is that $d_F$ satisfies both reverse inequalities: $d_F(A) + d_F(B) \ge d_F(A \cap B) + d_F(A \cup B)$ and $d_F(A) + d_F(B) \ge d_F(A \setminus B) + d_F(B \setminus A)$. Jain's algorithm works for every weakly supermodular $f$ for which the LP can be separated.

**Jain's theorem.** If $f$ is weakly supermodular and not identically 0, every vertex $x$ of the cut LP has an edge with $x_e \ge 1/2$. The proof is on the [algorithm page](/jain-iterative-rounding-network-design/).

## Variants

- **Requirements in $\{0, 1\}$.** The function $f$ is then *proper* in the sense of Goemans and Williamson, and the problem is the [Steiner forest problem](/steiner-forest/). The primal-dual algorithm gives ratio $2 - 2/k$.
- **Multiple copies.** If each edge can be bought any number of times, the LP has $x_e \ge 0$ with no upper bound. Agrawal, Klein and Ravi gave ratio $2 \lceil \log_2(r_{\max} + 1) \rceil$ for this version, and Jain's ratio 2 holds for it too.
- **General weakly supermodular $f$.** Any weakly supermodular $f$ with a polynomial separation method gives the same ratio 2, even if it does not come from pair requirements.
- **Vertex and element connectivity.** The cut form is different, since a cut must also count removed vertices. See [survivable network design](/survivable-network-design/).
- **Degree bounds.** Adding $x(\delta(v)) \le b_v$ to the LP and using [iterative relaxation](/iterative-relaxation/) gives cost $2 \cdot \text{OPT}$ with degree at most $2b_v + 3$.

## Examples

**An LP vertex.** Take vertices $a, b, c, d, e$, the edges $ab$ of cost 1, $bc$ 1, $ca$ 1, $cd$ 2, $de$ 2, $ea$ 2 and $bd$ 4, and $r_{ab} = 1$, $r_{ac} = 1$, $r_{ad} = 2$. Then $f(\{a\}) = 2$, $f(\{b\}) = 1$, $f(\{d\}) = 2$, $f(\{e\}) = 0$, and $f(\{a, b, c\}) = 2$, because the set splits $a$ and $d$. The LP optimum $15/2$ is reached at $x_{ca} = x_{cd} = 1$, $x_{ab} = x_{de} = x_{ea} = x_{bd} = 1/2$, $x_{bc} = 0$. The cuts around $a$, $b$ and $d$ are tight: $2$, $1$ and $2$. Six edges have $x_e \ge 1/2$, as Jain's theorem promises at least one. The optimum is 8.

**A half-integral vertex.** On a triangle with unit costs and $r_{uv} = 1$ for all three pairs, the point $x = (1/2, 1/2, 1/2)$ is a vertex: the three tight cuts $x_e + x_{e'} = 1$ around the three vertices have only this solution. It has value $3/2$, while the optimum is 2. On a cycle of $n$ vertices the same point gives the gap $(n - 1)/(n/2) = 2 - 2/n$. So the $1/2$ in Jain's theorem cannot be raised.

**Weak, not full, supermodularity.** Take $r_{uv} = 1$ for one pair only, $A = \{u\}$ and $B = \{u, v\}$. Then $f(A) + f(B) = 1 + 0$, and $f(A \cap B) + f(A \cup B) = 1 + 0$, so the first inequality holds. With $A = \{u, w\}$ and $B = \{v, w\}$, $f(A) + f(B) = 2$ but $f(A \cap B) + f(A \cup B) = f(\{w\}) + f(\{u, v, w\}) = 0$. Here the second inequality holds, since $f(\{u\}) + f(\{v\}) = 2$. So $f$ is not supermodular, but it is weakly supermodular.

## Known algorithms

| algorithm | guarantee |
|---|---|
| brute force over edge sets | exact, time $O(2^m n^2 m^2)$ |
| solving the cut LP by the [ellipsoid method](/ellipsoid-method/) with a max flow [separation oracle](/separation-oracle/) | polynomial time, the lower bound |
| primal-dual of Williamson, Goemans, Mihail and Vazirani (1995) | ratio $2 r_{\max}$ |
| primal-dual in phases of Goemans et al. (1994) | ratio $2 H(r_{\max})$ |
| [Jain's iterative rounding](/jain-iterative-rounding-network-design/) (2001) | ratio 2 against the cut LP |

The separation oracle is simple: for a point $x$, compute a minimum $u$-$v$ cut with capacities $x$ for each pair with $r_{uv} > 0$. A cut of capacity less than $r_{uv}$ is a violated constraint. A [Gomory-Hu tree](/gomory-hu-tree/) gives all of them with $n - 1$ max flows.

## Bounds

- **Integrality gap.** At most 2 by Jain's theorem and the telescoping argument of [iterative rounding](/iterative-rounding/), and at least $2 - 2/n$ by the cycle above.
- **Extreme point structure.** After the edges with $x_e = 0$ or $x_e = 1$ are removed, each vertex has a laminar family $\mathcal{L}$ of tight sets with linearly independent cut vectors, and $|\mathcal{L}|$ equals the number of the remaining edges. The proof uses uncrossing, which needs weak supermodularity.
- **Hardness.** The problem contains Steiner tree, so it is NP-hard to approximate within $96/95$. No ratio below 2 is known.
- **Thresholds above $1/2$ fail.** On the triangle above, every edge has value exactly $1/2$, so a rounding step that only buys edges with $x_e \ge \theta$ for some $\theta > 1/2$ may find nothing to buy.

## Reductions

- **From survivable network design.** The edge-connectivity version of [SNDP](/survivable-network-design/) is the same problem, by Menger's theorem.
- **Residual problems.** After buying a set $F$, the rest of the problem is the same problem on $E \setminus F$ with the function $f(S) - |F \cap \delta(S)|$. This function is weakly supermodular, so the method can repeat.
- **Steiner forest.** Requirements in $\{0, 1\}$ give the [Steiner forest problem](/steiner-forest/), and the cut LP is its cut LP.
- **Minimum cost $k$-edge-connected subgraph.** All $r_{uv} = k$ gives $f(S) = k$ for each $\emptyset \ne S \ne V$.

## Applications

- **Robust network design.** It is the model for networks that must keep pairs connected after edge failures, used in fiber and backbone network planning.
- **A test case for LP methods.** Jain's theorem started [iterative rounding](/iterative-rounding/). The same counting proof was then used for bounded-degree trees, matroid problems and the generalized assignment problem.

## References
