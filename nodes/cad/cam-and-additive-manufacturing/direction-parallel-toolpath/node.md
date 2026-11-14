---
tag: ZR545D
kind: algorithm
slug: direction-parallel-toolpath
name: Direction-parallel toolpath
aliases:
- zigzag toolpath
- raster toolpath
area: cad/cam-and-additive-manufacturing
level: core
summary: Covers a region with parallel line passes clipped to its boundary and joined end to end, simple and used for pocketing and infill.
solves: [pocket-machining]
model: real-ram
complexity:
  vars: {n: number of edges of the tool-center region, K: number of pass lines, I: number of intervals on the pass lines}
  time: {worst: "O(K n log n + I n^3)"}
  space: {extra: "O(n + I)"}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1991
  people: [Martin Held]
  note: Zigzag milling is as old as NC pocketing. Held's 1991 monograph gave its computational geometry, and Arkin, Held and Smith proved that minimizing the retractions of a zigzag path is NP-hard for pockets with holes.
prereqs: [pocket-machining, scanline-polygon-fill, point-in-polygon]
see_also: [contour-parallel-toolpath, infill-pattern, coverage-path-planning, boustrophedon-cell-decomposition, polygon-with-holes, even-odd-fill-rule, minkowski-sum, scallop-height]
sources:
  - book: isbn:978-3-540-54103-5
    title: Martin Held, On the Computational Geometry of Pocket Machining, Lecture Notes in Computer Science 500, Springer, 1991
    locator: the chapters on direction-parallel machining, the machining graph of the zigzag intervals and its traversal
  - paper: doi:10.1007/s004539910010
    title: Esther M. Arkin, Martin Held and Christopher L. Smith, Optimization problems related to zigzag pocket machining, Algorithmica 26(2), 197-236, 2000
    locator: the NP-hardness of minimizing retractions for pockets with holes, and the linear-time method with at most 5 OPT + 6h retractions
  - paper: doi:10.1016/S0010-4485(99)00080-9
    title: Sang C. Park and Byoung K. Choi, Tool-path planning for direction-parallel area milling, Computer-Aided Design 32(1), 17-25, 2000
    locator: the choice of the pass direction and the linking of the zigzag passes into few tool paths
---

A direction-parallel toolpath clears a [pocket](/pocket-machining/) by moving the tool center along parallel straight passes, all in one direction, each clipped to the region where the tool center may go. Neighbouring passes are joined end to end, so the tool runs back and forth in a zigzag, and a last pass runs once around the boundary. This is a manufacturing method of mechanical CAD: placement and routing here mean where a milling tool goes and how it moves, not the placement and routing of a circuit. The same pattern, with the tool replaced by a nozzle, is a common [infill pattern](/infill-pattern/) of additive manufacturing. The page proves that with a step-over of at most twice the tool radius, the passes and the boundary pass cut everything that the tool can reach. The code builds the path with exact rational geometry for a polygon with holes.

## In plain words

Think of mowing a lawn in straight strips. You mow one strip from left to right, step up by a little less than the blade width, and mow the next strip from right to left. The strips cover the lawn if the gap between them is never more than the blade width.

A lawn with a pond or a flower bed in the middle breaks some strips into two pieces. You then cannot mow all the pieces in one long zigzag. You lift the mower, carry it to the next piece and start again. Each lift costs time, so a good plan lifts as few times as it can.

Some grass stays where the fence makes a narrow nook that no strip enters. One last lap along the fence and around every flower bed takes it out.

## The problem

The tool is a disk of radius $r$ in the plane. The region $C$ is the set of positions of the tool center that keep the tool inside the pocket, which for a pocket $P$ is the inward offset by $r$. The code takes $C$ as given, a closed [polygon with holes](/polygon-with-holes/) under the [even-odd rule](/even-odd-fill-rule/), as when a CAM system has already computed the offset. A path $\Gamma \subseteq C$ cuts the set $\Gamma \oplus D_r$, the [Minkowski sum](/minkowski-sum/) of the path and the disk. No path in $C$ cuts more than $C \oplus D_r$, so the goal is to cut all of $C \oplus D_r$ with few retractions and a short path.

