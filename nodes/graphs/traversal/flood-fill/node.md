---
tag: M5TTW9
kind: algorithm
slug: flood-fill
name: Flood fill
aliases:
- bucket fill
- paint bucket fill
- seed fill
area: graphs/traversal
level: intro
summary: Marks all cells connected to a seed cell that share its color or label.
solves: [graph-reachability]
model: word-ram
complexity:
  vars: {k: the number of cells in the region of the seed}
  time: {worst: Θ(k), best: Θ(1)}
  space: {extra: O(k)}
properties: {deterministic: true, recursive: false}
prereqs: [breadth-first-search, depth-first-search, implicit-graph]
see_also: [connected-component-labeling, connected-components, region-filling, scanline-polygon-fill, multi-source-bfs, whatever-first-search, iterative-depth-first-search, graph-traversal]
sources:
  - paper: doi:10.1145/800249.807456
    title: Alvy Ray Smith, Tint fill, Proceedings of the 6th Annual Conference on Computer Graphics and Interactive Techniques (SIGGRAPH 1979), 276 to 283
    locator: the whole paper (seed fill of a region of pixels, and the fill by horizontal spans)
  - paper: doi:10.1016/b978-0-08-050753-8.50058-9
    title: Paul S. Heckbert, A seed fill algorithm, in Graphics Gems, Academic Press (1990), 275 to 277
    locator: the whole article (a span-based seed fill with an explicit stack)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Sections 20.2 and 20.3, Breadth-first search and Depth-first search (the searches that flood fill runs on the grid graph)
---

Flood fill recolours the region of a seed cell in a grid: all cells that have the colour of the seed and that the seed reaches by steps between neighbouring cells of that colour. It is the "paint bucket" tool of drawing programs, and it also finds the connected regions of a maze, a game board or a binary image. The grid is an [implicit graph](/implicit-graph/): each cell is a vertex, and two cells are adjacent if they are neighbours and have the same colour. Flood fill is a [graph traversal](/graph-traversal/) of this graph from the seed, done by [depth-first search](/depth-first-search/) with an explicit stack or by [breadth-first search](/breadth-first-search/) with a queue. The new colour itself serves as the visited mark, so the algorithm needs no other array, and it takes $\Theta(k)$ time for a region of $k$ cells.

## In plain words

Pour paint on one square of a tiled floor. The paint runs onto every next square of the same colour, and from there onto the next ones, but it stops at squares of another colour. Flood fill does the same thing, one square at a time.

It keeps a pile of squares that are painted but whose neighbours are not checked yet. It takes a square from the pile, looks at the four squares above, below, left and right, and paints each one that still has the old colour, and puts it on the pile. When the pile is empty, the whole region is painted. A painted square no longer has the old colour, so no square is painted twice.

## The problem

The input is a grid $A$ of $R \times C$ cells, each with a colour, a seed cell $s$ and a new colour $c$. Two cells are *neighbours* if they share a side (4-connectivity). Let $o = A[s]$ be the old colour. The *region* of $s$ is the set of cells $p$ for which a sequence $s = p_0, p_1, \ldots, p_j = p$ of cells exists, each a neighbour of the one before, all with colour $o$. The task is to give every cell of the region the colour $c$ and leave all other cells unchanged. In graph terms, this is [graph reachability](/graph-reachability/) from $s$ in the graph whose vertices are the cells of colour $o$.

## The algorithm

```pseudo id=main
FLOOD-FILL(A, s, c)
L1  o ← A[s]
L2  if o = c then return
L3  A[s] ← c
L4  S ← a stack that holds s
L5  while S is not empty do
L6      p ← POP(S)
L7      for each neighbour q of p inside the grid do
L8          if A[q] = o then
L9              A[q] ← c
L10             PUSH(S, q)
L11 return
```

Line L2 is necessary: if the new colour equals the old one, the test of line L8 never fails for a filled cell, and the loop never ends. Lines L9 and L10 recolour a cell at the moment it is pushed, so a cell is pushed at most once. A [queue](/queue/) in place of the [stack](/stack/) gives the same region, filled in order of distance from the seed.

## Example

Take this grid of 5 rows and 6 columns, the seed $(0, 0)$ with colour 1, and the new colour 3. The neighbours of a cell are tried in the order up, down, left, right.

```
1 1 1 2 2 2        3 3 3 2 2 2
1 2 1 2 1 2        3 2 3 2 3 2
1 2 1 1 1 2   ->   3 2 3 3 3 2
2 2 2 2 1 1        2 2 2 2 3 3
1 1 2 1 1 2        1 1 2 3 3 2
```

The trace, with cells as (row, column):

