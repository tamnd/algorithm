---
tag: 1ZY6ZC
kind: algorithm
slug: theta-star
name: "Theta*"
aliases:
- Theta star
- any-angle path planning
area: games-and-search/heuristic-search
level: advanced
summary: "A* on the corners of a grid that connects each new corner straight to the parent of its predecessor when the segment is free. Paths turn at any angle and are short, but not always optimal."
solves: [euclidean-shortest-path]
model: word-ram
complexity:
  vars: {n: the number of corners of the grid, k: the width plus the height of the grid}
  time: {worst: O(n log n + n k)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false}
prereqs: [a-star-search, bresenham-line-algorithm]
see_also: [visibility-graph, euclidean-shortest-path, jump-point-search, hierarchical-pathfinding-a-star, motion-planning, d-star-lite]
sources:
  - paper: "Alex Nash, Kenny Daniel, Sven Koenig and Ariel Felner, Theta*: any-angle path planning on grids, AAAI 2007"
    title: "Theta*: any-angle path planning on grids (AAAI 2007)"
    locator: pp. 1177 to 1183; the pseudocode of basic Theta* with path 1 and path 2, and the experiments against A* and Field D*
  - paper: doi:10.1613/jair.2994
    title: "Kenny Daniel, Alex Nash, Sven Koenig and Ariel Felner, Theta*: any-angle path planning on grids, Journal of Artificial Intelligence Research 39 (2010)"
    locator: pp. 533 to 579; basic Theta*, its line of sight test, angle-propagation Theta*, the properties of the paths, and the experiments
  - paper: doi:10.1613/jair.5007
    title: "Daniel Harabor, Alban Grastien, Dindar Öz and Vural Aksakalli, Optimal any-angle pathfinding in practice, Journal of Artificial Intelligence Research 56 (2016)"
    locator: pp. 89 to 118; Anya, which finds shortest any-angle paths on grids
---

Theta* is a version of [A*](/a-star-search/) that finds paths on a grid whose segments may go at any angle, not only along the 8 grid directions. It searches the corners of the cells like A* on a grid. When it reaches a corner $y$ from a corner $x$, it first checks whether the parent of $x$ can see $y$ in a straight line, and if so it makes that parent the parent of $y$. So the path cuts across open space instead of following the zigzag of the grid. Alex Nash, Kenny Daniel, Sven Koenig and Ariel Felner introduced it in 2007. Its paths are never longer than the shortest grid path, but they are not always the shortest paths in the plane.

## In plain words

A path on a grid can only go straight or at 45 degrees, so it often makes small detours and needless turns. A person on a field would walk straight to the next corner of an obstacle.

Theta* works like A* on the grid, with one extra check. Each time it extends a path by one step, it asks whether the point before this step can see the new point directly. If it can, the step in the middle is cut out, and the path goes straight. After the search, the path has few turns, and each turn is at the corner of an obstacle or close to one.

## The problem

The input is a grid of free and blocked square cells, a start corner $s$ and a goal corner $t$. The obstacle is the interior of the union of the blocked cells, and the outside of the map counts as blocked. Two corners *see* each other if the segment between them does not meet the obstacle. So a segment may run along the side of a blocked cell, and it may pass through a corner where two blocked cells touch at a point. The task is a short path from $s$ to $t$ made of segments between corners that see each other, with the Euclidean length as the cost.

The shortest such path is a [Euclidean shortest path](/euclidean-shortest-path/) around the obstacles, and its corners are corners of obstacles, so a [visibility graph](/visibility-graph/) of the corners gives the optimum. The *grid path* is the shortest path in the graph that joins each corner to the 8 corners around it that it sees; A* on the grid finds it. Theta* is between the two: no longer than the grid path, and no shorter than the optimum.

## The algorithm

The heuristic is the straight-line distance $h(x) = |x t|$.

