---
title: Rates of convergence of Bernstein polynomials, Voronovskaya's formula and the convergence of derivatives
proves: [statement]
status: full
---

We use the notation of the statement. Fix $n \ge 1$ and $x \in [0, 1]$. Let $X_1, \dots, X_n$ be independent random variables with $\Pr(X_j = 1) = x$ and $\Pr(X_j = 0) = 1 - x$, let $S = X_1 + \dots + X_n$, and let $Y = S/n - x$. Then $\Pr(S = k) = b_{n,k}(x)$, so for every function $g$ on $[0, 1]$,
$$B_n g(x) = \mathbb{E}\, g(S/n). \tag{1}$$

**Lemma 1 (moments).** Put $v = x (1 - x)$. Then $\mathbb{E}\, Y = 0$, $\mathbb{E}\, Y^2 = v / n$, and
$$\mathbb{E}\, Y^4 = \frac{v \big(1 + 3 (n - 2) v\big)}{n^3} \le \frac{7}{16 n^2}.$$

*Proof.* Let $Z_j = X_j - x$, so $n Y = \sum_j Z_j$, the $Z_j$ are independent, and $\mathbb{E}\, Z_j = 0$. Also $\mathbb{E}\, Z_j^2 = x (1 - x)^2 + (1 - x) x^2 = v$ and
$$\mathbb{E}\, Z_j^4 = x (1 - x)^4 + (1 - x) x^4 = v \big((1 - x)^3 + x^3\big) = v (1 - 3x + 3x^2) = v (1 - 3v).$$
Expand $(\sum_j Z_j)^2$ and $(\sum_j Z_j)^4$. Every product that contains some $Z_j$ to the first power has mean 0, by independence. So $\mathbb{E} (\sum_j Z_j)^2 = n v$, and in the fourth power only the terms $Z_j^4$ ($n$ of them) and $Z_i^2 Z_j^2$ with $i \ne j$ remain; each unordered pair $\{i, j\}$ appears $\binom42 = 6$ times, so the second kind contributes $6 \binom n2 v^2 = 3 n (n - 1) v^2$. Hence
$$n^4\, \mathbb{E}\, Y^4 = n v (1 - 3v) + 3 n (n - 1) v^2 = n v \big(1 + 3 (n - 2) v\big).$$
For the bound, let $n \ge 2$. Then $v \le \frac14$ gives $v (1 + 3 (n - 2) v) \le \frac14 \big(1 + \frac34 (n - 2)\big) = \frac{3n - 2}{16} \le \frac{7n}{16}$. For $n = 1$ the value is $v (1 - 3v) \le \frac14 < \frac{7}{16}$. Divide by $n^3$. $\square$

By Cauchy-Schwarz, Lemma 1 gives
$$\mathbb{E} |Y| \le \big(\mathbb{E}\, Y^2\big)^{1/2} = \sqrt{v / n} \le \frac{1}{2 \sqrt n}. \tag{2}$$

**Lemma 2 (the modulus of continuity).** For a continuous $f$, $\delta > 0$ and $x, y \in [0, 1]$, $|f(y) - f(x)| \le (1 + |y - x| / \delta)\, \omega_f(\delta)$.

*Proof.* Let $m = \lceil |y - x| / \delta \rceil$, or $m = 1$ if $y = x$. Split the segment from $x$ to $y$ into $m$ equal parts of length at most $\delta$. By the triangle inequality, $|f(y) - f(x)| \le m\, \omega_f(\delta)$, and $m \le 1 + |y - x| / \delta$. $\square$

**Proof of (a).** By (1) and $\sum_k b_{n,k}(x) = 1$, $B_n f(x) - f(x) = \mathbb{E} \big(f(S/n) - f(x)\big)$. By Lemma 2 and (2),
$$|B_n f(x) - f(x)| \le \mathbb{E} |f(S/n) - f(x)| \le \omega_f(\delta) \Big(1 + \frac{\mathbb{E} |Y|}{\delta}\Big) \le \omega_f(\delta) \Big(1 + \frac{1}{2 \delta \sqrt n}\Big).$$
Take $\delta = n^{-1/2}$. The bound $\frac32 \omega_f(n^{-1/2})$ does not depend on $x$. A continuous function on $[0, 1]$ is uniformly continuous, so $\omega_f(\delta) \to 0$ as $\delta \to 0$, and $B_n f \to f$ uniformly. $\square$

