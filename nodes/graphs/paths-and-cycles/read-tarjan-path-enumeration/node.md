---
tag: 89EF45
kind: algorithm
slug: read-tarjan-path-enumeration
name: Read-Tarjan path enumeration
aliases:
- Read-Tarjan algorithm
area: graphs/paths-and-cycles
level: advanced
summary: Output-sensitive enumeration of simple s-t paths by DFS with pruning.
solves: [enumerating-simple-paths]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, N: the number of simple s-t paths}
  time: {worst: O((n + m)(N + 1)), best: Θ(n + m)}
  space: {extra: O(n · m)}
properties: {deterministic: true, recursive: false, output-sensitive: true}
history:
  year: 1975
  people: [R. C. Read, Robert E. Tarjan]
  note: Bounds on backtrack algorithms for listing cycles, paths, and spanning trees, Networks; O(n + m + mN) time and O(n + m) space for the simple paths between two vertices.
prereqs: [simple-path, depth-first-search, output-sensitive-enumeration, reachability]
see_also: [enumerating-simple-paths, johnson-elementary-cycles-algorithm, gabow-myers-enumeration, enumerating-elementary-cycles, longest-path-problem, hamiltonian-path, walk, stack]
sources:
  - paper: doi:10.1002/net.1975.5.3.237
    title: R. C. Read and R. E. Tarjan, Bounds on backtrack algorithms for listing cycles, paths, and spanning trees, Networks 5(3), 237 to 252 (1975)
    locator: the backtrack algorithm for the simple paths between two vertices and its O(V + E + EN) time and O(V + E) space bounds
  - paper: Etienne Birmelé, Rui Ferreira, Roberto Grossi, Andrea Marino, Nadia Pisanti, Romeo Rizzi and Gustavo Sacomoto, Optimal listing of cycles and st-paths in undirected graphs, SODA 2013
    title: Birmelé et al., optimal listing of st-paths
    locator: the binary partition method for st-paths and the comparison with Read and Tarjan
  - paper: doi:10.1137/0208032
    title: Leslie G. Valiant, The complexity of enumeration and reliability problems, SIAM Journal on Computing 8(3), 1979
    locator: "the #P-completeness of counting the simple s-t paths"
---

The Read-Tarjan method lists all [simple paths](/simple-path/) from a vertex $s$ to a vertex $t$ so that the work is proportional to the output: $O(n + m)$ per path, and $O(n + m)$ between two consecutive outputs. Plain backtracking can spend exponential time in dead ends that lead to no path. Read-Tarjan never enters a dead end: before it follows a branch it checks, by a [reachability](/reachability/) search, that the branch can still reach $t$, so every branch it opens yields at least one new path. This page gives the method in the binary partition form: find one path, then split the other paths by the place where they first leave it. The graph may be directed or undirected; parallel edges are merged and self-loops are ignored, since a simple path uses neither. See [enumerating simple paths](/enumerating-simple-paths/) for the problem.

## In plain words

You want every route from home to work that never passes the same crossing twice.

First find any one route and write it down. Every other route follows this route for a while and then turns off somewhere. So go back along the route, crossing by crossing. At each crossing, look at each road that turns off. Follow it only if from there you can still reach work without using the crossings already on your route.

Each road that you follow therefore gives at least one new route, and you never walk into a dead end. The total work is about one search of the map per route found.

## The problem

Given a graph $G = (V, E)$ with $V = \{0, \ldots, n - 1\}$, directed or undirected, and two vertices $s$ and $t$, list every simple path from $s$ to $t$ exactly once, as a sequence of vertices. If $s = t$, the only simple path is $(s)$. If $t$ cannot be reached from $s$, the list is empty. Parallel edges give the same vertex sequence and are merged; to list paths as edge sequences, multiply each path by the numbers of parallel edges along it. Isolated vertices change nothing. The number $N$ of paths can be exponential in $n$, and counting them is #P-complete (Valiant, 1979), so the cost is measured per path.

## The algorithm

