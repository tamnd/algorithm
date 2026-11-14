---
title: The layer-cake identity and the shrinkage law of nested sampling
proves: [correctness]
status: full
---

**Setting.** $\pi$ is a prior probability measure on a parameter space $\Theta$, and $L(\theta) = f(x \mid \theta) \ge 0$ is the likelihood, with $Z = \int L\, d\pi < \infty$. For $\lambda \ge 0$ let

$$X(\lambda) = \pi(\{\theta : L(\theta) > \lambda\}),$$

the prior mass above the level $\lambda$. $X$ is non-increasing, $X(\lambda) \le 1$, and $X$ is right-continuous, because $\{L > \lambda_k\} \uparrow \{L > \lambda\}$ when $\lambda_k \downarrow \lambda$. For $x \in (0, 1)$ define the generalized inverse

$$L(x) = \sup\{\lambda \ge 0 : X(\lambda) > x\}, \qquad \sup\emptyset = 0.$$

## Claim 1: the layer-cake identity

$Z = \int_0^\infty X(\lambda)\, d\lambda = \int_0^1 L(x)\, dx$, and $x \mapsto L(x)$ is non-increasing.

*Proof.* First, $L(\theta) = \int_0^\infty \mathbf{1}\{\lambda < L(\theta)\}\, d\lambda$, so Tonelli's theorem gives $Z = \int\!\int_0^\infty \mathbf{1}\{L(\theta) > \lambda\}\, d\lambda\, \pi(d\theta) = \int_0^\infty X(\lambda)\, d\lambda$.

Second, for $\lambda \ge 0$ and $x \in (0, 1)$,

$$X(\lambda) > x \iff \lambda < L(x). \tag{1}$$

