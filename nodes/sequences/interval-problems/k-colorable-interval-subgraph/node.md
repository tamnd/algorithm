---
tag: BSZ8S6
kind: problem
slug: k-colorable-interval-subgraph
name: Maximum weight k-colorable interval subgraph
aliases:
- Maximum weight k-colorable subgraph of an interval graph
area: sequences/interval-problems
level: research
summary: Select a maximum-weight subfamily of intervals that uses at most k colors.
prereqs: [k-machine-interval-scheduling, interval-coloring-depth-theorem, perfect-graph, chordal-graph]
see_also: [weighted-interval-scheduling, maximum-independent-set, consecutive-ones-property, pq-tree, chromatic-number, clique-number, min-cost-flow-problem, perfect-elimination-ordering]
sources:
  - paper: doi:10.1016/0020-0190(87)90107-4
    title: "Mihalis Yannakakis and Fanica Gavril, The maximum k-colorable subgraph problem for chordal graphs, Information Processing Letters 24(2) (1987), pages 133 to 137"
    locator: polynomial time for chordal graphs with k fixed, NP-hardness for chordal graphs with k in the input, and the interval graph case for every k
  - paper: doi:10.1016/0166-218X(93)E0174-W
    title: "Martin C. Carlisle and Errol L. Lloyd, On the k-coloring of intervals, Discrete Applied Mathematics 59(3) (1995), pages 225 to 235"
    locator: the O(k + n) algorithm for maximum cardinality with presorted end points and the O(k S(n)) algorithm for maximum weight
  - url: https://arxiv.org/abs/2001.09644
    title: "Olga Kuryatnikova, Renata Sotirov and Juan C. Vera, The maximum k-colorable subgraph problem and related problems, arXiv:2001.09644"
    locator: Section 1, Introduction (the survey of graph classes where the problem is polynomial or NP-hard)
  - paper: doi:10.1016/0166-218X(87)90037-0
    title: "Esther M. Arkin and Ellen B. Silverberg, Scheduling jobs with fixed start and end times, Discrete Applied Mathematics 18(1) (1987), pages 1 to 8"
    locator: the minimum cost flow solution of the weighted problem on k machines
---

The maximum weight $k$-colorable subgraph problem asks, for a graph with vertex weights and an integer $k$, for a heaviest set of vertices whose induced subgraph can be properly colored with $k$ colors. On general graphs it contains maximum independent set ($k = 1$) and so is NP-hard, and Yannakakis and Gavril showed that it stays NP-hard on [chordal graphs](/chordal-graph/) when $k$ is part of the input, though it is polynomial there for each fixed $k$. On interval graphs it is polynomial for every $k$: by the [depth theorem](/interval-coloring-depth-theorem/) it is the same as choosing a heaviest family of depth at most $k$, which is [k-machine interval scheduling](/k-machine-interval-scheduling/) and is solved by a minimum cost flow. This page treats the problem from the graph side: why interval graphs are easy inside a hard class, what is known nearby, and how the end point type changes the graph.

## In plain words

Draw a dot for each interval and join two dots when their intervals overlap. Each dot has a value. You may paint dots with $k$ colors, and two joined dots must get different colors. Dots you cannot paint are thrown away. Keep as much value as possible.

For dots that come from intervals, a set of dots can be painted with $k$ colors exactly when no point of the line lies in more than $k$ of their intervals. That makes the problem a question about piles of intervals, which a flow computation solves.

For other graphs, even for graphs that look very much like interval graphs, nobody knows a fast method when $k$ can be large, and most likely none exists.

## Definition

**Input.** A graph $G = (V, E)$ with weights $w : V \to \mathbb{R}_{> 0}$ and an integer $k \ge 1$. In the interval case, $G$ is the interval graph of intervals $I_v = \langle l_v, r_v \rangle$, $v \in V$, of one type, with an edge $uv$ when $I_u \cap I_v \ne \emptyset$; the intervals are part of the input, or are first found by a linear time recognition algorithm.

**Output.** A set $S \subseteq V$ such that the induced subgraph $G[S]$ has a proper coloring $c : S \to \{1, \ldots, k\}$, with $c(u) \ne c(v)$ for each edge $uv$ inside $S$, and of largest weight $w(S) = \sum_{v \in S} w(v)$.

**The interval case is a depth bound.** For an interval graph, the following are equivalent for $S \subseteq V$:

1. $G[S]$ is $k$-colorable, $\chi(G[S]) \le k$.
2. $G[S]$ has no clique of more than $k$ vertices, $\omega(G[S]) \le k$.
3. No point lies in more than $k$ of the intervals $I_v$, $v \in S$.

*Proof.* $G[S]$ is the interval graph of the subfamily $\{I_v : v \in S\}$, so the [depth theorem](/interval-coloring-depth-theorem/) gives $\chi(G[S]) = \omega(G[S]) = $ the depth of the subfamily. $\square$

The equivalence of 1 and 2 holds in every [perfect graph](/perfect-graph/), since there $\chi = \omega$ for every induced subgraph. The equivalence with 3 uses the [Helly property](/helly-property-intervals/) of intervals: a clique is a set of intervals through one point.

**End point types.** The type changes the graph, not the problem. Closed intervals that touch, $[1, 3]$ and $[3, 5]$, are adjacent; half-open ones, $[1, 3)$ and $[3, 5)$, are not. A family of depth $k + 1$ as closed intervals can have depth $k$ as half-open intervals, so the optimum can differ.

## Variants

