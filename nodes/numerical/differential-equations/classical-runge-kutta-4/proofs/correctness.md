---
title: Order and convergence of the classical Runge-Kutta method
proves: [correctness]
status: full
---

**Setting.** $y' = f(t, y)$ on $[t_0, T]$, $y(t_0) = y_0$, $y \in \mathbb{R}^d$, with $\|\cdot\|$ any norm on $\mathbb{R}^d$. One step of RK4 with step $h$ is $y_{n+1} = y_n + h\Phi(t_n, y_n, h)$, where
$$\Phi(t, y, h) = \tfrac16(k_1 + 2k_2 + 2k_3 + k_4),$$
$$k_1 = f(t, y),\ k_2 = f(t + \tfrac h2, y + \tfrac h2 k_1),\ k_3 = f(t + \tfrac h2, y + \tfrac h2 k_2),\ k_4 = f(t + h, y + hk_3).$$
The local error of step $n$ is $\tau_{n+1} = y(t_{n+1}) - y(t_n) - h\Phi(t_n, y(t_n), h)$, and the global error is $e_n = y(t_n) - y_n$.

## Lemma 1 (order conditions)

The tableau $c = (0, \tfrac12, \tfrac12, 1)$, $a_{21} = a_{32} = \tfrac12$, $a_{43} = 1$ (other $a_{ij} = 0$), $b = (\tfrac16, \tfrac13, \tfrac13, \tfrac16)$ satisfies the row-sum condition $c_i = \sum_j a_{ij}$ and the eight order conditions for the rooted trees with at most four vertices, and it fails one condition of order 5.

*Proof.* The row sums are $0, \tfrac12, \tfrac12, 1$. Direct computation with exact fractions:

| tree order | condition | value |
|---|---|---|
| 1 | $\sum b_i = 1$ | $\tfrac16 + \tfrac13 + \tfrac13 + \tfrac16 = 1$ |
| 2 | $\sum b_ic_i = \tfrac12$ | $\tfrac16 + \tfrac16 + \tfrac16 = \tfrac12$ |
| 3 | $\sum b_ic_i^2 = \tfrac13$ | $\tfrac1{12} + \tfrac1{12} + \tfrac16 = \tfrac13$ |
| 3 | $\sum b_ia_{ij}c_j = \tfrac16$ | $b_3a_{32}c_2 + b_4a_{43}c_3 = \tfrac1{12} + \tfrac1{12} = \tfrac16$ |
| 4 | $\sum b_ic_i^3 = \tfrac14$ | $\tfrac1{24} + \tfrac1{24} + \tfrac16 = \tfrac14$ |
| 4 | $\sum b_ic_ia_{ij}c_j = \tfrac18$ | $b_3c_3a_{32}c_2 + b_4c_4a_{43}c_3 = \tfrac1{24} + \tfrac1{12} = \tfrac18$ |
| 4 | $\sum b_ia_{ij}c_j^2 = \tfrac1{12}$ | $b_3a_{32}c_2^2 + b_4a_{43}c_3^2 = \tfrac1{24} + \tfrac1{24} = \tfrac1{12}$ |
| 4 | $\sum b_ia_{ij}a_{jk}c_k = \tfrac1{24}$ | $b_4a_{43}a_{32}c_2 = \tfrac16 \cdot 1 \cdot \tfrac12 \cdot \tfrac12 = \tfrac1{24}$ |

For order 5 the condition $\sum b_ic_i^4 = \tfrac15$ fails: $\tfrac13 \cdot \tfrac1{16} \cdot 2 + \tfrac16 = \tfrac5{24}$. $\square$

By the order condition theorem for Runge-Kutta methods (Butcher 1963; Hairer, Nørsett and Wanner, Section II.2), a method whose tableau satisfies the conditions of all trees with at most $p$ vertices has order $p$: if $f$ is $C^p$ in a neighbourhood of the solution, then $\|\tau_{n+1}\| \le Ch^{p+1}$ for $h \le h_0$, with $C$ depending on bounds for the derivatives of $f$ up to order $p$ near the solution. So RK4 has order 4. Because a condition of order 5 fails, there are smooth problems (for example $y' = t^4$, where $\Phi$ is Simpson's rule) with $\tau_{n+1}$ exactly of size $h^5$ and not smaller.

*Check on $y' = t^4$.* With $f$ independent of $y$, $h\Phi(t, y, h) = \tfrac h6(t^4 + 4(t + \tfrac h2)^4 + (t + h)^4)$, Simpson's rule, whose error for $\int_t^{t+h}s^4\,ds$ is $-\tfrac{h^5}{2880}\cdot 4! = -\tfrac{h^5}{120}$. So $\tau_{n+1} = -h^5/120 \ne 0$.

## Lemma 2 (Lipschitz constant of the increment)

If $\|f(t, u) - f(t, v)\| \le L\|u - v\|$ for all $t, u, v$, then for $h \ge 0$
$$\|\Phi(t, u, h) - \Phi(t, v, h)\| \le \Lambda\|u - v\|, \qquad \Lambda = L\Big(1 + \frac{hL}{2} + \frac{(hL)^2}{6} + \frac{(hL)^3}{24}\Big).$$