```pseudo id=main
THETA*(s, t)
L1  g(s) ← 0, parent(s) ← s, open ← {s}, closed ← ∅
L2  while open is not empty do
L3      take x with the least g(x) + h(x) from open, add x to closed
L4      if x = t then return the corners on the parent chain of t
L5      for each of the 8 corners y around x that x sees, with y ∉ closed do
L6          p ← parent(x)
L7          if LINE-OF-SIGHT(p, y) then
L8              if g(p) + |p y| < g(y) then g(y) ← g(p) + |p y|, parent(y) ← p, put y in open
L9          else if g(x) + |x y| < g(y) then g(y) ← g(x) + |x y|, parent(y) ← x, put y in open
L10 return no path
LINE-OF-SIGHT(a, b)
L11 if a and b are on one grid line then return true if no unit edge between them has blocked cells on both sides
L12 for each column strip i ≤ x ≤ i + 1 between a and b do
L13     for each row j whose open interval meets the y-range of the segment over the strip do
L14         if cell (i, j) is blocked then return false
L15 return true
```

Line L8 is *path 2*, the straight segment from the parent of $x$. Line L9 is *path 1*, the ordinary A* step. The line of sight test of the paper walks the cells along the segment with integer steps, like the [Bresenham line algorithm](/bresenham-line-algorithm/). The test here does the same with exact integer floor and ceiling, one column strip at a time. Corner cases matter: the rules for a segment that touches a blocked cell or passes between two blocked cells decide which paths are legal, and the grid A* that Theta* is compared with must use the same rules.

## Example

The grid has 5 columns and 2 rows of cells, so its corners are $(x, y)$ with $0 \le x \le 5$ and $0 \le y \le 2$, with $y$ counted down. The cells $(4, 0)$, $(0, 1)$ and $(2, 1)$ are blocked. The start is the top left corner $s = (0, 0)$ and the goal is the bottom right corner $t = (5, 2)$.

```
row 0  . . . . #
row 1  # . # . .
```

| step | corner expanded | parent | $g$ | $g + h$ | what happens |
| --- | --- | --- | --- | --- | --- |
| 1 | $(0, 0)$ | itself | $0$ | $5.385$ | its 3 free neighbours get parent $s$ |
| 2 | $(1, 0)$ | $(0, 0)$ | $1$ | $5.472$ | $(2, 1)$ gets parent $s$ by path 2, $g = \sqrt 5$ |
| 3 | $(2, 1)$ | $(0, 0)$ | $2.236$ | $5.398$ | $(3, 1)$ gets parent $s$, $g = \sqrt{10}$ |
| 4 | $(3, 1)$ | $(0, 0)$ | $3.162$ | $5.398$ | $(4, 1)$ gets parent $s$, $g = \sqrt{17}$; $(4, 2)$ gets parent $(3, 1)$, $g + h = 5.576$ |
| 5 | $(1, 1)$ | $(0, 0)$ | $1.414$ | $5.537$ | nothing better |
| 6 | $(4, 1)$ | $(0, 0)$ | $4.123$ | $5.537$ | $s$ cannot see $t$, so $t$ gets parent $(4, 1)$ by path 1 |
| 7 | $(5, 2)$ | $(4, 1)$ | $5.537$ | $5.537$ | the goal |

Theta* returns the path $(0, 0), (4, 1), (5, 2)$ of length $\sqrt{17} + \sqrt 2 \approx 5.537$. The grid path has length $3 + 2\sqrt 2 \approx 5.828$, so Theta* is shorter. But the shortest path in the plane is $(0, 0), (3, 1), (5, 2)$, of length $\sqrt{10} + \sqrt 5 \approx 5.398$. Theta* would find it through $(4, 2)$, whose parent is $(3, 1)$, but $(4, 2)$ has $g + h = 5.576$, and the goal is taken first, at $5.537$. So Theta* is not optimal here, whatever the tie rule.

**A measured experiment.** On 40 random 10 by 10 grids (each cell blocked with probability 0.2, random start and goal corners that are connected, `random.Random(9)` of Python), the Theta* paths had a total length of 233.111, the grid paths 242.551 and the shortest paths in the plane 232.779. Theta* was strictly shorter than the grid path on 27 maps and equal on 13, and it was optimal on 38 of the 40. These are measurements on these grids, not bounds.

## Correctness

The [proof](proofs/correctness.md) shows the following.

