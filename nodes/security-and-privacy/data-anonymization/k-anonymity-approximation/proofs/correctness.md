---
title: The forest algorithm is k-anonymous and within 3k - 3 of the fewest suppressions
proves: [correctness]
status: full
---

The input is $n$ rows of $d$ values each, and $2 \le k \le n$. For rows $x$ and $y$, $w(x, y)$ is the number of columns where they differ. For a set $C$ of rows, $\delta(C)$ is the number of columns where not all rows of $C$ are equal. The algorithm releases each row of a cluster $C$ with its cells in these $\delta(C)$ columns suppressed, so its cost is $\sum_C |C| \, \delta(C)$.

**Lemma 1 (the optimum).** Let OPT be the fewest suppressed cells in a k-anonymous release of the rows. Then OPT $= \min \sum_C |C| \, \delta(C)$, over all partitions of the rows into clusters of at least $k$ rows.

*Proof.* Take an optimal release, and group the rows by their released row. Each group has at least $k$ rows. The rows of a group are equal after suppression, so in each column where the group differs, each of its rows has a suppressed cell. So the cost is at least $\sum_C |C| \, \delta(C)$ for this partition. Conversely, suppressing the differing columns of each cluster of a partition gives a k-anonymous release with this cost. $\square$

For a row $u$, let $d_{k-1}(u)$ be the $(k - 1)$-th smallest value of $w(u, y)$ over the other rows $y$.

**Lemma 2 (the forest).** Lines L1 to L6 stop with a forest $F$ on the rows, each tree of $F$ has at least $k$ vertices, and the total weight $W(F)$ is at most OPT.

*Proof.* Each step of line L6 adds an edge between two different trees, so $F$ stays a forest, and the number of trees goes down by one. So the loop stops, and then no tree has fewer than $k$ vertices. A tree has exactly one root, the vertex with no outgoing edge. Line L6 adds an edge from the root $u$ of the small tree, and the root of the merged tree is the root of the tree of $x$. So $u$ is never a root again, and each vertex is the start of at most one edge.

When line L6 adds the edge $(u, x)$, the tree $T$ of $u$ has at most $k - 1$ vertices. At most $k - 2$ of the $k - 1$ rows nearest to $u$ are in $T$, so one of them is outside $T$, and line L5 gives $w(u, x) \le d_{k-1}(u)$.

In an optimal partition (Lemma 1), the cluster $C$ of $u$ has at least $k - 1$ other rows, and $\delta(C) \ge w(u, y)$ for each $y \in C$. So $\delta(C)$ is at least the largest of these $k - 1$ or more distances, which is at least $d_{k-1}(u)$. Each vertex starts at most one edge, so $W(F) \le \sum_u d_{k-1}(u) \le \sum_u \delta(C_u) = $ OPT, where $C_u$ is the cluster of $u$. $\square$

In the next part, a tree may also have *Steiner* vertices. A Steiner vertex is a copy of the vector of some vertex, and it is not a row. The *size* of a tree is its number of row vertices.

**Lemma 3 (one split).** Let a tree have size $s \ge 3k - 2$. DECOMPOSE returns two trees of size at least $k$ each, whose row vertices are a partition of the row vertices of the tree, and whose total weight is at most the weight of the tree.

*Proof.* For a vertex $u$ and a neighbor $y$, let side$(y)$ be the size of the part that holds $y$ when the edge $u$-$y$ is cut. Root the tree at the start vertex $r$ of line L12. Lines L13 and L14 move $u$ to the neighbor $c$ with the largest side while that side is more than $s - k$. If the walk moves from $u$ to $c$, then the part of $c$ that holds $u$ has size $s - \mathrm{side}(c) < k \le s - k$, because $s \ge 2k$. So the walk never moves back, it goes down in the tree rooted at $r$, and it stops. A move needs a side of at least $s - k + 1 \ge 2$, so the walk never reaches a leaf, and $u$ always has a neighbor. When the walk stops, each neighbor of $u$ has side at most $s - k$.

If the largest side $\varphi$ is at least $k$ (line L15), cutting the edge $u$-$c$ gives a tree of size $\varphi$ and a tree of size $s - \varphi$, and both are at least $k$.

Otherwise each side is at most $k - 1$. The sides add up to $s$ or $s - 1$, which is at least $3k - 3 \ge k$, so line L16 can take sides until their total is at least $k$. The total before the last one is at most $k - 1$, so the final total is at most $2k - 2$. The rest, with $u$, has size at least $s - (2k - 2) \ge k$. Line L17 joins the taken parts to a Steiner copy of $u$ and not to $u$. Each new edge has the weight of the edge it replaces, because the copy has the vector of $u$. Both new trees are connected, and both have size at least $k$.

In both cases no edge gets a larger weight, and one edge goes away in the first case. $\square$

**Lemma 4 (a cluster and its tree).** If the rows of a cluster $C$ are the row vertices of a tree $T_C$, possibly with Steiner vertices, then $\delta(C) \le W(T_C)$.

*Proof.* Take a column $j$ where two rows $x, y \in C$ differ. The path from $x$ to $y$ in $T_C$ has an edge whose two ends differ in column $j$. Map $j$ to this edge. Different columns give different pairs (edge, column), and an edge $e$ is in at most $w(e)$ such pairs. So $\delta(C) \le \sum_e w(e) = W(T_C)$. $\square$

**Theorem.** ANONYMIZE returns clusters that partition the rows, each with between $k$ and $3k - 3$ rows. The released table is k-anonymous, and its cost is at most $(3k - 3)\,$OPT.

*Proof.* By Lemma 2, line L7 starts with trees of size at least $k$. Line L8 splits a tree only when its size is more than $3k - 3$, and by Lemma 3 both parts have size at least $k$, so both are smaller than the tree. So the loop stops, and each final tree has a size between $k$ and $3k - 3$. Note that $k \le 3k - 3$ because $k \ge 2$. The row vertices of the final trees are a partition of the rows.

Line L10 suppresses, in each row of a cluster $C$, the $\delta(C)$ columns where $C$ differs. Then all rows of $C$ are equal, and $C$ has at least $k$ rows, so the table is k-anonymous. By Lemma 4, Lemma 3 and Lemma 2, the cost is
$$\sum_C |C| \, \delta(C) \le (3k - 3) \sum_C W(T_C) \le (3k - 3)\, W(F) \le (3k - 3)\,\mathrm{OPT}. \qquad \blacksquare$$
