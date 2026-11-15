---
tag: TYA2PW
kind: algorithm
slug: point-algebra-consistency
name: Point algebra consistency algorithm
aliases:
- van Beek's algorithm
area: information-retrieval-and-ai-reasoning/qualitative-temporal-and-spatial-reasoning
level: advanced
summary: Decides consistency of a point algebra network, including not-equal labels, with strongly connected components of the order graph, and returns a solution, in O(n^2) time.
model: word-ram
complexity:
  vars: {n: the number of points, e: the number of labelled pairs}
  time: {worst: O(n + e)}
  space: {extra: O(n + e)}
properties: {deterministic: true, exact: true, in_place: false, online: false, recursive: false}
history:
  year: 1990
  people: [Peter van Beek, Peter B. Ladkin, Roger D. Maddux]
  note: Van Beek (AAAI 1990, journal version 1992) gave the O(n^2) method that finds a consistent scenario of a point algebra network with strongly connected components and a topological sort.
prereqs: [point-algebra, strongly-connected-components, qualitative-constraint-network]
see_also: [tarjan-scc, topological-sort, algebraic-closure, simple-temporal-problem, ord-horn-subclass, allen-constraint-propagation]
sources:
  - paper: doi:10.1016/0004-3702(92)90011-L
    title: Peter van Beek, Reasoning about qualitative temporal information, Artificial Intelligence 58(1-3), 1992
    locator: pages 297 to 326 (the O(n^2) algorithm for a consistent scenario of a point algebra network, and the O(n^4) algorithm for its minimal labels)
  - paper: "Peter van Beek, Reasoning about qualitative temporal information, Proceedings of AAAI-90, AAAI Press, 1990, pages 728 to 734"
    locator: the conference version of the same results
  - paper: doi:10.1145/176584.176585
    title: Peter B. Ladkin and Roger D. Maddux, On binary constraint problems, Journal of the ACM 41(3), 1994
    locator: pages 435 to 469 (path consistency decides consistency of point algebra networks, and a solution can then be found in O(n^2) time)
  - paper: doi:10.1137/0201010
    title: Robert Tarjan, Depth-first search and linear graph algorithms, SIAM Journal on Computing 1(2), 1972
    locator: pages 146 to 160 (strongly connected components in linear time)
  - paper: doi:10.1016/b978-1-4832-1447-4.50034-1
    title: Marc Vilain, Henry Kautz and Peter van Beek, Constraint propagation algorithms for temporal reasoning, a revised report, in Readings in Qualitative Reasoning about Physical Systems, Morgan Kaufmann, 1990
    locator: pages 373 to 381 (the point algebra, and propagation for networks of points)
  - book: isbn:9781558608900
    title: Rina Dechter, Constraint Processing, Morgan Kaufmann, 2003
    locator: Chapter 12, Temporal constraint networks (qualitative point networks)
---

The point algebra consistency algorithm decides whether a network of [point algebra](/point-algebra/) constraints has a solution, and it returns one. A label on a pair of points is a union of $<$, $=$ and $>$, so it can say $\le$, $\ge$ or $\ne$. The algorithm builds a directed graph with an edge for each label that says "at most", finds its [strongly connected components](/strongly-connected-components/), rejects the network if a label inside one component forbids equality, and numbers the components in topological order. It runs in $O(n + e)$ time, which is $O(n^2)$, against $O(n^3)$ for [algebraic closure](/algebraic-closure/), which also decides this problem. The component step is the plain graph algorithm; what this page adds is the reduction from labels to edges and the test for $\ne$.

## In plain words

Each constraint compares two moments in time. "a is at most b" is an arrow from a to b. If the arrows go round in a circle, every moment on the circle must be the same moment, so they collapse to one. If a constraint inside such a circle says "these two are different" or "this one is strictly earlier", there is no answer. Otherwise the collapsed groups can be put in a line that follows all the arrows, and giving each group its position in that line gives times that keep every constraint, including the "different" ones, because different groups get different times.

## The problem

The input is a network on the points $0, \ldots, n-1$ with a label $R_{ij} \subseteq \{<, =, >\}$ on some pairs $i < j$. A missing pair has the universal label, and $R_{ji}$ is the converse of $R_{ij}$, which swaps $<$ and $>$. There are $2^3 = 8$ labels: $\emptyset$, $<$, $=$, $>$, $\le$, $\ge$, $\ne$ and the universal label. The question is whether there are numbers $v_0, \ldots, v_{n-1}$ with $\mathrm{sign}(v_i - v_j) \in R_{ij}$ for every pair; if so, return them. The cost is counted on a word-RAM, in the number of points $n$ and of labelled pairs $e \le \binom{n}{2}$.

## The algorithm

```pseudo id=main
PA-CONSISTENCY(n, R)                 ▷ R[i][j] ⊆ {<, =, >}, with R[j][i] = conv R[i][j]
L1  if some R[i][j] = ∅ then return INCONSISTENT
L2  G ← the directed graph on the points 0 .. n-1 with no edges
L3  for each ordered pair (i, j) with R[i][j] ⊆ {<, =} do add the edge i → j
L4  C ← the strongly connected components of G, numbered in topological order
L5  for each labelled pair {i, j} with C(i) = C(j) do
L6      if = ∉ R[i][j] then return INCONSISTENT
L7  return v with v[i] ← the number of C(i)
```

