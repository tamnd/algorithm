---
tag: NES9Z4
kind: theorem
slug: cycle-property
name: Cycle property
aliases:
- red rule
area: graphs/spanning-trees
level: intro
summary: The heaviest edge on any cycle belongs to no minimum spanning tree (for distinct weights).
prereqs: [spanning-tree, minimum-spanning-tree, simple-cycle, cut-property]
see_also: [cut-property, fundamental-cycle, reverse-delete, greedy-mst-algorithm, mst-optimality-conditions, mst-verification, mst-uniqueness]
sources:
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 4.5, The Minimum Spanning Tree Problem (the cycle property, for distinct costs, and the proof of the reverse-delete algorithm)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.3, Minimum Spanning Trees (the exercises on the cycle property and reverse-delete)
  - book: isbn:9780898711875
    title: Robert E. Tarjan, Data Structures and Network Algorithms, SIAM (1983)
    locator: Chapter 6, Minimum Spanning Trees (the red rule)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 21, Minimum Spanning Trees (the exercises of Section 21.1 and the chapter problems)
  - paper: doi:10.1090/S0002-9939-1956-0078686-7
    title: "Joseph B. Kruskal, On the shortest spanning subtree of a graph and the traveling salesman problem, Proceedings of the American Mathematical Society 7(1) (1956), 48-50"
    locator: the whole paper (Construction B, which removes the longest edges that do not disconnect the graph)
---

The cycle property says that, in an undirected [weighted graph](/weighted-graph/), an edge that is strictly heavier than every other edge of some cycle belongs to no [minimum spanning tree](/minimum-spanning-tree/), and that, when weights tie, a heaviest edge of a cycle can always be left out of some minimum spanning tree. It is the dual of the [cut property](/cut-property/): the cut property says which edges are safe to take, and the cycle property says which edges are safe to throw away. Tarjan calls the step that it justifies the *red rule*, and it is the proof of the [reverse-delete](/reverse-delete/) algorithm and of [MST verification](/mst-verification/).

## Statement

Let $G = (V, E)$ be a finite undirected graph with a real weight $w(e)$ on each edge. Parallel edges are allowed, and $G$ need not be connected; "minimum spanning tree" then means minimum spanning forest. A cycle is a [simple cycle](/simple-cycle/) of $G$, seen as a set $C$ of edges. An edge $e \in C$ is a *heaviest* edge of $C$ when $w(e) \ge w(f)$ for each $f \in C$.

**Theorem (cycle property).**

1. **Strict form.** If $e \in C$ and $w(e) > w(f)$ for each $f \in C \setminus \{e\}$, then $e$ is in no minimum spanning tree.
2. **Form with ties (the red rule).** Let $R \subseteq E$ be a set such that some minimum spanning tree $T$ has $T \cap R = \emptyset$. Let $C$ be a cycle with $C \cap R = \emptyset$, and let $e$ be a heaviest edge of $C$. Then some minimum spanning tree $T'$ has $T' \cap (R \cup \{e\}) = \emptyset$. Moreover, if $e \in T$, then $T' = (T \setminus \{e\}) \cup \{f\}$ for an edge $f \in C$ with $w(f) = w(e)$.
3. **Which edges are in some MST.** An edge $e = (u, v)$ is in some minimum spanning tree if and only if $G$ has no path from $u$ to $v$ whose edges are all strictly lighter than $e$; equivalently, if and only if $e$ is not the strictly heaviest edge of any cycle.

## In plain words

Look at any loop of roads in a road network. To keep all towns connected, you never need every road of the loop, because the towns of the loop stay connected when you remove one of its roads. So you can remove the most expensive road of the loop. If that road is strictly more expensive than all others on the loop, no cheapest network ever uses it.

If two roads of the loop tie for the most expensive, you can still remove one of them, but a cheapest network may use either one. You can apply the rule again and again, to loops that use no removed road, and some cheapest network survives all the removals.

## Proof

*Proof of part 2.* If $e \notin T$, take $T' = T$. Otherwise remove $e$ from $T$. Since $e$ is a bridge of the forest $T$, the tree of $T$ that holds $e$ splits into two trees. Let $S$ be the vertex set of the one that holds the end $u$ of $e = (u, v)$; then $v \notin S$, and no edge of $T \setminus \{e\}$ has exactly one end in $S$. The set $C \setminus \{e\}$ is a path from $u$ to $v$, so it has an edge $f$ with exactly one end in $S$. This $f$ is not in $T \setminus \{e\}$, and $f \ne e$, so $f \notin T$. Let $T' = (T \setminus \{e\}) \cup \{f\}$. The edge $f$ joins the two trees again, so $T'$ is a spanning forest with the same components as $T$. Since $e$ is a heaviest edge of $C$, $w(f) \le w(e)$, so $w(T') = w(T) - w(e) + w(f) \le w(T)$, and $T'$ is a minimum spanning tree. Since $T$ is minimum, $w(T') \ge w(T)$ too, so $w(f) = w(e)$. Finally $f \in C$ and $C \cap R = \emptyset$, so $f \notin R$, and $T'$ avoids $R \cup \{e\}$. $\square$

