---
tag: 04S04K
kind: algorithm
slug: edmonds-arborescence
name: Edmonds' algorithm for minimum arborescence
aliases:
- Chu-Liu/Edmonds algorithm
- Edmonds' branching algorithm
area: graphs/spanning-trees
level: advanced
summary: Contract cycles of cheapest incoming edges and recurse, in O(mn) time.
solves: [minimum-arborescence]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of arcs}
  time: {worst: O(m n)}
  space: {extra: O(m n)}
properties: {deterministic: true, recursive: true}
prereqs: [minimum-arborescence, arborescence, cycle-contraction, directed-graph]
see_also: [cycle-contraction, minimum-spanning-tree, prim, edmonds-blossom, fibonacci-heap, skew-heap, disjoint-set, matroid-intersection]
sources:
  - paper: doi:10.6028/jres.071B.032
    title: "Jack Edmonds, Optimum branchings, Journal of Research of the National Bureau of Standards 71B(4) (1967), 233-240"
    locator: the whole paper (the contraction of cycles of cheapest entering arcs, and the proof by linear programming duality)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 4.9, Minimum-Cost Arborescences, a Multi-Phase Greedy Algorithm (the algorithm and its proof by an exchange argument)
  - paper: doi:10.1002/net.3230070103
    title: "Robert E. Tarjan, Finding optimum branchings, Networks 7(1) (1977), 25-35"
    locator: the whole paper (the O(m log n) and O(n^2) implementations)
  - paper: doi:10.1007/BF02579168
    title: "Harold N. Gabow, Zvi Galil, Thomas Spencer and Robert E. Tarjan, Efficient algorithms for finding minimum spanning trees in undirected and directed graphs, Combinatorica 6(2) (1986), 109-122"
    locator: the sections on directed graphs (the O(m + n log n) algorithm)
---

Edmonds' algorithm, also called the Chu-Liu/Edmonds algorithm, solves the [minimum arborescence](/minimum-arborescence/) problem: given a [directed graph](/directed-graph/) with arc costs and a root $r$, it finds a cheapest set of arcs that gives every other vertex exactly one entering arc and reaches every vertex from $r$. It lets every vertex pick its cheapest entering arc. If the picks form no cycle, they are the answer. Otherwise it contracts a cycle into one vertex, lowers the cost of each arc that enters the cycle by the cost of the pick it would replace, solves the smaller graph, and opens the cycle again, dropping exactly one of its arcs. This is the model case of [cycle contraction](/cycle-contraction/). The plain version takes $O(mn)$ time; Tarjan's version takes $O(m \log n)$, and the version of Gabow, Galil, Spencer and Tarjan $O(m + n \log n)$.

## In plain words

Each point of a one-way network must get a message over exactly one incoming link, starting from a source. First let every point choose its cheapest incoming link. If these links lead back to the source, there is nothing more to do: no point can pay less.

The trouble is a loop of points that only feed each other. Some point of the loop must take a link from outside instead. Treat the whole loop as one big point, and price each outside link into it by how much more it costs than the link it would replace. Solve this smaller problem the same way. Then open the loop again: the outside link that was chosen tells you which loop link to drop, and the rest of the loop stays.

## The problem

The input is a directed graph $G = (V, A)$ with $n$ vertices and $m$ arcs, a root $r$, and a real cost $c(a)$ on each arc. Costs may be negative and may tie. Parallel arcs and self-loops are allowed; self-loops and arcs into $r$ are never used. The graph need not be strongly connected, but a solution exists only if every vertex is reachable from $r$; otherwise the algorithm returns NONE. The output is an arborescence rooted at $r$ of least total cost.

## The algorithm

```pseudo id=main
EDMONDS(G, r, c)
L1  for each vertex v ≠ r do
L2      in[v] ← a cheapest arc (u, v) with u ≠ v                    ▷ ties: the smaller index
L3  if some v ≠ r has no such arc then return NONE                  ▷ v is not reachable from r
L4  if the arcs in[·] form no cycle then return {in[v] : v ≠ r}
L5  let C be a cycle of arcs in[·]
L6  G' ← G with C contracted to one vertex x: drop arcs inside C; an arc (u, v) with v ∈ C costs c(u, v) − c(in[v])
L7  T' ← EDMONDS(G', r, c')
L8  if T' = NONE then return NONE
L9  let (u, v) be the arc of G behind the arc of T' that enters x
L10 return (the arcs of G behind T') ∪ (C ∖ {in[v]})
```

