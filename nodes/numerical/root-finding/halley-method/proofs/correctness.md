---
title: Correctness of Halley's method
proves: [correctness, termination, convergence-rate]
status: full
---

We use the notation of the page: $e_k = x_k - x^*$, and at a simple root $c_j = f^{(j)}(x^*)/(j!\,f'(x^*))$. The step is $s(x) = 2f(x)f'(x)/D(x)$ with $D = 2f'^2 - ff''$, and $x_{k+1} = x_k - s(x_k)$. All results below are in exact arithmetic unless stated otherwise.

## Termination

Each pass of the loop L1 either returns at L3, L4, L5 or L7, or ends with $k$ increased by one. After $K$ passes the loop exits and L8 returns. So the procedure stops after at most $K$ passes and at most $3K$ evaluations (one each of $f$, $f'$, $f''$ per pass). Non-finite values stop it at L2 with an error. No status claims more than its test shows: "exact" means $f(x) = 0$ was computed; "converged" means the step was small; "stalled" means $s = 0$ while $f(x) \ne 0$ and $D \ne 0$, which forces $f'(x) = 0$ (or an underflow in the product $2ff'$).

## Lemma 1 (Newton's method on a transformed function)

Let $f'(x) \ne 0$ on an interval and $g = f/\sqrt{|f'|}$. Then $g/g' = s$ on that interval, so Halley's method is Newton's method on $g$. If $f \in C^3$ and $x^*$ is a simple root, then $g''(x^*) = 0$.

*Proof.* The derivative of $|f'|^{-1/2}$ is $-\tfrac12 f''/(f'|f'|^{1/2})$, so
$$g' = |f'|^{-1/2}\Bigl(f' - \frac{ff''}{2f'}\Bigr) = \frac{2f'^2 - ff''}{2f'|f'|^{1/2}},$$
and $g/g' = 2ff'/(2f'^2 - ff'') = s$. Differentiating $g'$ once more and putting $f(x^*) = 0$: the derivative of $f' - ff''/(2f')$ at $x^*$ is $f'' - f'f''/(2f') = f''/2$, and the derivative of the factor $|f'|^{-1/2}$ times $f'$ gives $-\tfrac12 f''/|f'|^{1/2}$. The sum is $g''(x^*) = |f'|^{-1/2}(f''/2 - f''/2) = 0$. $\square$

Newton's error constant is $g''/(2g')$, so Newton on $g$ loses its quadratic term; this is the reason for the cubic order. Theorem 1 proves it directly and gives the constant.

## Theorem 1 (cubic local convergence at a simple root)

Let $f \in C^3$ on a neighbourhood of $x^*$, $f(x^*) = 0 \ne f'(x^*)$, and $C = c_2^2 - c_3$. Then $e_{k+1} = C e_k^3 + o(e_k^3)$, and there is $\rho > 0$ such that from every $x_0$ with $|e_0| \le \rho$ the iterates are defined, stay in $[x^* - \rho, x^* + \rho]$, converge to $x^*$, and satisfy $e_{k+1}/e_k^3 \to C$ when no $e_k$ is $0$.