- **Line of sight is exact.** LINE-OF-SIGHT lists exactly the cells whose interior the segment meets, so it accepts exactly the segments that do not meet the obstacle.
- **The path is valid.** Each parent sees its child, and $g$ of a corner is $g$ of its parent plus the length of the segment. So the parent chain of $t$ is a path of segments with line of sight, of length $g(t)$.
- **No longer than the grid path.** Path 2 is never worse than path 1, by the triangle inequality. With this, the usual A* argument with a consistent heuristic shows that each corner leaves the open list with $g$ at most its distance in the grid graph. So the result is no longer than the path of A* on the grid with the same rules.
- **Complete.** If the goal can be reached in the grid graph, Theta* returns a path. If not, it returns none.

The returned path is not always a shortest path in the plane, as the example shows. Theta* only tries the parent of the predecessor as a shortcut, so it cannot turn at a corner that was not on a good parent chain when it was needed.

## Complexity

The model is the [word RAM](/word-ram/). Let $n$ be the number of corners and $k$ the width plus the height of the grid. Each corner is expanded at most once, and an expansion looks at 8 neighbours and makes up to 2 line of sight tests each. A test visits $O(k)$ cells. The heap operations cost $O(\log n)$ each. So the time is $O(n \log n + n k)$ in the worst case, and the space is $O(n)$. In practice most line of sight tests are short, but they make Theta* slower per expansion than A* on the grid.

## Properties

- **Any-angle paths** made of segments between corners.
- **No longer than the grid path** of A* on the 8-connected corner graph with the same line of sight rules.
- **Not optimal** in the plane: the path can be longer than the shortest path around the obstacles.
- **Complete** on finite grids.
- **No preprocessing.** It works on the grid as it is.

## Variants and improvements

- **Lazy Theta*** (Nash, Koenig and Tovey 2010) assumes that path 2 is free and checks line of sight only when a corner is expanded, which saves many tests.
- **Angle-propagation Theta*** (in the 2010 journal paper) keeps a range of angles for each corner, so that a line of sight test takes constant amortized time. Its paths are a little longer than those of basic Theta*.
- **Field D*** (Ferguson and Stentz) interpolates the costs along the edges of the cells and can work with different costs per cell. Theta* compares well with it in the experiments of the Theta* papers.
- **Anya** (Harabor, Grastien, Öz and Aksakalli 2016) searches intervals of points on the rows of the grid and returns shortest any-angle paths, without preprocessing.
- **Visibility graphs.** A [visibility graph](/visibility-graph/) of the obstacle corners gives the optimum too, but it has up to quadratic size and must be built first.

## When to use it

Use Theta* when units in a game or robots on a grid map should move along short, natural-looking paths with few turns, and the exact optimum does not matter. For the optimum on a grid, use Anya or a [visibility graph](/visibility-graph/). For paths along the grid, use A* or [jump point search](/jump-point-search/). For big maps where speed matters more than path quality, use a hierarchy such as [HPA*](/hierarchical-pathfinding-a-star/). If the map changes while the robot moves, incremental versions of Theta* exist, and [D* Lite](/d-star-lite/) covers the grid case.

## Pitfalls

- **Calling it optimal.** Theta* is not optimal in the plane. Use Anya or a visibility graph when the optimum is needed.
- **Mixed rules.** The line of sight test and the grid moves must use the same rules for touching corners and for squeezing between blocked cells. If they do not, a path can pass where the grid search could not go.
- **Inexact line of sight.** A test that uses floating point steps can miss a cell that the segment just touches, or block a segment that only touches a corner.
- **Post-smoothing is not the same.** Smoothing an A* path afterwards only removes corners of that path. Theta* considers shortcuts during the search and usually finds shorter paths.

## Implementations

## History

Nash, Daniel, Koenig and Felner introduced Theta* at AAAI 2007, as a simple way to get any-angle paths from A* on grids, and they compared it with A* followed by post-smoothing and with Field D*. Daniel, Nash, Koenig and Felner gave the journal version in 2010, with angle-propagation Theta* and an analysis of the paths. Nash, Koenig and Tovey gave Lazy Theta* in 2010. Harabor, Grastien, Öz and Aksakalli gave the optimal method Anya in 2016.

## References
