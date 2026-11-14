---
tag: 58DVMM
kind: algorithm
slug: bounded-radius-bounded-cost-tree
name: Bounded-radius bounded-cost tree
aliases:
- BRBC
area: eda/routing
level: advanced
summary: Cong and coauthors' routing tree that walks the MST and adds shortcuts to the source, so the radius is within 1 + eps of optimal and the cost within 1 + 2/eps of the MST.
model: real-ram
complexity:
  vars: {n: the number of pins}
  time: {worst: Θ(n^2)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1992
  people: [Jason Cong, Andrew B. Kahng, Gabriel Robins, Majid Sarrafzadeh, C. K. Wong]
  note: Cong, Kahng, Robins, Sarrafzadeh and Wong presented the BRBC construction at ISCAS 1992 and published it in IEEE Transactions on Computer-Aided Design in the same year.
prereqs: [minimum-spanning-tree, depth-first-search, dijkstra]
see_also: [prim-dijkstra-tradeoff, minimum-spanning-tree, shortest-path-tree, rectilinear-minimum-spanning-tree, rectilinear-steiner-arborescence, elmore-delay, global-routing, approximation-ratio]
sources:
  - paper: doi:10.1109/43.137519
    title: J. Cong, A. B. Kahng, G. Robins, M. Sarrafzadeh and C. K. Wong, Provably good performance-driven global routing, IEEE Transactions on Computer-Aided Design 11(6), 739 to 752, 1992
    locator: the BRBC algorithm and the bounds (1 + ε) R on the radius and (1 + 2/ε) on the cost ratio
  - paper: doi:10.1109/43.391737
    title: C. J. Alpert, T. C. Hu, J. H. Huang, A. B. Kahng and D. Karger, Prim-Dijkstra tradeoffs for improved performance-driven routing tree design, IEEE Transactions on Computer-Aided Design 14(7), 890 to 896, 1995
    locator: the comparison of BRBC trees with the Prim-Dijkstra trees
---

The bounded-radius bounded-cost (BRBC) tree of Jason Cong, Andrew Kahng, Gabriel Robins, Majid Sarrafzadeh and C. K. Wong is a routing tree for a net in electronic design automation (EDA) with proved bounds on both its length and its longest path from the source. Given a parameter $\varepsilon > 0$, it walks around the [minimum spanning tree](/minimum-spanning-tree/) of the pins and, whenever the walk has gone more than $\varepsilon R$ since the last shortcut, adds a direct edge from the source to the current pin, where $R$ is the largest distance from the source to a pin. A shortest path tree of the result has radius at most $(1 + \varepsilon) R$ and cost at most $(1 + 2/\varepsilon)$ times the minimum spanning tree. Small $\varepsilon$ gives short paths and more wire; large $\varepsilon$ gives a tree close to the minimum spanning tree.

## In plain words

The driver of a net sends a signal to many sinks. The minimum spanning tree uses the least wire, but a sink can be far from the driver along the tree. A direct wire to every sink gives the shortest paths, but too much wire.

Start with the minimum spanning tree. Walk around it, along every edge down and back up, as you would trace its outline with a pencil. Keep a counter of how far you have walked. When the counter passes $\varepsilon R$, add a wire straight from the driver to the sink you are at, and reset the counter.

Every sink is then close, along the walk, to a sink with a direct wire, so its path from the driver is short. The walk has a fixed length, twice the spanning tree, so not many direct wires are added, and the extra wire is limited too.

## The problem

The input is a set of $n$ points with a source $s$, and a metric $\mathrm{dist}$, in routing the L1 distance. For a tree rooted at $s$, the *cost* is the sum of its edge lengths and the *radius* is the largest path length $d(v)$ from $s$ to a point $v$ in the tree. Let $R = \max_v \mathrm{dist}(s, v)$, a lower bound on the radius of every tree, and let $\mathrm{MST}$ be the cost of a minimum spanning tree, a lower bound on the cost of every spanning tree. Given $\varepsilon > 0$, the task is a spanning tree with radius at most $(1 + \varepsilon) R$ and cost within a constant factor of $\mathrm{MST}$ that depends only on $\varepsilon$.

## The algorithm

```pseudo id=main
BRBC(points, s, ε)
L1  Q ← a minimum spanning tree of the points;  R ← max_v dist(s, v)
L2  run ← 0
L3  for each step from u to v of the depth-first tour of Q from s do
L4      run ← run + dist(u, v)
L5      if run > ε · R then
L6          if v ≠ s and v has no edge to s yet then add the edge (s, v) to Q
L7          run ← 0
L8  return a shortest path tree from s in the graph Q, found with Dijkstra's algorithm
```

The depth-first tour goes down each tree edge to a child and back up, so it has $2(n - 1)$ steps and length $2 \cdot \mathrm{MST}$. The graph $Q$ after line L7 is the tree plus at most $n - 1$ shortcuts, so the shortest path tree of line L8 is cheap to find.

## Example

Take nine points that run up, across and down, with the source at the bottom left:

$p_0 = (0, 0)$, $p_1 = (1, 3)$, $p_2 = (2, 6)$, $p_3 = (3, 9)$, $p_4 = (6, 9)$, $p_5 = (9, 9)$, $p_6 = (9, 6)$, $p_7 = (9, 3)$, $p_8 = (9, 0)$.

The minimum spanning tree is the chain $p_0, \ldots, p_8$ with cost 27, and $R = 18$, the distance to $p_5$. In the chain, $p_8$ is 27 away from the source. Take $\varepsilon = 1$, so the threshold is 18.

| step of the tour | run after the step | action |
| --- | --- | --- |
| $p_0$ to $p_5$ | 4, 8, 12, 15, 18 | none, 18 is not more than 18 |
| $p_5$ to $p_6$ | 21 | add $(p_0, p_6)$ of length 15, reset |
| $p_6$ to $p_8$, back to $p_4$ | 3, 6, 9, 12, 15, 18 | none |
| $p_4$ to $p_3$ | 21 | add $(p_0, p_3)$ of length 12, reset |
| $p_3$ back to $p_0$ | 4, 8, 12 | none |

The shortest path tree of the chain plus the two shortcuts gives the path lengths $0, 4, 8, 12, 15, 18, 15, 18, 21$, so the radius is 21, within the bound $(1 + 1) \cdot 18 = 36$. Its edges are $p_0 p_1$, $p_1 p_2$, $p_0 p_3$, $p_3 p_4$, $p_4 p_5$, $p_0 p_6$, $p_6 p_7$ and $p_7 p_8$, of cost 47, within the bound $3 \cdot 27 = 81$.

| $\varepsilon$ | shortcuts to | cost | radius |
| --- | --- | --- | --- |
| 1/4 | $p_2, p_4, p_6, p_8$ | 61 | 18 |
| 1/2 | $p_3, p_7, p_5, p_2$ | 63 | 18 |
| 1 | $p_6, p_3$ | 47 | 21 |
| 2 | $p_4$ | 39 | 27 |
| 100 | none | 27 | 27 |

A smaller $\varepsilon$ is not always cheaper for the same radius: $\varepsilon = 1/2$ adds four shortcuts and costs more than $\varepsilon = 1/4$. The [Prim-Dijkstra tradeoff](/prim-dijkstra-tradeoff/) with $c = 1/2$ reaches radius 18 here at cost 33.

## Correctness

The [proof](proofs/correctness.md) shows the following.

- **A spanning tree.** The graph $Q$ is connected, since it contains the minimum spanning tree, so the shortest path tree of line L8 spans all points.
- **Radius.** Every point $v$ is reached on the tour at a moment when the run since the last reset is at most $\varepsilon R$. The last reset happened at the source or at a point $w$ with an edge to the source, so $d(w) \le R$, and the tree path from $w$ to $v$ is no longer than that part of the tour. So $d(v) \le R + \varepsilon R$.
- **Cost.** Each shortcut uses up a part of the tour of length more than $\varepsilon R$, and these parts do not overlap. The tour has length $2 \cdot \mathrm{MST}$, so there are fewer than $2 \cdot \mathrm{MST} / (\varepsilon R)$ shortcuts, each of length at most $R$. The shortest path tree is a subgraph of $Q$, so its cost is at most $\mathrm{MST} + 2 \cdot \mathrm{MST}/\varepsilon$.

## Complexity

- **Time.** The minimum spanning tree with Prim's algorithm on all pairs takes $\Theta(n^2)$. The tour has $2(n - 1)$ steps of $O(1)$ each. Dijkstra's algorithm with a binary heap on $Q$, which has at most $2(n - 1)$ edges, takes $O(n \log n)$. The total is $\Theta(n^2)$, or $O(n \log n)$ with the [rectilinear minimum spanning tree](/rectilinear-minimum-spanning-tree/) in the L1 metric.
- **Space.** The tree, the shortcuts, the tour stack and the distances take $\Theta(n)$.

## Properties

- **What is proved.** For every $\varepsilon > 0$ the result is a spanning tree with radius at most $(1 + \varepsilon) R$ and cost at most $(1 + 2/\varepsilon) \cdot \mathrm{MST}$. As $\varepsilon \to 0$ the radius goes to $R$, and as $\varepsilon \to \infty$ the cost bound goes to $\mathrm{MST}$.
- **The tradeoff is real.** Some point sets have no tree that is near both lower bounds at once. For the source at $(0, 0)$ and the points $(i, k - i)$ for $i = 0, \ldots, k$, every point is at distance $k$ from the source, so a tree of radius exactly $R = k$ must join each point straight to the source and costs $(k + 1) k$, while the minimum spanning tree costs $3k$.
- **What is measured.** On 100 random nets of 30 points with coordinates from 0 to 999, the source being the first point (Python `random.Random(2027)`):

| $\varepsilon$ | mean cost / MST | worst cost / MST | mean radius / $R$ | worst radius / $R$ |
| --- | --- | --- | --- | --- |
| 1/4 | 2.670 | 3.584 | 1.030 | 1.202 |
| 1/2 | 2.106 | 2.571 | 1.049 | 1.224 |
| 1 | 1.617 | 1.919 | 1.102 | 1.439 |
| 2 | 1.307 | 1.522 | 1.256 | 2.017 |

All values are within the proved bounds, and far inside the cost bound. On the same nets the Prim-Dijkstra tree with $c = 1/2$ had a mean cost ratio of 1.150 and a mean radius ratio of 1.054. These are toy inputs, not benchmark results.
- **Deterministic.** The tour visits children in the order of their index, and ties in the shortest path tree go to the first path found.

## Variants and improvements

- **Steiner trees.** The output is a spanning tree. Routers turn it into a rectilinear Steiner tree by merging overlapping wires, which lowers the cost and does not make any path longer, so both bounds still hold.
- **Per-sink bounds.** Later constructions bound each path by its own lower bound, $d(v) \le (1 + \varepsilon) \mathrm{dist}(s, v)$ for every $v$, with a cost bound of the same form. These trees are called light approximate shortest-path trees in the work of Khuller, Raghavachari and Young.
- **Prim-Dijkstra.** The [Prim-Dijkstra tradeoff](/prim-dijkstra-tradeoff/) has no proved cost bound but often gives better trees in practice, as in the measurements above.
- **Arborescences.** If every path must be shortest, the tree is a [rectilinear Steiner arborescence](/rectilinear-steiner-arborescence/), the Steiner form of the case $\varepsilon = 0$.

## When to use it

- When a routing tree must come with a guarantee on both its delay, through the radius, and its wire, through the cost.
- As a baseline with proved bounds when testing timing-driven tree heuristics.

When the best practical tradeoff matters more than a guarantee, try the [Prim-Dijkstra tradeoff](/prim-dijkstra-tradeoff/) for a few values of $c$. When a better delay model than the path length is needed, evaluate the trees with the [Elmore delay](/elmore-delay/).

## Pitfalls

- **Taking R as the radius of the MST.** The threshold uses $R = \max_v \mathrm{dist}(s, v)$, the distance in the plane, not the radius of the spanning tree. With the tree radius the threshold is larger, and the bound $(1 + \varepsilon) R$ on the radius no longer holds.
- **Keeping the walk tree as the output.** The graph $Q$ after the shortcuts has cycles. The output is a shortest path tree of it, not $Q$ itself.
- **Resetting at the wrong time.** The run must be reset whenever the threshold is passed, also when the point already has an edge to the source or is the source. Otherwise the cost bound breaks, since one shortcut would no longer stand for its own part of the tour.
- **Floating point thresholds.** With $\varepsilon$ as a float, a run that equals $\varepsilon R$ may or may not pass it. Use exact numbers when the tie matters, as in the tests.

## Implementations

## History

The minimum spanning tree and the shortest path tree were the two classical routing trees when wire delay began to matter in the early 1990s. Jason Cong, Andrew Kahng, Gabriel Robins, Majid Sarrafzadeh and C. K. Wong presented the BRBC construction, with its bounds on both the radius and the cost, at ISCAS and in IEEE Transactions on Computer-Aided Design in 1992, under the title of provably good performance-driven global routing. Charles Alpert and coauthors compared it with their Prim-Dijkstra trees in 1995. In network design, Samir Khuller, Balaji Raghavachari and Neal Young gave trees with a bound for each path in 1995.

## References
