---
title: The 1/e stopping rule hires the best with probability (r/n) Σ 1/(j − 1), which tends to 1/e
proves: [correctness, success-probability]
status: full
---

Let $C[1 \ldots n]$ hold distinct values, and let $1 \le r \le n$ unless we say otherwise. We call position $i$ a *record* if $C[i] > C[k]$ for each $k < i$.

**Lemma 1 (what the rule does).** ONE-OVER-E with cutoff $r$ returns the least record $i > r$, or none if there is no record after position $r$.

*Proof.* After line L3, $best = \max(C[1], \ldots, C[r])$ (or $-\infty$ if $r = 0$), and the loop of line L4 does not change $best$. Let $i > r$ be the first position with $C[i] > best$, if one exists; line L5 returns it. Each position $k$ with $r < k < i$ has $C[k] < best$, because the loop did not stop there and the values are distinct. So $C[i]$ is larger than each of $C[1 \ldots r]$ and each of $C[r+1 \ldots i-1]$, and $i$ is a record. A record $i' > r$ with $i' < i$ cannot exist, because a record beats $best$ and line L5 would have stopped at $i'$. If no position after $r$ beats $best$, there is no record after $r$, because a record after $r$ beats the first $r$ values, and line L6 returns none. $\square$

**Lemma 2 (the event of success).** Let $j$ be the position of the maximum of $C$. The rule hires the maximum if and only if $j > r$ and the maximum of $C[1 \ldots j-1]$ is at a position at most $r$.

*Proof.* If $j \le r$, then no later value beats $best = C[j]$, so the rule hires nobody. Let $j > r$. If the maximum of $C[1 \ldots j-1]$ is at a position $m \le r$, then each position strictly between $r$ and $j$ holds a value less than $C[m] \le best$, so it is not a record, while $j$ is a record. By Lemma 1 the rule returns $j$. If instead $m > r$, then $r < m < j$ and $m$ is a record, since $C[m]$ is the largest of $C[1 \ldots j-1]$. By Lemma 1 the rule returns a position at most $m < j$, which is not the maximum. $\square$

**Theorem.** If the order of $C$ is uniformly random, the rule with cutoff $r$ hires the maximum with probability

$$P_n(r) = \frac{r}{n} \sum_{j=r+1}^{n} \frac{1}{j-1} \quad \text{for } 1 \le r \le n - 1, \qquad P_n(0) = \frac1n, \qquad P_n(n) = 0.$$

*Proof.* For $r = 0$ the rule hires $C[1]$, which is the maximum with probability $1/n$. For $r = n$ it hires nobody. Let $1 \le r \le n-1$. The maximum is at position $j$ with probability $1/n$ for each $j$. Fix $j \ge r + 1$, so $j \ge 2$. Given that the maximum is at $j$, the other $n - 1$ values fill the other $n - 1$ positions in a uniformly random order, because each of the $(n-1)!$ arrangements comes from exactly one permutation with the maximum at $j$. The transposition of positions $p$ and $q$ (both less than $j$) is a bijection on these arrangements that moves the maximum of $C[1 \ldots j-1]$ from $p$ to $q$. So this maximum is at each of the $j - 1$ positions with probability $1/(j-1)$, and it is at a position at most $r$ with probability $r/(j-1)$. By Lemma 2 and the law of total probability,

$$P_n(r) = \sum_{j=r+1}^{n} \frac1n \cdot \frac{r}{j-1}. \qquad \square$$

**Corollary (bounds and the limit).** For $1 \le r \le n - 1$, let $x = r/n$. Then

$$-x \ln x \;\le\; P_n(r) \;\le\; \frac1n - x \ln x \;\le\; \frac1e + \frac1n,$$

and $P_n(\lfloor n/e \rfloor) \to 1/e$ as $n \to \infty$.

*Proof.* Write $A = \sum_{i=r}^{n-1} 1/i$, so that $P_n(r) = (r/n) A$. The function $1/t$ decreases on $t > 0$.

1. For each $i \ge 1$, $1/i \ge \int_i^{i+1} dt/t$. Summing over $i = r, \ldots, n - 1$ gives $A \ge \ln(n/r)$.
2. For each $i \ge 2$, $1/i \le \int_{i-1}^{i} dt/t$. Summing over $i = r + 1, \ldots, n - 1$ gives $A - 1/r \le \ln((n-1)/r) \le \ln(n/r)$.
3. Multiply both bounds by $r/n$. Since $(r/n)\ln(n/r) = -x \ln x$, this gives the first two inequalities.
4. Let $\varphi(x) = -x \ln x$ on $(0, 1)$. Its derivative $-\ln x - 1$ is positive for $x < 1/e$ and negative for $x > 1/e$, so $\varphi(x) \le \varphi(1/e) = 1/e$. This gives the third inequality.
5. Let $r_n = \lfloor n/e \rfloor$. For $n \ge 3$, $r_n \ge 1$, and $x_n = r_n / n$ satisfies $1/e - 1/n < x_n \le 1/e$. So $x_n \to 1/e$, and by the continuity of $\varphi$ both bounds of step 3 tend to $\varphi(1/e) = 1/e$. So $P_n(r_n) \to 1/e$. $\blacksquare$

**Remark.** Since $P_n(0) = 1/n$, the corollary shows that no cutoff gives more than $1/e + 1/n$. The [secretary problem](/secretary-problem/) page proves that the best cutoff rule is optimal among all rules, so $1/e + 1/n$ bounds every rule.
