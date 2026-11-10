---
tag: Q77RQ3
kind: problem
slug: survivable-network-design
name: Survivable network design
aliases:
- SNDP
- survivable network design problem
- EC-SNDP
area: approximation/lp-rounding
level: advanced
summary: Find the cheapest subgraph with at least r(u, v) disjoint paths between each pair u, v, so that each pair stays connected after r(u, v) - 1 failures.
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(2^m n^2 m^2)}
prereqs: [steiner-forest, menger-theorem, edge-connectivity, lp-relaxation, np-hard]
see_also: [generalized-steiner-network, jain-iterative-rounding-network-design, steiner-forest, goemans-williamson-steiner-forest, k-edge-connected-graph, vertex-connectivity, iterative-rounding, steiner-tree-problem]
sources:
  - paper: doi:10.1007/s004930170004
    title: Kamal Jain, A factor 2 approximation algorithm for the generalized Steiner network problem, Combinatorica 21(1), 2001
    locator: the cut LP, weak supermodularity, and the factor 2 for edge connectivity
  - title: David P. Williamson, Michel X. Goemans, Milena Mihail and Vijay V. Vazirani, A primal-dual approximation algorithm for generalized Steiner network problems, Combinatorica 15(3), 1995
    locator: the primal-dual algorithm with ratio 2 times the largest requirement
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 11.3 (survivable network design by iterative rounding)
  - book: isbn:9783540653677
    title: Vijay V. Vazirani, Approximation Algorithms
    locator: Chapter 23 (Steiner network)
  - book: isbn:9781107007512
    title: Lap Chi Lau, R. Ravi and Mohit Singh, Iterative Methods in Combinatorial Optimization, Cambridge University Press, 2011
    locator: Chapter 10 (network design)
---

