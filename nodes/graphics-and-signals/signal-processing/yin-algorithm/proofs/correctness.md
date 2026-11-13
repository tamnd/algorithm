---
title: What the steps of YIN compute, and when the estimate is exact
proves: [correctness]
status: full
---

YIN is an estimator, so its correctness has two parts: each line computes the quantity the page names, and on two families of periodic signals the returned value is the exact period. We work in the real RAM, so sums and divisions are exact. The samples $x[t \ldots t + W + T - 1]$ exist, $W \ge 1$ and $T \ge 1$.

**Lemma 1 (the difference function).** For $0 \le \tau \le T$, with $e(s) = \sum_{j=s}^{s+W-1} x[j]^2$ and $r_t(\tau) = \sum_{j=t}^{t+W-1} x[j]\, x[j + \tau]$,

$$d(\tau) = \sum_{j=t}^{t+W-1} (x[j] - x[j+\tau])^2 = e(t) + e(t + \tau) - 2 r_t(\tau).$$

*Proof.* Expand $(x[j] - x[j+\tau])^2 = x[j]^2 + x[j+\tau]^2 - 2x[j]\,x[j+\tau]$ and sum over $t \le j \le t + W - 1$. The first terms sum to $e(t)$. The second terms sum to $\sum_{i=t+\tau}^{t+\tau+W-1} x[i]^2 = e(t + \tau)$. The third terms sum to $-2r_t(\tau)$. $\square$

So line L1 computes $d$ by either form, and the implementation checks the two forms against each other.

**Lemma 2 (the normalization).** After line L5, for $1 \le \tau \le T$, $d'(\tau) = \tau\, d(\tau) / \sum_{j=1}^{\tau} d(j)$ when the sum is positive and $d'(\tau) = 1$ otherwise. Also $0 \le d'(\tau) \le \tau$, and $d'(1) = 1$.

*Proof.* By induction on $\tau$, after line L4 in round $\tau$ the variable $S$ is $\sum_{j=1}^{\tau} d(j)$: it starts at 0 and line L4 adds $d(\tau)$ in round $\tau$. Line L5 then stores the stated value. Each $d(j) \ge 0$, as a sum of squares, so $S \ge d(\tau) \ge 0$, which gives $0 \le \tau d(\tau) / S \le \tau$. For $\tau = 1$, $S = d(1)$, so $d'(1) = 1$ in both cases. $\square$

**Lemma 3 (the choice of lag).** Lines L6 to L8 return a lag $1 \le \tau^* \le T$. If some $\tau$ has $d'(\tau) < \theta$, then $\tau^*$ is the end of the run of strict decreases of $d'$ that starts at the smallest such $\tau$, so $\tau^* = T$ or $d'(\tau^* + 1) \ge d'(\tau^*)$. Otherwise $\tau^*$ is the smallest lag at which $d'$ takes its minimum over $1 \le \tau \le T$.

*Proof.* Line L6 searches a finite range. The loop of line L7 increases $\tau^*$ by one while $\tau^* < T$, so it stops after at most $T - 1$ rounds, and it stops exactly when $\tau^* = T$ or $d'(\tau^* + 1) \ge d'(\tau^*)$. Line L8 is the definition. $\square$

**Lemma 4 (the parabola).** If $1 \le \tau^* < T$ and $a = d(\tau^* - 1) - 2d(\tau^*) + d(\tau^* + 1) \ne 0$, line L10 returns the abscissa of the vertex of the parabola through the points $(\tau^* + u, d(\tau^* + u))$ for $u = -1, 0, 1$.

*Proof.* Write the parabola as $p(u) = \alpha u^2 + \beta u + \gamma$. From $p(-1) = d(\tau^* - 1)$, $p(0) = d(\tau^*)$ and $p(1) = d(\tau^* + 1)$, we get $\gamma = d(\tau^*)$, $2\alpha = a$ and $2\beta = d(\tau^* + 1) - d(\tau^* - 1)$. With $\alpha \ne 0$, the vertex is at $u = -\beta / (2\alpha) = (d(\tau^* - 1) - d(\tau^* + 1)) / (2a)$, so its abscissa is $\tau^*$ plus this number, as in line L10. $\square$

