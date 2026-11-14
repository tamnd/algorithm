---
title: The Nadaraya-Watson estimate reproduces a constant exactly, stays in the range of the responses, and has a boundary bias of order h
proves: [correctness]
status: full
---

**Setting.** The data are pairs $(x_1, y_1), \ldots, (x_n, y_n)$ with $y_i = m(x_i) + e_i$, where the errors have mean 0. The kernel $K \ge 0$ is symmetric, vanishes outside $[-1, 1]$, and has $\int K = 1$; the Epanechnikov kernel of the code is one. For $h > 0$ and a point $x$ with $D(x) = \sum_j K((x - x_j)/h) > 0$, the estimate is
$$\hat m(x) = \sum_{i=1}^n w_i(x)\,y_i, \qquad w_i(x) = \frac{K((x - x_i)/h)}{D(x)}.$$
Lines L1 to L3 compute the numerator $\sum_i K((x - x_i)/h)\,y_i$ and the denominator $D(x)$, line L4 detects $D(x) = 0$, and line L5 returns their ratio, which is $\hat m(x)$.

## Part 1. Exact properties

**Lemma 1.** The weights are non-negative and sum to 1.

*Proof.* Each $K((x - x_i)/h) \ge 0$, and the sum of the numerators of the $w_i$ is the denominator $D(x) > 0$. $\square$

**Theorem 2 (a constant is reproduced exactly).** If $y_i = c$ for all $i$, then $\hat m(x) = c$ at every $x$ where the estimate is defined.

*Proof.* $\hat m(x) = \sum_i w_i(x)\,c = c\sum_i w_i(x) = c$ by Lemma 1. $\square$

The test file checks Theorem 2 in exact rational arithmetic on random designs.

**Corollary 3.** $\min_i y_i \le \hat m(x) \le \max_i y_i$, and adding a constant $c$ to every $y_i$ adds $c$ to $\hat m(x)$.

*Proof.* By Lemma 1, $\hat m(x)$ is a convex combination of the $y_i$. The second claim is Theorem 2 plus the linearity of $\hat m$ in $y$. $\square$

A line is not reproduced in general. With $m(x) = a + bx$ and no noise, $\hat m(x) - m(x) = b\sum_i w_i(x)(x_i - x)$, which is 0 only when the weighted mean of the $x_i$ is $x$. That holds when the design is symmetric around $x$ within distance $h$, as at the interior grid points of an equally spaced design, but it fails near the ends of the data.

**Lemma 4 (the leave-one-out shortcut).** Let $N_i$ and $D_i$ be the numerator and denominator at $x = x_i$ with all points. Then the estimate at $x_i$ without point $i$ is $(N_i - K(0)\,y_i)/(D_i - K(0))$, when $D_i > K(0)$.

*Proof.* Point $i$ contributes $K((x_i - x_i)/h)\,y_i = K(0)\,y_i$ to $N_i$ and $K(0)$ to $D_i$. $\square$

## Part 2. Bias at the boundary and in the interior

Take the equally spaced design $x_i = i/N$, $i = 0, \ldots, N$, on $[0, 1]$, so $n = N + 1$. The weights depend only on the design, so $\mathbb{E}\,\hat m(x) = \sum_i w_i(x)\,m(x_i)$, and the bias is $\sum_i w_i(x)\big(m(x_i) - m(x)\big)$. Let
$$\mu_k^+ = \int_0^1 u^k K(u)\,du, \qquad \mu_0^+ = \tfrac12, \qquad \mu_1^+ > 0.$$

**Lemma 5 (Riemann sums).** Let $\delta = 1/(Nh)$ and $S_k = \delta\sum_{i \ge 0,\ i\delta \le 1} K(i\delta)\,(i\delta)^k$ for $k = 0, 1$. Then $|S_k - \mu_k^+| \le \delta\,(V + 2M)$, where $V$ is the total variation of $u^k K(u)$ on $[0, 1]$ and $M = \sup K$.

*Proof.* Let $g(u) = u^k K(u)$ on $[0, 1]$ and let $J$ be the largest $i$ with $i\delta \le 1$. On each cell $[i\delta, (i+1)\delta]$ with $i < J$, $|\delta\,g(i\delta) - \int_{\text{cell}} g| \le \delta \cdot (\text{variation of } g \text{ on the cell})$, and the variations of the cells add up to at most $V$. The last term $\delta\,g(J\delta)$ and the integral over $[J\delta, 1]$, a piece of length less than $\delta$, each add at most $\delta M$. $\square$

