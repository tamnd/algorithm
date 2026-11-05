---
tag: HKSZQ9
kind: theorem
slug: upper-bound-property
name: Upper-bound property of relaxation
aliases:
- Upper-bound property
area: graphs/shortest-paths
level: core
summary: Shortest-path estimates never fall below true distances under any sequence of relaxations, and stay at the true value once reached.
prereqs: [edge-relaxation, shortest-path, shortest-path-optimal-substructure]
see_also: [edge-relaxation, generic-shortest-path-algorithm, shortest-path-optimality-conditions, shortest-path-tree, bellman-ford, dijkstra, dag-shortest-paths, spfa]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 22, introduction (the list of properties of shortest paths and relaxation, with the upper-bound, no-path, convergence, path-relaxation and predecessor-subgraph properties) and Section 22.5, Proofs of shortest-paths properties
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 5, Section 5.3, Generic label-correcting algorithms (the labels are upper bounds on the distances)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 8, Section 8.3, The only SSSP algorithm (tense edges and relaxation)
---

The upper-bound property says that when the labels of a shortest-path algorithm start at $d(s) = 0$ and $d(v) = \infty$ for $v \ne s$, and are changed only by [edge relaxation](/edge-relaxation/), each label $d(v)$ is at all times at least the true distance $\delta(s, v)$, and once $d(v) = \delta(s, v)$ it never changes again. It holds for any weights and any order of relaxations, even with negative cycles. With the convergence and path-relaxation properties that follow from it, it proves [Bellman-Ford](/bellman-ford/), [Dijkstra](/dijkstra/) and [DAG shortest paths](/dag-shortest-paths/) correct.

## Statement

Let $G = (V, E)$ be a directed graph with weights $w : E \to \mathbb{R}$ and a source $s$. Labels $d : V \to \mathbb{R} \cup \{+\infty\}$ and parents $\pi : V \to V \cup \{\mathrm{nil}\}$ start as

$$d(s) = 0, \qquad d(v) = +\infty \text{ and } \pi(v) = \mathrm{nil} \text{ for } v \ne s.$$

A *relaxation* of an arc $(u, v) \in E$ is the step: if $d(u) + w(u, v) < d(v)$, then set $d(v) \leftarrow d(u) + w(u, v)$ and $\pi(v) \leftarrow u$. Here $\infty + x = \infty$ for real $x$.

**Theorem.** After any finite sequence of relaxations, in any order, with repetitions allowed:

1. for every $v \in V$, $d(v) \ge \delta(s, v)$;
2. for every $v$ with $d(v) < \infty$, $d(v)$ is the weight of some walk from $s$ to $v$;
3. if at some moment $d(v) = \delta(s, v)$, then $d(v)$ keeps this value after every later relaxation.

**Corollary (no-path property).** If $v$ is not reachable from $s$, then $d(v) = \infty$ at all times.

## In plain words

A shortest-path program keeps a best-known cost for each place. At the start it knows only that the start costs nothing. It improves a cost only when it finds a road that gives a cheaper way in, and the new cost is always the cost of a real route that it has just put together.

So a best-known cost can never be cheaper than the true cheapest cost, because it always belongs to an actual route, and no route beats the cheapest one. And once a cost reaches the true cheapest value, nothing can lower it further, and the program only ever lowers costs, so it stays.

## Proof

We prove statements 1 and 2 together by induction on the number $k$ of relaxations performed.

**Base, $k = 0$.** $d(s) = 0$ is the weight of the empty walk $\langle s \rangle$. For 1, $\delta(s, s) \le 0$ because of that walk, so $d(s) = 0 \ge \delta(s, s)$. Every other label is $\infty \ge \delta(s, v)$, and statement 2 does not apply to it.

**Step.** Assume 1 and 2 hold before the relaxation of an arc $(u, v)$. If the test $d(u) + w(u, v) < d(v)$ fails, no label changes, and both statements still hold. If it succeeds, then $d(u) < \infty$, and only $d(v)$ changes, to $d'(v) = d(u) + w(u, v)$.

- *Statement 2.* By the hypothesis, $d(u) = w(p)$ for a walk $p$ from $s$ to $u$. The walk $p$ followed by the arc $(u, v)$ goes from $s$ to $v$ and has weight $w(p) + w(u, v) = d'(v)$.
- *Statement 1.* $d'(v)$ is the weight of a walk from $s$ to $v$, so $d'(v) \ge \delta(s, v)$ by the definition of $\delta(s, v)$ as the infimum of these weights. If $\delta(s, v) = -\infty$, the inequality is trivial.

So both statements hold after each relaxation, and by induction after any finite sequence. $\square$

**Statement 3.** Labels only decrease: a relaxation changes $d(v)$ only to a smaller value. Suppose $d(v) = \delta(s, v)$ at some moment. A later change would make $d(v)$ smaller than $\delta(s, v)$, which contradicts statement 1. So $d(v)$ never changes again. $\square$

