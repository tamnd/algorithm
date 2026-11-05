---
tag: WNETNH
kind: algorithm
slug: eppstein-k-shortest-paths
name: Eppstein's k shortest paths
aliases:
- Eppstein's algorithm
area: graphs/shortest-paths
level: research
summary: Enumerates k shortest (not necessarily simple) paths in O(m + n log n + k) time using a path-sidetrack structure.
solves: [k-shortest-paths]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges, k: the number of walks asked for}
  time: {worst: O(m + n log n + k log k), best: Θ(n + m)}
  space: {extra: O(m + n log n + k)}
properties: {deterministic: true, recursive: false}
prereqs: [k-shortest-paths, dijkstra, shortest-path-tree, potential-function-reduced-costs, leftist-heap, persistent-data-structure]
see_also: [yen-k-shortest-paths, best-first-search, binary-heap, fibonacci-heap, bellman-ford, negative-cycle, single-pair-shortest-path, a-star-search]
sources:
  - paper: doi:10.1137/S0097539795290477
    title: David Eppstein, Finding the k shortest paths, SIAM Journal on Computing 28(2), 652 to 673 (1998)
    locator: the definitions of sidetracks, the heaps H_out(v) and H_T(v), the path graph P(G), the bijection between paths in P(G) and s-t walks, and the O(m + n log n + k) bound with heap selection
  - paper: doi:10.1006/inco.1993.1030
    title: Greg N. Frederickson, An optimal algorithm for selection in a min-heap, Information and Computation 104(2), 197 to 214 (1993)
    locator: the O(k) selection of the k smallest elements of a heap-ordered tree of bounded degree, used for the O(k) term
  - paper: "Walter Hoffman and Richard Pavley, A method for the solution of the Nth best path problem, Journal of the ACM 6(4), 506 to 514 (1959)"
    locator: the description of the next-best path as a deviation from a shortest-path tree, the idea behind sidetracks
---

Eppstein's algorithm lists the $k$ lightest walks from $s$ to $t$ in a weighted directed graph, in order of weight. Walks may repeat vertices; for paths without repeated vertices see [Yen's algorithm](/yen-k-shortest-paths/). It computes one [shortest-path tree](/shortest-path-tree/) into $t$, describes every other walk by the edges where it leaves the tree, and builds a heap-ordered graph of bounded out-degree in which each walk is one path from a root. A [best-first search](/best-first-search/) of that graph produces the walks one by one, in $O(\log k)$ time each with a binary heap, or $O(1)$ each with Frederickson's heap selection. The preprocessing is one run of [Dijkstra's algorithm](/dijkstra/) plus $O(m + n \log n)$ heap work, so the total is $O(m + n \log n + k)$ for the $k$ walks, given implicitly. David Eppstein published it in 1994 (journal version 1998).

## In plain words

From every place there is a best way to the goal, and together these best ways form a tree. Any other route follows the tree most of the time and now and then takes a road off the tree, a *sidetrack*. Each sidetrack has a penalty: how much longer the trip gets than staying on the tree. A route's length is the best length plus the penalties of its sidetracks.

So the problem becomes: list the cheapest sequences of sidetracks. Eppstein keeps, for each place, a heap of the sidetracks still available from there on. Moving down a heap means "take a slightly worse sidetrack here instead", and jumping to the heap at the end of a sidetrack means "take this one and look for the next". No move makes a route cheaper, so a priority queue hands out the routes cheapest first.

## The problem

The input is a directed graph $G = (V, E)$ with $n$ vertices and $m$ edges, a real weight $w(u, v)$ on each edge, two vertices $s$ and $t$, and a number $k \ge 0$. A *walk* from $s$ to $t$ is a sequence of edges $e_1, \ldots, e_j$ with the tail of $e_1$ equal to $s$, the head of $e_j$ equal to $t$, and the head of each edge equal to the tail of the next; $j = 0$ is allowed when $s = t$. Vertices and edges may repeat, and two parallel edges give two different walks. The output is $k$ different $s$-$t$ walks $W_1, \ldots, W_k$ with $w(W_1) \le \cdots \le w(W_k)$ such that no other walk is lighter than $W_k$; if fewer than $k$ walks exist, all of them, in order.

