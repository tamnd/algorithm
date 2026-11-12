---
title: The V-optimal dynamic program is optimal, and equi-depth range estimates have bounded error
proves: [correctness]
status: full
---

We write $f_1, \ldots, f_n$ for the frequencies of the distinct values in value order, and, for $0 \le i < j \le n$, $\mathrm{SSE}(i, j) = \sum_{t=i+1}^{j} (f_t - \mu)^2$ with $\mu = \frac{1}{j-i} \sum_{t=i+1}^{j} f_t$. A *$b$-split* of $f_1 \ldots f_j$ is a list $0 = i_0 < i_1 < \cdots < i_b = j$, and its error is $\sum_{k=1}^{b} \mathrm{SSE}(i_{k-1}, i_k)$.

**Lemma 1 (line L1).** $\mathrm{SSE}(i, j) = (Q_j - Q_i) - (P_j - P_i)^2/(j - i)$, where $P$ and $Q$ are the prefix sums of $f_t$ and $f_t^2$.

*Proof.* Let $m = j - i$ and $s = P_j - P_i$, so $\mu = s/m$. Then $\sum (f_t - \mu)^2 = \sum f_t^2 - 2\mu \sum f_t + m \mu^2 = (Q_j - Q_i) - 2s^2/m + s^2/m$, which is the claim. $\square$

**Lemma 2 (lines L2 to L8).** After the iteration $b$ of line L3, for each $j$ with $b \le j \le n$, $E[j][b]$ is the least error of a $b$-split of $f_1 \ldots f_j$, and $T[j][b]$ is the value $i_{b-1}$ of a $b$-split with that error.

*Proof.* By induction on $b$. Let $E[0][0] = 0$ (line L2): the only 0-split is of the empty prefix, with error 0, and no 0-split of a nonempty prefix exists. Take $b \ge 1$ and $j \ge b$. Each $b$-split of $f_1 \ldots f_j$ has a last cut $i = i_{b-1}$ with $b - 1 \le i \le j - 1$, because the $b - 1$ cuts before it are distinct and positive (or $i = 0$ when $b = 1$). Its error is (the error of the $(b-1)$-split $i_0, \ldots, i_{b-1}$ of $f_1 \ldots f_i$) $+ \mathrm{SSE}(i, j)$. The first term is at least $E[i][b-1]$ by the induction hypothesis, so the error is at least the value $c$ of line L6 for this $i$. Conversely, for each $i$ in the range of line L5, an optimal $(b-1)$-split of $f_1 \ldots f_i$ followed by the cut $j$ is a $b$-split with error exactly $c$. So the least $c$ over $i$, which lines L7 and L8 store, is the least error of a $b$-split, and its $i$ is the last cut of a split that reaches it. $\square$

**Lemma 3 (fewer buckets do not help).** For $b < n$, the least error of a $(b+1)$-split of $f_1 \ldots f_n$ is at most that of a $b$-split.

*Proof.* Take an optimal $b$-split. Some bucket has at least two values, because $b < n$. Split it into two nonempty parts with means $\mu_1, \mu_2$. For each part, the mean is the constant that minimizes the sum of squared deviations, so $\sum_{\text{part } 1} (f_t - \mu_1)^2 \le \sum_{\text{part } 1} (f_t - \mu)^2$, and the same for part 2. The sum of both is at most the old $\mathrm{SSE}$ of the bucket. $\square$

**Theorem 1.** V-OPTIMAL$(f, B)$ with $B \le n$ returns the least error of a split of $f_1 \ldots f_n$ into at most $B$ buckets, and a split with that error.

*Proof.* By Lemma 2 with $j = n$ and $b = B$, $E[n][B]$ is the least error of a $B$-split. By Lemma 3, applied $B - b$ times, a split into $b \le B$ buckets is never better, so it is also the least over at most $B$ buckets. Line L9 starts at $j = n$, $b = B$ and reads $i = T[j][b]$. By Lemma 2 there is an optimal $b$-split of $f_1 \ldots f_j$ whose last bucket is $f_{i+1} \ldots f_j$, and whose first $b - 1$ buckets form a $(b-1)$-split of $f_1 \ldots f_i$ with error $E[i][b-1]$, which is optimal. So the traceback continues from $(i, b - 1)$ with the same property, and the $B$ buckets it collects have the total error $E[n][B]$. $\square$

For the second claim, let $H$ be an equi-depth histogram of $N$ integer values with buckets $(lo_k, hi_k, c_k, d_k)$, $k = 1, \ldots, m$, built from consecutive groups of $d = \lceil N/B \rceil$ sorted values. So $c_k \le d$, $lo_k \le hi_k \le lo_{k+1}$, and bucket $k$ holds exactly the $k$-th group of the sorted values.

**Theorem 2.** For all integers $a \le b$, $|\text{ESTIMATE-RANGE}(H, a, b) - |\{v : a \le v \le b\}|| \le 2d$.

*Proof.* Write $\text{true}_k$ for the number of values of group $k$ in $[a, b]$, and $\text{est}_k = c_k \cdot |[a, b] \cap [lo_k, hi_k]| / (hi_k - lo_k + 1)$ for its term in line E4. Both lie in $[0, c_k]$, so $|\text{est}_k - \text{true}_k| \le c_k \le d$ for every $k$.

Call bucket $k$ *inside* if $a \le lo_k$ and $hi_k \le b$, and *outside* if $hi_k < a$ or $b < lo_k$. All values of group $k$ lie in $[lo_k, hi_k]$. If $k$ is inside, then $\text{true}_k = c_k$ and the overlap is the full range, so $\text{est}_k = c_k$. If $k$ is outside, then $\text{true}_k = 0 = \text{est}_k$. So only the other buckets have an error. A bucket that is neither has $lo_k < a \le hi_k$ or $lo_k \le b < hi_k$.

At most one bucket has $lo_k < a \le hi_k$: if $k < k'$ both did, then $a \le hi_k \le lo_{k'} < a$, which is false. In the same way, at most one bucket has $lo_k \le b < hi_k$: if $k < k'$ both did, then $b < hi_k \le lo_{k'} \le b$, which is false. So at most two buckets have an error, each at most $d$, and the total error is at most $2d$. $\blacksquare$