Line L2 is the greedy step. Line L6 holds the key idea: the cost of an arc into the cycle becomes the *extra* cost of using it instead of the cycle arc it pushes out, $\mathrm{in}[v]$. Each arc of $G'$ remembers the arc of $G$ it came from, which is what lines L9 and L10 use. Arcs that leave $C$ keep their cost and get $x$ as their tail; parallel arcs created by the contraction are kept.

## Example

Take the root $r$, the vertices $a, b, c$ and the arcs $ra = 5$, $rb = 6$, $ab = 1$, $ba = 2$, $ac = 4$, $bc = 3$, $rc = 10$.

**Level 1.** The cheapest arcs are $\mathrm{in}[a] = ba = 2$, $\mathrm{in}[b] = ab = 1$, $\mathrm{in}[c] = bc = 3$. The arcs $ab$ and $ba$ form the cycle $C$ on $\{a, b\}$, so line L6 contracts it to $x$:

| arc of $G$ | arc of $G'$ | cost in $G'$ |
|---|---|---|
| $ra = 5$ | $rx$ | $5 - c(ba) = 3$ |
| $rb = 6$ | $rx$ | $6 - c(ab) = 5$ |
| $ac = 4$ | $xc$ | 4 |
| $bc = 3$ | $xc$ | 3 |
| $rc = 10$ | $rc$ | 10 |
| $ab$, $ba$ | dropped | |

**Level 2.** In $G'$ the cheapest arcs are $rx = 3$ (from $ra$) and $xc = 3$ (from $bc$). They form no cycle, so $T' = \{ra, bc\}$ with cost 6 in $G'$.

**Expansion.** The arc of $T'$ into $x$ comes from $ra$, which enters $C$ at $a$. So line L10 drops $\mathrm{in}[a] = ba$ and keeps $ab$. The result is $\{ra, ab, bc\}$ of cost $5 + 1 + 3 = 9$, which is the cost $6$ in $G'$ plus the cost $3$ of the cycle. The graph has nine arborescences, and the other eight cost from 10 to 21.

