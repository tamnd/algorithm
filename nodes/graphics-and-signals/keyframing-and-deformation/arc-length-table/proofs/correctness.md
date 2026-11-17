---
title: The arc length table gives a valid interval, a second order inverse and quadratic Newton refinement
proves: [correctness]
status: full
---

We use the notation of the page.
The curve $c$ is $C^2$ on $[a, b]$, and its speed $v(u) = |c'(u)|$ satisfies $0 < v_{\min} \le v(u) \le v_{\max}$.
Then $s(u) = \int_a^u v$ is $C^2$ with $s' = v$ and $s'' = v'$, and it has a $C^2$ inverse $u(s)$ on $[0, s(b)]$ with $u' = 1/v$ and $u'' = -v'/v^3$.
We first assume that the table is exact, $s_k = s(u_k)$, and treat the quadrature error at the end.

## The search

**Lemma 1.** The values $s_0, \dots, s_m$ are strictly increasing, and for each $s^* \in [0, s_m]$ line L9 finds $k$ with $s_k \le s^* \le s_{k+1}$.

*Proof.*
$s_{k+1} - s_k = \int_{u_k}^{u_{k+1}} v \ge h\,v_{\min} > 0$.
A sorted sequence with $s_0 = 0 \le s^* \le s_m$ has such an index, and binary search finds it in $O(\log m)$ comparisons. $\square$

## The linear inverse

**Lemma 2.** Let $\hat u$ be the value of line L10. Then $|\hat u - u(s^*)| \le \frac18 h^2 v_{\max}^2 \max|u''| \le \frac{h^2 v_{\max}^2 \max|v'|}{8 v_{\min}^3}$.

*Proof.*
On $[s_k, s_{k+1}]$, the inverse function satisfies $u(s_k) = u_k$ and $u(s_{k+1}) = u_k + h$.
Line L10 is the linear interpolant of $u$ through these two points.
The error of linear interpolation of a $C^2$ function on an interval of length $\Delta$ is at most $\frac18\Delta^2\max|u''|$.
Here $\Delta = s_{k+1} - s_k \le h\,v_{\max}$, and $|u''| = |v'|/v^3 \le \max|v'|/v_{\min}^3$. $\square$

So the error is $O(h^2)$.
If $v$ is constant, $u'' = 0$ and line L10 is exact.

## Newton refinement

**Lemma 3.** Let $g(u) = s(u) - s^*$ and $e = u - u(s^*)$ for the current value $u$ in $[u_k, u_{k+1}]$.
One Newton step $u \leftarrow u - g(u)/v(u)$ gives a new error $e'$ with $|e'| \le \frac{\max|v'|}{2v_{\min}}e^2$.

*Proof.*
Write $u^\circ = u(s^*)$.
By Taylor's theorem, $0 = g(u^\circ) = g(u) - v(u)\,e + \frac12 v'(\xi)\,e^2$ for some $\xi$ between $u$ and $u^\circ$.
So $u - g(u)/v(u) - u^\circ = e - g(u)/v(u) = \frac{v'(\xi)}{2v(u)}e^2$. $\square$

Clamping $u$ to $[u_k, u_{k+1}]$ does not increase the error, because $u^\circ$ is in this interval.
With the start error $O(h^2)$ of Lemma 2, one step gives $O(h^4)$ and two steps $O(h^8)$.

## The quadrature error

**Lemma 4.** If each call of AGL on the interval $k$ returns its integral with the error $\delta_k$, then $|s_k - s(u_k)| \le \eta = \sum_j|\delta_j|$ for every $k$.
If $2\eta < h\,v_{\min}$, the value of lines L9 and L10 differs from the value with the exact table by at most $\eta/(v_{\min} - 2\eta/h)$.

*Proof.*
The first claim is the triangle inequality on the sum of line L4.
Let $F$ and $\tilde F$ be the piecewise linear functions of $u$ through the exact and the computed table values.
Lines L9 and L10 solve $\tilde F(u) = s^*$, and the exact table gives the root of $F(u) = s^*$.
On each interval, $\tilde F - F$ is a convex combination of two end differences, so $|\tilde F - F| \le \eta$.
The slope of $\tilde F$ on an interval is at least $(h\,v_{\min} - 2\eta)/h > 0$.
A function with this slope that is within $\eta$ of $F$ reaches $s^*$ within $\eta$ divided by the slope of the root of $F$. $\square$

The five-point Gauss-Legendre rule on an interval of length $\ell$ has the error $\frac{(5!)^4}{11\,(10!)^3}\,\ell^{11} f^{(10)}(\xi)$ for a $C^{10}$ integrand, so for a smooth curve $\delta_k$ is far below the interpolation error of Lemma 2.
The stopping test of line L7 compares two estimates and is a heuristic, not a bound; Lemma 4 holds with the true errors $\delta_k$.
