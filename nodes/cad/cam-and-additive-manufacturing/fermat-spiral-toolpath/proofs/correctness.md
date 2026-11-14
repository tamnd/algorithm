---
title: The Fermat spiral of a rectangle is a simple path inside it that covers all but the core
proves: [correctness, termination]
status: full
---

**Claim.** Let $W \ge H > 0$ and $w > 0$, let $n \ge 2$ be the number of $i \ge 1$ with $d_i = (i - \tfrac12)w < H/2$, and let $(2n - \tfrac32)w < X < W - \tfrac32 w$. Write $c_j = X - jw$. Then FERMAT-RECTANGLE$(W, H, w, X)$ stops and returns a polyline $P$ with these properties:

1. every segment of $P$ is horizontal or vertical and has positive length, and two segments of $P$ meet only if they are consecutive, and then only at their shared point;
2. every point of $P$ lies in $[w/2, W - w/2] \times [w/2, H - w/2]$;
3. $P$ starts at $(c_{-1}, w/2)$ and ends at $(c_0, w/2)$;
4. the union of the closed squares of side $w$ centered at the points of $P$ is the set of points of the rectangle at distance at most $nw$ from its boundary, where the distance is $\delta(x, y) = \min(x, y, W - x, H - y)$.

Termination is clear: the loop of line L3 runs $n$ times, and every other line does a fixed amount of work.

**Step 0 (two inequalities).** For $1 \le i \le n$: $c_{\min(i, n-1)} > d_i$, because $c_{\min(i,n-1)} - d_i \ge c_{n-1} - d_n = X - (2n - \tfrac32)w > 0$ (the left side decreases in $i$ for $i \le n-1$, and for $i = n$ it is exactly $c_{n-1} - d_n$). And $c_{i-2} < W - d_i$, because $W - d_i - c_{i-2} = W - X - \tfrac32 w > 0$. Also $d_n < H/2$ gives $d_i < H - d_i$ for all $i \le n$, and $W \ge H$ gives $d_i < W - d_i$.

**Step 1 (the pieces).** Let $Q_i$ be the rectangle $[d_i, W - d_i] \times [d_i, H - d_i]$, contour $i$. By Step 0 it is not degenerate. The open contour $R_i$ of line L7 is $Q_i$ without the open interval $G_i = (e_i, s_i)$ of its bottom side, where $s_i = c_{i-2}$, $e_i = c_i$ for $i < n$ and $e_n = c_{n-1}$. By Step 0, $d_i < e_i < s_i < W - d_i$, so $G_i$ lies strictly inside the bottom side, and the five segments of $R_i$ have positive length. The other segments of $P$ are:

- the links of lines L8 and L9: for $1 \le i \le n - 2$, the vertical segment $V_i$ at $x = c_i$ from $y = d_i$ (the end of $R_i$) to $y = d_{i+2}$ (the start of $R_{i+2}$);
- the center join $J$ at $x = c_{n-1}$ from $d_{n-1}$ to $d_n$: the last point of $A$ and the last point of $B$ are the ends $e_{n-1} = (c_{n-1}, d_{n-1})$ and $e_n = (c_{n-1}, d_n)$, in some order;
- the exit $E$ at $x = c_0$ from $y = d_2$ (the start $s_2$ of $R_2$, which is the last point of $B$ reversed) to $y = d_1 = w/2$.

So $P$ is the chain $R_1, V_1, R_3, V_3, \dots$, then $J$, then the even contours in reverse with their links, then $E$. Every segment is horizontal or vertical with positive length.

**Step 2 (simple).** The rectangles $Q_i$ are nested and disjoint: $Q_{i+1}$ lies in the interior of $Q_i$, since $d_{i+1} = d_i + w$. So two different contours never meet. A vertical segment at abscissa $x$ with heights in $[d_i, d_{i+2}]$ meets only $Q_i$, $Q_{i+1}$ and $Q_{i+2}$, and it meets $Q_j$ only where it crosses or touches the bottom side $y = d_j$, provided $d_{i+2} < x < W - d_{i+2}$. This holds for the link $V_i$ at $x = c_i$, $i \le n - 2$: $c_i + d_{i+2} = X + \tfrac32 w < W$ and $c_i - d_{i+2} \ge c_{n-2} - d_n = X - (2n - \tfrac52)w > 0$. It holds for $J$ (contours $n - 1$ and $n$): $c_{n-1} + d_n = X + \tfrac12 w < W$ and $c_{n-1} > d_n$ by Step 0. It holds for $E$ (contours 1 and 2): $c_0 + d_2 = X + \tfrac32 w < W$ and $c_0 > c_{n-1} > d_n \ge d_2$.

