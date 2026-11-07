---
title: Neumaier summation is as accurate as summation in twice the working precision
proves: [correctness]
status: full
---

**Setting.** Binary floating-point arithmetic with round to nearest (any tie rule), subnormal numbers and no overflow; $u = 2^{-p}$. Every addition and subtraction satisfies $\mathrm{fl}(a \pm b) = (a \pm b)(1 + \delta)$ with $|\delta| \le u$, and is exact if its result is subnormal. $\gamma_k = ku/(1 - ku)$ for $ku < 1$, with $\gamma_0 = 0$; $\gamma_k$ is increasing in $k$.

**The iteration.** Let $t_0 = 0$ and, for $i = 1, \ldots, n$, $t_i = \mathrm{fl}(t_{i-1} + x_i)$ and $q_i = \mathrm{fl}(\mathrm{fl}(a - t_i) + b)$, where $(a, b) = (t_{i-1}, x_i)$ if $|t_{i-1}| \ge |x_i|$ and $(a, b) = (x_i, t_{i-1})$ otherwise. Let $c_0 = 0$, $c_i = \mathrm{fl}(c_{i-1} + q_i)$, and $\hat s = \mathrm{fl}(t_n + c_n)$. Let $A = \sum_{i=1}^n |x_i|$, $s = \sum_{i=1}^n x_i$, and assume $(n - 1)u < 1$.

**Theorem.** $q_i = t_{i-1} + x_i - t_i$ exactly for every $i$, $s = t_n + \sum_{i=1}^n q_i$, and

$$|\hat s - s| \le u|s| + (1 + u)\gamma_{n-2}\gamma_{n-1} A.$$

If moreover $n(n - 2)u \le 1$, then $|\hat s - s| \le u|s| + \gamma_{n-1}^2 A$.

**Step 1 (exact errors).** If $|a| \ge |b|$ then $e_a \ge e_b$, so by the theorem on [Fast2Sum](/fast-two-sum/), $\mathrm{fl}(a - t_i) = a - t_i$ and the error $b - (t_i - a)$ is a float; here the algorithm computes $\mathrm{fl}((a - t_i) + b)$, which is that same float, so $q_i = a + b - t_i = t_{i-1} + x_i - t_i$. Summing over $i$ telescopes: $\sum_i q_i = \sum_i x_i + t_0 - t_n = s - t_n$.

**Step 2 (size of the errors).** $q_i$ is the rounding error of $t_i = \mathrm{fl}(t_{i-1} + x_i)$, so $|q_i| \le u|t_i|$ (if $t_i$ is normal, $|q_i| \le \tfrac12\mathrm{ulp}(t_i) \le u|t_i|$; if $t_i$ is subnormal, the addition is exact and $q_i = 0$). Also $q_1 = 0$, since $t_0 = 0$ makes the first addition exact. The $t_i$ are the partial sums of a plain loop, and by the standard analysis of recursive summation (Higham, Section 4.2, from Lemma 3.1), $t_i = \sum_{j \le i} x_j (1 + \theta^{(i)}_j)$ with $|\theta^{(i)}_j| \le \gamma_{i-1}$, so $|t_i| \le (1 + \gamma_{i-1})\sum_{j \le i}|x_j| \le (1 + \gamma_{n-1})A$. Hence

$$Q := \sum_{i=1}^n |q_i| = \sum_{i=2}^n |q_i| \le (n - 1)u(1 + \gamma_{n-1})A = \gamma_{n-1}A,$$

because $(n - 1)u(1 + \gamma_{n-1}) = (n - 1)u/(1 - (n - 1)u) = \gamma_{n-1}$.

**Step 3 (summing the errors).** Since $q_1 = 0$, $c_1 = 0$ and $c_2 = q_2$ exactly, and $c_n$ is a plain loop over the $n - 1$ terms $q_2, \ldots, q_n$, which makes $n - 2$ rounded additions. By the same analysis, $|c_n - \sum_i q_i| \le \gamma_{n-2} Q \le \gamma_{n-2}\gamma_{n-1}A$. (For $n \le 2$ this error is $0$.)

**Step 4 (the final addition).** Let $E = c_n - \sum_i q_i$. Then $t_n + c_n = s + E$ by Step 1, and $\hat s = (s + E)(1 + \delta)$ with $|\delta| \le u$. So

$$|\hat s - s| = |\delta s + (1 + \delta)E| \le u|s| + (1 + u)|E| \le u|s| + (1 + u)\gamma_{n-2}\gamma_{n-1}A.$$

**Step 5 (the simpler form).** It suffices that $(1 + u)\gamma_{n-2} \le \gamma_{n-1}$ for $n \ge 3$ (for $n \le 2$ the left side is $0$). Multiplying out with the positive denominators, this is $(n - 2)(1 + u)(1 - (n - 1)u) \le (n - 1)(1 - (n - 2)u)$. The left side is at most $(n - 2)(1 + u) = n - 2 + (n - 2)u$, and the inequality $n - 2 + (n - 2)u \le n - 1 - (n - 1)(n - 2)u$ is equivalent to $n(n - 2)u \le 1$. $\square$

**Remark.** The theorem needs no assumption on the order or the signs of the terms. It says that $\hat s$ is the rounding of a value within $\gamma_{n-1}^2 A$ (to first order, $n^2 u^2 A$) of $s$, which is what a plain loop in a format with unit roundoff $u^2$ would guarantee, up to the constant.
