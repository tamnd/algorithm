---
title: Order, zero-stability and convergence of the Adams-Bashforth methods
proves: [correctness]
status: full
---

**Setting.** $y' = f(t, y)$ on $[t_0, T]$, $y \in \mathbb{R}^d$ with a norm $\|\cdot\|$, uniform grid $t_n = t_0 + nh$, $f_n = f(t_n, y_n)$. The $k$-step Adams-Bashforth method is
$$y_{n+1} = y_n + h\sum_{j=0}^{k-1}\beta_j f_{n-j}, \qquad \beta_j = \int_0^1 \ell_j(s)\,ds, \qquad \ell_j(s) = \prod_{m \ne j}\frac{s + m}{m - j}\quad(0 \le j, m \le k - 1).$$

## Lemma 1 (local truncation error)

Let $y$ be the exact solution, $y \in C^{k+1}$, and $M_{k+1} = \max_t\|y^{(k+1)}(t)\|$. The local truncation error
$$\tau_{n+1} = y(t_{n+1}) - y(t_n) - h\sum_{j=0}^{k-1}\beta_j\,y'(t_{n-j})$$
satisfies $\|\tau_{n+1}\| \le \gamma_k M_{k+1}h^{k+1}$, where $\gamma_k = \int_0^1 \frac{s(s+1)\cdots(s+k-1)}{k!}\,ds$. For $d = 1$, $\tau_{n+1} = \gamma_k h^{k+1}y^{(k+1)}(\xi)$ for some $\xi \in (t_{n-k+1}, t_{n+1})$.

*Proof.* Let $P$ be the polynomial of degree at most $k - 1$ that interpolates $y'$ at $t_n, t_{n-1}, \dots, t_{n-k+1}$. With $t = t_n + sh$, $P(t) = \sum_j \ell_j(s)\,y'(t_{n-j})$, so $h\sum_j\beta_jy'(t_{n-j}) = \int_{t_n}^{t_{n+1}}P(t)\,dt$, and
$$\tau_{n+1} = \int_{t_n}^{t_{n+1}}\big(y'(t) - P(t)\big)\,dt.$$
For $d = 1$ the interpolation error formula gives $y'(t) - P(t) = \frac{y^{(k+1)}(\xi(t))}{k!}\prod_{j=0}^{k-1}(t - t_{n-j})$. On $[t_n, t_{n+1}]$ every factor $t - t_{n-j}$ is nonnegative, so the product $w(t)$ does not change sign, and the integral mean value theorem gives $\tau_{n+1} = \frac{y^{(k+1)}(\xi)}{k!}\int_{t_n}^{t_{n+1}}w(t)\,dt$. Substituting $t = t_n + sh$, $w = h^k s(s+1)\cdots(s+k-1)$ and $dt = h\,ds$, which gives $\gamma_kh^{k+1}y^{(k+1)}(\xi)$. For $d > 1$, apply the scalar Hermite-Genocchi form componentwise in integral form: $y'(t) - P(t) = w(t)\,y'[t_{n-k+1}, \dots, t_n, t]$, and the divided difference of order $k$ of $y'$ is an average of $y^{(k+1)}/k!$ over a simplex, so its norm is at most $M_{k+1}/k!$. Integrating $|w|$ gives the bound. $\square$

The exact error constants $\gamma_1, \dots, \gamma_6 = \tfrac12, \tfrac5{12}, \tfrac38, \tfrac{251}{720}, \tfrac{95}{288}, \tfrac{19087}{60480}$ are checked in the tests in the equivalent form $C_{k+1} = \frac{1}{(k+1)!}\big(\sum_i\alpha_ii^{k+1} - (k+1)\sum_i\beta_ii^k\big)$, together with $C_0 = \dots = C_k = 0$.

## Lemma 2 (zero-stability)

$\rho(\zeta) = \zeta^k - \zeta^{k-1} = \zeta^{k-1}(\zeta - 1)$. Its roots are 1 (simple) and 0 (multiplicity $k - 1$), all in the closed unit disc with the only root on the circle simple. So the method satisfies the root condition. Moreover $\rho(1) = 0$ and $\rho'(1) = 1 = \sum_j\beta_j = \sigma(1)$ ($\sum_j\ell_j \equiv 1$), so it is [consistent](/consistency/). $\square$

By Dahlquist's equivalence theorem this already gives convergence. For the Adams family a direct proof with explicit constants is short.

## Theorem (convergence)

Assume $\|f(t, u) - f(t, v)\| \le L\|u - v\|$, $y \in C^{k+1}$, and let $B = \sum_j|\beta_j|$ and $\delta = \max_{0 \le m \le k-1}\|e_m\|$. Then for $k - 1 \le n \le N$
$$\|e_n\| \le e^{LB(t_n - t_0)}\,\delta + \frac{\gamma_kM_{k+1}h^k}{LB}\big(e^{LB(t_n - t_0)} - 1\big).$$

*Proof.* Subtracting the method from the identity $y(t_{n+1}) = y(t_n) + h\sum_j\beta_jf(t_{n-j}, y(t_{n-j})) + \tau_{n+1}$ gives
$$e_{n+1} = e_n + h\sum_j\beta_j\big(f(t_{n-j}, y(t_{n-j})) - f(t_{n-j}, y_{n-j})\big) + \tau_{n+1}.$$
Let $E_n = \max_{m \le n}\|e_m\|$. Then $\|e_{n+1}\| \le E_n + hLB\,E_n + \gamma_kM_{k+1}h^{k+1}$, and so $E_{n+1} \le (1 + hLB)E_n + \gamma_kM_{k+1}h^{k+1}$. Starting from $E_{k-1} = \delta$, induction gives
$$E_n \le (1 + hLB)^{n-k+1}\delta + \gamma_kM_{k+1}h^{k+1}\frac{(1 + hLB)^{n-k+1} - 1}{hLB},$$
and $(1 + hLB)^{m} \le e^{LBmh} \le e^{LB(t_n - t_0)}$. $\square$

## Starting values in the implementation

The implementation computes $y_1, \dots, y_{k-1}$ by $m \le k - 1$ steps of RK4. By the convergence proof for RK4 (on its own page), if $f \in C^4$ then $\|e_m\| \le Ch^4(e^{\Lambda mh} - 1)/\Lambda \le Cmh^5e^{\Lambda mh}$, since $e^x - 1 \le xe^x$. As $m < k$ is bounded, $\delta = O(h^5)$. Hence the implementation converges with order $\min(k, 5)$ when $f$ and $y$ are smooth enough; for $k \le 5$ this is order $k$.

## Exactness on polynomials

If $y$ is a polynomial of degree at most $k$, then $y'$ has degree at most $k - 1$, so $P = y'$ and $\tau_{n+1} = 0$. With exact starting values the method then reproduces $y$ up to rounding. For $y' = t^3$ and $k = 4$ the RK4 starting values are exact as well (Simpson's rule is exact for cubics), which the tests check.
