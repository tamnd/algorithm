---
tag: XNV0WK
kind: algorithm
slug: hierarchical-pathfinding-a-star
name: Hierarchical pathfinding A*
aliases:
- HPA*
area: games-and-search/heuristic-search
level: advanced
summary: "Splits a grid map into clusters, links the entrances between them in a small graph, runs A* on that graph and refines the result into a grid path. Fast on big maps, but not always optimal."
solves: [single-pair-shortest-path]
model: word-ram
complexity:
  vars: {n: the number of cells of the grid, c: the side of a cluster}
  time: {build: O(n c), worst: O(n c)}
  space: {extra: O(n)}
properties: {deterministic: true, recursive: false}
prereqs: [a-star-search, breadth-first-search]
see_also: [jump-point-search, theta-star, dijkstra, multi-agent-pathfinding, d-star-lite, motion-planning]
sources:
  - paper: "Adi Botea, Martin Müller and Jonathan Schaeffer, Near optimal hierarchical path-finding, Journal of Game Development 1(1) (2004)"
    title: "Near optimal hierarchical path-finding (Journal of Game Development, 2004)"
    locator: pp. 7 to 28; clusters, entrances and transitions, the abstract graph, inserting the start and the goal, refinement, smoothing, and the experiments on game maps
  - paper: "Nathan Sturtevant and Michael Buro, Partial pathfinding using map abstraction and refinement, AAAI 2005"
    title: "Partial pathfinding using map abstraction and refinement (AAAI 2005)"
    locator: the description of PRA*, an abstraction by small cliques of cells with partial refinement, and its experiments
---

Hierarchical pathfinding A* (HPA*) finds paths on big grid maps fast by planning at two scales. Before any query, it cuts the map into square clusters, puts a few *transition* cells on the openings between neighbouring clusters, and stores the distances between the transitions inside each cluster. A query runs [A*](/a-star-search/) on this small graph and then turns each step of the abstract path into a path on the grid. Adi Botea, Martin Müller and Jonathan Schaeffer introduced it in 2004 for computer games. The path is always valid, and usually close to the shortest, but it is not always optimal.

## In plain words

To drive across a country, you first choose the cities to pass through, and only then the streets inside each city. HPA* does the same on a grid. It divides the map into blocks. Where two blocks touch and the border is open, it marks one or two crossing points. For each block, it notes how far each crossing point is from each other one.

To find a path, it adds the start and the goal to this network of crossing points, and it searches the network. That search is small, because there are few crossing points. Then it fills in the walk inside each block. Because the path must go through the marked points, it can be a little longer than the best path.

## The problem

The input is a grid of free and blocked cells, a start cell $s$ and a goal cell $t$. A move goes to one of the 4 neighbouring free cells and costs 1. The task is a path from $s$ to $t$, or the answer that there is none. This is a [single-pair shortest path](/single-pair-shortest-path/) problem on the grid graph, but HPA* gives up the exact optimum for speed. Many queries are asked on the same map, so work done once before the queries pays off.

The paper uses 8-connected grids, with diagonal moves of cost $\sqrt 2$. The page uses the 4-connected case, which keeps the example and the proof short. The method and the argument are the same.

## The algorithm

The map is cut into clusters of $c$ by $c$ cells. An *entrance* is a maximal run of free cell pairs straight across one border segment between two clusters.

```pseudo id=main
BUILD(grid, c)
L1  cut the grid into clusters of c by c cells and list the border segments between them
L2  for each border segment do
L3      for each maximal run of pairs (a, b) with a and b free, straight across the border do
L4          if the run has fewer than 6 pairs then choose its middle pair, else choose its two end pairs
L5          for each chosen pair (a, b), add a and b as nodes with an edge of cost 1
L6  for each cluster do
L7      for each two nodes u, v of the cluster, add an edge between u and v of cost d(u, v) inside the cluster, if v is reachable
FIND-PATH(s, t)
L8  add s and t as nodes, with edges to the nodes of their clusters (and to each other) at the distances inside the cluster
L9  run A* from s to t on the abstract graph, with the Manhattan distance as heuristic
L10 if A* finds no path then return no path
L11 replace each abstract edge by its grid path: one move across a border, or a shortest path inside the cluster
```

