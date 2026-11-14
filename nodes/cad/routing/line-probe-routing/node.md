---
tag: CEQKHV
kind: algorithm
slug: line-probe-routing
name: Line-probe routing
aliases:
- Hightower algorithm
- Mikami-Tabuchi algorithm
area: cad/routing
level: core
summary: Routers that grow free horizontal and vertical line segments from both pins until two segments meet. Mikami-Tabuchi always finds a path if one exists; Hightower's faster form may not.
solves: [graph-reachability]
model: word-ram
complexity:
  vars: {M: the number of rows of the routing grid, N: the number of columns}
  time: {worst: Θ(M N)}
  space: {extra: Θ(M N)}
properties: {deterministic: true, recursive: false, exact: false}
history:
  year: 1968
  people: [K. Mikami, K. Tabuchi, D. W. Hightower]
  note: Mikami and Tabuchi presented the line search with all points of each line as new base points at the IFIP Congress in 1968. Hightower gave a faster form with escape points at the Design Automation Workshop in 1969.
prereqs: [lee-maze-routing]
see_also: [lee-maze-routing, hadlock-algorithm, soukup-algorithm, minimum-link-path, breadth-first-search, rectilinear-polygon, visibility-graph, detailed-routing]
sources:
  - paper: "K. Mikami and K. Tabuchi, A computer program for optimal routing of printed circuit conductors, Proceedings of the IFIP Congress 1968, volume 2, North-Holland, 1475 to 1478"
    locator: the lines from the source and the target, the base points of each level and the meeting of the two trees of lines
  - paper: doi:10.1145/800260.809014
    title: D. W. Hightower, A solution to line-routing problems on the continuous plane, Proceedings of the 6th Design Automation Workshop, 1 to 24, 1969
    locator: the escape lines and escape points in the continuous plane (general locator)
  - paper: "C. Y. Lee, An algorithm for path connections and its applications, IRE Transactions on Electronic Computers EC-10(3), 346 to 365, 1961"
    locator: the cell-by-cell wave that line probes replace by whole segments
  - paper: "Naveed A. Sherwani, Algorithms for VLSI Physical Design Automation, 3rd edition, Kluwer, 1999"
    locator: the section on line-probe algorithms in the chapter on maze routing (general locator)
---

Line-probe routing is a family of routers for electronic design automation (EDA) that connect two pins with horizontal and vertical wires by growing whole free line segments instead of single grid cells. From each pin, a probe runs left and right, and up and down, until it hits an obstacle. Points on these lines start new probes at a right angle, level by level, until a line from the source meets a line from the target. In the version of Mikami and Tabuchi (1968) every point of a line is a new base point, so a path is always found if one exists. In Hightower's version (1969) only a few *escape points* start new lines, which is much faster but can miss a path. Neither version promises a shortest path.

## In plain words

Lee's router floods the board square by square. A line-probe router looks along straight lines instead, like a person who stands at a pin and looks as far as possible up, down, left and right.

Do this from both pins. If a line seen from one pin crosses a line seen from the other, you have a wire with a few bends: go along the first line, turn at the crossing, and go along the second.

If the lines do not cross, walk along each line and look again at a right angle from every point on it. Each round adds one more bend. Keep going until two lines cross. If no new lines appear, there is no wire at all.

The wire found has few bends, but it can be longer than the shortest one.

## The problem

