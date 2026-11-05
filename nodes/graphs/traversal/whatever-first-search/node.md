---
tag: 4TP999
kind: algorithm
slug: whatever-first-search
name: Whatever-first search
aliases:
- generic graph search
- generic traversal
area: graphs/traversal
level: core
summary: A generic graph traversal that keeps a bag of unvisited edges and repeatedly extracts one, with the bag's discipline giving depth-first or breadth-first search.
solves: [graph-reachability]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, T: the time of one bag operation}
  time: {worst: O(n + m T), best: Θ(n)}
  space: {extra: O(n + m)}
properties: {deterministic: true, recursive: false}
prereqs: [graph-traversal, queue, stack]
see_also: [breadth-first-search, depth-first-search, best-first-search, prim, dijkstra, iterative-depth-first-search, lexicographic-bfs, flood-fill]
sources:
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 5, Basic graph algorithms (the sections on whatever-first search, its analysis, and its important variants with a stack, a queue and a priority queue)
  - paper: doi:10.1137/050623498
    title: Derek G. Corneil and Richard M. Krueger, A unified view of graph searching, SIAM Journal on Discrete Mathematics 22(4), 1259 to 1276 (2008)
    locator: the generic search and the characterization of the orderings of BFS, DFS, LexBFS and MCS
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 20.2, Breadth-first search, and Section 20.3, Depth-first search (the queue and the stack disciplines)
---

Whatever-first search is the generic form of [graph traversal](/graph-traversal/). It keeps a *bag* of pairs $(p, v)$, each meaning "$v$ was seen from $p$". Each step takes some pair out of the bag, and if $v$ is not yet marked, marks it, records $p$ as its parent, and puts a pair $(v, w)$ into the bag for each neighbour $w$. The bag may be any container. With a [stack](/stack/) the search is [depth-first search](/depth-first-search/), with a [queue](/queue/) it is [breadth-first search](/breadth-first-search/), and with a [priority queue](/priority-queue/) it becomes [best-first search](/best-first-search/), which includes [Prim's](/prim/) and [Dijkstra's](/dijkstra/) algorithms. For every bag, the search marks exactly the vertices reachable from the start, and the parents form a tree on them. The name is from Jeff Erickson's textbook.

## In plain words

You explore a network from one starting point. You carry a bag of notes. Each note says "from here you can go to there".

Take any note out of the bag. If you have already been to "there", throw the note away. If not, go there, mark it, remember which note brought you, and write a new note for each road that leaves it.

When the bag is empty, you have been to every place you can reach, and the notes you remembered form a tree back to the start.

The only free choice is which note you take next. Always the newest note gives depth-first search. Always the oldest gives breadth-first search. The note with the best score gives best-first search.

## The problem

Given a directed or undirected graph $G = (V, E)$ in [adjacency lists](/adjacency-list/) and a vertex $s$, find the set of vertices reachable from $s$, and a tree rooted at $s$ whose paths are paths of $G$ to each of them. This is the [graph reachability](/graph-reachability/) problem with a certificate.

## The algorithm

The bag $B$ supports PUT and TAKE, and TAKE returns any item that is in the bag. Its rule, the *discipline*, decides which.

```pseudo id=main
WHATEVER-FIRST-SEARCH(G, s)
L1  for each vertex u ∈ V do mark[u] ← FALSE, π[u] ← NIL
L2  B ← empty bag, PUT(B, (NIL, s))
L3  while B is not empty do
L4      (p, v) ← TAKE(B)
L5      if mark[v] = FALSE then
L6          mark[v] ← TRUE, π[v] ← p
L7          for each w ∈ Adj[v] do PUT(B, (v, w))
L8  return mark, π
```

A vertex is marked when a pair for it is taken, not when it is put, so the bag can hold several pairs for one vertex. Line L5 throws away all of them except the first one taken. The test at line L5 is the whole correctness of the search: it makes each vertex scan its list at most one time.

**The main instances.**

