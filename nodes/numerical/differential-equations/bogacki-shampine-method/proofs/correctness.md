---
title: Orders, error estimate and termination of the Bogacki-Shampine 3(2) pair
proves: [correctness]
status: full
---

**Setting.** $y' = f(t, y)$, $y \in \mathbb{R}^d$ with a norm $\|\cdot\|$. One step from $(t, y)$ with size $h$ uses the stages $k_j = f(t + c_jh, y + h\sum_{l<j}a_{jl}k_l)$ of the tableau on the page. It gives $y_{n+1} = y + h\sum b_jk_j$, $\hat y_{n+1} = y + h\sum\hat b_jk_j$ and $\mathrm{est} = y_{n+1} - \hat y_{n+1}$. For an exact solution through $(t, y)$, the local errors are $\tau = y(t + h) - y_{n+1}$ and $\hat\tau = y(t + h) - \hat y_{n+1}$.

## Lemma 1 (order conditions, checked exactly)

The row sums satisfy $c_j = \sum_l a_{jl}$. For $b = (2/9, 1/3, 4/9, 0)$, with $Ac = (0, 0, 3/8, 1/2)$:

| tree | condition | value for $b$ | value for $\hat b$ |
|---|---|---|---|
| order 1 | $\sum b_i = 1$ | $1$ | $1$ |
| order 2 | $\sum b_ic_i = 1/2$ | $1/2$ | $1/2$ |
| order 3 | $\sum b_ic_i^2 = 1/3$ | $1/3$ | $3/8$ |
| order 3 | $\sum b_i(Ac)_i = 1/6$ | $1/6$ | $3/16$ |
| order 4 | $\sum b_ic_i^3 = 1/4$ | $11/48$ | |
| order 4 | $\sum b_ic_i(Ac)_i = 1/8$ | $1/8$ | |
| order 4 | $\sum b_i(Ac^2)_i = 1/12$ | $1/12$ | |
| order 4 | $\sum b_i(A^2c)_i = 1/24$ | $0$ | |

Each entry is a finite sum of fractions, computed exactly by the tests. By Butcher's order condition theorem, if $f$ is $C^p$ near the solution, a Runge-Kutta method has local error $O(h^{p+1})$ exactly when the conditions for all trees with at most $p$ vertices hold. If one condition of order $p + 1$ fails, the $h^{p+1}$ term does not vanish for every $f$. Hence $y_{n+1}$ has order exactly 3 and $\hat y_{n+1}$ has order exactly 2. $\square$

The fourth row of $A$ equals $b$, so $k_4 = f(t + h, y_{n+1})$. That is the first stage of the next step from $(t + h, y_{n+1})$.

## Lemma 2 (the estimate is asymptotically the local error of the order-2 solution)

Let $f$ be $C^3$ near the solution. Then $\mathrm{est} = \hat\tau - \tau$ with $\tau = O(h^4)$ and $\hat\tau = O(h^3)$. So $\mathrm{est} = \hat\tau + O(h^4)$. When the leading term $\hat\tau = h^3\Psi(t, y) + O(h^4)$ has $\Psi \ne 0$, $\|\mathrm{est}\|/\|\hat\tau\| \to 1$ as $h \to 0$.

*Proof.* $\mathrm{est} = y_{n+1} - \hat y_{n+1} = (y(t + h) - \hat y_{n+1}) - (y(t + h) - y_{n+1}) = \hat\tau - \tau$. Lemma 1 gives the orders. $\square$

So, for small $h$, the scaled test $\mathrm{err} \le 1$ bounds the local error of $\hat y$, which is larger than that of the value kept by a factor of order $1/h$. The tests check that halving $h$ divides the estimate by about 8.

## Lemma 3 (stability function)

On $y' = \lambda y$ with $z = h\lambda$, an explicit method gives $y_{n+1} = R(z)y_n$ with $R(z) = 1 + z\,b^T(I - zA)^{-1}\mathbf 1 = \sum_{q \ge 0}z^{q+1}b^TA^q\mathbf 1$. Because $b_4 = 0$ and the first three stages form an explicit 3-stage method, $b^TA^q\mathbf 1 = 0$ for $q \ge 3$. The order conditions give $b^T\mathbf 1 = 1$, $b^Tc = 1/2$ and $b^TAc = 1/6$. Hence $R(z) = 1 + z + z^2/2 + z^3/6$. For real $x < 0$, $R(x) > -1$ exactly when $x > x^*$, where $x^* \approx -2.5127$ is the real root of $R(x) = -1$. For $x < 0$, $R(x) < 1$ always, since $R(x) - 1 = x(1 + x/2 + x^2/6)$ and the quadratic has no real roots. On the imaginary axis, $|R(iy)|^2 = (1 - y^2/2)^2 + (y - y^3/6)^2 = 1 - y^4/12 + y^6/36$, which is at most 1 exactly when $y^2 \le 3$. $\square$

## Lemma 4 (termination of the loop)

Assume the stages are defined and $\|\mathrm{est}\| \le Kh^3$ for $h \le h_0$, uniformly near the solution. A rejected step has $\mathrm{err} > 1$, so the next attempt uses a factor $\min(1, 0.9\,\mathrm{err}^{-1/3}) \le 0.9$. After $m$ consecutive rejections, $h \le 0.9^mh_{\mathrm{first}}$. Once $Kh^3 \le \min_i(\mathrm{atol} + \mathrm{rtol}\cdot|y_i|)$, the step is accepted. This bound is positive when $\mathrm{atol} > 0$. Hence each point is left after finitely many attempts. Each accepted step advances $t$ by $h$. When $t + h \ge T$, line L3 sets $h = T - t$, so that step, once accepted, ends exactly at $T$. With a positive lower bound on the step sizes, which holds for fixed tolerances on a smooth problem, the number of accepted steps is finite. The implementation enforces termination anyway with a maximum number of attempts. $\square$

## Convergence with fixed steps

Let $f$ be $L$-Lipschitz in $y$. The increment $\Phi(t, y, h) = \sum b_jk_j$ is Lipschitz in $y$ with constant $\Lambda = L(1 + \tfrac12hL + \tfrac16(hL)^2)$. Here $k_4$ has weight 0, and the nested Lipschitz bounds give $\|k_2 - k_2'\| \le L(1 + \tfrac h2L)\|y - y'\|$ and $\|k_3 - k_3'\| \le L(1 + \tfrac{3h}{4}L(1 + \tfrac h2L))\|y - y'\|$. Weighting with $b$ gives a constant at most $L(1 + \tfrac12hL + \tfrac16(hL)^2)$. If also $\|\tau\| \le Ch^4$ on each step, the standard one-step argument gives $\|e_n\| \le Ch^3(e^{\Lambda(t_n - t_0)} - 1)/\Lambda$. This is the observed order 3 in the fixed-step table. $\square$

## FSAL count

Each attempt evaluates $k_2$, $k_3$ and $k_4$. After an acceptance, $k_1 \leftarrow k_4$ is the derivative at the new point, so no evaluation is needed. After a rejection, $(t, y)$ and therefore $k_1$ are unchanged. With the initial $k_1$, the total is $1 + 3$ times the number of attempts. The tests check this identity exactly.