If $\lambda < L(x)$, there is $\lambda' > \lambda$ with $X(\lambda') > x$, and $X(\lambda) \ge X(\lambda') > x$ because $X$ is non-increasing. If $X(\lambda) > x$, right-continuity gives $\delta > 0$ with $X(\lambda + \delta) > x$, so $L(x) \ge \lambda + \delta > \lambda$. By (1) and Tonelli's theorem on $(0, 1) \times [0, \infty)$,

$$\int_0^1 L(x)\, dx = \int_0^1\!\!\int_0^\infty \mathbf{1}\{\lambda < L(x)\}\, d\lambda\, dx = \int_0^\infty\!\!\int_0^1 \mathbf{1}\{x < X(\lambda)\}\, dx\, d\lambda = \int_0^\infty X(\lambda)\, d\lambda,$$

where the last step uses $0 \le X(\lambda) \le 1$. Finally, if $x < x'$ then every $\lambda$ with $X(\lambda) > x'$ also has $X(\lambda) > x$, so $L(x) \ge L(x')$. $\blacksquare$

The identity holds for every prior and likelihood, with or without atoms, in any dimension: the integral over $\Theta$ becomes an integral of a monotone function on $(0, 1)$.

## Claim 2: the prior mass of a prior draw is uniform

Assume that the law of $L(\theta)$ under $\theta \sim \pi$ has no atoms. Let $\theta \sim \pi$ and $U = X(L(\theta))$. Then $U \sim \mathrm{U}(0, 1)$. Moreover, for every $\lambda$ with $X(\lambda) > 0$, if $\theta$ is drawn from $\pi$ restricted to $\{L > \lambda\}$, then $U \sim \mathrm{U}(0, X(\lambda))$.

*Proof.* Let $F$ be the distribution function of $Y = L(\theta)$; it is continuous, and $X(\lambda) = 1 - F(\lambda)$. For $u \in (0, 1)$ the set $\{y : F(y) = u\}$ is non-empty (intermediate value theorem, as $F$ goes from $0$ to $1$), closed and bounded above; let $q$ be its largest element. If $Y \le q$ then $F(Y) \le u$. If $Y > q$ then $F(Y) \ge u$ and $F(Y) \ne u$, so $F(Y) > u$. Hence $P(F(Y) \le u) = P(Y \le q) = F(q) = u$, so $F(Y)$ and $U = 1 - F(Y)$ are uniform on $(0, 1)$.

For the second part, $\{L(\theta) > \lambda\}$ and $\{U < X(\lambda)\}$ differ by a null set. If $L(\theta) \le \lambda$ then $U = 1 - F(L(\theta)) \ge 1 - F(\lambda) = X(\lambda)$. If $L(\theta) > \lambda$ then $U \le X(\lambda)$, with equality only when $F(Y) = F(\lambda)$. Let $q'$ be the largest $y$ with $F(y) = F(\lambda)$; then $\{Y > \lambda,\ F(Y) = F(\lambda)\} \subseteq \{\lambda < Y \le q'\}$, which has probability $F(q') - F(\lambda) = 0$. So, conditional on $L(\theta) > \lambda$, $U$ is a uniform variable conditioned to lie below $X(\lambda)$, which is $\mathrm{U}(0, X(\lambda))$. $\blacksquare$

## Claim 3: the shrinkage law

Under the assumption of Claim 2, and with exact and independent constrained draws on line L7, let $X_i = X(L_i^*)$ be the true prior mass above the $i$-th dead point. Then $t_i = X_i/X_{i-1}$ ($X_0 = 1$) are independent with $t_i \sim \mathrm{Beta}(N, 1)$, that is $P(t_i \le s) = s^N$ on $[0, 1]$. Consequently

$$\mathbb{E}\log t_i = -\frac{1}{N}, \qquad \mathrm{Var}\log t_i = \frac{1}{N^2}, \qquad \mathbb{E}\log X_i = -\frac{i}{N}, \qquad \mathrm{Var}\log X_i = \frac{i}{N^2}.$$

*Proof.* Map each live point to its prior mass $U = X(L(\theta))$. Because $X$ is non-increasing and, by Claim 2, the values $U$ are almost surely distinct, the live point with the lowest likelihood is the one with the largest $U$.

Induction hypothesis $H_{i}$: after $i$ iterations, given $X_1, \ldots, X_i$, the $N$ live values $U$ are independent and $\mathrm{U}(0, X_i)$. $H_0$ holds by Claim 2 with $X_0 = 1$.

Assume $H_{i-1}$. The dead point of iteration $i$ has $X_i = \max$ of $N$ independent $\mathrm{U}(0, X_{i-1})$ values, so $P(X_i \le s X_{i-1}) = s^N$, and $t_i \sim \mathrm{Beta}(N, 1)$ independently of the past. Given the maximum $X_i$, the joint density of the other $N - 1$ values is $\prod_j \mathbf{1}\{u_j < X_i\}/X_i^{N-1}$, so they are independent $\mathrm{U}(0, X_i)$. The new point of line L7 has $L > L_i^*$, so by Claim 2 its value is $\mathrm{U}(0, X_i)$, independent of the others because the draw is independent. This is $H_i$.

For the moments, $P(-\log t > y) = P(t < e^{-y}) = e^{-Ny}$, so $-\log t$ is exponential with rate $N$: mean $1/N$ and variance $1/N^2$. Sums of independent terms give the last two formulas. $\blacksquare$

## Claim 4: what the estimate computes

Let $m$ be the number of dead points. The estimate is

$$\hat Z = \sum_{i=1}^m L_i^*\,(\hat X_{i-1} - \hat X_i) + \frac{\hat X_m}{N}\sum_{k=1}^N L(\theta_k^{\mathrm{live}}), \qquad \hat X_i = e^{-i/N}.$$

(a) **With the true masses $X_i$ in place of $\hat X_i$,** the sum is an upper Riemann sum of $\int_{X_m}^1 L(x)\, dx$. Indeed $L_i^* = L(X_i)$ almost surely, and $L(x) \le L(X_i)$ for $x \in [X_i, X_{i-1}]$ by Claim 1. Since $L$ is monotone, the gap between the upper sum and the integral is at most $(L(X_m) - L(1))\max_i (X_{i-1} - X_i)$. The rest, $\int_0^{X_m} L(x)\, dx$, lies between $0$ and $X_m L_{\max}$; the stopping rule of line L8 asks that $L_{\max}^{\mathrm{live}} \hat X_m < \varepsilon \hat Z$, and the live-point term of line L9 is a Monte Carlo estimate of that rest, since the live values $U$ are uniform on $(0, X_m)$ by Claim 3.

(b) **The plug-in.** By Claim 3, $\hat X_i = e^{-i/N} = \exp(\mathbb{E}\log X_i)$, the geometric mean of $X_i$. The error $\log X_i - \log\hat X_i$ has mean $0$ and standard deviation $\sqrt{i}/N$.

(c) **The information.** Let $H = \int \log\frac{p(\theta \mid x)}{\pi(\theta)}\, p(\theta \mid x)\, d\theta$ be the [Kullback-Leibler divergence](/kullback-leibler-divergence/) from the prior to the posterior. The posterior mass sits where $\log X \approx -H$, so it is reached after about $NH$ iterations. There, by (b), the error of $\log X$ is about $\sqrt{NH}/N = \sqrt{H/N}$, which is the error estimate $\sqrt{H/N}$ of $\log\hat Z$ (Skilling 2006).

Part (a) and the moments in (b) are exact. The step from (b) to the size of the error of $\log\hat Z$ in (c) is a heuristic: it treats the posterior mass as sitting at one value of $\log X$. Chopin and Robert (2010) prove that, with exact constrained draws, the estimate is consistent and its error is of order $N^{-1/2}$. On the page, the ratio of the measured standard deviation to $\sqrt{H/N}$ is measured, not proved. $\blacksquare$

## Claim 5: the exact information of the normal-normal model

For $x_1, \ldots, x_n \sim N(\theta, \sigma^2)$ and $\theta \sim N(0, \tau^2)$ the posterior is $N(m, v)$ with $v = (n/\sigma^2 + 1/\tau^2)^{-1}$ and $m = v n\bar x/\sigma^2$, and

$$H = \tfrac12\log\frac{\tau^2}{v} - \tfrac12 + \frac{v + m^2}{2\tau^2}.$$

*Proof.* $H = \mathbb{E}_{N(m, v)}\big[\log N(\theta; m, v) - \log N(\theta; 0, \tau^2)\big] = \big(-\frac12\log(2\pi v) - \frac12\big) - \big(-\frac12\log(2\pi\tau^2) - \frac{v + m^2}{2\tau^2}\big)$, using $\mathbb{E}(\theta - m)^2 = v$ and $\mathbb{E}\theta^2 = v + m^2$. $\blacksquare$
