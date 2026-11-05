---
tag: KY82A5
kind: theorem
slug: mst-optimality-conditions
name: MST optimality conditions
area: graphs/spanning-trees
level: core
summary: Theorem stating a spanning tree is minimal exactly when no non-tree edge is heavier than every edge on its tree cycle.
prereqs: [minimum-spanning-tree, fundamental-cycle, cut]
see_also: [cut-property, cycle-property, mst-uniqueness, mst-verification, mst-sensitivity-analysis, safe-edge, second-best-mst]
sources:
  - book: isbn:9780136175490
    title: Ravindra K. Ahuja, Thomas L. Magnanti and James B. Orlin, Network Flows, Theory, Algorithms, and Applications
    locator: Chapter 13, Minimum Spanning Trees, Section 13.3, Optimality conditions (the cut optimality and path optimality conditions and the proof of their equivalence)
  - book: isbn:9780898711875
    title: Robert E. Tarjan, Data Structures and Network Algorithms
    locator: Chapter 6, Minimum spanning trees (the red rule and the blue rule)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 21, Section 21.1, Growing a minimum spanning tree (Theorem 21.1, the cut property)
---

The MST optimality conditions say when a given spanning tree $T$ is a [minimum spanning tree](/minimum-spanning-tree/), with a test that looks only at $T$ and one edge at a time. The *path condition*: each edge outside $T$ weighs at least as much as each edge on the path in $T$ between its ends. The *cut condition*: each edge of $T$ weighs at most as much as each edge that crosses the cut that the tree edge defines. Both are equivalent to minimality. So minimality, a global property over all spanning trees, can be checked locally, which is the base of [MST verification](/mst-verification/) and [sensitivity analysis](/mst-sensitivity-analysis/).

## Statement

Let $G = (V, E)$ be a finite, connected, undirected graph with a weight $w(e) \in \mathbb{R}$ on each edge. Weights may tie and may be negative. Parallel edges are allowed. Let $T$ be a spanning tree of $G$.

- For an edge $e = uv \notin T$, let $P_T(e)$ be the set of edges of the path from $u$ to $v$ in $T$. With $e$, these edges form the [fundamental cycle](/fundamental-cycle/) of $e$.
- For an edge $f \in T$, removing $f$ splits $T$ into two trees. Let $S_f$ be the vertex set of one of them. The *fundamental cut* of $f$ is the set $D_T(f)$ of edges of $G$ with exactly one end in $S_f$. It contains $f$, and $f$ is its only edge in $T$.

**Theorem.** The following are equivalent.

1. $T$ is a minimum spanning tree of $G$.
2. **(Path condition.)** For each $e \notin T$ and each $f \in P_T(e)$: $w(e) \ge w(f)$.
3. **(Cut condition.)** For each $f \in T$ and each $e \in D_T(f)$: $w(f) \le w(e)$.

The graph must be connected so that a spanning tree exists. For a graph that is not connected, the theorem holds for spanning forests, with paths and cuts taken inside each component.

## In plain words

You have a network of roads that connects all towns, and you want to know if it is the cheapest one. You do not need to compare it with all other networks.

Take one road that you did not build. Adding it would close a loop with your roads. If it is cheaper than some road on that loop, swap them and you save money, so your network was not the cheapest. The theorem says the converse also holds: if no unused road is cheaper than a road on its loop, your network is the cheapest.

The second test looks from the other side. Remove one of your roads, and the towns fall into two groups. The removed road must be among the cheapest roads between the two groups.

## Proof

**One exchange.** For $e \notin T$ and $f \in P_T(e)$, the set $T - f + e = (T \setminus \{f\}) \cup \{e\}$ is a spanning tree. Removing $f$ splits $T$ into two trees, and the ends of $e$ lie in different ones, because the only path between them in $T$ uses $f$. Adding $e$ joins them again, so the result is connected with $n - 1$ edges. Its weight is $w(T) - w(f) + w(e)$.

**The two conditions say the same thing.** For $e \notin T$ and $f \in T$: $f \in P_T(e)$ if and only if $e \in D_T(f)$. Indeed, $e \in D_T(f)$ means that the ends of $e$ are in different trees of $T \setminus \{f\}$. That holds if and only if the path in $T$ between the ends of $e$ uses $f$. The pairs $(e, f)$ with $e \in T$ add nothing to the cut condition: the only tree edge in $D_T(f)$ is $f$, and $w(f) \le w(f)$. So conditions 2 and 3 compare the same pairs of edges in the same direction, and 2 holds if and only if 3 holds.

**1 implies 2.** Let $T$ be an MST, $e \notin T$ and $f \in P_T(e)$. If $w(e) < w(f)$, then $T - f + e$ is a spanning tree with weight less than $w(T)$, which is false. So $w(e) \ge w(f)$.

**3 implies 1.** Let $T$ satisfy the cut condition. Among all minimum spanning trees, choose $T^*$ with the largest number of edges in common with $T$. Such a $T^*$ exists because $G$ has finitely many spanning trees and at least one. Suppose that $T^* \ne T$. Both have $n - 1$ edges, so there is an edge $f \in T \setminus T^*$.

