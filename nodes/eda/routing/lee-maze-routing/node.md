---
tag: EQ37HH
kind: algorithm
slug: lee-maze-routing
name: Lee's maze routing algorithm
aliases:
- Lee algorithm
- wave propagation routing
area: eda/routing
level: intro
summary: Lee's router expands a wave of grid cells from the source by breadth-first search until it reaches the target, then traces back a shortest path.
solves: [single-pair-shortest-path]
model: word-ram
complexity:
  vars: {M: the number of rows of the routing grid, N: the number of columns}
  time: {worst: Θ(M N), best: Θ(1)}
  space: {extra: Θ(M N)}
properties: {deterministic: true, recursive: false, exact: true}
history:
  year: 1961
  people: [C. Y. Lee]
  note: Lee published the wave expansion and backtrace for wiring on a grid in the IRE Transactions on Electronic Computers in 1961. Moore had given the same breadth-first idea for mazes in 1959.
prereqs: [breadth-first-search]
see_also: [breadth-first-search, flood-fill, hadlock-algorithm, soukup-algorithm, line-probe-routing, a-star-search, detailed-routing, rip-up-and-reroute]
sources:
  - paper: "C. Y. Lee, An algorithm for path connections and its applications, IRE Transactions on Electronic Computers EC-10(3), 346 to 365, 1961"
    locator: the wave expansion from the source, the labels by distance and the backtrace from the target
  - paper: "E. F. Moore, The shortest path through a maze, Proceedings of the International Symposium on the Theory of Switching, Part II, Harvard University Press, 285 to 292, 1959"
    locator: the breadth-first labeling of a maze by distance from the start (general locator, not checked against the text)
  - paper: "S. B. Akers, A modification of Lee's path connection algorithm, IEEE Transactions on Electronic Computers EC-16, 97 to 98, 1967"
    locator: the labeling of cells with the repeating sequence 0, 0, 1, 1, which needs two bits per cell
  - paper: "Naveed A. Sherwani, Algorithms for VLSI Physical Design Automation, 3rd edition, Kluwer, 1999"
    locator: the chapter on maze routing (general locator)
---

Lee's algorithm is a maze router for electronic design automation (EDA): it connects two cells of a routing grid by a path that avoids blocked cells and has the fewest steps. It is a [breadth-first search](/breadth-first-search/) on the grid graph. A *wave* of labels grows out from the source, one step at a time, until it reaches the target. A *backtrace* then walks from the target to the source through labels that fall by 1 at each step. If a path exists, the algorithm finds a shortest one, at the cost of $\Theta(MN)$ time and memory on an $M \times N$ grid.

## In plain words

Think of the chip as a sheet of squared paper. Some squares are full, and a wire cannot cross them. You want to join two squares with a wire that is as short as possible.

Write 0 in the start square. Write 1 in each free square next to it. Then write 2 in each free empty square next to a 1, and so on, like a ring of water that spreads out from a stone dropped in a pond. Stop when the ring reaches the goal square.

The number in the goal square is the length of the shortest wire. To draw the wire, start at the goal and step to a neighbor with a number one smaller. Keep doing this until you reach 0. If the ring stops growing before it reaches the goal, no wire is possible.

## The problem

The input is a grid of $M$ rows and $N$ columns, where each cell is free or blocked, and two free cells $s$ and $t$. Two cells are neighbors if they share a side. A path is a sequence of free cells in which each cell is a neighbor of the next. Its length is the number of steps. The output is a shortest path from $s$ to $t$, or the answer that no path exists. In a detailed router the blocked cells are the pins, the wires of nets that are already routed and the obstacles. In a global router the cells are larger tiles, and the same search runs with costs on the edges (see [global routing](/global-routing/)).

## The algorithm

```pseudo id=main
LEE(grid, s, t)
L1  label(s) ← 0;  queue ← [s]
L2  while queue is not empty and t has no label do
L3      u ← remove the first cell of queue
L4      for each free neighbor v of u with no label do
L5          label(v) ← label(u) + 1;  add v at the end of queue
L6  if t has no label then return "no path"
L7  path ← [t];  u ← t
L8  while u ≠ s do
L9      u ← a neighbor of u with label(u) - 1   (fixed order: up, right, down, left)
L10     add u to path
L11 return path in reverse order
```

Lines L1 to L5 are the wave expansion. All cells with label $k$ form the $k$-th wave front. Lines L7 to L10 are the backtrace. The fixed order of neighbors on line L9 decides which shortest path is returned when there are several.

## Example

Take this grid of 5 rows and 5 columns, with rows and columns numbered from 0, $s = (2, 0)$ and $t = (2, 4)$. A `#` is a blocked cell. The second grid shows the label of each cell after the expansion.

```
. . . . .        2 3 4 5 6
. # # # .        1 # # # 7
s . . # t        0 1 2 # 8
# . # . .        # 2 # 6 7
. . . . .        4 3 4 5 6
```

The wave fronts are:

| label | cells |
| --- | --- |
| 0 | (2,0) |
| 1 | (1,0), (2,1) |
| 2 | (0,0), (2,2), (3,1) |
| 3 | (0,1), (4,1) |
| 4 | (0,2), (4,0), (4,2) |
| 5 | (0,3), (4,3) |
| 6 | (0,4), (3,3), (4,4) |
| 7 | (1,4), (3,4) |
| 8 | (2,4) |

The target gets label 8, so the shortest path has 8 steps. All 19 free cells were labeled before the target. The backtrace starts at $(2, 4)$ with label 8. The neighbor above, $(1, 4)$, has label 7, so it goes there, then to $(0, 4)$ with 6, and along the top row to $(0, 0)$ with 2, then down to $(1, 0)$ and $(2, 0)$. The path is

