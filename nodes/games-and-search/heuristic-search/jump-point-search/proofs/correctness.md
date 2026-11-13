---
title: Jump point search without corner cutting returns an optimal path
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page and its grid model. The grid is finite and 8-connected. A straight move costs $1$ and a diagonal move costs $\sqrt 2$. A diagonal move from $x$ by $(d_x, d_y)$ is allowed only if the target and both cells $x + (d_x, 0)$ and $x + (0, d_y)$ are free (no corner cutting). Let $C^*$ be the cost of a shortest grid path from $s$ to $t$.

We say that a pair of consecutive moves $(m, m')$ at a cell $x$ is *allowed* if $m'$ is in PRUNED$(x, m)$, that is:

- $m$ is diagonal and $m'$ is $m$ or one of its two straight parts; or
- $m$ is straight and $m' = m$; or
- $m$ is straight and $m'$ is a forced move of $(x, m)$: for a perpendicular unit vector $q$, the cell $x - m + q$ is blocked, $x + q$ is free, and $m'$ is $q$ or $m + q$.

A grid path is *allowed* if every pair of consecutive moves on it is allowed. Any first move is allowed (line L10).

**Lemma 1 (the pairs on a shortest path).** Let $p \to x \to z$ be two consecutive moves $m, m'$ of a shortest path. Then $(m, m')$ is allowed, or $m$ is straight, $m' = m + q$ for a perpendicular $q$, and the cell $p + q$ is free.

*Proof.* We go through the cases up to symmetry, with the coordinates of $p$ as origin.

- $m'$ is the reverse of $m$: the path goes back to $p$, and a shortest path with positive costs does not visit a cell twice.
- A turn of 135 degrees. If $m = (1, 0)$ and $m' = (-1, 1)$, then $x = (1, 0)$ and $z = (0, 1)$. The cell $z$ is free, so the straight move $p \to z$ is allowed, and it costs $1 < 1 + \sqrt 2$. If $m = (1, 1)$ and $m' = (0, -1)$ or $(-1, 0)$, then $z = (1, 0)$ or $(0, 1)$. Both cells are free because the diagonal move $p \to x$ needs them, so one straight move of cost $1 < \sqrt 2 + 1$ reaches $z$. The other cases are mirror images. So the path is not shortest.
- A turn of 90 degrees between diagonals, $m = (1, 1)$ and $m' = (1, -1)$: then $x = (1, 1)$ and $z = (2, 0)$. The move $x \to z$ needs the cells $x + (0, -1) = (1, 0)$ and $z = (2, 0)$, so they are free, and two straight moves $p \to (1, 0) \to (2, 0)$ of total cost $2 < 2\sqrt 2$ reach $z$. Not shortest.
- $m = (1, 0)$ and $m' = (0, 1)$ (a turn of 90 degrees between straight moves): $z = (1, 1)$. If $p + q = (0, 1)$ is free, the diagonal move $p \to z$ is allowed (its cells $(1, 0)$, $(0, 1)$ and $(1, 1)$ are free) and costs $\sqrt 2 < 2$, so the path is not shortest. If $(0, 1)$ is blocked, then $(x, m)$ has the forced move $q = (0, 1)$, and the pair is allowed.
- $m = (1, 0)$ and $m' = (1, 1) = m + q$ with $q = (0, 1)$: if $(0, 1)$ is blocked, $m'$ is a forced move and the pair is allowed. If not, we are in the second case of the claim.
- The remaining pairs are $(m, m)$, and a diagonal $m$ followed by one of its straight parts. These are allowed. $\square$

**Lemma 2 (an allowed shortest path exists).** If $t$ can be reached from $s$, some shortest path from $s$ to $t$ is allowed.

*Proof.* Take a shortest path, and while it is not allowed, take a pair that is not allowed. By Lemma 1 it is $p \to x \to z$ with $m$ straight, $m' = m + q$ and $p + q$ free. By symmetry let $p = (0, 0)$, $m = (1, 0)$ and $q = (0, 1)$, so $x = (1, 0)$ and $z = (2, 1)$. Replace $x$ by $x' = (1, 1)$, so that the path makes the diagonal move first and the straight move second. The move $p \to x'$ is diagonal; its cells $(1, 0)$, $(0, 1)$ and $(1, 1)$ are free, because $(1, 0) = x$, $(0, 1) = p + q$ is free by the case, and $(1, 1)$ is needed by the move $x \to z$. The move $x' \to z$ is straight to a free cell. The cost does not change, so the new path is a shortest path. The diagonal move is now one place earlier. The number of diagonal moves stays the same, and the sum of their positions on the path goes down by $1$. This sum is a nonnegative integer, so after finitely many steps every pair is allowed. $\square$

**The jump graph.** Let $J$ be the graph whose nodes are $(s, \text{none})$ and the pairs $(y, m)$ of a cell and a move. From a node $(x, d)$ there is an arc to $(y, m)$ for each $m$ in PRUNED$(x, d)$ with $y = $ JUMP$(x, m) \ne$ none. Its cost is $k$ times the cost of $m$, where $k$ is the number of steps of the scan. Lines L1 to L9 are A* on $J$ from $(s, \text{none})$, with the octile heuristic $h(y) = \sqrt 2 \min(|\Delta x|, |\Delta y|) + \bigl| |\Delta x| - |\Delta y| \bigr|$ to $t$, and they stop at the first node with cell $t$ that is taken from the open set.

