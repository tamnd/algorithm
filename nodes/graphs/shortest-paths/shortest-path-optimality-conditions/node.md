---
tag: GC7TD6
kind: theorem
slug: shortest-path-optimality-conditions
name: Shortest-path optimality conditions
aliases:
- triangle inequality for shortest paths
- Bellman optimality conditions
area: graphs/shortest-paths
level: core
summary: Labels d with d(s)=0 that are weights of real s-v walks are the true distances iff d(v) <= d(u)+w(u,v) for every edge (u,v).
prereqs: [shortest-path, edge-relaxation, shortest-path-optimal-substructure]
see_also: [upper-bound-property, shortest-path-tree, potential-function-reduced-costs, negative-cycle, bellman-ford, dijkstra, difference-constraints, lp-duality]
sources:
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 5, Section 5.2, Optimality conditions (Theorem 5.1, the shortest path optimality conditions, and the reduced-cost form)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 22, introduction and Section 22.5 (the triangle inequality and the properties of relaxation)
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency
    locator: Chapter 8, Shortest paths, arbitrary lengths (potentials and the theorem that a potential exists if and only if there is no negative cycle)
---

The shortest-path optimality conditions say when a set of labels $d(v)$ is exactly the set of distances $\delta(s, v)$ from a source $s$. If each finite label is the weight of a real walk from $s$, and $d(s) = 0$, then the labels are the distances if and only if every arc $(u, v)$ satisfies the *triangle inequality* $d(v) \le d(u) + w(u, v)$. The conditions give a check of any claimed answer in $O(n + m)$ time, they are the stopping rule of every [label-correcting](/bellman-ford/) algorithm, and they are the dual feasibility conditions of the shortest-path linear program.

## Statement

Let $G = (V, E)$ be a directed graph with weights $w : E \to \mathbb{R}$, let $s \in V$, and let $R$ be the set of vertices reachable from $s$. Let $d : V \to \mathbb{R} \cup \{+\infty\}$ be labels with $d(v) < \infty$ exactly for $v \in R$.

**Theorem A (lower bound).** If $d(s) = 0$ and

$$d(v) \le d(u) + w(u, v) \quad \text{for every arc } (u, v) \in E \text{ with } u \in R, \tag{T}$$

then $d(v) \le \delta(s, v)$ for every $v \in V$, and no [negative cycle](/negative-cycle/) is reachable from $s$.

**Theorem B (optimality).** Suppose $d(s) = 0$ and, for each $v \in R$, $d(v) = w(p_v)$ for some walk $p_v$ from $s$ to $v$. Then $d(v) = \delta(s, v)$ for every $v \in V$ if and only if (T) holds.

**Theorem C (trees).** Suppose no negative cycle is reachable from $s$, and $T$ is a tree rooted at $s$ that spans $R$, with arcs of $E$. Let $d(v)$ be the weight of the tree path from $s$ to $v$ for $v \in R$, and $d(v) = \infty$ otherwise. Then $T$ is a [shortest-path tree](/shortest-path-tree/) if and only if (T) holds.

**Reduced-cost form.** Write $w_d(u, v) = w(u, v) + d(u) - d(v)$ for arcs inside $R$. Then (T) says $w_d \ge 0$ on every such arc, and in Theorem C the arcs of $T$ have $w_d = 0$.

## In plain words

You are given a table that claims to list the cheapest cost from the start to every place, and each cost in the table is the cost of some real route. How do you check the claim without searching again? Look at every road once. If some road leads from a place to another place more cheaply than the table says, the table is wrong there. If no road does that, the table is right.

The reason is that a better route would have to use roads, and summing the "no road helps" checks along that route shows it cannot be better. The check also proves that there is no loop of roads with a negative total cost in reach of the start.

## Proof

*Proof of Theorem A.* Let $v \in R$ and let $p = \langle v_0 = s, v_1, \ldots, v_k = v \rangle$ be any walk from $s$ to $v$. All $v_i$ are in $R$, so (T) applies to each arc of $p$:

$$d(v_k) \le d(v_{k-1}) + w(v_{k-1}, v_k) \le d(v_{k-2}) + w(v_{k-2}, v_{k-1}) + w(v_{k-1}, v_k) \le \cdots \le d(s) + w(p) = w(p).$$

So $d(v)$ is a real number that is at most the weight of every walk from $s$ to $v$, and hence at most their infimum $\delta(s, v)$. If $v \notin R$, both sides are $+\infty$. Now suppose a negative cycle $C$ were reachable from $s$, through a vertex $x \in R$. Going around $C$ $j$ times gives walks to $x$ of weight tending to $-\infty$, so $\delta(s, x) = -\infty$. Then the real number $d(x)$ would be at most $-\infty$, which is impossible. $\square$

*Proof of Theorem B.* ($\Leftarrow$) If (T) holds, Theorem A gives $d(v) \le \delta(s, v)$. For $v \in R$, $d(v) = w(p_v) \ge \delta(s, v)$ by the definition of $\delta$ as an infimum. So $d(v) = \delta(s, v)$ on $R$, and outside $R$ both are $+\infty$.

