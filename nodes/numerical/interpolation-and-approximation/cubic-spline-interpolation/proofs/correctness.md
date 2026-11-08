---
title: Cubic spline interpolation is well defined, the moment system is solved without pivoting, and the result is the unique C^2 cubic spline interpolant
proves: [correctness, termination, uniqueness]
status: full
---

We use the notation of the page: increasing knots $x_0 < \cdots < x_n$ with $n \ge 1$, values $y_k$, $h_k = x_{k+1} - x_k > 0$, $\delta_k = (y_{k+1} - y_k)/h_k$, and the moments $M_0, \ldots, M_n$. On $[x_k, x_{k+1}]$ let $a = x_{k+1} - t$, $b = t - x_k$, so $a + b = h_k$, and
$$P_k(t) = \frac{M_k a^3 + M_{k+1} b^3}{6 h_k} + \Big(\frac{y_k}{h_k} - \frac{M_k h_k}{6}\Big) a + \Big(\frac{y_{k+1}}{h_k} - \frac{M_{k+1} h_k}{6}\Big) b.$$

## Claim 1: for any moments, the pieces interpolate and are C^2 across knots

$P_k$ is a cubic in $t$ since $a$ and $b$ are linear in $t$, with $da/dt = -1$ and $db/dt = 1$. At $t = x_k$ we have $a = h_k$, $b = 0$, and $P_k(x_k) = M_k h_k^2/6 + y_k - M_k h_k^2/6 = y_k$. Symmetrically $P_k(x_{k+1}) = y_{k+1}$. Differentiating twice, $P_k''(t) = (M_k a + M_{k+1} b)/h_k$, so $P_k''(x_k) = M_k$ and $P_k''(x_{k+1}) = M_{k+1}$. Hence the function $s$ equal to $P_k$ on $[x_k, x_{k+1}]$ is well defined at the knots, interpolates, and has continuous second derivative.

## Claim 2: continuity of s' is equivalent to the interior rows

Differentiating once,
$$P_k'(t) = \frac{-M_k a^2 + M_{k+1} b^2}{2 h_k} + \delta_k + \frac{(M_k - M_{k+1}) h_k}{6}.$$
At $t = x_{k+1}$ ($a = 0$, $b = h_k$) this is $\delta_k + h_k(M_k + 2M_{k+1})/6$. At $t = x_k$ ($a = h_k$, $b = 0$) it is $\delta_k - h_k(2M_k + M_{k+1})/6$. So $P_{k-1}'(x_k) = P_k'(x_k)$ holds if and only if
$$\delta_{k-1} + \frac{h_{k-1}(M_{k-1} + 2M_k)}{6} = \delta_k - \frac{h_k(2M_k + M_{k+1})}{6},$$
which, multiplied by 6, is row $k$ of line L3: $h_{k-1} M_{k-1} + 2(h_{k-1} + h_k) M_k + h_k M_{k+1} = 6(\delta_k - \delta_{k-1})$. The clamped conditions $P_0'(x_0) = d_a$ and $P_{n-1}'(x_n) = d_b$ are, by the same two formulas, $2h_0 M_0 + h_0 M_1 = 6(\delta_0 - d_a)$ and $h_{n-1} M_{n-1} + 2h_{n-1} M_n = 6(d_b - \delta_{n-1})$, the rows of line L4. The natural conditions $s''(x_0) = M_0 = 0$, $s''(x_n) = M_n = 0$ are the identity rows of line L2.

Conversely, every $C^2$ piecewise cubic $g$ with $g(x_k) = y_k$ equals the $s$ built from its own moments $M_k = g''(x_k)$: on each interval $g''$ is linear with end values $M_k, M_{k+1}$, so $g - P_k$ has zero second derivative and vanishes at both ends, hence is zero. So the spline interpolants (natural or clamped) correspond exactly to solutions of the system of lines L2 to L4.

## Claim 3: the system is strictly diagonally dominant by rows, hence uniquely solvable

Write the system as $T M = r$ with $T$ tridiagonal, subdiagonal $\ell_k$, diagonal $d_k$, superdiagonal $u_k$. For an interior row $|d_k| = 2(h_{k-1} + h_k) > h_{k-1} + h_k = |\ell_k| + |u_k|$. A clamped end row has $2h_0 > h_0$ or $2h_{n-1} > h_{n-1}$, and a natural end row is $(0, 1, 0)$ with $1 > 0$. A strictly diagonally dominant matrix is nonsingular: if $Tv = 0$ with $v \ne 0$, pick $i$ with $|v_i| = \|v\|_\infty$; then $|d_i||v_i| = |\ell_i v_{i-1} + u_i v_{i+1}| \le (|\ell_i| + |u_i|)|v_i| < |d_i||v_i|$, a contradiction. So by Claim 2 there is exactly one natural and exactly one clamped cubic spline interpolant. For $n = 1$ the natural spline is the chord and the clamped spline is the cubic Hermite interpolant on one interval.

## Claim 4: the Thomas algorithm in line L5 never divides by zero and computes the solution

Forward elimination replaces $d_k$ by $d_k' = d_k - (\ell_k / d_{k-1}') u_{k-1}$ for $k = 1, \ldots, n$, with $d_0' = d_0$. We show by induction that $|d_k'| > |u_k|$ (with $u_n = 0$) and $d_k' \ne 0$. For $k = 0$ this is diagonal dominance of row 0. If $|d_{k-1}'| > |u_{k-1}|$, then
$$|d_k'| \ge |d_k| - |\ell_k| \frac{|u_{k-1}|}{|d_{k-1}'|} > |d_k| - |\ell_k| \ge |u_k| \ge 0$$
when $\ell_k \ne 0$, and $|d_k'| = |d_k| > |u_k|$ when $\ell_k = 0$. So every pivot is nonzero. Forward elimination is Gaussian elimination without row exchanges, which applies the same row operations to $r$ and turns the system into an equivalent upper bidiagonal one with diagonal $d_k'$ and superdiagonal $u_k$; back substitution solves it exactly in exact arithmetic. So line L5 returns the unique $M$ of Claim 3.

## Claim 5: termination and evaluation

Lines L1 to L5 are loops with fixed bounds, about $15n$ operations in all. Line L6 is a binary search over $n + 1$ sorted knots, and the clamp puts $k$ in $\{0, \ldots, n - 1\}$; for $t \in [x_0, x_n)$ it is the index with $x_k \le t < x_{k+1}$, and $t = x_n$ gives $k = n - 1$, which is right because $P_{n-1}(x_n) = y_n$. Lines L7 to L9 evaluate $P_k(t)$ as written in Claim 1, with $h_k > 0$ since the knots are distinct. For $t$ outside $[x_0, x_n]$ the same end cubic is extended, as the problem states.

## Claim 6: polynomial reproduction

If $y_k = q(x_k)$ for a cubic $q$ and the clamped slopes are $q'(x_0)$ and $q'(x_n)$, then $q$ itself is a $C^2$ cubic spline satisfying all the conditions, so by uniqueness (Claim 3) the algorithm returns $q$. If $q$ is linear, $q'' = 0$ satisfies the natural conditions too, so the natural spline also returns $q$.
