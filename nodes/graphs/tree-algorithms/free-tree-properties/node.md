---
tag: X0X301
kind: theorem
slug: free-tree-properties
name: Properties of free trees
aliases:
- characterizations of trees
- equivalent definitions of a tree
area: graphs/tree-algorithms
level: intro
summary: Equivalent characterizations of a free tree, such as connected and acyclic, connected with n minus one edges, or a unique path between any two vertices.
prereqs: [tree, connected-graph, acyclic-graph, simple-path]
see_also: [rooted-tree, spanning-tree, spanning-forest, fundamental-cycle, cayley-formula, tree-edge-count, handshaking-lemma, arborescence]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Appendix B.5.1 (Free trees), Theorem B.2 (Properties of free trees) with its proof
  - book: isbn:9780201896831
    title: Donald E. Knuth, The Art of Computer Programming, Volume 1, third edition
    locator: Section 2.3.4.1 (Free trees), Theorem A
  - book: isbn:9783662536216
    title: Reinhard Diestel, Graph Theory, fifth edition, Springer, 2017
    locator: Section 1.5 (Trees and forests), Theorem 1.5.1 and Corollary 1.5.3
---

A free tree is an undirected graph that is [connected](/connected-graph/) and has no cycle. This theorem says that six conditions on a finite undirected graph are equivalent: connected and acyclic; a unique simple path between any two vertices; connected but disconnected by the removal of any edge; connected with $n - 1$ edges; acyclic with $n - 1$ edges; acyclic but given a cycle by the addition of any edge. Each of them can serve as the definition of a [tree](/tree/), and algorithms use whichever one is easiest to check or to apply. The counting forms, with $n - 1$ edges, give a linear-time test for a tree and the edge count of every [spanning tree](/spanning-tree/).

## Statement

Let $G = (V, E)$ be a finite simple undirected graph with $n = |V| \ge 1$ vertices and $m = |E|$ edges. A *cycle* is a closed path with at least three distinct vertices, and a *simple path* is a path with no repeated vertex. $G$ is a *free tree* if it is connected and acyclic.

**Theorem** (CLRS Theorem B.2; Knuth, Section 2.3.4.1, Theorem A; Diestel, Theorem 1.5.1 and Corollary 1.5.3). The following statements are equivalent.

1. $G$ is connected and acyclic.
2. Any two vertices of $G$ are joined by a unique simple path.
3. $G$ is connected, and for every edge $e$ the graph $G - e$ is disconnected (*minimally connected*).
4. $G$ is connected, and $m = n - 1$.
5. $G$ is acyclic, and $m = n - 1$.
6. $G$ is acyclic, and for any two non-adjacent vertices $u, v$ the graph $G + uv$ has a cycle (*maximally acyclic*).

## In plain words

A tree is a network of points and lines with no loop, in which you can get from any point to any other point. The theorem says that there are several other ways to say the same thing. Between any two points there is exactly one route that does not repeat a point. Every line is needed: take any one away and the network falls into two parts. The network has exactly one line fewer than it has points. Any new line closes a loop. Each of these facts alone, with the side condition that goes with it, is enough to know that the network is a tree.

## Proof

The proof uses one lemma about adding edges.

**Lemma 1.** Let $H$ be a graph and $u, v$ two non-adjacent vertices of $H$. If $u$ and $v$ are in different components of $H$, then $H + uv$ has one component fewer than $H$, and the edge $uv$ lies on no cycle of $H + uv$. If $u$ and $v$ are in the same component, then $H + uv$ has as many components as $H$, and $uv$ lies on a cycle of $H + uv$.

*Proof.* Only the components of $u$ and $v$ can change, and in $H + uv$ they become one, so the count drops by one if they were different and stays the same if not. If $uv$ were on a cycle of $H + uv$, the rest of the cycle would be a $u$-$v$ path in $H$, so $u$ and $v$ would be in the same component. If they are in the same component, a shortest $u$-$v$ path in $H$ has at least two edges, because $u$ and $v$ are not adjacent, and with $uv$ it forms a cycle. $\square$

