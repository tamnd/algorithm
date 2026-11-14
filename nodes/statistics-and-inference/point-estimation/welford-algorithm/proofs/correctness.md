---
title: Welford's algorithm returns the mean and the sum of squared deviations
proves: [correctness]
status: full
---

The arithmetic is exact. For $1 \le k \le n$ write $\bar x_k = \frac1k \sum_{i=1}^k x_i$ for the mean of the first $k$ values and $\mathrm{SS}_k = \sum_{i=1}^k (x_i - \bar x_k)^2$ for their sum of squared deviations. $M_k$ and $S_k$ are the values of $M$ and $S$ after iteration $k$ of the loop of line L2, and $M_0 = S_0 = 0$ are the values set in line L1.

**Lemma 1 (shift).** For $k \ge 1$ and every real $c$,
$$\sum_{i=1}^k (x_i - c)^2 = \mathrm{SS}_k + k(\bar x_k - c)^2.$$

*Proof.* Write $x_i - c = (x_i - \bar x_k) + (\bar x_k - c)$ and expand the square. The sum of the cross terms is $2(\bar x_k - c)\sum_{i=1}^k (x_i - \bar x_k) = 2(\bar x_k - c)(k\bar x_k - k\bar x_k) = 0$, and the last terms add up to $k(\bar x_k - c)^2$. $\square$

**Lemma 2 (mean).** $M_k = \bar x_k$ for $1 \le k \le n$.

*Proof.* By induction on $k$. For $k = 1$, line L3 gives $d = x_1 - 0$ and line L4 gives $M_1 = 0 + x_1/1 = x_1 = \bar x_1$. For $k \ge 2$, assume $M_{k-1} = \bar x_{k-1}$. Lines L3 and L4 give
$$M_k = M_{k-1} + \frac{x_k - M_{k-1}}{k} = \frac{(k-1)\bar x_{k-1} + x_k}{k} = \frac1k \sum_{i=1}^k x_i = \bar x_k. \qquad \square$$

**Lemma 3 (one step).** Let $2 \le k \le n$ and $d = x_k - \bar x_{k-1}$. Then
$$\mathrm{SS}_k = \mathrm{SS}_{k-1} + d\,(x_k - \bar x_k) = \mathrm{SS}_{k-1} + \frac{k-1}{k} d^2.$$

*Proof.* Lemma 1 for the first $k - 1$ values with $c = \bar x_k$ gives $\sum_{i=1}^{k-1}(x_i - \bar x_k)^2 = \mathrm{SS}_{k-1} + (k-1)(\bar x_{k-1} - \bar x_k)^2$. Add the term $i = k$:
$$\mathrm{SS}_k = \mathrm{SS}_{k-1} + (k-1)(\bar x_k - \bar x_{k-1})^2 + (x_k - \bar x_k)^2.$$
The computation in Lemma 2 shows $\bar x_k - \bar x_{k-1} = d/k$, so $x_k - \bar x_k = d - d/k = (k-1)d/k$. The two added terms are
$$(k-1)\frac{d^2}{k^2} + \frac{(k-1)^2 d^2}{k^2} = \frac{(k-1)d^2}{k^2}\,(1 + k - 1) = \frac{(k-1)d^2}{k} = d \cdot \frac{(k-1)d}{k} = d\,(x_k - \bar x_k). \qquad \square$$

**Theorem.** Let $n \ge 2$. After iteration $k$ of the loop, $M = \bar x_k$ and $S = \mathrm{SS}_k$, for $k = 1, \ldots, n$. So WELFORD returns $M = \bar x_n$, $S = \mathrm{SS}_n$ and $V = \mathrm{SS}_n/(n-1)$, the [sample variance](/sample-variance/) $S^2$.

*Proof.* $M_k = \bar x_k$ is Lemma 2. For $S$, use induction on $k$. For $k = 1$, line L5 gives $S_1 = 0 + d\,(x_1 - M_1) = d \cdot 0 = 0 = \mathrm{SS}_1$, since $M_1 = x_1$. For $k \ge 2$, assume $S_{k-1} = \mathrm{SS}_{k-1}$. In iteration $k$, line L3 computes $d = x_k - M_{k-1} = x_k - \bar x_{k-1}$ by Lemma 2, and line L5 computes $S_k = S_{k-1} + d\,(x_k - M_k) = \mathrm{SS}_{k-1} + d\,(x_k - \bar x_k)$, which is $\mathrm{SS}_k$ by Lemma 3. The loop runs exactly $n$ times, so it ends with $k = n$, and lines L6 and L7 return $V = \mathrm{SS}_n/(n - 1)$, which is defined because $n \ge 2$. $\square$

**Corollary (monotone and nonnegative).** In exact arithmetic each increment of line L5 is $\frac{k-1}{k}d^2 \ge 0$, so $S_1 \le S_2 \le \cdots \le S_n$ and $V \ge 0$. The textbook formula $\sum_i x_i^2 - n\bar x^2$ has the same value, but it is a difference, and in floating point it can be negative.

**Termination and cost.** The loop has $n$ iterations, and each iteration runs lines L3 to L5 once: one subtraction in L3, one division and one addition in L4, and one subtraction, one multiplication and one addition in L5, so 6 arithmetic operations. Line L6 adds one division. The total is $6n + 1$ operations, and the extra storage is the three numbers $M$, $S$ and $d$ and the counter $k$. $\square$
