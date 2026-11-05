---
title: The Kou-Markowsky-Berman algorithm returns a Steiner tree of weight at most 2(1 - 1/l) times the optimum
proves: [correctness, termination]
status: full
---

Let $G = (V, E)$ be a finite undirected graph with a weight $w(e) \ge 0$ on each edge, and let $S \subseteq V$ be the set of terminals, with $s = |S| \ge 2$. Parallel edges and self-loops are allowed, and weights may tie. A *Steiner tree* for $S$ is a tree in $G$ that contains every vertex of $S$. Let $\mathrm{OPT}$ be the least weight of a Steiner tree; it exists if and only if all terminals lie in one component of $G$. For $u, v \in V$, let $d(u, v)$ be the shortest path distance in $G$. For $s \le 1$ the algorithm returns the empty tree, which is optimal, so assume $s \ge 2$.

The algorithm (lines L1 to L6 of the page) computes:

- L1 and L2: the distance graph $G_1$, the complete graph on $S$ with weight $d(a, b)$ on the edge $ab$;
- L3: a minimum spanning tree $T_1$ of $G_1$;
- L4: the subgraph $G_S$ of $G$ formed by one shortest path $P_{ab}$ for each edge $ab$ of $T_1$;
- L5: a minimum spanning tree $T_2$ of $G_S$;
- L6: the tree $T_H$ obtained from $T_2$ by deleting, again and again, a leaf that is not a terminal.

## Part 1: the output is a Steiner tree

If two terminals lie in different components, some distance $d(a, b)$ is infinite, and the algorithm returns NONE, which is correct, since no Steiner tree exists. Otherwise all distances are finite.

**Lemma 1.** $G_S$ is connected and contains every terminal.

*Proof.* $T_1$ is a spanning tree of the complete graph $G_1$, so it is connected and contains all of $S$. Each edge $ab$ of $T_1$ is replaced by a path $P_{ab}$ of $G$ from $a$ to $b$. A path is connected, and two paths for edges of $T_1$ that share a terminal share a vertex, so the union of the paths is connected, as $T_1$ is. $\square$

So $T_2$, a minimum spanning tree of the connected graph $G_S$, is a tree that contains every terminal.

**Lemma 2.** Line L6 stops, and $T_H$ is a tree that contains every terminal, in which every leaf is a terminal.

*Proof.* Each deletion removes a leaf vertex and its one edge from a tree, which leaves a tree, and does not remove a terminal. Each deletion removes an edge, so there are at most $|T_2|$ of them. When the loop stops, no leaf is a non-terminal. $\square$

## Part 2: the weight bound

**Lemma 3.** $w(T_H) \le w(T_2) \le w(G_S) \le w(T_1)$.

*Proof.* The first inequality holds because the weights are non-negative and $T_H \subseteq T_2$. The second because $T_2 \subseteq G_S$. For the third, each edge of $G_S$ lies on some path $P_{ab}$, so $w(G_S) \le \sum_{ab \in T_1} w(P_{ab}) = \sum_{ab \in T_1} d(a, b) = w(T_1)$. $\square$

**Lemma 4.** Let $T^*$ be an optimal Steiner tree with $l$ leaves. Then $w(T_1) \le 2 (1 - 1/l)\, \mathrm{OPT}$.

*Proof.* First, we may assume that every leaf of $T^*$ is a terminal: deleting a non-terminal leaf does not raise the weight, so it keeps $T^*$ optimal, and it does not raise the number of leaves (the parent of the deleted leaf may become a leaf in its place), which can only lower the bound $2(1 - 1/l)$. Since $T^*$ contains at least two terminals, it has at least one edge and $l \ge 2$ leaves.

Root $T^*$ at a leaf $r_0$ and walk around it in depth-first order, so that each edge is used twice, once down and once up. This closed walk $W$ has length $2\, w(T^*)$ and meets the leaves in a cyclic order $r_0 = x_1, x_2, \ldots, x_l$. Cut $W$ at the leaves into $l$ segments, from $x_j$ to $x_{j+1}$, and from $x_l$ back to $x_1$.

*Each edge lies in two different segments.* For an edge from a vertex $p$ to its child $c$, the walk goes down the edge just before it reaches the first leaf $f$ below $c$, and goes up the edge just after it leaves the last leaf $g$ below $c$. The down step lies in the segment that ends at $f$, and the up step in the segment that starts at $g$. These are the same segment only if that segment runs from $g$ to $f$, which would be the closing segment from $x_l$ to $x_1 = r_0$ with $f = r_0$. But $r_0$ is not below $c$. So the two steps lie in different segments.

The segments have total length $2\, w(T^*)$, so the longest one has length at least $2\, w(T^*)/l$. Delete it. What is left is one walk $W'$, the remaining segments in cyclic order, of length at most $2 (1 - 1/l)\, w(T^*)$. By the claim above, every edge of $T^*$ still lies on $W'$, so $W'$ passes through every vertex of $T^*$, and in particular through every terminal.

List the terminals in the order in which $W'$ first meets them: $t_1, t_2, \ldots, t_s$. The part of $W'$ between $t_i$ and $t_{i+1}$ is a walk in $G$ from $t_i$ to $t_{i+1}$, so its length is at least $d(t_i, t_{i+1})$, and these parts do not overlap. So the path $t_1 t_2 \cdots t_s$ in $G_1$ has weight at most the length of $W'$. It is a spanning tree of $G_1$, and $T_1$ is a minimum one, so

$$w(T_1) \le \sum_{i=1}^{s-1} d(t_i, t_{i+1}) \le |W'| \le 2 \left(1 - \frac{1}{l}\right) w(T^*) = 2 \left(1 - \frac{1}{l}\right) \mathrm{OPT}. \qquad \square$$

## The theorem

**Theorem.** For non-negative weights and $s \ge 2$ terminals in one component, the algorithm stops and returns a Steiner tree $T_H$ for $S$ whose leaves are all terminals and whose weight satisfies

$$w(T_H) \le 2 \left(1 - \frac{1}{l}\right) \mathrm{OPT} \le 2 \left(1 - \frac{1}{s}\right) \mathrm{OPT},$$

where $l$ is the number of leaves of any optimal Steiner tree. If the terminals lie in different components, it returns NONE.

*Proof.* Lemmas 1 and 2 give the tree, Lemmas 3 and 4 the first inequality. For the second, an optimal tree with all leaves terminals has $l \le s$. $\blacksquare$

**Ties.** Nothing above uses distinct weights or a particular choice of shortest paths or minimum spanning trees, so every tie rule gives the same guarantee. Zero weights are allowed; negative weights are not, because Lemma 3 and the shortest paths need $w \ge 0$.
