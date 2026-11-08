---
title: Heun's method computes its grid values, has local error O(h^3) and global error O(h^2)
proves: [correctness, termination, convergence]
status: full
---

**Setting.** We use any norm $\|\cdot\|$ on $\mathbb{R}^d$. The function $f : [t_0, T] \times \mathbb{R}^d \to \mathbb{R}^d$ is continuous and Lipschitz in $y$ with constant $L$. By the [Picard-Lindelöf theorem](/picard-lindelof-theorem/) the problem $y' = f(t, y)$, $y(t_0) = y_0$ has a unique solution on $[t_0, T]$. For the order statement we also assume that $y \in C^3[t_0, T]$, and we write $M_2 = \max \|y''\|$ and $M_3 = \max \|y'''\|$. This holds when $f$ is $C^2$. The step map of Heun's method is

$$\Phi_h(t, u) = u + \frac{h}{2}\Bigl(f(t, u) + f\bigl(t + h, u + h f(t, u)\bigr)\Bigr).$$

**Lemma 1 (the loop).** Let $N$ be the value of line L1. After the iteration with index $n$ of lines L3 to L9, the variables hold $t = t_{n+1}$ and $y = y_{n+1}$, where $t_m = t_0 + m h$ for $m < N$, $t_N = T$, and $y_{m+1} = \Phi_{h_m}(t_m, y_m)$ with $h_m = t_{m+1} - t_m$.

*Proof.* Induction on $n$. Before the loop, line L2 sets $t = t_0$ and $y = y_0$. Assume $t = t_n$ and $y = y_n$ at the start of iteration $n$. Line L4 sets $t_{\text{next}} = t_{n+1}$ by the definition of the grid, and line L5 sets $h_n$. Lines L6 and L7 compute $k_1 = f(t_n, y_n)$ and $k_2 = f(t_n + h_n, y_n + h_n k_1)$, and line L8 sets $y = y_n + h_n (k_1 + k_2)/2 = \Phi_{h_n}(t_n, y_n)$. Line L9 sets $t = t_{n+1}$. $\square$

**Termination.** The loop of line L3 runs exactly $N = \lceil (T - t_0)/h \rceil$ times, and each run makes two evaluations of $f$. In exact arithmetic $h_m = h$ for $m < N - 1$ and $0 < h_{N-1} \le h$. (In floating point the slack of line L1 can stretch the last step by a relative amount of at most $10^{-9}$, which we ignore.)

**Lemma 2 (local error).** For $t \in [t_0, T]$ and $0 < k \le T - t$, the local error $\delta(t, k) = y(t + k) - \Phi_k(t, y(t))$ satisfies

$$\|\delta(t, k)\| \le C k^3, \qquad C = \frac{M_3}{12} + \frac{L M_2}{4}.$$

*Proof.* Split $\delta$ into a quadrature error and a predictor error:

$$\delta = \underbrace{y(t + k) - y(t) - \frac{k}{2}\bigl(y'(t) + y'(t + k)\bigr)}_{\delta_1} + \underbrace{\frac{k}{2}\Bigl(f\bigl(t + k, y(t + k)\bigr) - f\bigl(t + k, y(t) + k f(t, y(t))\bigr)\Bigr)}_{\delta_2},$$

where we used $y'(s) = f(s, y(s))$. The term $\delta_1$ is the error of the trapezoidal rule applied to $y'$. In the Peano kernel form,

$$\delta_1 = -\frac12 \int_t^{t + k} (s - t)(t + k - s)\, y'''(s)\, ds,$$

as two integrations by parts of the right-hand side show (for $y''' \equiv 1$ both sides equal $-k^3/12$). The kernel is nonnegative and $\int_t^{t+k} (s - t)(t + k - s)\, ds = k^3/6$, so $\|\delta_1\| \le \frac12 M_3 \frac{k^3}{6} = \frac{M_3}{12} k^3$. For $\delta_2$, the Lipschitz condition gives $\|\delta_2\| \le \frac{k}{2} L\, \|y(t + k) - y(t) - k y'(t)\|$, and Taylor's formula with integral remainder gives $\|y(t + k) - y(t) - k y'(t)\| = \|\int_t^{t+k} (t + k - s) y''(s)\, ds\| \le M_2 k^2 / 2$. So $\|\delta_2\| \le \frac{L M_2}{4} k^3$. $\square$

**Lemma 3 (stability of one step).** For all $t$, $u$, $v$ and $0 < k \le h$, $\|\Phi_k(t, u) - \Phi_k(t, v)\| \le (1 + k\Lambda) \|u - v\|$ with $\Lambda = L (1 + hL/2)$.

*Proof.* Let $u^* = u + k f(t, u)$ and $v^* = v + k f(t, v)$. Then $\|u^* - v^*\| \le (1 + kL)\|u - v\|$, and

$$\|\Phi_k(t, u) - \Phi_k(t, v)\| \le \|u - v\| + \frac{k}{2} L \|u - v\| + \frac{k}{2} L (1 + kL)\|u - v\| = \bigl(1 + kL(1 + kL/2)\bigr)\|u - v\|,$$

which is at most $(1 + k\Lambda)\|u - v\|$ because $k \le h$. $\square$

**Theorem (convergence of order 2).** Under the assumptions of the setting, the global errors $e_n = y(t_n) - y_n$ satisfy, for $n = 0, \dots, N$,

$$\|e_n\| \le C h^2\, \frac{e^{\Lambda (t_n - t_0)} - 1}{\Lambda}, \qquad C = \frac{M_3}{12} + \frac{L M_2}{4}, \quad \Lambda = L\Bigl(1 + \frac{hL}{2}\Bigr),$$

when $L > 0$. (For $L = 0$ the bound reads $\|e_n\| \le C h^2 (t_n - t_0)$.)

*Proof.* Write $E_n = \|e_n\|$. Then $e_{n+1} = \delta(t_n, h_n) + \Phi_{h_n}(t_n, y(t_n)) - \Phi_{h_n}(t_n, y_n)$, so by Lemmas 2 and 3,

$$E_{n+1} \le (1 + h_n \Lambda) E_n + C h_n^3 \le e^{h_n \Lambda} E_n + C h^2 h_n.$$

We show $E_n \le C h^2 (e^{\Lambda (t_n - t_0)} - 1)/\Lambda$ by induction. It holds for $n = 0$ since $E_0 = 0$. If it holds for $n$, then

$$E_{n+1} \le \frac{C h^2}{\Lambda}\Bigl(e^{\Lambda (t_{n+1} - t_0)} - e^{h_n \Lambda} + \Lambda h_n\Bigr) \le \frac{C h^2}{\Lambda}\Bigl(e^{\Lambda (t_{n+1} - t_0)} - 1\Bigr),$$

because $e^{x} \ge 1 + x$. $\blacksquare$

**Remark (exactness on the test equation).** For $f(t, y) = \lambda y$, lines L6 to L8 give $k_1 = \lambda y_n$, $k_2 = \lambda (1 + h\lambda) y_n$ and $y_{n+1} = (1 + z + z^2/2) y_n$ with $z = h\lambda$. So $y_n = R(z)^n y_0$ with $R(z) = 1 + z + z^2/2$, in exact arithmetic, for each $n$.
