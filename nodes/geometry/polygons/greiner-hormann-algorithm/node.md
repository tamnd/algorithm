---
tag: 34CRJR
kind: algorithm
slug: greiner-hormann-algorithm
name: Greiner-Hormann algorithm
aliases:
- Greiner-Hormann clipping
- greiner-hormann
- Greiner-Hormann polygon clipping
area: geometry/polygons
level: advanced
summary: Polygon clipping by intersecting boundaries and walking between the two polygons.
solves: [polygon-clipping]
model: real-ram
complexity:
  vars: {n: the number of subject vertices, m: the number of clip vertices, k: the number of boundary crossings}
  time: {worst: O(n m + k log k)}
  space: {extra: Θ(n + m + k)}
properties: {online: false, deterministic: true, recursive: false}
history:
  year: 1998
  people: [Günther Greiner, Kai Hormann]
  note: Greiner and Hormann published the algorithm in ACM Transactions on Graphics in 1998; Foster, Hormann and Popa extended it to degenerate intersections in 2019.
prereqs: [polygon-clipping, simple-polygon, segment-intersection-point, doubly-linked-list, point-in-polygon]
see_also: [weiler-atherton-algorithm, sutherland-hodgman, vatti-clipping, polygon-union, even-odd-fill-rule, bentley-ottmann-algorithm, polygon-area, crossing-number-algorithm]
sources:
  - paper: doi:10.1145/274363.274364
    title: Günther Greiner and Kai Hormann, Efficient clipping of arbitrary polygons, ACM Transactions on Graphics 17(2), 1998, 71 to 83
    locator: the three phases (intersection, entry and exit marking, traversal), the union and difference by negated flags, and the perturbation of degenerate vertices
  - paper: doi:10.1016/j.cagx.2019.100007
    title: Erich L. Foster, Kai Hormann and Romeo Traian Popa, Clipping simple polygons with degenerate intersections, Computers and Graphics X 2, 2019, 100007
    locator: the classification of intersections at vertices and along overlapping edges, which removes the need for perturbation
  - paper: "Kevin Weiler and Peter Atherton, Hidden surface removal using polygon area sorting, SIGGRAPH 1977, Computer Graphics 11(2), 214 to 222"
    locator: the earlier method that walks between the boundaries of the subject and the clip polygon
---

