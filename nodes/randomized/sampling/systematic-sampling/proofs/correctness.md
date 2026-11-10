---
title: Each item of a systematic sample has inclusion probability n over N
proves: [correctness]
status: full
---

**Statement.** Let $1 \le n \le N$, let $r$ be uniform in $\{0, \ldots, N - 1\}$, and let $p_i = \lfloor (r + iN)/n \rfloor$ for $i = 0, \ldots, n - 1$. Then:

1. $0 \le p_0 < p_1 < \cdots < p_{n-1} \le N - 1$, so the sample has exactly $n$ distinct items, in input order.
2. Each position $j \in \{0, \ldots, N - 1\}$ is in the sample with probability exactly $n/N$.
3. Hence the sample mean $\bar y = \frac{1}{n} \sum_i y_{p_i}$ is an unbiased estimate of the population mean $\bar Y = \frac{1}{N} \sum_j y_j$.
4. If $n$ divides $N$ and $k = N/n$, then $p_i = s + ik$ with $s = \lfloor r/n \rfloor$ uniform in $\{0, \ldots, k - 1\}$: the classical rule "random start, then every $k$-th item".

**Proof of 1.** Since $(r + (i+1)N)/n - (r + iN)/n = N/n \ge 1$, the floors strictly increase. Also $p_0 = \lfloor r/n \rfloor \ge 0$ and $p_{n-1} \le (r + (n-1)N)/n < (N + (n-1)N)/n = N$.

**Proof of 2.** Fix $j$. Position $j$ is in the sample if and only if some $i \in \{0, \ldots, n-1\}$ has $jn \le r + iN < jn + n$. The numbers $r + iN$ for $i = 0, \ldots, n - 1$ are exactly the integers $m$ in $[0, nN)$ with $m \equiv r \pmod N$. The window $W_j = \{jn, \ldots, jn + n - 1\}$ lies in $[0, nN)$, because $j \le N - 1$. So $j$ is sampled if and only if $W_j$ contains an integer congruent to $r$ modulo $N$. The window holds $n \le N$ consecutive integers, so their residues modulo $N$ are $n$ distinct values. So exactly $n$ of the $N$ equally likely values of $r$ put $j$ in the sample, and $\Pr[j \text{ sampled}] = n/N$.

**Proof of 3.** By part 1 the sample has exactly $n$ items. By linearity of expectation and part 2,
$$E[\bar y] = \frac{1}{n} \sum_{j=0}^{N-1} y_j \Pr[j \text{ sampled}] = \frac{1}{n} \sum_{j} y_j \frac{n}{N} = \bar Y.$$

**Proof of 4.** Write $r = sn + c$ with $0 \le c < n$. Then $(r + iN)/n = s + ik + c/n$, whose floor is $s + ik$. As $r$ runs over $\{0, \ldots, N - 1\}$, the value $s$ runs over $\{0, \ldots, k - 1\}$, each value $n$ times, so $s$ is uniform. $\blacksquare$
