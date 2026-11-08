---
title: Order, solvability and convergence of the Adams-Moulton methods
proves: [correctness]
status: full
---

**Setting.** $y' = f(t, y)$ on $[t_0, T]$, $y \in \mathbb{R}^d$ with a norm $\|\cdot\|$, uniform grid $t_n = t_0 + nh$. The $k$-step Adams-Moulton method ($k \ge 0$) is
$$y_{n+1} = y_n + h\sum_{j=-1}^{k-1}\beta^*_jf_{n-j}, \qquad \beta^*_j = \int_0^1\ell^*_j(s)\,ds,$$
where $\ell^*_j$ is the Lagrange basis polynomial for the node $-j$ among the nodes $1, 0, -1, \dots, -(k-1)$.

## Lemma 1 (local truncation error)

Let $y \in C^{k+2}$ and $M_{k+2} = \max_t\|y^{(k+2)}(t)\|$. Define $\tau_{n+1} = y(t_{n+1}) - y(t_n) - h\sum_{j=-1}^{k-1}\beta^*_jy'(t_{n-j})$ and
$$\gamma^*_k = \int_0^1\frac{(s - 1)s(s + 1)\cdots(s + k - 1)}{(k + 1)!}\,ds.$$
Then $\|\tau_{n+1}\| \le |\gamma^*_k|M_{k+2}h^{k+2}$, and for $d = 1$, $\tau_{n+1} = \gamma^*_kh^{k+2}y^{(k+2)}(\xi)$ with $\xi \in (t_{n-k+1}, t_{n+1})$.

*Proof.* Let $P$ interpolate $y'$ at the $k + 1$ nodes $t_{n+1}, t_n, \dots, t_{n-k+1}$. Then $h\sum_j\beta^*_jy'(t_{n-j}) = \int_{t_n}^{t_{n+1}}P\,dt$, so $\tau_{n+1} = \int_{t_n}^{t_{n+1}}(y' - P)\,dt$. The interpolation error is $y'(t) - P(t) = w(t)\,y'[t_{n-k+1}, \dots, t_{n+1}, t]$ with $w(t) = \prod_{j=-1}^{k-1}(t - t_{n-j})$, and by the Hermite-Genocchi formula the divided difference is the average of $y^{(k+2)}/(k+1)!$ over a simplex, hence has norm at most $M_{k+2}/(k + 1)!$, and for $d = 1$ equals $y^{(k+2)}(\xi(t))/(k + 1)!$. On $[t_n, t_{n+1}]$ the factor $t - t_{n+1}$ is $\le 0$ and all other factors are $\ge 0$, so $w$ has constant sign. The bound follows by integrating $|w|$, and the scalar formula by the integral mean value theorem. With $t = t_n + sh$, $w = h^{k+1}(s - 1)s\cdots(s + k - 1)$ and $dt = h\,ds$. $\square$

In particular $\gamma^*_k < 0$, the method has order exactly $k + 1$, and it is [consistent](/consistency/). The tests check $C_0 = \dots = C_{k+1} = 0$ and $C_{k+2} = \gamma^*_k$ exactly with fractions for $k = 0, \dots, 5$, where $C_q = \frac{1}{q!}\big(\sum_i\alpha_ii^q - q\sum_i\beta_ii^{q-1}\big)$.

## Lemma 2 (unique solvability of the step)

Let $f$ be $L$-Lipschitz in $y$ and $h|\beta^*_{-1}|L < 1$. For any $g$, the equation $x = g + h\beta^*_{-1}f(t_{n+1}, x)$ has exactly one solution.

*Proof.* The map $\Psi(x) = g + h\beta^*_{-1}f(t_{n+1}, x)$ satisfies $\|\Psi(x) - \Psi(x')\| \le h|\beta^*_{-1}|L\|x - x'\|$, a contraction on the complete space $\mathbb{R}^d$. By the Banach fixed point theorem it has exactly one fixed point. $\square$

Newton's method, used in the implementation, converges to this solution from a close enough guess when $f$ has a Lipschitz continuous Jacobian and $I - h\beta^*_{-1}J$ is invertible at the solution; this is the standard local convergence theorem for Newton's method and is not reproved here.

## Lemma 3 (zero-stability)

For $k \ge 1$, $\rho(\zeta) = \zeta^{k-1}(\zeta - 1)$; for $k = 0$, $\rho(\zeta) = \zeta - 1$. The roots are 1 (simple) and possibly 0, so the root condition holds. $\square$

## Theorem (convergence)

Let $f$ be $L$-Lipschitz in $y$, $y \in C^{k+2}$, $h|\beta^*_{-1}|L \le \tfrac12$, $B^* = \sum_{j=-1}^{k-1}|\beta^*_j|$ and $\delta = \max_{m \le \max(k-1, 0)}\|e_m\|$. Then
$$\|e_n\| \le e^{2LB^*(t_n - t_0)}\big(\delta + 2|\gamma^*_k|M_{k+2}h^{k+1}(t_n - t_0)\big).$$

*Proof.* Subtracting the method from the identity satisfied by the exact solution,
$$e_{n+1} = e_n + h\beta^*_{-1}\big(f(t_{n+1}, y(t_{n+1})) - f(t_{n+1}, y_{n+1})\big) + h\sum_{j=0}^{k-1}\beta^*_j\big(f(t_{n-j}, y(t_{n-j})) - f(t_{n-j}, y_{n-j})\big) + \tau_{n+1}.$$
With $E_n = \max_{m \le n}\|e_m\|$, $a = h|\beta^*_{-1}|L$ and $B_0 = \sum_{j \ge 0}|\beta^*_j|$,
$$(1 - a)\|e_{n+1}\| \le (1 + hLB_0)E_n + \|\tau_{n+1}\|.$$
Since $a \le 1/2$, $1/(1 - a) \le 1 + 2a \le e^{2a}$ and $1/(1 - a) \le 2$, so $\|e_{n+1}\| \le e^{2hL|\beta^*_{-1}| + hLB_0}E_n + 2\|\tau_{n+1}\| \le e^{2hLB^*}E_n + 2|\gamma^*_k|M_{k+2}h^{k+2}$. The same bound holds for $E_{n+1}$. Induction from $E_{\max(k-1,0)} = \delta$ gives $E_n \le e^{2LB^*(t_n - t_0)}(\delta + 2n|\gamma^*_k|M_{k+2}h^{k+2})$, and $nh \le t_n - t_0$. $\square$

## Starting values

The implementation computes $y_1, \dots, y_{k-1}$ with RK4, so $\delta = O(h^5)$ when $f \in C^4$ (as shown on the Adams-Bashforth page). Hence the implementation converges with order $\min(k + 1, 5)$; for $k \le 4$ this is $k + 1$.

## Two special cases used in the tests

- *Exactness on polynomials.* If $y$ is a polynomial of degree at most $k + 1$, then $P = y'$, $\tau_{n+1} = 0$, and with exact starting values the method reproduces $y$. For $y' = t^3$ and $k = 3$ the RK4 starting values are exact too.
- *Energy of the trapezoidal rule.* For $y' = Sy$ with $S$ skew-symmetric, the trapezoidal step is $y_{n+1} = (I - \tfrac h2S)^{-1}(I + \tfrac h2S)y_n$, the Cayley transform of $\tfrac h2 S$, which is orthogonal. So $\|y_{n+1}\|_2 = \|y_n\|_2$ exactly in exact arithmetic.
