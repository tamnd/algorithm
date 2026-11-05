---
tag: R2NH2H
kind: problem
slug: vertex-connectivity
name: Vertex connectivity
aliases:
- k-vertex-connectivity
- Node connectivity
area: graphs/connectivity
level: advanced
summary: Compute the minimum number of vertices whose removal disconnects the graph.
prereqs: [vertex-cut, menger-theorem, k-vertex-connected-graph, max-flow-problem]
see_also: [even-tarjan-vertex-connectivity, edge-connectivity, nagamochi-ibaraki-certificate, vertex-disjoint-paths, hopcroft-tarjan-biconnectivity, articulation-point, dinic, global-min-cut-problem]
sources:
  - paper: doi:10.1137/0204043
    title: Shimon Even and Robert Endre Tarjan, Network flow and testing graph connectivity, SIAM Journal on Computing 4(4), 507 to 518 (1975)
    locator: the abstract and the section on vertex connectivity (Dinic's algorithm in O(n^{1/2} m) time on unit vertex capacities; vertex connectivity in O(n^{1/2} m^2) time)
  - paper: doi:10.1137/0204034
    title: Shimon Even, An algorithm for determining whether the connectivity of a graph is at least k, SIAM Journal on Computing 4(3), 393 to 396 (1975)
    locator: the whole paper (the test that runs flows only from the first few vertices; O(k n^3) steps when k is below the square root of n; the directed variation)
  - paper: doi:10.1006/jagm.1999.1055
    title: Monika R. Henzinger, Satish Rao and Harold N. Gabow, Computing vertex connectivity, new bounds from old techniques, Journal of Algorithms 34(2), 222 to 250 (2000)
    locator: the main theorems (vertex connectivity in about O(mn) time)
  - paper: doi:10.1145/3743670
    title: Jason Li, Danupon Nanongkai, Debmalya Panigrahi, Thatchaphol Saranurak and Sorrachai Yingchareonthawornchai, Vertex connectivity in poly-logarithmic max-flows, Journal of the ACM 72(4) (2025)
    locator: the abstract (a randomized reduction to poly-logarithmically many max-flow calls; the question of Aho, Hopcroft and Ullman)
  - paper: doi:10.1137/0202012
    title: John E. Hopcroft and Robert E. Tarjan, Dividing a graph into triconnected components, SIAM Journal on Computing 2(3), 135 to 158 (1973)
    locator: the whole paper (deciding 3-connectivity in linear time)
  - paper: doi:10.1073/pnas.48.7.1142
    title: Frank Harary, The maximum connectivity of a graph, Proceedings of the National Academy of Sciences 48(7), 1142 to 1146 (1962)
    locator: the main theorem (the largest connectivity of a graph with n vertices and m edges is the floor of 2m/n)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 4.1, Cuts and connectivity (connectivity, Whitney's inequality, Harary graphs), and Section 4.2, k-connected graphs (Menger's theorem)
---

The vertex connectivity $\kappa(G)$ of a graph is the least number of vertices whose removal leaves it disconnected or with a single vertex. It measures how well a network survives node failures: $\kappa(G) \ge k$ means that any $k - 1$ nodes may fail and the rest still talk. By [Menger's theorem](/menger-theorem/) it equals the least, over pairs of non-adjacent vertices, of the number of internally disjoint paths between them, so it reduces to [maximum flow](/max-flow-problem/). The classic method needs about $\kappa n$ flow computations; recent work brings it down to a poly-logarithmic number.

## In plain words

Picture a computer network. You want to know how many machines an attacker must knock out to split it into parts that can no longer reach each other. That number is the vertex connectivity.

To test a single pair of machines, count how many routes join them with no machine in common. An attacker must hit every one of those routes, and there is always a way to do it with exactly that many hits. So the answer for the whole network is the smallest such count over all pairs that are not directly wired together.

Trying every pair is slow. A smarter search notes that the attacker's chosen machines are few, so one of the first few machines you look at is spared, and only pairs that start at those few need checking.

## Definition

**Input.** An undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges. [Parallel edges](/multigraph/) and [self-loops](/self-loop/) are allowed but change nothing: removing vertices removes all their edges, and whether $G - S$ is connected does not depend on how many copies of an edge there are or on loops. One may drop them first.

**Separating set.** A set $S \subseteq V$ is a [vertex cut](/vertex-cut/) if $G - S$ is disconnected.

**Output.** The number
$$\kappa(G) = \min\{\, |S| : S \subseteq V,\ G - S \text{ is disconnected or has at most one vertex} \,\}.$$
The second clause handles complete graphs, which have no vertex cut: $\kappa(K_n) = n - 1$. A disconnected graph has $\kappa = 0$, and by convention $\kappa(K_1) = 0$. The search version also asks for a minimum vertex cut.

**Decision version.** Given $k$, decide whether $\kappa(G) \ge k$, that is, whether $G$ is [k-vertex-connected](/k-vertex-connected-graph/).

**Local version.** For non-adjacent $s \ne t$, $\kappa(s, t)$ is the least size of a set $S \subseteq V \setminus \{s, t\}$ with no $s$-$t$ path in $G - S$. By Menger's theorem $\kappa(s, t)$ is also the largest number of internally vertex-disjoint $s$-$t$ paths.

**Fact.** If $G$ is not complete, then $\kappa(G) = \min \kappa(s, t)$ over non-adjacent pairs $s \ne t$.

*Proof.* A minimum vertex cut $S$ leaves at least two components; pick $s$ and $t$ in different ones. They are non-adjacent, and $S$ separates them, so $\kappa(s, t) \le |S| = \kappa(G)$. Conversely, any set separating a non-adjacent pair is a vertex cut, so $\kappa(G) \le \kappa(s, t)$ for every such pair. $\square$

## Variants

- **Directed graphs.** For a [directed graph](/directed-graph/), $\kappa(G)$ is the least $|S|$ such that $G - S$ is not [strongly connected](/strongly-connected-graph/) or has one vertex. Here $\kappa(s, t)$ and $\kappa(t, s)$ may differ (see the tightness section of [Menger's theorem](/menger-theorem/)), so both directions must be checked. An undirected graph has the same $\kappa$ as the directed graph with both arcs of every edge.
- **Decision for small $k$.** $\kappa \ge 1$ is [connectivity](/connected-components/), $\kappa \ge 2$ is [biconnectivity](/hopcroft-tarjan-biconnectivity/), and $\kappa \ge 3$ is decided in linear time by Hopcroft and Tarjan's triconnected components. For fixed $k \ge 4$ the flow-based methods below are used.
- **Edge version.** Removing edges instead of vertices gives the [edge connectivity](/edge-connectivity/) $\lambda(G)$, a different problem with faster algorithms.
- **Weighted version.** Vertices carry costs and the cut of least total cost is wanted. The flow reduction below handles it with vertex capacities equal to the costs.

## Examples

Take two copies of $K_4$, on $\{0, 1, 2, 3\}$ and on $\{4, 5, 6, 7\}$, and add the edges $\{0, 4\}$, $\{1, 5\}$ and $\{0, 6\}$. The degrees are $5, 4, 3, 3, 4, 4, 4, 3$.

- **$\kappa = 2$.** Removing $\{0, 1\}$ leaves the two halves with no edge between them. No single vertex works: without $0$ the edge $\{1, 5\}$ joins the halves, and without $1$ the edge $\{0, 4\}$ does, and removing any other vertex leaves both edges.
- **$\lambda = 3$ and $\delta = 3$.** The three crossing edges form a minimum edge cut, and vertex $2$ has degree $3$. So $\kappa < \lambda = \delta$ here, matching Whitney's inequality $\kappa \le \lambda \le \delta$.
- **The local values differ.** $\kappa(0, 5) = 3$, through $0 \to 4 \to 5$, $0 \to 6 \to 5$ and $0 \to 1 \to 5$. But $\kappa(2, 4) = 2$, cut by $\{0, 1\}$. A method that tried only the pair $(0, 5)$ would report $3$.

The pair search (Known algorithms) on this graph runs from vertex $0$ and finds $\kappa(0, 5) = \kappa(0, 7) = 3$; from vertex $1$ it finds $2$; it then runs from vertex $2$, finds nothing smaller, and stops because the next start index $3$ exceeds the current best $2$. It used 9 flow computations instead of one for each of the 13 non-adjacent pairs.

Edge cases:

- $K_n$ has $\kappa = n - 1$ and no non-adjacent pair, so the minimum over pairs is empty and the convention applies.
- A tree with $n \ge 3$ vertices has $\kappa = 1$: any inner vertex is an [articulation point](/articulation-point/).
- The cycle $C_n$, $n \ge 4$, has $\kappa = 2$.
- Adding a parallel copy of an edge or a self-loop leaves $\kappa$ unchanged.

## Known algorithms

| Method | Idea | Time |
|---|---|---|
| All pairs | one flow per non-adjacent pair | $O(n^2)$ flows |
| Pair search, after Even (1975) | flows only from the first $\kappa + 1$ vertices | $O(\kappa n)$ flows |
| Even and Tarjan (1975) | the pair search with unit-capacity Dinic | $O(n^{1/2} m^2)$ |
| Henzinger, Rao and Gabow (2000) | reusing flow work across many sinks | $\tilde O(mn)$ |
| Li et al. (2021, 2025) | randomized reduction to few max-flow calls | poly-logarithmic many max-flows |

**One pair by flow.** To compute $\kappa(s, t)$, split each vertex $v \notin \{s, t\}$ into $v^{-}$ and $v^{+}$ joined by an arc of capacity $1$. Each edge $\{u, v\}$ becomes arcs $u^{+} \to v^{-}$ and $v^{+} \to u^{-}$ of large capacity. A maximum $s^{+}$-$t^{-}$ flow has value $\kappa(s, t)$, and a minimum cut uses only split arcs and names a minimum separating set. Every vertex of this network other than the ends has in-degree or out-degree $1$, and Even and Tarjan showed that [Dinic's algorithm](/dinic/) then takes $O(n^{1/2} m)$ time, so one pair costs $O(n^{1/2} m)$. The page on [vertex-disjoint paths](/vertex-disjoint-paths/) covers this reduction.

**The pair search.** This is a simple form of the idea in Even's 1975 paper. Number the vertices $v_1, \dots, v_n$. Keep a bound $b$, at first $n - 1$. For $i = 1, 2, \dots$ while $i \le b + 1$, compute $\kappa(v_i, w)$ for every $w$ not adjacent to $v_i$ and lower $b$ to the least value found. Return $b$.

*Why it is correct.* Every value found is the size of a vertex cut, so $b \ge \kappa$ throughout. Let $S$ be a minimum vertex cut. The loop reaches every $i \le \kappa + 1 \le b + 1$, and $S$, of size $\kappa$, misses one of $v_1, \dots, v_{\kappa+1}$, say $v_i$. Some vertex $w$ lies in a component of $G - S$ other than that of $v_i$, so $w$ is not adjacent to $v_i$ and $\kappa(v_i, w) \le \kappa$. That value lowers $b$ to $\kappa$. $\square$

Once $b = \kappa$ the loop stops after start index $\kappa + 1$, so the search runs at most $(\kappa + 1)\, n$ flows. Even's paper bounds its own version by $O(k n^3)$ steps when $k < \sqrt{n}$. For directed graphs, check both $\kappa(v_i, w)$ and $\kappa(w, v_i)$. The algorithm page [Even-Tarjan vertex connectivity](/even-tarjan-vertex-connectivity/) treats the method in detail.

**Sparsifying first.** To decide $\kappa \ge k$, one may first replace $G$ by a [Nagamochi-Ibaraki certificate](/nagamochi-ibaraki-certificate/), a subgraph with at most $k n$ edges that is $k$-vertex-connected exactly when $G$ is. Every flow then runs on $O(kn)$ edges.

## Bounds

- **Whitney's inequality.** $\kappa(G) \le \lambda(G) \le \delta(G)$, where $\delta$ is the least degree. The proof is on the [vertex cut](/vertex-cut/) page. Both gaps can be large: two copies of $K_{k}$ joined at a single shared vertex have $\kappa = 1$ and $\lambda = \delta = k - 1$.
- **Edge count.** Since $\delta \le 2m/n$, $\kappa \le \lfloor 2m/n \rfloor$. Harary showed that this is tight for every $m \ge n - 1$: the Harary graphs reach it.
- **Lower bound for any algorithm.** The input has size $n + m$ and every edge can matter, so $\Omega(n + m)$ time is needed. Aho, Hopcroft and Ullman asked in 1974 whether linear time suffices; as of the 2025 paper of Li et al. the best answers are almost linear and randomized.
- **Small $k$.** For $k \le 3$ the decision $\kappa \ge k$ takes $\Theta(n + m)$ time.

## Reductions

- **To maximum flow.** The local value $\kappa(s, t)$ is a maximum flow in the split network above, by Menger's theorem and the [max-flow min-cut theorem](/max-flow-min-cut-theorem/). The global value is a minimum over $O(\kappa n)$ such flows.
- **From connectivity and biconnectivity.** Deciding $\kappa \ge 1$ or $\kappa \ge 2$ is a special case, solved by one [depth-first search](/depth-first-search/).
- **From the undirected to the directed case.** Replace each edge by two opposite arcs; vertex cuts and $\kappa$ are unchanged.
- **Not to global min cut.** The edge-based [global min cut](/global-min-cut-problem/) problem does not solve vertex connectivity directly: in the example above $\lambda = 3$ but $\kappa = 2$.

## Applications

- **Network reliability.** A communication network with $\kappa \ge k$ survives the failure of any $k - 1$ routers. Designers check $\kappa$ and add links where it is low.
- **Fault-tolerant routing.** By Menger's theorem a $k$-connected network has $k$ internally disjoint routes between any two nodes, which can carry copies of a message so that it arrives even if $k - 1$ routes fail.
- **Graph theory.** Many theorems assume a connectivity: for example, a $3$-connected planar graph has an essentially unique embedding. Algorithms that rely on such theorems first check $\kappa$.
- **Structure.** The triconnected components of Hopcroft and Tarjan, built to decide $\kappa \ge 3$, split a biconnected graph into $3$-connected pieces, cycles and bonds, a decomposition used in planarity and embedding algorithms.

## References