$(2,0), (1,0), (0,0), (0,1), (0,2), (0,3), (0,4), (1,4), (2,4)$.

The route along the bottom, through $(3, 4)$, also has 8 steps. The backtrace takes the top route because it tries the neighbor above first.

## Correctness

The [proof](proofs/correctness.md) shows the following.

- **Labels are distances.** Each label is the length of a shortest path from $s$ to that cell, as in [breadth-first search](/breadth-first-search/), because the queue holds the cells in order of their labels.
- **Early stop is safe.** When $t$ gets its label $L$, every cell at distance less than $L$ already has its label. So line L9 always finds a neighbor with the label one less.
- **Shortest path.** The backtrace makes $L$ steps and every step goes to a neighbor, so the path has length $L$, the distance from $s$ to $t$.
- **No false failures.** If the queue empties before $t$ is labeled, the labeled cells form the whole component of $s$, so no path exists.
- **Akers coding.** Two bits per cell are enough for the backtrace, because the two kinds of neighbors of a cell, one step nearer to $s$ or one step farther, always get different bits in the sequence 0, 0, 1, 1.

## Complexity

- **Time.** Each free cell enters the queue at most once, and each cell has at most 4 neighbors. So the expansion takes $O(MN)$ time, and the backtrace takes $O(L) = O(MN)$. In the worst case, for example when $t$ is the last free cell of a long spiral, the wave visits every cell, so the bound is $\Theta(MN)$.
- **Space.** A label for every cell takes $\Theta(MN)$ memory. Lee stored the distance in each cell. With Akers' coding the label takes one bit, and with the free and blocked states a cell needs two bits.
- **Wasted work.** The wave grows in all directions, also away from the target. In an open grid it labels about $2L^2$ cells to find a path of length $L$. [Hadlock's algorithm](/hadlock-algorithm/) and [A* search](/a-star-search/) aim the search at the target.

## Properties

- **What is proved.** If a path exists, Lee's algorithm finds a shortest one. If no path exists, it says so. These are the guarantees of [breadth-first search](/breadth-first-search/).
- **Exact and deterministic.** The result depends only on the grid and on the fixed order of neighbors in the backtrace.
- **One net at a time.** The path is shortest for this net, given the wires that are already in place. The order in which nets are routed changes the result, and a net routed early can block a later one. Lee's algorithm says nothing about the total wire length of many nets.
- **Uniform cost.** Every step costs 1. Bends and vias have no cost unless the search is changed, as in the variants below.

## Variants and improvements

- **Akers coding (1967).** Label the cells with the sequence 0, 0, 1, 1, 0, 0, 1, 1, ... by distance, instead of the distance itself. A cell then needs two bits, and the backtrace still works.
- **Bidirectional search.** Grow waves from $s$ and from $t$ and stop when they meet. In an open grid this labels about half as many cells.
- **Bounding box.** Search only inside a box around $s$ and $t$ with a margin. This is faster, but it can miss a path that leaves the box.
- **Costs on cells and edges.** With costs for bends, vias, layers or congestion, the wave becomes [Dijkstra's algorithm](/dijkstra/) with a priority queue. With costs 0 and 1 it is a [0-1 BFS](/zero-one-bfs/). Global routers and [negotiated congestion routing](/negotiated-congestion-routing/) use this form.
- **Search toward the target.** [Hadlock's algorithm](/hadlock-algorithm/) orders the cells by detour number, which is [A* search](/a-star-search/) with the Manhattan distance. [Soukup's algorithm](/soukup-algorithm/) runs depth first toward the target and gives up the guarantee of a shortest path.
- **Multi-pin nets.** Start the wave from all cells of the tree built so far, and connect the nearest unconnected pin. Repeat until all pins are connected. This builds a Steiner tree heuristically.
- **Line probes.** [Line-probe routing](/line-probe-routing/) works with whole free segments instead of single cells and needs much less memory.

## When to use it

- To route a two-pin connection on a grid when a shortest path is needed and a path must be found whenever one exists.
- As the base search of a [rip-up and reroute](/rip-up-and-reroute/) loop, with costs added.
- On small grids or inside a small window, where $\Theta(MN)$ memory is not a problem.

When the grid is large and open, use [Hadlock's algorithm](/hadlock-algorithm/) or A*, which label far fewer cells. When memory is the limit, use [line-probe routing](/line-probe-routing/).

## Pitfalls

- **Stopping too late.** The expansion can stop as soon as $t$ has a label. Going on to fill the whole grid gives the same path but costs more time.
- **Backtrace without a fixed order.** Any neighbor with the label one less is correct, but an order that is not fixed makes the result change from run to run. Some routers prefer the neighbor in the same direction as the last step, which gives fewer bends.
- **Diagonal moves.** The grid has four neighbors per cell. Adding diagonal steps changes the problem, and the labels are no longer the rectilinear length.
- **Pins on blocked cells.** If $s$ or $t$ is itself marked as blocked, for example because it is a pin of the net, the search must treat it as free.
- **Akers labels without the phase.** With Akers' coding, the backtrace must know which bit it expects next. It starts from the bit of the target and steps back one position in the sequence at each cell.

## Implementations

## History

C. Y. Lee, at Bell Telephone Laboratories, published the algorithm in 1961 for path connections on a grid, with wiring of printed circuit boards as the main use. E. F. Moore had described the same breadth-first labeling in 1959 to find the shortest path through a maze, and the method is the breadth-first search of graph theory. In 1967 S. B. Akers showed that the labels can be cut to two bits per cell with the sequence 0, 0, 1, 1. Lee's router became the base of grid routers in EDA. Later work aimed the search at the target, with Hadlock in 1977 and Soukup in 1978, or replaced the cells by line segments, with Mikami and Tabuchi in 1968 and Hightower in 1969.

## References
