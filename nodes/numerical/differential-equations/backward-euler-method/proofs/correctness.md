---
title: The backward Euler step is well defined, has order 1, converges, and is A-stable and L-stable
proves: [correctness]
status: full
---

We use the notation of the page. $f : [t_0, T] \times \mathbb{R}^d \to \mathbb{R}^d$ is continuous, $\|\cdot\|$ is a vector norm, and the step is $y_{n+1} = y_n + h f(t_{n+1}, y_{n+1})$. We assume that each step equation is solved exactly; the Newton iteration of lines L6 to L10 only approximates this solution, and the proofs say nothing about its convergence for a general $f$.

**Lemma 1 (existence and uniqueness of the step).** Assume $\|f(t, u) - f(t, v)\| \le L \|u - v\|$ for all $t, u, v$, and $hL < 1$. Then for each $y_n$ the equation $Y = y_n + h f(t_{n+1}, Y)$ has exactly one solution.

*Proof.* The map $\Phi(Y) = y_n + h f(t_{n+1}, Y)$ satisfies $\|\Phi(u) - \Phi(v)\| \le hL \|u - v\|$, so it is a contraction of the complete space $\mathbb{R}^d$. The [Banach fixed-point theorem](/banach-fixed-point-theorem/) gives exactly one fixed point. $\square$

**Lemma 2 (contractivity under a one-sided condition).** Use the Euclidean inner product and norm. Assume $\langle f(t,u) - f(t,v), u - v \rangle \le \nu \|u - v\|_2^2$ for all $t, u, v$, with $h\nu < 1$. If $y_{n+1}$ and $z_{n+1}$ are backward Euler steps from $y_n$ and $z_n$ with the same $t_n$ and $h$, then $\|y_{n+1} - z_{n+1}\|_2 \le \|y_n - z_n\|_2 / (1 - h\nu)$.

*Proof.* Let $\Delta = y_{n+1} - z_{n+1}$ and $\delta = y_n - z_n$. Subtracting the two step equations gives $\Delta = \delta + h\,(f(t_{n+1}, y_{n+1}) - f(t_{n+1}, z_{n+1}))$. Take the inner product with $\Delta$:
$$\|\Delta\|_2^2 = \langle \delta, \Delta \rangle + h \langle f(t_{n+1}, y_{n+1}) - f(t_{n+1}, z_{n+1}), \Delta \rangle \le \|\delta\|_2 \|\Delta\|_2 + h\nu \|\Delta\|_2^2,$$
by the Cauchy-Schwarz inequality and the hypothesis. So $(1 - h\nu)\|\Delta\|_2^2 \le \|\delta\|_2 \|\Delta\|_2$. If $\Delta = 0$ the claim holds. Otherwise divide by $\|\Delta\|_2 > 0$; since $1 - h\nu > 0$, the claim follows. $\square$

With $\nu \le 0$ the factor $1/(1 - h\nu)$ is at most 1 for every $h > 0$. This also gives uniqueness of the step without any bound on $hL$: two solutions of the same step equation have $\delta = 0$, so $\Delta = 0$.

**Lemma 3 (local truncation error).** Assume the exact solution $y$ is $C^2$ on $[t_0, T]$ and let $M_2 = \max_t \|y''(t)\|$. Define $\tau_{n+1} = y(t_{n+1}) - y(t_n) - h f(t_{n+1}, y(t_{n+1}))$. Then $\|\tau_{n+1}\| \le M_2 h^2 / 2$.

*Proof.* Since $y' = f(t, y)$, $\tau_{n+1} = y(t_{n+1}) - y(t_n) - h y'(t_{n+1})$. Taylor's formula with integral remainder, expanded at $t_{n+1}$, gives
$$y(t_n) = y(t_{n+1}) - h y'(t_{n+1}) + \int_{t_n}^{t_{n+1}} (s - t_n)\, y''(s)\, ds.$$
So $\tau_{n+1} = -\int_{t_n}^{t_{n+1}} (s - t_n) y''(s)\, ds$, and $\|\tau_{n+1}\| \le M_2 \int_{t_n}^{t_{n+1}} (s - t_n)\, ds = M_2 h^2/2$. $\square$

