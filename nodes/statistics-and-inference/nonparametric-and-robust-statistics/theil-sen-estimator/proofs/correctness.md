---
title: COUNT counts the slopes in an interval by inversions, SELECT-SLOPE returns the k-th slope, and the Theil-Sen slope breaks down at about 1 - 1/sqrt(2)
proves: [correctness]
status: full
---

**Setting.** The data are $(x_1, y_1), \ldots, (x_n, y_n)$. For a pair $i \ne j$ with $x_i \ne x_j$, the slope is $s_{ij} = (y_j - y_i)/(x_j - x_i)$. Pairs with $x_i = x_j$ have no slope and are skipped. $N$ is the number of slopes, and $\sigma_1 \le \cdots \le \sigma_N$ are the slopes in sorted order, with repeats. For a value $v$, $c_<(v)$ and $c_\le(v)$ are the numbers of slopes $< v$ and $\le v$.

For a finite $s$, the key of point $i$ at $s$ is $z_i(s) = y_i - s x_i$. The key at $-\infty$ is the pair $(x_i, y_i)$, and the key at $+\infty$ is $(-x_i, y_i)$, both compared in lexicographic order. These are the orders of $y_i - s x_i$ for $s$ very negative and for $s$ very large.

## Part 1. Counting

**Lemma 1 (sign of a key difference).** Let $x_i < x_j$. For finite $s$, $z_j(s) - z_i(s)$ has the sign of $s_{ij} - s$. The key of $j$ is larger than the key of $i$ at $-\infty$, and smaller at $+\infty$. If $x_i = x_j$, the keys of $i$ and $j$ compare in the same way at every $s$, finite or not.

*Proof.* $z_j(s) - z_i(s) = (y_j - y_i) - s (x_j - x_i) = (x_j - x_i)(s_{ij} - s)$, and $x_j - x_i > 0$. At $-\infty$, $(x_i, y_i) < (x_j, y_j)$ because $x_i < x_j$; at $+\infty$, $(-x_j, y_j) < (-x_i, y_i)$. If $x_i = x_j$, every comparison reduces to the comparison of $y_i$ and $y_j$. $\square$

Call a pair **discordant** for $lo < hi$ if its two keys are in strict opposite order at $lo$ and at $hi$.

**Lemma 2.** For $lo < hi$ (each finite or infinite), the number of discordant pairs is the number of slopes in the open interval $(lo, hi)$.

*Proof.* A pair with $x_i = x_j$ is never discordant, by Lemma 1. For $x_i < x_j$, Lemma 1 says that the key of $j$ is above the key of $i$ at $lo$ exactly when $s_{ij} > lo$, and below it at $hi$ exactly when $s_{ij} < hi$. The other discordant case would need $s_{ij} < lo$ and $s_{ij} > hi$, which is impossible. So the pair is discordant exactly when $lo < s_{ij} < hi$. $\square$

**Lemma 3 (COUNT).** Lines L14 and L15 return the number of discordant pairs, in $O(n \log n)$ time.

*Proof.* Line L14 lists the points in the order of the key at $lo$, with ties broken by the key at $hi$. Let $w$ be the keys at $hi$ in that order. A pair tied at $lo$ appears with its keys at $hi$ in nondecreasing order, so it is not an inversion of $w$, and it is not discordant. A pair in strict order at $lo$ is an inversion of $w$ exactly when its keys at $hi$ are in strict opposite order. So the inversions of $w$ are the discordant pairs. The merge sort count of [counting inversions](/counting-inversions/) takes $O(n \log n)$ time. $\square$

So $N = $ COUNT$(-\infty, +\infty)$, $c_<(s) = $ COUNT$(-\infty, s)$ and $c_\le(s) = N - $ COUNT$(s, +\infty)$. In particular, the number of slopes below $s$ is the number of [inversions](/inversion/) of the sequence $y_i - s x_i$ when the points are listed by $x$ (ties in $x$ listed by $y$).

## Part 2. Selection

**Lemma 4.** A value $v$ equals $\sigma_k$ if and only if $c_<(v) < k \le c_\le(v)$.

*Proof.* If $v = \sigma_k$, the slopes below $v$ are among $\sigma_1, \ldots, \sigma_{k-1}$, and $\sigma_1, \ldots, \sigma_k$ are $\le v$. Conversely, at least $k$ slopes are $\le v$, so $\sigma_k \le v$, and fewer than $k$ are $< v$, so $\sigma_k \not< v$. $\square$

**Lemma 5 (sampling).** Each slope drawn at line L5 is uniform over the slopes in $(lo, hi)$, and the draws are independent.

*Proof.* Use the sequence $w$ of Lemma 3. For each position $b$, let $\iota_b$ be the number of earlier positions $a < b$ with $w_a > w_b$; a Fenwick tree over the ranks of $w$ gives all $\iota_b$ in $O(n \log n)$ time. List the inversions $(a, b)$ by $b$, and for a fixed $b$ by the rank of $w_a$. This list has $C = \sum_b \iota_b$ entries, one for each slope in $(lo, hi)$ by Lemma 3. A uniform integer $g \in [0, C)$ picks entry $g$: the position $b$ is where the prefix sums of $\iota$ pass $g$, and the partner $a$ is found by a find-$k$-th query in the Fenwick tree of the earlier positions. Independent uniform integers give independent uniform entries. $\square$

**Invariant of the loop.** At line L4, $below = c_\le(lo)$, $inside$ is the number of slopes in $(lo, hi)$, and $below < k \le below + inside$. So $\sigma_k \in (lo, hi)$.

