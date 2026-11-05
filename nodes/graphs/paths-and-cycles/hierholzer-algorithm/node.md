---
tag: 0QG3S6
kind: algorithm
slug: hierholzer-algorithm
name: Hierholzer's algorithm
aliases:
- Hierholzer's Eulerian circuit algorithm
area: graphs/paths-and-cycles
level: intro
summary: Builds an Eulerian circuit or trail by splicing closed sub-tours, with one stack and one pass over the edges, in O(n + m) time.
solves: [eulerian-path-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: Θ(n + m), best: Θ(n + m)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false}
history:
  year: 1873
  people: [Carl Hierholzer]
  note: Published after his death; the paper also proves that even degrees suffice for an Euler tour.
prereqs: [eulerian-circuit, eulerian-path, stack]
see_also: [eulers-theorem-eulerian-graphs, eulerian-path-problem, fleury-algorithm, chinese-postman-problem, de-bruijn-sequence, incidence-list, trail, depth-first-search]
sources:
  - paper: doi:10.1007/BF01442866
    title: Carl Hierholzer and Chr. Wiener, Ueber die Möglichkeit, einen Linienzug ohne Wiederholung und ohne Unterbrechung zu umfahren, Mathematische Annalen 6, 30 to 32 (1873)
    locator: the whole paper (the construction by joining closed lines)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 20, Problem 20-3, Euler tour (an O(E) algorithm for an Euler tour of a directed graph)
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 1.8, Euler tours (Theorem 1.8.1 and its proof by a longest trail)
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition
    locator: Section 1.2, Eulerian circuits (the characterization theorem and its proof by maximal trails)
---

Hierholzer's algorithm finds an [Eulerian circuit](/eulerian-circuit/), or an [Eulerian path](/eulerian-path/) when no circuit exists, in time linear in the size of the graph. It walks along unused edges until it gets stuck, which closes a sub-tour, and then backs up and starts new sub-tours from vertices that still have unused edges. A stack holds the current walk, and each vertex is written to the output when it is popped, which splices all sub-tours into one trail. The graph may be directed or undirected, and it may be a [multigraph](/multigraph/) with [self-loops](/self-loop/) and isolated vertices.

## In plain words

You must draw a figure without lifting the pen and without drawing a line twice.

Start at a corner and draw along lines you have not drawn yet, until you reach a corner with no free line. If every corner touches an even number of lines, you are back where you started, so you have drawn one closed loop.

Now go back along your loop. At the first corner that still has free lines, draw a new loop from there in the same way, and insert it into the old loop at that corner. Repeat until no free line is left.

If exactly two corners touch an odd number of lines, start at one of them; the first walk then ends at the other one, and the rest works the same.

## The problem

Given a graph $G = (V, E)$ with $V = \{0, \ldots, n - 1\}$ and $m$ numbered edges, directed or undirected, with parallel edges and self-loops allowed, return an Eulerian trail: a sequence $v_0, e_1, v_1, \ldots, e_m, v_m$ that uses each edge exactly once, with $e_i$ joining $v_{i-1}$ to $v_i$ (from $v_{i-1}$ to $v_i$ if directed). Return a closed one ($v_m = v_0$) whenever one exists. If no Eulerian trail exists, report that.

