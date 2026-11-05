---
tag: ZJCSGN
kind: theorem
slug: mst-uniqueness
name: Uniqueness of the minimum spanning tree
area: graphs/spanning-trees
level: intro
summary: If all edge weights are distinct, the minimum spanning tree is unique.
prereqs: [minimum-spanning-tree, fundamental-cycle, cut]
see_also: [mst-optimality-conditions, cut-property, cycle-property, second-best-mst, kruskal, boruvka, mst-verification]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 21, Section 21.1, Growing a minimum spanning tree (the exercises of the section on unique light edges and unique MSTs)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Eva Tardos, Algorithm Design
    locator: Section 4.5, The minimum spanning tree problem (the assumption of distinct costs and how to remove it)
  - paper: doi:10.1090/S0002-9939-1956-0078686-7
    title: "Joseph B. Kruskal, On the shortest spanning subtree of a graph and the traveling salesman problem, Proceedings of the American Mathematical Society 7(1) (1956), 48-50"
    locator: the theorem on uniqueness when all lengths are different
  - book: isbn:9781792644832
    title: Jeff Erickson, Algorithms
    locator: Chapter 7, Minimum Spanning Trees (Section 7.1, Distinct edge weights)
---

The uniqueness theorem says that a connected weighted graph whose edge weights are all distinct has exactly one [minimum spanning tree](/minimum-spanning-tree/). A sharper form says when the MST is unique for any weights: exactly when each edge outside the tree is strictly heavier than every edge on the tree path between its ends. Many MST algorithms and proofs assume distinct weights for this reason, and a fixed tie-break on the edge index makes any input look like one with distinct weights.

## Statement

Let $G = (V, E)$ be a finite, connected, undirected graph with a weight $w(e) \in \mathbb{R}$ on each edge. Parallel edges are allowed. For a spanning tree $T$ and an edge $e = uv \notin T$, write $P_T(e)$ for the set of edges of the unique path from $u$ to $v$ in $T$. The edges of $P_T(e)$ and $e$ form the [fundamental cycle](/fundamental-cycle/) of $e$.

**Theorem.**