**Weight assumptions.** Weights are any real numbers. Only the vertices that lie on some $s$-$t$ walk (reachable from $s$ and reaching $t$) matter, and the algorithm first restricts the graph to them. If that part has no negative cycle, the answer is well defined, and with nonnegative weights the tree is computed by Dijkstra's algorithm, otherwise by [Bellman-Ford](/bellman-ford/) (which changes the $n \log n$ term to $nm$). If a [negative cycle](/negative-cycle/) lies on some $s$-$t$ walk, walks around it get arbitrarily light, there is no lightest walk, and the algorithm reports this instead of an answer. Negative cycles that are not on any $s$-$t$ walk are ignored. Zero-weight cycles are allowed; they make infinitely many walks of the same weight, and the algorithm lists $k$ of them. If $t$ is not reachable from $s$, there is no walk and the output is empty.

## The algorithm

Let $d(v)$ be the distance from $v$ to $t$, and fix a shortest-path tree $T$ into $t$: every $v \ne t$ has one tree edge $(v, \mathrm{next}(v))$ with $d(v) = w(v, \mathrm{next}(v)) + d(\mathrm{next}(v))$. Every other edge $e = (u, x)$ is a *sidetrack*, with cost $\delta(e) = w(u, x) + d(x) - d(u) \ge 0$, its [reduced cost](/potential-function-reduced-costs/) for the potential $d$. A walk is determined by its sequence of sidetracks: from $s$ follow the tree until the tail of the first sidetrack, take it, follow the tree from its head to the tail of the next one, and so on, ending with the tree path to $t$. The weight of the walk is $d(s)$ plus the sum of the costs of its sidetracks.

For each vertex $v$, the sidetracks out of $v$ go into a heap $H_{\mathrm{out}}(v)$: the cheapest one at the root, the rest heap-ordered below it. The heap $H_G(v)$ holds the roots of $H_{\mathrm{out}}(u)$ for all $u$ on the tree path from $v$ to $t$, each with its $H_{\mathrm{out}}(u)$ below it. Because the tree path of $v$ is that of $\mathrm{next}(v)$ plus $v$, $H_G(v)$ is $H_G(\mathrm{next}(v))$ with one insertion, done persistently (a [persistent](/persistent-data-structure/) [leftist heap](/leftist-heap/) copies only $O(\log n)$ nodes), so all $n$ heaps take $O(n \log n)$ space together.

The *path graph* has a node for each heap node of every $H_G(v)$. From a node holding sidetrack $e$ it has an edge to each heap child $c$ of cost $\delta(c) - \delta(e)$, and a *cross edge* to the root of $H_G(\mathrm{head}(e))$ of cost $\delta(\text{that root})$. Every node has at most five out-edges, and all costs are nonnegative.

```pseudo id=main
EPPSTEIN(G, w, s, t, k)
L1  restrict G to the vertices on s-t walks; compute d(·) to t and a tree T (report a negative cycle if found)
L2  for each sidetrack e = (u, x): δ(e) ← w(u, x) + d(x) − d(u); heapify the sidetracks out of each u
L3  for each v in tree order from t: H_G(v) ← persistent insert of the best sidetrack of v into H_G(next(v))
L4  output the tree walk from s to t, of weight d(s)
L5  Q ← {(d(s) + δ(root of H_G(s)), root of H_G(s), ())}, if H_G(s) is not empty
L6  while fewer than k walks are output and Q ≠ ∅ do
L7      remove from Q the state (c, x, σ) with the least c
L8      output the walk with the sidetracks σ, e(x), of weight c
L9      for each heap child y of x: insert (c − δ(x) + δ(y), y, σ) into Q
L10     if H_G(head(e(x))) is not empty: insert (c + δ(its root), its root, σ + e(x)) into Q
L11 return the walks output
```

A state $(c, x, \sigma)$ stands for the walk whose sidetracks are $\sigma$ followed by the sidetrack $e(x)$ held at node $x$, and $c$ is its weight. Line L9 swaps the last sidetrack for a slightly costlier one from the same heap, and line L10 keeps the last sidetrack and makes room for one more after it. With $\sigma$ stored as a pointer to the parent state, each state takes $O(1)$ space, and the walk itself can be written out in time proportional to its length.

## Example

The vertices are $s, a, b, t$ and the edges $s \to a$ (1), $s \to b$ (2), $a \to b$ (0), $a \to t$ (3), $b \to t$ (1), $t \to s$ (4).

