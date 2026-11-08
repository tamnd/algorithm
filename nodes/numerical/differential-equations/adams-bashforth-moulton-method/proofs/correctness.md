---
title: Order, convergence and Milne's estimate for the Adams-Bashforth-Moulton PECE scheme
proves: [correctness]
status: full
---

**Setting.** $y' = f(t, y)$, $y \in \mathbb{R}^d$ with a norm $\|\cdot\|$, $f$ is $L$-Lipschitz in $y$, uniform grid $t_n = t_0 + nh$. The predictor is AB$k$ with weights $\beta_0, \dots, \beta_{k-1}$, the corrector is AM with $k - 1$ steps and weights $\beta^*_{-1}, \dots, \beta^*_{k-2}$. Write $B_P = \sum_j|\beta_j|$, $B_C = \sum_j|\beta^*_j|$, $B = \max(B_P, B_C)$. From the pages on the two families: if $y \in C^{k+1}$ with $M_{k+1} = \max\|y^{(k+1)}\|$, the local truncation errors of the two formulas satisfy $\|\tau^P\| \le \gamma_kM_{k+1}h^{k+1}$ and $\|\tau^*\| \le |\gamma^*_{k-1}|M_{k+1}h^{k+1}$.

## Lemma 1 (local error of PECE)

Let $\tilde y^P = y(t_n) + h\sum_j\beta_jy'(t_{n-j})$ be the predictor computed from exact past values, and $\tilde y^C = y(t_n) + h\big(\beta^*_{-1}f(t_{n+1}, \tilde y^P) + \sum_{j \ge 0}\beta^*_jy'(t_{n-j})\big)$ the corrected value. Then $\tau^{PECE}_{n+1} = y(t_{n+1}) - \tilde y^C$ satisfies
$$\|\tau^{PECE}_{n+1}\| \le \big(|\gamma^*_{k-1}| + h|\beta^*_{-1}|L\gamma_k\big)M_{k+1}h^{k+1}.$$

*Proof.* Since $y'(t_{n+1}) = f(t_{n+1}, y(t_{n+1}))$,
$$y(t_{n+1}) - \tilde y^C = \tau^*_{n+1} + h\beta^*_{-1}\big(f(t_{n+1}, y(t_{n+1})) - f(t_{n+1}, \tilde y^P)\big),$$
and $\|y(t_{n+1}) - \tilde y^P\| = \|\tau^P_{n+1}\| \le \gamma_kM_{k+1}h^{k+1}$. The Lipschitz bound finishes the proof. $\square$

So PECE has order $k$, and its leading local error is that of the corrector; the predictor contributes only at order $h^{k+2}$.

## Theorem (convergence)

Let $\delta = \max_{m \le k-1}\|e_m\|$ and $c = LB(1 + h|\beta^*_{-1}|L)$. Then
$$\|e_n\| \le e^{c(t_n - t_0)}\delta + \frac{(|\gamma^*_{k-1}| + h|\beta^*_{-1}|L\gamma_k)M_{k+1}h^k}{c}\big(e^{c(t_n - t_0)} - 1\big).$$

*Proof.* Let $E_n = \max_{m \le n}\|e_m\|$. The computed predictor and the exact-data predictor differ by $\|y^P - \tilde y^P\| \le E_n + hLB_PE_n$. The computed and exact-data corrected values differ by
$$\|y_{n+1} - \tilde y^C\| \le E_n + hL\sum_{j \ge 0}|\beta^*_j|E_n + h|\beta^*_{-1}|L(1 + hLB_P)E_n \le (1 + hLB_C + h^2L^2|\beta^*_{-1}|B_P)E_n \le (1 + hc)E_n.$$
Adding the local error, $\|e_{n+1}\| \le (1 + hc)E_n + \|\tau^{PECE}_{n+1}\|$, and the same bound holds for $E_{n+1}$. The discrete Gronwall argument used for Adams-Bashforth, $(1 + hc)^m \le e^{cmh}$, gives the result. $\square$

With RK4 starting values $\delta = O(h^5)$, so the implementation has order $\min(k, 5)$.

## Theorem (Milne's estimate)

Assume $y \in C^{k+2}$. For exact past data,
$$\frac{\gamma^*_{k-1}}{\gamma_k - \gamma^*_{k-1}}\big(\tilde y^C - \tilde y^P\big) = \tau^{PECE}_{n+1} + O(h^{k+2}).$$

*Proof.* By the Peano kernel form of the interpolation remainder in the proofs for the two families, with $y \in C^{k+2}$ one has $\tau^P_{n+1} = \gamma_kh^{k+1}y^{(k+1)}(t_n) + O(h^{k+2})$ and $\tau^*_{n+1} = \gamma^*_{k-1}h^{k+1}y^{(k+1)}(t_n) + O(h^{k+2})$: the integrand $w(t)\,y'[\dots, t]$ has the divided difference equal to $y^{(k+1)}(t_n)/k! + O(h)$. By Lemma 1, $\tau^{PECE} = \tau^* + O(h^{k+2})$. Hence
$$\tilde y^C - \tilde y^P = (y(t_{n+1}) - \tilde y^P) - (y(t_{n+1}) - \tilde y^C) = (\gamma_k - \gamma^*_{k-1})h^{k+1}y^{(k+1)}(t_n) + O(h^{k+2}).$$
Multiplying by $\gamma^*_{k-1}/(\gamma_k - \gamma^*_{k-1})$ gives $\gamma^*_{k-1}h^{k+1}y^{(k+1)}(t_n) + O(h^{k+2}) = \tau^{PECE}_{n+1} + O(h^{k+2})$. $\square$

The estimate is therefore asymptotically correct: the ratio of estimate to true local error tends to 1 wherever $y^{(k+1)} \ne 0$, at rate $O(h)$. The tests confirm this for $k = 4$, and the exact factors $-19/270$ ($k = 4$) and $-1/6$ ($k = 2$) are checked with fractions.

## Iterated correction

For P(EC)$^m$E the corrector map $x \mapsto g + h\beta^*_{-1}f(t_{n+1}, x)$ is a contraction with factor $q = h|\beta^*_{-1}|L$ when $q < 1$. After $m$ corrections the distance to the Adams-Moulton solution is at most $q^m$ times the predictor's distance, so as $m \to \infty$ the scheme converges to the implicit Adams-Moulton step, which the tests check for the trapezoidal corrector on $y' = -y$.
