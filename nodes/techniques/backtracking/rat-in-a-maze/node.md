---
tag: 17W3YZ
kind: problem
slug: rat-in-a-maze
name: Rat in a maze
aliases:
- maze path enumeration
- rat in a maze problem
area: techniques/backtracking
level: intro
summary: Find a path through a grid maze from the start cell to the exit, moving only through open cells.
prereqs: [generic-backtracking-algorithm, depth-first-search, breadth-first-search]
see_also: [grid-paths-with-obstacles, flood-fill, enumerating-simple-paths, read-tarjan-path-enumeration, tremaux-traversal, longest-path-problem, reachability-problem]
sources:
  - book: isbn:9780929306414
    title: Ellis Horowitz, Sartaj Sahni and Sanguthevar Rajasekaran, Computer Algorithms, second edition
    locator: Chapter 6 (basic traversal and search, breadth-first and depth-first search) and Chapter 7 (backtracking)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Sections 20.2 (breadth-first search) and 20.3 (depth-first search)
  - paper: doi:10.1002/net.1975.5.3.237
    title: R. C. Read and R. E. Tarjan, Bounds on backtrack algorithms for listing cycles, paths, and spanning trees, Networks 5(3), 1975
    locator: pp. 237 to 252
  - paper: doi:10.1137/0208032
    title: Leslie G. Valiant, The complexity of enumeration and reliability problems, SIAM Journal on Computing 8(3), 1979
    locator: pp. 410 to 421
  - paper: doi:10.1137/0211056
    title: Alon Itai, Christos H. Papadimitriou and Jayme Luiz Szwarcfiter, Hamilton paths in grid graphs, SIAM Journal on Computing 11(4), 1982
    locator: pp. 676 to 686
---

The rat in a maze problem gives a grid of open and blocked cells and asks for a path of open cells from the start cell, usually the top-left corner, to the exit, usually the bottom-right corner, with each step to a cell that shares a side. It is a standard first exercise in [backtracking](/generic-backtracking-algorithm/): the rat walks forward, and at a dead end it steps back and tries another way. To find one path or a shortest path, the problem needs only a linear-time graph search; backtracking is needed when every path must be listed.

## In plain words

A rat stands in the top-left square of a grid. Some squares are walls. The rat wants to reach the bottom-right square, moving up, down, left or right, and never into a wall.

The rat tries a direction and keeps going. If it reaches a square with no new way out, it walks back to the last square where it had another choice, and tries that choice. It marks the squares it is on, so it never walks in a circle. This walking back is backtracking. To find just one way out, the rat needs to visit each square at most once. To list every way out, it must walk many more paths, and their number can grow very fast with the size of the maze.

## Definition

**Input.** An $r \times c$ matrix $M$ with $M[i][j] \in \{0, 1\}$, where 1 is an open cell and 0 a blocked cell, with rows $0 \ldots r-1$ and columns $0 \ldots c-1$. The start is $s = (0, 0)$ and the exit is $t = (r-1, c-1)$. A set of allowed moves $\Delta$: the four moves $\{(\pm 1, 0), (0, \pm 1)\}$ in the general version, or the two moves $\{(1, 0), (0, 1)\}$ (down and right) in the classic textbook version.

**Paths.** A path is a sequence of cells $p_0 = s, p_1, \ldots, p_L = t$ such that each $p_k$ is open and $p_{k+1} - p_k \in \Delta$ for each $k$. Its length is $L$. With four moves, the path is *simple* when no cell occurs twice.

**Output.** One of these, by variant:

- **decision:** whether a path exists;
- **search:** one path, or "none";
- **enumeration:** the list of all simple paths;
- **counting:** the number of simple paths;
- **optimization:** a path of minimum length.

The open cells and the moves form the *maze graph*: a vertex for each open cell and an edge for each move between two open cells. With four moves it is an undirected grid graph, an induced subgraph of the infinite grid. With two moves it is a directed acyclic graph.

## Variants

- **Down and right only.** Each path has length exactly $r + c - 2$, and the graph is acyclic, so no cell can repeat. The number of paths is computed by a simple recurrence, as in [grid paths with obstacles](/grid-paths-with-obstacles/).
- **Four directions, one path.** This is $s$-$t$ [reachability](/reachability-problem/) in the maze graph.
- **Four directions, shortest path.** This is a single-source shortest path in an unweighted graph, solved by [breadth-first search](/breadth-first-search/).
- **Four directions, all simple paths.** This is the listing of simple $s$-$t$ paths, the true backtracking variant. See [enumerating simple paths](/enumerating-simple-paths/).
- **Longest simple path, or a path through every open cell.** A [longest path](/longest-path-problem/) or Hamilton path variant, which is hard.
- **Eight directions, weighted cells, several exits, or a maze not known in advance.** The same methods apply with a different move set or with [Dijkstra's algorithm](/dijkstra/). In a maze that is explored on foot, [Tremaux's traversal](/tremaux-traversal/) is the depth-first search done with marks on the floor.