The input is a grid of $M$ rows and $N$ columns, where each cell is free or blocked, and two free cells $s$ and $t$. Moves go between free cells that share a side. The output is a path from $s$ to $t$, or the answer that no path exists. Line-probe routers were made for printed circuit boards and for layouts with large obstacles, where a path with few bends and little memory matters more than the exact length. A shortest path is the task of [Lee's algorithm](/lee-maze-routing/).

A *probe* from a free cell $b$ in orientation $o$, horizontal or vertical, gives the maximal run of free cells in the row or column of $b$ that contains $b$. The cell $b$ is its *base point*.

## The algorithm

This is the version of Mikami and Tabuchi, run from both ends.

```pseudo id=main
MIKAMI-TABUCHI(grid, s, t)
L1  for side X in {S, T}: mark the origin (s or t) as covered by X;  todo_X ← [(origin, horizontal), (origin, vertical)]
L2  while todo_S or todo_T is not empty do
L3      for side X in {S, T} do
L4          next_X ← []
L5          for each (b, o) in todo_X do
L6              if X already has a line in orientation o through b then skip it
L7              for each cell c on the probe from b in orientation o do
L8                  if c is not yet covered by X then
L9                      record base_X(c) ← b
L10                     if c is covered by the other side then return the path through c
L11                     add (c, the other orientation) to next_X
L12         todo_X ← next_X
L13 return "no path"
```

The lines drawn in the $i$-th round of line L2 are the lines of *level* $i$. A cell first reached at level $i$ from $s$ is joined to $s$ by a path with at most $i$ bends: follow its line back to the base point, then the line of that base point, and so on. On line L10 the path goes from $s$ to $c$ by the base points of side $S$, and from $c$ to $t$ by those of side $T$. If this walk passes a cell twice, the loop between the two visits is cut out.

## Example

Take a grid of 5 rows and 6 columns, rows and columns numbered from 0, with $s = (2, 0)$ and $t = (2, 5)$.

```
. . . . . .
. # # # # .
s . . . # t
# # # . # .
. . . . . .
```

At level 0, four lines are drawn.

| level | side | base point | orientation | cells |
| --- | --- | --- | --- | --- |
| 0 | S | (2,0) | horizontal | (2,0) to (2,3) |
| 0 | S | (2,0) | vertical | (0,0) to (2,0) |
| 0 | T | (2,5) | horizontal | (2,5) only |
| 0 | T | (2,5) | vertical | (0,5) to (4,5) |
| 1 | S | (2,1) | vertical | (2,1) only |
| 1 | S | (2,2) | vertical | (2,2) only |
| 1 | S | (2,3) | vertical | (2,3) to (4,3) |
| 1 | S | (0,0) | horizontal | (0,0) to (0,5): meets T at (0,5) |

No line of level 0 from $s$ meets a line from $t$. At level 1 the new cells of each line become base points in the other orientation. The vertical lines from $(2, 1)$ and $(2, 2)$ are blocked at once. The vertical line from $(2, 3)$ reaches the bottom row. The horizontal line from $(0, 0)$ runs along the top row and reaches $(0, 5)$, which lies on the vertical line from $t$. The path goes up from $s$ to $(0, 0)$, right to $(0, 5)$ and down to $t$:

$(2,0), (1,0), (0,0), (0,1), \ldots, (0,5), (1,5), (2,5)$,

with 9 steps and 2 bends. Here this is also the length found by [Lee's algorithm](/lee-maze-routing/). The route through the bottom row also has 9 steps but 3 bends.

## Correctness

The [proof](proofs/correctness.md) shows the following.

- **Valid path.** Every cell with a base point is joined to its base point by free cells in one row or column, so following base points gives a path from $s$, and the same from $t$. Cutting loops keeps it a path.
- **Completeness of Mikami-Tabuchi.** The cells covered by one side are closed under free neighbors when no new line appears: a free neighbor of a covered cell lies on the perpendicular line through that cell, which is drawn at the next level. So if no meeting happens, the side of $s$ has covered the whole component of $s$, and $t$ is not in it.
- **Not shortest.** On the grid with rows `...`, `...` and `.#.`, from $s = (2, 2)$ to $t = (2, 0)$, the lines of level 1 go through the top row first, and the path found has 6 steps while 4 suffice.
- **Hightower may fail.** Hightower's rules start new lines only from chosen escape points, so the covered cells need not be closed under free neighbors. The search can then stop without a path even when one exists, as the textbook accounts of the method point out.

## Complexity

- **Time.** A side draws at most one line through each cell in each orientation, by line L6, and a line through a cell is the same maximal run for every base point on it. So each side draws each maximal run at most once, and the total length of all maximal runs is at most $2MN$. The time is $O(MN)$, and a maze that the lines must cover cell by cell gives $\Theta(MN)$.
- **Space.** This implementation keeps a base point for every covered cell, $\Theta(MN)$. Line-probe routers on a gridless layout store only the line segments and the obstacles, which is their main saving over Lee's router.
- **Hightower.** With only a few escape points per line, the number of lines is small, and in the gridless form the time depends on the number of obstacles rather than on the size of a grid.

## Properties

- **What is proved.** Mikami-Tabuchi finds a path whenever one exists. Hightower's version can fail on a grid where a path exists. Neither version promises a shortest path. A cell met at level $i$ from one side has a path to that side with at most $i$ bends.
- **What is measured.** On 16362 random grids with a path from $s$ to $t$ (sizes 2 to 8 on each side, 10 to 40 percent blocked cells, Python `random.Random(47)`), the path of the Mikami-Tabuchi implementation here was longer than the shortest in 347 grids, with a mean ratio of 1.0101 and a worst ratio of 3.0. These are toy inputs, not benchmark results.
- **Deterministic.** The result depends on the order in which lines and cells are taken. The implementation draws side $S$ before side $T$ in each level and takes the cells of a line from left to right or from top to bottom.

## Variants and improvements

- **Hightower's escape points.** From each line, a new line starts only at an escape point: the point of the line from which a perpendicular line can pass the end of the obstacle that blocks the line. This makes the search very fast on boards with few large obstacles, at the cost of completeness.
- **Gridless routing.** The probes do not need a grid. They can run in the plane among rectilinear obstacles, with the lines found by searching the obstacle edges. This is the setting of Hightower's paper.
- **Fewest bends.** A path with the least number of bends among rectilinear obstacles is a [minimum-link path](/minimum-link-path/). Line probes are a heuristic form of that search.
- **Fallback.** A router can run Hightower's search first and fall back to Mikami-Tabuchi or to [Lee's algorithm](/lee-maze-routing/) for the nets it could not route.

## When to use it

- When memory for a label per grid cell is too much, or the layout is gridless, and a path with few bends is wanted.
- On boards or chips with few large obstacles, where a few long lines cover most of the free space.

When the path must be shortest, use [Lee's algorithm](/lee-maze-routing/) or [Hadlock's algorithm](/hadlock-algorithm/). When every existing path must be found, do not use Hightower's form alone.

## Pitfalls

- **Treating Hightower as complete.** Hightower's search can stop with no path. A router that uses it alone must report such nets as unrouted and retry them with a complete search.
- **Claiming a shortest path.** The level structure counts bends, not steps. The first meeting can be a long way round.
- **Drawing a line twice.** Without the test of line L6, every cell of a long run starts the same line again, and the time grows by a factor of the run length.
- **Loops in the path.** The walk back by base points from both sides can pass the same cell twice. Cut out the loop, or the path is not simple.

## Implementations

## History

K. Mikami and K. Tabuchi presented their line search at the IFIP Congress in 1968 for the routing of printed circuit conductors. D. W. Hightower presented his line-routing method at the 6th Design Automation Workshop in 1969. His method works in the continuous plane and uses escape points to keep the number of lines small. Both methods came after Lee's grid router of 1961 and use much less memory than a label for every cell. Later routers combined line probes with maze search, using the probes for long open runs and the grid search where the layout is crowded.

## References