**Why greedy growth fails.** With the arcs $ra = 2$, $rb = 3$ and $ba = 1$, growing a tree from $r$ like [Prim's algorithm](/prim/) takes $ra$, then $rb$, for a cost of 5. Edmonds' algorithm picks $\mathrm{in}[a] = ba$ and $\mathrm{in}[b] = rb$, which form no cycle, and returns $\{rb, ba\}$ of cost 4.

## Correctness

**Theorem.** EDMONDS stops after at most $n$ nested calls. It returns NONE exactly when some vertex is not reachable from $r$, and otherwise it returns a minimum-cost arborescence.

The proof has three steps.

1. If the picks form no cycle, they are an arborescence, and each arborescence pays at least $c(\mathrm{in}[v])$ for the arc into each $v$, so the picks are optimal.
2. *The cycle lemma.* Some optimal arborescence enters $C$ exactly once and contains all arcs of $C$ except the one into the entry vertex. Take an optimal $T$ and the first arc $(a, b)$ by which a shortest path of $T$ from $r$ enters $C$; replace all other arcs of $T$ into $C$ by the arcs of $C$. After shifting costs so that every pick costs 0, the new arcs cost 0 and the removed arcs at least 0, and the result is still an arborescence.
3. *The contraction is exact.* The arborescences of $G$ of the form in step 2 correspond one to one to the arborescences of $G'$, and the cost in $G$ is the cost in $G'$ plus the fixed amount $\sum_{w \in C} c(\mathrm{in}[w])$. So an optimal arborescence of $G'$ expands to an optimal one of $G$.

Each contraction removes at least one vertex, since a cycle of picks has at least two vertices. Ties need no care: step 2 works for any choice of cheapest arcs. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

The model is the word RAM, with arc costs that can be compared and subtracted in $O(1)$ time.

- **One level.** Lines L1 to L5 scan all arcs once and follow the picks to find a cycle, in $O(n + m)$ time. Line L6 builds $G'$ in $O(n + m)$ time. Lines L9 and L10 take $O(n)$ time.
- **Levels.** Each contraction lowers the number of vertices by at least one, so there are at most $n - 1$ contractions.
- **Total.** $O(n (n + m)) = O(mn)$ time in the worst case, when every vertex is reachable, so that $m \ge n - 1$. The bound is reached, up to a constant, on graphs where every level contracts a 2-cycle and keeps most arcs.
- **Space.** This recursive version keeps the arc list of every level until the expansion, which is $O(mn)$ in the worst case. Storing only the arcs of the current level and a stack of the contracted cycles brings it to $O(n + m)$.

| claim | bound | case |
|---|---|---|
| time | $O(m n)$ | worst |
| contractions | at most $n - 1$ | every input |
| extra space, recursive version | $O(m n)$ | worst |

## Properties

- **Exact.** It returns an optimal arborescence for every cost function, including negative costs and ties.
- **Detects unreachable vertices.** It returns NONE exactly when no arborescence exists.
- **Deterministic** with the tie rule of line L2.
- **A primal-dual method.** The amounts subtracted at line L6, together with the costs of the picks, form a dual solution of the cut linear program of the [minimum arborescence](/minimum-arborescence/) problem, and the returned arborescence meets it with equality. This is how Edmonds' paper proves optimality.

## Variants and improvements

- **Tarjan (1977).** Keep, for each contracted vertex, a mergeable heap such as a [skew heap](/skew-heap/) of its entering arcs, with a lazy offset for the cost reductions, and a [disjoint-set](/disjoint-set/) structure for the contracted sets. Growing one path of picks and contracting each cycle when it closes gives $O(m \log n)$ time, and an array version gives $O(n^2)$ for dense graphs.
- **Gabow, Galil, Spencer and Tarjan (1986).** The same growth with [Fibonacci heaps](/fibonacci-heap/) gives $O(m + n \log n)$, the best known deterministic bound.
- **Maximum branching.** Edmonds' paper solves the maximum weight branching, with no fixed root: drop arcs of non-positive weight, use the heaviest entering arcs, and allow a vertex to stay a root.
- **Any root.** Add a new root with an arc of a large equal cost to every vertex.
- **Matroid intersection.** Arborescences are common bases of a graphic and a partition matroid, so weighted [matroid intersection](/matroid-intersection/) also solves the problem, more slowly.

## When to use it

Use it whenever arcs have a direction, so that the undirected [minimum spanning tree](/minimum-spanning-tree/) algorithms do not apply: broadcast trees over one-way links, the best dependency tree of a sentence in natural language processing, or a cheapest choice of one parent per object. The plain $O(mn)$ version is short and fast enough for dense graphs of a few thousand vertices; for large sparse graphs use Tarjan's heap-based version.

## Pitfalls

- **Forgetting the reduced costs.** If line L6 keeps the original costs of arcs into $C$, the recursion compares arcs into different vertices of the cycle unfairly. In the example, $rx$ from $ra$ would cost 5 and $rx$ from $rb$ 6, which happens to work there; with $ra = 5$, $rb = 4$, $ab = 1$, $ba = 3$ it picks $rb$ and gets $rb + ba = 7$ instead of $ra + ab = 6$.
- **Expanding with the wrong arc.** Line L10 must drop $\mathrm{in}[v]$ for the vertex $v$ where the chosen arc enters $C$, not an arbitrary arc of the cycle. Keep the original arc behind each contracted arc.
- **Unreachable vertices after contraction.** Every vertex can have an entering arc while a cycle has no arc from outside. The check of line L3 must run again at each level, which line L8 passes up.
- **Self-loops and arcs into the root.** A self-loop of negative cost must never be picked, and neither must an arc into $r$. Contraction makes new self-loops out of the arcs inside $C$; drop them.
- **Prim-like growth or the undirected MST.** Neither solves the directed problem, as the three-arc example shows.

## Implementations

## History

Yoeng-Jin Chu and Tseng-Hong Liu published the algorithm in 1965, and Jack Edmonds found it independently and published it in 1967 under the name "optimum branchings", with a proof by linear programming duality; F. Bock gave a related method in 1971. Robert Tarjan's 1977 paper gave the $O(m \log n)$ and $O(n^2)$ implementations, with a correction to its analysis published later by Camerini, Fratta and Maffioli. Gabow, Galil, Spencer and Tarjan reached $O(m + n \log n)$ in 1986. Kleinberg and Tardos present the algorithm with an exchange proof, which is the one followed here.

## References