By [Euler's theorem](/eulers-theorem-eulerian-graphs/), an Eulerian trail exists if and only if all edges lie in one connected component (weakly connected, for a directed graph) and the degrees meet this condition:

| graph | Eulerian circuit | Eulerian trail that is not closed |
|---|---|---|
| undirected | every degree is even | exactly two vertices of odd degree, the two ends |
| directed | out-degree equals in-degree at every vertex | one vertex with out minus in equal to 1 (the start), one with in minus out equal to 1 (the end), all others balanced |

A self-loop adds 2 to the degree of its vertex in an undirected graph, and 1 to both the in-degree and the out-degree in a directed graph. Isolated vertices do not matter. The algorithm checks the degree condition first and finds a missing connection at the end, by counting the edges it used.

## The algorithm

$\mathrm{Inc}[v]$ is the list of edges at $v$: for a directed graph the edges that leave $v$, for an undirected graph all edges at $v$. $\mathrm{next}[v]$ is a pointer into $\mathrm{Inc}[v]$ that only moves forward. The stack $S$ holds pairs $(v, e)$: the current walk from the start, with the edge $e$ by which it reached $v$. The list $T$ receives the pairs as they are popped.

```pseudo id=main
HIERHOLZER(G)
L1  if the degree condition of the table fails then return "no Eulerian trail"
L2  s ← the vertex with odd degree (out minus in = 1) if there is one, else a vertex with an edge, else any vertex
L3  mark every edge unused; next[v] ← 1 for each vertex v
L4  S ← stack holding (s, NIL); T ← empty list
L5  while S is not empty do
L6      (v, e) ← TOP(S)
L7      while next[v] ≤ |Inc[v]| and Inc[v][next[v]] is used do next[v] ← next[v] + 1
L8      if next[v] ≤ |Inc[v]| then
L9          f ← Inc[v][next[v]]; mark f used; w ← the other end of f
L10         PUSH(S, (w, f))
L11     else append POP(S) to T
L12 if |T| < m + 1 then return "no Eulerian trail"
L13 return T in reverse order
```

Lines L6 to L10 extend the current walk by one unused edge. Line L11 runs when the top vertex has no unused edge: that vertex is final, and it goes to the output. The output read backwards is the trail. A vertex goes back on the walk only by popping, so a new sub-tour starts at the first vertex on the way back that still has unused edges, and the sub-tour is spliced into the output at that point.

In an undirected graph, each edge $f = \{u, w\}$ appears in $\mathrm{Inc}[u]$ and in $\mathrm{Inc}[w]$, and a loop appears twice in $\mathrm{Inc}[u]$. The used mark is on the edge, so the second copy is skipped at line L7. Parallel edges are separate entries and need no special case.

## Example

Take the undirected graph with vertices 0 to 5 and edges $e_0 = \{0, 1\}$, $e_1 = \{1, 2\}$, $e_2 = \{2, 0\}$, $e_3 = \{1, 3\}$, $e_4 = \{3, 4\}$, $e_5 = \{4, 1\}$. Vertex 1 has degree 4, vertices 0, 2, 3, 4 have degree 2, and vertex 5 is isolated. All degrees are even, so line L2 takes $s = 0$, the first vertex with an edge. The lists hold the edges in the order of their numbers.

| step | top of $S$ | action | $S$ after the step (vertices) | $T$ after the step (vertices) |
|---|---|---|---|---|
| 1 | 0 | take $e_0$ to 1 | 0, 1 | |
| 2 | 1 | take $e_1$ to 2 | 0, 1, 2 | |
| 3 | 2 | take $e_2$ to 0 | 0, 1, 2, 0 | |
| 4 | 0 | stuck, pop | 0, 1, 2 | 0 |
| 5 | 2 | stuck, pop | 0, 1 | 0, 2 |
| 6 | 1 | take $e_3$ to 3 | 0, 1, 3 | 0, 2 |
| 7 | 3 | take $e_4$ to 4 | 0, 1, 3, 4 | 0, 2 |
| 8 | 4 | take $e_5$ to 1 | 0, 1, 3, 4, 1 | 0, 2 |
| 9 to 13 | | stuck at each, pop all | empty | 0, 2, 1, 4, 3, 1, 0 |

Steps 1 to 3 find the sub-tour $0, 1, 2, 0$. Steps 6 to 8 find the sub-tour $1, 3, 4, 1$ from vertex 1, the first vertex on the way back with an unused edge. $T$ has $7 = m + 1$ entries, and reversed it gives the Eulerian circuit

$$0 \xrightarrow{e_0} 1 \xrightarrow{e_3} 3 \xrightarrow{e_4} 4 \xrightarrow{e_5} 1 \xrightarrow{e_1} 2 \xrightarrow{e_2} 0,$$

which is the first sub-tour with the second one inserted at vertex 1.

**An open trail.** Delete $e_2$. Now 0 and 2 have odd degree, line L2 takes $s = 0$, and the first walk $0, 1, 2$ stops at 2, the other odd vertex. The output is $0, 1, 3, 4, 1, 2$.

**No trail.** For the star with edges $\{0, 1\}, \{0, 2\}, \{0, 3\}$, four vertices have odd degree, and line L1 answers no. For two disjoint triangles, all degrees are even, so line L1 passes; the walk from 0 uses only the first triangle, $T$ ends with 4 entries, fewer than $m + 1 = 7$, and line L12 answers no. A loop at a vertex that no other edge touches is caught in the same way.

## Correctness

Two facts carry the proof. First, a walk on unused edges from a vertex $p$ that stops only when stuck ends at a vertex where the unused edges have odd degree (or more in than out, if directed), and at $p$ itself if there is no such vertex. So the first walk ends at the other odd vertex, or back at $s$, and every later walk is a closed sub-tour. Second, when a pair is popped, the pair below it is the vertex at which the next output edge starts, so the output, read backwards, is a trail that splices the sub-tours together. A vertex is popped only when it has no unused edge, so at the end the unused edges touch no vertex of the trail; if some remain, the edges are not in one component. The full proof is below.

## Complexity

The cost is in the [word RAM](/word-ram/) model, with the edges given as a list of pairs.

- **Building $\mathrm{Inc}$ and the degrees, lines L1 to L3.** $\Theta(n + m)$.
- **The loop, lines L5 to L11.** Each iteration pushes one pair or pops one pair. Each edge is pushed at most once, since it is marked at line L9, so there are at most $m + 1$ pushes, counting the first pair, and as many pops. The pointer $\mathrm{next}[v]$ only moves forward, so line L7 does at most $\sum_v |\mathrm{Inc}[v]| \le 2m$ steps in total.
- **Lines L12 and L13.** $O(m)$.

The time is $\Theta(n + m)$ on every input, and the extra space is $\Theta(n + m)$ for the lists, the marks, the stack and the output. The stack can hold $m + 1$ pairs, for example on a long cycle, which is why the implementation uses an explicit stack and not recursion.

## Properties

- **Deterministic.** With the lists in a fixed order, the output is fixed. Another order of the lists gives another Eulerian trail.
- **Not recursive.** The explicit stack replaces the recursive form, which is a depth-first search on edges and can recurse $m$ deep.
- **Output from the end.** Vertices are output in the reverse order of the trail, so the trail is known only when the algorithm ends. Read the output backwards, or run the algorithm on the reversed graph if the trail is wanted from the front.
- **Closed when possible.** If all degrees are even (or balanced), the result is a circuit; otherwise it starts at the odd vertex with the smaller number (or at the vertex with one more out-edge).

## Variants and improvements

- **Splicing with linked lists.** Hierholzer's original description: find a closed trail, then find a vertex on it with unused edges, find a closed trail from there, and splice it in. With a doubly linked list for the tour and a list of vertices on the tour that still have unused edges, this also runs in $O(n + m)$ time. The stack version does the same splicing without explicit links.
- **Recursive form.** EULER$(v)$: while $v$ has an unused edge $f$ to $w$, mark $f$ and call EULER$(w)$; then append $v$. It is short, but its depth can be $m$.
- **Fleury's algorithm.** [Fleury's algorithm](/fleury-algorithm/) builds the trail from the front by never crossing a bridge of the remaining graph unless forced. It needs bridge tests and is slower.
- **Directed graphs and de Bruijn sequences.** On the de Bruijn graph, every vertex has in-degree and out-degree $k$, and an Eulerian circuit gives a [de Bruijn sequence](/de-bruijn-sequence/).
- **Chinese postman.** If the graph has odd vertices, the [Chinese postman problem](/chinese-postman-problem/) adds copies of edges to make all degrees even, and Hierholzer's algorithm then gives the closed walk.

