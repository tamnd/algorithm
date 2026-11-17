---
title: SOR keeps exactly the points whose mean k-neighbor distance is at most mu + alpha sigma, and removes at most n/(1 + alpha^2) points
proves: [correctness]
status: full
---

Let $P = (p_1, \ldots, p_n)$ with $n \ge 2$, let $1 \le k \le n - 1$ and $\alpha \ge 0$. For each $i$ let $D_i$ be the multiset of the $n - 1$ distances $\|p_i - p_j\|$, $j \ne i$.

**Lemma 1 (line L2 and L3 are well defined).** The value $d_i$ of line L3 equals the mean of the $k$ smallest elements of $D_i$, whatever neighbors line L2 picks among equal distances.

*Proof.* Sort $D_i$ as $\delta_1 \le \delta_2 \le \cdots \le \delta_{n-1}$. A valid choice at line L2 is a set $N$ of $k$ points other than $p_i$ such that no point outside $N$ is strictly closer to $p_i$ than some point of $N$. First, every point of $N$ is at distance at most $\delta_k$: at least $k$ points are at distance at most $\delta_k$, so if $N$ held a point farther than $\delta_k$, one of those $k$ points would be outside $N$ and strictly closer. Next, let $a < k$ be the number of points at distance strictly less than $\delta_k$. All of them are in $N$: if one were missing, $N$ would hold at most $a - 1$ points at distance below $\delta_k$, so at least one point of $N$ would be at distance $\delta_k$, and the missing point would be strictly closer than it. So $N$ is the $a$ points below $\delta_k$ plus $k - a$ points at distance exactly $\delta_k$, and its distances are $\delta_1, \ldots, \delta_k$ as a multiset. The sum at line L3 is $\delta_1 + \cdots + \delta_k$ for every valid choice. $\square$

**Theorem 1 (output).** Lines L4 to L7 return exactly the indices $i$ with $d_i \le \mu + \alpha \sigma$, in input order, where $\mu = \frac{1}{n} \sum_i d_i$ and $\sigma^2 = \frac{1}{n-1} \sum_i (d_i - \mu)^2$.

*Proof.* By Lemma 1 the loop of line L1 computes each $d_i$. Lines L4, L5 and L6 compute $\mu$, $\sigma$ and the threshold $T = \mu + \alpha \sigma$ by their definitions, with $n - 1 \ge 1$. Line L7 scans $i = 1, \ldots, n$ in order and keeps $i$ exactly when $d_i \le T$. $\square$

The values $d_i$ depend only on the distances between points. A rigid motion keeps all distances, and a permutation of the input permutes the $d_i$ without changing $\mu$ and $\sigma$. So the set of kept points does not change under a rigid motion of the cloud or a new order of the input. A uniform scaling by $c > 0$ multiplies every $d_i$, $\mu$ and $\sigma$ by $c$, so it does not change the kept set either.

**Theorem 2 (at most a fixed fraction is removed).** If $\alpha > 0$, the number of removed points is at most $n / (1 + \alpha^2)$.

*Proof.* Let $s^2 = \frac{1}{n} \sum_i (d_i - \mu)^2$ be the variance of the $d_i$ with the divisor $n$. Then $\sigma^2 = \frac{n}{n-1} s^2 \ge s^2$, so $T \ge \mu + \alpha s$, and every removed index has $d_i - \mu > \alpha s$.

If $s = 0$, all $d_i$ equal $\mu = T$, and nothing is removed. Otherwise put $t = \alpha s > 0$, and let $R = \{ i : d_i - \mu \ge t \}$, which contains every removed index. For any $u \ge 0$ and $i \in R$ we have $d_i - \mu + u \ge t + u > 0$, so $(d_i - \mu + u)^2 \ge (t + u)^2$. Summing over $R$ and then over all $i$, since the terms are squares,

$$|R| (t + u)^2 \le \sum_{i=1}^{n} (d_i - \mu + u)^2 = n s^2 + 2u \sum_{i=1}^n (d_i - \mu) + n u^2 = n (s^2 + u^2),$$

because $\sum_i (d_i - \mu) = 0$. Take $u = s^2 / t$. Then

$$\frac{|R|}{n} \le \frac{s^2 + s^4/t^2}{(t + s^2/t)^2} = \frac{s^2 (t^2 + s^2)/t^2}{(t^2 + s^2)^2 / t^2} = \frac{s^2}{s^2 + t^2} = \frac{1}{1 + \alpha^2}.$$

This is the one-sided Chebyshev inequality of Cantelli, applied to the uniform distribution on the values $d_i$. $\square$

With $\alpha = 1$ at most half of the points go, and with $\alpha = 2$ at most a fifth. The bound needs no assumption on how the points are distributed. It also shows the weak side of the method: it is a bound on how much the filter removes, not a promise that it removes the outliers. $\blacksquare$