## Examples

Take this $5 \times 5$ maze, with $s$ at the top-left and $t$ at the bottom-right. Row 0 is at the top.

```
row 0:  1 1 0 1 1
row 1:  0 1 1 1 0
row 2:  1 1 0 1 1
row 3:  1 0 1 1 0
row 4:  1 1 1 1 1
```

It has 19 open cells. The answers of the variants are:

| variant | answer |
|---|---|
| down and right only: number of paths | 1, the moves R D R R D D D R |
| four directions: does a path exist? | yes |
| four directions: number of simple paths | 4, of lengths 8, 10, 10 and 12 |
| four directions: shortest path length | 8 |

The backtracking search that tries the moves in the order down, right, up, left makes 54 calls to list all 4 simple paths. The first path it finds has length 10:

$$(0,0), (0,1), (1,1), (2,1), (2,0), (3,0), (4,0), (4,1), (4,2), (4,3), (4,4).$$

It is not the shortest. The shortest path, of length 8, goes $(0,0), (0,1), (1,1), (1,2), (1,3), (2,3), (3,3), (4,3), (4,4)$, and the right-and-down path is the same path. A depth-first search does not find shortest paths, while a breadth-first search does.

For an $n \times n$ grid with no blocked cell and the moves down and right, the number of paths is the [binomial coefficient](/binomial-coefficient/) $\binom{2n-2}{n-1}$: each path is an order of $n - 1$ down moves and $n - 1$ right moves. For $n = 5$ this is 70.

## Known algorithms

- **Backtracking.** Walk from $s$, mark the current path, try each move to an open unmarked cell, and unmark on return. It solves all the variants. Used for the search variant, it is a [depth-first search](/depth-first-search/) only if cells stay marked after the return; if they are unmarked, it can take exponential time before it gives up.
- **[Depth-first search](/depth-first-search/) or [flood fill](/flood-fill/).** Mark each cell when it is first reached and never unmark it. Finds a path, or proves that none exists, in $O(rc)$ time.
- **[Breadth-first search](/breadth-first-search/).** Finds a shortest path in $O(rc)$ time.
- **Dynamic programming for down and right moves.** $N[i][j] = N[i-1][j] + N[i][j-1]$ for an open cell, $N[i][j] = 0$ for a blocked cell, and $N[0][0] = M[0][0]$. Counts the paths in $O(rc)$ additions.
- **Listing with a reachability check.** Before each move, test whether $t$ is still reachable from the new cell without the marked cells, and cut the branch if it is not. Each branch then ends in a path, and the time per path is polynomial. Read and Tarjan (1975) give a backtracking method that lists the simple paths between two vertices in $O(V + E)$ time per path, which for a maze graph is $O(rc)$ per path. See [Read-Tarjan path enumeration](/read-tarjan-path-enumeration/).

## Bounds

- **One path or a shortest path.** $\Theta(rc)$ in the worst case. The upper bound is breadth-first search. For the lower bound, an algorithm that has not read some cell cannot know whether that cell is the only gap in a wall between $s$ and $t$, so in the worst case it must read $\Omega(rc)$ cells.
- **Number of simple paths.** The output of the listing variant can be exponential in the number of cells, so no listing method is polynomial in the input alone. On the open $n \times n$ grid with four moves, the numbers of simple corner-to-corner paths for $n = 2, 3, 4, 5$ are 2, 12, 184 and 8512.
- **Counting simple paths.** Counting the simple $s$-$t$ paths of a general graph is #P-complete (Valiant 1979). The page makes no claim for grid graphs.
- **Longest path.** Itai, Papadimitriou and Szwarcfiter (1982) proved that deciding whether a grid graph has a Hamilton path is NP-complete. A maze graph with four moves is a grid graph, so the question "is there a simple path through every open cell?" is NP-complete for mazes.
- **Plain backtracking without a reachability check.** It can spend exponential time on branches that never reach $t$, for example in a large open region that is cut off from $t$ by a wall near $t$.

## Reductions

- **To graph search.** The maze becomes a graph with at most $rc$ vertices and at most $2rc$ edges in $O(rc)$ time. Each variant is then the same variant on the graph.
- **From Hamilton path in grid graphs.** Each grid graph is a maze: draw its vertices as open cells in a large enough grid. This is how the hardness of the longest-path variant follows.

## Applications

- **Teaching.** It is a standard first example of backtracking, of the difference between depth-first and breadth-first search, and of why a visited mark changes exponential time into linear time.
- **Robot and game path finding.** Grids are a common map model, and the shortest-path variant with weights or a heuristic leads to [A* search](/a-star-search/).
- **Routing on a grid.** Wire routing on a chip and connected-region filling in images use the same grid searches, as in [flood fill](/flood-fill/) and [connected-component labeling](/connected-component-labeling/).

## References