*Proof.* By Taylor's theorem with Peano remainder, writing $e = x - x^*$ and dividing by $f'(x^*)$,
$$\frac{f}{f'(x^*)} = e + c_2e^2 + c_3e^3 + o(e^3),\quad \frac{f'}{f'(x^*)} = 1 + 2c_2e + 3c_3e^2 + o(e^2),\quad \frac{f''}{f'(x^*)} = 2c_2 + 6c_3e + o(e).$$
Multiplying out,
$$\frac{2ff'}{f'(x^*)^2} = 2e + 6c_2e^2 + (4c_2^2 + 8c_3)e^3 + o(e^3),$$
$$\frac{2f'^2}{f'(x^*)^2} = 2 + 8c_2e + (8c_2^2 + 12c_3)e^2 + o(e^2),\qquad \frac{ff''}{f'(x^*)^2} = 2c_2e + (2c_2^2 + 6c_3)e^2 + o(e^2),$$
so $D/f'(x^*)^2 = 2 + 6c_2e + (6c_2^2 + 6c_3)e^2 + o(e^2)$. The numerator of $s/e$ and the denominator agree up to first order in $e$ and differ by $(2c_3 - 2c_2^2)e^2 + o(e^2)$ at second order, so
$$\frac{s}{e} = 1 + \frac{(2c_3 - 2c_2^2)e^2 + o(e^2)}{2 + O(e)} = 1 + (c_3 - c_2^2)e^2 + o(e^2).$$
Hence $e_{k+1} = e - s = (c_2^2 - c_3)e^3 + o(e^3)$.

For the ball: $D(x^*) = 2f'(x^*)^2 > 0$ and $D$ is continuous, so $D > 0$ on some $[x^* - \rho_1, x^* + \rho_1]$ and the step is defined there. By the expansion there is $\rho_2$ with $|e - s| \le (|C| + 1)|e|^3$ for $|e| \le \rho_2$. Take $\rho = \min(\rho_1, \rho_2, (2(|C| + 1))^{-1/2})$. If $|e_k| \le \rho$ then $|e_{k+1}| \le (|C| + 1)\rho^2 |e_k| \le |e_k|/2$, so by induction all iterates stay in the ball and $|e_k| \le 2^{-k}\rho \to 0$. If some $e_k = 0$ then $f(x_k) = 0$ and the method stops there (L3). Otherwise the expansion gives $e_{k+1}/e_k^3 \to C$. $\square$

So the order is at least 3, exactly 3 when $c_2^2 \ne c_3$, and higher on the special functions with $c_2^2 = c_3$. This is a local result: nothing is claimed for starts outside the ball, whose size depends on $f$.

## Corollary (the stopping test)

In the ball of Theorem 1, $e_k = s_k + e_{k+1}$ with $|e_{k+1}| \le (|C| + 1)|e_k|^3 \le |e_k|/2$, so $|e_k| \le 2|s_k|$ and $|e_{k+1}| \le 8(|C| + 1)|s_k|^3$. When L7 fires with $|s_k| \le \delta(1 + |x_{k+1}|)$, the returned point therefore has error far below $\delta(1 + |x|)$ in exact arithmetic. Outside the ball a small step proves nothing.

## Theorem 2 (multiple roots)

Let $f(x) = (x - x^*)^m h(x)$ with $m \ge 2$, $h \in C^2$ near $x^*$ and $h(x^*) \ne 0$. Then $e_{k+1} = \frac{m - 1}{m + 1}e_k + O(e_k^2)$, and the iteration converges linearly to $x^*$ from every start close enough to $x^*$.

*Proof.* With $e = x - x^*$,
$$f' = e^{m-1}(mh + eh'),\qquad f'' = e^{m-2}\bigl(m(m-1)h + 2meh' + e^2h''\bigr).$$
Then $2ff' = 2e^{2m-1}h(mh + eh')$ and
$$D = e^{2m-2}\bigl(2(mh + eh')^2 - h(m(m-1)h + 2meh' + e^2h'')\bigr) = e^{2m-2}\bigl(m(m+1)h^2 + 2mehh' + O(e^2)\bigr),$$
where the $O(e^2)$ is uniform because $h, h', h''$ are bounded near $x^*$. Since $h(x^*) \ne 0$, $D \ne 0$ for small $e \ne 0$, and
$$s = e\,\frac{2mh^2 + 2ehh'}{m(m+1)h^2 + 2mehh' + O(e^2)} = \frac{2e}{m+1}\cdot\frac{1 + eh'/(mh)}{1 + 2eh'/((m+1)h) + O(e^2)} = \frac{2e}{m+1}\bigl(1 + O(e)\bigr).$$
So $e_{k+1} = e - s = \frac{m-1}{m+1}e + O(e^2)$. With $r = (m - 1)/(m + 1) < 1$, choose $\rho$ so small that $D \ne 0$ and $|e - s| \le \frac{1 + r}{2}|e|$ for $0 < |e| \le \rho$; then $|e_k| \le (\frac{1+r}{2})^k \rho \to 0$, and $e_{k+1}/e_k \to r$. Since $h \ne 0$ near $x^*$, $f(x_k) \ne 0$ for every $x_k \ne x^*$ in the ball. $\square$

For $f = x^m$ the $O(e^2)$ term vanishes ($h = 1$) and $x_{k+1} = \frac{m-1}{m+1}x_k$ exactly; for $m = 3$ the iterates halve, as the tests check. Halley's method applied to $F = f^{1/m}$, which has a simple root, gives the step $f/\bigl(\frac{m+1}{2m}f' - \frac{ff''}{2f'}\bigr)$, and Theorem 1 applied to $F$ shows that this modified step has order 3 when $m$ is known.

## Floating point

The theorems are about exact arithmetic. In floating point the computed $f$ near a simple root is dominated by rounding once $|e| \lesssim u\,\mathrm{cond}$, and the iteration then either hits a computed zero of $f$ (status "exact") or takes steps of the size of the rounding noise, which the relative test at L7 accepts. At a root of multiplicity $m$ the attainable error is of order $u^{1/m}$ relative to the scale of $f$, and the step test may fire there or the loop may reach $K$. These floating point statements are observations on the test functions, not theorems.
