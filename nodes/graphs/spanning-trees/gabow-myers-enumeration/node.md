---
tag: NE4VW0
kind: algorithm
slug: gabow-myers-enumeration
name: Gabow-Myers spanning tree enumeration algorithm
aliases:
- Gabow-Myers algorithm
area: graphs/spanning-trees
level: research
summary: Lists all spanning trees of a graph by depth-first backtracking with bridge tests, in O(n + m + nN) time for N trees of an undirected graph and O(n + m) space.
solves: [spanning-tree-enumeration]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, N: the number of spanning trees}
  time: {worst: O(n + m + n N)}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: true}
prereqs: [spanning-tree, spanning-tree-enumeration, bridge, depth-first-search, generic-backtracking-algorithm, connected-graph]
see_also: [counting-spanning-trees, matrix-tree-theorem, bridge-finding, reverse-search, arborescence, aldous-broder, second-best-mst, fundamental-cycle]
sources:
  - paper: doi:10.1137/0207024
    title: "Harold N. Gabow and Eugene W. Myers, Finding all spanning trees of directed and undirected graphs, SIAM Journal on Computing 7(3) (1978), 280-287"
    locator: the whole paper (the backtracking algorithm GROW, the bridge test that uses the last tree found, O(V + E + VN) time for undirected graphs and O(V + E + EN) for directed graphs, O(V + E) space)
  - paper: doi:10.1002/net.1975.5.3.237
    title: "Ronald C. Read and Robert E. Tarjan, Bounds on backtrack algorithms for listing cycles, paths, and spanning trees, Networks 5(3) (1975), 237-252"
    locator: the whole paper (backtracking with bridge tests, O(V + E + EN) time and O(V + E) space)
  - paper: doi:10.1137/S009753979225030X
    title: "Sanjiv Kapoor and H. Ramesh, Algorithms for enumerating all spanning trees of undirected and weighted graphs, SIAM Journal on Computing 24(2) (1995), 247-265"
    locator: the whole paper (O(N + V + E) time when only the change from one tree to the next is output)
---

The Gabow-Myers algorithm lists every [spanning tree](/spanning-tree/) of a graph exactly once by [backtracking](/generic-backtracking-algorithm/). It grows a partial tree $T$ from a fixed root. At each level it takes an edge $e$ that leaves $T$ and splits the search in two: first all trees that contain $e$, then all trees that avoid $e$. It stops splitting at that level as soon as $e$ is a [bridge](/bridge/) of the remaining graph, because then every remaining tree must contain $e$. Every branch of the search ends in a tree, so no work is wasted on dead ends. Gabow and Myers (1978) grow $T$ in [depth-first](/depth-first-search/) order, which lets the bridge test reuse the last tree found. This gives $O(n + m + nN)$ time for the $N$ trees of an undirected graph, which is optimal when each tree is written out in full as $n - 1$ edges, and $O(n + m)$ space. The same method lists the spanning [arborescences](/arborescence/) of a directed graph in $O(n + m + mN)$ time.

## In plain words

You want to write down every way to connect all the towns of a road network with a tree of roads. Start at one town. Look at a road that leaves the towns you have reached. First, decide to use it, and list everything that follows from that choice. Then decide never to use it, cross it off the map, and list everything again.

There is one shortcut. If crossing the road off would cut the map into two pieces, every tree needs that road, so the "never use it" branch is empty and you do not explore it. Because of the shortcut, every path you explore ends in a real tree, and the work stays proportional to the number of trees you list.

## The problem

The input is an undirected graph $G = (V, E)$ with $n$ vertices $0, \dots, n - 1$ and $m$ edges. Parallel edges are distinct edges, so they give distinct trees. Self-loops are allowed and lie in no tree. The graph has no weights, so the question of ties does not arise. The output is the list of all spanning trees of $G$, each exactly once. If $G$ is not [connected](/connected-graph/), it has no spanning tree and the list is empty. This page enumerates trees, not forests, so it does not return a spanning forest per component.

The number $N$ of trees can be computed in advance by the [matrix-tree theorem](/matrix-tree-theorem/). It can be exponential in $n$, for example $n^{n-2}$ for the complete graph, which is why the cost is measured per tree listed.

## The algorithm

The graph $G$ is global, and deletions from it are undone on the way back. $V(T)$ is the root together with the ends of the edges of $T$. The stack $F$ always holds exactly the edges of the current $G$ with one end in $V(T)$ and the other outside.