A *branch* is a simple path $\pi$ from $s$ to a vertex $u$ such that some simple $s$-$t$ path starts with $\pi$. The branch stands for all those paths. To list them, the algorithm finds one, $\pi$ followed by a path $P = (p_0 = u, p_1, \ldots, p_k = t)$ that avoids $\pi$, and splits the rest by the last vertex $p_i$ that they share with $P$ and the next vertex $x \ne p_{i+1}$. The set $R$ holds the vertices that can reach $t$ without the blocked vertices $\pi \cup \{p_0, \ldots, p_i\}$, so a new branch is opened only when $x \in R$. As $i$ goes down, one vertex is unblocked at a time, and $R$ only grows.

```pseudo id=main
READ-TARJAN(G, s, t)
L1  if s = t then output (s) and stop
L2  if t is not reachable from s then stop
L3  S ← stack holding the branch (s)
L4  while S is not empty do
L5      π ← POP(S); u ← the last vertex of π
L6      if u = t then output π; continue
L7      B ← the vertices of π other than u
L8      P = (p0 = u, p1, …, pk = t) ← a path from u to t in G − B, by depth-first search
L9      output π followed by p1, …, pk
L10     blocked ← B ∪ {p0, …, pk−1}; R ← the vertices that reach t in G − blocked, by a reverse search from t
L11     for i ← k − 1 down to 0 do
L12         if i < k − 1 then unblock p(i+1); if it has an edge into R, add it to R and continue the reverse search from it over unblocked vertices
L13         for each edge from p(i) to a vertex x ≠ p(i+1) with x in R do
L14             PUSH(S, π followed by p1, …, pi, x)
```

In an undirected graph, each edge $\{u, v\}$ is used as the two arcs $u \to v$ and $v \to u$; the reverse search uses the same lists. To save space, a pushed branch is stored as a reference to the parent path, a cut length and the vertex $x$, and it is built only when it is popped.

## Example

A directed graph on the vertices $0, \ldots, 5$ with the arcs $0 \to 1$, $0 \to 2$, $1 \to 2$, $2 \to 1$, $1 \to 3$, $2 \to 3$, $3 \to 4$, $2 \to 4$, $4 \to 5$, with $s = 0$ and $t = 4$. Vertex 5 lies beyond $t$ and is on no path. The lists are in increasing order, and the depth-first search at line L8 takes the last pushed neighbour first.

| branch popped | path found at L8 | output | $R$ at each $i$ and branches pushed |
|---|---|---|---|
| $(0)$ | $0, 2, 4$ | $0, 2, 4$ | $i = 1$: $R = \{4, 3, 1\}$, push $(0, 2, 1)$ and $(0, 2, 3)$; $i = 0$: 2 joins $R$, push $(0, 1)$ |
| $(0, 1)$ | $1, 3, 4$ | $0, 1, 3, 4$ | $i = 1$: $R = \{4, 2\}$, none; $i = 0$: 3 joins, push $(0, 1, 2)$ |
| $(0, 1, 2)$ | $2, 4$ | $0, 1, 2, 4$ | $i = 0$: $R = \{4, 3\}$, push $(0, 1, 2, 3)$ |
| $(0, 1, 2, 3)$ | $3, 4$ | $0, 1, 2, 3, 4$ | $i = 0$: $R = \{4\}$, none |
| $(0, 2, 3)$ | $3, 4$ | $0, 2, 3, 4$ | none |
| $(0, 2, 1)$ | $1, 3, 4$ | $0, 2, 1, 3, 4$ | $i = 0$: 3 joins $R$; the arc $1 \to 2$ goes to a blocked vertex, none |

Six branches give six paths, which is all of them, and no work is spent on a branch without a path. The arc $4 \to 5$ is never followed, because a path stops at $t$. Add a vertex 6 with the arcs $1 \to 6$ and $6 \to 6$: plain backtracking enters the branch $(0, 1, 6)$ and finds nothing there, while Read-Tarjan never pushes it, because 6 is not in $R$.

## Correctness

Each popped branch lists exactly the simple $s$-$t$ paths that start with it. If its last vertex is $t$, that is the branch itself. Otherwise, the paths are $\pi P$ and, for each $i$ and $x$, the paths that follow $P$ up to $p_i$ and then go to $x$; these sets are disjoint and cover all the paths, and the set for $(i, x)$ is nonempty exactly when $x$ can reach $t$ avoiding $\pi$ and $p_0, \ldots, p_i$, which is the test $x \in R$. Branches get longer, so the process ends. The full proof is below.

## Complexity

The cost is in the [word RAM](/word-ram/) model with adjacency lists and hash sets.

