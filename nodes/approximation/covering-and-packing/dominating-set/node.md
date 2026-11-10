---
tag: S38CYJ
kind: problem
slug: dominating-set
name: Dominating set problem
aliases:
- k-dominating set
- minimum dominating set
area: approximation/covering-and-packing
level: intro
summary: Find a smallest vertex set such that every vertex is in it or adjacent to it; it is set cover on closed neighbourhoods, so greedy gives ln(Δ + 1) + 1.
prereqs: [set-cover]
see_also: [set-cover, greedy-set-cover, dominating-set-inapproximability, parameterized-dominating-set, distributed-dominating-set, vertex-cover, baker-planar-ptas, element-frequency]
sources:
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability
    locator: Appendix A1.1, problem GT2 (dominating set)
  - book: isbn:9781119061953
    title: Noga Alon and Joel H. Spencer, The Probabilistic Method, fourth edition
    locator: Chapter 1, Section 1.2 (dominating sets of graphs with large minimum degree)
  - paper: doi:10.1016/S0022-0000(74)80044-9
    title: David S. Johnson, Approximation algorithms for combinatorial problems, Journal of Computer and System Sciences 9(3), 1974
    locator: pages 256 to 278
  - paper: doi:10.1145/285055.285059
    title: Uriel Feige, A threshold of ln n for approximating set cover, Journal of the ACM 45(4), 1998
    locator: pages 634 to 652
  - paper: doi:10.1145/2591796.2591884
    title: Irit Dinur and David Steurer, Analytical approach to parallel repetition, STOC 2014
    locator: the set cover corollary
---

The dominating set problem asks for a smallest set $D$ of vertices of a graph such that each vertex is in $D$ or has a neighbour in $D$. The least size is the domination number $\gamma(G)$. The problem is a case of [set cover](/set-cover/): the elements are the vertices, and each vertex $v$ gives the set $N[v]$ of itself and its neighbours. So the [greedy algorithm](/greedy-set-cover/) gives ratio $H_{\Delta + 1} \le \ln(\Delta + 1) + 1$, where $\Delta$ is the largest degree. A reduction in the other direction shows that this is close to the best possible: dominating set is as hard to approximate as set cover. It is one of the standard NP-complete graph problems (Garey and Johnson, GT2).

## In plain words

A town has crossings joined by streets. You want to put fire stations at some crossings so that each crossing has a station or is one street away from one. You want as few stations as possible.

Each crossing, with its next crossings, is a group that one station can serve. So the task is to pick few groups that together hold all crossings. This is the general covering problem, and the same greedy rule works well: put the next station where it serves the most crossings that no station serves yet. No fast method is known that is much better than this rule in the worst case, and good evidence says that none exists.

## Definition

**Input.** An undirected graph $G = (V, E)$ with $n$ vertices, $m$ edges and largest degree $\Delta$. In the weighted version, each vertex has a cost $c(v) \ge 0$.

**Output.** A set $D \subseteq V$ such that each $u \in V$ has $u \in D$ or a neighbour in $D$, a *dominating set*. With $N[v] = \{v\} \cup \{u : \{u, v\} \in E\}$, the condition is $\bigcup_{v \in D} N[v] = V$.

**Goal.** Minimize $|D|$, or $c(D)$. OPT $= \gamma(G)$, and the ratio convention is ALG $\le \rho \cdot$ OPT.

**Decision version.** Given $G$ and $k$, does $G$ have a dominating set of at most $k$ vertices? This is the *$k$-dominating set* problem.

**Integer program.**

$$\min \sum_{v \in V} c(v) x_v \quad \text{subject to} \quad \sum_{v \in N[u]} x_v \ge 1 \text{ for each } u \in V, \quad x_v \in \{0, 1\}.$$

The LP relaxation has optimum LP* $\le$ OPT, the *fractional domination number*.

**The set cover form.** The universe is $V$ and the sets are $N[v]$ for $v \in V$, each of size $\deg(v) + 1 \le \Delta + 1$. Each vertex $u$ is in $N[v]$ for $v = u$ and for each neighbour $v$, so its [frequency](/element-frequency/) is also $\deg(u) + 1$.