| bag | TAKE returns | search | parent tree |
|---|---|---|---|
| [stack](/stack/), lists put in reverse order | the newest pair | [DFS](/depth-first-search/) | the depth-first tree of the recursive DFS from $s$ |
| [queue](/queue/) | the oldest pair | [BFS](/breadth-first-search/) | the BFS tree, a [shortest path tree](/shortest-path-tree/) |
| [priority queue](/priority-queue/), key $w(p, v)$ | the lightest edge | [Prim](/prim/) | a minimum spanning tree of the component |
| priority queue, key $\mathrm{dist}(p) + w(p, v)$ | the closest vertex | [Dijkstra](/dijkstra/) | a shortest path tree for nonnegative weights |
| priority queue, key from a heuristic | the most promising | [best-first search](/best-first-search/), [A*](/a-star-search/) | depends on the key |

With a stack, putting $\mathrm{Adj}[v]$ in reverse order makes the first neighbour come out first, and then the marks and the parents are exactly those of the recursive DFS that starts at $s$. With a queue, the first pair taken for $v$ is the first pair put for $v$, so $\pi[v]$ is the vertex that discovered $v$ first, as in BFS.

## Example

Take the undirected graph with vertices 0 to 3 and the edges $\{0,1\}$, $\{0,2\}$, $\{1,2\}$, $\{2,3\}$, with the lists $0: 1, 2$; $1: 0, 2$; $2: 0, 1, 3$; $3: 2$, and start at $s = 0$.

**Stack.** The top of the stack is on the right.

| step | taken | action | stack after the step |
|---|---|---|---|
| 1 | (NIL, 0) | mark 0 | (0,2) (0,1) |
| 2 | (0, 1) | mark 1, $\pi[1] = 0$ | (0,2) (1,2) (1,0) |
| 3 | (1, 0) | skip | (0,2) (1,2) |
| 4 | (1, 2) | mark 2, $\pi[2] = 1$ | (0,2) (2,3) (2,1) (2,0) |
| 5 | (2, 0) | skip | (0,2) (2,3) (2,1) |
| 6 | (2, 1) | skip | (0,2) (2,3) |
| 7 | (2, 3) | mark 3, $\pi[3] = 2$ | (0,2) (3,2) |
| 8 | (3, 2) | skip | (0,2) |
| 9 | (0, 2) | skip | empty |

The marking order is $0, 1, 2, 3$, and the tree is the path $0, 1, 2, 3$, the DFS tree.

**Queue.** The front of the queue is on the left.

| step | taken | action | queue after the step |
|---|---|---|---|
| 1 | (NIL, 0) | mark 0 | (0,1) (0,2) |
| 2 | (0, 1) | mark 1, $\pi[1] = 0$ | (0,2) (1,0) (1,2) |
| 3 | (0, 2) | mark 2, $\pi[2] = 0$ | (1,0) (1,2) (2,0) (2,1) (2,3) |
| 4 to 7 | (1,0), (1,2), (2,0), (2,1) | skip | (2,3) |
| 8 | (2, 3) | mark 3, $\pi[3] = 2$ | (3,2) |
| 9 | (3, 2) | skip | empty |

The tree has the edges $0 - 1$, $0 - 2$, $2 - 3$, the BFS tree, and the tree path to each vertex is a shortest path. Both runs put $2m + 1 = 9$ pairs and take 9.

## Correctness

The search marks only reachable vertices, because a pair $(p, v)$ is put only when $p$ is marked and $(p, v)$ is an edge. It marks every reachable vertex: on a path from $s$ to an unmarked $v$, the first unmarked vertex has a marked predecessor, which put a pair for it, and the bag is empty at the end, so that pair was taken and the vertex was marked. Each parent was marked before its child, so the parent chains reach $s$. None of this depends on the discipline of the bag. The full proof is below.

## Complexity

Let $T$ be the time of one PUT or TAKE.