*Proof.* At the start, $lo = -\infty$ and $hi = +\infty$, so $below = 0$, $inside = N$ and $1 \le k \le N$. In a round, line L8 computes $c_<$ and $c_\le$ at the new ends, and returns an end only when Lemma 4 says it is $\sigma_k$. Line L10 changes the interval only when $c_\le(lo') < k \le c_<(hi')$, which is the invariant for $(lo', hi')$, since the number of slopes in $(lo', hi')$ is $c_<(hi') - c_\le(lo')$. Otherwise the old values stay. $\square$

At line L12 the invariant holds, so the slopes in $(lo, hi)$ are $\sigma_{below + 1}, \ldots, \sigma_{below + inside}$, and line L13 returns the $(k - below)$-th smallest of them, which is $\sigma_k$. Line L12 lists the inversions of $w$ by the merge sort that counts them, which takes $O(n \log n + inside)$ time. $\square$

**One round succeeds with probability at least 7/8.** Index the slopes in $(lo, hi)$ as $1, \ldots, C$ in sorted order, and let $\tau = k - below$ be the index of $\sigma_k$. Let $Y$ be the number of the $r$ draws with index $\le \tau$, and $X$ the number with index $< \tau$. Then $Y \sim \mathrm{Bin}(r, \tau/C)$ with mean $t$, the value of line L6, and $X \sim \mathrm{Bin}(r, (\tau - 1)/C)$ with mean $t - r/C \le t$. The sample $S$ is sorted and indexed from 0. The low end $lo' = S[a]$ is at most $\sigma_k$ when $Y \ge a + 1$, and the high end $hi' = S[b]$ is at least $\sigma_k$ when $X \le b$. The code takes $a = \lfloor t \rfloor - \delta \le t - \delta$ and $b = \lfloor t \rfloor + \delta > t + \delta - 1$, so $b + 1 > t + \delta$, with $\delta = 2\lfloor\sqrt r\rfloor + 2 \ge 2\sqrt r$. Chebyshev's inequality, with variance at most $r/4$, gives
$$\Pr[Y \le a] \le \frac{r/4}{\delta^2} \le \frac1{16}, \qquad \Pr[X \ge b + 1] \le \frac{r/4}{\delta^2} \le \frac1{16}.$$
(If $a < 0$ or $b \ge r$, that end stays at $lo$ or $hi$, which is safe.) So with probability at least $7/8$, $lo' \le \sigma_k \le hi'$, and the round either returns $\sigma_k$ or shrinks the interval. Matoušek (1991) shows that after a successful round the expected number of slopes left in the interval is $O(C/\sqrt r)$. With $r = n$ and $C \le n^2/2$, two successful rounds bring $C$ to $O(n)$, below the stop value $4r$. So the expected number of rounds is $O(1)$, each round takes $O(n \log n)$ time, and the expected total time is $O(n \log n)$. The correctness above does not depend on this analysis; only the time does.

## Part 3. The estimator

Line L17 takes the median of the $N$ slopes: $\sigma_{(N+1)/2}$ for odd $N$, and the mean of $\sigma_{N/2}$ and $\sigma_{N/2+1}$ for even $N$. Line L18 takes the median of the residuals $y_i - b x_i$ as the intercept. If $y_i$ is replaced by $y_i + c + d x_i$, each slope grows by $d$, so $b$ grows by $d$, and each residual grows by $c$, so $a$ grows by $c$.

## Part 4. The breakdown point

Assume the clean data have distinct $x_i$. Replace $m$ of the $n$ points by arbitrary points. Let $G = \binom{n-m}{2}$ be the number of slopes among the clean points; these values do not change. Let $B'$ be the number of slopes that involve a replaced point; $B' \le B = \binom n2 - \binom{n-m}2$, with equality when all $x$ values are distinct. The total is $N' = G + B'$.

**Lemma 6.** The median of $N'$ numbers, $G$ of them fixed and $B'$ of them free, stays bounded over all values of the free numbers if and only if $B' < G$.

*Proof.* The $k$-th smallest of the $N'$ numbers can be sent to $+\infty$ exactly when $B' \ge N' - k + 1$ (send all free numbers up), and to $-\infty$ exactly when $B' \ge k$; otherwise it lies between two fixed numbers. The median uses $k_L = \lfloor (N'+1)/2 \rfloor$ and $k_U = \lfloor N'/2 \rfloor + 1$, and $N' - k_U + 1 = k_L = \lceil N'/2 \rceil$. So the median is bounded exactly when $B' < \lceil N'/2 \rceil$, that is $B' < N'/2$, that is $B' < G$. $\square$

The free slopes can all be sent to $+\infty$ together: put the $j$-th replaced point at $x = \max_i x_i + j$ and $y = j^2 t$. Its slope to a clean point is about $j^2 t$ divided by a positive distance, and the slope between replaced points $j < j'$ is $(j' + j) t$; all grow without bound as $t \to \infty$. Equal $x$ values only lower $B'$. So the Theil-Sen slope can be carried to infinity by $m$ points exactly when $B \ge G$, that is
$$m^* = \min\Big\{ m : 2\binom{n-m}{2} \le \binom n2 \Big\}, \qquad \varepsilon^*_n = \frac{m^*}{n}.$$
For example $m^* = 3$ for $n = 10$, $30$ for $n = 100$, and $293$ for $n = 1000$. As $n \to \infty$, $\binom{n-m}2 / \binom n2 \to (1 - \varepsilon)^2$, and $(1 - \varepsilon)^2 = 1/2$ gives
$$\varepsilon^* = 1 - \frac{1}{\sqrt 2} \approx 0.2929. \qquad \square$$