**Proof of (b).** Let $f \in C^2[0, 1]$. By Taylor's theorem with the Lagrange remainder, for each $y \in [0, 1]$ there is $\xi$ between $x$ and $y$ with
$$f(y) = f(x) + f'(x)(y - x) + \tfrac12 f''(\xi)(y - x)^2. \tag{3}$$
Put $y = S/n$ and take the mean. By Lemma 1, the mean of the linear term is $f'(x)\, \mathbb{E}\, Y = 0$, so
$$|B_n f(x) - f(x)| \le \tfrac12 \lVert f'' \rVert\, \mathbb{E}\, Y^2 = \frac{x (1 - x)}{2n} \lVert f'' \rVert \le \frac{\lVert f'' \rVert}{8n},$$
since $x (1 - x) \le \frac14$. $\square$

**Proof of (c).** Let $f \in C^2[0, 1]$, and write (3) as
$$f(y) = f(x) + f'(x)(y - x) + \tfrac12 f''(x)(y - x)^2 + h(y)(y - x)^2, \qquad h(y) = \tfrac12 \big(f''(\xi) - f''(x)\big).$$
Then $|h(y)| \le \frac12 \omega_{f''}(|y - x|)$, because $|\xi - x| \le |y - x|$, and $|h(y)| \le \lVert f'' \rVert$. Put $y = S/n$, take the mean and multiply by $n$. By Lemma 1,
$$n \big(B_n f(x) - f(x)\big) - \frac{x (1 - x)}{2} f''(x) = n\, \mathbb{E} \big(h(S/n)\, Y^2\big).$$
Fix $\delta > 0$. On the event $|Y| < \delta$, $|h(S/n)| Y^2 \le \frac12 \omega_{f''}(\delta)\, Y^2$. On the event $|Y| \ge \delta$, $|h(S/n)| Y^2 \le \lVert f'' \rVert\, Y^4 / \delta^2$. So, by Lemma 1,
$$\Big| n\, \mathbb{E} \big(h(S/n)\, Y^2\big) \Big| \le \tfrac12 \omega_{f''}(\delta)\, n\, \mathbb{E}\, Y^2 + \frac{\lVert f'' \rVert}{\delta^2}\, n\, \mathbb{E}\, Y^4 \le \tfrac18 \omega_{f''}(\delta) + \frac{7 \lVert f'' \rVert}{16\, n\, \delta^2}.$$
The right side does not depend on $x$. Its limit superior as $n \to \infty$ is at most $\frac18 \omega_{f''}(\delta)$, and this tends to 0 as $\delta \to 0$, because $f''$ is uniformly continuous. So the convergence is uniform in $x$. $\square$

**Proof of (d).** Let $f \in C^1[0, 1]$ and $n \ge 2$. By the derivative rule of the Bernstein basis, $b_{n,k}' = n (b_{n-1,k-1} - b_{n-1,k})$ with $b_{n-1,-1} = b_{n-1,n} = 0$ (property of [Bernstein polynomials](/bernstein-polynomials/)). Collect the coefficient of $b_{n-1,k}$:
$$(B_n f)'(x) = \sum_{k=0}^{n-1} n \Big(f\big(\tfrac{k+1}{n}\big) - f\big(\tfrac{k}{n}\big)\Big) b_{n-1,k}(x).$$
By the mean value theorem, $n \big(f(\frac{k+1}{n}) - f(\frac kn)\big) = f'(\xi_k)$ for some $\xi_k \in (\frac kn, \frac{k+1}{n})$. For $0 \le k \le n - 1$, $\frac kn \le \frac{k}{n-1} \le \frac{k+1}{n}$, because the first inequality is $k (n - 1) \le k n$ and the second is $k n \le (k + 1)(n - 1)$, that is, $k \le n - 1$. So $|\xi_k - \frac{k}{n-1}| \le \frac1n$ and $|f'(\xi_k) - f'(\frac{k}{n-1})| \le \omega_{f'}(\frac1n)$. Since the $b_{n-1,k}(x)$ are nonnegative with sum 1,
$$\big|(B_n f)'(x) - B_{n-1}(f')(x)\big| \le \omega_{f'}(1/n).$$
By part (a) for the continuous function $f'$, $\lVert B_{n-1}(f') - f' \rVert \le \frac32 \omega_{f'}\big((n - 1)^{-1/2}\big)$. Both bounds tend to 0, uniformly in $x$. $\blacksquare$
