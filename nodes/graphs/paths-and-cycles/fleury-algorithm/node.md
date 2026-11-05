---
tag: CVA0RG
kind: algorithm
slug: fleury-algorithm
name: Fleury's algorithm
area: graphs/paths-and-cycles
level: core
summary: Builds an Eulerian trail of an undirected multigraph edge by edge, never crossing a bridge of the unused edges unless it is the only edge left at the current vertex.
solves: [eulerian-path-problem]
model: word-ram
complexity:
  vars: {n: the number of vertices, m: the number of edges}
  time: {worst: O(m (n + m)), best: Θ(n + m)}
  space: {extra: Θ(n + m)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1883
  people: [Fleury]
  note: Fleury published the rule of not crossing a bridge unless forced in the Journal de mathématiques élémentaires in 1883.
prereqs: [eulers-theorem-eulerian-graphs, bridge, eulerian-path]
see_also: [hierholzer-algorithm, eulerian-path-problem, eulerian-circuit, bridge-finding, dynamic-connectivity, chinese-postman-problem, handshaking-lemma, graph-reachability]
sources:
  - book: isbn:9781846289699
    title: J. A. Bondy and U. S. R. Murty, Graph Theory, Graduate Texts in Mathematics 244, Springer (2008)
    locator: Section 3.3, Euler tours (Fleury's algorithm and its correctness)
  - paper: "Fleury, Deux problèmes de géométrie de situation, Journal de mathématiques élémentaires, second series, volume 2, 257 to 261 (1883)"
    locator: the whole paper
  - book: isbn:9783030542559
    title: Steven S. Skiena, The Algorithm Design Manual, third edition, Springer (2020)
    locator: Section 18.7, Eulerian cycle
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Problem 20-3, Euler tour (the linear-time method to compare with)
---

Fleury's algorithm finds an [Eulerian trail](/eulerian-path/) in an undirected [multigraph](/multigraph/): it starts at an odd vertex, if there is one, and at each step it leaves the current vertex by an unused edge that is not a [bridge](/bridge/) of the graph of unused edges, unless that edge is the only one left there. So it never cuts off edges that it has not yet walked. With a plain search for each bridge test it runs in $O(m(n + m))$ time, which is slower than the linear time of [Hierholzer's algorithm](/hierholzer-algorithm/), but its rule is local and easy to follow by hand. It handles parallel edges, self-loops and isolated vertices; it is stated here for undirected graphs.

## In plain words

You want to draw a figure without lifting the pen and without drawing a line twice. Start at a point where an odd number of lines meet, if there is one. Then draw one line at a time, and erase it in your mind once it is drawn.

The one rule: do not take a line that would cut the rest of the figure into two pieces, because you could never come back to the other piece. Take such a line only when it is the last line at your point. If you follow the rule, you never get stuck before all lines are drawn.

## The problem

The input is an undirected multigraph $G$ with vertices $0, \ldots, n-1$ and $m$ numbered edges; parallel edges, self-loops and isolated vertices are allowed. A self-loop adds 2 to the degree of its vertex. The output is an Eulerian trail, given as the sequence of its $m$ edges and $m + 1$ vertices, or NIL if $G$ has none. By [Euler's theorem](/eulers-theorem-eulerian-graphs/), a trail exists if and only if all edges lie in one connected component and at most two vertices have odd degree; it is closed, an [Eulerian circuit](/eulerian-circuit/), when no vertex has odd degree.

## The algorithm

$H$ is the graph of the unused edges, on all the vertices; at the start $H = G$.

```pseudo id=main
FLEURY(G)
L1  if G has more than two odd vertices or its edges are in two components then return NIL
L2  u ← an odd vertex if one exists, else an end of some edge
L3  W ← (u); T ← (); H ← G
L4  while deg_H(u) > 0 do
L5      if deg_H(u) = 1 then e ← the only edge of H at u
L6      else e ← an edge of H at u that is not a bridge of H
L7      remove e from H; append e to T
L8      u ← the other end of e; append u to W
L9  return (W, T)
```

An edge $e = uv$ is a bridge of $H$ if $v$ cannot be reached from $u$ in $H - e$; a self-loop is never a bridge. Line L6 tests the edges at $u$ in order by a search in $H - e$. At most one edge at $u$ is a bridge (see Correctness), so line L6 needs at most two tests. The case $m = 0$ returns the trail of one vertex.

## Example

The graph has the edges $e_0 = 03$, $e_1 = 01$, $e_2 = 12$ and $e_3 = 20$: a triangle $0, 1, 2$ with a pendant edge to vertex 3. The degrees are $3, 2, 2, 1$, so the odd vertices are 0 and 3, and the walk starts at 0.

| step | $u$ | $\deg_H(u)$ | edge tested | result | edge taken |
|---|---|---|---|---|---|
| 1 | 0 | 3 | $e_0 = 03$ | bridge: 3 is cut off | |
| | | | $e_1 = 01$ | not a bridge: $1, 2, 0$ | $e_1$, go to 1 |
| 2 | 1 | 1 | | forced | $e_2$, go to 2 |
| 3 | 2 | 1 | | forced | $e_3$, go to 0 |
| 4 | 0 | 1 | | forced | $e_0$, go to 3 |

The trail is $0, 1, 2, 0, 3$ with the edges $e_1, e_2, e_3, e_0$. A walk that takes the first edge $e_0$ at step 1 gets stuck at 3 with the triangle unused: this is the mistake that the rule prevents. At step 4 the edge $e_0$ is a bridge of $H$, but it is the last edge at 0, so the walk takes it.

A graph with the edges $01$ and $23$ in two components, or the star with the edges $01$, $02$, $03$ with four odd vertices, gives NIL at line L1.

## Correctness

The full proof is in the [correctness proof](proofs/correctness/). Let $t$ be the other odd vertex of $G$, or $t = s$, the start, if all degrees are even. Two invariants hold at line L4:

- (a) the edges of $H$ all lie in the component of $H$ that contains $u$, if $H$ has edges;
- (b) if $u \ne t$, the odd vertices of $H$ are exactly $u$ and $t$, and if $u = t$, $H$ has no odd vertex.

Removing an edge $uv$ flips the parity of $u$ and of $v$, which keeps (b) with $v$ as the new current vertex. For (a), the key lemma is: **if $\deg_H(u) \ge 2$, at most one edge at $u$ is a bridge of $H$**. If a bridge $uv$ at $u$ had no $t$ on its far side, that side would have exactly one odd vertex after the bridge is removed, namely $v$, which is impossible by the [handshaking lemma](/handshaking-lemma/). So the far side of every bridge at $u$ contains $t$, and two bridges at $u$ would have disjoint far sides that both contain $t$. So line L6 always finds an edge, and removing a non-bridge keeps all edges in one component. When $\deg_H(u) = 1$, removing the last edge isolates $u$ and leaves the other edges in the component of the new vertex. By (a), the loop stops only when $H$ has no edges, so the walk uses every edge once.

## Complexity

Line L1 takes $O(n + m)$ time. The loop runs $m$ times. In each step, line L6 does at most two searches of $H - e$, each in $O(n + m)$ time, so the total is $O(m(n + m))$. The search can stop as soon as it reaches the other end of the edge, so on many graphs the steps are much cheaper; when every step is forced, as on a path, no search runs at all and the time is $\Theta(n + m)$. The extra space is $\Theta(n + m)$ for the incidence lists, the used marks and the search.

## Properties

- **Local rule.** Each step looks only at the current vertex and asks one global question, whether an edge is a bridge. A person can follow it with a pencil on a small drawing.
- **Online output.** The trail comes out in order, from the start to the end. Hierholzer's algorithm, by contrast, finds the trail in pieces and splices them.
- **Any choice works.** Any non-bridge at line L6 gives a correct trail, so Fleury's rule can produce every Eulerian trail that starts at the chosen vertex.
- **Undirected.** This page and the implementation treat undirected graphs. Directed graphs are usually handled with [Hierholzer's algorithm](/hierholzer-algorithm/).

## Variants and improvements

- **Dynamic bridge structures.** With a fully [dynamic connectivity](/dynamic-connectivity/) or 2-edge-connectivity structure under edge deletions, each bridge test costs polylogarithmic time, and the total time becomes $O(m \cdot \mathrm{polylog}\, n)$. This is of theoretical interest only, since Hierholzer's algorithm is linear.
- **Recompute bridges.** Run a [bridge-finding](/bridge-finding/) algorithm once per step instead of two searches; the bound $O(m(n + m))$ does not change.
- **Lexicographic order.** Trying the edges at $u$ in a fixed order gives the lexicographically first Eulerian trail from $s$ with respect to that order, because a non-bridge is taken whenever one comes first in the order.

## When to use it

Use it to teach Euler trails, to construct one by hand, or when the trail must be produced edge by edge in its final order with a simple local rule. For large graphs use [Hierholzer's algorithm](/hierholzer-algorithm/), which takes $O(n + m)$ time.

## Pitfalls

- **Forgetting the forced case.** When only one edge is left at $u$, it must be taken even if it is a bridge, as in step 4 of the example; a rule that never crosses a bridge gets stuck.
- **Bridges of the wrong graph.** The test is for bridges of the graph of unused edges, not of $G$.
- **Starting at an even vertex.** When there are two odd vertices, the walk must start at one of them, or it gets stuck.
- **Treating a loop as a bridge, or parallel edges as one edge.** A self-loop is never a bridge, and two parallel edges are never bridges. A test that works on vertex adjacency instead of edge identities gets these wrong.
- **Skipping line L1.** On a graph with no trail the loop still stops, with some edges unused, so the output must be checked, or the condition tested first.

## Implementations

## History

Fleury published the rule in 1883 in the Journal de mathématiques élémentaires, ten years after Hierholzer's paper on the existence of Euler circuits appeared. It became the standard method in textbooks of graph theory with applications, for example in Bondy and Murty, while algorithm books prefer Hierholzer's linear method.

## References