## Variants

- **Weighted dominating set.** Each vertex has a cost. The weighted greedy rule, cost per newly dominated vertex, still gives $H_{\Delta + 1}$.
- **Connected dominating set.** $D$ must also induce a connected subgraph. It is used as a backbone in wireless networks. Guha and Khuller (1998) give ratio $\ln \Delta + O(1)$ by a greedy rule that grows a tree.
- **Independent dominating set.** $D$ must also be independent, so it is a smallest maximal independent set. It is much harder: ratio $n^{1 - \varepsilon}$ is NP-hard (Halldórsson 1993).
- **Total domination.** Each vertex, also in $D$, needs a neighbour in $D$. The sets become the open neighbourhoods $N(v)$, and greedy gives $H_\Delta$.
- **Distance-$r$ and multiple domination.** Each vertex must be within distance $r$ of $D$, or must be dominated $k$ times. These are set cover and set multicover problems again.
- **Parameterized.** $k$-dominating set is W[2]-complete (Downey and Fellows), so no $f(k) \cdot n^{O(1)}$ algorithm is expected; see [parameterized dominating set](/parameterized-dominating-set/).
- **Distributed.** Each vertex knows only its neighbours; see [distributed dominating set](/distributed-dominating-set/).

## Examples

**Greedy is not exact.** The graph has the vertices 0 to 7 and the edges 0-1, 0-2, 0-6, 0-7, 1-4, 1-5, 1-7, 2-6, 3-6 and 3-7. The set $\{1, 6\}$ dominates it, because $N[1] = \{0, 1, 4, 5, 7\}$ and $N[6] = \{0, 2, 3, 6\}$, and no single vertex does, so $\gamma = 2$. Greedy, with ties to the smaller index, takes 0, which dominates $\{0, 1, 2, 6, 7\}$, then 1, which dominates $4$ and $5$, and then 3 for the last vertex. It returns 3 vertices.

**Greedy is exact here.** On the graph with the edges 0-1, 0-2, 1-2, 1-3, 2-3, 3-4, 4-5, 4-6 and 5-6, greedy takes 1, which dominates $\{0, 1, 2, 3\}$, and then 4. So it returns 2 vertices, and $\gamma = 2$, because no vertex has degree 6.

**Standard graphs.**

| graph | $n$ | $\gamma$ |
|---|---|---|
| complete graph $K_n$ or star $K_{1,n-1}$ | $n$ | 1 |
| path $P_n$ or cycle $C_n$ | $n$ | $\lceil n/3 \rceil$ |
| $C_3, C_4, C_5, C_6, C_7, C_8$ | 3 to 8 | 1, 2, 2, 2, 3, 3 |
| Petersen graph | 10 | 3 |
| $K_{k,k}$, $k \ge 2$ | $2k$ | 2 |

The Petersen graph is 3-regular, so each vertex dominates 4 vertices, and $\gamma \ge \lceil 10/4 \rceil = 3$. Label the outer cycle 0 to 4, the spokes $i$ to $i + 5$, and the inner edges $5 + i$ to $5 + ((i + 2) \bmod 5)$. Then $N[0] = \{0, 1, 4, 5\}$, $N[7] = \{2, 5, 7, 9\}$ and $N[8] = \{3, 5, 6, 8\}$, so $\{0, 7, 8\}$ dominates all 10 vertices and $\gamma = 3$.

## Known algorithms

