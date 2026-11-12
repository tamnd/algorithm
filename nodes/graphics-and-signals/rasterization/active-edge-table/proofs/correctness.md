---
title: The active edge table holds the exact sorted crossings of each center line, and its re-sort makes at most one move per pair of intersecting edges
proves: [correctness]
status: full
---

We use the pseudocode of the page and exact arithmetic. Row $j$ has its center line at $y_j = j + 1/2$, and $y$ grows downward. For a non-horizontal edge $e$ with top end point $t_e$ and bottom end point $b_e$, so that $y(t_e) < y(b_e)$, let $x_e(y)$ be the $x$ of the edge line at height $y$, let $\Delta_e = (x(b_e) - x(t_e)) / (y(b_e) - y(t_e))$, and let $d_e$ be $+1$ when the ring runs from $t_e$ to $b_e$ and $-1$ otherwise. Call $e$ *active on row $j$* when $y(t_e) \le y_j < y(b_e)$.

**Lemma 1 (the rows of an edge).** With $j_0 = \max(\lceil y(t_e) - 1/2 \rceil, 0)$ and $j_1 = \lceil y(b_e) - 1/2 \rceil$, the rows $j \ge 0$ on which $e$ is active are exactly $j_0 \le j < j_1$.

*Proof.* For an integer $j$, the condition $y(t_e) \le j + 1/2$ is $j \ge y(t_e) - 1/2$, which holds exactly when $j \ge \lceil y(t_e) - 1/2 \rceil$. The condition $j + 1/2 < y(b_e)$ is $j < y(b_e) - 1/2$, which holds exactly when $j < \lceil y(b_e) - 1/2 \rceil$. Intersect with $j \ge 0$. $\square$

**Invariant.** After the call of NEXT-ROW that returns row $j$, the list $A$ holds each edge that is active on row $j$ exactly once, with no other edge, each record has $x = x_e(y_j)$, and $A$ is sorted by $x$.

*Proof.* By induction on $j$. Lines L1 and L2 put each edge with $j_0 < \min(j_1, H)$ into the bucket of row $j_0$, with $x = x_e(y_{j_0})$, and they put no horizontal edge anywhere. By Lemma 1, the other edges are active on no row $0 \le j < H$.

For $j = 0$, line L3 does nothing, line L4 removes nothing from the empty list, line L5 sorts the empty list, and line L6 makes $A$ equal to bucket 0. This bucket holds the edges with $j_0 = 0$ that are active on row 0, which by Lemma 1 are all edges active on row 0. Line L2 sorted it by $x$.

For $j \ge 1$, assume the invariant for row $j - 1$. Line L3 adds $\Delta_e$ to each record, and $x_e(y_{j-1}) + \Delta_e = x_e(y_j)$ because $y_j - y_{j-1} = 1$ and $x_e$ is linear with slope $\Delta_e$. Line L4 removes the records with $j_1 \le j$. An edge active on row $j - 1$ has $j_0 \le j - 1 < j_1$, so after line L4 the list holds the edges with $j_0 < j < j_1$, which by Lemma 1 are the edges active on row $j$ that were also active on row $j - 1$. Line L5 sorts this list by $x$. Bucket $j$ holds the edges with $j_0 = j$, which are the other edges active on row $j$, sorted by $x$, with their values $x_e(y_j)$. Line L6 merges the two sorted lists into one sorted list. No edge is in both lists, because their values of $j_0$ differ. $\square$

**Corollary (crossings).** CROSSINGS on row $j$ returns the pairs $(x_e(y_j), d_e)$ of the edges active on row $j$, sorted by $x$. These are the points where the polygon meets the center line under the half-open rule: a vertex on the line is counted once for each edge that leaves it downward, so it counts once at a point where the boundary passes through, and 0 or 2 times at a local top or bottom. Horizontal edges give no pair.

**Lemma 2 (each pair moves once).** Over all calls, line L5 makes at most $K$ moves, where $K$ is the number of unordered pairs of edges that intersect.

*Proof.* Insertion sort makes exactly one move for each pair of records $(a, b)$ with $a$ before $b$ in the list and $x_a > x_b$. Fix a pair of edges $a$ and $b$. While both are in $A$, the difference $g(y) = x_a(y) - x_b(y)$ is a linear function of $y$ on the interval of heights where both are active.

Suppose line L5 of row $j$ moves this pair. By the invariant, at row $j - 1$ the list was sorted, so $a$ was before $b$ with $g(y_{j-1}) \le 0$, and now $g(y_j) > 0$. If $g(y_{j-1}) < 0$, then $g$ has a zero strictly between $y_{j-1}$ and $y_j$. If $g(y_{j-1}) = 0$, then $g$ is zero at $y_{j-1}$. In both cases there is a height $y^*$ with $y_{j-1} \le y^* < y_j$ where both edges are active, as both are active on rows $j - 1$ and $j$, and $x_a(y^*) = x_b(y^*)$. So the two segments share a point, and the pair is one of the $K$ intersecting pairs.

After the move, $b$ is before $a$ and $g(y_j) > 0$. Since $g$ is linear and $g(y_{j-1}) \le 0 < g(y_j)$, it is not constant, and $g(y) > 0$ for all $y > y_j$. So the pair is in the right order on every later row while both stay active, and it is never moved again. An edge that leaves $A$ never comes back, by Lemma 1, so the pair has no second chance. Each intersecting pair causes at most one move, and other pairs cause none. $\square$

**Ties at insertion.** Line L6 puts a new edge $e$ after an old edge $f$ with the same $x$ only when $\Delta_f \le \Delta_e$, and line L2 orders a bucket in the same way. Then $x_f(y) \le x_e(y)$ just below the shared point, so the pair is in order on the next row and costs no move there. The invariant and Lemma 2 do not need this order. It only removes the moves of pairs that start at one point, such as the two edges below a top vertex.
