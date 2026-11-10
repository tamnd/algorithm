---
title: COMPRESS keeps the weight, the order and the size bound, and leaves at most ⌈δ⌉ centroids
proves: [correctness]
status: full
---

The t-digest has no accuracy theorem, and the page shows inputs on which its rank error is almost $n$. What can be proved is the form of the digest after COMPRESS (lines L3 to L8): the weights, the order, the size bound, and the number of centroids. We prove these for any scale function $k$ that is continuous and strictly increasing on $[0, 1]$, with $k^{-1}$ its inverse, extended by $k^{-1}(y) = 1$ for $y \ge k(1)$. Both $k_0(q) = \delta q/2$ and $k_1(q) = (\delta/2\pi)\arcsin(2q - 1)$ are such functions, and for both $k(1) - k(0) = \delta/2$.

Let $X = x_1, \ldots, x_N$ be the sorted input of line L3, with weights $v_j > 0$ and total $S = \sum_j v_j$. The pass cuts $X$ into consecutive runs $R_1, \ldots, R_m$, one per output centroid. Let $W_i$ be the weight of $R_i$, $Q_i = (W_1 + \cdots + W_i)/S$, and $Q_0 = 0$. So run $R_i$ covers the quantile interval $[Q_{i-1}, Q_i]$.

**Lemma 1 (weight and order).** The output weights add up to $S$, and the output means are sorted: $c_1 \le c_2 \le \cdots \le c_m$. Each $c_i$ lies between the smallest and the largest element of $R_i$.

*Proof.* Each input element joins exactly one run (line L6 adds it to $\sigma$, or line L7 starts a new $\sigma$ with it), and weights are added, so the sum is $S$. The mean of a run is a weighted average of its elements, so it lies between its first and its last element. The runs are consecutive in the sorted order, so the last element of $R_i$ is at most the first element of $R_{i+1}$, and hence $c_i \le c_{i+1}$. $\square$

**Lemma 2 (the variables of the pass).** When the pass works on run $R_i$, the variable $q_0$ equals $Q_{i-1}$ and $q_{\text{limit}} = k^{-1}(k(Q_{i-1}) + 1)$.

*Proof.* At the start $q_0 = 0 = Q_0$ (line L4). Line L7 closes $R_i$ and adds $W_i/S$ to $q_0$, which gives $Q_i$, and recomputes $q_{\text{limit}}$ from it. $\square$

**Lemma 3 (size bound).** Every run with more than one element satisfies $k(Q_i) - k(Q_{i-1}) \le 1$.

*Proof.* A run gets its second and later elements only in line L6. Consider the last element added to $R_i$. At that moment $q = Q_{i-1} + W_i/S = Q_i$ by Lemma 2, and the test of line L6 gave $Q_i \le k^{-1}(k(Q_{i-1}) + 1)$. If $k(Q_{i-1}) + 1 \ge k(1)$, then $k(Q_i) \le k(1) \le k(Q_{i-1}) + 1$. Otherwise $k^{-1}$ is the true inverse there, and $k$ is increasing, so $k(Q_i) \le k(Q_{i-1}) + 1$. $\square$

**Lemma 4 (neighbors cannot be joined).** For $1 \le i < m$, $k(Q_{i+1}) - k(Q_{i-1}) > 1$.

*Proof.* Run $R_i$ was closed in line L7 when the first element $x$ of $R_{i+1}$ was tested. With $q_0 = Q_{i-1}$, the test computed $q = Q_{i-1} + (W_i + v(x))/S$ and found $q > k^{-1}(k(Q_{i-1}) + 1)$. Since $q \le 1$, the value $k(Q_{i-1}) + 1$ is below $k(1)$ (else $k^{-1}$ gives 1 and the test cannot fail), so $k^{-1}$ is the true inverse and $k(q) > k(Q_{i-1}) + 1$. Run $R_{i+1}$ contains $x$, so $Q_{i+1} \ge q$, and $k(Q_{i+1}) \ge k(q) > k(Q_{i-1}) + 1$. $\square$

**Theorem 1 (number of centroids).** After COMPRESS, $m < 2\big(k(1) - k(0)\big) + 1$. For $k_0$ and $k_1$ this is $m < \delta + 1$, so $m \le \lceil \delta \rceil$.

*Proof.* Take the $p = \lfloor m/2 \rfloor$ disjoint pairs $(R_1, R_2), (R_3, R_4), \ldots, (R_{2p-1}, R_{2p})$. By Lemma 4, pair $j$ adds more than 1 to $k$: $k(Q_{2j}) - k(Q_{2j-2}) > 1$. These intervals of $q$ do not overlap and lie in $[0, 1]$, and $k$ is increasing, so the sum of these increases is at most $k(1) - k(0)$. Hence $p < k(1) - k(0)$ when $p \ge 1$, and $m \le 2p + 1 < 2(k(1) - k(0)) + 1$. For $k_0$ and $k_1$, $k(1) - k(0) = \delta/2$, so $m < \delta + 1$. Since $m$ is an integer, $m \le \lceil \delta \rceil$. $\square$

**What these lemmas do not give.** Lemma 3 bounds the *weight* of each centroid in terms of its place, but the rank estimate of line L9 also assumes where the values of a cluster lie, namely half of the weight on each side of the mean. Lemma 1 only says that the mean lies between the smallest and the largest value of the cluster. So the error of Rank at a point inside the range of cluster $i$ can be close to $w_i$, and since the ranges of clusters formed at different times can nest, these errors can add up over many clusters. This is the attack of Cormode, Mishra, Ross and Veselý, and it is why no bound on the error follows from the structure. $\blacksquare$
