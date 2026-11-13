---
title: Theta* returns a path with line of sight between its corners, no longer than the shortest grid path
proves: [correctness, termination]
status: full
---

We use the pseudocode and the grid model of the page. The vertices are the corners of the cells, two corners *see* each other if the segment between them does not meet the interior of the union of the blocked cells, and the *grid graph* $G$ joins each corner to the 8 corners around it that it sees, with the Euclidean length $|xy|$ of the segment as the cost. Let $d(x)$ be the length of a shortest path in $G$ from $s$ to $x$; this is the length that A* on the grid returns. The heuristic is $h(x) = |x t|$.

**Lemma 1 (line of sight).** LINE-OF-SIGHT$(a, b)$ returns true exactly when $a$ and $b$ see each other, for $a \ne b$.

*Proof.* Let $U$ be the interior of the union of the blocked cells (with the outside of the map blocked). A point in the open interior of a cell is in $U$ exactly when the cell is blocked. A point inside a unit edge is in $U$ exactly when both cells beside the edge are blocked. A corner point is in $U$ exactly when all four cells around it are blocked.

If the segment is on a grid line (line L11), each of its points is inside a unit edge or is a corner, and it meets $U$ exactly when some unit edge on it has blocked cells on both sides (a corner with four blocked cells around it makes the edges next to it on the line have two blocked sides too).

Otherwise the segment is neither horizontal nor vertical. It meets the open interior of a cell $(i, j)$ exactly when, over the strip $i \le x \le i + 1$, its range of $y$ values meets the open interval $(j, j + 1)$; the range is the interval between $n_1 / d_x$ and $n_2 / d_x$, and lines L12 and L13 list exactly the $j$ with $j < \max$ and $j + 1 > \min$, with integer floor and ceiling. If all these cells are free, the segment does not meet $U$ in a cell interior. A point where it crosses an edge between two cells lies between two cells that the segment passes through, which are free, so the point is not in $U$. A corner that it passes through has the two cells that the segment passes through around it, which are free, so it is not in $U$ either. $\square$

**Lemma 2 (parents).** At all times, for each vertex $y$ with a $g$ value, $\mathrm{parent}(y)$ is $y = s$ or a closed vertex, $\mathrm{parent}(y)$ sees $y$, and $g(y) = g(\mathrm{parent}(y)) + |\mathrm{parent}(y)\, y|$. The $g$ value and the parent of a closed vertex never change.

*Proof.* At the start only $s$ has a value, with $\mathrm{parent}(s) = s$ and $g(s) = 0$. An update in line L8 or L9 happens while $x$ is expanded, so $x$ is closed. It sets $\mathrm{parent}(y)$ to $p = \mathrm{parent}(x)$, which is closed by the claim for $x$, or to $x$. In the first case line L7 checked that $p$ sees $y$, in the second case $x$ sees its neighbour $y$ (line L5). In both cases $g(y)$ is set to $g$ of the new parent plus the length. Line L5 skips closed vertices, so closed vertices are never updated, and the $g$ value of a closed parent stays the same. $\square$

**Lemma 3 (the path).** When line L4 returns, the parent chain from $t$ ends at $s$, every two consecutive corners on it see each other, and the sum of the lengths of its segments is $g(t)$.

*Proof.* By Lemma 2, along the chain each $g$ value is the $g$ value of the parent plus a positive length, so the $g$ values go down strictly along the chain and no vertex repeats. There are finitely many vertices, so the chain ends at the only vertex that is its own parent, $s$. The segments see each other by Lemma 2, and adding the equations of Lemma 2 along the chain gives the length $g(t) - g(s) = g(t)$. $\square$

**Lemma 4 (path 2 is never worse than path 1).** When $x$ is expanded and line L5 takes its neighbour $y$, the value that line L8 or L9 compares with $g(y)$ is at most $g(x) + |xy|$.

*Proof.* In line L9 the value is $g(x) + |xy|$. In line L8, with $p = \mathrm{parent}(x)$, the value is $g(p) + |py| \le g(p) + |px| + |xy| = g(x) + |xy|$, by the triangle inequality and Lemma 2. $\square$

**Theorem 5 (no longer than the grid path).** When a vertex $x$ is taken from the open set in line L3, $g(x) \le d(x)$.

*Proof.* By induction on the order in which vertices are taken. For $x = s$, $g(s) = 0 = d(s)$. Let $x \ne s$ be taken, with $d(x)$ finite, and fix a shortest path of $G$ from $s$ to $x$. Its first vertex $s$ is closed. Let $v$ be the first vertex on it that is not closed, and let $u$ be the vertex before $v$; $u$ is closed, so $g(u) \le d(u)$ by induction. When $u$ was expanded, $v$ was not closed, and $u$ sees $v$, so line L5 took $v$, and by Lemma 4, after that step $g(v) \le g(u) + |uv| \le d(u) + |uv| = d(v)$. Values only go down, so this still holds, and $v$ is in the open set. The heuristic satisfies $h(v) = |vt| \le |vx| + |xt| \le (d(x) - d(v)) + h(x)$, because a path of $G$ from $v$ to $x$ is at least as long as the segment $vx$. So
$$ g(v) + h(v) \le d(v) + d(x) - d(v) + h(x) = d(x) + h(x) . $$
Line L3 takes a vertex with the least $g + h$ (the heap holds old entries too, but an old entry of a vertex has a larger key than its current one, and the first entry of $x$ that is taken has its current key). So $g(x) + h(x) \le g(v) + h(v) \le d(x) + h(x)$. If $v = x$ the same bound holds directly. $\square$

**Theorem 6 (termination and completeness).** Theta* stops. If $t$ can be reached from $s$ in $G$, it returns a path as in Lemma 3 whose length is at most $d(t)$, and at least the length of a shortest path from $s$ to $t$ in the plane that avoids the obstacle. If not, it returns no path.

*Proof.* Each vertex is closed at most once, and each expansion pushes at most 8 entries, so the loop runs finitely often. Line L5 gives values only to neighbours in $G$ of closed vertices, so by induction only vertices that can be reached in $G$ from $s$ ever get values. If $t$ is not reachable, it never gets a value and line L10 returns no path.

If $t$ is reachable, assume that the loop ends without taking $t$. Take a path of $G$ from $s$ to $t$ and its first vertex $v$ that is never closed, with the vertex $u$ before it closed. When $u$ was expanded, $v$ got a value and an entry in the heap, so it would have been taken later, a contradiction. So line L4 returns, and the length is $g(t) \le d(t)$ by Theorem 5. The returned path is a path in the plane that avoids the interior of the obstacle (Lemma 1 and Lemma 3), so it is no shorter than a shortest such path. $\square$

**What is not proved.** The returned length is not always the shortest length in the plane. The example of the page has a Theta* path of length $\sqrt{17} + \sqrt 2 \approx 5.537$, while the shortest path in the plane, through the corner $(3, 1)$, has length $\sqrt{10} + \sqrt 5 \approx 5.398$. Theta* only takes the parent of a neighbour as a shortcut, so the corners of its path are limited by the order of the expansions.