Lines L1 to L7 run once for a map. The distances in line L7 and line L8 come from a [breadth-first search](/breadth-first-search/) that does not leave the cluster. Line L9 searches a graph of a few nodes for each cluster instead of $c^2$ cells. Line L11 can use the paths stored in line L7, or search them again inside the cluster. The paper also smooths the result: it replaces parts of the path with straight lines where they are free.

## Example

Take an open 10 by 10 grid with no walls, clusters of $c = 5$, so 4 clusters. Cells are $(x, y)$ with $y$ counted down. Each of the 4 border segments is one entrance of 5 pairs, shorter than 6, so line L4 chooses its middle pair. The abstract graph has 8 nodes.

| entrance | chosen pair |
| --- | --- |
| between columns 4 and 5, rows 0 to 4 | $(4, 2)$ and $(5, 2)$ |
| between columns 4 and 5, rows 5 to 9 | $(4, 7)$ and $(5, 7)$ |
| between rows 4 and 5, columns 0 to 4 | $(2, 4)$ and $(2, 5)$ |
| between rows 4 and 5, columns 5 to 9 | $(7, 4)$ and $(7, 5)$ |

Each cluster has 2 nodes, and lines L6 and L7 join them with an edge of cost 4: $(4, 2)$ with $(2, 4)$, $(5, 2)$ with $(7, 4)$, $(2, 5)$ with $(4, 7)$, and $(7, 5)$ with $(5, 7)$.

Ask for a path from $s = (0, 0)$ to $t = (9, 0)$. The shortest path goes straight along the top row and has length 9. Line L8 links $s$ to $(4, 2)$ at distance 6 and to $(2, 4)$ at distance 6, and $t$ to $(5, 2)$ at distance 6 and to $(7, 4)$ at distance 6. A* expands 4 abstract nodes: $s$, $(4, 2)$, $(5, 2)$ and $t$. The abstract path is $s, (4, 2), (5, 2), t$ of cost $6 + 1 + 6 = 13$. Line L11 refines it to

$$(0,0), (1,0), (2,0), (3,0), (4,0), (4,1), (4,2), (5,2), (6,2), (7,2), (8,2), (9,2), (9,1), (9,0).$$

The path is valid but 4 moves longer than the optimum, because it must cross the border at the transition in row 2. The proof shows that this is the worst case: each crossing of a shortest path costs at most twice the gap, the distance from a pair of an entrance to its nearest transition, here $2$.

**A measured experiment.** On 10 random 60 by 60 grids (each cell blocked with probability 0.2, `random.Random(10)` of Python), with clusters of $c = 10$ and 20 connected queries for each map, the abstract graphs had 3276 nodes in total, about 328 for each map of about 2900 free cells. The HPA* paths had a total length of 8193 against 8005 for the shortest paths, so they were 2.3 percent longer, without smoothing. A* on the abstract graph expanded 7176 nodes in total, about 36 for each query. These are measurements on these grids, not bounds.

## Correctness

The [proof](proofs/correctness.md) shows the following.

- **Every abstract edge is a real path.** An edge across a border is one move, and an edge inside a cluster has the length of a shortest path inside the cluster. So the refined path is valid, and its length is the cost that A* found. In particular, it is never shorter than the optimum $C^*$.
- **The Manhattan distance is consistent** on the abstract graph, so A* finds a cheapest abstract path.
- **The bound.** Take a shortest grid path with $X$ crossings of cluster borders. Each crossing belongs to an entrance. Moving it to the nearest transition of that entrance adds at most $2 \cdot \mathrm{gap}$ moves, and the new path follows abstract edges. So the cost is at most $C^* + 2 \cdot \mathrm{gap} \cdot X$, where the gap is at most $\max(2, \lfloor (c-1)/2 \rfloor)$ for the rule of line L4.
- **Complete.** By the same rerouting, if $t$ can be reached on the grid, the abstract graph has a path, so HPA* returns a path. If not, it returns none.

