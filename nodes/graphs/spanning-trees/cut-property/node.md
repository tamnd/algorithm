---
tag: 9P6A3Q
kind: theorem
slug: cut-property
name: Cut property
aliases:
- blue rule
area: graphs/spanning-trees
level: intro
summary: The lightest edge crossing any cut belongs to some minimum spanning tree.
prereqs: [spanning-tree, minimum-spanning-tree, cut, weighted-graph]
see_also: [cycle-property, safe-edge, generic-mst-method, greedy-mst-algorithm, kruskal, prim, boruvka, mst-optimality-conditions]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 21, Section 21.1, Growing a minimum spanning tree (the theorem on safe edges and light edges, and its corollary)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 4.5, The Minimum Spanning Tree Problem (the cut property, for distinct costs)
  - book: isbn:9780073523408
    title: Sanjoy Dasgupta, Christos Papadimitriou and Umesh Vazirani, Algorithms
    locator: Section 5.1, Minimum spanning trees (the cut property)
  - book: isbn:9780321573513
    title: Robert Sedgewick and Kevin Wayne, Algorithms, fourth edition
    locator: Section 4.3, Minimum Spanning Trees (the cut property and the greedy MST algorithm)
  - book: isbn:9780898711875
    title: Robert E. Tarjan, Data Structures and Network Algorithms, SIAM (1983)
    locator: Chapter 6, Minimum Spanning Trees (the blue rule and the red rule)
---

