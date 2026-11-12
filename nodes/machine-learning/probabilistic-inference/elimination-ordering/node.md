---
tag: BG2816
kind: concept
slug: elimination-ordering
name: Elimination ordering
aliases:
- min-fill heuristic
- variable elimination order
area: machine-learning/probabilistic-inference
level: advanced
summary: "The order in which variable elimination removes the variables. Its induced width sets the cost; the least width over all orders is the treewidth."
prereqs: [variable-elimination, treewidth, chordal-graph]
see_also: [perfect-elimination-ordering, tree-decomposition, treewidth-computation, junction-tree, maximum-cardinality-search, minimum-degree-ordering, fill-in, bucket-elimination]
sources:
  - paper: doi:10.1137/0608024
    title: "Stefan Arnborg, Derek G. Corneil and Andrzej Proskurowski, Complexity of finding embeddings in a k-tree, SIAM Journal on Algebraic and Discrete Methods 8(2), 1987, pages 277 to 284"
    locator: the NP-completeness of deciding whether a graph is a partial k-tree (treewidth at most k) when k is part of the input, and the O(n^(k+2)) algorithm for fixed k
  - paper: doi:10.1137/0205021
    title: "Donald J. Rose, R. Endre Tarjan and George S. Lueker, Algorithmic aspects of vertex elimination on graphs, SIAM Journal on Computing 5(2), 1976, pages 266 to 283"
    locator: elimination graphs, fill-in, perfect elimination orderings of chordal graphs, and lexicographic breadth-first search
  - paper: doi:10.1137/0602010
    title: "Mihalis Yannakakis, Computing the minimum fill-in is NP-complete, SIAM Journal on Algebraic and Discrete Methods 2(1), 1981, pages 77 to 79"
    locator: the NP-completeness of the minimum fill-in problem
  - book: isbn:9780262013192
    title: Daphne Koller and Nir Friedman, Probabilistic Graphical Models, Principles and Techniques, MIT Press, 2009
    locator: "Chapter 9, Section 9.4 (the induced graph, induced width, chordal graphs, and the greedy min-neighbors, min-weight, min-fill and weighted min-fill orderings)"
---

An elimination ordering is the order in which [variable elimination](/variable-elimination/) removes the variables of a graphical model. The order fixes the size of the tables that the algorithm builds: with an order of induced width $w$, each table has at most $w + 1$ variables, and the cost is exponential in $w$. The least induced width over all orders of a graph is its [treewidth](/treewidth/), so finding the best order is NP-hard. In practice the greedy min-degree and min-fill heuristics give good orders, and on a [chordal graph](/chordal-graph/) a [perfect elimination ordering](/perfect-elimination-ordering/) is optimal and adds no new edges.

## In plain words

Variable elimination removes one variable at a time. When it removes a variable, it joins all the tables that mention that variable into one big table. That big table mentions the variable and all of its current neighbours. After the step, those neighbours are all linked to each other.

So the order matters a lot. If you remove a well connected variable early, you build a huge table and you link many variables that were not linked before. If you remove the loose ends first, the tables stay small.

The best order is hard to find. Two simple rules work well: remove the variable with the fewest neighbours, or remove the variable whose removal adds the fewest new links.

## The idea

In this page $n$ is the number of variables and $d$ the largest domain size. Let $G = (V, E)$ be the interaction graph of a model: one vertex per variable, and an edge between two variables that appear together in a factor. For a [Bayesian network](/bayesian-network/) this is the moral graph.

**Elimination.** To *eliminate* a vertex $v$ from a graph, add an edge between each pair of neighbours of $v$ that are not adjacent (the *fill edges*), then delete $v$. An elimination ordering is an order $\pi = (v_1, \ldots, v_n)$ of $V$. Let $G_0 = G$ and let $G_i$ be $G_{i-1}$ with $v_i$ eliminated.

**Induced width.** The width of $\pi$ is
$$w(\pi) = \max_{1 \le i \le n} \deg_{G_{i-1}}(v_i),$$
the largest number of neighbours that a vertex has when it is eliminated. The *filled graph* $G_\pi^+$ is $G$ with all the fill edges added. The fill-in of $\pi$ is the number of fill edges. In variable elimination, the table built when $v_i$ is eliminated has exactly the variables $\{v_i\} \cup N_{G_{i-1}}(v_i)$, so its size is at most $d^{w(\pi) + 1}$, and the time is $O(n d^{w(\pi)+1})$ on a Bayesian network.

