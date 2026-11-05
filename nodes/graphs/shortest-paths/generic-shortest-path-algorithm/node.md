---
tag: 758800
kind: algorithm
slug: generic-shortest-path-algorithm
name: Generic shortest path algorithm
area: graphs/shortest-paths
level: core
summary: Repeatedly relaxes tight or improvable edges in a graph until distances are correct, a framework that Dijkstra and Bellman-Ford refine with specific edge orderings.
solves: [single-source-shortest-paths, negative-cycle-detection]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: 2^Ω(n), best: Θ(n + m)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
prereqs: [edge-relaxation, single-source-shortest-paths, upper-bound-property]
see_also: [dijkstra, bellman-ford, dag-shortest-paths, spfa, desopo-pape-algorithm, shortest-path-optimality-conditions, potential-function-reduced-costs, breadth-first-search]
sources:
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 8, Shortest Paths, the section The Only SSSP Algorithm (Ford's generic relaxation algorithm, its correctness, and the remark that bad orders take exponential time)
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 5, Section 5.2, Optimality conditions, and Section 5.3, Generic label-correcting algorithms
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 22, introduction (relaxation as the common step of all the algorithms), and Section 22.5, Proofs of shortest-paths properties
  - paper: doi:10.1145/321765.321768
    title: Donald B. Johnson, A note on Dijkstra's shortest path algorithm, Journal of the ACM 20(3), 385 to 388 (1973)
    locator: the whole note (graphs on which relaxation in a bad order takes exponential time)
---

The generic shortest-path algorithm, due to Ford, starts with the label 0 at the source and $\infty$ elsewhere, and repeatedly picks any *tense* edge, an edge $(u, v)$ with $d[u] + w(u, v) < d[v]$, and [relaxes](/edge-relaxation/) it, until no tense edge is left. Whatever the order, if no [negative cycle](/negative-cycle/) is reachable from the source, it ends with every label equal to the true distance. Every classic single-source method is this algorithm with a rule for which edge to pick: [Dijkstra](/dijkstra/), [Bellman-Ford](/bellman-ford/), [DAG shortest paths](/dag-shortest-paths/) and [breadth-first search](/breadth-first-search/). The rule decides the running time, which ranges from linear to exponential.

## In plain words

Each place holds a guess of its distance from the start: zero at the start, "unknown" everywhere else. A road from one place to another is "tense" if going to the first place and then down the road beats the second place's current guess.

Find any tense road and lower the second place's guess to match. Repeat until no road is tense. At that point every guess is the true distance, no matter which roads you fixed or in what order.

The order still matters for speed. A careless order can make the same place improve its guess a huge number of times. The famous algorithms are smart orders: by nearest place first, in rounds over all roads, or along a fixed line when there are no loops.

## The problem

The input is a directed graph $G = (V, E)$ with $n$ vertices and $m$ edges, a real weight $w(u, v)$ on each edge, and a source $s$. The output is $\delta(s, v)$ for every $v$ and a [shortest-path tree](/shortest-path-tree/), or a report that a negative cycle is reachable from $s$, as in the [single-source shortest-path problem](/single-source-shortest-paths/).

**Weight assumptions.** Weights are any real numbers; negative weights are allowed and need not be integers. If no negative cycle is reachable from $s$, the algorithm ends with the distances, and vertices that $s$ does not reach keep $+\infty$. If a negative cycle is reachable, tense edges never run out, and Ford's method alone runs forever; the version below keeps the number of edges behind each label and reports the cycle when that number reaches $n$. Negative cycles that $s$ cannot reach do not matter.

## The algorithm

```pseudo id=main
GENERIC-SSSP(G, w, s)
L1  for each v do d[v] ← ∞, π[v] ← nil, h[v] ← 0
L2  d[s] ← 0
L3  while some edge (u, v) has d[u] + w(u, v) < d[v] do
L4      choose any such tense edge (u, v)
L5      d[v] ← d[u] + w(u, v); π[v] ← u; h[v] ← h[u] + 1
L6      if h[v] ≥ n then return NEGATIVE-CYCLE
L7  return d, π
```

Line L5 is a successful relaxation. The count $h[v]$ is the number of edges of the walk whose weight is the current $d[v]$; without negative cycles that walk is a simple path, so $h[v] \le n - 1$. Line L4 is left open on purpose. Fixing it gives the familiar algorithms:

| rule for line L4 | algorithm | time |
|---|---|---|
| edges out of the unscanned vertex with the least label, each vertex once | [Dijkstra](/dijkstra/) (needs $w \ge 0$) | $O(m + n \log n)$ |
| all edges in a fixed order, round after round | [Bellman-Ford](/bellman-ford/) | $O(nm)$ |
| edges out of vertices in [topological order](/topological-sort/) (needs a DAG) | [DAG shortest paths](/dag-shortest-paths/) | $O(n + m)$ |
| edges out of vertices in FIFO order of their last change | [SPFA](/spfa/) | $O(nm)$ |
| edges out of the vertex at the front of a deque, with re-entries at the front | [D'Esopo-Pape](/desopo-pape-algorithm/) | exponential worst case |
| unit weights, FIFO | [breadth-first search](/breadth-first-search/) | $O(n + m)$ |

## Example

The vertices are $s, a, b, c, z$ and the edges, in this list order, $s \to b$ (4), $b \to c$ (1), $s \to a$ (1), $a \to c$ (6), $a \to b$ (2), $z \to s$ (1). Labels are listed as $s, a, b, c, z$.

**Order 1: always the first tense edge in the list.**

| relax | labels after |
|---|---|
| $s \to b$ | 0 ∞ 4 ∞ ∞ |
| $b \to c$ | 0 ∞ 4 5 ∞ |
| $s \to a$ | 0 1 4 5 ∞ |
| $a \to b$ | 0 1 3 5 ∞ |
| $b \to c$ | 0 1 3 4 ∞ |

**Order 2: always the last tense edge in the list.** $s \to a$ (a = 1), $a \to b$ (b = 3), $a \to c$ (c = 7), $b \to c$ (c = 4).

Both end with $\delta = (0, 1, 3, 4, \infty)$ and the tree $s \to a \to b \to c$, after 5 and 4 relaxations. In order 1, $c$ got a label from the path $s, b, c$ that was later beaten; in order 2, the edge $a \to c$ was relaxed for nothing. The vertex $z$ has an edge into $s$ but none from it, so its label stays $\infty$.

**An exponential order.** Take a chain $v_0, \ldots, v_k$ where each step $v_i \to v_{i+1}$ is either a direct edge of weight $2^{k-1-i}$ or a detour $v_i \to u_i \to v_{i+1}$ of weight 0. The graph has $2k + 1$ vertices, $3k$ edges and nonnegative weights, and the path weights from $v_0$ to $v_k$ are all integers from 0 to $2^k - 1$. Relax recursively: after the label of $v_i$ drops, take the direct edge and recurse from $v_{i+1}$, then take the detour and recurse again. The label of $v_k$ then takes every value $2^k - 1, 2^k - 2, \ldots, 0$ in turn, $2^k$ relaxations into one vertex. With the rule of Dijkstra, the same graph takes $O(k \log k)$ time.

**A negative cycle.** With the edges $s \to a$ (1), $a \to b$ ($-2$), $b \to a$ (1), the cycle $a \to b \to a$ has weight $-1$, and the edges $a \to b$ and $b \to a$ are tense in turn forever. Each relaxation raises $h$ by one, and when $h$ reaches $n = 3$, line L6 reports the cycle.

## Correctness

**Theorem.** For every rule in line L4, the algorithm ends. It returns NEGATIVE-CYCLE if and only if a negative cycle is reachable from $s$; otherwise it returns $d[v] = \delta(s, v)$ for every $v$, with $d[v] = d[\pi[v]] + w(\pi[v], v)$ for every reachable $v \ne s$.

The proof rests on two facts. **Walks.** Every finite label is the weight of a walk from $s$ with $h[v]$ edges, the walk of the label it was copied from plus one edge. If that walk repeats a vertex $x$, the two visits come from two settings of $d[x]$, the later one strictly smaller, so the closed part between them is negative, and a negative cycle is reachable. Without one, all walks are simple paths, each label is one of finitely many path weights, labels only decrease, and the loop ends; with one, labels fall forever, so the walks get long and line L6 fires, and line L6 never fires without one. **No tense edge.** At the end, $d[v] \le d[u] + w(u, v)$ for every edge with $d[u] < \infty$. Adding these along a shortest path gives $d[v] \le \delta(s, v)$, and the walks give $d[v] \ge \delta(s, v)$. These are the [optimality conditions](/shortest-path-optimality-conditions/): labels that are walk weights and have no tense edge are distances. The full proof is in the proof file below.

## Complexity

The model is the [word RAM](/word-ram/).

- **Number of relaxations.** Without negative cycles, each label is the weight of a simple path, so each vertex is relaxed at most as many times as there are simple paths to it; that bound is exponential, and the example shows it can be reached up to a constant in the exponent even with nonnegative weights.
- **Cost per step.** The pseudocode leaves finding a tense edge open. The implementation scans all edges, $O(m)$ per step; real rules keep a set of vertices whose labels changed and look only at their edges.
- **Best case.** If the rule happens to relax the edges of a shortest-path tree in order, $n - 1$ relaxations suffice, and with a scan to confirm that no tense edge is left the time is $\Theta(n + m)$.
- **Space.** The labels, predecessors and counts take $\Theta(n)$ extra space.

## Properties

- **Order-free correctness.** The answer does not depend on the rule, only the running time does.
- **Monotone labels.** Labels only decrease, and each finite label is the weight of a real walk ([upper-bound property](/upper-bound-property/)).
- **Certificate.** At the end, the labels form a [potential](/potential-function-reduced-costs/) with no tense edge, which proves optimality in $O(m)$ time.
- **Predecessor graph.** Without negative cycles, the predecessor edges always form a tree rooted at $s$; a cycle in them is always negative.
- **Negative weights allowed.** Unlike Dijkstra, the generic method is correct for any real weights without negative cycles.

## Variants and improvements

- **Vertex-based scanning.** Keep a bag of vertices whose labels changed and, for a vertex taken from the bag, relax all its edges. The kind of bag (stack, queue, deque, priority queue) gives the different algorithms. A stack can be exponential, a queue gives $O(nm)$, and a priority queue gives Dijkstra on nonnegative weights.
- **Label-setting and label-correcting.** Rules that scan each vertex once with its final label (Dijkstra, DAG order) are called label-setting; rules that may scan a vertex many times (Bellman-Ford, SPFA, D'Esopo-Pape) are label-correcting.
- **Negative cycle detection.** Instead of counts, check the predecessor graph for a cycle, as in [subtree disassembly](/tarjan-subtree-disassembly/).
- **All pairs.** The same relaxation on pairs gives the generic all-pairs method, of which [Floyd-Warshall](/floyd-warshall/) is an order.

## When to use it

Use it as a framework, not as code: to prove a new rule correct, show it is a run of the generic method and that it ends. In practice, choose a rule with a good bound: [Dijkstra](/dijkstra/) for nonnegative weights, [DAG shortest paths](/dag-shortest-paths/) for acyclic graphs, [Bellman-Ford](/bellman-ford/) or [SPFA](/spfa/) for negative weights. The implementation here, with a user-supplied rule, is useful for testing rules and for teaching.

## Pitfalls

- **Assuming any order is fast.** Correctness does not depend on the order, but the time does, and a natural-looking rule such as a stack of changed vertices can take exponential time.
- **Running forever.** Without a check like line L6, a reachable negative cycle keeps the loop alive.
- **Infinity arithmetic.** An edge out of a vertex with label $\infty$ is never tense. With a large number in place of $\infty$, $\infty + (-5)$ looks smaller than $\infty$ and gives false labels.
- **Stopping early.** One pass with no change on part of the edges does not mean that no tense edge is left; the test in line L3 must cover all edges.

## Implementations

The Python version takes the rule as a function that picks one index from the list of tense edges, scans all edges each step, and returns the number of relaxations along with the labels.

## History

Ford (1956) described the relaxation method in a RAND report on network flows, and Bellman (1958) and Moore (1959) gave the round-by-round order. Johnson (1973) showed that relaxation in a bad order can take exponential time, even with nonnegative weights. Erickson calls the method "the only SSSP algorithm", since every standard algorithm is a choice of order within it.

## References