- **Maximum cardinality.** Unit weights: the largest $k$-colorable induced subgraph. Yannakakis and Gavril solve it on interval graphs for every $k$, and Carlisle and Lloyd in $O(k + n)$ time with presorted end points.
- **Fixed $k$ on chordal graphs.** Polynomial for each fixed $k$, by Yannakakis and Gavril, with a running time that grows with $k$ in the exponent.
- **$k$ in the input on chordal graphs.** NP-hard, by Yannakakis and Gavril. Since interval graphs are chordal, this places the easy case of this page inside a hard class.
- **$k = 1$.** Maximum weight [independent set](/maximum-independent-set/): [weighted interval scheduling](/weighted-interval-scheduling/) on interval graphs, polynomial on chordal graphs and on perfect graphs in general, NP-hard on all graphs.
- **Connected version.** Yannakakis and Gavril also study the largest connected $k$-colorable induced subgraph of a chordal graph.
- **Other classes.** The survey of Kuryatnikova, Sotirov and Vera lists polynomial cases, among them circular-arc graphs and tolerance graphs for $k = 2$.
- **The edge version.** Maximum $k$-colorable subgraph is sometimes stated with edges deleted instead of vertices; this page is about induced subgraphs, the vertex version.

## Examples

**Intervals.** The six weighted intervals of the [k-machine scheduling](/k-machine-interval-scheduling/) page, $a = (0, 3), b = (3, 6), c = (1, 5), d = (5, 8), e = (6, 9), f = (8, 10)$ with weights $2, 4, 5, 3, 4, 2$:

- *As closed intervals*, the interval graph has the edges $ab, ac, bc, bd, be, cd, de, df, ef$, and its largest cliques, $\{a, b, c\}$, $\{b, c, d\}$, $\{b, d, e\}$ and $\{d, e, f\}$, have 3 vertices. For $k = 2$ an optimal $S$ must meet each of these triangles in at most 2 vertices. $S = \{b, c, e, f\}$ does, with weight 15, and induces the path $c - b - e - f$, colored $1, 2, 1, 2$.
- *As half-open intervals*, the touching pairs $ab, cd, be, df$ are no longer edges. The graph has the edges $ac, bc, bd, de, ef$, a path $a - c - b - d - e - f$, which is 2-colorable, so for $k = 2$ all six vertices are kept, weight 20.

**Why perfection matters.** In the 5-cycle, $\omega = 2$ but $\chi = 3$, so the largest 2-colorable induced subgraph has 4 vertices, a path, even though the whole graph has no triangle. The clique bound of item 2 fails there, and the 5-cycle is not an interval graph, since it is not chordal.

**Edge cases.** If $k$ is at least the clique number, $S = V$. If the graph has no edges, $S = V$ for every $k \ge 1$.

## Known algorithms

- **Minimum cost flow.** Solve the depth form by the flow of Arkin and Silverberg described on the [k-machine scheduling](/k-machine-interval-scheduling/) page: $k$ units along the sorted end points, an arc of cost $-w_v$ for each interval. With successive shortest paths this takes $O(k n \log n)$ time; Carlisle and Lloyd give $O(k S(n))$, with $S(n)$ the time of one shortest path computation.
- **Unit weights.** Carlisle and Lloyd, $O(k + n)$ time after sorting the end points.
- **Linear programming.** The constraints "at most $k$ chosen intervals through each point" form a matrix with the [consecutive ones property](/consecutive-ones-property/), which is totally unimodular, so the LP relaxation has an integral optimal vertex.
- **Chordal graphs, fixed $k$.** The algorithm of Yannakakis and Gavril, polynomial for each fixed $k$; chordal graphs are the graphs with a [perfect elimination ordering](/perfect-elimination-ordering/), the structure such algorithms work along.
- **From a graph alone.** If only $G$ is given, an interval model is found in linear time by the [PQ-tree](/pq-tree/) algorithm of Booth and Lueker, and then the flow applies.

## Bounds

**Upper bound for interval graphs.** $O(k n \log n)$ time for weights by the flow, and $O(k + n)$ for unit weights after sorting, given the intervals.

**Lower bound.** $\Omega(n \log n)$ in the algebraic decision tree model when the intervals are given, by the element distinctness reduction on the [k-machine scheduling](/k-machine-interval-scheduling/) page.

**Hardness nearby.** NP-hard on chordal graphs with $k$ in the input, by Yannakakis and Gavril. With $k = 1$ it is maximum weight independent set, NP-hard on general graphs.

## Reductions

- **Equivalent to k-machine interval scheduling.** By the equivalence of 1 and 3 above, for a graph given by intervals.
- **From maximum weight independent set.** The case $k = 1$, in any class of graphs.
- **To minimum cost flow and to linear programming.** For interval graphs, as above.
- **Via perfection.** On a perfect graph the problem is the heaviest induced subgraph with no clique of size $k + 1$; on interval graphs, cliques are points, which turns this into the depth constraint.

## Applications

- **Register allocation.** Interval graphs of live ranges with $k$ registers: keep the heaviest set of variables that fits, as Carlisle and Lloyd note.
- **Scheduling on identical machines.** The fixed job scheduling of the [k-machine](/k-machine-interval-scheduling/) page.
- **Routing.** Assigning nets to $k$ tracks of a channel, where each net occupies an interval, also named by Carlisle and Lloyd.
- **Complexity theory.** Interval graphs mark a boundary: the problem is polynomial for every $k$ on interval graphs but NP-hard on chordal graphs, which makes it a test case for which structure of interval graphs an algorithm uses.

## References