1. Add $f$ to $T^*$. Since $f \notin T^*$, the set $P_{T^*}(f)$ is defined, and $P_{T^*}(f) \cup \{f\}$ is a cycle.
2. The edge $f$ crosses the fundamental cut $D_T(f)$, so the cycle crosses it once along $f$. A cycle crosses each cut an even number of times, so the cycle has another edge $e \ne f$ in $D_T(f)$. Then $e \in P_{T^*}(f) \subseteq T^*$.
3. The only edge of $T$ in $D_T(f)$ is $f$, so $e \notin T$.
4. The cut condition for $T$ gives $w(f) \le w(e)$.
5. $T^*$ is an MST, so it satisfies the path condition (1 implies 2). Since $f \notin T^*$ and $e \in P_{T^*}(f)$, this gives $w(f) \ge w(e)$. So $w(e) = w(f)$.
6. The exchange $T^{**} = T^* - e + f$ is a spanning tree of weight $w(T^*) - w(e) + w(f) = w(T^*)$, so it is an MST. It has one more edge in common with $T$ than $T^*$: it gains $f \in T$ and loses $e \notin T$.

Step 6 contradicts the choice of $T^*$. So $T^* = T$, and $T$ is an MST.

With "2 if and only if 3", the three conditions are equivalent. $\blacksquare$

## Consequences

- **The cut and cycle properties.** The [cut property](/cut-property/) and the [cycle property](/cycle-property/) are the rules that the conditions turn into algorithms. Tarjan calls them the *blue rule* (color a lightest edge of a cut blue, that is, take it) and the *red rule* (color a heaviest edge of a cycle red, that is, drop it). Any order of applications of the two rules ends with an MST.
- **Correctness of greedy algorithms.** [Kruskal's](/kruskal/), [Prim's](/prim/) and [Borůvka's](/boruvka/) algorithms apply the blue rule, and [reverse-delete](/reverse-delete/) applies the red rule.
- **Uniqueness.** The strict form of the path condition, $w(e) > w(f)$ for each pair, holds exactly when $T$ is the only MST ([MST uniqueness](/mst-uniqueness/)).
- **Verification.** Condition 2 asks, for each non-tree edge $e$, for the heaviest edge on its tree path. This is a set of path-maximum queries on a tree. Komlós showed that $O(m)$ comparisons suffice, and Dixon, Rauch and Tarjan, and later King, gave linear-time algorithms ([MST verification](/mst-verification/)).
- **Sensitivity.** A tree edge $f$ stays in the MST while $w(f)$ is at most the lightest non-tree edge of its cut, and a non-tree edge $e$ stays out while $w(e)$ is at least the heaviest edge of its path ([MST sensitivity analysis](/mst-sensitivity-analysis/)).
- **Second-best trees.** The [second-best MST](/second-best-mst/) is $T - f + e$ for the pair $(e, f)$ with $f \in P_T(e)$ that minimizes $w(e) - w(f)$.

## Tightness

**A tree that fails the conditions.** Take the graph on $a$ to $f$ with the weights $ab = 4$, $ac = 3$, $bc = 1$, $bd = 2$, $cd = 4$, $ce = 5$, $de = 7$, $df = 6$, $ef = 2$. The spanning tree $T = \{ab, bc, bd, ce, ef\}$ has weight 14. The non-tree edge $ac$ has the path $a, b, c$ in $T$, with $ab = 4 > 3 = w(ac)$. The path condition fails, and the exchange $T - ab + ac$ gives the MST $\{ac, bc, bd, ce, ef\}$ of weight 13. In the same tree, the cut condition fails at $f = ab$: the fundamental cut of $ab$ separates $\{a\}$ from the rest, and $ac$ crosses it with a smaller weight.

**The inequalities cannot be strict.** With ties, an MST can have $w(e) = w(f)$ for some $f \in P_T(e)$. In the triangle with weights $1, 2, 2$, the MST $\{1, 2\}$ has the non-tree edge of weight 2 on a path that holds the other edge of weight 2. So "$\ge$" in condition 2 cannot be replaced by "$>$" as a test for minimality; the strict form is the test for uniqueness.

**The conditions need a spanning tree.** The conditions say nothing about a set of edges that is not a spanning tree. For example, the empty set has no paths, and a forest with two trees has no tree path for an edge that joins them. The proof of "3 implies 1" uses that $T$ has $n - 1$ edges.

## History

The two conditions are the classical cut and cycle rules, which go back to the first papers on the problem: Borůvka (1926) and Jarník (1930) used the cut rule, and Kruskal (1956) described methods based on both. Tarjan's book (1983, Chapter 6) presents the red and blue rules as one framework. Ahuja, Magnanti and Orlin (1993, Chapter 13) state the path and cut optimality conditions in the form above and prove their equivalence by the exchange argument.

## References
