---
title: The second-order Taylor interpolator moves the arc length L per period up to an error of order L cubed, so its relative feedrate error is of order (V tau) squared
proves: [correctness]
status: full
---

**Setting.** Let $C : [a, b] \to \mathbb{R}^d$ be three times continuously differentiable and regular, $|C'(u)| > 0$ on $[a, b]$. Its arc length $s(u) = \int_a^u |C'(w)|\, dw$ has $s' = |C'| > 0$, and $s$ is three times continuously differentiable, because $|C'| = \sqrt{C' \cdot C'}$ is twice continuously differentiable where $C' \ne 0$. So $s$ has an inverse $u(s)$ on $[0, s(b)]$, also three times continuously differentiable. The feed is $V$, the period is $\tau$, and $L = V\tau$. Let
$$
M_1 = \max_{[a,b]} |C'|, \qquad M_2 = \max \Big|\frac{d^2u}{ds^2}\Big|, \qquad M_3 = \max \Big|\frac{d^3u}{ds^3}\Big|.
$$

**Lemma 1 (derivatives of the inverse).** At $u = u(s)$,
$$
\frac{du}{ds} = \frac{1}{|C'|}, \qquad \frac{d^2u}{ds^2} = -\frac{C' \cdot C''}{|C'|^4}.
$$

*Proof.* The first is the derivative of an inverse function, $1/s'(u)$. For the second, write $g(u) = |C'(u)|^{-1} = (C' \cdot C')^{-1/2}$. Then $g'(u) = -(C' \cdot C')^{-3/2} (C' \cdot C'')$, and by the chain rule $d^2u/ds^2 = g'(u)\, du/ds = g'(u) g(u) = -(C' \cdot C'')/|C'|^4$. $\square$

So line L5 computes $\Delta u_2 = L\, u'(s_k) + \tfrac12 L^2 u''(s_k)$, the Taylor polynomial of degree 2 of $u(s_k + L) - u(s_k)$, where $s_k = s(u_k)$. The first-order interpolator uses $\Delta u_1 = L\, u'(s_k)$.

**Theorem.** Let $\Delta S_k = s(u_k + \Delta u_2) - s(u_k)$ be the arc length that a step of the second-order interpolator covers, and suppose that $u_k + \Delta u_2$ and $u(s_k + L)$ are in $[a, b]$. Then
$$
|\Delta S_k - L| \le \frac{M_1 M_3}{6} L^3, \qquad \text{so} \qquad \Big|\frac{\Delta S_k}{L} - 1\Big| \le \frac{M_1 M_3}{6} (V\tau)^2 .
$$
For the first-order step, $|\Delta S_k - L| \le \tfrac12 M_1 M_2 L^2$, a relative error of order $V\tau$.

*Proof.* By Taylor's theorem with the Lagrange remainder, there is $\xi$ between $s_k$ and $s_k + L$ with
$$
u(s_k + L) = u_k + L u'(s_k) + \tfrac12 L^2 u''(s_k) + \tfrac16 L^3 u'''(\xi) = u_k + \Delta u_2 + \tfrac16 L^3 u'''(\xi).
$$
The exact step ends at $u^\ast = u(s_k + L)$, where $s(u^\ast) - s(u_k) = L$. So
$$
\Delta S_k - L = s(u_k + \Delta u_2) - s(u^\ast).
$$
By the mean value theorem, $|s(x) - s(y)| \le M_1 |x - y|$, and $|u_k + \Delta u_2 - u^\ast| = \tfrac16 L^3 |u'''(\xi)| \le \tfrac16 M_3 L^3$. This gives the first bound, and division by $L$ gives the second. For the first-order step the remainder is $\tfrac12 L^2 u''(\xi)$ instead, and the same argument gives $\tfrac12 M_1 M_2 L^2$. $\square$

**The orders are sharp.** Write $\Delta S_k - L = s'(\eta)\big(u_k + \Delta u_2 - u^\ast\big)$ for some $\eta$ between the two end parameters. As $L \to 0$, $\eta \to u_k$ and $\xi \to s_k$, so
$$
\frac{\Delta S_k - L}{L^3} \to -\frac{|C'(u_k)|\, u'''(s_k)}{6}.
$$
This limit is not zero where $u''' \ne 0$, so the error is of order exactly $L^3$ there. In the same way, the first-order error divided by $L^2$ tends to $-|C'| u''/2 = (C' \cdot C'')/(2|C'|^3)$, which is not zero where the speed of the curve changes.

**Exact check on a Pythagorean hodograph cubic.** For $C(t) = (t - t^3/3,\ t^2)$, $C' = (1 - t^2, 2t)$ and $|C'| = 1 + t^2$, so $s(t) = t + t^3/3$. Then $C'' = (-2t, 2)$ and $C' \cdot C'' = 2t(1 + t^2)$, so
$$
\Delta u_2 = \frac{L}{1 + t^2} - \frac{L^2 t}{(1 + t^2)^3}.
$$
Also $u''(s) = -2t/(1+t^2)^3$ and $u'''(s) = (10t^2 - 2)/(1 + t^2)^5$, so the limit above is $(1 - 5t^2)/(3(1 + t^2)^4)$. At $t = 0$, $\Delta u_2 = L$ and $\Delta S - L = L^3/3$ exactly. At $t = 1$, the first-order step is $L/2$ with the error $L^2/4 + L^3/24$ exactly, and the second-order error is $-L^3/12 + O(L^4)$. The tests check these values in exact rational arithmetic.

**The loop.** Each pass of the loop moves $u$ forward by a positive step, and the code stops with an error if the step is not positive. On a regular curve, $\Delta u_2 = L/|C'| + O(L^2)$ is at least $L/(2M_1)$ once $L$ is small enough, so the loop ends after at most $2M_1(b - a)/L + 1$ passes, and the last point is clipped to $u_{\text{end}}$.

**What is not covered.** The theorem bounds the arc length of each step. The machine moves along the chord between $C(u_k)$ and $C(u_{k+1})$, which is shorter than the arc by $\kappa^2 \Delta S^3/24 + O(\Delta S^4)$ for a curve of curvature $\kappa$, so the feed along the chords has a relative error of order $L^2$ as well, from this second source. The errors of all steps add up, so after $n$ steps the position along the curve may drift by up to $n M_1 M_3 L^3 / 6$, which is of order $L^2$ times the length of the path.
