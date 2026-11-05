---
tag: PSDN67
kind: technique
slug: longest-to-shortest-paths-reduction
name: Reduction of longest paths to shortest paths
aliases:
- weight negation
area: graphs/shortest-paths
level: core
summary: Technique that negates edge weights so a longest path problem becomes a shortest path problem on the same graph.
prereqs: [shortest-path, negative-cycle, dag-shortest-paths, bellman-ford]
see_also: [dag-longest-path, longest-path-problem, critical-path, pert-chart, dag-shortest-paths, bellman-ford, currency-arbitrage, difference-constraints]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 22.2, Single-source shortest paths in directed acyclic graphs (PERT charts and critical paths by negated weights or by max in place of min), and Section 14.3 on the lack of optimal substructure for longest simple paths
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 8, Shortest Paths (the remarks on longest paths, negative cycles and NP-hardness) and Chapter 6, Depth-First Search (dynamic programming in DAGs)
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 4, Shortest paths, label-setting algorithms (the section on acyclic networks and its project scheduling application)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability
    locator: Appendix A3.1, problem ND29 LONGEST PATH
---

The longest-to-shortest reduction replaces each weight $w(u, v)$ by $-w(u, v)$, so that a walk of largest weight under $w$ is a walk of least weight under $-w$. It is correct exactly when the new weights have no [negative cycle](/negative-cycle/) on the routes in question, that is, when the old weights have no positive cycle there. This always holds in a directed acyclic graph, so [longest paths in a DAG](/dag-longest-path/) take $O(n + m)$ time by [DAG shortest paths](/dag-shortest-paths/). In a general graph the reduction turns positive cycles into negative ones, and the [longest simple path problem](/longest-path-problem/) is NP-hard; negation does not change that.

## In plain words

Suppose you want the most valuable route, not the cheapest. Write every road value with the opposite sign. Now the most valuable route is the one with the smallest total, and any method for the cheapest route finds it.

There is one catch. A loop of roads with a positive total would let you gain value forever by going around it, so no best route exists. After the sign change, that loop has a negative total, and a good cheapest-route method reports it. If there are no loops at all, as in a plan where each task comes after the tasks it needs, the catch never happens.

## When it applies