*Proof.* Write $k_i, k_i'$ for the stages at $u$ and $v$, and $\delta = \|u - v\|$. Then $\|k_1 - k_1'\| \le L\delta$. Next, $\|k_2 - k_2'\| \le L(\delta + \tfrac h2 L\delta) = L\delta(1 + \tfrac{hL}2)$. Then $\|k_3 - k_3'\| \le L(\delta + \tfrac h2\|k_2 - k_2'\|) \le L\delta(1 + \tfrac{hL}2 + \tfrac{(hL)^2}4)$. Finally $\|k_4 - k_4'\| \le L(\delta + h\|k_3 - k_3'\|) \le L\delta(1 + hL + \tfrac{(hL)^2}2 + \tfrac{(hL)^3}4)$. So
$$\|\Phi(t,u,h) - \Phi(t,v,h)\| \le \frac{L\delta}{6}\Big(1 + 2(1 + \tfrac{hL}2) + 2(1 + \tfrac{hL}2 + \tfrac{(hL)^2}4) + (1 + hL + \tfrac{(hL)^2}2 + \tfrac{(hL)^3}4)\Big) = \frac{L\delta}{6}\Big(6 + 3hL + (hL)^2 + \tfrac{(hL)^3}4\Big),$$
which is $\Lambda\delta$. $\square$

$\Lambda$ is increasing in $h$, and $1 + h\Lambda = R(hL)$ with $R(z) = 1 + z + z^2/2 + z^3/6 + z^4/24$.

## Theorem (convergence of order 4)

Assume $f$ is $L$-Lipschitz in $y$ and the local errors satisfy $\|\tau_{n+1}\| \le Ch^5$ for every step of size at most $h$ (by Lemma 1 and the order condition theorem, this holds when $f$ is $C^4$ near the solution and $h \le h_0$). Let the steps be $h_n = t_{n+1} - t_n \le h$, as produced by the algorithm (all equal to $h$ except possibly the last). Then, with $\Lambda$ from Lemma 2,
$$\|e_n\| \le \frac{Ch^4}{\Lambda}\big(e^{\Lambda(t_n - t_0)} - 1\big).$$

*Proof.* Subtract $y_{n+1} = y_n + h_n\Phi(t_n, y_n, h_n)$ from $y(t_{n+1}) = y(t_n) + h_n\Phi(t_n, y(t_n), h_n) + \tau_{n+1}$:
$$e_{n+1} = e_n + h_n\big(\Phi(t_n, y(t_n), h_n) - \Phi(t_n, y_n, h_n)\big) + \tau_{n+1}.$$
By Lemma 2 and the monotonicity of $\Lambda$ in the step, $\|e_{n+1}\| \le (1 + h_n\Lambda)\|e_n\| + Ch_n h^4$, using $h_n^5 \le h_n h^4$. Since $e_0 = 0$, induction gives
$$\|e_n\| \le Ch^4\sum_{m=0}^{n-1} h_m\prod_{j=m+1}^{n-1}(1 + h_j\Lambda) \le Ch^4\sum_{m=0}^{n-1} h_m e^{\Lambda(t_n - t_{m+1})} \le Ch^4\int_{t_0}^{t_n} e^{\Lambda(t_n - s)}\,ds,$$
where $1 + x \le e^x$ was used, and the last step holds because $e^{\Lambda(t_n - s)} \ge e^{\Lambda(t_n - t_{m+1})}$ for $s \in [t_m, t_{m+1}]$. The integral equals $(e^{\Lambda(t_n - t_0)} - 1)/\Lambda$. $\square$

If $f$ is only locally Lipschitz, the same argument applies in a tube around the exact solution, for $h$ small enough that the numerical solution stays in the tube.

## The stability function

On $y' = \lambda y$ with $z = h\lambda$: $hk_1 = zy$, $hk_2 = z(1 + \tfrac z2)y$, $hk_3 = z(1 + \tfrac z2 + \tfrac{z^2}4)y$, $hk_4 = z(1 + z + \tfrac{z^2}2 + \tfrac{z^3}4)y$. Then
$$y_{n+1} = \Big(1 + \frac{z}{6}\big(6 + 3z + z^2 + \tfrac{z^3}4\big)\Big)y_n = \Big(1 + z + \frac{z^2}2 + \frac{z^3}6 + \frac{z^4}{24}\Big)y_n,$$
the Taylor polynomial of $e^z$ of degree 4. So $R(z) = \sum_{j=0}^4 z^j/j!$, and $|R(z)| \to \infty$ as $z \to -\infty$: the method is not A-stable. On the imaginary axis, $|R(iy)|^2 = 1 - y^6/72 + y^8/576$, which is at most 1 exactly when $y^2 \le 8$, so the stability region meets the imaginary axis in $[-2\sqrt2, 2\sqrt2]i$.