| algorithm | ratio | lower bound used |
|---|---|---|
| [Greedy set cover](/greedy-set-cover/) on the sets $N[v]$ | $H_{\Delta + 1} \le \ln(\Delta + 1) + 1$ | LP*, by dual fitting |
| [Frequency rounding](/frequency-rounding-set-cover/) or [primal-dual](/set-cover-primal-dual/) | $\Delta + 1$ | LP* |
| Trees: dynamic programming | 1, in $O(n)$ time | none |
| Planar graphs: [Baker's technique](/baker-planar-ptas/) | $1 + \varepsilon$ | none |
| Exact, measure and conquer (Fomin, Grandoni and Kratsch 2009) | 1, in $O(c^n)$ time for a constant $c < 2$ | none |

The greedy algorithm runs in $O(n + m)$ time with a bucket queue, because the sets $N[v]$ have total size $n + 2m$. All ratios hold in the worst case.

## Bounds

- **NP-completeness.** The decision version is NP-complete, also for planar graphs of degree at most 3, bipartite graphs and split graphs (Garey and Johnson; Bertossi 1984 for split graphs).
- **Upper bound (proved on the linked page).** The ratio $H_{\Delta + 1}$ is the greedy set cover bound $H_d$ with largest set size $d = \Delta + 1$; the proof is on the [greedy set cover](/greedy-set-cover/) page.
- **Hardness (cited).** The reverse reduction below keeps OPT, so the set cover hardness carries over. Unless P = NP, no polynomial algorithm has ratio $c \ln n$ for some constant $c > 0$, by the set cover hardness of Feige (1998) and of Dinur and Steurer (2014). The sharp form of the threshold is on the [dominating set inapproximability](/dominating-set-inapproximability/) page.
- **Bounded degree (cited).** For each fixed $\Delta \ge 3$ the problem is APX-hard, and for large $\Delta$ the ratio $\ln \Delta - O(\ln \ln \Delta)$ is NP-hard (Chlebík and Chlebíková 2008).
- **Combinatorial bounds.** Each vertex dominates at most $\Delta + 1$ vertices, so $\gamma \ge n/(\Delta + 1)$. If each degree is at least $\delta \ge 1$, then $\gamma \le n \frac{1 + \ln(\delta + 1)}{\delta + 1}$ (Alon and Spencer, Section 1.2, by choosing each vertex with a fixed probability and adding the vertices that remain undominated). A graph with no isolated vertex has $\gamma \le n/2$ (Ore 1962).

## Reductions

- **To set cover.** Universe $V$, sets $N[v]$. A dominating set is a cover and the cost is the same, so each set cover algorithm applies with $d = f = \Delta + 1$.
- **From set cover.** Let a set cover instance have universe $U$ of $n$ elements and sets $S_1, \ldots, S_m$, each element in some set. Build a graph with a vertex $s_j$ for each set and a vertex $u_e$ for each element. Join all the $s_j$ to each other, and join $u_e$ to $s_j$ when $e \in S_j$. A cover $\{S_j : j \in J\}$ gives the dominating set $\{s_j : j \in J\}$: the $s_j$ form a clique, and each $u_e$ has a neighbour $s_j$ with $e \in S_j$. In the other direction, replace each element vertex $u_e$ of a dominating set by some $s_j$ with $e \in S_j$; the result is still dominating and has no more vertices, and its sets cover $U$. So $\gamma = $ OPT of the set cover instance, and the graph has $n + m$ vertices.
- **From vertex cover.** For a graph $H$ with no isolated vertex, add a new vertex $x_{uv}$ joined to $u$ and $v$ for each edge $\{u, v\}$. To dominate $x_{uv}$, a set needs $u$, $v$ or $x_{uv}$, and $x_{uv}$ can be swapped for $u$. So the new graph has $\gamma$ equal to the vertex cover number of $H$. This proves NP-hardness, also for planar graphs.
- **To and from hitting set.** Since $N[v]$ is symmetric, $u \in N[v]$ if and only if $v \in N[u]$, the set cover form and the [hitting set](/hitting-set/) form are the same instance.

## Applications

- **Facility placement.** Place shops, fire stations or servers so that each site is at most one link from one of them.
- **Wireless and ad hoc networks.** A connected dominating set is a virtual backbone: the dominating nodes route messages for their neighbours.
- **Sensor and monitor placement.** In a power grid, a phase measurement unit at a node observes the node and its neighbours.
- **Social networks.** Pick few people so that each person knows one of them, as a simple model for spreading information.

## References