**The filled graph is chordal.** In $G_\pi^+$, the neighbours of $v_i$ that come later in $\pi$ are exactly $N_{G_{i-1}}(v_i)$, and they form a clique, because the elimination of $v_i$ joined them. So $\pi$ is a [perfect elimination ordering](/perfect-elimination-ordering/) of $G_\pi^+$, and $G_\pi^+$ is a [chordal graph](/chordal-graph/) by the theorem of Fulkerson and Gross. Its largest clique has $w(\pi) + 1$ vertices. Conversely, each chordal supergraph $H$ of $G$ has a perfect elimination ordering $\sigma$, and on $G$ the order $\sigma$ adds only edges of $H$, so $w(\sigma) \le \omega(H) - 1$. Rose, Tarjan and Lueker (1976) worked out this link between elimination and chordal graphs.

**Theorem (minimum width equals treewidth).** For each graph $G$, $\min_\pi w(\pi) = \mathrm{tw}(G)$.

*Proof.* ($\ge$) Fix $\pi$ and let $H = G_\pi^+$. For each vertex $v$, let $N^+(v)$ be the neighbours of $v$ in $H$ that come after $v$ in $\pi$, and let the bag of $v$ be $B_v = \{v\} \cup N^+(v)$. It has at most $w(\pi) + 1$ vertices. Make the bag of $v$ a child of the bag of $p(v)$, the first vertex of $N^+(v)$ in $\pi$; if $N^+(v)$ is empty, make it a child of the bag of the next vertex in $\pi$ (or the root, for the last vertex). This is a tree, since each parent comes later in $\pi$. Each edge $uv$ of $G$ with $u$ before $v$ has $v \in N^+(u)$, so it lies in $B_u$. For the connectivity condition, take a vertex $x$ and a bag $B_v \ni x$ with $v \ne x$. Then $x \in N^+(v)$. If $p(v) \ne x$, both $p(v)$ and $x$ are in $N^+(v)$, which is a clique of $H$, and $x$ comes after $p(v)$, so $x \in N^+(p(v)) \subseteq B_{p(v)}$. Following parents from $v$, the position in $\pi$ grows and each bag holds $x$, until we reach $B_x$. So the bags that hold $x$ form a connected subtree. This is a [tree decomposition](/tree-decomposition/) of width at most $w(\pi)$.

($\le$) Take a tree decomposition of $G$ of width $k$. We build an order of width at most $k$ and keep this invariant: the bags form a tree decomposition of the current graph. Take a leaf bag $t$ with neighbour bag $s$ (if only one bag is left, eliminate its vertices in any order; each has at most $k$ neighbours). If $B_t \subseteq B_s$, delete $t$. Otherwise pick $v \in B_t \setminus B_s$. By the connectivity condition, $v$ is in no other bag, so each edge at $v$ lies in $B_t$, and $v$ has at most $|B_t| - 1 \le k$ neighbours. Eliminate $v$ and remove it from $B_t$. Its fill edges join vertices of $B_t$, so they are covered, and the invariant holds. Each step deletes a bag or a vertex, so the process ends with all vertices eliminated, and each had at most $k$ neighbours at its turn. $\blacksquare$

**Hardness.** Arnborg, Corneil and Proskurowski (1987) proved that deciding $\mathrm{tw}(G) \le k$ is NP-complete when $k$ is part of the input. By the theorem, so is deciding whether some order has width at most $k$. A different objective, the least number of fill edges, is also NP-hard: Yannakakis (1981) proved that minimum fill-in is NP-complete. The two objectives can disagree on the best order. For each fixed $k$, Arnborg, Corneil and Proskurowski gave an $O(n^{k+2})$ algorithm; see [treewidth computation](/treewidth-computation/) for the faster and approximate algorithms.

**Greedy heuristics.** Both rules eliminate one vertex at a time from the current graph, choose the vertex with the least score, and break ties by a fixed rule.

