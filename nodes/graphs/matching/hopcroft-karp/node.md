---
tag: V8H9RQ
kind: algorithm
slug: hopcroft-karp
name: Hopcroft-Karp algorithm
aliases:
- Hopcroft-Karp matching
area: graphs/matching
level: core
summary: Finds maximum bipartite matching in O(E√V) time by augmenting along a maximal set of shortest paths per phase.
solves: [bipartite-matching]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O((n + m) n^(1/2))}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false}
history:
  year: 1973
  people: [John Hopcroft, Richard Karp]
  note: Hopcroft and Karp published the phase method and its O(n^(1/2)) bound on the number of phases in 1973; Karzanov found the same bound independently for flows in unit networks.
prereqs: [bipartite-matching, augmenting-path, breadth-first-search]
see_also: [kuhn-algorithm, dinic, blocking-flow, level-graph, berge-lemma, hall-theorem, micali-vazirani-algorithm, edmonds-blossom]
sources:
  - paper: doi:10.1137/0202019
    title: John E. Hopcroft and Richard M. Karp, An n^(5/2) algorithm for maximum matchings in bipartite graphs, SIAM Journal on Computing 2(4), 225 to 231 (1973)
    locator: the whole paper (the phase lemma and the bound on the number of phases)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 25.1, Maximum bipartite matching (revisited)
  - book: isbn:9783540443896
    title: Alexander Schrijver, Combinatorial Optimization, Polyhedra and Efficiency
    locator: Section 16.4, An O(n^(1/2) m) algorithm, and Section 16.7a, Complexity survey
---

The Hopcroft-Karp algorithm finds a maximum matching in a [bipartite graph](/bipartite-graph/) by working in phases. Each phase runs one [breadth-first search](/breadth-first-search/) to find the length of a shortest [augmenting path](/augmenting-path/), and then one depth-first pass that augments along a maximal set of vertex-disjoint augmenting paths of that length. The shortest length grows from phase to phase, which caps the number of phases at $O(\sqrt n)$ and the running time at $O((n + m)\sqrt n)$. The graph is bipartite and unweighted; for general graphs the same bound needs the [Micali-Vazirani algorithm](/micali-vazirani-algorithm/).

## In plain words

