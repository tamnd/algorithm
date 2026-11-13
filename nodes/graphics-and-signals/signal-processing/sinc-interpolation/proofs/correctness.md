---
title: Sinc interpolation computes the truncated cardinal series, which converges to every band-limited signal
proves: [correctness]
status: full
---

We write $u = t/T$, $W = \{n_0, \ldots, n_0 + N - 1\}$ for the window of sample indices, $x[n] = x(nT)$, and $S(t) = \sum_{n \in W} x[n]\, \mathrm{sinc}(u - n)$ with $\mathrm{sinc}(v) = \sin(\pi v)/(\pi v)$ and $\mathrm{sinc}(0) = 1$. The array of the pseudocode holds $x[n_0 + j]$ at position $j$.

**Lemma 1 (the procedure returns $S(t)$).** SINC-INTERPOLATE$(x, n_0, T, t)$ returns $S(t)$, in exact arithmetic, and never divides by zero.

*Proof.* Line L1 sets $u = t/T$. Two cases.

*Case 1: $u$ is an integer $m \in W$.* Line L2 returns $x[m]$. In $S(t)$ the term $n = m$ is $x[m]\,\mathrm{sinc}(0) = x[m]$, and each term with $n \ne m$ is $x[n] \sin(\pi(m - n))/(\pi(m - n)) = 0$, since $m - n$ is a nonzero integer. So $S(t) = x[m]$.

*Case 2: otherwise.* Then $u \ne n$ for every $n \in W$: either $u$ is not an integer, or it is an integer outside $W$. Line L3 sets $s = 0$. We use the invariant: before the iteration of line L4 with index $j$, $s = \sum_{k < j} x[n_0 + k]\, \mathrm{sinc}(u - n_0 - k)$. It holds for $j = 0$, as the sum is empty. In the iteration, line L5 sets $v = u - (n_0 + j) \ne 0$, so the division in line L6 is defined, and line L6 adds $x[n_0 + j]\,\mathrm{sinc}(v)$, which is the term with index $j$. So the invariant holds for $j + 1$. After the iteration with $j = N - 1$, $s$ is the sum over all of $W$, which line L7 returns. $\square$

**Lemma 2 (the sum of squared shifted sincs).** For every real $u$, $\sum_{n \in \mathbb{Z}} \mathrm{sinc}^2(u - n) = 1$.

*Proof.* The function $y(s) = \mathrm{sinc}(u - s)$ has finite energy and the spectrum $e^{-2\pi i f u}$ for $|f| < 1/2$, zero outside. By the energy identity of the sampling theorem with $T = 1$ (which holds for finite-energy signals with spectrum in $[-1/2, 1/2]$), $\sum_n |y(n)|^2 = \int |y(s)|^2 ds = \int_{-1/2}^{1/2} |e^{-2\pi i f u}|^2 df = 1$. $\square$

**Theorem (convergence and error bound).** Let $x \in L^2(\mathbb{R})$ have its spectrum zero outside $[-1/(2T), 1/(2T)]$. Then for every $t$ and every finite window $W$,

$$|x(t) - S(t)| \le \Big(\sum_{n \notin W} |x[n]|^2\Big)^{1/2} \Big(\sum_{n \notin W} \mathrm{sinc}^2(u - n)\Big)^{1/2} \le \Big(\sum_{n \notin W} |x[n]|^2\Big)^{1/2}.$$

In particular, $S(t) \to x(t)$ uniformly in $t$ as $W$ grows to $\mathbb{Z}$.

*Proof.* By the sampling theorem, $x(t) = \sum_{n \in \mathbb{Z}} x[n]\,\mathrm{sinc}(u - n)$, and $\sum_n |x[n]|^2 < \infty$. By Lemma 2, $\sum_n \mathrm{sinc}^2(u - n)$ is finite, so the Cauchy-Schwarz inequality for sequences applies to the part of the series outside $W$:

$$|x(t) - S(t)| = \Big|\sum_{n \notin W} x[n]\,\mathrm{sinc}(u - n)\Big| \le \Big(\sum_{n \notin W} |x[n]|^2\Big)^{1/2}\Big(\sum_{n \notin W} \mathrm{sinc}^2(u - n)\Big)^{1/2}.$$

The second factor is at most $1$ by Lemma 2. The first factor does not depend on $t$, and it tends to $0$ as $W$ grows, because $\sum_n |x[n]|^2$ converges. $\square$

**Corollary (the $1/N$ rate).** Let $W = \{-N, \ldots, N\}$ and assume $|x[n]| \le C/|n|$ for $n \ne 0$. Fix $u$ with $|u| \le N/2$. Then $|x(t) - S(t)| \le \frac{4C}{\pi N}$ for $N \ge 2$.

*Proof.* $\sum_{|n| > N} C^2/n^2 \le 2C^2 \int_N^\infty ds/s^2 = 2C^2/N$. For $|n| > N$, $|u - n| \ge |n| - N/2 \ge |n|/2$, so $\mathrm{sinc}^2(u - n) \le 1/(\pi^2 (u - n)^2) \le 4/(\pi^2 n^2)$ and $\sum_{|n| > N} \mathrm{sinc}^2(u - n) \le 8/(\pi^2 N)$. The theorem gives $|x(t) - S(t)| \le (2C^2/N)^{1/2}(8/(\pi^2 N))^{1/2} = 4C/(\pi N)$. $\square$

**Remark (the rate is attained).** For $x(t) = \mathrm{sinc}(t - 1/2)$ with $T = 1$, the samples are $x[n] = (-1)^{n+1}/(\pi(n - 1/2))$ and, at $u = 1/2$, $\mathrm{sinc}(1/2 - n) = (-1)^{n+1}/(\pi(n - 1/2))$ as well, so the two sequences in the Cauchy-Schwarz step are equal and the inequality is an equality. The error at $t = 1/2$ is $\sum_{|n| > N} 1/(\pi^2 (n - 1/2)^2) = \frac{2}{\pi^2 N} + O(N^{-2})$. So no bound better than order $1/N$ holds for samples of order $1/n$.