- **One branch, lines L5 to L14.** Building $\pi$ and $B$ is $O(n)$. The search at line L8 is $O(n + m)$. The reverse searches at lines L10 and L12 together add each vertex to $R$ once and read each incoming list once, and line L12 reads each outgoing list of a path vertex once, so $O(n + m)$. Lines L13 and L14 read each outgoing list of a path vertex once.
- **Number of branches.** Every branch outputs one path at line L6 or L9, and different branches output different paths, so there are exactly $N$ branches.
- **Total.** $O(n + m)$ for lines L1 and L2, plus $O((n + m) N)$. Between two outputs the algorithm finishes one branch and starts the next, so the delay is $O(n + m)$.
- **Space.** The stack can hold up to $O(m)$ pending branches for each of up to $n$ nested paths, so $O(nm)$ in the worst case. Read and Tarjan's recursive form keeps only the current path and $O(n + m)$ space.

The best case is a graph with no path or one path: $\Theta(n + m)$.

## Properties

- **Output-sensitive.** Linear time per path, and linear delay. It never explores a dead end.
- **Exact and without repeats.** Every simple $s$-$t$ path is listed exactly once.
- **Deterministic and not recursive.** The order of the paths depends on the order of the lists.
- **Directed and undirected.** Both work. In an undirected graph, an edge between $u$ and $v$ never forms a path $u, v, u$, since paths are simple.
- **Loops and parallel edges.** Loops are dropped and parallel edges merged when the lists are built.

## Variants and improvements

- **Read and Tarjan's original.** A depth-first backtrack that, at each step, tests by a search whether the current path can still be extended to $t$, with $O(n + m + mN)$ time and $O(n + m)$ space.
- **Optimal for undirected graphs.** Birmelé et al. (2013) list the $s$-$t$ paths of an undirected graph in $O(m + \sum_P |P|)$ time, the size of the output, with a certificate based on biconnected components.
- **Cycles.** The same idea lists cycles: the cycles through an arc $u \to v$ are the paths from $v$ to $u$. Johnson's algorithm uses blocking instead of a search per branch; see [Johnson's algorithm](/johnson-elementary-cycles-algorithm/).
- **Paths in order of length.** To list the shortest paths first, use a $k$ shortest simple paths algorithm such as Yen's instead.
- **Counting.** Counting the paths is #P-complete, so no polynomial counting method is expected; the enumeration time grows with $N$.
- **Bounded length.** Restricting to paths with at most $L$ edges needs a distance test instead of a reachability test, with distances to $t$ that avoid the blocked vertices.

## When to use it

Use it when you need all simple paths between two vertices and the graph has many dead ends, for example in network reliability, in listing all routes for a small network, or in program analysis. When the number of paths is huge, list them lazily and stop early; the linear delay makes that cheap. If you need only the shortest few paths, a $k$ shortest paths method is better, and if you need only their number, no fast method exists in general.

## Pitfalls

- **Backtracking without the test.** Plain depth-first backtracking is correct but can take exponential time per path. A graph with $s$ joined to a large part of the graph from which $t$ cannot be reached is explored completely before any path is found.
- **Testing reachability in the wrong graph.** The test for $x$ must avoid the vertices of $\pi$ and $p_0, \ldots, p_i$, not only those of $\pi$; otherwise a branch can be opened that has no path.
- **Following the found path again.** At $p_i$ the edge to $p_{i+1}$ must be skipped; those paths belong to the branch that continues along $P$.
- **Edges versus vertices.** With parallel edges, decide whether paths are vertex sequences or edge sequences. This implementation lists vertex sequences.
- **Memory of the output.** Storing all $N$ paths takes $\Theta(nN)$ memory; for large $N$, process each path as it is found.

## Implementations

## History

Ronald Read and Robert Tarjan published "Bounds on backtrack algorithms for listing cycles, paths, and spanning trees" in Networks in 1975. They showed that backtracking with a test, at each step, that the partial solution can still be completed lists the simple paths between two vertices, the cycles, and the spanning trees of a graph in time linear in the size of the graph per object. Later work made the method faster and simpler for undirected graphs: Birmelé, Ferreira, Grossi, Marino, Pisanti, Rizzi and Sacomoto (2013) reached time linear in the total size of the output.

## References