**Tree and sidetracks.** The distances to $t$ are $d(t) = 0$, $d(b) = 1$, $d(a) = 1$, $d(s) = 2$, and the tree edges are $s \to a$, $a \to b$, $b \to t$. The sidetracks and their costs are $s \to b$: $2 + 1 - 2 = 1$; $a \to t$: $3 + 0 - 1 = 2$; $t \to s$: $4 + 2 - 0 = 6$. The heaps along the tree are $H_G(t) = H_G(b) = \{t{\to}s\}$, $H_G(a) = \{a{\to}t, t{\to}s\}$ and $H_G(s) = \{s{\to}b, a{\to}t, t{\to}s\}$, each a chain here: $s{\to}b$ (1) above $a{\to}t$ (2) above $t{\to}s$ (6).

**Search.** The tree walk $s, a, b, t$ of weight 2 comes first. Then:

| pop | sidetracks | walk | weight | pushed |
|---|---|---|---|---|
| 1 | $s{\to}b$ | $s, b, t$ | 3 | child $a{\to}t$ at 4; cross to $H_G(b)$ at $3 + 6 = 9$ |
| 2 | $a{\to}t$ | $s, a, t$ | 4 | child $t{\to}s$ at 8; cross to $H_G(t)$ at 10 |
| 3 | $t{\to}s$ | $s, a, b, t, s, a, b, t$ | 8 | cross to $H_G(s)$ at $8 + 1 = 9$ |
| 4 | $s{\to}b$, $t{\to}s$ | $s, b, t, s, a, b, t$ | 9 | ... |
| 5 | $t{\to}s$, $s{\to}b$ | $s, a, b, t, s, b, t$ | 9 | ... |

So the six lightest walks weigh 2, 3, 4, 8, 9, 9. The two walks of weight 9 tie; either order is correct.

**Unreachable and negative cases.** If the edges $a \to t$ and $b \to t$ are removed, $t$ is not reachable from $s$ and the output is empty. If $a$ gets a self-loop of weight $-1$, then $a$ is on an $s$-$t$ walk, the walks $s, a, a, \ldots, a, t$ get arbitrarily light, and the algorithm reports a negative cycle. If instead a new vertex $z$ with edges $s \to z$ (1) and a self-loop at $z$ of weight $-1$ is added, $z$ does not reach $t$, line L1 removes it, and the answer is unchanged.

## Correctness

**Theorem.** If no negative cycle lies on an $s$-$t$ walk, the algorithm outputs $\min(k, N)$ different $s$-$t$ walks, where $N \le \infty$ is the number of $s$-$t$ walks, in nondecreasing order of weight, each with its correct weight, and no walk left out is lighter than the last one output. Otherwise it reports a negative cycle.

The proof has three parts. First, sidetrack sequences: a sequence of sidetracks $e_1, \ldots, e_j$ is the sidetrack sequence of a walk exactly when the tail of each $e_{i+1}$ lies on the tree path from the head of $e_i$ (and the tail of $e_1$ on the tree path from $s$), and then the walk is unique and weighs $d(s) + \sum \delta(e_i)$, because the reduced costs telescope and tree edges have reduced cost 0. Second, the path graph: $H_G(v)$ holds exactly the sidetracks whose tails lie on the tree path from $v$, each at one node with one heap path from the root, so the states of the search are in one-to-one correspondence with the nonempty valid sequences, and the cost of a state is the weight of its walk. Third, the search: every move costs at least zero (heap order, and $\delta \ge 0$ because $d$ is a distance function), the states form a tree under "parent state", and best-first search on such a tree removes states in nondecreasing order of cost, each exactly once. The tree walk weighs $d(s)$, the minimum. The negative-cycle report comes from line L1: after the restriction, every cycle lies on an $s$-$t$ walk, so a negative cycle is found exactly when one lies on such a walk. The full proof is in the proof file below.

## Complexity

The model is the [word RAM](/word-ram/).

