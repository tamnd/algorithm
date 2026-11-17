---
title: The R-table votes count matching edge pairs, and a translated or 90 degree rotated copy of the template gets at least m votes at its reference point
proves: [correctness]
status: full
---

We use the notation of the page. The template edge points are $(x_i, b_i)$ for $i = 1, \ldots, m$, the image edge points are $(y_j, b_j)$ for $j = 1, \ldots, e$, the reference point is $c$, and $G$ is the set of grid cells of the image. All points are integer pairs $(u, v)$.

**Theorem 1 (the votes count matching pairs).** After lines L1 to L7, for every $p \in G$,
$$A[p] = \#\{(i, j) : b_i = b_j,\ y_j + c - x_i = p\}.$$

*Proof.* After lines L1 and L2, $R[b]$ is the list of the offsets $c - x_i$ over the indices $i$ with $b_i = b$, one entry for each such $i$ (two template points give two entries even if the offsets are equal, since the points differ, and in fact the offsets differ too). Line L3 sets $A = 0$. Lines L4 and L5 visit each pair $(j, i)$ with $b_i = b_j$ exactly once. For such a pair, line L6 computes $p = y_j + c - x_i$, and line L7 adds 1 to $A[p]$ if $p \in G$ and does nothing otherwise. No other line changes $A$. So $A[p]$ is the number of pairs with $b_i = b_j$ and $y_j + c - x_i = p$, for every $p \in G$. $\square$

**Theorem 2 (translated copy).** Let $t$ be an integer vector. Suppose that for each $i$, $(x_i + t, b_i)$ is an image edge point, and that $c + t \in G$. Then $A[c + t] \ge m$. If, in addition, the image edge points are exactly $(x_i + t, b_i)$ for $i = 1, \ldots, m$, then $A[c + t] = m$.

*Proof.* For each $i$, let $j(i)$ be the index of the image edge point $x_i + t$. Then $b_{j(i)} = b_i$ and $y_{j(i)} + c - x_i = c + t$, so the pair $(i, j(i))$ is counted in $A[c + t]$ by Theorem 1. The $m$ pairs are distinct since their first indices are distinct. So $A[c + t] \ge m$.

For the equality, every image edge point is $y_j = x_{i'} + t$ with $b_j = b_{i'}$ for one $i'$. A pair $(i, j)$ is counted in $A[c + t]$ if and only if $b_i = b_j$ and $x_{i'} + t + c - x_i = c + t$, that is, $x_i = x_{i'}$, that is, $i = i'$, since distinct template edge points are distinct pixels. So for each $j$ exactly one pair is counted, and $A[c + t] = e = m$. $\square$

**Lemma 1 (when the image edges are the translated template edges).** Suppose the template $T$ of size $W_t \times H_t$ is 0 on its two outer rows and columns on each side, the image $I$ satisfies $I[v + t_v][u + t_u] = T[v][u]$ for all template pixels, $I$ is 0 at all other pixels, and the copy satisfies $t_u \ge 1$, $t_v \ge 1$, $t_u + W_t \le W - 1$ and $t_v + H_t \le H - 1$. Then the image edge points are exactly $(x_i + t, b_i)$.

*Proof.* The Sobel gradient at a pixel that is not on the border of its array depends only on the $3 \times 3$ neighborhood of the pixel. Take a pixel $z$ of the image and consider three cases. (a) $z = x + t$ for a template pixel $x$ that is not on the border of $T$: its neighborhood in $I$ is the translate of its neighborhood in $T$, and $z$ is not on the border of $I$ by the conditions on $t$, so the gradients are equal and $z$ is an edge point with bin $b$ if and only if $x$ is one with bin $b$. (b) $z = x + t$ for $x$ on the border of $T$: the gradient of $x$ in $T$ is 0 by convention. The neighborhood of $z$ in $I$ consists of pixels of the two outer rings of the copy and pixels outside the copy, all 0, so the gradient of $z$ is 0. (c) $z$ is not in the copy: its neighborhood consists of pixels outside the copy and pixels of the outer ring of the copy, all 0, or $z$ is on the border of $I$. In both cases the gradient is 0. So the edge points of $I$ are exactly the translates of the edge points of $T$, with the same bins. $\square$

Lemma 1 with Theorem 2 gives $A[c + t] = m$ for a clean copy, which is the example of the page and the first test.

**Theorem 3 (rotation by 90 degrees).** Let $\rho(u, v) = (-v, u)$, the rotation by 90 degrees in the $(u, v)$ frame, and let $B$ be a multiple of 4. Suppose that each template edge point $(x_i, b_i)$ appears in the image as the edge point $(\rho(x_i) + t, (b_i + B/4) \bmod B)$, and that $c' = \rho(c) + t \in G$. Let $A'$ be the accumulator of lines L3 to L7 when line L5 reads $R[(b - B/4) \bmod B]$ and line L6 uses $p \leftarrow y + \rho(r)$. Then $A'[c'] \ge m$.

