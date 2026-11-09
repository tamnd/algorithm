---
tag: 78899M
kind: data-structure
slug: yao-graph
name: Yao graph
aliases:
- theta-graph
- Yao graph Y_k
- cone graph
area: geometry/proximity
level: research
summary: Geometric graph that connects each point to its nearest point in each of k cones around it; a spanner construction.
model: real-ram
complexity:
  vars: {n: the number of points, k: the number of cones, d: the degree of the queried vertex}
  time: {build: O(n^2), has_edge: O(1), neighbors: O(d)}
  space: {total: O(k n)}
history:
  year: 1982
  people: [Andrew Chi-Chih Yao]
  note: Yao used the nearest neighbour in each of a fixed number of cones in 1982 to compute minimum spanning trees in k-dimensional space faster than by examining all pairs; the graph later became a standard spanner construction.
prereqs: [geometric-spanner, euclidean-distance, minimum-spanning-tree]
see_also: [euclidean-minimum-spanning-tree, well-separated-pair-decomposition, proximity-graphs, nearest-neighbor-graph, dijkstra, delaunay-triangulation, gabriel-graph]
sources:
  - paper: doi:10.1137/0211059
    title: Andrew Chi-Chih Yao, On constructing minimum spanning trees in k-dimensional spaces and related problems, SIAM Journal on Computing 11(4), 1982, 721-736
    locator: the partition of space around each point into cones of small angle and the nearest neighbour in each cone, used to reduce the candidate edges of a minimum spanning tree
  - book: isbn:9780521815130
    title: Giri Narasimhan and Michiel Smid, Geometric Spanner Networks, Cambridge University Press, 2007
    locator: the chapters on the Theta-graph and the Yao graph (the stretch bound 1/(1 - 2 sin(theta/2)) and the constructions)
  - paper: "Kenneth L. Clarkson, Approximation algorithms for shortest path motion planning, Proceedings of the 19th Annual ACM Symposium on Theory of Computing, 1987, 56-65"
    locator: the cone-based spanner of the visibility graph, one origin of Theta-graphs
  - paper: "J. Mark Keil, Approximating the complete Euclidean graph, Proceedings of the 1st Scandinavian Workshop on Algorithm Theory, Lecture Notes in Computer Science 318, 1988, 208-213"
    locator: the cone-based spanner of the complete Euclidean graph and its stretch bound
  - paper: "Prosenjit Bose, Mirela Damian, Karim Douieb, Joseph O'Rourke, Ben Seamone, Michiel Smid and Stefanie Wuhrer, pi/2-angle Yao graphs are spanners, International Journal of Computational Geometry and Applications 22(1), 2012, 61-82"
    locator: the proof that the Yao graph with four cones has bounded stretch
---

The Yao graph $Y_k$ of a point set $P$ divides the plane around each point $p$ into $k$ cones of angle $2\pi/k$ with apex $p$, and joins $p$ to a nearest point of $P$ in each nonempty cone. Each point picks at most $k$ neighbours, so the graph has at most $kn$ edges. For $k \ge 7$ it is a [geometric spanner](/geometric-spanner/): between any two points there is a path at most $t = 1/(1 - 2 \sin(\pi/k))$ times their distance, about $4.26$ for $k = 8$. For $k \ge 6$ it contains every [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/), which is how Yao (1982) used it. This page fixes the cones to the four quadrants or the eight octants bounded by the axes and the diagonals, so the cone of a vector is found by exact comparisons, and builds the graph in $O(n^2)$ time.

## In plain words

Stand at a point and split the view around you into eight equal slices, like a pie. In each slice, find the closest other point and connect to it. Every point does the same.

Each point has at most eight links, so the network stays small. Yet it gets you anywhere without a big detour: to reach a far point, take the link in the slice that contains it. That link goes to a point at most as far away, in nearly the right direction, and from there you are strictly closer. Repeating gives a route at most about four times as long as the straight line, and usually much better.

The cheapest network that connects all the points is always inside this one.

## The abstract type

A static undirected graph on $\{0, \ldots, n-1\}$, built from distinct points $p_0, \ldots, p_{n-1}$ and the number of cones $k$:

