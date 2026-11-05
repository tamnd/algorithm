---
tag: 0RC5G2
kind: algorithm
slug: yen-k-shortest-paths
name: Yen's algorithm
aliases:
- Yen's k shortest loopless paths
area: graphs/shortest-paths
level: advanced
summary: Finds the k shortest loopless paths by repeated spur-path computations with Dijkstra.
solves: [k-shortest-paths]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, k: the number of paths asked for}
  time: {worst: O(k n (m + n log n))}
  space: {extra: O(k n^2 + m)}
properties: {deterministic: true, recursive: false}
prereqs: [k-shortest-paths, dijkstra, shortest-path]
see_also: [k-shortest-paths, replacement-paths, dijkstra, eppstein-k-shortest-paths, shortest-path-tree, single-pair-shortest-path, binary-heap, fibonacci-heap]
sources:
  - paper: doi:10.1287/mnsc.17.11.712
    title: Jin Y. Yen, Finding the K shortest loopless paths in a network, Management Science 17(11), 712 to 716 (1971)
    locator: the whole paper (root and spur paths, the lists A and B, and the analysis)
  - paper: "Eugene L. Lawler, A procedure for computing the K best solutions to discrete optimization problems and its application to the shortest path problem, Management Science 18(7), 401 to 405 (1972)"
    locator: the partition of the solution space and the saving of spur computations
  - paper: "John Hershberger, Matthew Maxel and Subhash Suri, Finding the k shortest simple paths, a new algorithm and its implementation, ACM Transactions on Algorithms 3(4), article 45 (2007)"
    locator: the description of Yen's algorithm and the speed-up by replacement paths
  - paper: doi:10.1137/S0097539795290477
    title: David Eppstein, Finding the k shortest paths, SIAM Journal on Computing 28(2), 652 to 673 (1998)
    locator: the introduction, on loopless paths against paths with repeated vertices
---

Yen's algorithm lists the $k$ shortest simple paths from $s$ to $t$ in a directed graph with nonnegative weights, in nondecreasing order of weight. It finds the first path with [Dijkstra's algorithm](/dijkstra/). To find the next path, it takes each vertex of the last path found as a *spur vertex*: it keeps the part of that path up to the spur vertex, the *root*, blocks the arcs that earlier paths with the same root took next, blocks the other root vertices, and finds a shortest *spur path* from the spur vertex to $t$. Root plus spur path is a candidate. The cheapest candidate not yet output is the next path. With up to $n$ Dijkstra runs per path, the time is $O(kn(m + n \log n))$. It solves the [k shortest paths](/k-shortest-paths/) problem for simple paths.

## In plain words

You want the best route, then the second best, then the third, and no route may visit a place twice.

The best route is easy: use Dijkstra. For the next one, note that any other route must leave the best route somewhere. So for each place on the last route found, follow that route up to the place, then forbid the roads that the routes found so far took from there, and find the cheapest way on to the goal without going back to places already used. Each try gives a new candidate route. Keep all candidates in a pile, and the cheapest one in the pile is the next best route.

## The problem

