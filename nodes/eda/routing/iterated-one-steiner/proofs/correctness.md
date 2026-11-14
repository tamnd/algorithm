---
title: Iterated 1-Steiner never makes the tree longer than the minimum spanning tree, ends, keeps at most n − 2 Steiner points and is exact for three pins
proves: [correctness, termination, fast gain update, steiner point bound, exact for three pins]
status: full
---

Let $P$ be a set of $n$ distinct pins and $d$ the L1 distance. For a finite set $Q$ of points, $\mathrm{MST}(Q)$ is a minimum spanning tree of the complete graph on $Q$ with lengths $d$, and $|\mathrm{MST}(Q)|$ is its length. The value $|\mathrm{MST}(Q)|$ does not depend on which minimum spanning tree is taken. Let $H$ be the Hanan grid of $P$ minus the pins, and let $S \subseteq H$ be the current set of Steiner points.

**Lemma 1 (path bound).** Let $T$ be a minimum spanning tree of a complete graph with lengths $d$, and let $u, v$ be two of its vertices. Every edge on the path of $T$ from $u$ to $v$ has length at most $d(u, v)$.

*Proof.* Suppose an edge $f$ on the path has $d(f) > d(u, v)$. Removing $f$ splits $T$ into two parts, and $u$ and $v$ are in different parts, since $f$ is on the path between them. Then $T - f + uv$ is a spanning tree shorter than $T$, a contradiction. $\square$

**Lemma 2 (fast gain update).** Let $Q$ be a finite set of points, $T$ a minimum spanning tree of $Q$ and $x \notin Q$. Let $G$ be the graph on $Q \cup \{x\}$ with the edges of $T$ and the edges $xq$ for all $q \in Q$. Then a minimum spanning tree of $G$ is a minimum spanning tree of the complete graph on $Q \cup \{x\}$.

*Proof.* Let $T^*$ be a minimum spanning tree of the complete graph on $Q \cup \{x\}$ with the most edges in $G$. Suppose $T^*$ has an edge $uv$ not in $G$. Every edge at $x$ is in $G$, so $u, v \in Q$. Removing $uv$ splits $T^*$ into two parts with $u$ and $v$ in different parts. The path of $T$ from $u$ to $v$ has an edge $f$ that joins the two parts, and $d(f) \le d(u, v)$ by Lemma 1. So $T^* - uv + f$ is a spanning tree no longer than $T^*$, so it is minimum, and it has one more edge in $G$, a contradiction. So $T^*$ lies in $G$. A minimum spanning tree of $G$ is no longer than $T^*$, and no shorter, since it spans the same points. $\square$

So line L4 computes the exact gain $\Delta(x, S)$ from $T$ and the $|P \cup S|$ edges at $x$.

**Lemma 3 (removal is safe).** Let $T$ be a spanning tree of $P \cup S$ and let $D \subseteq S$ be a set of points that each have degree at most 2 in $T$. Then $|\mathrm{MST}(P \cup S \setminus D)| \le |T|$.

*Proof.* Remove the points of $D$ one at a time. Let $s$ be the next point, with degree at most 2 in the current tree. If $s$ has degree 1, remove $s$ and its edge. If $s$ has degree 2 with neighbors $a$ and $b$, remove $s$ and its two edges, and add the edge $ab$. In both cases the result is a spanning tree of the remaining points, and it is no longer, since $d(a, b) \le d(a, s) + d(s, b)$ by the triangle inequality. A point of $D$ that was a neighbor of $s$ loses the edge to $s$ and gains at most one new edge, so its degree does not grow and stays at most 2. At the end we have a spanning tree of $P \cup S \setminus D$ no longer than $T$, and the minimum spanning tree is no longer than that. $\square$

