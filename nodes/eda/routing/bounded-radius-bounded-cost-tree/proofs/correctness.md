---
title: The BRBC tree has radius at most (1 + ε) R and cost at most (1 + 2/ε) times the minimum spanning tree
proves: [correctness, radius bound, cost bound]
status: full
---

Let the points have source $s$ and a metric $\mathrm{dist}$. Let $M$ be the minimum spanning tree of line L1 with cost $\mathrm{MST}$, let $R = \max_v \mathrm{dist}(s, v)$, and fix $\varepsilon > 0$. The depth-first tour of $M$ from $s$ is the sequence of points $t_0 = s, t_1, \ldots, t_{2n-2} = s$ in which each step goes along a tree edge, down to a child or back up to the parent. Each tree edge is used twice, so the tour has length $2 \cdot \mathrm{MST}$, and every point appears in it. Let $Q$ be the graph at line L8, and let $d(v)$ be the distance from $s$ to $v$ in $Q$, which is the path length in the shortest path tree of line L8.

**Lemma 1 (spanning tree).** The output is a spanning tree of all points rooted at $s$, and its path lengths are $d(v)$.

*Proof.* $Q$ contains $M$, so it is connected. Dijkstra's algorithm from $s$ on the connected graph $Q$ with lengths that are not negative gives a shortest path tree that spans all points, with path lengths $d(v)$. $\square$

**Lemma 2 (reset points).** Call $t_i$ a *reset point* if line L7 runs after the step to $t_i$, and also call $t_0 = s$ a reset point. Every reset point $w$ has $d(w) \le \mathrm{dist}(s, w) \le R$.

*Proof.* If $w = s$, then $d(w) = 0$. Otherwise line L6 makes sure that $Q$ has the edge $sw$, either added now or before, so $d(w) \le \mathrm{dist}(s, w)$. $\square$

**Lemma 3 (tour segments).** If $t_i$ and $t_j$ with $i < j$ are points of the tour, then the distance between them in $M$ is at most the length of the tour from $t_i$ to $t_j$.

*Proof.* The tour from $t_i$ to $t_j$ is a walk in $M$ between these points, and the tree path is the shortest walk in a tree, since every walk between two vertices of a tree uses each edge of the path between them. $\square$

**Theorem 1 (radius).** For every point $v$, $d(v) \le (1 + \varepsilon) R$.

*Proof.* Let $t_j = v$ be the first time the tour reaches $v$, and let $t_i$, $i \le j$, be the last reset point at or before position $j$. If $i = j$, Lemma 2 gives $d(v) \le R$. Otherwise no reset happened after the steps to $t_{i+1}, \ldots, t_j$, so after each of these steps the run was at most $\varepsilon R$. The run after the step to $t_j$ is the length of the tour from $t_i$ to $t_j$, so this length is at most $\varepsilon R$. By Lemma 3 and since $M \subseteq Q$, $d(v) \le d(t_i) + \varepsilon R \le R + \varepsilon R$, using Lemma 2. $\square$

**Theorem 2 (cost).** The output costs at most $(1 + 2/\varepsilon) \cdot \mathrm{MST}$.

*Proof.* Let the reset points other than $t_0$ be $t_{i_1}, \ldots, t_{i_k}$ in tour order, and set $i_0 = 0$. The run is reset after each, so the tour from $t_{i_{m-1}}$ to $t_{i_m}$ has length more than $\varepsilon R$, by the test of line L5. These $k$ parts of the tour do not overlap, so $k \varepsilon R < 2 \cdot \mathrm{MST}$ when $k \ge 1$, and $k \le 2 \cdot \mathrm{MST} / (\varepsilon R)$ in all cases. Each shortcut is added at a reset point, at most one per reset, and has length $\mathrm{dist}(s, w) \le R$. So the total length of $Q$ is at most $\mathrm{MST} + k R \le \mathrm{MST} + 2 \cdot \mathrm{MST} / \varepsilon$. The output tree is a subgraph of $Q$, so it costs no more. If $R = 0$, all points coincide with $s$, every cost is 0, and the bound holds. $\square$

**Running time.** Line L1 takes $\Theta(n^2)$ with Prim's algorithm on all pairs. The tour has $2(n - 1)$ steps, each $O(1)$ with a stack. $Q$ has at most $(n - 1) + (n - 1)$ edges, so Dijkstra's algorithm with a binary heap takes $O(n \log n)$. The total is $\Theta(n^2)$ time and $\Theta(n)$ space. $\square$
