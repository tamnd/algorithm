---
title: Fisher's statistic has the chi-squared law with 2k degrees of freedom, and the finite Poisson sum is its exact upper tail
proves: [correctness, termination]
status: full
---

We prove that, when $p_1, \dots, p_k$ are independent and uniform on $(0, 1)$, the statistic $X = -2\sum_i \ln p_i$ has the $\chi^2_{2k}$ law, that FISHER-METHOD returns $P = P(\chi^2_{2k} \ge X)$ through the finite sum $e^{-h}\sum_{j<k}h^j/j!$ with $h = X/2$, and that rejecting when $P \le \alpha$ has size exactly $\alpha$. We also prove that the test stays valid, with size at most $\alpha$, when the p-values are independent and only satisfy $P(p_i \le u) \le u$. Nothing on the page about the method itself is only measured; the sizes under dependence are computed from a closed form, and the tests check them by simulation.

**Lemma 1 (one p-value).** If $U$ is uniform on $(0, 1)$, then $Y = -2\ln U$ has the $\chi^2_2$ law, the exponential law with mean 2.

*Proof.* For $y \ge 0$, $P(Y \ge y) = P(\ln U \le -y/2) = P(U \le e^{-y/2}) = e^{-y/2}$. This is the upper tail of the exponential law with mean 2. The $\chi^2_2$ density is $\frac{1}{2^{1}\Gamma(1)}y^{0}e^{-y/2} = \frac12e^{-y/2}$, whose upper tail is also $e^{-y/2}$. $\square$

For $k = 1$ this already gives the result: $P = P(\chi^2_2 \ge -2\ln p_1) = e^{\ln p_1} = p_1$. The combined p-value of one p-value is itself, exactly.

**Lemma 2 (sums).** If $Y_1, \dots, Y_k$ are independent and each is $\chi^2_2$, then $\sum_i Y_i$ is $\chi^2_{2k}$, with density $f_k(x) = \dfrac{x^{k-1}e^{-x/2}}{2^k(k - 1)!}$ for $x > 0$.

*Proof.* By induction on $k$. For $k = 1$, $f_1(x) = \frac12e^{-x/2}$ is the density of Lemma 1. If $\sum_{i<k}Y_i$ has density $f_{k-1}$, then the density of the sum with $Y_k$ is the convolution
$$\int_0^x f_{k-1}(s)f_1(x - s)\,ds = \int_0^x \frac{s^{k-2}e^{-s/2}}{2^{k-1}(k - 2)!}\cdot\frac{e^{-(x - s)/2}}{2}\,ds = \frac{e^{-x/2}}{2^k(k - 2)!}\cdot\frac{x^{k-1}}{k - 1} = f_k(x).$$
The function $f_k$ is the $\chi^2_{2k}$ density, which is $x^{\nu/2 - 1}e^{-x/2}/(2^{\nu/2}\Gamma(\nu/2))$ with $\nu = 2k$. $\square$

**Lemma 3 (the tail is a finite Poisson sum).** For $x \ge 0$ and $h = x/2$, $\int_x^\infty f_k(s)\,ds = e^{-h}\sum_{j=0}^{k-1}h^j/j!$.

*Proof.* Let $S_k(h) = e^{-h}\sum_{j<k}h^j/j!$. Differentiating,
$$S_k'(h) = e^{-h}\left(\sum_{j=1}^{k-1}\frac{h^{j-1}}{(j - 1)!} - \sum_{j=0}^{k-1}\frac{h^j}{j!}\right) = -e^{-h}\frac{h^{k-1}}{(k - 1)!},$$
because the two sums telescope and only the last term of the second remains. With $h = x/2$, $\frac{d}{dx}S_k(x/2) = -\frac12e^{-x/2}\frac{(x/2)^{k-1}}{(k - 1)!} = -f_k(x)$. Also $S_k(h) \to 0$ as $h \to \infty$, since $e^{-h}$ times a polynomial tends to 0. So $S_k(x/2) = \int_x^\infty f_k(s)\,ds$. $\square$

