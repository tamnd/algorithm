---
tag: ARRKJG
kind: concept
slug: potential-function-reduced-costs
name: Potential function and reduced costs
aliases:
- reduced cost
- reweighting
- vertex potential
area: graphs/shortest-paths
level: core
summary: A vertex function h such that w(u,v)+h(u)-h(v) >= 0 preserves shortest paths while making weights nonnegative.
prereqs: [shortest-path, negative-cycle, shortest-path-optimality-conditions]
see_also: [johnson, shortest-path-optimality-conditions, negative-cycle-detection, a-star-search, alt-algorithm, difference-constraints, min-cost-flow-problem, lp-duality]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 23.3, Johnson's algorithm for sparse graphs (the lemma that reweighting preserves shortest paths and cycle weights, and the construction of h from an added source)
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 2, Section 2.4, Network transformations (node potentials and reduced costs), and Chapter 5, Section 5.2, Optimality conditions (the reduced-cost form)
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency
    locator: Chapter 8, Shortest paths, arbitrary lengths (potentials, and the theorem that a potential exists if and only if no cycle has negative length)
  - paper: doi:10.1145/321992.321993
    title: Donald B. Johnson, Efficient algorithms for shortest paths in sparse networks, Journal of the ACM 24(1), 1 to 13 (1977)
    locator: the reweighting step of the all-pairs algorithm
---

A potential is a function $h$ from the vertices of a weighted directed graph to the real numbers, and the *reduced cost* of an arc under $h$ is $w_h(u, v) = w(u, v) + h(u) - h(v)$. Reduced costs change the weight of every walk from $a$ to $b$ by the same amount $h(a) - h(b)$, so they keep the same [shortest paths](/shortest-path/) and the same cycle weights. A potential is *feasible* when all reduced costs are nonnegative, and one exists exactly when the graph has no [negative cycle](/negative-cycle/). This lets an algorithm for nonnegative weights, such as [Dijkstra's](/dijkstra/), work on a graph with negative arcs, which is the idea of [Johnson's algorithm](/johnson/), of [A* search](/a-star-search/) and of successive shortest paths in [min-cost flow](/min-cost-flow-problem/).

## In plain words

Give every place a height. When you walk along a road, add to its cost the height where you start and subtract the height where you end. Over a whole trip, the heights of the places in the middle cancel out: you add each one once and subtract it once. What is left is the height of the start minus the height of the end. That change is the same for every trip between the same two places, so the cheapest trip stays the cheapest.

If you choose the heights well, every road gets a cost of zero or more, even roads that had a negative cost before. Then the fast methods that need nonnegative costs work. Good heights exist exactly when no loop of roads has a negative total.

## The idea

Let $G = (V, E)$ be a directed graph with weights $w : E \to \mathbb{R}$, and let $h : V \to \mathbb{R}$.

**Definition.** The *reduced cost* of $(u, v) \in E$ is $w_h(u, v) = w(u, v) + h(u) - h(v)$. The potential $h$ is *feasible* for $(G, w)$ when $w_h(u, v) \ge 0$ for every arc.

**Lemma 1 (walks).** For every walk $p = \langle v_0, \ldots, v_k \rangle$, $w_h(p) = w(p) + h(v_0) - h(v_k)$.

*Proof.* $w_h(p) = \sum_{i=1}^{k} \big(w(v_{i-1}, v_i) + h(v_{i-1}) - h(v_i)\big) = w(p) + \sum_{i=1}^{k} \big(h(v_{i-1}) - h(v_i)\big)$, and the last sum telescopes to $h(v_0) - h(v_k)$. $\square$

**Consequences of Lemma 1.**

- *Shortest paths are kept.* For fixed ends $a, b$, every walk from $a$ to $b$ changes by the same constant $h(a) - h(b)$. So a walk is a shortest path under $w$ if and only if it is one under $w_h$, and $\delta_h(a, b) = \delta(a, b) + h(a) - h(b)$, with $\pm\infty$ kept.
- *Cycle weights are kept.* For a cycle, $v_0 = v_k$, so $w_h(C) = w(C)$. In particular $w_h$ has a negative cycle if and only if $w$ has one.

**Lemma 2 (existence).** A feasible potential exists if and only if $G$ has no negative cycle.

*Proof.* If $h$ is feasible, each cycle has $w(C) = w_h(C) \ge 0$, as a sum of nonnegative reduced costs. Conversely, suppose there is no negative cycle. Add a new vertex $q$ and an arc $q \to v$ of weight 0 for each $v \in V$. The new graph has no negative cycle either, because no cycle passes through $q$, which has no incoming arc. Every vertex is reachable from $q$, so $h(v) = \delta(q, v)$ is a real number, at most 0. The [optimality conditions](/shortest-path-optimality-conditions/) (the triangle inequality for $\delta$) give $h(v) \le h(u) + w(u, v)$ for each arc $(u, v)$ of $G$, which is $w_h(u, v) \ge 0$. $\square$