- `build(P, k)`: compute the graph.
- `has_edge(i, j)`: whether $\{i, j\}$ is an edge.
- `neighbors(i)`: the vertices adjacent to $i$.

The cones are half-open, $C_j = \{v \ne 0 : \text{angle}(v) \in [2\pi j/k, 2\pi (j+1)/k)\}$, so each vector is in exactly one. Among several nearest points in a cone, the smallest index wins. The directed version keeps the choice of each point; the graph here is its undirected union.

## Representation

For each point, the array $best[0..k-1]$ of its chosen neighbours, and a hash set of neighbours per vertex holding the undirected edges. The total size is $O(kn)$.

## Operations

```pseudo id=main
BUILD(P, k)
L1  for each i do
L2    best[0..k−1] ← none
L3    for each j ≠ i do
L4      c ← CONE(P[j] − P[i])
L5      if best[c] = none or ‖P[j] − P[i]‖² < ‖P[best[c]] − P[i]‖² then best[c] ← j
L6    for each c with best[c] ≠ none do add the edge {i, best[c]}

HAS-EDGE(i, j)
L7  return j ∈ adj[i]

NEIGHBORS(i)
L8  return adj[i]
```

CONE in line L4 is exact for the octants. If $dy < 0$, or $dy = 0$ and $dx < 0$, negate the vector and add 4. Then the octant is 0 if $dx > 0$ and $dy < dx$, 1 if $dx > 0$ and $dy \ge dx$, 2 if $-dx < dy$, and 3 otherwise. Quadrants are pairs of octants. For other values of $k$ the boundaries have irrational slopes, and an exact cone test needs a rational approximation of the boundary directions; the stretch bound only needs the cones to have angle at most $2\pi/k$.

## Example

$P = \{(1,3), (1,11), (2,8), (5,1), (9,6), (11,1), (11,4)\}$, the set used on the [Gabriel graph](/gabriel-graph/) page, with $k = 8$. Octants are numbered counterclockwise from the positive $x$-axis.

| point | chosen neighbours (octant: point) |
| --- | --- |
| $(1,3)$ | 0: $(9,6)$; 1: $(2,8)$; 2: $(1,11)$; 7: $(5,1)$ |
| $(1,11)$ | 6: $(2,8)$; 7: $(9,6)$ |
| $(2,8)$ | 2: $(1,11)$; 5: $(1,3)$; 6: $(5,1)$; 7: $(9,6)$ |
| $(5,1)$ | 0: $(11,1)$; 1: $(9,6)$; 2: $(2,8)$; 3: $(1,3)$ |
| $(9,6)$ | 3: $(2,8)$; 4: $(1,3)$; 5: $(5,1)$; 6: $(11,1)$; 7: $(11,4)$ |
| $(11,1)$ | 2: $(11,4)$; 3: $(1,3)$; 4: $(5,1)$ |
| $(11,4)$ | 3: $(9,6)$; 4: $(5,1)$; 6: $(11,1)$ |

In octant 0 of $(1,3)$, both $(9,6)$ and $(11,4)$ are candidates, at squared distances 73 and 101, and $(9,6)$ wins. The 25 choices give 15 undirected edges. The graph is not planar: $(1,3)$, $(9,6)$ crosses $(2,8)$, $(5,1)$. All-pairs [Dijkstra](/dijkstra/) gives a largest stretch of about $1.11$, for the pair $(1,3)$, $(11,4)$, far below the bound $4.26$. With $k = 4$ the graph has 10 edges and largest stretch about $1.27$.

## Correctness

Line L5 keeps the strictly nearest point per cone, so after the scan each cone holds a nearest point. The spanner bound comes from one step. For a pair $p, q$, let $r$ be the point chosen in the cone of $p$ that contains $q$. Then $\|pr\| \le \|pq\|$ and the angle $rpq$ is less than the cone angle $\theta$. Placing $r'$ on $pq$ at distance $\|pr\|$ from $p$ gives $\|rq\| \le \|pq\| - (1 - 2\sin(\theta/2))\|pr\|$, which is less than $\|pq\|$ when $\theta < \pi/3$. Induction on the distance then gives a path of length at most $t\|pq\|$ with $t = 1/(1 - 2\sin(\theta/2))$. The same step shows that an edge missing from the Yao graph is the longest edge of a triangle, so it is in no minimum spanning tree. The full proof is in the correctness proof below.