**Lemma 2.** Let $G$ have $n$ vertices, $m$ edges and $c$ components. Then $c \ge n - m$, and $c = n - m$ if and only if $G$ is acyclic.

*Proof.* Build $G$ from the graph with the same $n$ vertices and no edges, which has $n$ components, by adding the edges $e_1, \ldots, e_m$ one at a time. By Lemma 1 each step lowers the number of components by 1 or by 0, so $c \ge n - m$, with equality if and only if every edge $e_j$ joins two different components of the graph before step $j$.

If some $e_j$ joins two vertices of one component, Lemma 1 gives a cycle through $e_j$ at step $j$, and the cycle is still in $G$. So equality implies that $G$ is acyclic. Conversely, if every $e_j$ joins two components, suppose $G$ has a cycle $C$, and let $e_j$ be the edge of $C$ added last. At step $j$, the other edges of $C$ are present and form a path between the ends of $e_j$, so the ends were in one component, a contradiction. So $G$ is acyclic exactly when equality holds. $\square$

Now the theorem.

**1 ⇔ 4 ⇔ 5.** If $G$ is connected and acyclic, then $c = 1$ and Lemma 2 gives $1 = n - m$, so $m = n - 1$; this gives 4 and 5. If 4 holds, then $c = 1 = n - m$, so by Lemma 2 $G$ is acyclic, which gives 1. If 5 holds, Lemma 2 gives $c = n - m = 1$, so $G$ is connected, which gives 1.

**1 ⇒ 2.** Connectivity gives a path, and a shortest path is simple. Suppose $P = p_0 p_1 \cdots p_k$ and $Q = q_0 q_1 \cdots q_l$ are two different simple paths from $u = p_0 = q_0$ to $v = p_k = q_l$. Neither is a proper prefix of the other, because then $v$ would appear twice on the longer one. So there is a least $i$ with $p_{i+1} \ne q_{i+1}$, and $p_s = q_s$ for $s \le i$. Let $j > i$ be the least index such that $p_j$ lies on $Q$; it exists because $p_k = v$ is on $Q$. Write $p_j = q_t$. Then $t > i$, because $p_j \ne p_s = q_s$ for $s \le i$ by the simplicity of $P$. The walk $p_i, p_{i+1}, \ldots, p_j = q_t, q_{t-1}, \ldots, q_i = p_i$ repeats no vertex except its ends: the vertices $p_{i+1}, \ldots, p_{j-1}$ are off $Q$ by the choice of $j$, and the two pieces are simple. It has $(j - i) + (t - i) \ge 2$ edges, and if it had exactly 2 then $j = t = i + 1$ and $p_{i+1} = q_{i+1}$, against the choice of $i$. So it is a cycle with at least three vertices, which contradicts 1.

**2 ⇒ 3.** The paths of 2 make $G$ connected. Let $e = uv$ be an edge. The path $u, v$ is a simple path, so by 2 it is the only simple $u$-$v$ path in $G$. A $u$-$v$ path in $G - e$ would contain a simple $u$-$v$ path that avoids $e$, a second one in $G$. So $u$ and $v$ are in different components of $G - e$.

**3 ⇒ 1.** Suppose $G$ has a cycle, and let $e = uv$ be one of its edges. The rest of the cycle is a $u$-$v$ path in $G - e$, so any walk in $G$ that uses $e$ can use that path instead, and $G - e$ is still connected. That contradicts 3. So $G$ is acyclic, and it is connected by 3.

**1 ⇒ 6.** $G$ is acyclic. If $u$ and $v$ are not adjacent, they are in the same component, since $G$ is connected, so by Lemma 1 the graph $G + uv$ has a cycle.

**6 ⇒ 1.** $G$ is acyclic. If $G$ were not connected, take $u$ and $v$ in different components; they are not adjacent, and by Lemma 1 the edge $uv$ lies on no cycle of $G + uv$, and $G$ itself has none, so $G + uv$ is acyclic, against 6. So $G$ is connected.