**Theorem 1 (never longer than the MST).** Let $L_r$ be $|\mathrm{MST}(P \cup S)|$ at line L3 of round $r$. Then $L_1 = |\mathrm{MST}(P)|$ and $L_{r + 1} < L_r$ for every round $r$ that does not return. So the output tree $T$ is a rectilinear Steiner tree of $P$ with $|T| \le |\mathrm{MST}(P)|$.

*Proof.* At the start $S = \emptyset$. If round $r$ does not return, line L6 adds a point $x$ with $\Delta(x, S) > 0$, so the length after line L6 is $L_r - \Delta(x, S) < L_r$. Each removal in line L7 does not make the length longer, by Lemma 3. So $L_{r + 1} < L_r$. The output is a spanning tree of $P \cup S$, so it is a Steiner tree of $P$ with the points of $S$ as Steiner points, and its length is the last $L_r$, which is at most $L_1$. $\square$

By Hwang's theorem, $|\mathrm{MST}(P)| \le \frac{3}{2} |\mathrm{RSMT}(P)|$, so the output is within a factor 3/2 of the optimum.

**Theorem 2 (termination).** The algorithm returns after finitely many rounds.

*Proof.* The value $L_r$ depends only on the set $S$ at line L3, and $L_r$ strictly decreases by Theorem 1. So the sets $S$ at line L3 of different rounds are all different. They are subsets of the finite set $H$, so there are at most $2^{|H|}$ rounds. The loop of lines L7 and L8 ends because each pass that does not stop removes a point from the finite set $S$. $\square$

**Lemma 4 (at most $n - 2$ Steiner points).** After line L8, $|S| \le \max(n - 2, 0)$.

*Proof.* After line L8 every point of $S$ has degree at least 3 in $T = \mathrm{MST}(P \cup S)$. Let $k = |S|$. If $k \ge 1$ then $T$ has $n + k \ge 2$ points, so every pin has degree at least 1. The degrees of a tree sum to $2(n + k - 1)$, so $3k + n \le 2(n + k - 1)$, which gives $k \le n - 2$. $\square$

**Theorem 3 (exact for $n \le 3$).** For $n \le 3$ the output is a rectilinear Steiner minimal tree.

*Proof.* For $n \le 2$ every Steiner tree has length at least $d(p, q)$ for the two pins, and the minimum spanning tree has exactly this length. Let $n = 3$, and let $B$ be the half perimeter of the bounding box of $P$, the width plus the height. Every Steiner tree of $P$ has length at least $B$: its edges project onto the $x$ axis with total length at least the width, since the tree connects the leftmost and the rightmost pin, and the same holds for the $y$ axis. Let $m = (x_{\mathrm{med}}, y_{\mathrm{med}})$ be the point with the median $x$ and the median $y$ of the pins, a point of the Hanan grid. For three numbers $a \le b \le c$, $|a - b| + |b - b| + |c - b| = c - a$, so the star from $m$ to the three pins has length exactly $B$. If $m$ is a pin, the star is a spanning tree of $P$, so $|\mathrm{MST}(P)| \le B$ and the output, which is no longer, is optimal. Otherwise $m \in H$ and $|\mathrm{MST}(P \cup \{m\})| \le B$. If $|\mathrm{MST}(P)| = B$ the start is optimal. If not, the gain of $m$ in round 1 is positive, so the point chosen in line L6 has gain at least that of $m$, and the length after round 1 is at most $B$. By Theorem 1 the output is at most this, so it equals $B$. $\square$

**Running time of one round.** By Lemma 4, at line L3 the set $P \cup S$ has fewer than $2n$ points, so the minimum spanning tree of line L3 takes $O(n^2)$ time on all pairs. For each of the at most $n^2$ points $x$, Lemma 2 gives the gain from a graph with fewer than $4n$ edges, and Kruskal's algorithm takes $O(n \log n)$ on it. Each pass of lines L7 and L8 takes $O(n^2)$ and removes a point, so there are $O(n)$ passes, for $O(n^3)$. A round takes $O(n^3 \log n)$ time and $O(n^2)$ space. $\square$