The bound does not depend on the walls inside the clusters, only on the number of border crossings of some shortest path.

## Complexity

The model is the [word RAM](/word-ram/). Let $n$ be the number of cells and $c$ the side of a cluster. A cluster has $O(c)$ transitions, at most 2 for each entrance on its 4 borders, so the abstract graph has $N = O(n/c)$ nodes and $O(n)$ edges inside the clusters. Line L7 makes one breadth-first search of $O(c^2)$ steps from each node, so the build takes $O(N c^2) = O(n c)$ time and the graph takes $O(n)$ space.

A query inserts $s$ and $t$ with two searches of $O(c^2)$ steps, runs A* in $O(n + N \log N)$ time on the abstract graph, and refines the path with at most one search of $O(c^2)$ steps for each abstract edge. In the worst case this is $O(n c)$, more than plain A* on the grid. In practice the abstract path has a few nodes for each cluster it passes, so a query costs about the clusters on the path times $c^2$, much less than a search of the whole map. Stored paths for the edges make the refinement linear in the length of the path, at the price of more memory.

## Properties

- **Valid paths**, never shorter than the optimum and at most $C^* + 2 \cdot \mathrm{gap} \cdot X$ long.
- **Not optimal.** The example has a path of length 13 where the optimum is 9.
- **Complete** on finite grids.
- **Preprocessing** once for each map, and a local update of the clusters next to a cell when the map changes.
- **Hierarchical.** The same construction can be applied again to the abstract graph, with bigger clusters, for more levels.

## Variants and improvements

- **More levels.** The paper builds clusters of clusters for very big maps.
- **Smoothing.** The paper replaces parts of the refined path with straight segments where they are free, which removes most of the extra length.
- **PRA*** (Sturtevant and Buro 2005) abstracts the map by small cliques of cells and refines only a part of the abstract path at a time, which helps when the goal moves.
- **Other choices of transitions.** More transitions for each entrance give a smaller gap and better paths, but a bigger graph. The bound of the proof holds with the gap of any rule that puts at least one transition on each entrance.
- **Compressed path databases and contraction hierarchies** store more and answer queries optimally, at a higher cost of memory or preprocessing.

## When to use it

Use HPA* for big grid maps in games, with many queries and units that need a good path quickly, when a path a few percent longer than the optimum is fine. It also gives a first part of the path at once, so a unit can start to move before the whole path is refined. For optimal paths on a grid, use A* or [jump point search](/jump-point-search/). For paths at any angle, use [Theta*](/theta-star/). For many agents that must not collide, see [multi-agent pathfinding](/multi-agent-pathfinding/).

## Pitfalls

- **Calling it optimal.** The transitions force where paths cross borders, so paths can be longer than the shortest, as in the example.
- **Forgetting the start-goal edge.** If $s$ and $t$ are in the same cluster and connected inside it, line L8 must link them directly. Without the edge, the path leaves the cluster and comes back.
- **Searching outside the cluster.** The distances of line L7 must use only cells of the cluster. A search over the whole grid gives edges that the refinement inside the cluster cannot follow.
- **Insertion cost.** Inserting $s$ and $t$ needs a search in their clusters on every query. With very big clusters this part dominates.
- **Expanded nodes are not time.** An abstract expansion looks at all the nodes of a cluster and the refinement searches inside clusters, so compare running times, not only expansions.

## Implementations

## History

Botea, Müller and Schaeffer described HPA* in the Journal of Game Development in 2004, and they measured it on maps from the game Baldur's Gate, where the smoothed paths were close to optimal and the searches much faster than A* on the grid. Hierarchical abstraction for pathfinding was older in robotics and in games, and HPA* made it simple and general enough for games. Sturtevant and Buro gave PRA* in 2005, and later work, such as the hierarchies used in game engines, built on the same idea of clusters and entrances.

## References
