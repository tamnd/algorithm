---
title: Gouraud scanline interpolation covers the top-left pixels and writes the barycentric value
proves: [correctness]
status: full
---

Let $T$ be the triangle with vertices $v_0, v_1, v_2$, with nonzero area, and vertex intensities $I_0, I_1, I_2$. Coordinates are exact rationals. Let $f$ be the affine function of the plane with $f(v_k) = I_k$ for $k = 0, 1, 2$. It exists and is unique because the vertices are not on one line, and $f(p) = \sum_k \lambda_k(p) I_k$, where $\lambda_k$ are the barycentric coordinates ([edge function](/edge-function/), property 6).

**Claim.** GOURAUD-TRIANGLE writes pixel $(i, j)$ if and only if $T$ covers its center $p = (x_c, y_c)$ under the [top-left fill rule](/top-left-fill-rule/). It writes each such pixel once, with the value $f(p)$.

Let $d(\varepsilon) = (\varepsilon, \varepsilon^2)$. Step 1 of the proof of the theorem on the [top-left fill rule](/top-left-fill-rule/) page shows: $T$ covers $p$ if and only if $p + d(\varepsilon)$ is in the interior of $T$ for all small enough $\varepsilon > 0$. So it is enough to prove that the scanline rule has the same description.

**Lemma 1 (the rows).** Let $y' = y_c + \varepsilon^2$. For all small $\varepsilon > 0$, $y_{\min} < y' < y_{\max}$ holds if and only if $y_{\min} \le y_c < y_{\max}$. *Proof.* If $y_{\min} \le y_c < y_{\max}$, then $y' > y_{\min}$, and $y' < y_{\max}$ once $\varepsilon^2 < y_{\max} - y_c$. If $y_c < y_{\min}$, then $y' < y_{\min}$ for small $\varepsilon$. If $y_c \ge y_{\max}$, then $y' > y_{\max}$. $\square$

So line L1 visits exactly the rows that can hold a covered center. Fix such a row.

**Lemma 2 (the two edges).** There are exactly two edges $(a, b)$ with $y_a \le y_c < y_b$, and for all small $\varepsilon > 0$ these two edges are the edges of $T$ that the horizontal line at height $y'$ meets. *Proof.* A horizontal edge has $y_a = y_b$ and is never selected. For $y_{\min} < y' < y_{\max}$, the horizontal line at $y'$ meets the boundary of the convex set $T$ in exactly two points, on two different non-horizontal edges, and does not pass through a vertex once $\varepsilon$ is so small that no vertex has its $y$ in $(y_c, y_c + \varepsilon^2]$. An edge with $y_a < y_b$ meets the line at $y'$ exactly when $y_a < y' < y_b$ (no vertex is at $y'$), and for small $\varepsilon$ this holds exactly when $y_a \le y_c < y_b$. $\square$

Let the two edges cross the line $y = y_c$ at $x_l \le x_r$, as in line L4, and let $\sigma_l$ and $\sigma_r$ be their slopes $dx/dy$. Both edges are selected on $[y_c, y_c + \delta)$ for some $\delta > 0$, so on that interval the edge through $x_l$ is the left boundary of $T$ and the edge through $x_r$ is the right one, except when $x_l = x_r$, where the left one is the one with the smaller slope. At height $y'$ the interior of $T$ is the open interval between $X_l = x_l + \sigma_l \varepsilon^2$ and $X_r = x_r + \sigma_r \varepsilon^2$ (in the case $x_l = x_r$, between the smaller and the larger of these two).

**Lemma 3 (the span).** For all small $\varepsilon > 0$, $p + d(\varepsilon)$ is in the interior of $T$ if and only if $x_l < x_r$ and $x_l \le x_c < x_r$. *Proof.* The point is inside if and only if $X_l < x_c + \varepsilon < X_r$.

- If $x_l = x_r$, both inequalities need $x_c + \varepsilon$ strictly between $x_l + \sigma_l \varepsilon^2$ and $x_l + \sigma_r \varepsilon^2$, which are at distance $O(\varepsilon^2)$ from $x_l$. If $x_c \ne x_l$, the point is at distance about $|x_c - x_l|$ from both, so it is outside. If $x_c = x_l$, the point is at distance $\varepsilon$ from $x_l$, which is more than $O(\varepsilon^2)$, so it is outside. This is line L5.
- If $x_l < x_r$: the left inequality $x_l + \sigma_l \varepsilon^2 < x_c + \varepsilon$ holds for all small $\varepsilon$ if $x_c > x_l$, holds if $x_c = x_l$ (since $\varepsilon > \sigma_l \varepsilon^2$ for small $\varepsilon$), and fails if $x_c < x_l$. So it holds if and only if $x_c \ge x_l$. The right inequality $x_c + \varepsilon < x_r + \sigma_r \varepsilon^2$ holds if $x_c < x_r$, fails if $x_c = x_r$ (since $\varepsilon > \sigma_r \varepsilon^2$), and fails if $x_c > x_r$. So it holds if and only if $x_c < x_r$. $\square$

Lines L7 and L9 select exactly the centers of the row with $x_l \le x_c < x_r$, in order, each once. With Lemmas 1 to 3, a pixel is written if and only if $p + d(\varepsilon)$ is in the interior of $T$ for all small $\varepsilon > 0$, that is, if and only if $T$ covers $p$. Each pixel is written at most once, because the rows are visited once and the centers of a row in increasing order.

**The values.** The function $f$ is affine, so on the edge from $a$ to $b$, $f(a + t(b - a)) = f(a) + t(f(b) - f(a))$. The edge ends are vertices with $f(a) = I_a$ and $f(b) = I_b$, so line L3 computes $I = f(x, y_c)$ at both span ends: $I_l = f(x_l, y_c)$ and $I_r = f(x_r, y_c)$. On the row, $x \mapsto f(x, y_c)$ is affine, so for each $x$,

$$f(x, y_c) = I_l + (x - x_l)\frac{I_r - I_l}{x_r - x_l} = I_l + (x - x_l)\,\Delta I .$$

Line L8 sets $I = f(x_c, y_c)$ for the first center. If $I = f(x_c, y_c)$ before line L11, then after it $I + \Delta I \cdot u = f(x_c + u, y_c)$, where $u$ is the pixel width, and $x_c$ has moved by $u$. By induction, line L10 writes $f(x_c, y_c)$ at each center, and $f(x_c, y_c) = \sum_k \lambda_k I_k$.

**Termination.** Line L1 visits finitely many rows, and in each row the loop of line L9 adds a fixed positive width to $x_c$ until $x_c \ge x_r$ or the screen ends. $\blacksquare$