**Lemma 3 (scans stop).** Each call of JUMP stops, and if it returns $y$, then the cells from $x$ to $y$ in direction $m$ form a straight grid path of allowed moves.

*Proof.* Each pass of the loop moves one step in direction $m$, or returns. The grid is finite, so line L14 is reached at the border at the latest. A straight scan does not call JUMP, and a diagonal scan calls JUMP only for straight moves, so the calls inside line L18 stop too. Each step was checked by line L14. $\square$

**Lemma 4 (soundness).** Each path of $J$ from $(s, \text{none})$ to a node with cell $t$ gives a grid path from $s$ to $t$ of the same cost. So the cost of every such path is at least $C^*$.

*Proof.* Replace each arc by the straight grid path of Lemma 3. Its cost is the cost of the arc. $\square$

**Lemma 5 (completeness of the jumps).** If $t$ can be reached from $s$, then $J$ has a path from $(s, \text{none})$ to a node with cell $t$ of cost $C^*$.

*Proof.* Let $P = v_0, v_1, \dots, v_n$ be an allowed shortest path (Lemma 2), with $v_0 = s$, $v_n = t$, and move $m_i$ from $v_{i-1}$ to $v_i$. If $n = 0$, the root node has cell $t$. Else we build nodes $(v_{i_0}, d_0), (v_{i_1}, d_1), \dots$ of $J$, joined by arcs, with $i_0 = 0$, $d_0 = $ none, and with this property: $m_{i_j + 1}$ is in PRUNED$(v_{i_j}, d_j)$. This holds at the root, where every move is in PRUNED.

Let $(x, d) = (v_i, d_j)$ have the property, with $i < n$, and let $m = m_{i+1}$. Let $v_l$ be the end of the straight run of $P$ in direction $m$ from $v_i$: $m_{i+1} = \dots = m_l = m$, and $l = n$ or $m_{l+1} \ne m$. JUMP$(x, m)$ walks over $v_{i+1}, v_{i+2}, \dots$, and these moves are allowed because $P$ makes them. We show that it returns some $v_k$ with $i < k \le l$.

It is enough to show that the scan stops at $v_l$ if it gets there. If $v_l = t$, line L16 stops it. Else the pair $(m, m_{l+1})$ at $v_l$ is allowed and is not $(m, m)$. If $m$ is straight, $m_{l+1}$ is a forced move of $(v_l, m)$, and line L17 stops the scan. If $m$ is diagonal, $m_{l+1}$ is a straight part $c$ of $m$. The path $P$ goes on from $v_l$ in direction $c$, to the end $v_r$ of that straight run. At $v_r$ either $v_r = t$, or the next pair is allowed and not $(c, c)$, so $m_{r+1}$ is a forced move of $(v_r, c)$. So the scan JUMP$(v_l, c)$ stops at $v_r$ or before, by line L16 or L17, and returns a cell. Then line L18 stops the outer scan at $v_l$.

So the arc goes to $(v_k, m)$ with $i < k \le l$, and its cost is the cost of the moves $m_{i+1}, \dots, m_k$ of $P$. If $k = n$ we are done. If $k < l$, the next move of $P$ is $m$, which is in PRUNED$(v_k, m)$ for straight and for diagonal $m$, because the move is allowed. If $k = l$, the pair $(m, m_{l+1})$ is allowed, so $m_{l+1}$ is in PRUNED$(v_k, m)$. In both cases the new node has the property, and its index is larger. So after at most $n$ arcs we reach $t$, and the total cost is the cost of $P$, which is $C^*$. $\square$

**Lemma 6 (the heuristic is consistent on $J$).** For each arc $(x, d) \to (y, m)$ of cost $w$, $h(x) \le w + h(y)$, and $h(t) = 0$.

*Proof.* The octile distance is the length of a shortest path in the 8-connected grid with no walls, so it obeys the triangle inequality. The arc moves $k$ steps in one direction, so $w$ equals the octile distance from $x$ to $y$. So $h(x) \le \text{octile}(x, y) + h(y) = w + h(y)$. $\square$

**Theorem 7.** JUMP-POINT-SEARCH stops. If $t$ can be reached from $s$, it returns a list of jump points whose straight segments form a grid path from $s$ to $t$ of cost $C^*$. If not, it returns no path.

*Proof.* $J$ is finite: it has at most $9$ nodes per cell. Each node is taken from the open set and expanded at most once (the closed set), and each expansion makes finitely many scans, which stop by Lemma 3. So the search stops. With a consistent heuristic, A* on a finite graph with positive arc costs returns a cheapest path to the goal set (see [A*](/a-star-search/) and its proof; the goal set here is all nodes with cell $t$, and $h$ is $0$ on all of them). By Lemmas 4 and 5, the cheapest path of $J$ to a node with cell $t$ costs exactly $C^*$, and Lemma 4 turns it into a grid path of that cost. If $t$ cannot be reached, $J$ has no node with cell $t$ (Lemma 4), so the open set becomes empty and line L9 returns no path. $\square$

**Remarks.** The nodes of $J$ are pairs of a cell and a direction. If a search keeps only one node per cell, two arrivals with the same cost but different directions share one set of pruned directions, and Lemma 5 does not apply as stated. The proof above is for the version with pairs, which is what the implementation does. The proof uses the rule without corner cutting in Lemma 1 and in Lemma 2. With corner cutting, as in the 2011 paper, diagonal moves have forced neighbours too, and the cases of Lemma 1 change.