- **Line L1.** $\Theta(n)$. With a dictionary for the marks, it can be skipped, and the search then costs nothing for vertices it does not reach.
- **Puts.** Line L7 runs one time for each marked vertex, and it puts one pair for each entry of its list. With $n_s$ reachable vertices and $m_s$ edges out of them, there are at most $m_s + 1$ puts for a directed graph and $2 m_s + 1$ for an undirected one.
- **Takes.** Each pair is taken at most one time, so there are at most as many takes as puts.

So the time is $O(n + m T)$. For a stack or a queue $T = O(1)$, and the time is $O(n + m)$. For a [binary heap](/binary-heap/), $T = O(\log m) = O(\log n)$ for a simple graph, and the time is $O(n + m \log n)$. The bag can hold $\Theta(m)$ pairs at once, as in the queue example above, so the extra space is $O(n + m)$. The best case is a start vertex without edges, where only line L1 costs, $\Theta(n)$.

## Properties

- **One loop for all searches.** The code of lines L1 to L8 does not depend on the bag. Only the order of the marks and the shape of the tree change.
- **Deterministic.** For a fixed bag rule, a fixed order of the lists and fixed tie breaking, the result is fixed.
- **Not recursive.** The bag replaces the call stack, so long paths do not overflow.
- **Space.** Pairs for marked vertices stay in the bag until they are taken. A variant that does not put a pair $(v, w)$ when $w$ is already marked has the same output and often a smaller bag, but the bound $O(m)$ is the same.
- **Reach only.** The search visits the vertices reachable from $s$. For a whole graph, restart it from each unmarked vertex, which gives a whatever-first forest.

## Variants and improvements

- **Mark on put.** For a queue, the vertex can be marked when its first pair is put. Then each vertex is put at most once, the queue holds at most $n$ vertices, and the result is the usual [breadth-first search](/breadth-first-search/). For a stack, marking on put does not give a depth-first order: it gives a tree where the children of a vertex are all its unmarked neighbours.
- **Iterative DFS.** A stack of pairs (vertex, position in its list) gives DFS with a stack of size at most $n$ and also the finish times. See [nonrecursive depth-first search](/iterative-depth-first-search/).
- **Best-first search.** With a priority queue and a key on the pairs, the search becomes [best-first search](/best-first-search/). Prim's and Dijkstra's algorithms are the two classic keys.
- **Graph searches on chordal graphs.** [Lexicographic BFS](/lexicographic-bfs/) and [maximum cardinality search](/maximum-cardinality-search/) take the next vertex by a rule on the labels of the vertices. Corneil and Krueger describe BFS, DFS and these searches as restrictions of one generic search, by the orders of vertices that each can produce.
- **Implicit graphs.** The lists can be computed on the fly, as in [flood fill](/flood-fill/) on a grid and in [state-space search](/state-space-search/).

## When to use it

Use the generic form to explain and to prove facts that hold for all searches, such as "the marked set is the reachable set". In code, pick the discipline that the task needs: a queue for fewest edges, a stack or recursion for structure such as cycles and orders, and a priority queue for weighted problems. Use the generic form directly when only reachability matters and any order is fine, as in [flood fill](/flood-fill/) or garbage marking.

## Pitfalls

- **Marking on put with a stack.** With a stack, a vertex must be marked when it is taken, as in line L6. Marking it when it is put gives a valid tree, but not a depth-first tree, and the order is not a DFS order.
- **Missing the test of line L5.** Without it, vertices on a cycle are scanned again and again, and the search does not stop.
- **Bag of vertices only.** If the bag holds only $v$ and not the pair $(p, v)$, the parent is lost. Store the pair, or set the parent at the put.
- **Size of the bag.** A bag that keeps all pairs can grow to $\Theta(m)$ items. On a dense graph this is much more than $n$.

## Implementations

## History

Breadth-first and depth-first search were known long before their common form was named. Jeff Erickson calls the generic form "whatever-first search" in his textbook, and shows that a stack, a queue and a priority queue as the bag give depth-first search, breadth-first search and best-first search. Corneil and Krueger, in 2008, gave a unified view of graph searches by the orders of the vertices that they can produce.

## References
