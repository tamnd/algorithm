---
tag: 3EPVRE
kind: theorem
slug: tree-edge-count
name: A tree on n nodes has n-1 edges
area: graphs/tree-algorithms
level: intro
summary: Every connected acyclic graph with n vertices has exactly n minus one edges, a basic structural fact about trees.
prereqs: [tree, connected-graph, acyclic-graph, induction]
see_also: [rooted-tree, free-tree-properties, handshake-lemma, spanning-tree, spanning-forest, pruefer-code, cayley-formula]
sources:
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.3.4.1 (Free trees), Theorem A, the equivalent conditions for a finite graph with n vertices to be a free tree
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix B.5.1 (Free trees), Theorem B.2 (Properties of free trees) and its proof
  - book: isbn:9780130144003
    title: Douglas B. West, Introduction to Graph Theory, second edition, Prentice Hall, 2001
    locator: Section 2.1 (Basic properties of trees), the lemma that a tree with at least two vertices has at least two leaves, and the characterization theorem of trees
---

The tree edge count theorem says that a [tree](/tree/), that is, a [connected](/connected-graph/) [acyclic](/acyclic-graph/) graph, with $n \ge 1$ vertices has exactly $n - 1$ edges. Any two of the three properties "connected", "acyclic" and "$n - 1$ edges" imply the third. The theorem is the reason why tree algorithms run in $O(n)$ time when they look at each edge a constant number of times, and why a [spanning tree](/spanning-tree/) of a connected graph always has $n - 1$ edges.

## Statement

Let $G = (V, E)$ be a finite simple undirected graph with $n = |V| \ge 1$ vertices and $m = |E|$ edges.

1. If $G$ is a tree, then $m = n - 1$.
2. If $G$ is connected and $m = n - 1$, then $G$ is a tree.
3. If $G$ is acyclic and $m = n - 1$, then $G$ is a tree.
4. More generally, if $G$ is acyclic with $c$ connected components, then $m = n - c$.

Nothing in the statement depends on a root or on edge weights. The vertex names do not matter.

## In plain words

Build a tree one edge at a time. Start with all the dots and no lines: each dot is its own group. Each new line must join two different groups, because a line inside one group would close a loop. So each line merges two groups into one. You start with as many groups as dots and you want one group at the end, so you need exactly one line fewer than there are dots. With fewer lines, some dots stay apart. With more lines, some line closes a loop.

## Proof

**Lemma (leaves).** A tree with $n \ge 2$ vertices has at least two vertices of degree 1.

*Proof.* The tree is connected and has at least two vertices, so it has an edge, and so a path with at least one edge. Let $P = v_0, v_1, \ldots, v_k$ be a path with the largest number of edges, $k \ge 1$. Suppose that $v_0$ has a neighbour $w \ne v_1$. If $w = v_i$ for some $i \ge 2$, then $v_0, v_1, \ldots, v_i, v_0$ is a cycle, which a tree does not have. If $w$ is not on $P$, then $w, v_0, \ldots, v_k$ is a path with $k + 1$ edges, against the choice of $P$. So $v_0$ has degree 1. By symmetry $v_k$ has degree 1, and $v_0 \ne v_k$ because $k \ge 1$. $\square$

**Part 1.** By induction on $n$. For $n = 1$, a simple graph on one vertex has no edge, so $m = 0 = n - 1$. Let $n \ge 2$ and assume part 1 for trees with $n - 1$ vertices. By the lemma, $G$ has a leaf $v$ with one edge $e$. The graph $G - v$ has $n - 1$ vertices and $m - 1$ edges. It is acyclic, because it is a subgraph of $G$. It is connected: a path in $G$ between two vertices other than $v$ does not pass through $v$, since an inner vertex of a path has degree at least 2. So $G - v$ is a tree, and by the hypothesis $m - 1 = n - 2$, that is, $m = n - 1$.

