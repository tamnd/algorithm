---
tag: 775KP1
kind: algorithm
slug: path-cover-by-bipartite-matching
name: Path cover by bipartite matching
aliases:
- minimum path cover via maximum matching
area: graphs/paths-and-cycles
level: advanced
summary: Minimum path cover of a DAG equals the vertex count minus a maximum matching in the split bipartite graph.
solves: [minimum-path-cover-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of arcs}
  time: {worst: O(n(n + m)), best: Θ(n^2 + m)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false}
history:
  year: 1956
  people: [D. R. Fulkerson]
  note: Note on Dilworth's decomposition theorem; the split bipartite graph of a partial order and the chain cover from a maximum matching.
prereqs: [minimum-path-cover-problem, bipartite-matching, augmenting-path, directed-acyclic-graph]
see_also: [kuhn-algorithm, hopcroft-karp, dilworth-theorem, konig-theorem, transitive-closure, simple-path, maximum-matching, topological-sort]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Chapter 26, Problem 26-2, Minimum path cover (the reduction of a DAG path cover to a maximum matching or flow)
  - paper: D. R. Fulkerson, Note on Dilworth's decomposition theorem for partially ordered sets, Proceedings of the American Mathematical Society 7(4), 701 to 702 (1956)
    title: Fulkerson, Dilworth's theorem by bipartite matching
    locator: the whole note (the split bipartite graph and the chain decomposition from a matching)
  - paper: John E. Hopcroft and Richard M. Karp, An n^(5/2) algorithm for maximum matchings in bipartite graphs, SIAM Journal on Computing 2(4), 1973
    title: Hopcroft and Karp, maximum bipartite matching
    locator: the main algorithm, O(m sqrt(n)) time
  - book: isbn:9780486402581
    title: Christos H. Papadimitriou and Kenneth Steiglitz, Combinatorial Optimization, Algorithms and Complexity, Dover, 1998
    locator: Chapter 10, Matching (Berge's theorem on augmenting paths and the bipartite matching algorithm)
---

This algorithm covers the vertices of a [directed acyclic graph](/directed-acyclic-graph/) with the fewest vertex-disjoint paths. It splits every vertex $v$ into a left copy $v^{\text{out}}$ and a right copy $v^{\text{in}}$, turns each arc $u \to v$ into an edge $u^{\text{out}} v^{\text{in}}$, and finds a maximum [bipartite matching](/bipartite-matching/). A matched edge means that $v$ follows $u$ on a path, so every matched edge joins two paths into one, and the number of paths is $n - |M|$. With [Kuhn's augmenting paths](/kuhn-algorithm/) it runs in $O(n(n + m))$ time, and with [Hopcroft-Karp](/hopcroft-karp/) in $O(m\sqrt{n})$. The graph is directed and must have no cycle; parallel arcs are allowed, and isolated vertices become paths of one vertex. It solves the [minimum path cover problem](/minimum-path-cover-problem/).

## In plain words

You have tasks with "must come after" rules and no circular rules. Each worker does a chain of tasks, one after another, where each next task is allowed to follow the one before. Every task goes to exactly one worker. How few workers do you need?

Start with one worker per task. Each time you say "task $v$ comes right after task $u$", two chains join and you save one worker. Each task can have at most one task right after it and at most one right before it.

Choosing the most such pairs is a matching problem: pair "after" sides with "before" sides. The best matching saves the most workers.

## The problem

Given a directed acyclic graph $G = (V, A)$ with $V = \{0, \ldots, n - 1\}$, find a set of [simple paths](/simple-path/) such that every vertex lies on exactly one path, with as few paths as possible. A path may have one vertex and no arc. Parallel arcs are allowed and change nothing. If $G$ has a cycle, the reduction below can produce a cycle instead of a path, so the input is checked first; on general directed graphs the problem is NP-hard, since one path covers $G$ exactly when $G$ has a [Hamiltonian path](/hamiltonian-path/).

## The algorithm

The split graph $H$ has left vertices $u^{\text{out}}$, right vertices $v^{\text{in}}$, and the edge $u^{\text{out}} v^{\text{in}}$ for every arc $u \to v$; in the code, both copies of a vertex have the same number, and the adjacency list of $u$ is the list of right neighbours of $u^{\text{out}}$. Lines L3 to L11 are Kuhn's algorithm: from every left vertex in turn, a depth-first search looks for an augmenting path, and the stack is explicit. The list $\mathrm{via}$ holds the right vertex chosen at each stack level, so that the path is on the stack when a free right vertex is found.

```pseudo id=main
PATH-COVER(G)
L1  adj[u] ← the heads v of the arcs u → v, for every vertex u
L2  matchL[u] ← NIL and matchR[v] ← NIL for all vertices
L3  for each vertex r do
L4      visited[v] ← false and ptr[v] ← 0 for all v
L5      stack ← (r); via ← ()
L6      while stack is not empty do
L7          u ← top of stack; if ptr[u] = |adj[u]| then pop stack and pop via (if not empty); continue
L8          v ← adj[u][ptr[u]]; ptr[u] ← ptr[u] + 1; if visited[v] then continue; visited[v] ← true; append v to via
L9          if matchR[v] = NIL then
L10             for i ← 1 to |stack| do matchL[stack[i]] ← via[i]; matchR[via[i]] ← stack[i]  (flip the path) and leave the while loop
L11         else push matchR[v] onto stack
L12 for each vertex s with matchR[s] = NIL do
L13     start a path at s and follow matchL until it is NIL
L14 return the paths
```

A vertex $s$ with $\mathrm{matchR}[s] = \mathrm{NIL}$ has no chosen predecessor, so it starts a path, and $\mathrm{matchL}$ gives the next vertex.

## Example

Seven vertices and the arcs $0 \to 1$, $0 \to 2$, $1 \to 3$, $2 \to 3$, $3 \to 4$, $2 \to 5$, $5 \to 6$, $1 \to 5$, with the adjacency lists in this order.

| root | search | matching after it |
|---|---|---|
| 0 | $1^{\text{in}}$ is free | $0 \to 1$ |
| 1 | $3^{\text{in}}$ is free | $0 \to 1$, $1 \to 3$ |
| 2 | $3^{\text{in}}$ is taken by 1; push 1; $3^{\text{in}}$ is visited, $5^{\text{in}}$ is free; flip | $0 \to 1$, $1 \to 5$, $2 \to 3$ |
| 3 | $4^{\text{in}}$ is free | adds $3 \to 4$ |
| 4 | no arcs | no change |
| 5 | $6^{\text{in}}$ is free | adds $5 \to 6$ |
| 6 | no arcs | no change |

The matching has 5 edges, so the cover has $7 - 5 = 2$ paths. The vertices with no matched predecessor are 0 and 2, and following $\mathrm{matchL}$ gives the paths $0, 1, 5, 6$ and $2, 3, 4$. At root 2, the greedy choice $1 \to 3$ was undone by the augmenting path $2^{\text{out}}, 3^{\text{in}}, 1^{\text{out}}, 5^{\text{in}}$. One path cannot cover the graph: vertices 4 and 6 both have no outgoing arc, so both would have to be the last vertex of that path.

## Correctness

The matched edges, read as arcs, give every vertex at most one successor and at most one predecessor. In a graph without cycles such a set of arcs is a union of vertex-disjoint paths that covers $V$, with one path per vertex that has no predecessor; a path with $k$ vertices uses $k - 1$ arcs, so there are $n - |M|$ paths. Every path cover gives a matching in the same way, so a maximum matching gives a minimum cover. Kuhn's search finds an augmenting path from the root when one exists, and a left vertex that has no augmenting path at its turn never gets one later; by Berge's theorem, the final matching is maximum. The full proof is below.

## Complexity

The cost is in the [word RAM](/word-ram/) model with adjacency lists.

- **Line L1 and the acyclicity check.** $O(n + m)$.
- **One search, lines L4 to L11.** $O(n)$ to reset the arrays. Each left vertex enters the stack at most once per search, because it enters as $\mathrm{matchR}[v]$ of a newly visited $v$, and each arc is read at most once through $\mathrm{ptr}$. So $O(n + m)$.
- **All searches.** $n$ searches, $O(n(n + m))$ in total. The resets alone cost $\Theta(n^2)$, and the acyclicity check reads every arc, so the best case is $\Theta(n^2 + m)$, for example a graph with no arcs. Resetting only the marks that were set, with a list of visited vertices, lowers the best case to $\Theta(n + m)$ without changing the worst case.
- **Lines L12 to L14.** $O(n)$.

The extra space is $\Theta(n + m)$. With Hopcroft-Karp in place of lines L3 to L11, the time is $O(m\sqrt{n})$.

## Properties

- **Exact.** It returns a minimum cover, as explicit paths.
- **Deterministic and not recursive.**
- **Needs a DAG.** On a graph with a cycle, the matched arcs can close a cycle, and the result is a cover by paths and cycles. That cover is minimum among such covers, but it is not a path cover.
- **Any matching algorithm.** The reduction does not depend on how the matching is found.
- **Ties.** Different maximum matchings give different minimum covers; the number of paths is the same.

## Variants and improvements

- **Paths that may share vertices.** If the paths may share vertices, but every vertex must be on at least one path, apply the algorithm to the [transitive closure](/transitive-closure/) of $G$. A path in the closure is a chain of the reachability order, so this computes the minimum chain cover of a partial order, which equals the largest antichain by [Dilworth's theorem](/dilworth-theorem/). The closure costs $O(nm)$ time and can have $\Theta(n^2)$ arcs.
- **Maximum flow form.** Add a source joined to every $u^{\text{out}}$ and a sink joined from every $v^{\text{in}}$, all with capacity 1; a maximum flow is a maximum matching.
- **Faster matching.** Hopcroft-Karp gives $O(m\sqrt{n})$, and newer flow algorithms give better bounds for large graphs.
- **Weighted covers.** Give a cost to each arc used, or a cost per path; then the matching becomes a minimum cost assignment.
- **Paths and cycles on general digraphs.** The same matching gives a minimum cover by vertex-disjoint paths and cycles, where cycles are allowed; this is polynomial, unlike the pure path cover.
- **König's theorem.** The size of a maximum matching equals a minimum vertex cover of $H$, see [König's theorem](/konig-theorem/), which gives a certificate that the cover is minimum.

## When to use it

Use it to find the least number of chains or workers in a schedule with precedence rules, the least number of vehicles that serve trips when one vehicle can serve trip $v$ right after trip $u$ (an arc $u \to v$), or the width of a partial order through Dilworth's theorem. For large graphs, prefer Hopcroft-Karp for the matching. Do not use it on graphs with cycles.

## Pitfalls

- **Graphs with cycles.** A matching on the split graph of a cyclic graph can contain the arcs of a cycle, and following $\mathrm{matchL}$ from a start never reaches the vertices of that cycle. Check that the graph is acyclic, or use the cover by paths and cycles on purpose.
- **Disjoint against overlapping paths.** The algorithm counts vertex-disjoint paths. For paths that may share vertices, first take the transitive closure; without it the answer can be too large. On the arcs $0 \to 2$, $1 \to 2$, $2 \to 3$, $2 \to 4$, the disjoint cover needs 3 paths, while two overlapping paths $0, 2, 3$ and $1, 2, 4$ cover all vertices.
- **Greedy matching.** Choosing a successor for each vertex greedily is not optimal; augmenting paths are needed, as at root 2 in the example.
- **Not resetting visited per root.** Kuhn's search must clear the visited marks before each root; otherwise it misses augmenting paths.
- **Self-loops.** A self-loop $v \to v$ is a cycle; a matching may use $v^{\text{out}} v^{\text{in}}$, which is not a path arc.

## Implementations

## History

Dilworth proved in 1950 that the least number of chains that cover a finite partial order equals the largest antichain. Fulkerson (1956) gave a short proof with the split bipartite graph, so the chains come from a maximum matching, and König's theorem gives the antichain. The same reduction for path covers of DAGs is a standard exercise, for example Problem 26-2 in the third edition of Cormen, Leiserson, Rivest and Stein. Hopcroft and Karp (1973) gave the $O(m\sqrt{n})$ matching algorithm.

## References