The passes lie on the lines $y_k = y_{\min} + s/2 + ks$ for $k = 0, 1, \dots$ while $y_k < y_{\max}$, where $s$ is the step-over. Each line meets $C$ in a set of closed intervals, which the code finds with the half-open crossing rule of [scanline polygon fill](/scanline-polygon-fill/).

## The algorithm

```pseudo id=main
DIRECTION-PARALLEL(C, s)
L1  for each pass line y_k: I_k ← the intervals of C on y = y_k
L2  while some interval is unused do
L3      start a stroke at the left end of the lowest unused interval
L4      loop
L5          cut the current interval to its other end and mark it used
L6          J ← unused intervals on the next line whose end on the same side links to here by a segment in C
L7          if J is empty then exit the loop              ▷ the tool retracts
L8          link to the nearest member of J, which becomes the current interval
L9  add one stroke around each boundary ring of C
L10 return the strokes
```

Line L6 tests each link with an exact segment-in-region test. The test cuts the segment at every point where it meets an edge of $C$, including the ends of collinear overlaps, and checks the midpoint of each piece with a closed [point-in-polygon](/point-in-polygon/) test. A link that would cross a hole or a notch of $C$ is refused, and the stroke ends there.

The strokes after the first one start with a retraction: the tool lifts, moves fast above the part, and plunges at the start of the next stroke.

## Example

Take the U-shaped tool-center region $C$ with vertices $(0, 0)$, $(10, 0)$, $(10, 8)$, $(7, 8)$, $(7, 4)$, $(3, 4)$, $(3, 8)$, $(0, 8)$, a tool of radius $r = 1$ and a step-over $s = 2$. The pass lines are $y = 1, 3, 5, 7$. The lines $y = 1$ and $y = 3$ meet $C$ in $[0, 10]$, and the lines $y = 5$ and $y = 7$ meet it in $[0, 3]$ and $[7, 10]$.

| step | stroke | moves | length |
|---|---|---|---|
| L3 to L8 | 1 | $(0, 1) \to (10, 1) \to (10, 3) \to (0, 3) \to (0, 5) \to (3, 5) \to (3, 7) \to (0, 7)$ | 32 |
| L7 | | no unused interval on $y = 9$: retract | |
| L3 to L8 | 2 | $(7, 5) \to (10, 5) \to (10, 7) \to (7, 7)$ | 8 |
| L9 | 3 | once around the boundary of $C$ | 44 |

The tool cuts along 84 units of path, with two retractions. At $y = 5$ the first stroke ends at $(3, 5)$. The interval $[7, 10]$ on the same line is not on the next line, so the zigzag can reach it only through a retraction. Every point of $C$ is within $s/2 = 1$ of the path, and the cut region is the U grown by 1 on every side, with its six convex corners rounded to radius 1.

## Correctness

**Theorem.** DIRECTION-PARALLEL stops, it cuts each interval exactly once, and its path lies in $C$. If $s \le 2r$, every point of $C$ is within $s/2$ of the path, and the path cuts exactly $C \oplus D_r$.

The intervals lie in $C$ by the parity of the half-open rule, the links lie in $C$ by the exact segment test, and the boundary pass lies on $\partial C$. For the coverage, take a point $p$ of $C$ between two pass lines and walk straight up and straight down from it. Each walk stops at the first point that is on the boundary of $C$ or on a pass line, and both kinds of points are on the path. The two walks add up to at most the gap $s$ between the lines, so one of them is at most $s/2 \le r$. A point outside $C$ that is within $r$ of $C$ is within $r$ of a boundary point, which is on the path. The full proof is in the proof file.

The boundary pass is needed. A thin tongue of $C$ that lies between two pass lines and meets neither gets no cut from the zigzag, and the tests show such a case.

## Complexity