**Part 4.** Let the components of the acyclic graph $G$ have $n_1, \ldots, n_c$ vertices and $m_1, \ldots, m_c$ edges. Each component is connected and acyclic, so it is a tree, and part 1 gives $m_i = n_i - 1$. Each edge lies in exactly one component, so $m = \sum_i (n_i - 1) = n - c$.

**Part 3.** If $G$ is acyclic and $m = n - 1$, then part 4 gives $n - c = n - 1$, so $c = 1$ and $G$ is connected.

**Part 2.** Let $G$ be connected with $m = n - 1$. While the graph has a cycle, delete one edge of a cycle. The two ends of the deleted edge stay joined by the rest of the cycle, so each walk that used the edge can go around the cycle, and the graph stays connected. Each deletion lowers the number of edges by 1, so the process stops, with a connected acyclic graph $H$ on the same $n$ vertices. By part 1, $H$ has $n - 1$ edges, which is the number that $G$ had. So no edge was deleted, the first test found no cycle, and $G$ is acyclic. $\blacksquare$

## Consequences

- **Linear size.** A tree with $n$ vertices has $n - 1$ edges, so its [adjacency list](/adjacency-list/) has $2(n - 1)$ entries. A traversal such as [preorder](/preorder-traversal/) or [postorder](/postorder-traversal/) therefore takes $\Theta(n)$ time, and each $O(n + m)$ graph algorithm runs in $O(n)$ time on a tree.
- **Degree sum.** With the [handshake lemma](/handshake-lemma/), the degrees of a tree sum to $2n - 2$. So the average degree is below 2, and, for $n \ge 2$, the number of leaves is $2 + \sum_{v : \deg v \ge 3} (\deg v - 2)$. A star has $n - 1$ leaves, and a path has 2.
- **Spanning trees.** Each [spanning tree](/spanning-tree/) of a connected graph with $n$ vertices has $n - 1$ edges, so [Kruskal's algorithm](/kruskal/) can stop after it accepts $n - 1$ edges, and a [spanning forest](/spanning-forest/) of a graph with $c$ components has $n - c$ edges.
- **Recognition.** A graph with $n$ vertices is a tree if and only if it has $n - 1$ edges and one search from any vertex reaches all $n$ vertices. This test takes $O(n)$ time when the edge count is checked first.
- **Codes and counts.** The [Prüfer code](/pruefer-code/) of a tree on $n \ge 2$ labelled vertices has length $n - 2$, which is the edge count minus one, and it leads to [Cayley's formula](/cayley-formula/).

## Tightness

The hypotheses cannot be dropped.

- **Connected but not acyclic.** The triangle has $n = 3$ and $m = 3 \ne n - 1$. Each connected graph has at least $n - 1$ edges (by part 2, a minimal connected spanning subgraph is a tree), and a cycle adds edges above that.
- **Acyclic but not connected.** Two isolated vertices have $n = 2$ and $m = 0 = n - 2$, as part 4 predicts with $c = 2$.
- **$n - 1$ edges alone.** The triangle plus one isolated vertex has $n = 4$ and $m = 3 = n - 1$, but it is neither connected nor acyclic. So the count alone does not make a tree.
- **$n \ge 1$.** The graph with no vertex is connected and acyclic in a vacuous sense, but it has $0$ edges, not $-1$. The statement needs at least one vertex.
- **Simple graphs.** In a multigraph, two vertices joined by two parallel edges have $m = 2$, and the pair of edges is a cycle of length 2. The theorem is about simple graphs, or about multigraphs where a 2-cycle counts as a cycle.

Small cases match: the single vertex has $0$ edges, the path on $n$ vertices has $n - 1$ edges, and the star with $n - 1$ leaves has $n - 1$ edges.

## History

The fact is part of the classical characterization of trees. Knuth proves it as part of Theorem A of the section on free trees, which lists the equivalent conditions for a finite graph to be a tree. CLRS states it in Theorem B.2, the properties of free trees, and West proves it in the first section of the chapter on trees, from the lemma on leaves.

## References
