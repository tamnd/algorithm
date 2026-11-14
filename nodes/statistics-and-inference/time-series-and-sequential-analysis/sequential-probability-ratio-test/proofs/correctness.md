---
title: The SPRT stops, obeys Wald's error bounds, and has Wald's average sample number up to the overshoot
proves: [correctness]
status: full
---

Notation is that of the page. $X_1, X_2, \ldots$ are i.i.d., $Z_i = \log f_1(X_i) - \log f_0(X_i)$, $\Lambda_n = Z_1 + \cdots + Z_n$ is the value of $\Lambda$ after line L5 in iteration $n$, and $a < 0 < b$ are the thresholds of line L1. The test stops at
$$N = \inf\{n \ge 1 : \Lambda_n \notin (a, b)\},$$
rejects $H_0$ if $\Lambda_N \ge b$ (line L6) and accepts it if $\Lambda_N \le a$ (line L7). The two cases cannot both hold since $a < b$. $P_j$ and $E_j$ refer to the law under which the $X_i$ have density $f_j$. We assume that $f_0$ and $f_1$ are positive on the same set and are not equal $\nu$-almost everywhere, so $Z_1$ is finite and not almost surely 0 under $P_0$ and $P_1$.

**Lemma 1 (termination).** Let $P$ be any law of the $X_i$ under which they are i.i.d. and $P(Z_1 = 0) < 1$. Then there are an integer $m \ge 1$ and $\delta > 0$ such that $P(N > km) \le (1 - \delta)^k$ for every $k \ge 0$. In particular $P(N < \infty) = 1$ and $E[N^r] < \infty$ for every $r \ge 1$.

*Proof.* Since $P(Z_1 \ne 0) > 0$, either $P(Z_1 > c) > 0$ or $P(Z_1 < -c) > 0$ for some $c > 0$. Take the first case; the second is symmetric. Choose $m$ with $mc > b - a$ and let $\delta = P(Z_1 > c)^m > 0$. For $k \ge 1$, let $G_k$ be the event that $Z_i > c$ for all $i$ in the block $(k-1)m < i \le km$. If $N > (k-1)m$, then $\Lambda_{(k-1)m} \in (a, b)$, or $k = 1$ and $\Lambda_0 = 0 \in (a, b)$. On $G_k$ the walk then gains more than $mc > b - a$ inside the block, so it cannot stay in $(a, b)$ for the whole block, and $N \le km$. Hence $\{N > km\} \subseteq \{N > (k-1)m\} \cap G_k^c$. The event $\{N > (k-1)m\}$ depends on $X_1, \ldots, X_{(k-1)m}$ and $G_k$ on the next block, so they are independent, and
$$P(N > km) \le P(N > (k-1)m)(1 - \delta).$$
Induction gives $P(N > km) \le (1 - \delta)^k$. Then $P(N = \infty) \le \lim_k (1 - \delta)^k = 0$, and $E[N^r] \le \sum_{k \ge 0} ((k+1)m)^r (1 - \delta)^k < \infty$. $\square$

Both $f_0$ and $f_1$ give laws that satisfy the hypothesis of Lemma 1, so under $H_0$ and under $H_1$ the test stops almost surely with a decision.

**Lemma 2 (change of measure).** For every event $E$ that is determined by $N$ and $X_1, \ldots, X_N$, with $E \subseteq \{N < \infty\}$,
$$P_1(E) = E_0\bigl[e^{\Lambda_N}\,\mathbf 1_E\bigr].$$

*Proof.* Split $E$ into the disjoint events $E_n = E \cap \{N = n\}$. Since $N$ is a stopping time, $E_n$ is determined by $X_1, \ldots, X_n$, so $\mathbf 1_{E_n} = g_n(X_1, \ldots, X_n)$ for a measurable $g_n$ with values in $\{0, 1\}$. On the set where $f_0$ is positive,
$$P_1(E_n) = \int g_n \prod_{i=1}^n f_1(x_i)\,\nu(dx_i) = \int g_n \prod_{i=1}^n \frac{f_1(x_i)}{f_0(x_i)}\prod_{i=1}^n f_0(x_i)\,\nu(dx_i) = E_0\bigl[e^{\Lambda_n}\mathbf 1_{E_n}\bigr],$$
because $f_0$ and $f_1$ are positive on the same set. Add over $n$; both sides are sums of nonnegative terms. $\square$

**Theorem 1 (Wald's bounds).** Let $\alpha' = P_0(\Lambda_N \ge b)$ and $\beta' = P_1(\Lambda_N \le a)$. With $A = e^b = (1 - \beta)/\alpha$ and $B = e^a = \beta/(1 - \alpha)$,
$$1 - \beta' \ge A\,\alpha', \qquad \beta' \le B\,(1 - \alpha'),$$
and therefore
$$\alpha' \le \frac{\alpha}{1 - \beta}, \qquad \beta' \le \frac{\beta}{1 - \alpha}, \qquad \alpha' + \beta' \le \alpha + \beta.$$