($\Rightarrow$) If $d = \delta(s, \cdot)$, then all $\delta(s, v)$ with $v \in R$ are real, since $d$ is real there. Take an arc $(u, v)$ with $u \in R$. A shortest path to $u$ followed by $(u, v)$ is a walk to $v$ of weight $\delta(s, u) + w(u, v)$, so $\delta(s, v) \le \delta(s, u) + w(u, v)$, which is (T). $\square$

*Proof of Theorem C.* The tree paths are walks from $s$, and $d(s) = 0$ is the weight of the empty tree path, so the hypothesis of Theorem B holds. By Theorem B, $d = \delta(s, \cdot)$ if and only if (T) holds, and $d = \delta(s, \cdot)$ says exactly that each tree path is a shortest path, which is the definition of a shortest-path tree. For the last remark of the reduced-cost form: for a tree arc $(u, v)$ the tree path to $v$ is the tree path to $u$ followed by $(u, v)$, so $d(v) = d(u) + w(u, v)$ and $w_d(u, v) = 0$. $\blacksquare$

**Why the walk hypothesis is needed.** Without "each $d(v)$ is the weight of a walk", the conditions give only the lower bound of Theorem A. Labels that are all 0 satisfy (T) on every graph with nonnegative weights, yet they are not the distances.

**The linear program.** For $v \in R$ the distances are the optimal solution of the linear program "maximize $d(t)$ subject to $d(s) = 0$ and $d(v) - d(u) \le w(u, v)$ on every arc", for each target $t$ at once. Theorem A is its weak duality, and the tight tree arcs of Theorem C are complementary slackness: the primal flow of one unit from $s$ to $t$ uses only arcs with $w_d = 0$. See [LP duality](/lp-duality/).

## Consequences

- **Certificates.** A claimed answer of an SSSP code (labels, parents) is checked in $O(n + m)$ time: $d(s) = 0$, each parent arc is tight, the parents reach $s$, and (T) holds on every arc. This checker is the oracle of the tests of [Johnson's algorithm](/johnson/), [SPFA](/spfa/) and [0-1 BFS](/zero-one-bfs/).
- **Label-correcting algorithms.** [Bellman-Ford](/bellman-ford/) and [SPFA](/spfa/) relax violated arcs until (T) holds everywhere; at that moment Theorem B says the labels are the distances, because each label is the weight of a walk by the [upper-bound property](/upper-bound-property/).
- **Dijkstra's algorithm.** [Dijkstra](/dijkstra/) never revisits a finished vertex; its proof shows that (T) holds when it stops.
- **Potentials.** A real $d$ with (T) on all arcs, for the graph with an added source joined to every vertex, is a [potential](/potential-function-reduced-costs/). By Theorem A it exists only if there is no negative cycle, and the distances from the added source give one when there is none. [Johnson's algorithm](/johnson/) uses it.
- **Difference constraints.** (T) is the system $d(v) - d(u) \le w(u, v)$, so a system of [difference constraints](/difference-constraints/) is feasible exactly when its graph has no negative cycle.

## Tightness

Each hypothesis is needed.

- **The walk hypothesis.** As above, $d \equiv 0$ on a graph with positive weights satisfies (T) and $d(s) = 0$ but is not $\delta$.
- **(T) on every arc.** In the graph of CLRS Figure 22.4, with the arcs $s \to t$ (6), $s \to y$ (7), $t \to x$ (5), $t \to y$ (8), $t \to z$ ($-4$), $x \to t$ ($-2$), $y \to x$ ($-3$), $y \to z$ (9), $z \to s$ (2) and $z \to x$ (7), the distances $(0, 2, 4, 7, -2)$ for $(s, t, x, y, z)$ give the slacks $w_d$ of 4, 0, 3, 3, 0, 0, 0, 18, 0 and 1 on the arcs in this order, all nonnegative. The labels $(0, 6, 4, 7, 2)$ are also weights of walks ($s \to t$, $s \to y \to x$, $s \to y$, $s \to t \to z$), and they violate (T) only on the arc $x \to t$, where $4 - 2 = 2 < 6$. Ignoring that one arc would accept a wrong answer.
- **$d(s) = 0$.** Take the arcs $s \to t$ and $t \to s$, both of weight 1. The labels $d(s) = 2$ (the walk $s \to t \to s$) and $d(t) = 1$ (the walk $s \to t$) are weights of walks and satisfy (T), since $1 \le 2 + 1$ and $2 \le 1 + 1$. But $\delta(s, s) = 0$. Theorem A needs $d(s) = 0$ for its chain of inequalities to end at $w(p)$.

## History

Bellman (1958) wrote the distances as the solution of the equations $d(v) = \min_u (d(u) + w(u, v))$, and Ford (1956) gave the relaxation method that drives labels toward them. The form with inequalities and reduced costs is standard in network optimization; Ahuja, Magnanti and Orlin state it as Theorem 5.1 in their chapter on label-correcting algorithms, and Schrijver (Chapter 8) presents the equivalence of potentials and the absence of negative cycles.

## References