```pseudo id=main
GROW(T, F)
L1  if T has n − 1 edges then output T and return
L2  R ← empty list                                  ▷ edges deleted at this level
L3  repeat
L4      pop e = (v, w) from F, with v ∈ V(T) and w ∉ V(T)
L5      remove from F the edges (x, w) with x ∈ V(T); push onto F the edges (w, y) of G with y ∉ V(T) ∪ {w}
L6      GROW(T ∪ {e}, F)                            ▷ all trees that contain T and e
L7      undo line L5
L8      delete e from G; append e to R              ▷ from now on, trees that avoid e
L9      b ← (G is disconnected)                      ▷ was e a bridge?
L10 until b
L11 put the edges of R back into G, and push them back onto F, last deleted first
```

The top-level call checks that $G$ is connected, marks the root $0$ as the only vertex of $T$, and calls GROW with $T = \emptyset$ and $F$ the non-loop edges at $0$. Pushing the new edges at $w$ on top of $F$ at line L5 makes the search depth-first: the next edge to branch on leaves the most recently reached vertex. The order in which the trees appear depends on the order of the edges, but the set of trees does not.

## Example

The graph has the vertices $a$ to $f$ (0 to 5) and the edges $ab$, $ac$, $bc$, $bd$, $cd$, $ce$, $de$, $df$, $ef$ (indices 0 to 8). It has 55 spanning trees.

At the top level, $F = [ab, ac]$, with $ac$ on top.

| step | line | action | $F$ after the step (top on the right) |
|---|---|---|---|
| 1 | L4 | pop $ac$, reach $c$ | $[ab]$ |
| 2 | L5 | push the edges at $c$ that lead out: $bc$, $cd$, $ce$ | $[ab, bc, cd, ce]$ |
| 3 | L4, L5 | pop $ce$, reach $e$; push $de$, $ef$ | $[ab, bc, cd, de, ef]$ |
| 4 | L4, L5 | pop $ef$, reach $f$; push $df$ | $[ab, bc, cd, de, df]$ |
| 5 | L4, L5 | pop $df$, reach $d$; remove $cd$ and $de$, which now end in $T$; push $bd$ | $[ab, bc, bd]$ |
| 6 | L4, L1 | pop $bd$, reach $b$; $T$ has 5 edges | output $\{ac, ce, ef, df, bd\}$ |

The next two outputs replace $bd$ by $bc$ and then by $ab$. These are the other edges that can reach $b$ once $d$ is in $T$.

At the top level, the branch "$ac \in T$" lists 34 trees. Then line L8 deletes $ac$. The graph stays connected, so the loop goes on. It pops $ab$, and the branch "$ab \in T$, $ac \notin T$" lists 21 trees. Deleting $ab$ as well isolates $a$, so line L9 finds that $ab$ was a bridge and the loop stops. In total $34 + 21 = 55$ trees are listed, each once.

## Correctness

**Theorem.** If $G$ is connected, the top-level call outputs each spanning tree of $G$ exactly once, and it terminates. If $G$ is disconnected, it outputs nothing.

When GROW is called, $T$ is a tree on $V(T)$, the current graph is connected, and $F$ is the set of edges of the current graph that leave $V(T)$. Under these conditions, GROW outputs each spanning tree of the current graph that contains $T$ exactly once, and it restores $G$ and $F$ before it returns. The proof is by induction on $n - 1 - |T|$. Let $e_1, e_2, \dots$ be the edges popped at line L4. A spanning tree that contains $T$ is listed in iteration $j$ when $e_j$ is the first of these edges it contains. It is listed there by the recursive call, because the tree avoids the deleted edges $e_1, \dots, e_{j-1}$. So no tree is listed twice. Every tree is listed, because the loop stops only when the deletions disconnect $G$, and at that point no spanning tree avoids all of $e_1, \dots, e_k$. The loop never pops from an empty $F$, because a connected graph has an edge leaving $V(T)$ whenever $V(T) \ne V$. Each iteration deletes an edge, so the loop terminates. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the word RAM.

- **No dead ends.** Each call at line L6 is made with a connected graph and a tree $T \cup \{e\}$. The tree extends to a spanning tree, so every call outputs at least one tree. The calls form a recursion tree whose leaves are the $N$ outputs, and whose depth is $n - 1$. So there are at most $(n - 1)N + 1$ calls.
- **The bridge test of Gabow and Myers.** Line L9 is the expensive step. Gabow and Myers grow $T$ depth-first, so that the last tree output in the branch "$e \in T$" is a depth-first search tree of the current graph. They then decide whether $e$ is a bridge with a scan whose cost is charged to the trees already output. With this test, and with the stack operations of line L5 charged in the same way, the total time is $O(n + m + nN)$ for an undirected graph, and the space is $O(n + m)$ (Gabow and Myers, 1978).
- **Optimality.** Writing out $N$ trees of $n - 1$ edges each takes $\Omega(nN)$ time, and reading the graph takes $\Omega(n + m)$. So $O(n + m + nN)$ is optimal for this output format. Kapoor and Ramesh (1995) reach $O(n + m + N)$ by printing only the difference between consecutive trees.
- **The implementation on this site** tests for a bridge with a plain graph search costing $O(n + m)$. It also saves a copy of $F$ at each level instead of undoing line L5 in place. So it takes $O(n + m + n(n + m)N)$ time, and $O(nm)$ space for the saved copies. Its output is the same.