*Proof.* The image edge point $y = \rho(x_i) + t$ has bin $b = b_i + B/4 \pmod B$, so it reads $R[b_i]$, which holds $c - x_i$. Since $\rho$ is linear, it votes at $\rho(x_i) + t + \rho(c - x_i) = \rho(c) + t = c'$. The $m$ template points give $m$ distinct pairs, as in Theorem 2. $\square$

**Lemma 2 (the hypothesis of Theorem 3 holds for a rotated image).** Let $I'$ be the image $I$ rotated by 90 degrees, $I'[u][H - 1 - v] = I[v][u]$, so that the pixel $(u, v)$ moves to $(H - 1 - v, u) = \rho(u, v) + (H - 1, 0)$. If $(g_u, g_v)$ is the Sobel gradient of $I$ at an interior pixel $z$, then the Sobel gradient of $I'$ at the image of $z$ is $(-g_v, g_u) = \rho(g_u, g_v)$, and its bin is the bin of $z$ plus $B/4$ modulo $B$.

*Proof.* Write $I'(w) = I(\rho^{-1}(w - s))$ with $s = (H - 1, 0)$. The Sobel operator is a finite difference along an axis with smoothing $(1, 2, 1)$ across it. Let $w = \rho(z) + s$. A unit step along $+u$ at $w$ corresponds to the step $\rho^{-1}(1, 0) = (0, -1)$ at $z$, and a step along $+v$ at $w$ corresponds to $\rho^{-1}(0, 1) = (1, 0)$ at $z$. So $g'_u(w)$ is the Sobel difference of $I$ at $z$ along $-v$, which is $-g_v(z)$, and $g'_v(w)$ is the Sobel difference along $+u$, which is $g_u(z)$; the smoothing weights are symmetric, so they match. The magnitude is unchanged, so $w$ is an edge point if and only if $z$ is one. The angle grows by $\pi/2$, so $\varphi' / (2\pi / B) = \varphi / (2\pi / B) + B/4$ modulo $B$, and since $B/4$ is an integer, the floor of the value plus $1/2$ grows by exactly $B/4$. $\square$

With Lemma 1 applied to the rotated template (it also has a blank border of 2 pixels), Lemma 2 and Theorem 3 give the rotation test: in the accumulator for the shift of $B/4$ bins, the rotated reference point gets $m$ votes. The code rounds $\cos$ and $\sin$ of $\pi/2$ to 0 and 1, so its rotated offsets are exactly $\rho(r)$.

**What is not claimed.** Theorem 2 gives a lower bound at the true cell, not that the true cell is the largest. Edge points of clutter, or of the shape itself in a wrong pairing, can add votes to another cell, and nothing bounds them in general. For rotations that are not multiples of 90 degrees, the rotated offsets are rounded and the bins do not shift by an integer, so the votes spread and Theorem 3 does not apply. That the peak is the true position in real images is a heuristic, supported by experiments.