## Complexity

| operation | time | notes |
| --- | --- | --- |
| BUILD, this page | $O(n^2)$ | each point scans all others once |
| BUILD of the Theta-graph, plane, fixed $k$ | $O(n \log n)$ | one sweep per cone direction (Narasimhan and Smid) |
| HAS-EDGE | $O(1)$ expected | hash set lookup |
| NEIGHBORS | $O(d)$ | $d$ the degree, which can be large: a point can be chosen by many others |
| space | $O(kn)$ | at most $k$ choices per point |

The out-degree is at most $k$, but the in-degree is not bounded: the center of a ring of points is chosen by all of them.

## Variants

- **Theta-graph.** Instead of the Euclidean nearest point in a cone, choose the point whose projection onto the cone's bisector is closest to the apex. Clarkson (1987) and Keil (1988) introduced this rule; it is easier to compute with sweeps and has the stretch bound $1/(1 - 2\sin(\theta/2))$ as well for $\theta < \pi/3$. The two names are often used loosely for each other.
- **Few cones.** The bound above needs $k \ge 7$. Yao graphs with $k = 4$ are still spanners, with a large constant, as shown by Bose and coauthors in 2012; for $k \le 3$ there are point sets with unbounded stretch.
- **Bounded degree.** Keeping, in each cone of each point, only the shortest incoming Yao edge gives the Yao-Yao graph, with degree at most $2k$, but its stretch is much harder to analyse; Narasimhan and Smid describe other constructions of spanners with bounded degree.
- **Higher dimensions.** Cover the directions around a point by $O((1/\theta)^{d-1})$ cones of angular diameter $\theta$ and keep the nearest point in each. Yao's original use was in $\mathbb{R}^d$, to find a minimum spanning tree from $O(n)$ candidate edges.

## When to use it

Use a Yao or Theta graph when you need a sparse graph with guaranteed short paths and want a construction that is local: each point decides its edges from the points around it, which suits wireless network topology control and motion planning. Use it also as a candidate edge set for a minimum spanning tree in higher dimensions. For spanners with stretch arbitrarily close to 1 and a hierarchical structure, use the [well-separated pair decomposition](/well-separated-pair-decomposition/); for a planar spanner, the [Delaunay triangulation](/delaunay-triangulation/).

## Pitfalls

- **Cone boundaries.** A point exactly on a boundary ray must belong to one cone only; with closed cones it can be chosen twice or the angle argument can fail. Half-open cones with exact tests avoid this.
- **Floating-point angles.** Computing $\text{atan2}$ and dividing by $2\pi/k$ can put a point on the wrong side of a boundary. With octants, exact comparisons of $dx$ and $dy$ suffice.
- **Assuming bounded degree.** Each point chooses at most $k$ neighbours, but it can be chosen by many; the undirected degree can be $n - 1$.
- **Measuring the stretch with roots in the comparison.** The stretch is a ratio of sums of square roots; check it numerically with a tolerance, but make the construction itself exact.
- **Too few cones for the bound.** With $k = 6$ the formula gives $1/(1 - 2\sin(\pi/6)) = \infty$; the bound needs $\theta < \pi/3$.

## Implementations

## History

Yao (1982) introduced the cone construction to compute minimum spanning trees in $k$-dimensional space in subquadratic time, observing that in each cone of small angle only the nearest point can be a minimum spanning tree neighbour. Clarkson (1987) and Keil (1988) used cones to build sparse graphs that approximate Euclidean distances, the Theta-graphs, and Ruppert and Seidel (1991) gave the bound $1/(1 - 2\sin(\theta/2))$ in higher dimensions. Narasimhan and Smid (2007) collect the theory of these and other spanners.

## References
