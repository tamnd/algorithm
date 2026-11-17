---
tag: 6RYT0Z
kind: definition
slug: hypertree-width
name: Hypertree width
aliases:
- generalized hypertree width
area: databases/relational-theory
level: advanced
summary: A width measure of the hypergraph of a query; conjunctive queries of bounded hypertree width can be evaluated in polynomial time.
prereqs: [hypergraph, tree-decomposition, acyclic-hypergraph]
see_also: [fractional-hypertree-width, treewidth, gyo-reduction, yannakakis-algorithm, conjunctive-query, constraint-satisfaction-problem, edge-cover, np-complete]
sources:
  - paper: doi:10.1006/jcss.2001.1809
    title: Georg Gottlob, Nicola Leone and Francesco Scarcello, Hypertree decompositions and tractable queries, Journal of Computer and System Sciences 64(3), 579 to 627 (2002)
    locator: the definition of hypertree decompositions and hypertree width, width 1 for exactly the acyclic hypergraphs, and the polynomial test and evaluation for fixed width
  - paper: doi:10.1145/1568318.1568320
    title: Georg Gottlob, Zoltan Miklos and Thomas Schwentick, Generalized hypertree decompositions, NP-hardness and tractable variants, Journal of the ACM 56(6), article 30 (2009)
    locator: deciding whether the generalized hypertree width is at most 3 is NP-complete
  - paper: doi:10.1145/3196959.3196962
    title: Wolfgang Fischl, Georg Gottlob and Reinhard Pichler, General and fractional hypertree decompositions, hard and easy cases, Proceedings of the 37th ACM Symposium on Principles of Database Systems (PODS), 17 to 32 (2018)
    locator: deciding whether the generalized hypertree width is at most 2 is NP-complete
  - paper: doi:10.1016/j.ejc.2007.04.013
    title: Isolde Adler, Georg Gottlob and Martin Grohe, Hypertree width and related hypergraph invariants, European Journal of Combinatorics 28(8), 2167 to 2181 (2007)
    locator: hypertree width is equal, up to a constant factor, to several other hypergraph invariants
---

Hypertree width measures how far a [hypergraph](/hypergraph/) is from being [acyclic](/acyclic-hypergraph/). It is defined by a *hypertree decomposition*, a [tree decomposition](/tree-decomposition/) whose bags are each covered by a few edges of the hypergraph, and the width is the largest number of covering edges at one node. Gottlob, Leone and Scarcello (2002) defined it. The acyclic hypergraphs are exactly those of hypertree width 1. For each fixed $k$, one can decide in polynomial time whether the width is at most $k$ and find a decomposition, and a [conjunctive query](/conjunctive-query/) whose hypergraph has width at most $k$ can be evaluated in polynomial time. *Generalized hypertree width* drops one condition of the definition. It can only be smaller, but deciding it is [NP-complete](/np-complete/) already for width 2.

## Definition

Let $H = (V, E)$ be a hypergraph. For a set $\lambda \subseteq E$ of edges write $\bigcup \lambda$ for the set of vertices of its edges.

**Definition (Gottlob, Leone and Scarcello 2002).** A *hypertree decomposition* of $H$ is a triple $(T, \chi, \lambda)$, where $T$ is a rooted tree and each node $p$ of $T$ has a bag $\chi(p) \subseteq V$ and a set of edges $\lambda(p) \subseteq E$, such that:

1. for each edge $e \in E$ there is a node $p$ with $e \subseteq \chi(p)$;
2. for each vertex $v \in V$ the set $\{ p : v \in \chi(p) \}$ induces a connected subtree of $T$;
3. for each node $p$, $\chi(p) \subseteq \bigcup \lambda(p)$;
4. for each node $p$, $\bigcup \lambda(p) \cap \chi(T_p) \subseteq \chi(p)$, where $\chi(T_p)$ is the union of the bags in the subtree of $T$ rooted at $p$.

Conditions 1 and 2 say that $(T, \chi)$ is a tree decomposition of $H$. Condition 3 says that the edges of $\lambda(p)$ cover the bag. Condition 4 is the *special condition*: a vertex of a covering edge that is left out of the bag must not come back lower in the tree. The *width* of the decomposition is $\max_p |\lambda(p)|$. The *hypertree width* $\mathrm{hw}(H)$ is the smallest width of a hypertree decomposition of $H$.

**Generalized hypertree width.** A *generalized hypertree decomposition* has to meet only conditions 1, 2 and 3. Its smallest width is the *generalized hypertree width* $\mathrm{ghw}(H)$. It is a different measure, so the alias on this page names a close relative, not the same number. Each hypertree decomposition is a generalized one, so $\mathrm{ghw}(H) \le \mathrm{hw}(H)$. Adler, Gottlob and Grohe (2007) showed that hypertree width agrees, up to a constant factor, with several other hypergraph invariants.

**Facts.**