The cut property says that, in a connected undirected [weighted graph](/weighted-graph/), a lightest edge that crosses a [cut](/cut/) belongs to some [minimum spanning tree](/minimum-spanning-tree/), and in a form that allows a partial solution, that such an edge can be added to any set of edges that some minimum spanning tree contains and that no edge of the cut meets. It is the reason why [Kruskal's](/kruskal/), [Prim's](/prim/) and [Borůvka's](/boruvka/) algorithms are correct. Tarjan calls the step that it justifies the *blue rule*.

## Statement

Let $G = (V, E)$ be a connected undirected graph with a real weight $w(e)$ on each edge. Weights may tie, and parallel edges are allowed. A *cut* is a partition $(S, V \setminus S)$ with $\emptyset \ne S \ne V$. An edge *crosses* the cut when it has exactly one end in $S$. A set $A \subseteq E$ *respects* the cut when no edge of $A$ crosses it. An edge that crosses the cut is *light* for the cut when its weight is the least of all edges that cross the cut.

**Theorem (cut property).**

1. Let $A$ be a subset of some minimum spanning tree of $G$, let $(S, V \setminus S)$ be a cut that $A$ respects, and let $e$ be a light edge for the cut. Then $A \cup \{e\}$ is a subset of some minimum spanning tree of $G$.
2. In particular (take $A = \emptyset$), each light edge of each cut is in some minimum spanning tree.
3. If $e$ is the only light edge of the cut, that is, $w(e) < w(f)$ for each other edge $f$ that crosses the cut, then $e$ is in every minimum spanning tree.
4. Each minimum spanning tree contains at least one light edge of each cut.

The same statements hold for a graph that is not connected, with "minimum spanning forest" in place of "minimum spanning tree", for each cut that some edge crosses.

## In plain words

Split the towns into two groups in any way you like. At least one road of the final network must go from one group to the other, or the two groups stay apart. The cheapest road between the two groups is a safe choice: some cheapest network uses it. If that road is strictly cheaper than every other road between the groups, every cheapest network uses it.

This holds even after you have chosen some roads, as long as the roads you chose are part of a cheapest network and none of them goes between the two groups. So you can grow a network one cheap road at a time, and never need to undo a choice.

## Proof

*Proof of part 1.* Let $T$ be a minimum spanning tree with $A \subseteq T$. If $e \in T$, then $T$ is the tree we want. Otherwise let $e = (u, v)$ with $u \in S$ and $v \notin S$. The tree $T$ has exactly one path $P$ from $u$ to $v$. The path starts in $S$ and ends outside $S$, so at least one edge $f$ of $P$ crosses the cut. The edge $f$ is not in $A$, because $A$ respects the cut. Let

$$T' = (T \setminus \{f\}) \cup \{e\}.$$

Removing $f$ from $T$ splits it into two trees, one with $u$ and one with $v$, because $f$ is on the only path from $u$ to $v$. The edge $e$ joins these two trees, so $T'$ is connected, and it has $n - 1$ edges, so $T'$ is a spanning tree. The edge $e$ is light and $f$ crosses the cut, so $w(e) \le w(f)$ and

$$w(T') = w(T) - w(f) + w(e) \le w(T).$$

So $T'$ is a minimum spanning tree. It contains $A$, because $f \notin A$, and it contains $e$. $\square$

*Proof of part 2.* The empty set respects each cut and is a subset of each minimum spanning tree, so part 1 applies with $A = \emptyset$. $\square$

*Proof of part 3.* Let $T$ be any minimum spanning tree, and assume that $e \notin T$. Build $f$ and $T'$ as in the proof of part 1, with $A = \emptyset$. Now $f \ne e$ crosses the cut, so $w(e) < w(f)$, and $w(T') < w(T)$. This is false for a minimum spanning tree. So $e \in T$. $\square$

*Proof of part 4.* Let $T$ be a minimum spanning tree and let $e = (u, v)$ be a light edge of the cut. If $e \in T$, we are done. Otherwise build the path $P$ in $T$ from $u$ to $v$ and an edge $f$ of $P$ that crosses the cut, as above. Then $w(f) \ge w(e)$. If $w(f) > w(e)$, the tree $T'$ would be lighter than $T$, which is false. So $w(f) = w(e)$, and $f \in T$ is a light edge of the cut. $\square$

For a disconnected graph, apply the proofs inside the component that holds $e$: the path $P$ exists because $u$ and $v$ are in the same component, and the exchange keeps the components of the forest. $\blacksquare$

## Consequences

- **The generic method.** The [generic MST method](/generic-mst-method/) adds one [safe edge](/safe-edge/) at a time, and part 1 shows that a light edge of a cut that respects the current set is safe. All the classical algorithms are instances.
- **[Kruskal's algorithm](/kruskal/).** The next edge in sorted order that joins two trees is light for the cut around one of the two trees.
- **[Prim's algorithm](/prim/).** The cut is the tree grown so far against the rest of the graph, and the algorithm takes a light edge of it.
- **[Borůvka's algorithm](/boruvka/).** Each component takes a light edge of the cut around it. With ties, the edges of one round can close a cycle, so Borůvka needs a fixed tie-break. With an order that breaks ties, part 3 applies to each cut, and all chosen edges are in the one minimum spanning tree of the strict order.
- **Uniqueness.** If all weights are distinct, each edge of a minimum spanning tree $T$ is the only light edge of the cut that $T \setminus \{e\}$ defines, so part 3 gives [uniqueness of the MST](/mst-uniqueness/).
- **The [cycle property](/cycle-property/)** is the dual statement, the *red rule*. Together they give the [greedy MST algorithm](/greedy-mst-algorithm/) of Tarjan, which may apply the two rules in any order.
- **[Minimum bottleneck spanning tree](/minimum-bottleneck-spanning-tree/).** Part 4 is one way to show that each minimum spanning tree also minimizes the largest edge weight.

## Tightness

The hypotheses cannot be dropped.

- **"Some" cannot become "every" with ties.** Take a cycle $a, b, c, d$ with the four edges of weight 1. Each of its 4 spanning trees has weight 3 and is minimum. For the cut $S = \{a\}$, the edges $ab$ and $ad$ are both light, and the tree $\{ad, dc, cb\}$ does not contain $ab$. So part 3 needs the light edge to be the only one.
- **The cut must respect $A$.** Take the triangle with $w(ab) = 1$ and $w(bc) = w(ac) = 2$, and let $A = \{ab, bc\}$, which is a minimum spanning tree. The cut $S = \{a, b\}$ is crossed by $bc$ and $ac$, both of weight 2, so $ac$ is light. But $A \cup \{ac\}$ is the whole triangle, a cycle, and it is in no spanning tree. The theorem does not apply, because $bc \in A$ crosses the cut.
- **Light for the cut, not for a vertex of it.** An edge that is lightest at one vertex of $S$, but not among all edges that cross the cut, can be outside every minimum spanning tree. In the triangle above with $S = \{a, b\}$, the edge $ac$ is the lightest edge at $a$ that crosses the cut, but $bc$ is lighter, and $ac$ is in no minimum spanning tree.

**An example.** In the graph with the vertices $a$ to $f$ and the edges $ab = 4$, $ac = 3$, $bc = 1$, $bd = 2$, $cd = 4$, $ce = 5$, $de = 7$, $df = 6$, $ef = 2$, the cut $S = \{a, b, c\}$ is crossed by $bd$, $cd$ and $ce$, of weights 2, 4 and 5. The only light edge is $bd$, so $bd$ is in every minimum spanning tree. The cut $S = \{e, f\}$ is crossed by $ce$, $de$ and $df$, of weights 5, 7 and 6, so $ce$ is also in every minimum spanning tree. The graph has one minimum spanning tree, $\{bc, bd, ef, ac, ce\}$ of weight 13, which [Kruskal's algorithm](/kruskal/) finds.

## History

The exchange argument goes back to the first papers on the problem, by Borůvka (1926), Jarník (1930), Kruskal (1956) and Prim (1957), each for distinct weights or for its own algorithm. The names "blue rule" and "red rule", and the view of all the classical algorithms as applications of these two rules in different orders, are from Tarjan's 1983 monograph (Chapter 6). Textbooks now state the cut property for a cut that respects a partial solution, which handles ties, as CLRS does in Section 21.1.

## References