- **The objective is a sum of arc weights to be made largest** over walks from $s$ to $t$, or from $s$ to every vertex. Weights may have any sign.
- **No cycle of positive weight lies on a walk from $s$ to a target.** Then the longest walk exists and can be taken to be a simple path, and the reduction is exact. In a DAG this is automatic.
- **The shortest-path algorithm used accepts negative weights.** After negation, positive weights become negative, so [Dijkstra's algorithm](/dijkstra/) is not allowed; use [DAG shortest paths](/dag-shortest-paths/) or [Bellman-Ford](/bellman-ford/).
- **Products and other monotone objectives.** A largest product of positive factors becomes a smallest sum by $-\log$; this is the form used for [currency arbitrage](/currency-arbitrage/) and most likely paths.

It does not apply to longest *simple* paths in a graph with a positive cycle: the shortest-path algorithm then reports a negative cycle, and the simple-path question is NP-hard.

## The template

The holes are the source $s$ and the shortest-path algorithm called in line L2.

```pseudo id=main
LONGEST-VIA-SHORTEST(G, w, s)
L1  for each arc (u, v) in E do w′(u, v) ← −w(u, v)
L2  run a shortest-path algorithm on (G, w′, s) that allows negative weights   ▷ DAG-SHORTEST-PATHS if G is acyclic, else BELLMAN-FORD
L3  if it reports a negative cycle reachable from s then
L4      return "a positive cycle is reachable from s: longest walks are unbounded"
L5  for each v in V do L(v) ← −δ′(s, v)       ▷ +∞ becomes −∞ for unreachable v
L6  return L and the shortest-path tree of w′
```

**Why it is correct.** For every walk $p$, $w'(p) = -w(p)$, so $\max_p w(p) = -\min_p w'(p)$ over any set of walks. The cycles of positive weight under $w$ are exactly the cycles of negative weight under $w'$. If none is reachable from $s$, every $\delta'(s, v)$ is finite or $+\infty$, and a shortest walk under $w'$ can be taken to be a simple path; its negation is a longest walk under $w$, and also a longest simple path. If one is reachable from $s$, going around it gives walks under $w$ of unbounded weight to every vertex reachable from it, which line L4 reports. Unreachable vertices have no walk at all, and the convention $\max \emptyset = -\infty$ matches $-(+\infty)$.

**Cost.** Line L1 takes $O(m)$, and line L2 is the cost of the algorithm used: $O(n + m)$ for a DAG and $O(nm)$ for Bellman-Ford. The reduction adds nothing else.

**Weight assumptions.** Any real weights. The answer is a real number for every reachable $v$ exactly when no positive cycle lies on a walk from $s$ to $v$; this is the "no negative cycle" assumption of the shortest-path algorithm after negation.

## Classic examples

**Longest paths in a DAG.** Take the DAG with the arcs $s \to a$ (3), $s \to b$ (2), $a \to c$ (4), $b \to c$ (6), $a \to t$ (2) and $c \to t$ (1). After negation, DAG shortest paths in the topological order $s, a, b, c, t$ give $\delta'(s, \cdot) = (0, -3, -2, -8, -9)$ for $(s, a, b, c, t)$. So the longest values are $(0, 3, 2, 8, 9)$, and the longest path to $t$ is $s \to b \to c \to t$ with weight 9; the other two routes, $s \to a \to c \to t$ (8) and $s \to a \to t$ (5), are shorter. The same run with $\max$ in place of $\min$ in the relaxation gives the same values without negation.

**Critical path of a project.** In a [PERT chart](/pert-chart/), the vertices are events and an arc is a task of a given duration. The least time to finish the project is the longest path from the start event to the end event, and the tasks on it are the [critical path](/critical-path/). The graph is acyclic, because a task cannot depend on itself through other tasks, so the reduction is exact.

**A positive cycle.** Add the arc $t \to a$ of weight 1 to the DAG above. The cycle $a \to c \to t \to a$ has weight $4 + 1 + 1 = 6 > 0$, so it is a negative cycle of weight $-6$ under $w'$. Bellman-Ford on $w'$ reports it in line L3, and indeed the walks $s \to a \to c \to t \to a \to \cdots \to t$ have no largest weight. The longest *simple* path from $s$ to $t$ is still 9, but finding it in general graphs is NP-hard.

**Difference constraints with lower bounds.** A system of constraints $x_v \ge x_u + w(u, v)$ is the same as $x_u - x_v \le -w(u, v)$, the [difference constraints](/difference-constraints/) form with arcs $v \to u$ of weight $-w(u, v)$. The least solution with $x_s = 0$ is the longest path from $s$; it exists exactly when there is no positive cycle.

**Largest product.** For exchange rates $r(u, v) > 0$, the best product of rates along a route becomes the shortest path under $-\ln r(u, v)$. A product greater than 1 around a cycle, an arbitrage, is a negative cycle.

## Variations

- **Max in place of min.** Instead of negating the weights, change the relaxation test to $d(u) + w(u, v) > d(v)$ and start the labels at $-\infty$. This is the same algorithm and avoids confusion about signs. CLRS describes both forms for PERT charts.
- **Longest paths to every vertex from all sources.** In a DAG, add a source with arcs of weight 0 to every vertex, or start every label at 0.
- **Positive-cycle detection.** Bellman-Ford on $-w$ is a test for positive cycles, used for arbitrage and for checking that a scheduling system is feasible.
- **Fixed number of arcs.** For walks with exactly $k$ arcs, longest walks always exist, and the max-plus product computes them; see [shortest paths of fixed length](/shortest-paths-fixed-length/).
- **Simple paths, small graphs.** For longest simple paths in general graphs, use dynamic programming over subsets in $O(2^n n^2)$ time, or [color coding](/color-coding/) when the path length is small; see [parameterized longest path](/parameterized-longest-path/).

## Pitfalls

- **Using Dijkstra after negation.** All weights become nonpositive, and Dijkstra's greedy choice fails. On $s \to a$ (1), $s \to b$ (2) with $a \to b$ (5) negated, Dijkstra finishes $b$ at $-2$ before it finds $s \to a \to b$ at $-6$.
- **Adding a constant instead of negating.** Replacing $w$ by $C - w$ to keep the weights nonnegative does not give longest paths: a path with $k$ arcs changes by $kC$, so paths with different numbers of arcs are compared unfairly. In the DAG above, with $C = 6$, the route $s \to a \to t$ gets $3 + 4 = 7$, against 10 for $s \to a \to c \to t$ and 9 for $s \to b \to c \to t$. So the shortest route under $C - w$ is $s \to a \to t$, of weight 5 under $w$, which is the lightest route, not the heaviest.
- **Applying it to general graphs for simple paths.** If a positive cycle exists, the shortest-path algorithm reports a negative cycle; it does not return the longest simple path. Do not read the labels at that point as answers.
- **Forgetting the sign at the end.** Line L5 must negate the labels back, and $+\infty$ must become $-\infty$.
- **Positive cycles that do not matter.** A positive cycle that $s$ cannot reach, or that cannot reach the target, does not make that answer unbounded. Bellman-Ford from $s$ ignores the first kind but reports the second kind; check whether the target can be reached from the cycle before giving up.

## Exercises

1. Run the template on the DAG of the first example, with the arc $b \to c$ changed to weight 3, and give the new longest path to $t$.
2. Show that in a DAG the longest path problem with arbitrary real weights is solved by DAG shortest paths on $-w$, and explain why the absence of cycles is the only property used.
3. Give a graph with a positive cycle that $s$ can reach but $t$ cannot be reached from, and show that the longest walk from $s$ to $t$ is still finite.
4. Prove that the longest simple path problem is NP-hard by a reduction from the Hamiltonian path problem, and explain why negating weights does not give a polynomial algorithm.
5. Write the critical path computation for a project with five tasks and give the earliest start time of each task.

## References