**Theorem 6 (boundary bias of order $h$).** Let $m$ have a bounded second derivative on $[0, 1]$. Then at the end point $x = 0$,
$$\mathbb{E}\,\hat m(0) - m(0) = h\,m'(0)\,\frac{\mu_1^+}{\mu_0^+} + O\!\left(h^2 + \frac{1}{N}\right).$$
So if $m'(0) \ne 0$, the bias is of exact order $h$ as $h \to 0$ and $Nh \to \infty$. For the Epanechnikov kernel, $\mu_1^+ = \frac34\left(\frac12 - \frac14\right) = \frac3{16}$ and the factor is $\mu_1^+/\mu_0^+ = \frac38$.

*Proof.* Only the points with $x_i \le h$ have weight. By Taylor's theorem, $m(x_i) - m(0) = m'(0)\,x_i + r_i$ with $|r_i| \le \frac12\sup|m''|\,x_i^2 \le \frac12\sup|m''|\,h^2$. With Lemma 1,
$$\sum_i w_i(0)\big(m(x_i) - m(0)\big) = m'(0)\sum_i w_i(0)\,x_i + O(h^2).$$
Write $x_i = h\cdot(i\delta)$ with $\delta = 1/(Nh)$. Then $\sum_i w_i(0)\,x_i = h\,S_1/S_0$, with $S_0, S_1$ as in Lemma 5. Lemma 5 gives $S_k = \mu_k^+ + O(\delta)$, and $\mu_0^+ = \frac12$, so $S_1/S_0 = \mu_1^+/\mu_0^+ + O(\delta)$. Multiplying by $h$ turns $O(\delta)$ into $O(h\delta) = O(1/N)$. $\square$

The reason is plain: at the end of the data, all the points with weight lie on one side of $x$, so their weighted mean is about $0.375\,h$ away from $x$, and a sloped $m$ is evaluated there instead of at $x$. The test file measures the ratio of the bias to $b h$ for $m(x) = 2 - 3x$: 0.3722 for $N = 1000$, $h = 0.1$ and 0.3736 for $N = 4000$, $h = 0.05$, against the limit 0.375. For the Gaussian kernel, which is not compactly supported, the same computation gives the factor $\int_0^\infty u\varphi(u)\,du / \frac12 = \sqrt{2/\pi} \approx 0.798$; the test checks this too.

**Theorem 7 (interior bias of order $h^2$ on a symmetric design).** If $x = x_k$ is a design point with $h \le x \le 1 - h$, then $\mathbb{E}\,\hat m(x) - m(x) = O(h^2)$, and the bias is 0 when $m$ is linear.

*Proof.* The points with weight are $x_{k \pm j}$ with $j/N < h$, and $K$ is symmetric, so $w_{k+j}(x) = w_{k-j}(x)$ and $\sum_i w_i(x)(x_i - x) = 0$. So the linear term of the Taylor expansion cancels, and what remains is at most $\frac12\sup|m''|\,h^2$. If $m$ is linear, nothing remains. $\square$

## What is cited, not proved

For a random design with density $f$, the interior bias is $h^2\mu_2\big(\tfrac12 m''(x) + m'(x)f'(x)/f(x)\big) + o(h^2)$ and the variance is $\sigma^2(x)\,R(K)/(nh f(x)) + o(1/(nh))$ (Wand and Jones 1995, Chapter 5; Fan and Gijbels 1996, Chapter 3). The term $m'f'/f$, the design bias, is absent for a uniform design, as in Theorem 7. For a random design the boundary result of Theorem 6 holds in probability, with the same factor $\mu_1^+/\mu_0^+$, when $f$ is continuous and positive at the end point. The test file measures the interior bias of $m(x) = x^2$ on the uniform design: the ratio of the bias to $h^2$ was 0.19998 and 0.199995, against $\mu_2 m''/2 = 1/5$.

## Cost

Lines L1 to L5 make one pass over the data, with $O(1)$ work for each point, so the estimate at one point takes $O(n)$ time and $O(1)$ extra space. The leave-one-out score takes $O(n^2)$ time by Lemma 4.