The Greiner-Hormann algorithm computes the intersection, union or difference of two polygons, a subject $S$ and a clip polygon $C$, which may both be non-convex. It works in three phases. First it finds every point where the two boundaries cross and inserts each one into both vertex lists, which are [doubly linked lists](/doubly-linked-list/). Each crossing appears as two nodes that point to each other. Next, a [point in polygon](/point-in-polygon/) test at one vertex fixes whether the boundary of each polygon enters or leaves the other one at each crossing. The flags then simply alternate along the boundary. Last, the algorithm walks from crossing to crossing and switches to the other polygon at every crossing, tracing the boundary of the result. It goes forward from an entry and backward from an exit. Union and difference use the same walk with some flags negated. The algorithm is short and simpler than [Weiler and Atherton's](/weiler-atherton-algorithm/). The original version needs the boundaries to cross properly, so a crossing at a vertex or along a shared edge must be perturbed away or handled by the extension of Foster, Hormann and Popa.

## In plain words

Draw two overlapping shapes on paper and mark every place where their outlines cross. Each mark is a door: on one side you are inside the other shape, on the other side you are outside.

Walking along one outline, the doors alternate between "going in" and "going out". So it is enough to know whether your starting corner is inside the other shape. Then you can label every door.

To trace the overlap, start at any door. Walk along the current outline in the direction that stays inside the other shape until you reach the next door. Then step onto the other outline and do the same. When you are back at the start, you have drawn one piece of the answer. Repeat until every door has been used. For the union you walk the outside parts instead.

## The problem

**Input.** Two simple polygons, the subject $S$ with $n$ vertices and the clip polygon $C$ with $m$ vertices, as vertex lists in either orientation with exact coordinates, and an operation: $S \cap C$, $S \cup C$ or $S \setminus C$. Straight vertices are allowed. The boundaries must be in general position with respect to each other: no vertex of one polygon lies on the boundary of the other, which also excludes overlapping edges. This implementation raises an error otherwise.

**Output.** A list of closed rings. A point belongs to the result when it lies inside an odd number of rings, so a ring inside another ring is a hole. Intersections and differences of two simple polygons never have holes when the boundaries cross. A union can have holes.

**Notation.** A *crossing* is a point where an edge of $S$ and an edge of $C$ meet at a single point interior to both. For a crossing on the edge from $a$ to $b$, its parameter is $\alpha \in (0, 1)$ with the point $a + \alpha (b - a)$. A crossing node on the boundary of $P$ is an *entry* if, walking forward along $P$, one passes from outside the other polygon to inside it.

## The algorithm

```pseudo id=main
GREINER-HORMANN(S, C, op)
L1  for each edge e of S and each edge f of C: if e and f cross, make nodes i_S on e and i_C on f with their parameters α, linked as neighbors; if they touch in any other way, report a degenerate input
L2  if there are no crossings then return S, C, both or nothing, according to op and to whether the first vertex of each polygon lies in the other
L3  insert the new nodes into the doubly linked vertex lists of S and C, sorted by α along each edge
L4  for P in (S, C), with Q the other one: inside ← (first vertex of P lies in Q); walk P, and at each crossing node set entry ← not inside and inside ← not inside
L5  if op = union then negate every entry flag of S and of C; if op = S − C then negate every entry flag of S
L6  for each unvisited crossing node start of S do ring ← [start]; cur ← start; repeat
L7      mark cur and neighbor(cur) visited
L8      if cur.entry then repeat cur ← next(cur); append cur to ring until cur is a crossing node
L9      else repeat cur ← prev(cur); append cur to ring until cur is a crossing node
L10     cur ← neighbor(cur)
L11 until cur is visited; output ring without its repeated first point
```

Line L1 computes each crossing exactly. With $d = (b - a) \times (q - p)$ for edges $ab$ and $pq$, the parameters are $\alpha = ((p - a) \times (q - p))/d$ and $\beta = ((p - a) \times (b - a))/d$, and the edges cross when both lie strictly between $0$ and $1$. If either parameter is $0$ or $1$, or $d = 0$ with the edges on one line and overlapping, the boundaries touch at a vertex or share a segment. Line L2 handles boundaries that never meet: then one polygon contains the other or they are disjoint. Line L4 is the only place that uses a [crossing number](/crossing-number-algorithm/) test, once per polygon. After it, the flags alternate along each boundary. Line L5 changes the operation: negating a flag turns the walk from the inside of the other polygon to the outside. Lines L8 and L9 follow the current boundary to the next crossing, and line L10 jumps to the copy of that crossing on the other boundary.

## Example

Take the square $S = (0,0), (4,0), (4,4), (0,4)$ and the quadrilateral $C = (2,-1), (7,1), (5,5), (1,2)$, both counterclockwise. The bottom edge of $S$ crosses the edge of $C$ from $(1,2)$ to $(2,-1)$ at $I_1 = (5/3, 0)$, with $\alpha = 5/12$ on the square's edge. The top edge of $S$, from $(4,4)$ to $(0,4)$, crosses the edge of $C$ from $(5,5)$ to $(1,2)$ at $I_2 = (11/3, 4)$. There are no other crossings. The right edge of $S$ lies inside $C$, and the vertex $(7,1)$ of $C$ lies outside $S$.

The first vertex $(0,0)$ of $S$ is outside $C$, so along $S$ the crossing $I_1$ is an entry and $I_2$ an exit. The first vertex $(2,-1)$ of $C$ is outside $S$, and along $C$ the crossing $I_2$ comes first, so it is an entry and $I_1$ an exit.

| operation | flags on $S$ | flags on $C$ | walk | result | area |
|---|---|---|---|---|---|
| $S \cap C$ | $I_1$ entry, $I_2$ exit | $I_2$ entry, $I_1$ exit | $I_1$ forward on $S$ to $I_2$, then forward on $C$ to $I_1$ | $I_1, (4,0), (4,4), I_2, (1,2)$ | $26/3$ |
| $S \setminus C$ | negated: $I_1$ exit, $I_2$ entry | unchanged | $I_1$ backward on $S$ to $I_2$, then forward on $C$ to $I_1$ | $I_1, (0,0), (0,4), I_2, (1,2)$ | $22/3$ |
| $S \cup C$ | negated | negated: $I_2$ exit, $I_1$ entry | $I_1$ backward on $S$ to $I_2$, then backward on $C$ to $I_1$ | $I_1, (0,0), (0,4), I_2, (5,5), (7,1), (2,-1)$ | $161/6$ |

The areas check out: $26/3 + 22/3 = 16$ is the area of $S$, and $16 + 39/2 - 26/3 = 161/6$, where $39/2$ is the area of $C$. In the union and the difference the walk goes backward along $S$, so those rings come out clockwise. In general the orientation of a ring depends on whether its walk starts at an entry or at an exit, so it is not normalized.

## Correctness

Between two consecutive crossings, each piece of a boundary lies entirely inside or entirely outside the other polygon, because it does not meet the other boundary. By the [Jordan curve theorem](/jordan-curve-theorem/) it switches sides at every crossing. So the flags of line L4, computed from one exact inside test, are correct for every crossing node. The boundary of $S \cap C$ is the union of the pieces of each boundary that lie inside the other polygon. At a crossing it continues from a piece of one boundary to a piece of the other. Lines L8 and L9 follow such a piece in the direction that stays inside, and line L10 switches to the other boundary. So each ring traced is a closed curve made of result boundary pieces, and every crossing is used exactly once. For union and difference, negating the flags selects the outside pieces of the negated polygons instead. Every crossing node is visited once and every other node at most once, so the loops stop. The [full proof](proofs/correctness/) gives the details.

## Complexity

- **Time.** Line L1 tests all $nm$ pairs of edges, in $O(nm)$ time. Sorting the crossings along each edge in line L3 takes $O(k \log k)$ in total, and lines L4 to L11 visit each of the $n + m + 2k$ nodes $O(1)$ times. In total $O(nm + k \log k)$, where $k \le nm$ and $k$ is even.
- **Faster crossing detection.** With a sweep such as [Bentley and Ottmann's](/bentley-ottmann-algorithm/), the crossings take $O((n + m + k) \log (n + m))$ time, and the rest of the algorithm is unchanged.
- **Space.** $\Theta(n + m + k)$ for the two linked lists.
- **Output.** The result can have $\Theta(nm)$ vertices and $\Theta(nm)$ rings, as for two combs at right angles to each other, so no algorithm does better than $\Omega(nm)$ in the worst case.

## Properties

- **Exact.** With integer or rational input, the crossings have rational coordinates and every test is exact. The output coordinates are rationals whose size grows only once, since crossings are never intersected again.
- **Orientation free.** The inputs may be in either orientation, since the flags come from inside tests and not from the direction of the edges. The output rings are not oriented consistently: a ring traced from an exit starts backward. If a fixed orientation is needed, orient each ring afterwards by its nesting depth, outer rings counterclockwise and holes clockwise.
- **Self-intersecting input.** The original paper allows self-intersecting polygons with the even-odd interpretation, since the flags still alternate along each boundary. This implementation is tested on simple polygons only.
- **Not robust to touching.** A vertex on the other boundary, or an overlapping edge, makes the alternation of the flags fail. The original remedy is to move such a vertex slightly, which changes the input.

## Variants and improvements

- **Degenerate intersections.** Foster, Hormann and Popa classify each intersection at a vertex or along an overlapping edge as a crossing or a bouncing point, from the four edges around it. Only true crossings get entry and exit flags, which handles all degenerate cases without perturbation.
- **Perturbation.** The 1998 paper shifts a vertex that lies on the other boundary by a tiny amount and then runs the general position algorithm. The result is correct for the perturbed input but can contain slivers.
- **Sweep based crossings.** For large inputs, phase one is replaced by a plane sweep that reports only the $k$ crossings.
- **Several rings.** The walk extends to polygons with several boundary rings, such as polygons with holes, if the inside test of line L4 counts all rings of the other polygon by the even-odd rule.
- **Other clipping algorithms.** [Sutherland and Hodgman](/sutherland-hodgman/) clip against a convex window one edge at a time. [Vatti's algorithm](/vatti-clipping/) and the sweep of Martinez, Rueda and Feito handle arbitrary polygon sets with holes and degeneracies with a plane sweep.

## When to use it

Use it for boolean operations on a few simple polygons of moderate size, when the input is in general position or can be perturbed, and a short implementation matters more than robustness. For production geometry with shared edges and touching vertices, use the degenerate-case extension of Foster, Hormann and Popa or a sweep based library. For clipping against a convex window, the [Sutherland-Hodgman algorithm](/sutherland-hodgman/) is simpler. For many polygons at once, prefer a sweep such as Vatti's.

## Pitfalls

- **Vertices on the other boundary.** A vertex of $S$ on an edge of $C$ produces a crossing with parameter $0$ or $1$. If it is accepted as a crossing, the flags stop alternating, and the walk can trace the wrong pieces or loop. Detect these cases exactly and reject or perturb them.
- **Floating point parameters.** Computing $\alpha$ in floating point can produce two crossings with the same parameter in the wrong order, or a crossing reported twice on adjacent edges. Exact rational parameters avoid both.
- **The inside test at a crossing vertex.** The flags rely on a correct inside test at the first vertex of each polygon. That vertex must not lie on the other boundary, which general position guarantees.
- **Forgetting the nested case.** With no crossings, the walk produces nothing. One polygon may still contain the other, and the difference $S \setminus C$ is then $S$ with a hole $C$, returned as two rings.
- **Visited flags on both copies.** Each crossing has two nodes. Marking only one of them visited makes the outer loop start a second, duplicate ring from the other copy.

## Implementations

## History

Kevin Weiler and Peter Atherton introduced the idea of walking along the boundaries of two polygons and switching at crossings in 1977, for hidden surface removal. Günther Greiner and Kai Hormann published a simpler and faster version in 1998. It uses doubly linked lists with neighbor links between the two copies of each crossing and entry and exit flags computed from a single inside test. They treated degenerate intersections by perturbing vertices. In 2019 Erich L. Foster, Kai Hormann and Romeo Traian Popa extended the algorithm to degenerate intersections without perturbation.

## References