- **Preprocessing.** Restricting the graph is two graph searches, $O(n + m)$. Dijkstra's algorithm with a [Fibonacci heap](/fibonacci-heap/) takes $O(m + n \log n)$. Heapifying the sidetracks of every vertex takes $O(m)$, and the $n$ persistent insertions take $O(\log n)$ each, $O(n \log n)$ in total.
- **Enumeration.** Each removal from $Q$ inserts at most five states, so $Q$ holds $O(k)$ states and each operation costs $O(\log k)$ with a [binary heap](/binary-heap/): $O(k \log k)$ for $k$ walks. Eppstein replaces the best-first search by Frederickson's selection of the $k$ smallest nodes of a heap-ordered tree of bounded degree, which takes $O(k)$, giving $O(m + n \log n + k)$ in total.
- **Output.** Each walk is given implicitly, as a parent pointer and one sidetrack. Writing walk $W_i$ out explicitly takes time proportional to its number of edges, which can be far more than $n$ for walks around cycles.
- **Best case.** The two restriction searches are always needed, and the rest can cost $O(n + m)$, for example when $s$ has one edge to $t$ and $k = 1$; so the time is $\Theta(n + m)$ at best.
- **Space.** The persistent heaps take $O(m + n \log n)$, and the search $O(k)$.
- **Negative weights.** With Bellman-Ford for line L1, preprocessing takes $O(nm)$; the rest is unchanged.

## Properties

- **Walks, not simple paths.** The walks may repeat vertices. Listing the $k$ shortest simple paths is harder; Yen's algorithm takes $O(k n (m + n \log n))$.
- **Output-sensitive.** After preprocessing, each further walk costs $O(1)$ amortized with heap selection, or $O(\log k)$ with a priority queue.
- **Incremental.** The best-first version does not need $k$ in advance; it can stop whenever the caller has enough walks.
- **Ties.** Walks of equal weight come out in an order that depends on the heap; any order among ties is a correct answer.

## Variants and improvements

- **Lazy construction.** Jiménez and Marzal build the heaps only for the vertices that the enumeration actually reaches, which helps when $k$ is small.
- **Heuristic search.** The K* algorithm of Aljazzar and Leue runs [A*](/a-star-search/) instead of Dijkstra's algorithm, so the shortest-path tree is built only as far as the enumeration needs.
- **Negative weights.** With the tree from Bellman-Ford, all sidetrack costs are still nonnegative, and everything else is unchanged.
- **Simple paths.** For loopless paths, [Yen's algorithm](/yen-k-shortest-paths/) and its descendants solve a shortest-path problem per candidate; Eppstein's structure does not apply directly.

## When to use it

Use it when many alternative routes are needed and repeated vertices are acceptable or rare, for example in sequence alignment with several best alignments, in speech recognition and parsing, where the $k$ best derivations through a lattice are wanted, and as a building block for the $k$ best solutions of dynamic programs that are shortest paths in a DAG. On a DAG every walk is a simple path, so the algorithm gives the $k$ shortest simple paths there. When walks with repeated vertices are not allowed in a graph with cycles, use Yen's algorithm.

## Pitfalls

- **A zero-cost tree edge chosen by tightness alone.** With zero-weight cycles, a tight edge $d(u) = w(u, x) + d(x)$ need not be a tree edge; choosing tree edges by tightness can make the "tree" contain a cycle, and following it never reaches $t$. Take the tree edges from the shortest-path computation itself.
- **Vertices that cannot reach $t$.** Their distance is $\infty$, and $\infty - \infty$ appears in the sidetrack cost. Drop them, together with the vertices that $s$ cannot reach, before anything else; this also keeps negative cycles there from mattering.
- **Mutating heaps instead of copying.** $H_G(v)$ and $H_G(\mathrm{next}(v))$ share structure. Inserting in place destroys the heaps of the other vertices.
- **Parallel edges.** Two parallel edges are two walks. Identify sidetracks by the edge, not by the pair of endpoints.
- **Explicit walks blow up.** Walks around cycles can have many edges. Keep the parent-pointer form unless the walks are actually needed.

## Implementations

The Python version restricts the graph, computes the tree by Dijkstra's algorithm or by Bellman-Ford when there are negative weights (raising an error on a negative cycle on an $s$-$t$ walk), stores the sidetracks of each vertex as a binary heap array, builds $H_G$ as a persistent leftist heap, and runs best-first search with a binary heap. It returns the walks as vertex lists together with their weights.

## History

Hoffman and Pavley (1959) described next-best paths as deviations from a shortest-path tree. Eppstein's paper, first at FOCS 1994 and in the SIAM Journal on Computing in 1998, turned this into the path graph and reached $O(m + n \log n + k)$ with Frederickson's heap selection, which is optimal when the walks are given implicitly. Later work, such as the lazy variant of Jiménez and Marzal and the K* algorithm of Aljazzar and Leue, keeps the structure and reduces the preprocessing in practice.

## References