## When to use it

Use it whenever an Eulerian circuit or trail is needed: it is linear, simple and handles directed graphs, multigraphs and loops. Use the degree test alone, together with one search for connectivity, if only a yes or no answer is needed. Use [Fleury's algorithm](/fleury-algorithm/) only for teaching or when the trail must be built from the front with a local rule.

## Pitfalls

- **Starting at the wrong vertex.** If two vertices have odd degree, the walk must start at one of them. Starting elsewhere gives a trail that misses edges or fails.
- **Skipping the connectivity check.** The degree condition is not enough: two disjoint cycles pass it. Compare the length of the output with $m + 1$, or check connectivity of the edges first.
- **Starting at an isolated vertex.** If vertex 0 is isolated and $s$ is chosen as 0, the output has length 1 and the algorithm wrongly reports no trail. Choose a vertex with an edge.
- **Marking the edge entry, not the edge.** In an undirected graph each edge has two entries. If only the entry at $v$ is marked, the edge is used again from the other end.
- **Rescanning the lists.** Starting the scan of $\mathrm{Inc}[v]$ from the front every time gives quadratic time on vertices of high degree. Keep the pointer $\mathrm{next}[v]$.
- **Printing in push order.** The push order is not a trail: in the example it is $0, 1, 2, 0, 3, 4, 1$, which jumps from 0 to 3. Only the pop order, reversed, is correct.

## Implementations

## History

Euler's 1736 paper on the bridges of Königsberg states the degree condition but proves only that it is necessary. Carl Hierholzer proved that it is also sufficient, by joining closed lines into one; he died in 1871, and his proof was published in 1873 in Mathematische Annalen, prepared for print by Christian Wiener. The proof is already an algorithm: find a closed line, then join further closed lines to it at common vertices. CLRS gives the problem of an $O(E)$ Euler tour of a directed graph as an exercise.

## References