- *Width 1 (theorem).* $\mathrm{hw}(H) = 1$ if and only if $H$ is acyclic and has at least one edge (Gottlob, Leone and Scarcello). A join tree, with $\chi(p) = e_p$ and $\lambda(p) = \{e_p\}$, is a hypertree decomposition of width 1.
- *Recognition (theorem).* For each fixed $k$, deciding $\mathrm{hw}(H) \le k$ and computing a decomposition of width at most $k$ takes polynomial time. The problem is in the class LOGCFL (Gottlob, Leone and Scarcello).
- *Generalized width is hard (theorem).* Deciding $\mathrm{ghw}(H) \le 3$ is NP-complete (Gottlob, Miklos and Schwentick 2009), and so is deciding $\mathrm{ghw}(H) \le 2$ (Fischl, Gottlob and Pichler 2018). So without the special condition the test for a fixed small width is already NP-hard.
- *Evaluation (theorem).* Let $Q$ be a conjunctive query whose hypergraph has a hypertree decomposition of width $k$, and let each relation of the database have at most $N$ tuples. At each node $p$, join the at most $k$ relations of $\lambda(p)$ and project on $\chi(p)$, which gives at most $N^k$ tuples. The new relations form an acyclic query along $T$, and the [Yannakakis algorithm](/yannakakis-algorithm/) finishes. The time is polynomial in $N^k$, the size of the query and the size of the output. This is combined complexity, and the same holds for generalized decompositions once one is given.

## Examples and non-examples

- **Acyclic hypergraphs.** The path $AB$, $BC$, $CD$ has width 1, from its join tree.
- **The triangle.** The edges $e_1 = AB$, $e_2 = BC$, $e_3 = CA$ are cyclic, so the width is at least 2. One node with $\chi = \{A, B, C\}$ and $\lambda = \{e_1, e_2\}$ is a hypertree decomposition of width 2. So $\mathrm{hw} = 2$.
- **Cycles.** Let $C_n$, for $n \ge 3$, have the vertices $v_1, \ldots, v_n$ and the edges $e_i = \{v_i, v_{i+1}\}$, with $v_{n+1} = v_1$. Take a path of nodes $p_2, \ldots, p_{n-1}$, with
  $$\chi(p_i) = \{v_1, v_i, v_{i+1}\}, \qquad \lambda(p_i) = \{e_i, e_n\},$$
  rooted at $p_{n-1}$. Each edge lies in a bag: $e_1$ in $\chi(p_2)$, $e_i$ in $\chi(p_i)$, and $e_n = \{v_n, v_1\}$ in $\chi(p_{n-1})$. Vertex $v_1$ is in all bags, and $v_i$ is in $\chi(p_{i-1})$ and $\chi(p_i)$ only. The covering edges add only $v_n$ outside the bag, and $v_n$ is only in the root bag, so condition 4 holds. So $\mathrm{hw}(C_n) = 2$ for every $n$, while the cycle is not acyclic.
- **One big edge.** A hypergraph with the single edge $V$ has width 1 for every size of $V$. Its primal graph is a complete graph, of [treewidth](/treewidth/) $|V| - 1$. So hypertree width can be much smaller than treewidth.
- **Treewidth bounds generalized width.** If every vertex is in some edge, then $\mathrm{ghw}(H) \le \mathrm{tw}(H) + 1$, where $\mathrm{tw}$ is the treewidth of the primal graph. Take a tree decomposition of the primal graph with bags of at most $\mathrm{tw} + 1$ vertices, and cover each vertex of a bag by one edge that contains it. Each edge of $H$ is a clique of the primal graph, so some bag contains it.
- **Unbounded width: grids.** For a graph, read as a hypergraph with binary edges, each edge covers 2 vertices, so a bag of $b$ vertices needs at least $b / 2$ edges. Hence $\mathrm{ghw} \ge (\mathrm{tw} + 1) / 2$, and an $n \times n$ grid, of treewidth $n$, has unbounded width as $n$ grows.

## Related definitions

- **Fractional hypertree width.** Replace the number of covering edges by the weight of a fractional [edge cover](/edge-cover/) of the bag. This gives [fractional hypertree width](/fractional-hypertree-width/), which is at most the generalized hypertree width and can be much smaller.
- **Treewidth.** For graphs, read as hypergraphs with binary edges, the bounds above give $(\mathrm{tw} + 1) / 2 \le \mathrm{ghw} \le \mathrm{tw} + 1$, so treewidth and generalized hypertree width are within a factor of 2 of each other. For hypergraphs with large edges they can be far apart, as the single edge shows.
- **Acyclicity and GYO.** Width 1 is acyclicity, tested by the [GYO reduction](/gyo-reduction/).
- **Constraint satisfaction.** A [constraint satisfaction problem](/constraint-satisfaction-problem/) whose constraint hypergraph has bounded hypertree width is solvable in polynomial time by the same method as query evaluation.

## References