- *Min-degree* (min-neighbours): the score of $v$ is its current degree. One step costs $O(n)$ with degree counts, plus the cost of adding the fill edges.
- *Min-fill*: the score of $v$ is the number of fill edges its elimination would add. A simple version recomputes the score of each vertex at each step, in $O(n^3)$ per step; practical versions update only the scores near the eliminated vertex.
- *Weighted versions*: when the domains have different sizes, the score is the size of the table the step would build ($\prod_{u \in \{v\} \cup N(v)} d_u$), or the total size of the fill.

Neither rule has a guarantee: each can return an order whose width is larger than the treewidth, and no fixed approximation ratio is known for them. Their width is never smaller than the treewidth, by the theorem.

**Chordal graphs.** If $G$ is chordal, a perfect elimination ordering adds no fill edge, and its width is $\omega(G) - 1 = \mathrm{tw}(G)$, so it is optimal. [Lexicographic BFS](/lexicographic-bfs/) and [maximum cardinality search](/maximum-cardinality-search/) find one in $O(n + |E|)$ time. Min-fill also finds one: a chordal graph has a simplicial vertex (one whose neighbours form a clique), so the least fill score is 0, and eliminating a simplicial vertex leaves a chordal graph.

## Examples

**A star.** The star with centre $0$ and leaves $1, \ldots, 5$. The order $(0, 1, 2, 3, 4, 5)$ eliminates the centre first: its degree is 5, the fill makes the leaves a clique $K_5$, and the width is 5. The order $(1, 2, 3, 4, 5, 0)$ eliminates the leaves first, each with one neighbour, and the width is 1. For binary variables the first order builds a table of $2^6 = 64$ entries, the second only tables of $4$.

**The sprinkler network.** The moral graph of $C \to S$, $C \to R$, $S \to W$, $R \to W$ has the edges $CS$, $CR$, $SW$, $RW$ and the moral edge $SR$. It is chordal. The order $(W, C, S, R)$ is a perfect elimination ordering, adds no fill and has width 2, which is the treewidth.

**The $3 \times 3$ grid.** Its treewidth is 3. With the vertices numbered row by row from 0 to 8, min-degree and min-fill both reach width 3. Min-fill chooses the order $(0, 2, 1, 6, 3, 4, 5, 7, 8)$ and adds the 5 fill edges $\{1,3\}, \{1,5\}, \{3,5\}, \{3,7\}, \{5,7\}$.

**Min-degree is not optimal.** The graph on vertices $0, \ldots, 7$ with the 12 edges $05, 13, 14, 15, 16, 17, 23, 25, 27, 36, 56, 67$ has treewidth 3. Min-degree with ties to the smallest label gives the order $(0, 4, 2, 1, 3, 5, 6, 7)$ of width 4: after $0$ and $4$, vertex $2$ has the least degree, 3, and its elimination joins $3, 5, 7$; then vertex 1 has 4 neighbours. Min-fill gives width 3 on this graph.

**Min-fill is not optimal.** The graph on vertices $0, \ldots, 9$ with the 15 edges $01, 05, 08, 12, 14, 15, 17, 18, 26, 35, 37, 48, 68, 69, 89$ has treewidth 2. Min-fill gives the order $(4, 9, 0, 2, 6, 8, 1, 3, 5, 7)$ of width 3, while min-degree reaches width 2 on it. In a sample of 3000 random graphs with 5 to 8 vertices and edge probability 0.4 (seed 1), min-degree was above the treewidth on 2 graphs and min-fill on none, so both rules are usually close, but neither is always right.

## Where it is used

- [Variable elimination](/variable-elimination/) and [bucket elimination](/bucket-elimination/) take the order as input, and their cost is $O(n d^{w+1})$.
- The [junction tree](/junction-tree/) is built from the filled graph $G_\pi^+$: its cliques are the bags, and the [junction tree algorithm](/junction-tree-algorithm/) costs time exponential in the largest clique.
- [Marginal MAP](/map-inference/) needs a *constrained* order that eliminates all summed variables before the maximized ones, and the constrained width can be much larger than the treewidth.
- In sparse linear algebra, the elimination graph is the graph of [fill-in](/fill-in/) in Gaussian elimination and Cholesky factorization, and [minimum degree ordering](/minimum-degree-ordering/) and [nested dissection](/nested-dissection/) are the same kind of order with the number of fill entries as the goal.
- [Dynamic programming on tree decompositions](/dp-on-tree-decompositions/) for NP-hard graph problems uses a decomposition that an order of small width gives.

## References