**Lemma 5 (periodic signals).** Suppose $x[n + Q] = x[n]$ for every index $n$ in use, for an integer $Q \ge 1$, and $W$ is a multiple of $Q$. Then, for the lags in the range,

1. $d(\tau + Q) = d(\tau)$, and in particular $d(kQ) = 0$;
2. $d(Q - \tau) = d(\tau)$ for $0 \le \tau \le Q$.

*Proof.* Extend $x$ to all integers with period $Q$; it agrees with the given samples. For any $Q$-periodic $f$, the sum $\sum_{j=s}^{s+W-1} f(j)$ does not depend on $s$, because $W$ consecutive integers contain each residue modulo $Q$ exactly $W/Q$ times. Item 1: $x[j + \tau + Q] = x[j + \tau]$, so the summands are equal; and $d(0) = 0$. Item 2: $x[j + Q - \tau] = x[j - \tau]$, so $d(Q - \tau) = \sum_{j=t}^{t+W-1} (x[j] - x[j - \tau])^2$. The summand $f(j) = (x[j] - x[j - \tau])^2$ is $Q$-periodic, so the sum equals the sum of $f(j + \tau) = (x[j + \tau] - x[j])^2$ over the same range, which is $d(\tau)$. $\square$

**Lemma 6 (no early zero).** If $P$ is the smallest period of $x$ and $W \ge P$, then $d(\tau) > 0$ for $0 < \tau < P$.

*Proof.* If $d(\tau) = 0$, then $x[j + \tau] = x[j]$ for the $W \ge P$ consecutive indices $t \le j \le t + W - 1$. These indices cover every residue modulo $P$, so by periodicity $x[n + \tau] = x[n]$ for every $n$, and $\tau$ is a period. Then $\gcd(\tau, P)$ is a period, because the periods of a sequence on the integers are closed under the integer combinations given by Bezout's identity. Since $0 < \tau < P$, $\gcd(\tau, P) < P$, which contradicts the choice of $P$. $\square$

**Theorem 1 (integer period).** Let $P$ be the smallest period of $x$, with $2 \le P < T$, and let $W$ be a multiple of $P$. If lines L6 to L8 give $\tau^* = P$, YIN returns exactly $P$. Line L8 alone always gives $\tau^* = P$.

*Proof.* By Lemma 5 with $Q = P$, $d(P) = 0$, $d(P + 1) = d(1)$ and $d(P - 1) = d(1)$. So $a = 2d(1)$, which is positive by Lemma 6. Lemma 4 gives $P + (d(1) - d(1)) / (2a) = P$. For line L8: by Lemmas 2 and 6, $d'(\tau) > 0$ for $1 \le \tau < P$, because the sum in Lemma 2 is positive and $d(\tau) > 0$; and $d'(P) = 0$. So the smallest minimizer of $d'$ is $P$. $\square$

**Theorem 2 (half-integer period).** Let $x$ have period $Q$ with $W$ a multiple of $Q$, let $Q = 2m + 1$ be odd with $1 \le m < T$, and suppose lines L6 to L8 give $\tau^* = m$ and $d(m - 1) \ne d(m)$. Then YIN returns exactly $m + \frac{1}{2} = Q/2$.

*Proof.* By Lemma 5 item 2 with $\tau = m$, $d(m + 1) = d(Q - m) = d(m)$. So $a = d(m - 1) - d(m) \ne 0$, and Lemma 4 gives $m + (d(m - 1) - d(m)) / (2(d(m - 1) - d(m))) = m + \frac{1}{2}$. $\square$

The example on the page is Theorem 2 with $Q = 21$ and $m = 10$, where line L6 gives 10 because $d'(10) < 0.1$ and $d'(\tau) \ge 0.1$ for $\tau < 10$.

**What is not proved.** Whether line L6 finds the right dip depends on the threshold and on the signal; there is no condition on general signals that makes it do so. For signals that are not periodic over the frame, the parabola is only an approximation. The paper's support for the method is its measured error rates, not a theorem.