The input is a directed graph $G = (V, E)$ with $n = |V|$, $m = |E|$, weights $w : E \to \mathbb{R}_{\ge 0}$, vertices $s, t$ and an integer $k \ge 1$. The output is a list $A_1, \ldots, A_{k'}$ of distinct simple paths from $s$ to $t$, with $k' = \min(k, \text{the number of simple } s\text{-}t \text{ paths})$, such that $w(A_1) \le w(A_2) \le \cdots$ and no simple path outside the list is lighter than $A_{k'}$. Ties are broken in any way.

**Weight assumptions.** Nonnegative real weights, because each spur path is found by Dijkstra. Negative arcs are rejected, and so negative cycles cannot occur. Paths are sequences of vertices: parallel arcs are merged to the lightest one, and self-loops are ignored, since no simple path uses them. Integer weights are not needed. If $t$ is not reachable from $s$, the output is empty; if $s = t$, the only simple path is $\langle s \rangle$.

## The algorithm

$A$ is the list of paths output so far, and $B$ is a min-priority queue of candidates. Paths are lists of vertices, indexed from 0.

```pseudo id=main
YEN(G, w, s, t, K)
L1  A[1] ← a shortest s-t path found by DIJKSTRA; if there is none then return the empty list
L2  B ← an empty min-priority queue of paths, keyed by weight
L3  for k ← 2 to K do
L4      for i ← 0 to |A[k−1]| − 2 do
L5          spur ← A[k−1][i]; root ← A[k−1][0..i]
L6          block every arc (spur, p[i+1]) for each path p in A with p[0..i] = root
L7          block every vertex of root other than spur
L8          P ← a shortest spur-t path found by DIJKSTRA in the graph without the blocked arcs and vertices
L9          if P exists then add root followed by P[1..] to B, unless that path is already in A or B
L10         unblock all arcs and vertices
L11     if B is empty then return A
L12     A[k] ← EXTRACT-MIN(B)
L13 return A
```

Line L6 makes the candidate differ from every path in $A$ that shares the same root, so it is new. Line L7 keeps the candidate simple. The root is the same as the beginning of $A_{k-1}$, so its weight is a prefix sum of that path.

## Example

Take the graph with the vertices $C, D, E, F, G, H$ and the arcs $C \to D$ (3), $C \to E$ (2), $D \to F$ (4), $E \to D$ (1), $E \to F$ (2), $E \to G$ (3), $F \to G$ (2), $F \to H$ (1) and $G \to H$ (2), with $s = C$, $t = H$ and $K = 3$.

**Line L1.** Dijkstra gives $A_1 = C E F H$ with weight 5.

**$k = 2$, spurs on $A_1$.**

| $i$ | spur | root | blocked arcs | blocked vertices | spur path | candidate |
|---|---|---|---|---|---|---|
| 0 | $C$ | $C$ | $C \to E$ | none | $C D F H$ (8) | $C D F H$ (8) |
| 1 | $E$ | $C E$ | $E \to F$ | $C$ | $E G H$ (5) | $C E G H$ (7) |
| 2 | $F$ | $C E F$ | $F \to H$ | $C, E$ | $F G H$ (4) | $C E F G H$ (8) |

$B$ holds the weights 8, 7, 8, so $A_2 = C E G H$ with weight 7.

**$k = 3$, spurs on $A_2$.** For $i = 0$, both $A_1$ and $A_2$ start with $C \to E$, so $C \to E$ is blocked, and the spur path gives $C D F H$ again, which is already in $B$. For $i = 1$, the arcs $E \to F$ (from $A_1$) and $E \to G$ (from $A_2$) are blocked, and the spur path $E D F H$ gives $C E D F H$ (8). For $i = 2$, the spur $G$ has only the blocked arc $G \to H$, so there is no spur path. $B$ holds three paths of weight 8, and $A_3$ is one of them, $C D F H$ with the tie-break of the Python code.

The full list of simple paths has the weights 5, 7, 8, 8, 8, 11, 11. A path such as $C E D F G H$ (11) visits $D$ after $E$, which the shortest path never does; Yen finds it as a deviation of $C E D F H$.

**No path.** If $t$ is not reachable from $s$, line L1 returns the empty list. If fewer than $K$ simple paths exist, line L11 stops early.

## Correctness

**Theorem.** YEN returns $A_1, \ldots, A_{k'}$ as specified: distinct simple $s$-$t$ paths in nondecreasing order of weight, where each $A_j$ is a lightest simple path not among $A_1, \ldots, A_{j-1}$, and it stops early only when no other simple path exists.

The proof rests on one lemma. Let $P$ be a simple $s$-$t$ path not in $A = \{A_1, \ldots, A_{k-1}\}$. Choose the path $A_j$ that shares the longest common prefix with $P$, and among those the one with the largest $j$; let $P[0..i]$ be the common prefix. When the spurs of $A_j$ were computed, the arc $(P[i], P[i+1])$ was not blocked, since that would mean a path in $A$ with a longer common prefix, and the rest of $P$ avoids the root, since $P$ is simple. So the spur path at $P[i]$ gave a candidate $C$ with $w(C) \le w(P)$, and the choice of $j$ shows that $C$ is not in $A$. Hence $C$ is still in $B$, and the minimum of $B$ weighs at most $w(P)$. The full proof is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

- **Spur computations.** The path $A_{k-1}$ has at most $n$ vertices, so each round runs Dijkstra at most $n - 1$ times. With a [Fibonacci heap](/fibonacci-heap/), each run takes $O(m + n \log n)$, so the total is $O(kn(m + n \log n))$ in the worst case. With a [binary heap](/binary-heap/), as in the Python code, it is $O(kn(m + n) \log n)$.
- **Blocked arcs.** Line L6 looks at the paths in $A$, $O(kn)$ work per spur if done naively, or $O(1)$ amortized per blocked arc with a prefix tree (trie) of the paths in $A$. This is dominated by Dijkstra.
- **Candidates.** Each round adds at most $n - 1$ candidates, so $B$ holds $O(kn)$ paths of up to $n$ vertices: $O(kn^2)$ space if paths are stored in full, plus $O(m)$ for the graph. Storing each candidate as a pointer to its parent path and its spur gives $O(kn + m)$.

## Properties

- **Simple paths only.** Every output path is loopless. For walks that may repeat vertices, [Eppstein's algorithm](/eppstein-k-shortest-paths/) is much faster.
- **Incremental.** The paths come out one at a time in order, so the caller can stop as soon as one meets an extra condition, for example a path that avoids a given set of vertices.
- **Exact under ties.** With equal weights, the order among them depends on the tie-break of $B$, but the list of weights is unique.
- **Deterministic.** With a fixed tie-break, the output is fixed.

## Variants and improvements

- **Lawler's saving.** A candidate that came from the spur at index $i$ of its parent path does not need spurs at indices below $i$, because those deviations were already tried from the parent. This saves many Dijkstra runs in practice, with the same worst-case bound.
- **Undirected graphs.** Katoh, Ibaraki and Mine (1982) find $k$ shortest simple paths in an undirected graph in $O(k(m + n \log n))$ time, a factor $n$ better.
- **Replacement paths.** All spur paths of one round are [replacement paths](/replacement-paths/) of the last path with a growing set of blocked vertices. Hershberger, Maxel and Suri compute them together with one shortest-path tree in most cases, and fall back to Yen when this fails.
- **Reverse trees.** Many codes compute one shortest-path tree to $t$ first and use it to stop each spur search early, or to skip spurs whose best completion is already known.
- **Negative weights.** With negative arcs and no negative cycle, a [potential](/potential-function-reduced-costs/) from one Bellman-Ford run makes all weights nonnegative and keeps the order of $s$-$t$ paths, so Yen applies to the reduced costs.

## When to use it

Use Yen's algorithm when you need the $k$ best simple routes between two points, for $k$ up to a few hundred, for example in route planning with alternatives, in network design with backup routes, or in biology for alternative pathways. For walks with repeated vertices, use Eppstein. For large $k$ on undirected graphs, use the Katoh-Ibaraki-Mine algorithm, and on large directed graphs, use an implementation with Lawler's saving and replacement paths.

## Pitfalls

- **Blocking only the arc of $A_{k-1}$.** Line L6 must block the next arc of every path in $A$ with the same root, not only the arc of the last path. Otherwise the spur search can return a path that is already in $A$.
- **Not blocking the root vertices.** Without line L7, the spur path can go back through the root, and the candidate is not simple.
- **Duplicates in $B$.** The same candidate can come from different parents. Without the test of line L9, it is output twice.
- **Running Dijkstra on negative weights.** The spur paths are then wrong without any error. Reweight first, or reject the input, as the Python code does.
- **Parallel arcs.** If a path is a list of vertices, two parallel arcs give the same path. Merge them first, or represent paths by arcs.

## Implementations

## History

Jin Y. Yen published the algorithm in Management Science in 1971; the same idea of splitting the set of remaining paths by their first deviation appears in work of Hoffman and Pavley (1959) for paths that may repeat vertices. Lawler (1972) put it in a general scheme for the $k$ best solutions of discrete optimization problems and noted the saving of spur computations. Katoh, Ibaraki and Mine (1982) gave a faster algorithm for undirected graphs. Hershberger, Maxel and Suri (2003, 2007) sped up the directed case in practice with replacement paths, where the fast replacement-path step can fail on some directed graphs and then falls back to Yen's spur searches.

## References
