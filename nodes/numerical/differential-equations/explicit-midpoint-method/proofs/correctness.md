---
title: The explicit midpoint method computes its recurrence and converges with order 2
proves: [correctness, termination, convergence]
status: full
---

**Setting.** We use a norm $\|\cdot\|$ on $\mathbb{R}^d$. The function $f : [t_0, T] \times \mathbb{R}^d \to \mathbb{R}^d$ is continuous and Lipschitz in $y$ with constant $L$. The method is the one-step method $y_{n+1} = y_n + h_n \Phi(t_n, y_n, h_n)$ with the increment function

$$\Phi(t, y, h) = f\left(t + \tfrac{h}{2},\; y + \tfrac{h}{2} f(t, y)\right).$$

**Lemma 1 (the loop).** After the iteration with index $n$ of lines L3 to L8, $t = t_{n+1}$ and $y = y_{n+1}$, where $t_m = t_0 + m h$ for $m < N$, $t_N = T$, $h_m = t_{m+1} - t_m$ and $y_{m+1} = y_m + h_m \Phi(t_m, y_m, h_m)$. The algorithm stops after $N$ iterations and $2N$ evaluations of $f$.

*Proof.* Induction on $n$, as for [Euler's method](/euler-method/). Line L2 starts with $(t_0, y_0)$. If $t = t_n$ and $y = y_n$ at the start of iteration $n$, line L4 gives the step length $s = h_n$, line L5 gives $k_1 = f(t_n, y_n)$, line L6 gives $k_2 = \Phi(t_n, y_n, h_n)$, and lines L7 and L8 give $y = y_{n+1}$ and $t = t_{n+1}$. The for loop runs $N$ times, with two evaluations of $f$ each time. $\square$

**Lemma 2 (stability of the increment).** For all $t$, $u$, $v$ and $0 < h \le h_{\max}$, $\|\Phi(t, u, h) - \Phi(t, v, h)\| \le \Lambda \|u - v\|$ with $\Lambda = L(1 + \tfrac12 h_{\max} L)$.

*Proof.* By the Lipschitz condition twice, $\|\Phi(t, u, h) - \Phi(t, v, h)\| \le L\,\|u - v + \tfrac{h}{2}(f(t, u) - f(t, v))\| \le L(\|u - v\| + \tfrac{h}{2} L \|u - v\|)$. $\square$

**Lemma 3 (local error).** Assume in addition that $f$ is $C^2$ and that its second derivatives are bounded, and let $y$ be the exact solution. Then there is a constant $K$, which depends only on $\max \|y'''\|$ and the bound of the second derivatives of $f$, such that the defect $\tau_n = y(t_{n+1}) - y(t_n) - h_n \Phi(t_n, y(t_n), h_n)$ satisfies $\|\tau_n\| \le K h_n^3$.

*Proof.* Write $t = t_n$, $\eta = y(t)$ and $s = h_n$. Since $f \in C^2$, the solution is $C^3$. Taylor's formula gives $y(t + s) = \eta + s y'(t) + \tfrac12 s^2 y''(t) + r_1$ with $\|r_1\| \le \tfrac16 s^3 \max\|y'''\|$. Let $g(\sigma) = f(t + \sigma/2, \eta + (\sigma/2) f(t, \eta))$ for $\sigma \in [0, s]$. Then $g(0) = f(t, \eta) = y'(t)$ and, by the chain rule, $g'(0) = \tfrac12\big(f_t(t, \eta) + f_y(t, \eta) f(t, \eta)\big) = \tfrac12 y''(t)$, because $y'' = f_t + f_y f$ along the solution. Taylor's formula for $g$ gives $g(s) = g(0) + s g'(0) + r_2$ with $\|r_2\| \le \tfrac12 s^2 \max\|g''\|$, and $g''(\sigma) = \tfrac14 D^2 f[(1, f(t, \eta)), (1, f(t, \eta))]$ is bounded by the bound of the second derivatives of $f$ times $\tfrac14(1 + \|f(t, \eta)\|)^2$, which is bounded on the solution. Hence $s\Phi(t, \eta, s) = s g(s) = s y'(t) + \tfrac12 s^2 y''(t) + s r_2$, and $\tau_n = r_1 - s r_2$ has norm at most $K s^3$. $\square$

**Theorem (convergence of order 2).** Under the hypotheses of Lemmas 2 and 3, with $h = \max_n h_n$, the global error $e_n = y(t_n) - y_n$ satisfies

$$\|e_n\| \le \frac{K h^2}{\Lambda}\left(e^{\Lambda (t_n - t_0)} - 1\right) \quad \text{for all } n \le N.$$

*Proof.* Subtracting the numerical step from the definition of $\tau_n$ gives $e_{n+1} = e_n + h_n(\Phi(t_n, y(t_n), h_n) - \Phi(t_n, y_n, h_n)) + \tau_n$. By Lemmas 2 and 3, $\|e_{n+1}\| \le (1 + h_n\Lambda)\|e_n\| + K h_n h^2$. With $C = K h^2/\Lambda$ we show $\|e_n\| \le C(e^{\Lambda(t_n - t_0)} - 1)$ by induction. It holds for $n = 0$ since $e_0 = 0$. If it holds for $n$, then, since $1 + x \le e^x$,

$$\|e_{n+1}\| \le C e^{h_n \Lambda}\left(e^{\Lambda(t_n - t_0)} - 1\right) + C h_n \Lambda = C\left(e^{\Lambda(t_{n+1} - t_0)} - e^{h_n\Lambda} + h_n \Lambda\right) \le C\left(e^{\Lambda(t_{n+1} - t_0)} - 1\right). \qquad \blacksquare$$

**The order is not higher.** On $y' = \lambda y$ one step multiplies $y_n$ by $R(z) = 1 + z + \tfrac12 z^2$, while the exact factor is $e^z = 1 + z + \tfrac12 z^2 + \tfrac16 z^3 + O(z^4)$. The defect is $\tfrac16 z^3 y(t_n) + O(z^4)$, which is not $O(h^4)$, so the order is exactly 2. $\blacksquare$
