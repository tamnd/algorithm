---
title: The graph of nearest neighbors in the half-open octants contains a rectilinear minimum spanning tree, and the sweep finds those neighbors in O(n log n) time
proves: [correctness, octant lemma, running time]
status: full
---

Let $P$ be a set of $n$ distinct points and $d(p, q) = |x_p - x_q| + |y_p - y_q|$. For a point $p$ and $k \in \{0, \ldots, 7\}$, the octant $O_k(p)$ is the set of points $q \ne p$ whose direction from $p$ has angle in $[45k, 45(k + 1))$ degrees. Every $q \ne p$ is in exactly one octant of $p$. Let $G$ be the graph with an edge from each $p$ to one nearest point of $P$ in each non-empty upper octant $O_0(p), \ldots, O_3(p)$, with any rule for ties.

**Lemma 1 (octant lemma).** Let $q, r \in O_k(p)$ with $q \ne r$ and $d(p, q) \le d(p, r)$. Then $d(q, r) < d(p, r)$.

*Proof.* The swap $(x, y) \mapsto (y, x)$ and the reflections $(x, y) \mapsto (-x, y)$ and $(x, y) \mapsto (x, -y)$ keep L1 distances. These maps and their compositions take each half-open octant onto $[45, 90)$ or onto $(45, 90]$: for example the swap maps $[0, 45)$ onto $(45, 90]$, and the reflection in the $y$ axis maps $[90, 135)$ onto $(45, 90]$. So it suffices to prove the lemma for these two cones. Put $p$ at the origin, $q = (a, b)$ and $r = (c, e)$. In both cones $a, b, c, e \ge 0$, so $d(p, q) = a + b$, $d(p, r) = c + e$, and the hypothesis is $a + b \le c + e$. We split by the signs of $c - a$ and $e - b$. The case $c < a$ and $e < b$ is impossible, since it gives $c + e < a + b$.

Cone $[45, 90)$, where $0 < a \le b$ and $0 < c \le e$:

- $c \ge a$ and $e \ge b$: $d(q, r) = (c + e) - (a + b) < c + e$, since $a + b > 0$.
- $c < a$ and $e \ge b$: $d(q, r) = (a - c) + (e - b) = (e - c) + (a - b) \le e - c < e + c$, using $a \le b$ and $c > 0$.
- $c \ge a$ and $e < b$: $d(q, r) = (c - a) + (b - e)$, and $b - e \le c - a$ by the hypothesis. So $d(q, r) \le 2(c - a) < 2c \le c + e$, using $a > 0$ and $c \le e$.

Cone $(45, 90]$, where $0 \le a < b$ and $0 \le c < e$:

- $c \ge a$ and $e \ge b$: $d(q, r) = (c + e) - (a + b) < c + e$, since $b > 0$.
- $c < a$ and $e \ge b$: $d(q, r) = (e - c) + (a - b) < e - c \le e + c$, using $a < b$ and $c \ge 0$.
- $c \ge a$ and $e < b$: as above $d(q, r) \le 2(c - a) \le 2c < c + e$, using $a \ge 0$ and $c < e$.

In all cases $d(q, r) < d(p, r)$. $\square$

**Lemma 2 (short paths).** For every pair $p, r$ of points, $G$ has a path from $p$ to $r$ whose edges all have length at most $d(p, r)$.

*Proof.* By induction over the pairs in order of increasing $d(p, r)$. Swap the names if needed so that $r$ lies in an upper octant $O_k(p)$. Let $q$ be the neighbor of $p$ chosen in $O_k(p)$, so $pq$ is an edge of $G$ and $d(p, q) \le d(p, r)$. If $q = r$ we are done. Otherwise Lemma 1 gives $d(q, r) < d(p, r)$, so by induction $G$ has a path from $q$ to $r$ with edges at most $d(q, r)$. The edge $pq$ followed by this path joins $p$ to $r$ with all edges at most $d(p, r)$. The induction is well founded because there are finitely many pairs. $\square$

**Theorem 1 (the octant graph contains an RMST).** Every minimum spanning tree of $G$ is a minimum spanning tree of the complete graph on $P$ with L1 lengths.

*Proof.* By Lemma 2, $G$ is connected. Let $T$ be a minimum spanning tree of the complete graph that has the most edges in $G$. Suppose it has an edge $e = pr$ not in $G$. Removing $e$ splits $T$ into two parts, with $p$ in one and $r$ in the other. The path of Lemma 2 from $p$ to $r$ has an edge $f$ that joins the two parts, with length at most $d(p, r)$, and $f$ is in $G$. Then $T - e + f$ is a spanning tree of length at most that of $T$, so it is also minimum, and it has one more edge in $G$. This contradicts the choice of $T$. So $T$ lies in $G$, and a minimum spanning tree of $G$ has length at most that of $T$. It cannot be shorter, since it is also a spanning tree of the complete graph. $\square$

**Lemma 3 (the sweep).** After the map of line L3, the octant is the region $\{q : x_q > x_p,\ y_q - x_q \ge y_p - x_p\}$ or $\{q : x_q \ge x_p,\ y_q - x_q > y_p - x_p\}$ (with $q \ne p$), and in it $d(p, q) = (x_q + y_q) - (x_p + y_p)$. When the sweep handles $p$, the Fenwick tree holds exactly the points with $x_q > x_p$, or with $x_q \ge x_p$ and handled before $p$, according to the octant, and the query returns the point with the least $x + y$ among those with $y - x$ in the right range.

*Proof.* For $q$ in the region, $x_q - x_p \ge 0$ and $(y_q - y_p) \ge (x_q - x_p) \ge 0$, so both differences are non-negative and the L1 distance is their sum. The four maps take the octants $[0, 45)$, $[45, 90)$, $[90, 135)$ and $[135, 180)$ onto these regions, as a check of the inequalities shows. The sweep handles points by decreasing $x$, with ties by decreasing $y$. If the octant needs $x_q > x_p$, a group of points with equal $x$ is inserted after all its queries, so the tree holds the points of larger $x$. Otherwise each point is inserted right after its query, so the tree holds the points of larger $x$ and those of equal $x$ and larger $y$, which with $x_q = x_p$ are exactly the points with $y_q - x_q > y_p - x_p$. The query on ranks at least, or above, the rank of $y_p - x_p$ gives the right range of $y - x$. Among these points the least $x + y$ is the nearest, by the formula for $d$. $\square$

**Running time.** Line L1 takes $O(n \log n)$ with a sort or a hash table. Each of the four sweeps sorts $n$ points and makes $n$ queries and $n$ inserts in a Fenwick tree of size at most $n$, so it takes $O(n \log n)$. The graph has at most $4n$ edges. Kruskal's algorithm sorts them in $O(n \log n)$ and makes $O(n)$ disjoint-set operations. The space is $O(n)$. $\square$
