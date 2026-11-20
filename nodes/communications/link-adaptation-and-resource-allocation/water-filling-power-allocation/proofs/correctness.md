---
title: Water-filling is the unique optimal power allocation, and WATER-FILL finds its water level
proves: [correctness]
status: full
---

The levels are $\nu_1, \ldots, \nu_N > 0$ and the power is $P > 0$. The problem is

$$\max_{p} \; R(p) = \sum_{i=1}^{N} \log_2\!\left(1 + \frac{p_i}{\nu_i}\right) \quad \text{subject to} \quad \sum_{i=1}^N p_i \le P, \quad p_i \ge 0. \tag{1}$$

**Lemma 1 (existence and uniqueness).** Problem (1) has exactly one optimal point.

*Proof.* The feasible set is closed, bounded and not empty, and $R$ is continuous on it, so a maximum exists. Each term $\log_2(1 + p_i/\nu_i)$ is strictly concave in $p_i$ on $p_i > -\nu_i$, so $R$ is strictly concave. If $p \ne q$ were both optimal, the midpoint would be feasible, because the set is convex, and would give $R((p+q)/2) > (R(p) + R(q))/2 = R(p)$, a contradiction. $\square$

**Lemma 2 (KKT form).** A feasible $p$ is optimal if and only if there is a $\mu > 0$ with $p_i = \max(0, \mu - \nu_i)$ for every $i$ and $\sum_i p_i = P$.

*Proof.* The objective is concave and differentiable on a neighborhood of the feasible set, the constraints are affine, and the point $p_i = P/(2N)$ satisfies all of them strictly. So Slater's condition holds, and the [KKT conditions](/kkt-conditions/) are necessary and sufficient for optimality. With the multiplier $\lambda \ge 0$ for the sum constraint and $\kappa_i \ge 0$ for $p_i \ge 0$, they read

$$\frac{1}{(\nu_i + p_i)\ln 2} = \lambda - \kappa_i, \qquad \kappa_i p_i = 0, \qquad \lambda\Big(\sum_i p_i - P\Big) = 0.$$

The left side is positive, so $\lambda > \kappa_i \ge 0$, and then the sum constraint holds with equality. Put $\mu = 1/(\lambda \ln 2) > 0$. If $p_i > 0$, then $\kappa_i = 0$ and $\nu_i + p_i = \mu$, so $p_i = \mu - \nu_i > 0$. If $p_i = 0$, then $1/(\nu_i \ln 2) = \lambda - \kappa_i \le \lambda$, so $\nu_i \ge \mu$ and $\max(0, \mu - \nu_i) = 0 = p_i$. In both cases $p_i = \max(0, \mu - \nu_i)$.

Conversely, let $p_i = \max(0, \mu - \nu_i)$ with $\sum p_i = P$ and $\mu > 0$. Set $\lambda = 1/(\mu \ln 2)$, $\kappa_i = 0$ where $\nu_i < \mu$, and $\kappa_i = \lambda - 1/(\nu_i \ln 2) \ge 0$ where $\nu_i \ge \mu$. Then all KKT conditions hold, so $p$ is optimal. $\square$

**Lemma 3 (the water level).** Let $f(t) = \sum_i \max(0, t - \nu_i)$ and let $s[1] \le \cdots \le s[N]$ be the sorted levels. Then $f(s[1]) = 0$, $f$ is continuous, and $f$ is strictly increasing on $[s[1], \infty)$ with $f(t) \to \infty$. So there is exactly one $\mu$ with $f(\mu) = P$, and $\mu > s[1]$.

*Proof.* Each term is continuous and nondecreasing, and the term of $s[1]$ equals $t - s[1]$, which is strictly increasing and unbounded. At $t = s[1]$ every term is 0. The intermediate value theorem gives a solution of $f(\mu) = P$ in $(s[1], s[1] + P]$, and strict monotonicity makes it unique. $\square$

By Lemmas 1 to 3, the unique optimum is $p_i = \max(0, \mu - \nu_i)$ with the $\mu$ of Lemma 3. It remains to show that WATER-FILL computes this $\mu$.

**Lemma 4 (the test of line L3).** For $0 \le k < N$, let $S_k = s[1] + \cdots + s[k]$. Then $f(s[k+1]) = k\, s[k+1] - S_k$, and the test $k\, s[k+1] < P + S_k$ holds if and only if $s[k+1] < \mu$.

*Proof.* For $j \le k$, $s[j] \le s[k+1]$, so the term is $s[k+1] - s[j]$. For $j > k$, $s[j] \ge s[k+1]$, so the term is 0. Summing gives the formula. The test is therefore $f(s[k+1]) < P = f(\mu)$. Since $s[k+1] \ge s[1]$ and $f$ is strictly increasing on $[s[1], \infty)$, this holds if and only if $s[k+1] < \mu$. $\square$

**Theorem.** WATER-FILL returns the unique optimal powers of (1) and the water level $\mu$.

*Proof.* Let $k^* = |\{j : s[j] < \mu\}|$. By Lemma 3, $s[1] < \mu$, so $k^* \ge 1$. Because the list is sorted, $s[j] < \mu$ exactly for $j \le k^*$. Invariant of the loop: at the start of each test, $S = S_k$ and $k \le k^*$. It holds at the start with $k = 0$. If $k < k^*$, then $s[k+1] < \mu$, and by Lemma 4 the test is true, so the body runs and keeps the invariant with $k + 1 \le k^*$. If $k = k^* < N$, then $s[k+1] \ge \mu$, and the test is false. If $k = N$, the loop stops by its first condition. So the loop stops with $k = k^*$ after $k^*$ iterations. Then

$$P = f(\mu) = \sum_{j \le k^*} (\mu - s[j]) = k^* \mu - S_{k^*},$$

so $\mu = (P + S)/k$, which is line L5. Line L6 forms $p_i = \max(0, \mu - \nu_i)$, the optimum by Lemmas 1 and 2. $\square$

**Remark (termination and cost).** The loop variable $k$ grows by 1 in each iteration and is at most $N$, so the loop stops after at most $N$ iterations of constant work. The sort of line L1 costs $O(N \log N)$ comparisons, and lines L5 and L6 cost $O(N)$.

**Remark (the rate).** At the optimum, the active channels have $1 + p_i/\nu_i = \mu/\nu_i$, so $R = \sum_{j \le k^*} \log_2(\mu/s[j])$. For $\nu = (1, 2, 4)$ and $P = 3$ this is $\log_2 3 + \log_2 1.5$.