**Corollary.** If $v$ is not reachable, no walk from $s$ to $v$ exists, so by statement 2 the label $d(v)$ cannot be finite. $\blacksquare$

**A remark on negative cycles.** Nothing in the proof needs nonnegative weights or the absence of negative cycles. With a reachable negative cycle, statement 1 is trivial for the vertices with $\delta = -\infty$, statement 3 never applies to them, since a real label never equals $-\infty$, and their labels can keep falling forever. Statement 2 is the useful part there: it shows that every label is a real walk weight, so the parent pointers can be followed to find the cycle.

## Consequences

From the upper-bound property and the definition of relaxation, CLRS (Section 22.5) derives:

- **Convergence property.** If $s \leadsto u \to v$ is a shortest path and $d(u) = \delta(s, u)$ at some time before the arc $(u, v)$ is relaxed, then $d(v) = \delta(s, v)$ afterwards and forever. *Proof.* After the relaxation, $d(v) \le d(u) + w(u, v) = \delta(s, u) + w(u, v) = \delta(s, v)$, the last step by [optimal substructure](/shortest-path-optimal-substructure/). Statement 1 gives $\ge$, and statement 3 keeps the value.
- **Path-relaxation property.** If $p = \langle v_0 = s, v_1, \ldots, v_k \rangle$ is a shortest path and the arcs $(v_0, v_1), (v_1, v_2), \ldots, (v_{k-1}, v_k)$ are relaxed in this order, possibly with other relaxations in between, then $d(v_k) = \delta(s, v_k)$ afterwards. This follows from the convergence property by induction on $i$, starting with $d(s) = 0 = \delta(s, s)$, which holds when no negative cycle reaches $s$.
- **Predecessor-subgraph property.** Once $d(v) = \delta(s, v)$ for all $v$, the parent pointers form a [shortest-path tree](/shortest-path-tree/).

These are used by:

- [Bellman-Ford](/bellman-ford/): round $i$ relaxes every arc, so the $i$-th arc of every shortest path is relaxed in round $i$ or later; after $n - 1$ rounds the path-relaxation property gives all distances.
- [DAG shortest paths](/dag-shortest-paths/): the topological order relaxes the arcs of every path in order.
- [Dijkstra](/dijkstra/): its proof finishes a vertex $u$ only when $d(u) = \delta(s, u)$, and statement 3 keeps it.
- [SPFA](/spfa/) and the [generic shortest-path algorithm](/generic-shortest-path-algorithm/): they stop when no arc can be relaxed, and statement 2 together with the [optimality conditions](/shortest-path-optimality-conditions/) shows that the labels are then the distances.

## Tightness

**A worked run.** On the graph of CLRS Figure 22.4, with the arcs $s \to t$ (6), $s \to y$ (7), $t \to x$ (5), $t \to y$ (8), $t \to z$ ($-4$), $x \to t$ ($-2$), $y \to x$ ($-3$), $y \to z$ (9), $z \to s$ (2) and $z \to x$ (7), relax all arcs in this order, pass after pass. The successful relaxations and the labels of $(s, t, x, y, z)$ after each are:

| pass | arc | labels |
|---|---|---|
| 1 | $s \to t$ | $0, 6, \infty, \infty, \infty$ |
| 1 | $s \to y$ | $0, 6, \infty, 7, \infty$ |
| 1 | $t \to x$ | $0, 6, 11, 7, \infty$ |
| 1 | $t \to z$ | $0, 6, 11, 7, 2$ |
| 1 | $y \to x$ | $0, 6, 4, 7, 2$ |
| 2 | $x \to t$ | $0, 2, 4, 7, 2$ |
| 3 | $t \to z$ | $0, 2, 4, 7, -2$ |

The distances are $(0, 2, 4, 7, -2)$. Each label in the table is at least its distance, and each label stops changing as soon as it reaches its distance: $y$ and $x$ in pass 1, $t$ in pass 2 and $z$ in pass 3. Each label is the weight of a walk: 11 is $s \to t \to x$, and the final $-2$ is $s \to y \to x \to t \to z$.

**The start values matter.** If some label starts below its distance, the property fails at once: with $d(z) = -5$ at the start, $d(z) < \delta(s, z) = -2$, and no relaxation raises it. The property is about the standard start values.

**Only relaxation may change labels.** A step that raises a label, as some heuristics do when they remove a vertex from a tree, keeps statement 1 but breaks statement 3. [Tarjan's subtree disassembly](/tarjan-subtree-disassembly/) only marks vertices as inactive and leaves their labels alone, so it keeps all three statements.

## History

Ford (1956) introduced the relaxation step that drives labels down toward the distances, and Bellman (1958) and Moore (1959) used it in rounds. The form of the property used here, together with the no-path, convergence, path-relaxation and predecessor-subgraph properties, is the one of CLRS, which lists them at the start of its chapter on single-source shortest paths and proves them in Section 22.5.

## References
