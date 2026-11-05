---
title: Myers' greedy search finds a shortest edit script
proves: [correctness]
status: full
---

We use the pseudocode of the page. The search of lines L4 to L7 can produce points with $x > m$ or $y > n$, so we work in an extended graph $G$. Its vertices are all points $(x, y)$ with integers $x, y \ge 0$. Each point has a *right* edge to $(x + 1, y)$ and a *down* edge to $(x, y + 1)$, each of cost 1, and a *diagonal* edge to $(x + 1, y + 1)$ of cost 0 if $x < m$, $y < n$ and $a_{x+1} = b_{y+1}$. The edit graph of the page is the part with $x \le m$ and $y \le n$. Along each edge, $x$ and $y$ do not decrease. The *diagonal* of $(x, y)$ is $k = x - y$; a right edge raises $k$ by 1, a down edge lowers it by 1, and a diagonal edge keeps it. The cost of a path is its number of right and down edges.

For a point $P = (x, y)$, let $\mathrm{snake}(P)$ be the end of the longest run of diagonal edges from $P$: the point $(x + t, y + t)$ with $t \ge 0$ largest such that the $t$ diagonal edges exist. This is what line L7 computes.

Let $R_d$ be the set of points that are the end of some path of cost exactly $d$ from $(0, 0)$, and for each $k$ let $F_d[k] = \max\{ x : (x, x - k) \in R_d \}$, or undefined if no such point exists.

**Lemma 1 (diagonals).** If $(x, y) \in R_d$, then $|x - y| \le d$ and $x - y \equiv d \pmod 2$. For each $k \in \{-d, -d + 2, \ldots, d\}$, $F_d[k]$ is defined and finite.

*Proof.* A path of cost $d$ with $r$ right and $d - r$ down edges ends on diagonal $r - (d - r) = 2r - d$, which has the parity of $d$ and lies in $[-d, d]$. For a given $k = 2r - d$, the path of $r$ right edges then $d - r$ down edges reaches diagonal $k$, so $F_d[k]$ is defined. It is finite, since a path of cost $d$ has at most $d$ right edges and at most $\min(m, n)$ diagonal edges, so $x \le d + \min(m, n)$. $\square$

