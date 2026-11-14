---
tag: Q7C4F1
kind: algorithm
slug: hadlock-algorithm
name: Hadlock's algorithm
aliases:
- minimum detour routing
area: cad/routing
level: core
summary: A maze router that orders the search by detour number, the steps away from the target. It finds shortest paths and usually expands fewer cells than Lee's router.
solves: [single-pair-shortest-path]
model: word-ram
complexity:
  vars: {M: the number of rows of the routing grid, N: the number of columns}
  time: {worst: Θ(M N), best: Θ(1)}
  space: {extra: Θ(M N)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1977
  people: [F. O. Hadlock]
  note: Hadlock published the minimum detour search for grid graphs in the journal Networks in 1977, as a faster form of Lee's router.
prereqs: [lee-maze-routing, zero-one-bfs]
see_also: [lee-maze-routing, soukup-algorithm, line-probe-routing, a-star-search, consistent-heuristic, zero-one-bfs, dijkstra, detailed-routing]
sources:
  - paper: doi:10.1002/net.3230070404
    title: F. O. Hadlock, A shortest path algorithm for grid graphs, Networks 7(4), 323 to 334, 1977
    locator: the detour number, the identity of path length with the Manhattan distance plus twice the detours, and the search in order of detour number
  - paper: "C. Y. Lee, An algorithm for path connections and its applications, IRE Transactions on Electronic Computers EC-10(3), 346 to 365, 1961"
    locator: the wave expansion and backtrace that Hadlock's search replaces
  - paper: doi:10.1109/TSSC.1968.300136
    title: P. E. Hart, N. J. Nilsson and B. Raphael, A formal basis for the heuristic determination of minimum cost paths, IEEE Transactions on Systems Science and Cybernetics 4(2), 100 to 107, 1968
    locator: the A* search, of which Hadlock's search is the case of unit steps and the Manhattan heuristic
  - paper: "Naveed A. Sherwani, Algorithms for VLSI Physical Design Automation, 3rd edition, Kluwer, 1999"
    locator: the section on Hadlock's algorithm in the chapter on maze routing (general locator)
---

Hadlock's algorithm is a maze router for electronic design automation (EDA) that finds a shortest path between two cells of a routing grid, like [Lee's algorithm](/lee-maze-routing/), but aims the search at the target. It labels each cell with its *detour number*, the least number of steps away from the target on a path from the source, and expands the cells in order of this number. The length of a path is the Manhattan distance between its ends plus twice its detours, so the path with the fewest detours is a shortest path. The search is [A* search](/a-star-search/) with the Manhattan distance as the heuristic, and on an open grid it expands far fewer cells than Lee's wave.

## In plain words

Lee's router spreads out in all directions like a ring of water. Hadlock's router walks toward the goal as long as it can, and it only counts the steps that go the wrong way.

Each step either brings you one square nearer to the goal or takes you one square farther away. A step that takes you away is a detour. Every detour must be paid back later with one more step toward the goal. So a wire with $d$ detours is longer than the straight distance by exactly $2d$ squares.

The router first tries all squares it can reach with no detour. Then it tries those it can reach with one detour, then two, and so on. The first time it reaches the goal, it has used the fewest detours, so it has found a shortest wire.

## The problem