*Proof.* Let $R = \{N < \infty, \Lambda_N \ge b\}$ and $C = \{N < \infty, \Lambda_N \le a\}$. By Lemma 1, $P_0(R) + P_0(C) = 1$ and $P_1(R) + P_1(C) = 1$, so $P_0(C) = 1 - \alpha'$ and $P_1(R) = 1 - \beta'$. On $R$, $e^{\Lambda_N} \ge A$, and on $C$, $e^{\Lambda_N} \le B$. Lemma 2 gives
$$1 - \beta' = P_1(R) = E_0[e^{\Lambda_N}\mathbf 1_R] \ge A\,P_0(R) = A\,\alpha',$$
$$\beta' = P_1(C) = E_0[e^{\Lambda_N}\mathbf 1_C] \le B\,P_0(C) = B\,(1 - \alpha').$$
From the first inequality, $\alpha' \le (1 - \beta')/A \le 1/A = \alpha/(1 - \beta)$. From the second, $\beta' \le B = \beta/(1 - \alpha)$. For the sum, insert the values of $A$ and $B$ and clear the denominators, which are positive since $\alpha + \beta < 1$:
$$\alpha(1 - \beta') \ge (1 - \beta)\alpha' \quad\text{and}\quad (1 - \alpha)\beta' \le \beta(1 - \alpha').$$
Rewrite them as $\alpha' - \alpha \le \alpha'\beta - \alpha\beta'$ and $\beta' - \beta \le \alpha\beta' - \alpha'\beta$. Their sum is $\alpha' + \beta' - \alpha - \beta \le 0$. $\square$

The first two bounds can fail to be tight only through the overshoot: if $\Lambda_N$ were exactly $b$ on $R$ and exactly $a$ on $C$, the two inequalities of the proof would be equalities, and solving them would give $\alpha' = \alpha$ and $\beta' = \beta$.

**Theorem 2 (average sample number).** Let $j \in \{0, 1\}$ and suppose $E_j|Z_1| < \infty$ and $\mu_j = E_j[Z_1] \ne 0$. Then
$$E_j[N] = \frac{E_j[\Lambda_N]}{\mu_j}, \qquad \mu_0 = -D(f_0 \,\|\, f_1), \qquad \mu_1 = D(f_1 \,\|\, f_0).$$
If the overshoot is ignored, that is, if $\Lambda_N$ is replaced by $b$ on rejection and by $a$ on acceptance, and the error probabilities are replaced by $\alpha$ and $\beta$, this gives Wald's approximations
$$E_0[N] \approx \frac{\alpha b + (1 - \alpha)a}{-D(f_0 \,\|\, f_1)}, \qquad E_1[N] \approx \frac{(1 - \beta)b + \beta a}{D(f_1 \,\|\, f_0)}.$$

*Proof.* By Lemma 1, $E_j[N] < \infty$. The $Z_i$ are i.i.d. and integrable under $P_j$, and $\{N \ge i\} = \{N \le i - 1\}^c$ depends only on $Z_1, \ldots, Z_{i-1}$, so it is independent of $Z_i$. Wald's equation gives $E_j[\Lambda_N] = \mu_j E_j[N]$ exactly; for completeness,
$$E_j[\Lambda_N] = E_j\Bigl[\sum_{i \ge 1} Z_i \mathbf 1\{N \ge i\}\Bigr] = \sum_{i \ge 1} \mu_j P_j(N \ge i) = \mu_j E_j[N],$$
where the exchange of sum and expectation holds because $\sum_i E_j[|Z_i|\mathbf 1\{N \ge i\}] = E_j|Z_1|\,E_j[N] < \infty$. The values of $\mu_j$ are the definitions of the divergences:
$$\mu_0 = \int f_0 \log\frac{f_1}{f_0}\,d\nu = -D(f_0 \,\|\, f_1), \qquad \mu_1 = \int f_1 \log\frac{f_1}{f_0}\,d\nu = D(f_1 \,\|\, f_0).$$
Both are nonzero because $f_0 \ne f_1$ on a set of positive measure. Finally, $E_0[\Lambda_N] = \alpha' E_0[\Lambda_N \mid R] + (1 - \alpha')E_0[\Lambda_N \mid C]$, and the approximation replaces the conditional means by $b$ and $a$ and $\alpha'$ by $\alpha$; the same holds under $P_1$ with $1 - \beta'$ and $\beta'$. $\square$

The replacement is the only approximation, and it is not a bound in general. In the examples of the page, Wald's values are below the exact average sample numbers.

**Correctness of the procedure.** Lines L2 to L5 maintain $\Lambda = \Lambda_n$ after iteration $n$, by induction on $n$: $\Lambda = 0 = \Lambda_0$ before the loop, and line L5 adds $Z_n$. Lines L6 and L7 return at the first $n$ with $\Lambda_n \ge b$ or $\Lambda_n \le a$, which is $N$, with the decision described above. By Lemma 1 the loop ends with probability 1 under $H_0$ and $H_1$, and by Theorem 1 the decision has error probabilities $\alpha' \le \alpha/(1 - \beta)$ and $\beta' \le \beta/(1 - \alpha)$. $\blacksquare$