Survivable network design (SNDP) asks for the cheapest subgraph of a graph with edge costs that has many disjoint paths between chosen pairs of vertices. Each pair $u, v$ comes with a requirement $r_{uv}$, and the subgraph must have $r_{uv}$ edge-disjoint paths between $u$ and $v$. By [Menger's theorem](/menger-theorem/), the pair then stays connected after any $r_{uv} - 1$ edges fail. With requirements in $\{0, 1\}$ the problem is the [Steiner forest problem](/steiner-forest/), so it is NP-hard. For edge connectivity the best known ratio is 2, by the [iterative rounding algorithm of Jain](/jain-iterative-rounding-network-design/), and the problem with its cut LP is studied on the page on the [generalized Steiner network problem](/generalized-steiner-network/). If the paths must be vertex-disjoint, the problem is much harder to approximate.

## In plain words

You build a network of links, and each link has a price. Some pairs of sites must stay in contact even if links break. For each pair you say how many separate routes it needs: one route means no protection, two routes means it survives one broken link, and so on.

Two routes are separate if they share no link. The cheapest way to give every pair its routes is hard to find, but there is a fast method that never pays more than twice the best price.

A stronger version asks that routes share no site either, so the pair also survives the loss of a site. That version is much harder, even to approximate.

## Definition

**Input.** An undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges, a cost $c_e \ge 0$ for each edge, and a requirement $r_{uv} \in \{0, 1, 2, \ldots\}$ for each pair of vertices, with $r_{uv} = r_{vu}$.

**Output (edge connectivity, EC-SNDP).** A set $F \subseteq E$ of least cost $c(F)$ such that the subgraph $(V, F)$ has at least $r_{uv}$ edge-disjoint paths between $u$ and $v$, for each pair. Each edge is used at most once. If $G$ itself does not meet the requirements, there is no solution.

**Cut form.** For $S \subseteq V$, let $\delta_F(S)$ be the edges of $F$ with one end in $S$, and let

$$f(S) = \max \{ r_{uv} : |S \cap \{u, v\}| = 1 \},$$

with $f(S) = 0$ if no pair is split by $S$. By Menger's theorem, $F$ is feasible exactly when $|\delta_F(S)| \ge f(S)$ for each $S$. The LP relaxation of this form is the subject of the page on the [generalized Steiner network problem](/generalized-steiner-network/).

**Vertex connectivity (VC-SNDP).** The paths between $u$ and $v$ must have no inner vertex in common.

**Element connectivity.** A set $R$ of terminals is given, and all requirements are between terminals. The paths must not share an edge or a vertex outside $R$; they may share terminals.

**Decision version.** Given $B$, is there a feasible $F$ with $c(F) \le B$? It is NP-complete for edge connectivity.

## Variants

- **Steiner forest and Steiner tree.** Requirements in $\{0, 1\}$ give the [Steiner forest problem](/steiner-forest/). If also all pairs with $r_{uv} = 1$ meet a common root, it is the [Steiner tree problem](/steiner-tree-problem/).
- **$k$-connected spanning subgraph.** All requirements equal $k$. The output is a cheapest [$k$-edge-connected](/k-edge-connected-graph/) or [$k$-vertex-connected](/k-vertex-connected-graph/) spanning subgraph.
- **Copies allowed.** Each edge may be bought several times, at its cost each time. This version is easier, since the LP has no upper bounds $x_e \le 1$, and it is often called the generalized Steiner network problem with multiplicities.
- **Augmentation.** A graph is given for free, and the task is to buy the cheapest new edges that raise its connectivity.
- **Degree bounds.** Each vertex has a degree bound $b_v$. Iterative relaxation gives cost $2 \cdot$ OPT with degrees at most $2b_v + 3$ (Lau, Naor, Salavatipour and Singh 2007).
- **Directed graphs.** The requirements count directed paths from $u$ to $v$. Even the directed Steiner tree case has no known polylogarithmic ratio in polynomial time.

## Examples

Take vertices $a, b, c, d, e$, the edges $ab$ of cost 1, $bc$ 1, $ca$ 1, $cd$ 2, $de$ 2, $ea$ 2 and $bd$ 4, and the requirements $r_{ab} = 1$, $r_{ac} = 1$ and $r_{ad} = 2$, with all others 0.

An optimal solution is $\{ab, ca, cd, de, ea\}$ of cost 8. The cycle $a, c, d, e$ gives the two edge-disjoint paths $a c d$ and $a e d$, and the edges $ab$ and $ca$ join $b$ and $c$ to $a$. The cut LP has the optimum $15/2$, with $x_{ca} = x_{cd} = 1$, $x_{ab} = x_{de} = x_{ea} = x_{bd} = 1/2$ and $x_{bc} = 0$. Since costs are integers, no solution costs less than 8. Jain's algorithm rounds up the edges with $x_e \ge 1/2$ in the first round and returns a solution of cost 12, within $2 \cdot 15/2 = 15$.

## Known algorithms

| algorithm | connectivity | guarantee |
|---|---|---|
| brute force over edge sets, with a max flow for each pair | any | exact, time $O(2^m n^2 m^2)$ |
| [Goemans-Williamson](/goemans-williamson-steiner-forest/) (1995) | edge, $r \in \{0, 1\}$ | ratio $2 - 2/k$ |
| Williamson, Goemans, Mihail and Vazirani (1995) | edge | primal-dual, ratio $2 r_{\max}$ |
| Goemans, Goldberg, Plotkin, Shmoys, Tardos and Williamson (1994) | edge | primal-dual in phases, ratio $2 H(r_{\max})$ |
| Khuller and Vishkin (1994) | edge, all $r_{uv} = k$ | ratio 2, by two arborescence packings |
| [Jain](/jain-iterative-rounding-network-design/) (2001) | edge | iterative rounding, ratio 2 |
| Fleischer, Jain and Williamson (2006) | element | iterative rounding, ratio 2 |
| Chuzhoy and Khanna (2012) | vertex | ratio $O(k^3 \log n)$ for $k = r_{\max}$ |

$H(r) = 1 + 1/2 + \cdots + 1/r$ is the harmonic number. Exact methods use integer programming with the cut LP, separated by max flows; Grötschel, Monma and Stoer solved real instances in this way.

## Bounds

- **Lower bound used.** The value of the cut LP of the [generalized Steiner network problem](/generalized-steiner-network/).
- **Integrality gap.** At most 2 for edge connectivity, by Jain's analysis. At least $2 - 2/n$: on a cycle with unit costs and $r_{uv} = 1$ for all pairs, $x_e = 1/2$ has value $n/2$, while a solution needs $n - 1$ edges.
- **Hardness of EC-SNDP.** It contains Steiner tree, so it is NP-hard to approximate within $96/95$. No ratio below 2 is known, even for Steiner forest.
- **Hardness of VC-SNDP.** Kortsarz, Krauthgamer and Lee (2004) showed hardness within $2^{\log^{1 - \varepsilon} n}$ for each $\varepsilon > 0$, unless NP has quasi-polynomial algorithms. Chakraborty, Chuzhoy and Khanna (2008) showed hardness within $k^{\varepsilon}$ for some fixed $\varepsilon > 0$.
- **NP-hard with requirement 2.** Even the 2-edge-connected spanning subgraph problem with unit costs is NP-hard (see Reductions).

## Reductions

- **From Hamiltonian cycle.** With unit costs and $r_{uv} = 2$ for all pairs, a 2-edge-connected spanning subgraph has at least $n$ edges, since every vertex has degree at least 2. It has exactly $n$ edges if and only if it is a Hamiltonian cycle. So deciding whether the optimum is $n$ is NP-hard.
- **To the cut LP.** By Menger's theorem, the requirement for the pair $u, v$ holds exactly when every set $S$ that splits $u$ and $v$ has $|\delta_F(S)| \ge r_{uv}$. This turns SNDP into the covering problem of the [generalized Steiner network](/generalized-steiner-network/) page. A [separation oracle](/separation-oracle/) runs a [max flow](/max-flow-problem/) for each pair with $r_{uv} > 0$.
- **Vertex, element and edge.** Paths with no common inner vertex are element-disjoint, and element-disjoint paths are edge-disjoint. So a solution for vertex connectivity is a solution for element connectivity, which is a solution for edge connectivity, with the same requirements.
- **Metric closure fails.** Unlike for Steiner forest, the graph cannot be replaced by its shortest path closure. Two disjoint paths in the closure may map to paths in $G$ that share an edge.

## Applications

- **Telecommunication networks.** Fiber networks must keep important nodes in contact after one or two link cuts. Grötschel, Monma and Stoer built the integer programming methods for this setting in the early 1990s.
- **Power and transport networks.** The same model gives networks that keep supply routes open when some lines fail.
- **Theory.** SNDP was the problem for which [iterative rounding](/iterative-rounding/) was invented, and it is a main test case for primal-dual and LP methods in network design.

## References
