---
tag: 93CM0J
kind: algorithm
slug: prim-dijkstra-tradeoff
name: Prim-Dijkstra tradeoff
aliases:
- PD tree
- Alpert Prim-Dijkstra
area: cad/routing
level: advanced
summary: Alpert and coauthors' tree builder with a parameter c in [0, 1] that blends Prim's minimum spanning tree and Dijkstra's shortest path tree to trade wire length for radius.
model: real-ram
complexity:
  vars: {n: the number of pins}
  time: {worst: Θ(n^2)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1993
  people: [Charles J. Alpert, T. C. Hu, J. H. Huang, Andrew B. Kahng, David Karger]
  note: The method was presented in 1993, and the journal version appeared in IEEE Transactions on Computer-Aided Design in 1995. Alpert and coauthors revisited it for modern timing-driven routing in 2018.
prereqs: [prim, dijkstra]
see_also: [prim, dijkstra, minimum-spanning-tree, shortest-path-tree, bounded-radius-bounded-cost-tree, rectilinear-minimum-spanning-tree, elmore-delay, rectilinear-steiner-arborescence]
sources:
  - paper: doi:10.1109/43.391737
    title: C. J. Alpert, T. C. Hu, J. H. Huang, A. B. Kahng and D. Karger, Prim-Dijkstra tradeoffs for improved performance-driven routing tree design, IEEE Transactions on Computer-Aided Design 14(7), 890 to 896, 1995
    locator: the construction with the key c d(u) + dist(u, v) and its experiments
  - paper: doi:10.1109/43.137519
    title: J. Cong, A. B. Kahng, G. Robins, M. Sarrafzadeh and C. K. Wong, Provably good performance-driven global routing, IEEE Transactions on Computer-Aided Design 11(6), 739 to 752, 1992
    locator: the bounded-radius bounded-cost trees that the Prim-Dijkstra trees are compared with
---

The Prim-Dijkstra tradeoff of Charles Alpert, T. C. Hu, J. H. Huang, Andrew Kahng and David Karger builds a routing tree for a net in electronic design automation (EDA) that is short and also has short paths from the driver. It grows a tree from the source pin like [Prim's algorithm](/prim/) and [Dijkstra's algorithm](/dijkstra/), but it adds the pin $v$ and tree point $u$ that minimize $c \cdot d(u) + \mathrm{dist}(u, v)$, where $d(u)$ is the path length from the source to $u$ in the tree and $c \in [0, 1]$ is a parameter. With $c = 0$ this is Prim's algorithm and gives a [minimum spanning tree](/minimum-spanning-tree/). With $c = 1$ it is Dijkstra's algorithm and gives a [shortest path tree](/shortest-path-tree/). Values in between trade total wire, which sets the capacitance, against the radius, the longest source-to-sink path, which sets the delay to the far sinks.

## In plain words

A net has one driver and several sinks. The minimum spanning tree uses the least wire, but a sink can sit at the end of a long detour, and its signal arrives late. Wiring each sink straight to the driver gives the shortest paths, but uses a lot of wire.

Build the tree one sink at a time from the driver. Prim's rule adds the sink closest to the tree. Dijkstra's rule adds the sink whose path from the driver would be shortest.

The Prim-Dijkstra rule mixes the two. It adds the sink with the smallest value of "the wire to reach it" plus $c$ times "the path from the driver to where it joins". A small $c$ cares mostly about wire, a large $c$ mostly about path length. A designer tries a few values of $c$ and keeps the best tree.

## The problem

The input is a set of $n$ points $p_0, \ldots, p_{n-1}$ with a source $s = p_0$, and a metric $\mathrm{dist}$, in routing the L1 distance $|x_u - x_v| + |y_u - y_v|$. The output is a spanning tree rooted at $s$. Its *cost* is the sum of its edge lengths, and its *radius* is the largest path length $d(v)$ from $s$ to a point $v$ in the tree. Let $R = \max_v \mathrm{dist}(s, v)$. No tree has radius less than $R$, and no tree has cost less than the minimum spanning tree $\mathrm{MST}$. In general no single tree reaches both, so the goal is a good tradeoff, as in the [bounded-radius bounded-cost tree](/bounded-radius-bounded-cost-tree/).

## The algorithm

```pseudo id=main
PRIM-DIJKSTRA(points, s, c)
L1  d(s) ← 0;  T ← {s};  for each v ≠ s: key(v) ← dist(s, v), best(v) ← s
L2  repeat n − 1 times
L3      v ← the point not in T with the least key(v), ties to the smaller index
L4      u ← best(v);  add v to T with parent u;  d(v) ← d(u) + dist(u, v)
L5      for each point w not in T do
L6          if c · d(v) + dist(v, w) < key(w) then key(w) ← c · d(v) + dist(v, w);  best(w) ← v
L7  return the parents and the path lengths d
```

The keys are those of Prim's algorithm with an array, so each step takes $O(n)$ time. The key of $w$ is $\min_{u \in T} c \cdot d(u) + \mathrm{dist}(u, w)$ at all times, because $d(u)$ does not change once $u$ is in the tree.

## Example

Take nine points that run up, across and down, with the source at the bottom left:

$p_0 = (0, 0)$, $p_1 = (1, 3)$, $p_2 = (2, 6)$, $p_3 = (3, 9)$, $p_4 = (6, 9)$, $p_5 = (9, 9)$, $p_6 = (9, 6)$, $p_7 = (9, 3)$, $p_8 = (9, 0)$.

The minimum spanning tree is the chain $p_0, p_1, \ldots, p_8$, of cost 27. In it the last point $p_8$ is 27 away from the source along the tree, though it is only 9 away in the plane. The largest distance from the source is $R = 18$, to $p_5$.

| $c$ | parents of $p_1, \ldots, p_8$ | cost | radius |
| --- | --- | --- | --- |
| 0 | $p_0, p_1, p_2, p_3, p_4, p_5, p_6, p_7$ | 27 | 27 |
| 1/4 | $p_0, p_1, p_2, p_3, p_4, p_5, p_6, p_0$ | 33 | 24 |
| 1/2 | $p_0, p_1, p_2, p_3, p_4, p_7, p_8, p_0$ | 33 | 18 |
| 3/4 | the same as for 1/2 | 33 | 18 |
| 1 | $p_0$ for all | 93 | 18 |

With $c = 1/4$, the point $p_8$ is joined straight to the source. With $c = 1/2$, the right side of the net hangs from $p_8$, so both sides are reached by short paths. This tree has the optimal radius 18 at cost 33, while the shortest path tree of $c = 1$ has the same radius at cost 93: in the L1 metric many shortest path trees exist, and Dijkstra's rule with its ties picks the star.

## Correctness

The [proof](proofs/correctness.md) shows the following.

- **A spanning tree.** Each step adds one new point with a parent already in the tree, so the result is a spanning tree rooted at $s$, and $d(v)$ is the length of its tree path.
- **The keys are right.** Line L6 keeps $\mathrm{key}(w) = \min_{u \in T} c \cdot d(u) + \mathrm{dist}(u, w)$.
- **The two ends.** With $c = 0$ the key is the distance to the tree, so the result is Prim's minimum spanning tree. With $c = 1$ the key is $d(u) + \mathrm{dist}(u, w)$, so the result is Dijkstra's shortest path tree of the complete graph, and $d(v) = \mathrm{dist}(s, v)$ for every $v$ by the triangle inequality.
- **A radius bound.** For every $c \in (0, 1]$ and every point, $c \cdot d(v) \le \mathrm{dist}(s, v)$, so the radius is at most $R / c$.

## Complexity

- **Time.** $n - 1$ steps, each with a scan of $n$ keys and $n$ updates, so $\Theta(n^2)$, as for Prim's algorithm with an array. This is optimal for the complete graph, which has $\Theta(n^2)$ edges.
- **Space.** The keys, the best tree points, the parents and the path lengths take $\Theta(n)$.
- **Faster forms.** For $c = 0$ and the L1 metric an $O(n \log n)$ method exists, the [rectilinear minimum spanning tree](/rectilinear-minimum-spanning-tree/). For $0 < c < 1$ the keys depend on the tree, and the simple $\Theta(n^2)$ loop is the usual method for nets.

## Properties

- **What is proved.** The result is a spanning tree. It is a minimum spanning tree for $c = 0$ and a shortest path tree for $c = 1$. For every $c \in (0, 1]$ the radius is at most $R / c$. For $0 < c < 1$ no bound on the cost relative to the MST is proved on this page, and none is claimed. For $c = 1$ the cost can be $\Theta(n)$ times the MST: with the source at $(0, 0)$ and the points $(i, k - i)$ for $i = 0, \ldots, k$, every point is at distance $k$, the shortest path tree is the star of cost $(k + 1) k$, and the minimum spanning tree costs $3k$. For $k = 10$ these are 110 and 30.
- **What is measured.** On 100 random nets of 30 points with coordinates from 0 to 999, the source being the first point (Python `random.Random(2027)`), the mean and worst ratios were:

| $c$ | mean cost / MST | worst cost / MST | mean radius / $R$ | worst radius / $R$ |
| --- | --- | --- | --- | --- |
| 0 | 1.000 | 1.000 | 1.744 | 3.321 |
| 1/4 | 1.045 | 1.130 | 1.189 | 1.655 |
| 1/2 | 1.150 | 1.278 | 1.054 | 1.257 |
| 3/4 | 1.310 | 1.587 | 1.012 | 1.087 |
| 1 | 4.209 | 6.654 | 1.000 | 1.000 |

These are toy inputs, not benchmark results. The middle values of $c$ give most of the radius gain for a small part of the cost.
- **Deterministic.** Ties go to the smaller index of the new point and then to the first tree point that reached the key.

## Variants and improvements

- **Steiner trees.** The result is a spanning tree. Routers turn it into a rectilinear Steiner tree by merging overlapping L shapes of edges that leave the same point, which lowers the cost without making paths longer.
- **PD-II.** Alpert and coauthors revisited the method in 2018 and added steps that remove detours and improve the tree after it is built, for the timing-driven routing of modern chips.
- **Bounded radius.** The [bounded-radius bounded-cost tree](/bounded-radius-bounded-cost-tree/) gives a tree with proved bounds on both the radius and the cost, at the price of a looser practical tradeoff.
- **Monotone paths.** If every path from the source must be shortest, the tree is a [rectilinear Steiner arborescence](/rectilinear-steiner-arborescence/), the Steiner form of the case $c = 1$.
- **Delay models.** The path length is a stand-in for delay. The [Elmore delay](/elmore-delay/) of the tree is a better model, and timing-driven routers check the tree against it.

## When to use it

- To build the initial tree of a net in timing-driven global routing, when both wire length and the delay to critical sinks matter.
- When a single knob that moves smoothly from the minimum spanning tree to the shortest path tree is wanted.

When a proved guarantee on both cost and radius is needed, use the [bounded-radius bounded-cost tree](/bounded-radius-bounded-cost-tree/). When only the wire length matters, use the [rectilinear minimum spanning tree](/rectilinear-minimum-spanning-tree/) or a Steiner tree.

## Pitfalls

- **Recomputing d inside the key.** The key uses the path length $d(u)$ of the tree point, not the distance from the source in the plane. With $\mathrm{dist}(s, u)$ instead, the method is a different heuristic, and the proof of the radius bound does not apply to it.
- **Values of c outside [0, 1].** For $c > 1$ the radius bound and the link to Dijkstra's algorithm are lost, since the key is no longer at least $c \cdot d(v)$ of the added point.
- **Treating c = 1 as cheap.** In the L1 metric the shortest path tree is far from unique, and the choice made by the tie rule can be very costly. A [rectilinear Steiner arborescence](/rectilinear-steiner-arborescence/) gives the same path lengths with much less wire.
- **Floating point keys.** With $c$ given as a float, equal keys can compare unequal. Use exact fractions, or a tolerance, to keep the tie rule.

## Implementations

## History

Routing trees with short source-to-sink paths became important in the early 1990s, when wire delay grew in deep submicron chips. Jason Cong, Andrew Kahng, Gabriel Robins, Majid Sarrafzadeh and C. K. Wong gave the bounded-radius bounded-cost trees in 1992, with proved bounds. Charles Alpert, T. C. Hu, J. H. Huang, Andrew Kahng and David Karger presented the direct blend of Prim's and Dijkstra's algorithms in 1993, and published the journal version in 1995, where they compared it with the bounded-radius trees. In 2018 Alpert, Kahng and coauthors revisited the method as PD-II for timing-driven routing.

## References