| claim | bound | case |
|---|---|---|
| time, Gabow and Myers, undirected | $O(n + m + nN)$ | worst |
| time, Gabow and Myers, directed | $O(n + m + mN)$ | worst |
| time, implementation here | $O(n + m + n(n + m)N)$ | worst |
| space, Gabow and Myers | $O(n + m)$ | worst |

## Properties

- **Exhaustive and repetition-free.** Every spanning tree appears exactly once.
- **Output-sensitive.** The work is bounded by a linear term plus a cost per tree, with no exponential overhead on graphs that have few trees.
- **Deterministic.** The order of the output is fixed by the order of the edges.
- **Polynomial delay.** Between two outputs, the recursion goes up and down at most $n - 1$ levels, so the delay is polynomial. The implementation here has delay $O(n(n + m))$.

## Variants and improvements

- **Read and Tarjan (1975).** The same backtracking with bridge tests, in $O(n + m + mN)$ time and $O(n + m)$ space. Gabow and Myers improve the undirected bound to $O(n + m + nN)$ by growing $T$ depth-first.
- **Directed graphs.** Gabow and Myers list the spanning [arborescences](/arborescence/) from a root by the same scheme. A bridge becomes an arc whose deletion makes some vertex unreachable from the root. The time is $O(n + m + mN)$.
- **Listing by changes.** Kapoor and Ramesh (1995) arrange the trees so that consecutive trees differ by one exchange of edges, $T - f + e$ with $f$ on the [fundamental cycle](/fundamental-cycle/) of $e$. They print only the exchange, in $O(N + n + m)$ total time.
- **[Reverse search](/reverse-search/).** Avis and Fukuda's general method lists spanning trees by walking a tree of exchanges defined implicitly. It needs no stack of the search, and it gives polynomial delay.
- **Sampling instead of listing.** When $N$ is too large to list, [Aldous-Broder](/aldous-broder/) and Wilson's algorithm draw one tree uniformly at random.

## When to use it

Use it when every spanning tree must actually be visited, for example to check a property on each tree, or to compute a quantity that has no formula, on graphs with a moderate number of trees. To only count the trees, use the [matrix-tree theorem](/matrix-tree-theorem/), which takes polynomial time even when $N$ is exponential. To find the best tree under a weight, use a [minimum spanning tree](/minimum-spanning-tree/) algorithm. To find the next best tree, use the [second-best MST](/second-best-mst/) method.

## Pitfalls

- **Checking connectivity before deleting.** The test at line L9 must be made after $e$ is deleted. A test made before line L8 would ask whether the graph *with* $e$ is connected, which is always true. The loop would then pop from an empty $F$.
- **Stale edges in $F$.** When $w$ joins $T$, the edges from $T$ to $w$ must leave $F$ at line L5. Otherwise the search pops an edge whose ends are both in $T$, closes a cycle, and lists non-trees. In the implementation, this filter must run before $w$ is marked as a tree vertex. The tests caught this bug in a draft, which listed 58 "trees" for the 55-tree example.
- **Restoring the deleted edges.** Line L11 must put the deleted edges back in the reverse order of deletion. Otherwise the parent level sees a changed $F$ and lists some trees twice.
- **Parallel edges and loops.** Parallel edges must be kept apart by index. If they are merged, the count is wrong. A self-loop must never enter $F$.
- **Disconnected input.** Without the initial connectivity check, the root level would pop from an empty $F$ instead of listing nothing. The disconnected tests cover this case.

## Implementations

## History

Minty (1965) gave an early method for listing the spanning trees of a graph, and many methods followed. Read and Tarjan (1975) analysed backtracking with bridge tests and obtained $O(V + E + EN)$ time with linear space for spanning trees, cycles and paths. Gabow and Myers (1978) refined the method for undirected graphs to $O(V + E + VN)$, which is optimal when the trees are written out. They also extended it to the arborescences of directed graphs. Kapoor and Ramesh (1995) obtained $O(N + V + E)$ for the listing of exchanges.

## References
