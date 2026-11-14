---
title: The Anderson-Darling computing formula and the validity of its p-values
proves: [correctness]
status: full
---

We use the pseudocode of the page. $F_0$ is continuous, $u_1 \le \cdots \le u_n$ are the sorted values $F_0(x_i)$ from line L1, and we set $u_0 = 0$, $u_{n+1} = 1$ and $c_i = i/n$.

**Claim 1 (the computing formula).** If $0 < u_1$ and $u_n < 1$, then

$$n \int \frac{(F_n(t) - F_0(t))^2}{F_0(t)(1 - F_0(t))} \, dF_0(t) = -n - \frac{1}{n} \sum_{i=1}^{n} (2i - 1) \left[\ln u_i + \ln(1 - u_{n+1-i})\right].$$

If $u_1 = 0$ or $u_n = 1$, the integral is infinite.

*Proof.* Substitute $s = F_0(t)$. For continuous $F_0$, $s$ is uniform under the measure $dF_0$, and $F_n(t) = G(s)$, where $G$ is the empirical distribution function of the $u_i$. So the integral is $n \int_0^1 (G(s) - s)^2 / (s(1 - s)) \, ds$. On $[u_i, u_{i+1})$, $G = c_i$, and

$$\frac{(c - s)^2}{s(1 - s)} = \frac{c^2}{s} + \frac{(1 - c)^2}{1 - s} - 1,$$

which one checks by putting the right side over the common denominator $s(1-s)$: the numerator is $c^2(1 - s) + (1 - c)^2 s - s(1 - s) = c^2 - 2cs + s^2$. On the first piece $c_0 = 0$, and on the last piece $c_n = 1$, so the terms $c^2/s$ near $s = 0$ and $(1-c)^2/(1-s)$ near $s = 1$ do not appear there, and every piece has a finite integral when $0 < u_1$ and $u_n < 1$. If $u_1 = 0$, the piece $[u_1, u_2)$ has $c_1 > 0$ and $\int_0 c_1^2/s \, ds = \infty$; the case $u_n = 1$ is the same by symmetry.

The terms $-1$ add up to $-1$, which gives $-n$ after the factor $n$. The terms $c^2/s$ give, by summation by parts,

$$\sum_{i=0}^{n} c_i^2 (\ln u_{i+1} - \ln u_i) = \sum_{i=1}^{n} (c_{i-1}^2 - c_i^2) \ln u_i = -\frac{1}{n^2} \sum_{i=1}^{n} (2i - 1) \ln u_i,$$

because $c_0 = 0$ and $\ln u_{n+1} = 0$. The terms $(1 - c)^2/(1 - s)$ give

$$\sum_{i=0}^{n} (1 - c_i)^2 (\ln(1 - u_i) - \ln(1 - u_{i+1})) = \sum_{i=1}^{n} \left((1 - c_i)^2 - (1 - c_{i-1})^2\right) \ln(1 - u_i) = -\frac{1}{n^2} \sum_{i=1}^{n} (2(n - i) + 1) \ln(1 - u_i),$$

because $\ln(1 - u_0) = 0$ and $1 - c_n = 0$. With $j = n + 1 - i$, $2(n - i) + 1 = 2j - 1$, so the last sum is $-\frac{1}{n^2} \sum_{j} (2j - 1) \ln(1 - u_{n+1-j})$. Multiply by $n$ and add. Ties among the $u_i$ give empty pieces and change nothing. $\square$

So lines L2 to L4 return $A^2$, with $A^2 = \infty$ in line L2.

**Claim 2 (distribution-free).** Under $H_0$, $(u_1, \ldots, u_n)$ has the law of the order statistics of $n$ independent uniforms on $(0, 1)$, so the law of $A^2$ depends only on $n$.

*Proof.* For continuous $F_0$, $P(F_0(X) \le s) = s$ for $s \in [0, 1]$, so each $F_0(X_i)$ is uniform, the values are independent, and sorting commutes with the nondecreasing map $F_0$. By Claim 1, $A^2$ is a function of these values. $\square$

**Claim 3 (the Monte Carlo p-value).** Under $H_0$, the p-value $p = (1 + c)/(1 + b)$ of line L7 satisfies $P(p \le \alpha) \le \alpha$ for every $\alpha \in (0, 1)$ and every $b \ge 1$.

*Proof.* Let $T_0$ be the observed statistic and $T_1, \ldots, T_b$ the simulated ones. By Claim 2 the samples of line L6 have the null law of the data, so $T_0, \ldots, T_b$ are independent and identically distributed, hence exchangeable. Let $R_i = \#\{j \in \{0, \ldots, b\} : T_j \ge T_i\}$, so $p = R_0/(1 + b)$. For an integer $q \ge 1$, let $S = \{i : R_i \le q\}$. If $S$ is not empty, take $i^* \in S$ with the smallest $T_{i^*}$. Every $i \in S$ has $T_i \ge T_{i^*}$, so $\lvert S \rvert \le R_{i^*} \le q$. By exchangeability, $P(R_0 \le q) = \frac{1}{b+1} E\lvert S \rvert \le \frac{q}{b+1}$. With $q = \lfloor \alpha (1 + b) \rfloor$, $P(p \le \alpha) = P(R_0 \le q) \le q/(1 + b) \le \alpha$; if $q = 0$ the event is empty. Ties among the $T_j$ are allowed. $\square$

The random part of the Monte Carlo p-value does not affect this bound: it holds for the joint law of the data and the simulation.

**Claim 4 (the asymptotic p-value).** As $n \to \infty$, $A^2$ converges in law to $A^2_\infty = \sum_{j \ge 1} Z_j^2/(j(j+1))$, and the series for $\mathrm{ADINF}$ is its distribution function. We cite both results from Anderson and Darling (1952, 1954) and do not prove them here. The p-value $1 - \mathrm{ADINF}(A^2)$ therefore has size that tends to $\alpha$, and the page reports Monte Carlo sizes for small $n$.

**The numerical integrals.** The integrand of the $j$-th term is at most $\exp(z/8 - a_j w^2)$, because $w^2 + 1 \ge 1$. The code takes $W = \sqrt{(40 + z/8)/a_j}$, so beyond $W$ the integrand is below $e^{-40}$ and falls like a Gaussian. Simpson's rule on $[0, W]$ with 4000 steps has an error of order $h^4$ times the fourth derivative of a smooth integrand. The tests check the result against the published percentiles $2.4924$ and $3.8781$ to five digits, and check that the mean of the limit law is 1.

**Cost.** Line L1 sorts $n$ values. Lines L2 to L4 take $O(n)$. Line L6 sorts $b$ samples of size $n$. $\square$