**Lemma 2 (later is better).** Let $P = (x, y)$ and $P' = (x', y')$ be on the same diagonal with $x \le x'$. Then each point $Q$ on this diagonal that can be reached from $P$ by diagonal edges only has first coordinate at most that of $\mathrm{snake}(P')$.

*Proof.* The diagonal edges from $P$ go through the points $(x + s, y + s)$, $s = 0, 1, \ldots$ If the run from $P$ stops before $x'$, then $Q$ has first coordinate below $x' \le$ the first coordinate of $\mathrm{snake}(P')$. Otherwise the run passes through $P'$, and from there it uses the same edges as the run from $P'$, so it ends at $\mathrm{snake}(P')$, and $Q$ is on this run. $\square$

**Lemma 3 (the recurrence, Myers' Lemma 2).** $F_0[0]$ is the first coordinate of $\mathrm{snake}((0, 0))$. For $d \ge 1$ and $k \in \{-d, -d + 2, \ldots, d\}$, let

$$x_0 = \begin{cases} F_{d-1}[k + 1] & \text{if } k = -d, \\ F_{d-1}[k - 1] + 1 & \text{if } k = d, \\ \max(F_{d-1}[k - 1] + 1,\ F_{d-1}[k + 1]) & \text{otherwise}. \end{cases}$$

Then $F_d[k]$ is the first coordinate of $\mathrm{snake}((x_0, x_0 - k))$.

*Proof.* For $d = 0$, the paths of cost 0 are runs of diagonal edges from $(0, 0)$, and the furthest one ends at $\mathrm{snake}((0, 0))$.

Let $d \ge 1$. ($\ge$) The point of diagonal $k + 1$ at $x = F_{d-1}[k + 1]$ is in $R_{d-1}$; a down edge takes it to $(x, x - k)$ on diagonal $k$, at cost $d$; then the snake keeps cost $d$. In the same way, the point of diagonal $k - 1$ at $F_{d-1}[k - 1]$ and a right edge reach $x = F_{d-1}[k - 1] + 1$ on diagonal $k$. These points exist when $k + 1 \le d - 1$ and $k - 1 \ge -(d - 1)$ respectively, by Lemma 1, which are the cases of $x_0$. So $\mathrm{snake}((x_0, x_0 - k)) \in R_d$.

($\le$) Let $Q \in R_d$ be on diagonal $k$, at the end of a path of cost $d \ge 1$. Cut the path after its last right or down edge, at the point $S$. Then $Q$ is reached from $S$ by diagonal edges only. The point before this last edge is in $R_{d-1}$. If the edge is a down edge, that point is on diagonal $k + 1$ with first coordinate at most $F_{d-1}[k + 1]$, and $S$ has the same first coordinate. If it is a right edge, the point is on diagonal $k - 1$ with first coordinate at most $F_{d-1}[k - 1]$, and $S$ has one more. In both cases $S$ is on diagonal $k$ with first coordinate at most $x_0$. By Lemma 2 with $P = S$ and $P' = (x_0, x_0 - k)$, the first coordinate of $Q$ is at most that of $\mathrm{snake}((x_0, x_0 - k))$. $\square$

**Lemma 4 (the loop computes $F$).** After round $d$ of the loop of line L2, $V[k] = F_d[k]$ for each $k \in \{-d, -d + 2, \ldots, d\}$, and these values are saved as $V_d$.

*Proof.* Induction on $d$. In round 0, $k = 0 = -d$, so line L4 sets $x = V[1] = 0$ (line L1), and lines L6 to L8 store the snake from $(0, 0)$; this is $F_0[0]$ by Lemma 3. In round $d \ge 1$, the entries $V[k \pm 1]$ read in lines L4 and L5 are on diagonals of the parity of $d - 1$, which round $d$ does not write, so they hold $F_{d-1}[k \pm 1]$ by the induction hypothesis. If $k = -d$, line L4 takes $x = F_{d-1}[k + 1]$. If $k = d$, the test of line L4 fails and line L5 takes $F_{d-1}[k - 1] + 1$. Otherwise line L4 takes $F_{d-1}[k + 1]$ when $F_{d-1}[k - 1] < F_{d-1}[k + 1]$, that is, when $F_{d-1}[k + 1] \ge F_{d-1}[k - 1] + 1$, and line L5 takes $F_{d-1}[k - 1] + 1$ otherwise; in both cases $x = x_0$. Line L7 follows the snake: its test is exactly the condition for a diagonal edge of $G$. By Lemma 3, line L8 stores $F_d[k]$. $\square$

**Lemma 5 (the stop).** Let $D$ be the cost of a cheapest path from $(0, 0)$ to $(m, n)$, and call a point *final* if $x \ge m$ and $y \ge n$. If a final point is in $R_d$, then $d \ge D$, and if $d = D$ the point is $(m, n)$.

*Proof.* Let a path of cost $d$ end at a final point $(x, y)$. Along the path the coordinates grow by at most 1 per edge, from $(0, 0)$, so there is a first point $S = (s, t)$ of the path with $s = m$ or $t = n$; then $s \le m$ and $t \le n$. After $S$ the path has no diagonal edges, since these need $x < m$ and $y < n$, so the rest of the path costs $(x - s) + (y - t)$. The path from $(0, 0)$ to $S$, followed by $m - s$ right edges and $n - t$ down edges (one of the two numbers is 0), reaches $(m, n)$ at cost

$$d - (x - s) - (y - t) + (m - s) + (n - t) = d - (x - m) - (y - n) \le d.$$

So $D \le d$, with equality only if $x = m$ and $y = n$. $\square$

**Theorem.** MYERS returns $d = D$, and TRACEBACK outputs a shortest edit script from $A$ to $B$.

*Proof.* The point $(m, n)$ is reached by a path of cost $D$, so it is in $R_D$ on diagonal $m - n$, and $F_D[m - n] \ge m$, with $y = F_D[m - n] - (m - n) \ge n$; so round $D$ finds a final point. By Lemma 5, no earlier round does, since a final point of round $d$ is in $R_d$ by Lemma 4. So the loop stops at round $D$ (and $D \le m + n$, so line L2 runs far enough). In round $D$, each final point that line L9 finds is $(m, n)$, again by Lemma 5.

TRACEBACK starts at $(m, n) = (F_D[k], F_D[k] - k)$ with $k = m - n$. In step $d$, it is at the point $(F_d[k], F_d[k] - k)$ for the current $k$. Line L12 repeats the choice of line L4 in round $d$, with the same values $V_{d-1}$, so $(px, py)$ is the point of round $d - 1$ from which round $d$ started, $(sx, sy)$ is $(x_0, x_0 - k)$ after one down or right edge, and $(x, y)$ is the end of the snake from it (Lemma 4). So the steps of the traceback walk back a path of $G$: a snake, one right or down edge, then the same for $d - 1$, down to round 0, whose snake starts at $(0, 0)$. This path has cost $D$ and ends at $(m, n)$. A path of $G$ that ends at $(m, n)$ stays in the edit graph, since coordinates do not decrease. Its right edges are deletions, its down edges are insertions, and its diagonal edges are kept items, so the output is an edit script of $D$ operations. By the theorem of the [shortest edit script](/shortest-edit-script/) page, the edit scripts correspond to the paths of the edit graph, so no script is shorter. $\blacksquare$

**Cost.** Round $d$ visits $d + 1$ diagonals with $O(1)$ work outside line L7, so $O(D^2)$ in all. For line L7, consider a diagonal $k$ and rounds $d - 2$ and $d$ with $|k| \le d - 2$. The point of round $d - 2$ on diagonal $k$, followed by a right edge, gives $F_{d-1}[k + 1] \ge F_{d-2}[k] + 1$, so $x_0 > F_{d-2}[k]$ in round $d$: the snake of round $d$ starts after the end of the snake of round $d - 2$. So each diagonal edge on diagonal $k$ is walked at most once, and diagonal $k$ has at most $\min(m, n)$ diagonal edges. With at most $2D + 1$ diagonals, line L7 takes $O(D \min(m, n))$ steps, and the total is $O((m + n) D)$.