*Proof of part 1.* Let $T$ be any minimum spanning tree and assume $e \in T$. Apply part 2 with $R = \emptyset$. It gives an edge $f \in C \setminus \{e\}$ with $w(f) = w(e)$. This contradicts the hypothesis $w(e) > w(f)$. So $e \notin T$. $\square$

*Proof of part 3.* If $G$ has a path $P$ from $u$ to $v$ whose edges are all lighter than $e$, then $P$ does not use $e$, so $P \cup \{e\}$ contains a simple cycle through $e$ on which $e$ is strictly heaviest, and part 1 shows that $e$ is in no minimum spanning tree. Conversely, assume that no such path exists. Let $S$ be the set of vertices that $u$ reaches by edges of weight less than $w(e)$. Then $u \in S$ and $v \notin S$, so $e$ crosses the cut $(S, V \setminus S)$. Each edge $g$ that crosses this cut has $w(g) \ge w(e)$, because an edge of smaller weight would let $u$ reach its other end. So $e$ is a light edge of the cut, and the [cut property](/cut-property/) (part 2, applied in the component of $u$) gives a minimum spanning tree that contains $e$. The two forms of the condition are the same: a cycle on which $e$ is strictly heaviest is $e$ plus a path from $u$ to $v$ of strictly lighter edges. $\blacksquare$

## Consequences

- **[Reverse-delete](/reverse-delete/).** Scan the edges from the heaviest to the lightest and delete each edge that lies on a cycle of the remaining graph. Part 2 shows that each deletion keeps some minimum spanning tree, and the result is a minimum spanning forest.
- **[Kruskal's algorithm](/kruskal/) drops edges by this rule.** An edge whose ends are already joined by lighter edges is a heaviest edge of a cycle.
- **[MST optimality conditions](/mst-optimality-conditions/).** A spanning tree $T$ is minimum if and only if each edge $e \notin T$ is a heaviest edge of its [fundamental cycle](/fundamental-cycle/) with $T$. Part 1 and the exchange of part 2 give the two directions; that page has the proof.
- **[MST verification](/mst-verification/).** To check that $T$ is minimum, compare each non-tree edge with the heaviest tree edge on its tree path. The [Karger-Klein-Tarjan algorithm](/karger-klein-tarjan-mst/) uses this test to throw away edges in linear time.
- **[Uniqueness](/mst-uniqueness/).** With distinct weights, each edge outside a minimum spanning tree $T$ is the strict maximum of its fundamental cycle, so it is in no minimum spanning tree, and $T$ is the only one.
- **The [greedy MST algorithm](/greedy-mst-algorithm/)** applies the red rule of part 2 and the blue rule of the cut property in any order.

## Tightness

- **Strict cannot become weak in part 1.** In a triangle with three edges of weight 1, each edge is a heaviest edge of the only cycle, and each edge is in some minimum spanning tree: the three trees are the three pairs of edges. So a heaviest edge can be in a minimum spanning tree when it ties.
- **The red set must avoid the cycle in part 2.** In the same triangle, let $R = \{ab\}$, which the tree $\{bc, ca\}$ avoids. The cycle $C = \{ab, bc, ca\}$ meets $R$. If we apply the rule anyway and remove its heaviest edge $bc$, no spanning tree avoids both $ab$ and $bc$, because only the edge $ca$ is left.
- **A cycle, not a cut.** The heaviest edge at one vertex can be in every minimum spanning tree. In a path $a, b, c$ with $w(ab) = 1$ and $w(bc) = 5$, the edge $bc$ is the heaviest edge of the graph, and it is in the only spanning tree, because it lies on no cycle.

**An example.** In the graph with the vertices $a$ to $f$ and the edges $ab = 4$, $ac = 3$, $bc = 1$, $bd = 2$, $cd = 4$, $ce = 5$, $de = 7$, $df = 6$, $ef = 2$, the cycles and their strictly heaviest edges are:

| cycle | weights | strictly heaviest edge |
|---|---|---|
| $a, b, c$ | $ab = 4$, $bc = 1$, $ca = 3$ | $ab$ |
| $b, c, d$ | $bc = 1$, $cd = 4$, $db = 2$ | $cd$ |
| $d, e, f$ | $de = 7$, $ef = 2$, $fd = 6$ | $de$ |
| $c, d, f, e$ | $cd = 4$, $df = 6$, $fe = 2$, $ec = 5$ | $df$ |

So none of $ab$, $cd$, $de$ and $df$ is in a minimum spanning tree. The other five edges, $bc$, $bd$, $ef$, $ac$ and $ce$, form the only minimum spanning tree, of weight 13.

## History

The cycle property appears with the cut property in the early work on the problem, and Kruskal's 1956 paper describes a second construction that removes the longest edges that lie on cycles, which is the reverse-delete method. Tarjan's 1983 monograph (Chapter 6) named the step the red rule and proved that the blue and red rules, applied in any order, give a minimum spanning tree.

## References