1. *(Characterization.)* Let $T$ be an MST of $G$. Then $T$ is the only MST of $G$ if and only if $w(e) > w(f)$ for each edge $e \notin T$ and each edge $f \in P_T(e)$.
2. *(Distinct weights.)* If the weights are pairwise distinct, that is, $w(e) \ne w(e')$ for each two different edges $e \ne e'$, then $G$ has exactly one MST.
3. *(The converse of 2 is false.)* A graph with tied weights can still have a unique MST.

The graph must be connected for the statement to be about trees. For a graph that is not connected, the same three claims hold for minimum spanning forests, applied to each component.

## In plain words

If no two cables have the same price, there is only one cheapest network. The reason: if there were two different cheapest networks, you could take a cable that is in one and not in the other, and swap it for a cable of the other network. Because the prices differ, one of the two swaps would make a network cheaper than the cheapest, which is impossible.

When prices can tie, there may be several cheapest networks, but not always. The exact test is this: take each cable that is not in your network. Adding it closes one loop. If it is more expensive than every cable on that loop, no other cheapest network exists. If it costs the same as some cable on the loop, swap the two, and you get a second cheapest network.

## Proof

We use one exchange step. Let $T$ be a spanning tree, $e \notin T$ and $f \in P_T(e)$. Then $T' = T \setminus \{f\} \cup \{e\}$ is a spanning tree. Removing $f$ splits the tree $T$ into two trees, and the ends of $e$ are in different ones, because the only path in $T$ between them uses $f$. Adding $e$ joins the two trees again. So $T'$ is connected with $n - 1$ edges, and it is a spanning tree with $w(T') = w(T) - w(f) + w(e)$.

**Step 1: the weak condition holds for each MST.** Let $T$ be an MST, $e \notin T$ and $f \in P_T(e)$. If $w(e) < w(f)$, the exchange gives a spanning tree lighter than $T$, which is false. So $w(e) \ge w(f)$.

**Step 2: part 1, "only if".** Let $T$ be the only MST, and suppose that $w(e) \le w(f)$ for some $e \notin T$ and $f \in P_T(e)$. By Step 1, $w(e) = w(f)$. The exchange gives a spanning tree $T' \ne T$ with $w(T') = w(T)$, so $T'$ is a second MST, which is false. So $w(e) > w(f)$ for each such pair.

**Step 3: part 1, "if".** Let $T$ be an MST with $w(e) > w(f)$ for each $e \notin T$ and $f \in P_T(e)$. Suppose that $T^\circ \ne T$ is also an MST. Both have $n - 1$ edges, so there is an edge $f \in T \setminus T^\circ$.

Removing $f$ from $T$ leaves two trees with vertex sets $S$ and $V \setminus S$. The edge $f$ is the only edge of $T$ with one end in $S$ and the other in $V \setminus S$.

Add $f$ to $T^\circ$. Since $f \notin T^\circ$, this closes the fundamental cycle $C$ of $f$ with respect to $T^\circ$. The cycle $C$ crosses from $S$ to $V \setminus S$ along $f$ and must come back, so it has a second edge $e \ne f$ with one end in $S$ and one in $V \setminus S$. This edge lies in $T^\circ$, since $C \setminus \{f\} \subseteq T^\circ$.

The edge $e$ is not in $T$, because $f$ is the only edge of $T$ across the cut. Its two ends are in different trees of $T \setminus \{f\}$, so the path in $T$ between them uses $f$, that is, $f \in P_T(e)$. The hypothesis gives $w(e) > w(f)$.

Now $e \in P_{T^\circ}(f)$, because $e$ is on the cycle that $f$ closes with $T^\circ$. The exchange in $T^\circ$ gives the spanning tree $T^\circ \setminus \{e\} \cup \{f\}$ of weight $w(T^\circ) - w(e) + w(f) < w(T^\circ)$. This contradicts the minimality of $T^\circ$. So $T$ is the only MST.

**Step 4: part 2.** Since $G$ is connected and finite, an MST $T$ exists. Let $e \notin T$ and $f \in P_T(e)$. Then $e \ne f$, so $w(e) \ne w(f)$ by the hypothesis, and $w(e) \ge w(f)$ by Step 1. So $w(e) > w(f)$, and part 1 shows that $T$ is the only MST.

**Step 5: part 3.** The triangle with weights $1, 1, 2$ has two tied weights. Its tree $T$ of the two edges of weight 1 has weight 2, and the other two trees have weight 3. The only edge outside $T$ has weight 2, and both edges of its path have weight 1, so by part 1 the MST is unique. $\blacksquare$

## Consequences

- **Every correct algorithm returns the same tree.** With distinct weights, [Kruskal](/kruskal/), [Prim](/prim/), [Borůvka](/boruvka/) and [reverse-delete](/reverse-delete/) all return the one MST. Tests can then compare the edge sets, not only the weights.
- **Tie-breaking.** Order the edges by the pair $(w(e), \mathrm{index}(e))$ in lexicographic order. This is a total order with no ties, so it has a unique MST $T$. That tree is also an MST for $w$: for each $e \notin T$ and $f \in P_T(e)$, the pair of $e$ is larger than the pair of $f$, so $w(e) \ge w(f)$, and this weak condition is enough for an MST ([MST optimality conditions](/mst-optimality-conditions/)). [Borůvka's algorithm](/boruvka/) needs such a rule. With ties and no rule, two components can pick two different edges of the same weight between them, and the chosen edges can form a cycle.
- **The cut and cycle properties become exact.** With distinct weights, the lightest edge of each cut is in the MST, and the heaviest edge of each cycle is not. This gives a simple description of the MST as the set of edges that are the lightest in some cut ([cut property](/cut-property/), [cycle property](/cycle-property/)).
- **Testing uniqueness.** By part 1, the MST $T$ is unique if and only if no non-tree edge $e$ ties with the heaviest edge of $P_T(e)$. The heaviest edge on each path can be found with the methods of [MST verification](/mst-verification/), so the test runs in the same time as one MST computation plus $O(m \log n)$ for path maximum queries, or $O(m)$ with the linear-time verification algorithms.
- **Second-best trees.** The [second-best MST](/second-best-mst/) differs from an MST by one exchange. When the MST is unique, its weight is strictly larger than the minimum.

## Tightness

The hypothesis "distinct weights" cannot be dropped in part 2. In the triangle with weights $1, 2, 2$, the two trees $\{1, 2\}$ (one for each edge of weight 2) both have weight 3, so there are two MSTs. In the cycle $C_4$ with all weights 1, each of the four spanning trees is an MST. If all weights of a graph are equal, every spanning tree is an MST, and [Cayley's formula](/cayley-formula/) gives $n^{n-2}$ of them for the complete graph $K_n$.

Part 3 shows that part 2 is only a sufficient condition. A larger example: the graph with vertices $a$ to $f$ and weights $ab = 4$, $ac = 3$, $bc = 1$, $bd = 2$, $cd = 4$, $ce = 5$, $de = 7$, $df = 6$, $ef = 2$ has two tied pairs, but its MST $\{bc, bd, ef, ac, ce\}$ is the only spanning tree of weight 13 among its 55 spanning trees. Each non-tree edge is strictly heavier than its tree path: $ab = 4 > 3, 1$; $cd = 4 > 1, 2$; $de = 7 > 2, 1, 5$; $df = 6 > 2, 1, 5, 2$.

## History

Borůvka's paper of 1926 already assumes that all distances are different. Kruskal's paper of 1956 gives his construction for a graph with distinct lengths and proves in the same paper that the shortest spanning tree is then unique. Textbooks such as Kleinberg and Tardos (Section 4.5) and Erickson (Chapter 7) first assume distinct weights for the same reason, and then remove the assumption with a tie-break rule.

## References