The implications $1 \Rightarrow 2 \Rightarrow 3 \Rightarrow 1$, $1 \Leftrightarrow 4 \Leftrightarrow 5$ and $1 \Leftrightarrow 6$ prove that all six statements are equivalent. $\blacksquare$

## Consequences

- **Edge count of forests.** By Lemma 2, an acyclic graph with $n$ vertices and $c$ components, a [spanning forest](/spanning-forest/), has exactly $n - c$ edges. A connected graph has at least $n - 1$ edges.
- **A linear-time test.** To decide whether a graph given by adjacency lists is a tree, check $m = n - 1$ and then run one [breadth-first search](/breadth-first-search/) to check that it reaches all $n$ vertices. This is statement 4, and it takes $O(n)$ time, since the check of $m$ comes first and rejects dense inputs at once.
- **Leaves.** A tree with $n \ge 2$ vertices has at least two leaves. By the [handshaking lemma](/handshaking-lemma/) the degrees sum to $2m = 2n - 2$, and each degree is at least 1 because the tree is connected; if at most one vertex had degree 1, the sum would be at least $1 + 2(n - 1) > 2n - 2$. Deleting a leaf leaves a tree with $n - 1$ vertices, which is the base of many inductive proofs on trees.
- **Spanning trees.** Every connected graph has a spanning tree: delete edges that lie on cycles until none is left; statement 3 says when to stop. Each spanning tree has exactly $n - 1$ edges, which is why the greedy algorithms for the [minimum spanning tree](/minimum-spanning-tree/) stop after $n - 1$ edges.
- **Fundamental cycles.** By statement 6 and statement 2, adding a non-tree edge $uv$ to a spanning tree creates exactly one cycle, the [fundamental cycle](/fundamental-cycle/) made of $uv$ and the tree path from $u$ to $v$. A connected graph has $m - n + 1$ of them, one per non-tree edge.
- **Rooting.** By statement 2, choosing any vertex $r$ gives each other vertex $v$ a unique path to $r$, and so a unique parent: the next vertex on that path. This is how a free tree becomes a [rooted tree](/rooted-tree/) and, with directions, an [arborescence](/arborescence/).

## Tightness

None of the two-part conditions can drop a part. The examples use the vertices $0, \ldots, n-1$:

| graph | $n$ | $m$ | connected | acyclic | tree |
|---|---|---|---|---|---|
| one vertex | 1 | 0 | yes | yes | yes |
| path $0 - 1 - \cdots - (n-1)$ | $n$ | $n - 1$ | yes | yes | yes |
| star with center 0 | $n$ | $n - 1$ | yes | yes | yes |
| cycle $C_n$, $n \ge 3$ | $n$ | $n$ | yes | no | no |
| triangle on $\{0, 1, 2\}$ and the isolated vertex 3 | 4 | 3 | no | no | no |
| the edges $01$ and $23$ | 4 | 2 | no | yes | no |

- **Count alone.** The triangle with an isolated vertex has $m = n - 1$ but is neither connected nor acyclic, so the count needs one of the other two conditions.
- **Connected alone.** The cycle $C_n$ is connected with $m = n$. Removing any one edge of it leaves a path, which is a tree; this is statement 3 failing and then holding.
- **Acyclic alone.** Two disjoint edges are acyclic with $m = n - 2$; adding the edge $12$ keeps the graph acyclic, so statement 6 fails.
- **Infinite graphs.** Statements 1, 2, 3 and 6 stay equivalent for infinite graphs (Diestel, Theorem 1.5.1), but the counting statements 4 and 5 make sense only for finite ones.
- **Multigraphs.** With parallel edges, two edges between $u$ and $v$ form a cycle of length 2. With that convention the theorem holds for multigraphs; with the convention of this page, which requires three vertices on a cycle, the graph must be simple.

## History

Kirchhoff used spanning trees in 1847 to solve the equations of electrical networks, and Cayley named trees in 1857 and later counted them, which led to [Cayley's formula](/cayley-formula/). Jordan studied the centers of trees in 1869. The list of equivalent conditions is a standard part of textbooks, such as Knuth's Section 2.3.4.1 and Theorem B.2 of CLRS.

## References