| pop | pushed (and recoloured) | stack after the step |
|---|---|---|
| (0,0) | (1,0), (0,1) | (1,0), (0,1) |
| (0,1) | (0,2) | (1,0), (0,2) |
| (0,2) | (1,2) | (1,0), (1,2) |
| (1,2) | (2,2) | (1,0), (2,2) |
| (2,2) | (2,3) | (1,0), (2,3) |
| (2,3) | (2,4) | (1,0), (2,4) |
| (2,4) | (1,4), (3,4) | (1,0), (1,4), (3,4) |
| (3,4) | (4,4), (3,5) | (1,0), (1,4), (4,4), (3,5) |
| (3,5) | none | (1,0), (1,4), (4,4) |
| (4,4) | (4,3) | (1,0), (1,4), (4,3) |
| (4,3) | none | (1,0), (1,4) |
| (1,4) | none | (1,0) |
| (1,0) | (2,0) | (2,0) |
| (2,0) | none | empty |

The region has 14 cells. The two cells $(4, 0)$ and $(4, 1)$ also have colour 1, but the row of 2s above them separates them from the seed, so they keep their colour. The stack never holds more than 4 cells here.

## Correctness

Every recoloured cell is in the region, because it is pushed from a cell of the region and has colour $o$. Every cell of the region is recoloured: on a path of colour $o$ from $s$, the first cell that is not recoloured would follow a recoloured cell, which was pushed, popped, and tested this neighbour at line L8 while it still had colour $o$. The loop ends because each push changes one cell from $o$ to $c \ne o$. The full proof is below.

## Complexity

The cost is in the [word RAM](/word-ram/) model, with $k$ the number of cells in the region.

- Each push recolours a cell of the region, so there are exactly $k$ pushes and $k$ pops.
- Each pop tests at most 4 neighbours at lines L7 and L8.

So the time is $\Theta(k)$ when $o \ne c$, and $\Theta(1)$ when $o = c$ or the seed has no neighbour of its colour. The time does not depend on the size of the grid, only on the region. The stack holds at most $k$ cells, so the extra space is $O(k)$. A long thin region, such as a spiral, can put $\Theta(k)$ cells on the stack.

## Properties

- **Deterministic.** The order of the neighbours fixes the order of the fill, and the result does not depend on it.
- **In place.** The colour is the visited mark, and no array of size $R \times C$ is needed.
- **Not recursive.** The explicit stack does not overflow the call stack on large regions.
- **Output sensitive.** The cost depends on the region, not on the grid.

## Variants and improvements

- **Recursive fill.** The shortest program calls itself on the four neighbours. It is [depth-first search](/depth-first-search/), but a region of $10^6$ cells can need a call depth of $10^6$, which overflows the stack of most systems.
- **Breadth-first fill.** With a queue, the cells are recoloured in order of their distance from the seed inside the region, as in [BFS layers](/bfs-layers/). The queue is often shorter than the stack on open regions.
- **8-connectivity.** Neighbours across a corner also count. A region in 8-connectivity can pass between two cells that touch only at a corner. Image processing often pairs 8-connectivity for the foreground with 4-connectivity for the background, so that a closed curve has a well-defined inside.
- **Span fill.** Smith and later Heckbert fill a whole horizontal run of cells at once, then push one seed for each run of fillable cells in the rows above and below. This pushes far fewer cells and reads memory row by row. The time is still $O(k)$ for a region of $k$ cells.
- **Boundary fill.** Fill outward from the seed until a cell of a given boundary colour is met, instead of while the old colour holds. This fills a region drawn as an outline that may contain other colours.
- **Label all regions.** Run flood fill from every cell that is not yet labelled, with a new label each time. This is [connected component labeling](/connected-component-labeling/) in $\Theta(RC)$ time.
- **Several seeds.** Start with several seeds in the stack, or use [multi-source BFS](/multi-source-bfs/) to give each cell the label of its nearest seed.

## When to use it

Use flood fill to recolour or measure one region from a seed: the paint bucket in an image editor, the area of a lake in a height map, the cells a player can reach on a board, or the cells uncovered by a click in Minesweeper. Use the explicit stack or the queue for any region that can be large. For labelling all regions of a large image, use a two-pass [connected component labeling](/connected-component-labeling/) algorithm, which reads the image in raster order. For a polygon given by its edges rather than by pixels, use [scanline polygon fill](/scanline-polygon-fill/).

## Pitfalls

- **Same old and new colour.** Without line L2, the fill loops for ever, or a recursive version recurses for ever, when $o = c$.
- **Recolour on pop.** If cells are recoloured only when they are popped, a cell can be pushed by up to four neighbours before it is popped. The result is still right, but the stack can grow to about $4k$ entries.
- **Deep recursion.** The recursive version fails on large regions. Use a stack or a queue.
- **Bounds.** The neighbour test must check that $q$ is inside the grid before it reads $A[q]$.
- **Connectivity.** 4-connectivity and 8-connectivity give different regions. A diagonal line of a different colour stops a 4-connected fill but not an 8-connected one.

## Implementations

## History

Alvy Ray Smith described the fill of a region of pixels from a seed, including the fill by horizontal spans, in the paper "Tint fill" at SIGGRAPH 1979. Paul Heckbert published a compact span-based seed fill with an explicit stack in Graphics Gems in 1990. The method is a depth-first or breadth-first search of the grid graph, in the sense of [graph traversal](/graph-traversal/).

## References