For a scalar $y \in C^3$ the same expansion gives $\tau_{n+1} = -\tfrac{h^2}{2} y''(t_{n+1}) + O(h^3)$, so the error constant is $-1/2$ and the order is exactly 1 when $y'' \ne 0$.

**Theorem 1 (convergence).** Assume $f$ is continuous and $L$-Lipschitz in $y$ with $L > 0$, $y \in C^2$, $hL \le 1/2$, $t_n = t_0 + nh \le T$, and $e_0 = y(t_0) - y_0 = 0$. Then
$$\|e_n\| \le \frac{M_2 h}{2L}\left(e^{2L(t_n - t_0)} - 1\right).$$

*Proof.* By Lemma 1 the steps exist. Subtract $y_{n+1} = y_n + hf(t_{n+1}, y_{n+1})$ from $y(t_{n+1}) = y(t_n) + hf(t_{n+1}, y(t_{n+1})) + \tau_{n+1}$:
$$e_{n+1} = e_n + h\,(f(t_{n+1}, y(t_{n+1})) - f(t_{n+1}, y_{n+1})) + \tau_{n+1}.$$
Take norms and use the Lipschitz condition and Lemma 3: $\|e_{n+1}\| \le \|e_n\| + hL\|e_{n+1}\| + M_2h^2/2$. Since $hL < 1$, with $q = 1/(1 - hL)$,
$$\|e_{n+1}\| \le q\|e_n\| + q\, M_2 h^2/2.$$
By induction on $n$, with $e_0 = 0$, $\|e_n\| \le (M_2h^2/2)(q + q^2 + \dots + q^n) = (M_2h^2/2)\, q(q^n - 1)/(q - 1)$. Here $q - 1 = hL/(1 - hL) = hLq$, so $q(q^n - 1)/(q-1) = (q^n - 1)/(hL)$ and $\|e_n\| \le (M_2 h/(2L))(q^n - 1)$. Finally, for $0 \le x \le 1/2$, $-\ln(1 - x) = \sum_{k \ge 1} x^k/k \le x \sum_{k \ge 0} x^k = x/(1-x) \le 2x$, so $q = 1/(1 - hL) \le e^{2hL}$ and $q^n \le e^{2nhL} = e^{2L(t_n - t_0)}$. $\blacksquare$

The last step of the implementation is shorter than $h$ when $T - t_0$ is not a multiple of $h$. The same proof applies with a variable step $h_n \le h$, since each $h_n$ also satisfies $h_n L \le 1/2$ and $\|\tau_{n+1}\| \le M_2 h_n^2/2 \le M_2 h h_n/2$; the sum then gives the same bound with $t_n - t_0 = \sum h_k$.

**Theorem 2 (linear stability).** On $y' = \lambda y$ with $\lambda \in \mathbb{C}$ and $z = h\lambda \ne 1$, the step is $y_{n+1} = R(z) y_n$ with $R(z) = 1/(1 - z)$. If $\operatorname{Re} z \le 0$ then $|R(z)| \le 1$, so the method is A-stable. Also $R(z) \to 0$ as $|z| \to \infty$, so it is L-stable.

*Proof.* The step equation is $y_{n+1} = y_n + z\, y_{n+1}$, so $(1 - z) y_{n+1} = y_n$. If $\operatorname{Re} z \le 0$ then $|1 - z| \ge \operatorname{Re}(1 - z) = 1 - \operatorname{Re} z \ge 1$, so $|R(z)| \le 1$. And $|R(z)| = 1/|1 - z| \le 1/(|z| - 1)$ for $|z| > 1$, which tends to 0. $\blacksquare$

**Newton on a linear problem.** When $f(t, y) = A(t) y + g(t)$, the residual $G(Y) = (I - hA(t_{n+1}))Y - y_n - h g(t_{n+1})$ is affine with Jacobian $I - hA(t_{n+1})$, so one Newton step from any start gives the exact root (when the matrix is invertible). The loop of lines L6 to L10 then stops after the second iteration, whose correction is zero up to rounding.