Line L3 reads each label in both directions. The labels $<$, $\le$ and $=$ give an edge from $i$ to $j$, and $>$, $\ge$ and $=$ give an edge from $j$ to $i$; so $=$ gives edges both ways. The labels $\ne$ and universal give no edge, because they do not order the points. Line L4 uses [Tarjan's algorithm](/tarjan-scc/), which outputs the components in reverse [topological order](/topological-sort/). Line L6 catches both kinds of contradiction: a strict $<$ along a cycle of $\le$, and a $\ne$ between two points that a cycle forces to be equal.

## Example

Take 4 points with $x_0 \le x_1$, $x_1 \le x_2$, $x_0 \ge x_2$, $x_2 \ne x_3$ and $x_0 \ge x_3$.

| step | what happens |
|---|---|
| L3 | edges $0 \to 1$, $1 \to 2$, $2 \to 0$ (from $x_0 \ge x_2$) and $3 \to 0$ (from $x_0 \ge x_3$); no edge for $x_2 \ne x_3$ |
| L4 | components $\{0, 1, 2\}$ and $\{3\}$, with $\{3\}$ first in topological order |
| L5, L6 | the pairs $\{0, 1\}$, $\{1, 2\}$ and $\{0, 2\}$ are inside one component; each label contains $=$ |
| L7 | $v = (1, 1, 1, 0)$ |

The answer $x_0 = x_1 = x_2 = 1$ and $x_3 = 0$ satisfies $x_2 \ne x_3$ because the two points are in different components. If we add $x_1 = x_3$, line L3 adds the edges $1 \to 3$ and $3 \to 1$, all four points form one component, and line L6 finds the label $\ne$ of $\{2, 3\}$ inside it. The network is then inconsistent.

## Correctness

If the algorithm rejects, there is no solution: along a directed cycle of $\le$ edges every solution has equal values, which the label checked at line L6 forbids. If it accepts, take any labelled pair. Inside one component the two values are equal and the label allows $=$. In different components the values differ, and if the label did not allow the order that $v$ gives, the label in the other direction would be inside $\{<, =\}$, so there would be an edge that points against the topological order, which is impossible. So $v$ is a solution. The full proof is in the proof file of this page.

## Complexity

**Time.** Lines L1 and L3 read each labelled pair once and add at most 2 edges per pair, so $G$ has $O(e)$ edges. Tarjan's algorithm takes $O(n + e)$ time. Lines L5 to L7 take $O(n + e)$ more. The total is $O(n + e) = O(n^2)$, which is linear in the size of the input when the network is given as a complete matrix.

**Space.** The graph and the component numbers take $O(n + e)$ words.

Finding the *minimal* labels, the set of base relations of each pair that occur in some solution, is harder: van Beek (1992) needs $O(n^4)$ time when $\ne$ is allowed, because path consistency does not remove every impossible base relation. Without $\ne$, path consistency gives the minimal labels.

## Properties

- **Exact.** It decides consistency and returns a solution, for all 8 labels, including $\ne$.
- **Linear in the input.** It reads each label a constant number of times.
- **Solutions with few values.** The values are integers in $0, \ldots, n-1$, one per component. Points in different components always get different values, so the solution is as "spread out" as the constraints allow.
- **Not incremental.** Adding one constraint can merge components, and the algorithm is run again from the start. For a stream of additions, [algebraic closure](/algebraic-closure/) in the incremental form keeps all labels up to date.

## Variants and improvements

- **Path consistency.** [Algebraic closure](/algebraic-closure/) with the $3 \times 3$ table also decides consistency of point algebra networks (Ladkin and Maddux 1994), in $O(n^3)$ time, and it also tightens the labels.
- **Minimal labels.** Van Beek (1992) computes the minimal network in $O(n^4)$ time with an extra step for the $\ne$ labels that path consistency misses.
- **Pointisable interval networks.** An interval network whose labels can all be written as point algebra constraints on the endpoints (the pointisable relations, 188 of the $2^{13}$ including the empty relation) is solved by this algorithm on its $2n$ endpoints.
- **Metric constraints.** With bounds on differences, $a \le x_j - x_i \le b$, the problem is the [simple temporal problem](/simple-temporal-problem/), solved by shortest paths. Strict inequalities and $\ne$ need extra care there.

## When to use it

Use it when every constraint compares two time points or two numbers by $<$, $\le$, $=$, $\ge$, $>$ or $\ne$: event orders, version orders, the endpoints of pointisable interval networks. It is the fastest exact method for this class. If you also need the tightest label of each pair, run [algebraic closure](/algebraic-closure/) or van Beek's minimal-label algorithm. If the constraints relate intervals with disjunctions that are not pointisable, use [Allen's propagation](/allen-constraint-propagation/) with search instead.

## Pitfalls

- **Treating $\ne$ as an edge.** Line L3 must not add an edge for $\ne$. An edge for $\ne$ would force an order between two points that have none.
- **Checking only the strict labels.** Line L6 must test every labelled pair inside a component for $=$, not only the pairs labelled $<$. A $\ne$ inside a cycle of $\le$ is also a contradiction, and a test that looks only at the edges of $G$ does not see it, because $\ne$ makes no edge.
- **Reading one direction.** Line L3 must look at $R_{ji}$ as well as $R_{ij}$. A label $\ge$ stored on the pair $(i, j)$ gives the edge $j \to i$.
- **Numbering in the wrong direction.** Tarjan's algorithm finds sink components first. Line L7 must reverse that order; otherwise every strict constraint between components is violated.
- **Empty labels.** Line L1 is needed: an empty label on an isolated pair makes no edge and would not be found by the later lines.

## Implementations

## History

Vilain and Kautz (1986) introduced the point algebra and showed that propagation is polynomial for it. Van Beek (AAAI 1990, journal version 1992) gave the algorithm on this page for a consistent scenario, in $O(n^2)$ time, and an $O(n^4)$ algorithm for the minimal labels when $\ne$ is present. Ladkin and Maddux (1994) proved, in the language of relation algebras, that path consistency decides consistency of point algebra networks. The component step is Tarjan's linear-time algorithm (1972).

## References
