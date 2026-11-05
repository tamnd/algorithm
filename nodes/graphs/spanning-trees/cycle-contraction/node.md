---
tag: 1AHNJ8
kind: technique
slug: cycle-contraction
name: Cycle contraction
aliases:
- Contraction of a cycle
area: graphs/spanning-trees
level: core
summary: Replaces a cycle in a graph by a single vertex so a problem can be solved on the smaller graph and then expanded back.
prereqs: [graph, simple-cycle, directed-graph]
see_also: [edmonds-arborescence, minimum-arborescence, edmonds-blossom, condensation-graph, two-edge-connected-components, graph-contraction, boruvka, karger-min-cut]
sources:
  - paper: doi:10.6028/jres.071B.032
    title: "Jack Edmonds, Optimum branchings, Journal of Research of the National Bureau of Standards 71B(4) (1967), 233-240"
    locator: the whole paper (the contraction of a cycle of cheapest entering arcs, with reduced costs)
  - paper: doi:10.4153/CJM-1965-045-4
    title: "Jack Edmonds, Paths, trees, and flowers, Canadian Journal of Mathematics 17 (1965), 449-467"
    locator: the sections on blossoms and their shrinking
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 20, Section 20.5, Strongly connected components (the component graph)
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 7, Minimum Spanning Trees (contraction in Borůvka's algorithm)
---

Cycle contraction replaces the vertices of a cycle $C$ of a graph $G$ by one new vertex, deletes the edges inside $C$, and keeps each edge with one end in $C$ as an edge at the new vertex. The result is the contracted graph $G / C$. If the problem has the property that an optimal solution of $G / C$ can be turned back into an optimal solution of $G$, the method solves the smaller graph, often by recursion, and then *expands* the cycle. Edmonds used it twice: for the [minimum arborescence](/minimum-arborescence/) problem ([Chu-Liu/Edmonds](/edmonds-arborescence/)) and for blossoms in [maximum matching](/edmonds-blossom/). Each contraction removes at least one vertex, so there are at most $n - 1$ of them.

## In plain words

Some problems are hard only because of loops in the graph. When you find a loop whose parts can be treated as one unit, glue all its points together into one big point. Links inside the loop disappear. Links that touch the loop now touch the big point.

The new graph is smaller, so you solve the problem there, maybe by doing the same thing again. Then you open the big point back into its loop and fix the answer inside it. The fix uses what the solution on the small graph did at the big point.

The method is correct only for problems where you can show that gluing the loop loses nothing.

## When it applies

The method applies when three facts hold for the problem:

1. **A cycle can be found that acts as a unit.** There is a rule that finds a cycle $C$ such that some optimal solution meets $C$ in a known way: for example, it uses all edges of $C$ except one, or it enters $C$ exactly once.
2. **The problem on $G / C$ is the same problem**, possibly with changed weights, so that the method can recurse.
3. **Solutions can be expanded.** Each solution $S'$ of $G / C$ gives a solution $S$ of $G$, and $S'$ optimal implies $S$ optimal, usually with $\mathrm{cost}(S) = \mathrm{cost}(S') + \text{a constant that depends on } C$.

It does not apply when the inside of the cycle interacts with the rest of the graph in more than one way. For example, an undirected [minimum spanning tree](/minimum-spanning-tree/) cannot be found by contracting cycles, because no rule says which edge of an arbitrary cycle the tree leaves out without looking at the rest of the graph. MST algorithms contract trees instead, as [Borůvka's algorithm](/boruvka/) does.

**The contraction itself.** Let $C$ have vertex set $V_C$. Then $G / C$ has the vertices $(V \setminus V_C) \cup \{x\}$ for a new vertex $x$. Each edge with both ends in $V_C$ is deleted. Each edge with one end in $V_C$ gets the end $x$ in place of that end. Each other edge is kept. Parallel edges can appear, and each new edge keeps a pointer to the original edge it came from. With adjacency lists, the contraction takes $O(n + m)$ time.

## The template

```pseudo id=main
SOLVE-BY-CONTRACTION(G)
L1  if BASE-CASE(G) then return DIRECT(G)
L2  C ← FIND-UNIT-CYCLE(G)                  ▷ hole: a cycle that acts as a unit
L3  if there is no such C then return DIRECT(G)
L4  (G', x) ← contract C in G into the new vertex x
L5  ADJUST(G', C)                           ▷ hole: change the weights at x
L6  S' ← SOLVE-BY-CONTRACTION(G')
L7  return EXPAND(S', C, x)                 ▷ hole: map S' back and fix the inside of C
```

The holes are FIND-UNIT-CYCLE, ADJUST, EXPAND and the base case. Each call removes $|V_C| - 1 \ge 1$ vertices, so the recursion depth is at most $n - 1$, and with $O(n + m)$ time per level the total is $O(n (n + m))$ unless the levels share work.

## Classic examples

### Minimum arborescence (Chu-Liu/Edmonds)

The problem: in a directed graph with a root $r$ and a cost on each arc, find a spanning arborescence of least cost, in which each vertex other than $r$ has exactly one entering arc and all vertices are reachable from $r$.

- **FIND-UNIT-CYCLE.** For each vertex $v \ne r$, pick a cheapest entering arc. If the picked arcs have no cycle, they form an optimal arborescence (DIRECT). Otherwise take a cycle $C$ of picked arcs.
- **ADJUST.** For each arc $(u, v)$ with $u \notin C$ and $v \in C$, set $c'(u, x) = c(u, v) - c(\text{picked arc into } v)$.
- **EXPAND.** The arborescence $S'$ has one arc entering $x$; it comes from an arc $(u, v)$ with $v \in C$. Keep $(u, v)$, keep all arcs of $C$ except the one that enters $v$, and map the other arcs back. Then $\mathrm{cost}(S) = \mathrm{cost}(S') + \mathrm{cost}(C)$.

Example. Take the root $r$, the vertices $a, b, c$ and the arcs $ra = 5$, $rb = 6$, $ab = 1$, $ba = 2$, $ac = 4$, $bc = 3$, $rc = 10$. The cheapest entering arcs are $ba = 2$, $ab = 1$ and $bc = 3$; the first two form the cycle $C = \{ab, ba\}$ of cost 3. Contract $\{a, b\}$ into $x$. The arcs into $x$ get the costs $c'(ra) = 5 - 2 = 3$ and $c'(rb) = 6 - 1 = 5$; the arcs out of $x$ are $ac = 4$ and $bc = 3$. In $G / C$ the cheapest entering arcs are $ra$ (cost 3) into $x$ and $bc$ (cost 3) into $c$, with no cycle, so $S' = \{ra, bc\}$ of cost 6. The arc $ra$ enters $C$ at $a$, so expansion drops $ba$ and keeps $ab$: $S = \{ra, ab, bc\}$, of cost $5 + 1 + 3 = 9 = 6 + 3$. The other arborescences cost 10 or more. The page [Edmonds' algorithm](/edmonds-arborescence/) has the proof and an implementation.

### Blossoms in maximum matching

The problem: find a [maximum matching](/maximum-matching/) of an undirected graph by repeated [augmenting paths](/augmenting-path/).

- **FIND-UNIT-CYCLE.** During the search for an augmenting path from the free vertices, an edge between two even vertices of one search tree closes an odd cycle $B$, a [blossom](/blossom/), whose edges alternate except at one vertex, the base.
- **ADJUST.** None; the matching $M$ becomes $M / B$.
- **EXPAND.** An augmenting path of $G / B$ that passes through the new vertex is extended by the even-length alternating path around $B$ from the vertex where it enters to the base.

Edmonds proved that $G / B$ has an augmenting path for $M / B$ if and only if $G$ has one for $M$, which is what makes the shrinking correct; see [Edmonds' blossom algorithm](/edmonds-blossom/).

### Strongly connected components

The problem: answer reachability questions, or find an order of the vertices, in a directed graph that has cycles.

- **FIND-UNIT-CYCLE.** Any directed cycle. All its vertices reach each other, so for reachability they act as one vertex.
- **ADJUST.** None.
- **EXPAND.** A vertex of the contracted graph stands for all vertices of the cycle.

Contracting directed cycles until none remains gives the [condensation graph](/condensation-graph/), a directed acyclic graph whose vertices are the strongly connected components. Algorithms such as [Tarjan's](/tarjan-scc/) compute all the contractions at once in $O(n + m)$ time. [2-SAT](/2-sat/) uses the result: a formula is satisfiable if and only if no variable is in one component with its negation.

### Bridges and 2-edge-connected components

In an undirected graph, an edge is a [bridge](/bridge/) if and only if it lies on no cycle. Contracting a cycle keeps the bridges: an edge outside $C$ is on a cycle of $G$ if and only if it is on a cycle of $G / C$. Contracting cycles until none remains leaves a forest whose vertices are the [2-edge-connected components](/two-edge-connected-components/) and whose edges are the bridges.

## Variations

- **Contraction of trees or edges.** [Borůvka's algorithm](/boruvka/) contracts the trees of chosen edges, and [Karger's min-cut algorithm](/karger-min-cut/) contracts random edges. Both use the same bookkeeping: map each new edge to its original edge, and drop the self-loops. See [graph contraction](/graph-contraction/) for the parallel form.
- **Nested contraction with one data structure.** Instead of building $G / C$, keep the vertices of all cycles in a [disjoint-set](/disjoint-set/) structure and merge the entering-arc sets by a mergeable heap. Tarjan's version of Edmonds' algorithm does this in $O(m \log n)$ time.
- **Contraction with a weight shift.** In the arborescence case, ADJUST subtracts a value from each arc into the cycle. The same shift appears as a dual variable in the linear program of the problem.

## Pitfalls

- **Losing the original edges.** After a contraction, an edge of $G / C$ must remember which edge of $G$ it came from, or EXPAND cannot map the solution back. Keep the index of the original edge.
- **Parallel edges and self-loops.** Edges inside $C$ become self-loops at $x$ and must be deleted. Two edges into $C$ from one vertex become parallel; keep both, or keep the cheaper one after ADJUST, not before, since ADJUST can change their order.
- **Forgetting to undo the adjustment.** The cost of $S$ is computed with the original weights. In the arborescence example, $S'$ costs 6 under the adjusted weights and $S$ costs 9 under the original ones.
- **Contracting a cycle that is not a unit.** In matching, an even cycle cannot be shrunk: a path of length 3 $a, b, c, d$ with $bc$ matched has the augmenting path through all four vertices, but after the 4-cycle $a, b, c, d$ (with the extra edge $da$) is shrunk to one vertex, no free vertex is left outside it.
- **Recursion depth.** A chain of $n - 1$ contractions is possible, so a recursive version needs depth $n$; write it as a loop for large graphs.

## Exercises

1. In the arborescence example, give the cost of each of the spanning arborescences rooted at $r$ that use the arc $rb$, and check that none costs less than 9.
2. Prove the arborescence step: let $C$ be a cycle of cheapest entering arcs, with $y_v$ the cost of the picked arc into $v$. Show that each arborescence $S$ of $G$ that has exactly one arc entering $C$ satisfies $c(S) = c'(S / C) + c(C)$, where $c'$ is the adjusted cost.
3. Show that for each cycle $C$ of an undirected graph and each edge $e \notin C$, the edge $e$ is a bridge of $G$ if and only if its image is a bridge of $G / C$.
4. Give an example of a directed graph on 4 vertices in which Chu-Liu/Edmonds makes two nested contractions.
5. Show that $n - 1$ contractions of the arborescence kind, each in $O(m)$ time, give an $O(nm)$ algorithm, and find a graph on which the simple version needs $\Omega(n)$ contractions.

## References