The tests check the polynomial identity of this proof in exact rational arithmetic for $k \le 11$, and the case $k = 2$ against the direct integral $P(U_1U_2 \le q) = q(1 - \ln q)$.

**Lemma 4 (what the lines compute).** If all $p_i \in (0, 1]$ and not all are 1, lines L2 to L6 return $X = -2\sum_i \ln p_i$ and $P = S_k(X/2)$, which is at most 1. If some $p_i = 0$, line L1 returns $X = \infty$ and $P = 0$, the limit of both as $p_i \to 0$. If all $p_i = 1$, the code returns $X = 0$ and $P = 1$.

*Proof.* Line L2 computes $h = -\sum_i \ln p_i > 0$. Line L4 computes $t_j = \exp(-h + j\ln h - \ln j!) = e^{-h}h^j/j!$, and line L5 adds them, so $P = S_k(h)$. $S_k(h)$ is a probability, by Lemma 3, so it is at most 1 in exact arithmetic, and the minimum in line L6 only removes rounding. As $p_i \to 0$, $h \to \infty$ and $S_k(h) \to 0$. When all $p_i = 1$, $h = 0$ and $S_k(0) = 1$, because only the term $j = 0$ is not 0. $\square$

**Lemma 5 (exact size).** If the $p_i$ are independent and uniform on $(0, 1)$, then $P$ is uniform on $(0, 1)$, and $P(P \le \alpha) = \alpha$.

*Proof.* By Lemmas 1 and 2, $X \sim \chi^2_{2k}$. By Lemma 4, $P = G(X)$, where $G(x) = \int_x^\infty f_k$ is continuous and strictly decreasing from 1 to 0 on $[0, \infty)$. So $P(G(X) \le \alpha) = P(X \ge G^{-1}(\alpha)) = G(G^{-1}(\alpha)) = \alpha$. $\square$

**Lemma 6 (valid p-values).** If the $p_i$ are independent and $P(p_i \le u) \le u$ for all $u \in [0, 1]$, then $P(P \le \alpha) \le \alpha$.

*Proof.* Each $Y_i = -2\ln p_i$ satisfies $P(Y_i \ge y) = P(p_i \le e^{-y/2}) \le e^{-y/2}$, so $Y_i$ is stochastically smaller than a $\chi^2_2$ variable $Y_i^*$. By the quantile coupling, there are independent $Y_i^* \sim \chi^2_2$ with $Y_i \le Y_i^*$ for every $i$, so $X \le X^* = \sum_i Y_i^* \sim \chi^2_{2k}$. Since $G$ is decreasing, $P(G(X) \le \alpha) \le P(G(X^*) \le \alpha) = \alpha$, by Lemma 5. $\square$

**What fails under dependence.** Lemma 2 needs independence. If $p_1 = \dots = p_k = U$, then $X = -2k\ln U$ and $P(X \ge c) = P(U \le e^{-c/(2k)}) = e^{-c/(2k)}$. With $c = \chi^2_{2k, 0.95}$ this is 0.0933 for $k = 2$, so the nominal 5% test has size above 9%. This is a computation, and the tests confirm it by simulation.

**Termination.** Line L1 checks $k$ values. Line L2 takes $k$ logarithms and a compensated sum of $k$ numbers. Lines L4 and L5 compute and add $k$ terms. Every loop has $k$ steps, so the algorithm stops after $\Theta(k)$ operations.

**Theorem.** For independent p-values $p_1, \dots, p_k$ in $[0, 1]$, FISHER-METHOD returns $X = -2\sum_i \ln p_i$ and $P = P(\chi^2_{2k} \ge X) = e^{-X/2}\sum_{j<k}(X/2)^j/j!$. If the p-values are uniform under $H_0$, then $X \sim \chi^2_{2k}$ exactly and the test that rejects when $P \le \alpha$ has size exactly $\alpha$; if they are only valid, the size is at most $\alpha$.

*Proof.* Lemmas 1 to 6. $\blacksquare$
