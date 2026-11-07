---
title: The secant method ends, converges near a simple root, and has order (1 + 5^(1/2))/2
proves: [correctness, termination, local-convergence, order]
status: full
---

We write $x_{k-1}, x_k$ for the values of $x_0, x_1$ at the start of pass $k$ of the loop of lines L3 to L10, so the starting points are $x_0, x_1$ and pass $k$ computes $x_{k+1}$. Let $e_k = x_k - x^*$, $f_k = f(x_k)$, and let $f[a, b]$ and $f[a, b, c]$ be the first and second divided differences.

**Claim 1 (termination and flags).** SECANT returns after at most $k_{\max}$ passes and $k_{\max} + 2$ evaluations of $f$. A result with the flag "root" is an exact zero of $f$; a result with the flag "converged" passed the test of line L8.

*Proof.* Lines L1 and L2 make two evaluations, each pass makes at most one (line L9), and the loop of line L3 runs at most $k_{\max}$ times. Lines L1, L2 and L9 return only when the value is exactly $0$, and line L8 only after its test. The division in line L5 is defined because line L4 has checked $f_1 \ne f_0$. $\square$

**Lemma (the error identity).** Let $f \in C^2$ on an interval $I$ that holds $x_{k-1}$, $x_k$ and $x^*$, with $x_{k-1} \ne x_k$ and $f[x_{k-1}, x_k] \ne 0$. Then
$$e_{k+1} = \frac{f[x_{k-1}, x_k, x^*]}{f[x_{k-1}, x_k]}\, e_k e_{k-1},$$
and there are $\xi_k, \eta_k \in I$ with $f[x_{k-1}, x_k, x^*] = \tfrac12 f''(\xi_k)$ and $f[x_{k-1}, x_k] = f'(\eta_k)$.

*Proof.* Line L5 gives $x_{k+1} = x_k - f_k / f[x_{k-1}, x_k]$. Since $f(x^*) = 0$, $f_k = f_k - f(x^*) = f[x_k, x^*]\, e_k$ (if $x_k = x^*$ both sides are $0$, with $f[x^*, x^*] = f'(x^*)$). So
$$e_{k+1} = e_k - \frac{f[x_k, x^*]\, e_k}{f[x_{k-1}, x_k]} = e_k\, \frac{f[x_{k-1}, x_k] - f[x_k, x^*]}{f[x_{k-1}, x_k]}.$$
By the definition of the second divided difference, $f[x_{k-1}, x_k] - f[x_k, x^*] = (x_{k-1} - x^*)\, f[x_{k-1}, x_k, x^*] = e_{k-1}\, f[x_{k-1}, x_k, x^*]$. This gives the identity. The mean value forms of divided differences give $\xi_k$ and $\eta_k$ in the smallest interval that holds the points, which lies in $I$. $\square$

**Claim 2 (local convergence).** Let $f \in C^2$ on $I = [x^* - r, x^* + r]$ with $f(x^*) = 0$ and $f' \ne 0$ on $I$, let $M = \max_I |f''| / (2 \min_I |f'|)$, and let $x_0 \ne x_1$ in $I$ with $M |e_0| \le 1/2$ and $M |e_1| \le 1/2$. Then in exact arithmetic, with $k_{\max} = \infty$ and a zero tolerance, every $x_k$ lies in $I$, $|e_{k+1}| \le M |e_k| |e_{k-1}| \le \tfrac12 |e_k|$, and $x_k \to x^*$.

*Proof.* By induction on $k \ge 1$ we show: $x_{k-1}, x_k \in I$, $M |e_{k-1}| \le 1/2$ and $M |e_k| \le 1/2$. This holds for $k = 1$. Assume it for $k$. If $f_k = 0$ the method returns at line L2 or L9 with $x_k = x^*$, since $f' \ne 0$ on $I$ makes $x^*$ the only zero in $I$. Otherwise $x_k \ne x^*$. The points $x_{k-1}$ and $x_k$ differ: for $k = 1$ by assumption, and for $k \ge 2$ because $x_k = x_{k-1} + s$ with $s = 0$ only if $f_{k-1} = 0$, which has already returned. By the mean value theorem $f[x_{k-1}, x_k] = f'(\eta) \ne 0$, so $f_k \ne f_{k-1}$ and line L4 does not stop. The lemma gives $|e_{k+1}| \le M |e_k| |e_{k-1}| \le \tfrac12 |e_k| \le r$, so $x_{k+1} \in I$ and $M |e_{k+1}| \le \tfrac12 M |e_k| \le 1/2$. This completes the induction. Then $|e_{k+1}| \le \tfrac12 |e_k|$ for all $k \ge 1$, so $|e_k| \le 2^{1-k} |e_1| \to 0$. $\square$

**Claim 3 (order $\varphi$).** Under the hypotheses of Claim 2, assume also that $f''(x^*) \ne 0$ and that no $e_k$ is zero. Let $\varphi = (1 + \sqrt 5)/2$ and $C = |f''(x^*) / (2 f'(x^*))|$. Then
$$\lim_{k \to \infty} \frac{|e_{k+1}|}{|e_k|^{\varphi}} = C^{1/\varphi}.$$

*Proof.* Let $M_k = |e_{k+1}| / (|e_k| |e_{k-1}|)$. By the lemma $M_k = |f''(\xi_k)| / (2 |f'(\eta_k)|)$, and since $x_{k-1}, x_k \to x^*$, both $\xi_k$ and $\eta_k$ tend to $x^*$, so $M_k \to C > 0$ by continuity. Let $y_k = |e_{k+1}| / |e_k|^{\varphi}$. Since $\varphi^2 = \varphi + 1$, we have $(1 - \varphi)(-\varphi) = \varphi^2 - \varphi = 1$, and so
$$y_{k-1}^{1 - \varphi} = |e_k|^{1 - \varphi}\, |e_{k-1}|^{-\varphi(1 - \varphi)} = |e_k|^{1 - \varphi}\, |e_{k-1}|.$$
Hence $y_k = M_k |e_k| |e_{k-1}| / |e_k|^{\varphi} = M_k\, y_{k-1}^{1 - \varphi}$. Take logarithms, use $1 - \varphi = -1/\varphi$, and set $\rho = 1/\varphi \approx 0.618 < 1$:
$$\ln y_k = \ln M_k - \rho \ln y_{k-1}.$$
Let $L = \ln C / (1 + \rho)$, $z_k = \ln y_k - L$ and $\epsilon_k = \ln M_k - \ln C$. Then $z_k = \epsilon_k - \rho z_{k-1}$, so $|z_k| \le |\epsilon_k| + \rho |z_{k-1}|$, with $\epsilon_k \to 0$.

*The sequence $z_k$ tends to $0$.* Let $E = \sup_k |\epsilon_k| < \infty$. By induction $|z_k| \le E/(1 - \rho) + |z_1|$, so $(z_k)$ is bounded. Let $\lambda = \limsup |z_k|$. Taking the limit superior in $|z_k| \le |\epsilon_k| + \rho |z_{k-1}|$ gives $\lambda \le 0 + \rho \lambda$, so $\lambda = 0$.

So $\ln y_k \to L$, and $y_k \to e^L = C^{1/(1 + \rho)}$. Since $1 + \rho = 1 + 1/\varphi = (\varphi + 1)/\varphi = \varphi^2/\varphi = \varphi$, the limit is $C^{1/\varphi}$. $\square$

**Floating point.** Claim 1 holds in floating point as stated. Claims 2 and 3 hold in exact arithmetic; in floating point the iterates follow them until the error reaches the limiting accuracy. $\blacksquare$
