---
title: The Kruskal-Wallis statistic, its exact conditional p-value, and why both are valid
proves: [correctness]
status: full
---

We use the pseudocode of the page. The pooled sample has $N$ values with midranks $r_1, \ldots, r_N$ (line L1), group $i$ has size $n_i$ and rank sum $R_i$ (line L2), and $\bar r = (N+1)/2$.

**Claim 1 (the two forms of $H'$).** $\frac{12}{N(N+1)} \sum_i n_i (\bar R_i - \bar r)^2 = \frac{12}{N(N+1)} \sum_i R_i^2/n_i - 3(N+1)$.

*Proof.* Midranks keep the total rank sum: $\sum_i R_i = N(N+1)/2$, because replacing the ranks of a tie group by their mean does not change their sum. Expand: $\sum_i n_i (\bar R_i - \bar r)^2 = \sum_i R_i^2 / n_i - 2 \bar r \sum_i R_i + N \bar r^2 = \sum_i R_i^2/n_i - N(N+1)^2/4$. Multiply by $12/(N(N+1))$. $\square$

**Claim 2 (the tie correction).** With midranks, $SS_T = \sum_l (r_l - \bar r)^2 = \frac{N^3 - N}{12} C$, so $H = H'/C = (N - 1) SS_B / SS_T$ with $SS_B = \sum_i n_i (\bar R_i - \bar r)^2$, whenever $C > 0$.

*Proof.* Without ties $\sum_{l=1}^{N} (l - \bar r)^2 = (N^3 - N)/12$. A tie group covering ranks $a + 1, \ldots, a + t$ has mean $m = a + (t+1)/2$. Replacing these ranks by $m$ keeps their sum and lowers $\sum (r - \bar r)^2$ by $\sum_{s=1}^{t} (a + s - m)^2 = (t^3 - t)/12$. So $SS_T = (N^3 - N - \sum_j (t_j^3 - t_j))/12 = \frac{N^3 - N}{12} C$. Then $H'/C = \frac{12\, SS_B}{N(N+1)} \cdot \frac{N^3 - N}{12\, SS_T} = (N - 1) SS_B / SS_T$. If all values are tied, $C = 0$ and the code returns $H = 0$. $\square$

**Claim 3 (the null law).** Under $H_0$, conditional on the multiset of pooled values, the assignment of the $N$ sorted positions to the groups is uniform over the $N!/(n_1! \cdots n_k!)$ splits with the given sizes.

*Proof.* Under $H_0$ the $N$ observations are independent with one law, so their joint law is invariant under permutations of the observations. Given the multiset of values, every way of placing the observations in the sorted slots that is consistent with it is equally likely, so the set of slots of each group is a uniform split. The midranks depend only on the multiset. $\square$

**Claim 4 (the dynamic program).** After line L6 has processed the first $t$ pooled values, the count stored for the state (sizes $f_1, \ldots, f_k$, doubled rank sums $s_1, \ldots, s_k$) is the number of ways to assign these $t$ values to the groups so that group $i$ gets $f_i$ of them with doubled rank sum $s_i$, and $f_i \le n_i$.

*Proof.* Induction on $t$. At $t = 0$ only the empty assignment exists. Each assignment of the first $t$ values extends in one way for each group $i$ with $f_i < n_i$, adding 1 to $f_i$ and the doubled rank of value $t$ to $s_i$; the code makes exactly these moves and adds the counts. At $t = N$ every state has $f_i = n_i$, and the code sums the counts over the sizes to get the number of splits for each vector of rank sums. $\square$

**Claim 5 (the ordering).** Given the tie pattern, $H$ is a strictly increasing function of $Q = \sum_i R_i^2 / n_i$, and $Q \ge Q_{obs}$ exactly when the integer $\sum_i (2R_i)^2 L / n_i$ is at least its observed value, where $L = \operatorname{lcm}(n_1, \ldots, n_k)$.

*Proof.* By Claim 1, $H = (\frac{12}{N(N+1)} Q - 3(N+1))/C$ with $C > 0$ fixed by the tie pattern. Multiplying $Q$ by the positive integer $4L$ keeps the order and makes every term an integer, because $n_i$ divides $L$. $\square$

**Claim 6 (validity of the exact p-value).** For every $\alpha$, $P_{H_0}(p \le \alpha) \le \alpha$.

*Proof.* By Claims 3 to 5, line L8 returns $P(Q \ge Q_{obs})$ under the uniform law of splits, given the pooled values. The set of values $q$ with $P(Q \ge q) \le \alpha$ is empty or has a least element $q^*$, and the conditional probability of rejection is $P(Q \ge q^*) \le \alpha$. Averaging over the pooled values keeps the bound. $\square$

**The chi-square limit (the asymptotic p-value).** Under the uniform law of splits without ties, $E \bar R_i = \bar r$, $\operatorname{Var} \bar R_i = \frac{(N - n_i)(N+1)}{12 n_i}$ and $\operatorname{Cov}(\bar R_i, \bar R_j) = -\frac{N+1}{12}$ for $i \ne j$, from sampling without replacement. So the vector $Z_i = \sqrt{12 n_i / (N(N+1))}\,(\bar R_i - \bar r)$ has covariance $I - u u^{\top}$ with $u_i = \sqrt{n_i/N}$, a projection of rank $k - 1$, and $H' = \sum_i Z_i^2 = \lVert Z \rVert^2$. When every $n_i \to \infty$ with $n_i/N$ bounded away from 0, the central limit theorem for linear rank statistics (Hájek's theorem for sampling without replacement) makes $Z$ asymptotically normal with this covariance, and the squared length of such a vector is $\chi^2_{k-1}$. With ties the same argument applies to midranks with the variance multiplied by $C$, which is why $H = H'/C$ is used. The page's Monte Carlo runs show the size of the chi-square test approaching $0.05$ as the groups grow. This part gives an approximation, not a bound, and the page says so.

**Cost.** Lines L1 to L4 cost one sort and $O(N)$ further work. The exact branch keeps at most $\prod_{i<k} (n_i + 1)(2N n_i + 1)$ states, because the last group's size and rank sum are fixed by the others, and each of the $N$ steps updates each state in at most $k$ ways. $\square$
