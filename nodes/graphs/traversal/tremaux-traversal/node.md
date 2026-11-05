---
tag: BKR094
kind: algorithm
slug: tremaux-traversal
name: Trémaux traversal
aliases:
- Tremaux's algorithm
- Tremaux maze exploration
area: graphs/traversal
level: intro
summary: Explores a maze by marking each passage on entry and exit so every passage is walked at most twice.
solves: [graph-reachability, graph-exploration]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n + m), best: Θ(n + m)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false}
prereqs: [depth-first-search]
see_also: [dfs-forest, iterative-depth-first-search, graph-exploration, eulerian-circuit, edge-classification, white-path-theorem, graph-traversal, flood-fill]
sources:
  - book: isbn:9780521736534
    title: Shimon Even, Graph Algorithms, second edition (edited by Guy Even), Cambridge University Press
    locator: Chapter 3, Depth-first search, Section 3.1 (Trémaux's algorithm, with the marks on the passages and the proof that each passage is traversed twice)
  - paper: "Édouard Lucas, Récréations mathématiques, volume 1, Gauthier-Villars, Paris (1882)"
    locator: the recreation on mazes (le jeu des labyrinthes), which presents the method of Trémaux
  - paper: "Gaston Tarry, Le problème des labyrinthes, Nouvelles Annales de Mathématiques, 3rd series, 14 (1895), 187 to 190"
    locator: the whole note (a rule for walking each passage of a maze once in each direction)
---

Trémaux traversal is a rule for walking through a maze, by a person who sees only the junction where he stands and the marks that he has made, so that he passes along every corridor and returns to the start. Each corridor is marked when the walker enters it and again when he leaves it for the last time, and a corridor with two marks is never used again. The rule is [depth-first search](/depth-first-search/) done by a walker: the corridors with one mark always form the path back to the start, which is the stack of the search. On a connected maze with $m$ corridors, the walk has exactly $2m$ steps: each corridor is walked exactly twice, once in each direction. The corridors through which the walker first entered each junction form a spanning tree in which every other corridor joins a junction to one of its ancestors, a *Trémaux tree*, which is the [depth-first tree](/dfs-forest/) of the search.

## In plain words

You are in a maze with a piece of chalk. At each junction, you make a mark at the entrance of each corridor that you go into, and a second mark when you leave a corridor for good. The rules are:

- At a new junction, take any corridor without a mark.
- If a corridor without marks brings you to a junction you have already seen, turn back at once.
- If no corridor at your junction is free, go back along the corridor with one mark, which is the way you first came in.
- If there is no such corridor, you are back at the start, and you have seen the whole maze.

Nothing needs to be remembered except the chalk marks. Each corridor gets walked once each way, and no more.

## The problem

The maze is a connected undirected [multigraph](/multigraph/) $G = (V, E)$: the junctions are vertices and the corridors are edges, with loops and parallel corridors allowed. A walker starts at $s$. At each moment he knows the edges at his current vertex, the marks on them and whether the vertex has been visited, which a mark on the vertex, or on any of its edges, shows. He can move along one edge to its other end. The task is to visit every vertex of the component of $s$ and return to $s$, with a walk that is short. This is the offline maze version of [graph exploration](/graph-exploration/), and solves [graph reachability](/graph-reachability/) from $s$ without any memory in the walker.

## The algorithm

```pseudo id=main
TREMAUX(G, s)
L1  set marks[e] ← 0 for each edge e, visited[s] ← true, entry[s] ← NIL, v ← s
L2  loop
L3      if some edge e = {v, w} has marks[e] = 0 then
L4          marks[e] ← 1, walk to w
L5          if visited[w] then marks[e] ← 2, walk back to v
L6          else visited[w] ← true, entry[w] ← e, v ← w
L7      else if entry[v] ≠ NIL then
L8          marks[entry[v]] ← 2, walk along entry[v] to its other end u, v ← u
L9      else stop
```

The walker needs $\mathrm{entry}[v]$ only to find the way back, and he does not have to remember it: at each moment, it is the only edge at $v$ with one mark, as the proof shows.

## Example

Take the maze with vertices 0 to 7 and the edges $\{0,1\}$, $\{0,2\}$, $\{1,3\}$, $\{2,3\}$, $\{2,4\}$, $\{3,5\}$, $\{4,5\}$, $\{5,6\}$, with the edges at each vertex tried in this order, and $s = 0$.

| at | rule | move | marks after the move |
|---|---|---|---|
| 0 | L6 | to 1 | $\{0,1\} = 1$ |
| 1 | L6 | to 3 | $\{1,3\} = 1$ |
| 3 | L6 | to 2 | $\{2,3\} = 1$ |
| 2 | L5 | to 0 and back to 2 | $\{0,2\} = 2$ |
| 2 | L6 | to 4 | $\{2,4\} = 1$ |
| 4 | L6 | to 5 | $\{4,5\} = 1$ |
| 5 | L5 | to 3 and back to 5 | $\{3,5\} = 2$ |
| 5 | L6 | to 6 | $\{5,6\} = 1$ |
| 6 | L8 | back to 5 | $\{5,6\} = 2$ |
| 5 | L8 | back to 4 | $\{4,5\} = 2$ |
| 4 | L8 | back to 2 | $\{2,4\} = 2$ |
| 2 | L8 | back to 3 | $\{2,3\} = 2$ |
| 3 | L8 | back to 1 | $\{1,3\} = 2$ |
| 1 | L8 | back to 0 | $\{0,1\} = 2$ |
| 0 | L9 | stop | |

The walk is $0, 1, 3, 2, 0, 2, 4, 5, 3, 5, 6, 5, 4, 2, 3, 1, 0$, with 16 steps, twice the 8 edges. The entry edges form the path $0, 1, 3, 2, 4, 5, 6$, which is the DFS tree of the same graph on the [depth-first search](/depth-first-search/) page. The two other edges, $\{0, 2\}$ and $\{3, 5\}$, each join a vertex to one of its ancestors on this path. Vertex 7 is not in the component of 0 and is never reached.

## Correctness

At each moment, the edges with one mark are exactly the entry edges of the vertices on the path from $s$ to the walker, and each visited vertex off this path has no unmarked edge. So the edge with one mark at the walker is the way back, and when the walker stops at $s$, every visited vertex has all its edges marked. Then each edge of the component has two marks, so it has been walked twice, and every vertex is visited, because an edge from a visited vertex to an unvisited one would still be unmarked. Each step adds a mark, so the walk ends after at most $2m$ marks. The full proof is below.

## Complexity

The cost is in the [word RAM](/word-ram/) model, with the edges at each vertex in a list and a pointer per vertex to the first edge that may be unmarked. Marks only grow, so each pointer moves forward over its list one time.

- **Walk.** Each edge of the component of $s$ is walked exactly twice, so the walk has $2m$ steps on a connected graph.
- **Search for a free edge.** Each pointer scans its list one time: $\Theta(n + m)$ in total.

So the time is $\Theta(n + m)$, including the setup of the marks, and the extra space is $\Theta(n + m)$ for the marks. A physical walker needs no memory at all, because the marks are in the maze.

## Properties

- **Walks each edge twice.** Exactly $2m$ steps on a connected graph, one in each direction for each edge.
- **No memory in the walker.** All state is in the marks, and only local marks are read.
- **Depth-first.** If the edges at each vertex are tried in a fixed order, the order of first visits and the entry edges are those of the recursive DFS with the same lists.
- **Trémaux tree.** The entry edges form a spanning tree of the component in which each non-tree edge joins an ancestor and a descendant.
- **Deterministic** for a fixed order of the edges at each vertex. Any choice of free edge is allowed, and every choice gives a correct walk.

## Variants and improvements

- **Tarry's rule.** Tarry gave a rule with the same bound that also walks each edge once in each direction, and that allows any free edge to be chosen except that the first-entry edge is used last. Trémaux's rule, which also turns back at once at an old vertex, is a special case of it.
- **Eulerian circuit.** The walk of Trémaux traverses each edge once in each direction, so it is an [Eulerian circuit](/eulerian-circuit/) of the directed graph that has both directions of each edge.
- **Unknown graphs.** When the graph is not known in advance, the same rule explores it with $2m$ edge traversals. For exploring with a cost measured against the number of edges, see [graph exploration](/graph-exploration/).
- **Wall following.** In a maze whose walls are all connected to the outer wall, keeping one hand on a wall reaches the exit with no marks, but it fails when the maze has an island of walls. Trémaux's rule works on every maze.

## When to use it

Use Trémaux's rule to explore a maze or a graph in person or by a robot that can leave marks at junctions but has little memory, and when a return to the start is needed. In a program, the same search is [iterative depth-first search](/iterative-depth-first-search/), which gives the same tree. The marks with one and two counts are also a compact way to keep the stack of a DFS in the edges themselves.

## Pitfalls

- **Not turning back.** At a visited vertex reached by a free edge, the walker must turn back at once. If he goes on, a later step may follow a one-mark edge that is not the way back.
- **Leaving by a marked edge.** The walker may leave a vertex by its one-mark edge only after all other edges there are marked. Otherwise some edges are never walked.
- **Self-loops.** A loop at $v$ leads back to $v$ at once, which is a visited vertex, so line L5 walks it twice and marks it twice. The walk has two steps that stay at $v$.
- **Directed corridors.** The rule needs every edge to be walkable in both directions. On a directed graph, the walker can be trapped.

## Implementations

## History

Charles Pierre Trémaux, a French engineer of the 19th century, found the method, and Édouard Lucas published it in the first volume of his Récréations mathématiques in 1882. Gaston Tarry gave another rule for mazes in 1895, which traverses each passage once in each direction. Shimon Even presents Trémaux's algorithm at the start of the chapter on depth-first search in his book Graph Algorithms, as the walking form of DFS, and proves that it walks each edge twice.

## References