**Distances are potentials.** If every vertex is reachable from $s$ and there is no negative cycle, then $h = \delta(s, \cdot)$ is feasible by the same triangle inequality, and the arcs of every [shortest-path tree](/shortest-path-tree/) from $s$ have reduced cost exactly 0. So "the labels are the distances" and "the labels are a feasible potential that is tight on a tree" say the same thing.

**Potentials and duality.** The dual of the shortest-path linear program asks for labels $\pi$ with $\pi(v) - \pi(u) \le w(u, v)$ on every arc. This is the same as $w(u, v) + \pi(u) - \pi(v) \ge 0$, so the dual-feasible labels are exactly the feasible potentials. A reduced cost is the slack of one dual constraint, and complementary slackness says that a shortest path uses only arcs of slack 0. In network flow texts, the potential or its negative is often called the vertex *price*. See [LP duality](/lp-duality/).

## Examples

**Johnson's reweighting.** Take the graph of CLRS Figure 22.4, with the arcs $s \to t$ (6), $s \to y$ (7), $t \to x$ (5), $t \to y$ (8), $t \to z$ ($-4$), $x \to t$ ($-2$), $y \to x$ ($-3$), $y \to z$ (9), $z \to s$ (2) and $z \to x$ (7). With the added vertex $q$, the distances $h = \delta(q, \cdot)$ are $(-7, -5, -3, 0, -9)$ for $(s, t, x, y, z)$. The reduced costs are:

| arc | $w$ | $h(u) - h(v)$ | $w_h$ |
|---|---|---|---|
| $s \to t$ | 6 | $-2$ | 4 |
| $s \to y$ | 7 | $-7$ | 0 |
| $t \to x$ | 5 | $-2$ | 3 |
| $t \to y$ | 8 | $-5$ | 3 |
| $t \to z$ | $-4$ | 4 | 0 |
| $x \to t$ | $-2$ | 2 | 0 |
| $y \to x$ | $-3$ | 3 | 0 |
| $y \to z$ | 9 | 9 | 18 |
| $z \to s$ | 2 | $-2$ | 0 |
| $z \to x$ | 7 | $-6$ | 1 |

All reduced costs are nonnegative. Dijkstra from $s$ on $w_h$ gives $\delta_h(s, v) = 0$ for all five vertices. Undoing the shift, $\delta(s, v) = \delta_h(s, v) - h(s) + h(v)$, gives $(0, 2, 4, 7, -2)$, the true distances. For example $\delta(s, z) = 0 + 7 - 9 = -2$.

**The zero potential.** $h \equiv 0$ gives $w_h = w$. It is feasible exactly when all weights are nonnegative.

**A potential that is not feasible.** On the same graph, $h \equiv 0$ fails on the three negative arcs. A potential can also fail on a positive arc: with $h(s) = 0$ and $h(t) = 10$, the arc $s \to t$ gets $6 + 0 - 10 = -4$.

**No feasible potential.** Set $x \to t$ to $-6$. The cycle $t \to x \to t$ has weight $-1$. For any $h$, $w_h(t, x) + w_h(x, t) = -1$, so one of the two is negative.

**A heuristic as a potential.** In [A* search](/a-star-search/) toward a target $t$ with a heuristic $\eta(v)$ that estimates $\delta(v, t)$, A* is Dijkstra on the reduced costs with $h = -\eta$: $w(u, v) - \eta(u) + \eta(v)$. These are nonnegative exactly when $\eta(u) \le w(u, v) + \eta(v)$, which is the definition of a *consistent* heuristic. The [ALT algorithm](/alt-algorithm/) builds $\eta$ from distances to landmarks and the triangle inequality.

## Where it is used

- [Johnson's algorithm](/johnson/): one Bellman-Ford run from an added source gives $h$, then $n$ Dijkstra runs on $w_h$.
- [Negative cycle detection](/negative-cycle-detection/): a feasible potential is the certificate that no negative cycle exists.
- [Difference constraints](/difference-constraints/): a feasible potential for the constraint graph is a solution of the system $x_v - x_u \le w(u, v)$.
- [Min-cost flow](/min-cost-flow-problem/): successive shortest paths keep a feasible potential for the residual graph, so each augmentation needs only Dijkstra. [Cost scaling](/cost-scaling/) works with approximately feasible potentials.
- [A* search](/a-star-search/) and the [ALT algorithm](/alt-algorithm/): goal-directed search is Dijkstra on reduced costs.
- Scaling and near-linear algorithms for negative weights ([Goldberg](/goldberg-scaling-sssp/), [near-linear negative SSSP](/near-linear-negative-sssp/)) build $h$ step by step, making more and more reduced costs nonnegative.

## References