- $V_i$ meets $R_i$ only at its lower end and $R_{i+2}$ only at its upper end. It crosses the line $y = d_{i+1}$ at $x = c_i$, and $c_{i+1} < c_i < c_{i-1}$, so the crossing point lies in the gap $G_{i+1} = (c_{i+1}, c_{i-1})$ if $i + 1 < n$, or in $G_n = (c_{n-1}, c_{n-2})$ if $i + 1 = n$. So $V_i$ does not meet $R_{i+1}$.
- $J$ spans $[d_{n-1}, d_n]$ and meets only $R_{n-1}$ and $R_n$, at its ends.
- $E$ spans $[d_1, d_2]$. It meets $R_2$ only at $s_2$. At $y = d_1$ its point $(c_0, d_1)$ lies in $G_1 = (c_1, c_{-1})$, so it does not meet $R_1$.
- Two of these vertical segments have different abscissas $c_1, \dots, c_{n-2}$, $c_{n-1}$ and $c_0$, so they are disjoint.

Within one $R_i$, the five segments form a rectangle minus a gap, so only consecutive ones meet, at corners, and the first and the last do not meet because $G_i$ is not empty. A link meets the segments of $R_i$ and $R_{i+2}$ only at the shared end points. This proves part 1.

**Step 3 (inside, ends).** Every point of $P$ lies on some $Q_i$, and $Q_i \subseteq [d_1, W - d_1] \times [d_1, H - d_1]$ with $d_1 = w/2$. The first point of $P$ is $s_1 = (c_{-1}, d_1)$ and the last is $(c_0, w/2)$. This proves parts 2 and 3.

**Step 4 (coverage).** For a set $S$, let $S^+$ be the union of the closed squares of side $w$ centered at the points of $S$, which is the set of points at $L_\infty$ distance at most $w/2$ from $S$. For a rectangle, $Q_i^+$ is the closed frame $F_i = \{(i - 1)w \le \delta \le iw\}$. Every segment of $P$ lies on some $Q_i$ or between two of them, so $P^+ \subseteq \bigcup_i F_i = \{\delta \le nw\}$.

For the other inclusion, fix $i$ and a point $q \in F_i$. If $q$ is within $L_\infty$ distance $w/2$ of a point of $R_i$, it is covered. Otherwise its nearest points on $Q_i$ lie in the gap, and so $q$ lies in the box $[e_i + w/2, s_i - w/2] \times [(i-1)w, iw]$. For $i = n$ the gap has length $c_{n-2} - c_{n-1} = w$, so this box is the single segment $x = c_{n-1} + w/2$, and its points are at distance exactly $w/2$ from both ends of $R_n$, so they are covered. For $i < n$ the box is $[c_{i-1} - w/2, c_{i-1} + w/2] \times [(i-1)w, iw]$. If $2 \le i \le n - 1$, the link $V_{i-1}$ at $x = c_{i-1}$ spans the heights $d_{i-1}$ to $d_{i+1}$, so its square bead covers the heights $(i - 2)w$ to $(i + 1)w$ and the abscissas of the box. If $i = 1$, the exit $E$ at $x = c_0$ spans $d_1$ to $d_2$, and its bead covers the heights $0$ to $2w$. So $F_i \subseteq P^+$ for every $i$, and $P^+ = \{\delta \le nw\}$.

The core $\{\delta > nw\}$ is the open rectangle $(nw, W - nw) \times (nw, H - nw)$, of area $(W - 2nw)\max(0, H - 2nw)$; note $W > 2nw$ follows from the bounds on $X$. This proves part 4. $\blacksquare$
