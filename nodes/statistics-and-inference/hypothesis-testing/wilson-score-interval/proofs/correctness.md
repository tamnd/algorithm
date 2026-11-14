---
title: The Wilson interval is the set of p that the score test accepts, and its coverage dips below 0.84 for every n
proves: [correctness]
status: full
---

Let $X \sim \text{Binomial}(n, p)$ with $n \ge 1$, observed value $x$, and let $z = z_{1 - \alpha/2} > 0$ be the upper $\alpha/2$ point of the standard normal law. The two-sided score test of $H_0: p = p_0$ accepts when $(x - n p_0)^2 \le z^2 n p_0 (1 - p_0)$. The [score](/score-function/) of the binomial log-likelihood at $p_0$ is $(x - n p_0)/(p_0(1 - p_0))$ and the Fisher information is $n/(p_0(1 - p_0))$, so this is the squared score statistic compared with $z^2$.

**Claim 1 (the acceptance set is the interval of the page).** For $p \in [0, 1]$, the score test accepts $p$ if and only if $L \le p \le U$, where

$$L, U = c \mp h, \qquad c = \frac{x + z^2/2}{n + z^2}, \qquad h = \frac{z}{n + z^2} \sqrt{\frac{x (n - x)}{n} + \frac{z^2}{4}}.$$

*Proof.* Expand the acceptance condition and divide by $n > 0$:

$$q(p) = (n + z^2) p^2 - (2x + z^2) p + \frac{x^2}{n} \le 0.$$

$q$ is a quadratic with positive leading coefficient. Its discriminant is

$$(2x + z^2)^2 - 4 (n + z^2) \frac{x^2}{n} = 4 x z^2 + z^4 - \frac{4 z^2 x^2}{n} = 4 z^2 \Big(\frac{x(n - x)}{n} + \frac{z^2}{4}\Big) > 0,$$

so $q$ has two real roots $c \mp h$, and $q(p) \le 0$ exactly between them. $\square$

**Claim 2 (the ends lie in $[0, 1]$ and contain $x/n$).** $q(0) = x^2/n \ge 0$ and $q(1) = n - 2x + x^2/n = (n - x)^2/n \ge 0$, and the vertex $c$ lies in $(0, 1)$. A convex quadratic that is non-negative at $0$ and at $1$, with its vertex between them, has both roots in $[0, 1]$. Also $q(x/n) = -z^2 \frac{x}{n}\big(1 - \frac{x}{n}\big) \le 0$, so $L \le x/n \le U$. The root $0$ occurs exactly when $x = 0$, and the root $1$ exactly when $x = n$. $\square$

**Claim 3 (the code computes these roots).** Lines L2 and L3 compute $c$ and $h$, and line L4 sets $U = c + h$, or $U = 1$ exactly when $x = n$. By Vieta's formulas the product of the roots is $(x^2/n)/(n + z^2)$, so line L5 computes $L = (x^2/n)/((n + z^2) U)$. Since $U \ge c > 0$, the division is safe. This form has no subtraction, so it does not lose digits when $c$ and $h$ are close, and it gives $L = 0$ exactly when $x = 0$. $\square$

**Claim 4 (asymptotic coverage at a fixed $p$).** For fixed $p \in (0, 1)$, the coverage $C_n(p) = P_p(L \le p \le U)$ tends to $1 - \alpha$ as $n \to \infty$.

*Proof.* By Claim 1, $C_n(p) = P_p(\lvert Z_n \rvert \le z)$ with $Z_n = (X - np)/\sqrt{np(1 - p)}$. By the [central limit theorem](/central-limit-theorem/), $Z_n$ converges in distribution to $N(0, 1)$, and the normal law has no atom at $\pm z$, so $C_n(p) \to 1 - \alpha$. $\square$

The convergence is not uniform in $p$. The next claim gives a bound that holds for every $n$.

**Claim 5 (a dip near the ends, for every $n$).** Let $\alpha \le 0.38$, and let $\lambda^*$ be the smaller root of $g(\lambda) = \lambda^2 - (2 + z^2)\lambda + 1$. For every $n \ge 1$ and every $p$ with $0 < p < \lambda^*/n$, the interval covers $p$ only when $x = 0$, so $C_n(p) = (1 - p)^n$. Hence

$$\inf_{0 < p < 1} C_n(p) \le \Big(1 - \frac{\lambda^*}{n}\Big)^n < e^{-\lambda^*}.$$

For $\alpha = 0.05$, $\lambda^* = 0.176525$ and $e^{-\lambda^*} = 0.83818$.

*Proof.* Write $s = z^2$ and $\lambda = np$, so $0 < \lambda < \lambda^*$. Since $g(0) = 1 > 0$ and $g(1) = -s < 0$, the smaller root satisfies $0 < \lambda^* < 1$, and $g > 0$ on $[0, \lambda^*)$. By Claim 1, the interval for $x$ covers $p$ if and only if $(x - \lambda)^2 \le s \lambda (1 - p)$.

- *$x \ge 1$ does not cover $p$.* Since $\lambda < 1$, $(x - \lambda)^2 \ge (1 - \lambda)^2$. Since $g(\lambda) > 0$, $(1 - \lambda)^2 > s \lambda \ge s \lambda (1 - p)$.
- *$x = 0$ covers $p$.* The condition is $\lambda \le s(1 - p)$. Since $p \le \lambda$, it suffices that $\lambda \le s (1 - \lambda)$, that is $\lambda \le s/(1 + s)$. A direct expansion gives $(1 + s)^2 g\big(s/(1 + s)\big) = 1 - s^2 - s^3$, which is at most $0$ when $s \ge 0.7549$, that is when $z \ge 0.8688$, which holds for $\alpha \le 0.38$. Then $s/(1 + s)$ is not in the region where $g > 0$, so $\lambda < \lambda^* \le s/(1 + s)$.

So $C_n(p) = P_p(X = 0) = (1 - p)^n$. Letting $p$ rise to $\lambda^*/n$ gives the first bound, and $(1 - t/n)^n < e^{-t}$ for $0 < t < n$ gives the second. $\square$

**What is proved and what is measured.** Claims 1 to 5 are proved. The mean coverage near $1 - \alpha$, the place of the smallest coverage on a grid, and the share of $p$ with coverage below $1 - \alpha$ are measured on the page by exact binomial sums over a grid of $p$. They are not theorems.

**Cost.** Lines L1 to L6 do a fixed number of operations, one square root and one normal quantile, so the time and space are $\Theta(1)$. $\square$