People on one side want tasks on the other side, and each person can do only some tasks. The simple method, [Kuhn's algorithm](/kuhn-algorithm/), finds one chain of swaps at a time: a person without a task takes a task from someone, who takes another task, and so on until someone takes a free task. Each chain costs a full search.

Hopcroft-Karp first measures how short the shortest chain is. Then, in one sweep, it carries out as many chains of that shortest length as it can, as long as no two chains touch the same person or task. After the sweep, every remaining chain is longer. Long chains are rare when the matching is nearly done, so only a few sweeps are needed, about the square root of the number of people.

## The problem

The input is a bipartite graph $G = (X \cup Y, E)$ with the sides given, $n = |X| + |Y|$ vertices and $m$ edges, every edge joining $X$ to $Y$. The output is a matching $M$ of largest size $\nu(G)$, given by the arrays $\text{mate}$ on both sides, where $\text{mate}[v] = \text{NIL}$ for a free vertex. This is the [bipartite matching](/bipartite-matching/) problem.

**Assumptions.** The graph is unweighted and need not be connected. Isolated vertices, an empty side and parallel edges are allowed. If the sides are not known, a [bipartite test](/bipartite-testing/) finds them in $O(n + m)$ time. The graph must be bipartite: on an odd cycle the layers of the search are not well defined, and the method can miss augmenting paths; general graphs need [blossoms](/blossom/).

## The algorithm

Write $D$ for the number of $Y$ vertices on a shortest augmenting path, so that the path has $2D - 1$ edges. The labels $\text{dist}[x]$ on $X$ are the layers of the search.

```pseudo id=main
HOPCROFT-KARP(G = (X ∪ Y, E))
L1  for each vertex v do mate[v] ← NIL
L2  repeat
L3      for each x ∈ X do dist[x] ← 0 if mate[x] = NIL, else ∞
L4      Q ← a queue of the free vertices of X;  D ← ∞
L5      while Q is not empty do x ← DEQUEUE(Q)
L6          if dist[x] < D then for each edge xy do
L7              if mate[y] = NIL then D ← min(D, dist[x] + 1)
L8              else if dist[mate[y]] = ∞ then dist[mate[y]] ← dist[x] + 1;  ENQUEUE(Q, mate[y])
L9      if D = ∞ then return mate
L10     for each x ∈ X do
L11         if mate[x] = NIL and dist[x] = 0 then DFS(x)

DFS(x)
L12 d ← dist[x];  dist[x] ← ∞
L13 for each edge xy, each scanned once per phase, do
L14     if (mate[y] = NIL and d + 1 = D) or (mate[y] ≠ NIL and dist[mate[y]] = d + 1 and DFS(mate[y])) then
L15         mate[x] ← y;  mate[y] ← x;  return true
L16 return false
```

Lines L3 to L8 are a breadth-first search from all free vertices of $X$ at once. It follows an unmatched edge from $x$ to $y$ and then the matched edge from $y$ to its partner, so it explores [alternating paths](/alternating-path/), and $\text{dist}[x]$ is the number of matched edges on a shortest alternating path from a free vertex to $x$. The search stops expanding at the layer where it first sees a free $Y$ vertex. Lines L10 to L16 are the depth-first pass. It moves only from layer $d$ to layer $d + 1$, and it sets $\text{dist}[x] \leftarrow \infty$ when it enters $x$, so no vertex is entered twice in a phase and the paths found are vertex-disjoint. When it reaches a free vertex in the last layer, line L15 flips the edges of the path on the way back. The implementation keeps the path on an explicit stack instead of using recursion, because a path can have $\Theta(n)$ vertices.

## Example

The graph has $X = \{1, 2, 3, 4\}$, $Y = \{a, b, c, d\}$ and the edges $1a$, $1b$, $2a$, $3b$, $3c$, $4c$, $4d$, listed in this order.

| phase | layers $\text{dist}$ after the search | $D$ | paths found | matching after the phase |
|---|---|---|---|---|
| 1 | $1, 2, 3, 4$: 0 | 1 | $1a$, $3b$, $4c$; vertex 2 finds $a$ taken and fails | $\{1a, 3b, 4c\}$ |
| 2 | $2$: 0, $1$: 1, $3$: 2, $4$: 3 | 4 | $2\,a\,1\,b\,3\,c\,4\,d$, with 7 edges | $\{2a, 1b, 3c, 4d\}$ |
| 3 | no free vertex in $X$, the queue is empty | $\infty$ | none | stop, $\nu = 4$ |

In phase 1 every free vertex is in layer 0 and every augmenting path is a single edge, so the pass is a greedy matching. The set $\{1a, 3b, 4c\}$ is maximal: vertex 2 has only the neighbour $a$, which is taken. In phase 2 the search goes $2 \to a \Rightarrow 1 \to b \Rightarrow 3 \to c \Rightarrow 4 \to d$, where $\to$ is an unmatched edge and $\Rightarrow$ a matched one, and $D$ grew from 1 to 4. Kuhn's algorithm runs one search for each vertex of $X$, four here, and its last search walks the whole chain $4\,c\,3\,b\,1\,a\,2$ before it finds $d$; Hopcroft-Karp runs three searches.

**No perfect matching.** With $X = \{A, B, C, D, E\}$, $Y = \{1, 2, 3, 4, 5\}$, $A$, $B$, $C$ each adjacent to 1 and 2, $D$ to 3 and 4 and $E$ to 4 and 5, phase 1 matches $A1$, $B2$, $D3$, $E4$. Phase 2 starts from $C$ and reaches $A$ and $B$, whose other neighbours are 1 and 2 again, so $D = \infty$ and the answer is $\nu = 4$. The vertices reached, $\{C, A, B\}$ with neighbourhood $\{1, 2\}$, are a set that violates [Hall's condition](/hall-theorem/).

**Edge cases.** With no vertices, or with no edges, the first search finds no free $Y$ vertex and the empty matching is returned after one search. On the star with centre $x$ and four leaves, phase 1 matches $x$ to its first leaf and the next search stops.

## Correctness

The invariant is that $\text{mate}$ always describes a matching $M$, and each successful DFS in a phase flips an $M$-augmenting path of exactly $2D - 1$ edges, vertex-disjoint from the earlier paths of the phase. Each such flip raises $|M|$ by one. A phase that augments nothing is the last one: $D = \infty$ means that no alternating path from a free vertex of $X$ ends at a free vertex of $Y$, so there is no augmenting path, and $M$ is maximum by [Berge's lemma](/berge-lemma/). The paths found in one phase form a maximal set of vertex-disjoint shortest augmenting paths, and after augmenting along such a set every augmenting path is strictly longer. The full proof is in the proof files below.

## Complexity

The model is the [word RAM](/word-ram/); each operation on a vertex index costs $O(1)$.

- **One phase.** The search of lines L3 to L8 costs $O(n + m)$. In the pass, each vertex of $X$ is entered at most once, because line L12 sets its label to $\infty$, and each of its edges is scanned at most once. Flipping the paths costs their total length, at most $n$. So one phase costs $O(n + m)$.
- **Phases.** Let $\nu = \nu(G)$. The value $D$ grows by at least 1 per phase, so after $k$ phases every augmenting path has at least $k + 1$ edges outside $M$. A maximum matching $M^*$ and $M$ have $\nu - |M|$ vertex-disjoint augmenting paths in $M \triangle M^*$, each with at least $k + 1$ edges of $M^*$, so $\nu - |M| \le \nu / (k + 1)$. With $k = \lfloor \sqrt \nu \rfloor$ fewer than $\sqrt \nu$ augmentations remain, and each later phase does at least one. So there are at most $2\sqrt \nu + 1$ phases, and $\nu \le n / 2$.
- **Total.** $O((n + m)\sqrt n)$ time, which is $O(m\sqrt n)$ when there are no isolated vertices, and $\Theta(n + m)$ space for the adjacency lists, the labels, the queue and the stack.

The full argument is in the complexity proof below.

## Properties

- **Deterministic and exact.** The result is a maximum matching for every input; which one depends on the order of the adjacency lists.
- **Certificate.** The last search marks the vertices reachable by alternating paths from the free vertices of $X$. As in [Kőnig's theorem](/konig-theorem/), the unmarked vertices of $X$ and the marked vertices of $Y$ form a minimum [vertex cover](/vertex-cover/) of size $\nu$, found in $O(n + m)$ more time.
- **Monotone layers.** The length of a shortest augmenting path grows strictly from phase to phase.
- **Covered vertices stay covered.** An augmentation never makes a matched vertex free, so a vertex matched once stays matched.
- **Few phases in practice.** On random and on most practical graphs, the number of phases is far below $\sqrt n$.

## Variants and improvements

- **[Dinic's algorithm](/dinic/).** On the unit-capacity network of bipartite matching, Dinic's [level graph](/level-graph/) and [blocking flow](/blocking-flow/) are the layers and the vertex-disjoint path set of Hopcroft-Karp, and the two algorithms do the same work.
- **[Kuhn's algorithm](/kuhn-algorithm/).** One augmenting path per search: $O(nm)$ time, but shorter code and often fast enough.
- **Dense graphs.** Alt, Blum, Mehlhorn and Paul used bit-level parallelism to reach $O(n^{3/2}\sqrt{m / \log n})$ time.
- **General graphs.** The [Micali-Vazirani algorithm](/micali-vazirani-algorithm/) finds shortest augmenting paths in a graph with odd cycles and reaches the same $O(m\sqrt n)$ bound, with much more involved code.
- **Weighted matching.** Scaling algorithms of Gabow and Tarjan use Hopcroft-Karp style phases inside each cost scale; see the [assignment problem](/assignment-problem/).
- **Faster asymptotically.** Through [almost-linear max flow](/almost-linear-max-flow/), bipartite matching takes $m^{1 + o(1)}$ time.

## When to use it

Use Hopcroft-Karp for maximum bipartite matching on large graphs, when the $O(nm)$ worst case of Kuhn's algorithm is too slow, as in programming contests with $10^5$ vertices. It needs no flow network and less memory than [Dinic's algorithm](/dinic/) on the reduction. For weighted problems use the [Hungarian algorithm](/hungarian-algorithm/), and for general graphs [Edmonds' blossom algorithm](/edmonds-blossom/).

## Pitfalls

- **Not marking entered vertices.** If line L12 does not set $\text{dist}[x] \leftarrow \infty$, or pointers are not kept per phase, a vertex can be explored many times in one phase and the phase is no longer linear.
- **The layer test.** The pass must move from layer $d$ to exactly layer $d + 1$, and accept a free $Y$ vertex only at the last layer, $d + 1 = D$. Accepting a free vertex earlier is impossible, but accepting one later, or a jump over layers, gives paths that are not shortest and breaks the bound on phases.
- **Stopping the search too late or too early.** Vertices in layers below $D$ must all be expanded, even after $D$ is set; otherwise some shortest paths are missed. Expanding beyond $D$ wastes time but is harmless.
- **Recursion depth.** A recursive DFS can go $\Theta(n)$ deep, which overflows the default stack of many languages; use an explicit stack.
- **Non-bipartite input.** On a graph with odd cycles, the algorithm can return a matching that is not maximum, without an error.

## Implementations

The Python version takes the sizes of both sides and a list of edges $(x, y)$ and returns the size, the two $\text{mate}$ arrays, with $-1$ for a free vertex, and the number of searches. An optional callback reports $D$ and the paths of each phase. The depth-first pass keeps its path on an explicit stack.

## History

John Hopcroft and Richard Karp presented the algorithm in 1971 and published it in 1973, under the title "An $n^{5/2}$ algorithm for maximum matchings in bipartite graphs", the bound being $O(m\sqrt n)$ with $m \le n^2$. Alexander Karzanov proved the same bound on the number of phases for flows in unit networks independently, around the same time, and Even and Tarjan derived it from [Dinic's algorithm](/dinic/) in 1975. Micali and Vazirani extended the bound to general graphs in 1980.

## References
