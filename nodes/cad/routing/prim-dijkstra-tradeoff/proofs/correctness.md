---
title: The Prim-Dijkstra tree is a spanning tree, it is Prim's tree for c = 0 and a shortest path tree for c = 1, and its radius is at most R / c
proves: [correctness, key invariant, prim end, dijkstra end, radius bound]
status: full
---

Let $p_0, \ldots, p_{n-1}$ be points with source $s$, and let $\mathrm{dist}$ be a metric, so it satisfies the triangle inequality. Fix $c \in [0, 1]$. Write $T_k$ for the set of points in the tree after $k$ steps of line L2, so $T_0 = \{s\}$.

**Lemma 1 (spanning tree).** After the loop, the parents form a spanning tree rooted at $s$, and $d(v)$ is the length of the tree path from $s$ to $v$.

*Proof.* Each step adds one point $v \notin T$ with parent $u = \mathrm{best}(v) \in T$, by Lemma 2 below. So the parent edges never close a cycle, and after $n - 1$ steps all $n$ points are in $T$. By induction on the steps, $d(v) = d(u) + \mathrm{dist}(u, v)$ is the tree path length, since $d(u)$ already is. $\square$

**Lemma 2 (key invariant).** After each step, for every $w \notin T$, $\mathrm{key}(w) = \min_{u \in T} \big(c \cdot d(u) + \mathrm{dist}(u, w)\big)$ and $\mathrm{best}(w)$ is a point of $T$ that attains it.

*Proof.* At the start $T = \{s\}$ and $d(s) = 0$, so $\mathrm{key}(w) = \mathrm{dist}(s, w)$ is right. When $v$ joins $T$, the value $d(v)$ is fixed and never changes, and the only new term in the minimum is $c \cdot d(v) + \mathrm{dist}(v, w)$. Line L6 takes the minimum of the old key and this term, and updates $\mathrm{best}(w)$ when the new term is smaller. $\square$

**Theorem 1 (the Prim end).** For $c = 0$ the tree is a minimum spanning tree.

*Proof.* With $c = 0$ the key of $w$ is $\min_{u \in T} \mathrm{dist}(u, w)$, the length of the lightest edge from $T$ to $w$. So each step adds a lightest edge that leaves $T$, which is Prim's rule. By the cut property, every such edge belongs to a minimum spanning tree that contains the edges chosen before, so the final tree is a minimum spanning tree. $\square$

**Theorem 2 (the Dijkstra end).** For $c = 1$, $d(v) = \mathrm{dist}(s, v)$ for every $v$, so the tree is a shortest path tree.

*Proof.* With $c = 1$ the rule is Dijkstra's algorithm on the complete graph with lengths $\mathrm{dist}$, which are not negative, so $d(v)$ is the shortest path distance from $s$ in this graph. The direct edge $sv$ is a path of length $\mathrm{dist}(s, v)$, and every path is at least this long by the triangle inequality, so the shortest path distance is $\mathrm{dist}(s, v)$. $\square$

**Theorem 3 (radius bound).** For every $c \in [0, 1]$ and every point $v$, $c \cdot d(v) \le \mathrm{dist}(s, v)$. So for $c > 0$ the radius is at most $R / c$, where $R = \max_v \mathrm{dist}(s, v)$.

*Proof.* Let $v$ be added with parent $u$. The source is in $T$ when $v$ is added and $d(s) = 0$, so by Lemma 2, $\mathrm{key}(v) \le c \cdot 0 + \mathrm{dist}(s, v)$. Also $\mathrm{key}(v) = c \cdot d(u) + \mathrm{dist}(u, v) \ge c \cdot d(u) + c \cdot \mathrm{dist}(u, v) = c \cdot d(v)$, using $c \le 1$. Together, $c \cdot d(v) \le \mathrm{dist}(s, v) \le R$. For $v = s$ the claim is $0 \le 0$. $\square$

**Lemma 3 (the cost at c = 1 is not bounded).** For $c = 1$ there are inputs where the cost is $\Theta(n)$ times the minimum spanning tree.

*Proof.* Let $k \ge 1$, $s = (0, 0)$ and $q_i = (i, k - i)$ for $i = 0, \ldots, k$, with the L1 metric. Every $q_i$ has $\mathrm{dist}(s, q_i) = k$, and $\mathrm{dist}(q_i, q_j) = 2|i - j|$. In the tree of Theorem 2, $d(q_i) = k$. If the parent of $q_i$ were some $q_j$, then $d(q_i) = k + 2|i - j| > k$, so every parent is $s$, and the cost is $(k + 1) k$. The path $s, q_0, q_1, \ldots, q_k$ is a spanning tree of cost $k + 2k = 3k$. So the ratio is at least $(k + 1)/3$, with $n = k + 2$ points. $\square$

**Running time.** Each of the $n - 1$ steps scans at most $n$ keys in line L3 and updates at most $n$ keys in lines L5 and L6, each in $O(1)$. The total is $\Theta(n^2)$ time and $\Theta(n)$ space. $\square$