Line L1 finds the crossings of each of the $K$ lines with the $n$ edges and sorts them, in $O(K n \log n)$ time. Let $I$ be the number of intervals. Each pass of lines L5 to L8 tests at most $n$ candidates, and each exact segment test cuts the segment into $O(n)$ pieces and runs an $O(n)$ point test on each, so it costs $O(n^2)$. The linking takes $O(I n^3)$ time in this simple code, and much less in practice, where few candidates exist. A sweep that builds the machining graph of the intervals and their neighbours, as in Held (1991), does the linking in time close to linear in $n + I$. The extra space is $O(n + I)$.

The number of pass lines is about $(y_{\max} - y_{\min})/s$, so halving the step-over doubles the path length.

## Properties

- **Straight passes.** Most of the path is straight, at a constant feed in one direction, which a machine can run fast.
- **Mixed milling direction.** A zigzag alternates between climb milling and conventional milling from one pass to the next. A one-way raster cuts every pass in the same direction and returns over the part between passes, at the cost of more air moves.
- **Each interval once.** No interval is cut twice, so the path length is the total length of the intervals plus the links and the boundary pass.
- **Retractions.** The number of strokes depends on the shape and on the pass direction. For a pocket with holes, minimizing the number of retractions of a zigzag path is NP-hard (Arkin, Held and Smith, 2000).
- **Exact.** With rational vertices and step-over, every crossing, interval end and link test of the code is exact.

## Variants and improvements

- **Fewer retractions.** Arkin, Held and Smith gave a linear-time method that uses at most $5\,\mathrm{OPT} + 6h$ retractions on a pocket with $h$ holes, where OPT is the minimum for the given machining graph. Later work gives an optimal linear-time method for pockets without holes.
- **Choice of direction.** The direction of the passes changes the number of intervals and retractions. Park and Choi (2000) choose the direction and the links to get few tool paths. A good default runs the passes along the longest side.
- **Cell decomposition.** Cutting $C$ into cells, each of which one zigzag covers, is the [boustrophedon cell decomposition](/boustrophedon-cell-decomposition/) of robot [coverage path planning](/coverage-path-planning/).
- **Zigzag with contour.** Most CAM systems combine a zigzag for the interior with one or more [contour-parallel](/contour-parallel-toolpath/) passes along the walls, as here.
- **Surfaces.** On a curved surface, the passes become the cuts of the surface by parallel planes. See [iso-planar toolpath](/iso-planar-toolpath/).

## When to use it

Use a direction-parallel path for wide, open pockets and for roughing, where long straight passes are fast and the milling direction matters less. Use a contour-parallel path when the walls need a good finish, when the pocket has many thin features that would break the passes into many intervals, or when the tool must cut in one milling direction.

## Pitfalls

- **No boundary pass.** Without the last pass along the walls, thin tongues and the material between the ends of the passes and the wall stay uncut.
- **Step-over above twice the radius.** With $s > 2r$, the middle strip between two passes is more than $r$ from both. In a $10 \times 10$ square with $s = 3$ and $r = 1$, the passes are at $y = 1.5, 4.5, 7.5$, and the point $(5, 3)$ is $1.5$ from both neighbouring passes.
- **Links across holes.** A link drawn straight from one pass to the next can cross an island or a notch and cut the part. Each link must be tested against the region, or run along the boundary.
- **Vertices on a pass line.** A pass line through a vertex counts that vertex once, twice or not at all, depending on the rule. Without the half-open rule, an interval can start at a wrong place or the parity can flip. See [scanline polygon fill](/scanline-polygon-fill/).
- **Floor finish.** For a flat end mill on a flat floor, any $s < 2r$ leaves a flat floor. For a ball end mill on a curved surface, the step-over leaves ridges between passes. See [scallop height](/scallop-height/).

## Implementations

## History

Zigzag paths were among the first pocketing paths of numerical control, because they need only line intersections. Held (1991) treated direction-parallel and contour-parallel pocket machining in one computational geometry framework, with the machining graph of the zigzag intervals. Arkin, Held and Smith (extended abstract 1996, journal 2000) proved that minimizing retractions is NP-hard for pockets with holes, and gave the approximation bound.

## References