The input is a grid of $M$ rows and $N$ columns, where each cell is free or blocked, and two free cells $s$ and $t$. Moves go between free cells that share a side. The output is a shortest path from $s$ to $t$, or the answer that no path exists. This is the problem of [Lee's algorithm](/lee-maze-routing/).

For cells $u$ and $v$ let $\mathrm{md}(u, v) = |u_r - v_r| + |u_c - v_c|$ be the Manhattan distance between their row and column numbers. A step from $u$ to a neighbor $v$ is *toward* $t$ if $\mathrm{md}(v, t) = \mathrm{md}(u, t) - 1$, and a *detour* if $\mathrm{md}(v, t) = \mathrm{md}(u, t) + 1$. There is no third case. The *detour number* $\mathrm{det}(v)$ is the least number of detours on a path from $s$ to $v$.

## The algorithm

```pseudo id=main
HADLOCK(grid, s, t)
L1  det(s) ← 0;  deque ← [s];  done ← ∅
L2  while deque is not empty do
L3      u ← remove the first cell of deque
L4      if u ∈ done then continue
L5      add u to done
L6      if u = t then return the path from s to t by the parent links
L7      for each free neighbor v of u with v ∉ done do
L8          a ← 1 if md(v, t) > md(u, t), else 0
L9          if v has no label or det(u) + a < det(v) then
L10             det(v) ← det(u) + a;  parent(v) ← u
L11             if a = 0 then add v at the front of deque else add v at the back
L12 return "no path"
```

Line L11 is a [0-1 BFS](/zero-one-bfs/): a step toward the target costs 0 and goes to the front, a detour costs 1 and goes to the back. So the cells leave the deque in order of their detour number. Hadlock described the same order with a list of cells for each detour number.

## Example

Take the grid of the [Lee example](/lee-maze-routing/), with $s = (2, 0)$ and $t = (2, 4)$, so $\mathrm{md}(s, t) = 4$. The second grid shows the detour labels when the search stops. A `-` is a free cell that never got a label.

```
. . . . .        2 2 2 2 2
. # # # .        1 # # # 2
s . . # t        0 0 0 # 2
# . # . .        # 1 # - -
. . . . .        - 2 - - -
```

The search expands the cells in this order:

| detour number | cells expanded |
| --- | --- |
| 0 | (2,0), (2,1), (2,2) |
| 1 | (1,0), (3,1) |
| 2 | (0,0), (0,1), (0,2), (0,3), (0,4), (1,4), (2,4) |

From $s$ the search goes right with no detour until the wall at $(2, 3)$. The cells $(1, 0)$ and $(3, 1)$ cost one detour each, because they are one row away from the row of $t$. From $(1, 0)$ the step up to $(0, 0)$ is a second detour. Then every step along the top row and down the right column goes toward $t$, so these cells go to the front of the deque, and the search reaches $t$ with $\mathrm{det}(t) = 2$. The path is

$(2,0), (1,0), (0,0), (0,1), (0,2), (0,3), (0,4), (1,4), (2,4)$,

with length $4 + 2 \cdot 2 = 8$, the same as Lee's. Hadlock expanded 12 cells. Lee's wave labeled all 19 free cells.

## Correctness

The [proof](proofs/correctness.md) shows the following.

- **Length identity.** A path from $s$ to a cell $v$ with $D$ detours has length $\mathrm{md}(s, t) - \mathrm{md}(v, t) + 2D$. For $v = t$ this is $\mathrm{md}(s, t) + 2D$, so fewer detours means a shorter path.
- **Detour labels.** The deque holds labels of two consecutive values, sorted from front to back. So each cell is expanded first with its true detour number, as in [Dijkstra's algorithm](/dijkstra/) with costs 0 and 1.
- **Shortest path.** When $t$ is expanded, its label is $\mathrm{det}(t)$, and the parent links give a path with this many detours, which by the identity is a shortest path.
- **A* view.** For a path of length $g$ to $v$, $g + \mathrm{md}(v, t) = \mathrm{md}(s, t) + 2D$. So the order by detour number is the order of [A* search](/a-star-search/) with the [consistent heuristic](/consistent-heuristic/) $\mathrm{md}(v, t)$.
- **Completeness.** If the deque empties before $t$ is expanded, every cell reachable from $s$ was expanded, so no path exists.

## Complexity

- **Time.** Lines L4 and L5 expand each cell at most once, and each expansion adds at most 4 entries to the deque. So there are at most $4MN + 1$ entries, and the time is $O(MN)$. In the worst case, a maze that forces a long winding path, the search expands every cell, so the bound is $\Theta(MN)$.
- **Space.** Labels, parents and the deque take $\Theta(MN)$ memory. The detour numbers need fewer bits than Lee's distances in practice, but they still grow with the grid.
- **Open grid.** With no blockage between $s$ and $t$, every cell on a monotone path has detour number 0, and the search walks straight to $t$, expanding about $\mathrm{md}(s, t)$ cells in our implementation, against about $2L^2$ for Lee's wave.

## Properties

- **What is proved.** Hadlock's algorithm finds a shortest path whenever a path exists, and among the shortest paths it finds one with the fewest detours, which is the same thing. Every cell it expands has $\delta(s, v) + \mathrm{md}(v, t) \le L$, where $L$ is the length of the shortest path, so every cell it expands is also labeled by Lee's wave.
- **What is measured.** The inclusion above is about expanded cells. Hadlock also writes labels on the neighbors of expanded cells, and these can be more than the cells Lee labels. On 16386 random grids with a path from $s$ to $t$ (sizes 2 to 8 on each side, 10 to 40 percent blocked cells, Python `random.Random(41)`), Hadlock expanded fewer cells than Lee labeled in 15306 grids and never more, but it labeled more cells than Lee in 517 grids. These are toy inputs, not benchmark results.
- **Exact and deterministic.** The front and back rule of line L11 fixes the order. Among cells of the same detour number, the most recent toward step is followed first, so the search runs straight on when it can.
- **One net at a time.** As with Lee's router, the result is shortest for this net only, given the wires already placed.

## Variants and improvements

- **Bucket lists.** Hadlock kept a list of cells for each detour number. The deque of line L11 is the same idea with two lists, because labels in the deque differ by at most 1.
- **Weighted grids.** With costs for vias, bends or congestion, the same aim at the target is [A* search](/a-star-search/) with the Manhattan distance times the least step cost as the heuristic.
- **Bidirectional search.** Run detour searches from both ends, each aimed at the other end.
- **Soukup's search.** [Soukup's algorithm](/soukup-algorithm/) goes depth first toward the target and does not keep detour numbers. It is faster, but its path need not be shortest.

## When to use it

- To find a shortest path for a two-pin net on a grid that is large and mostly open, where Lee's wave would label many cells far from the target.
- As the search step of a rip-up and reroute loop with unit costs.

With costs that are not uniform, use A* or [Dijkstra's algorithm](/dijkstra/) directly. When the grid is small, plain [Lee's algorithm](/lee-maze-routing/) is simpler and just as fast.

## Pitfalls

- **Detour from the source.** The detour is measured against the target $t$, not against $s$. A step that goes away from $s$ but toward $t$ costs nothing.
- **Front and back mixed up.** A toward step must go to the front and a detour to the back. The other way round, the cells leave in the wrong order and the path need not be shortest.
- **Stopping when $t$ is labeled.** The search must stop when $t$ is expanded, not when it first gets a label. A first label can come through a detour, and a later toward step can lower it.
- **Old entries.** A cell can be in the deque twice after its label falls. Line L4 skips the copies of cells that are already done.

## Implementations

## History

F. O. Hadlock published the algorithm in 1977 in the journal Networks, under the title "A shortest path algorithm for grid graphs". He observed that on a grid the length of a path equals the Manhattan distance plus twice the number of steps away from the target, so the search can be ordered by this number instead of by distance. The same order follows from the A* search of Hart, Nilsson and Raphael (1968) with the Manhattan distance as the heuristic. Together with Lee's wave, Soukup's search (1978) and the line-probe routers, it became a standard maze router in textbooks of physical design.

## References
