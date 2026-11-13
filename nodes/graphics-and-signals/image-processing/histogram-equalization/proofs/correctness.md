---
title: Histogram equalization computes the rounded cumulative map, and its output histogram is close to flat
proves: [correctness]
status: full
---

The input is an image $I$ with $N = WH \ge 1$ pixels and values in $\{0, \ldots, L-1\}$, with $L \ge 2$. We write $h[k]$ for the number of pixels with value $k$, and $c(k) = \sum_{j \le k} h[j]$ for the cumulative count. The target map is

$$T(k) = \operatorname{round}\Big(\frac{(L-1)\, c(k)}{N}\Big),$$

where round takes halves up, so $\operatorname{round}(x) = \lfloor x + 1/2 \rfloor$.

**Claim 1 (the table).** After the loop of lines L5 to L7, $T[k] = T(k)$ for each $k$, and line L8 sets $O(x, y) = T(I(x, y))$.

*Proof.* Lines L2 and L3 count each pixel once in the bin of its value, so $h$ is the histogram and $\sum_k h[k] = N$, the value from line L1. Line L4 sets $c = 0$. Before the step for $k$ of the loop of line L5, $c = c(k-1)$, with $c(-1) = 0$; line L6 adds $h[k]$, so $c = c(k)$ at line L7, and the invariant holds for the next step. For integers $a \ge 0$ and $N \ge 1$,

$$\Big\lfloor \frac{2a + N}{2N} \Big\rfloor = \Big\lfloor \frac{a}{N} + \frac12 \Big\rfloor,$$

because the two fractions are equal. With $a = (L-1)c(k)$, line L7 stores $T(k)$. Line L8 reads the table at the value of each pixel. $\square$

**Claim 2 (shape of the map).** $T$ is nondecreasing, $0 \le T(k) \le L-1$, and $T(L-1) = L-1$.

*Proof.* $c$ is nondecreasing because $h[k] \ge 0$, and $x \mapsto \lfloor x + 1/2 \rfloor$ is nondecreasing, so $T$ is nondecreasing. $0 \le c(k) \le N$ gives $0 \le (L-1)c(k)/N \le L-1$, and rounding keeps an integer bound, so $0 \le T(k) \le L-1$. Also $c(L-1) = N$, so $T(L-1) = \lfloor L - 1 + 1/2 \rfloor = L - 1$. $\square$

So the output is a valid image, and the map keeps the order of the levels: if $I(p) < I(q)$ then $O(p) \le O(q)$. It can merge two levels but it never swaps them.

**Claim 3 (near uniform output).** Let $G(s)$ be the fraction of output pixels with a value of at most $s$, and $h_{\max} = \max_k h[k]$. For each $s \in \{0, \ldots, L-2\}$,

$$\frac{s + 1/2}{L-1} - \frac{h_{\max}}{N} \le G(s) < \frac{s + 1/2}{L-1}.$$

*Proof.* Fix $s \le L-2$. Let $K$ be the largest $k$ with $T(k) \le s$, or $K = -1$ if there is none, and set $c(-1) = 0$. By Claim 2, $T(k) \le s$ holds exactly for $k \le K$, so the output pixels with value at most $s$ are the input pixels with value at most $K$, and $G(s) = c(K)/N$.

Upper bound. If $K = -1$ then $G(s) = 0$, which is below the bound. Otherwise $T(K) \le s$ means $\lfloor (L-1)c(K)/N + 1/2 \rfloor \le s$, so $(L-1)c(K)/N + 1/2 < s + 1$, which is the bound.

Lower bound. $T(L-1) = L - 1 > s$, so $K + 1 \le L - 1$ and $T(K+1) \ge s + 1$. That is $(L-1)c(K+1)/N + 1/2 \ge s + 1$, so $c(K+1)/N \ge (s + 1/2)/(L-1)$. Then $c(K) = c(K+1) - h[K+1] \ge c(K+1) - h_{\max}$, and the bound follows. $\square$

The output cumulative fraction is therefore within one input bin of the uniform target, but it is equal to the target only when no single input level is too large. For $s = L - 1$, $G(L-1) = 1$.

**Claim 4 (idempotence).** Equalizing $O$ again gives $O$.

*Proof.* Let $T_2$ be the map that the algorithm computes for $O$, and let $s$ be a value that occurs in $O$, so $s = T(k_0)$ for some $k_0$ with $h[k_0] > 0$. Let $K$ be the largest $k$ with $T(k) \le s$; then $K \ge k_0$. As in the proof of Claim 3, the number of pixels of $O$ with value at most $s$ is $c(K)$. So $T_2(s) = \operatorname{round}((L-1)c(K)/N) = T(K)$. Claim 2 and $k_0 \le K$ give $s = T(k_0) \le T(K) \le s$, so $T_2(s) = s$. Each pixel of $O$ has such a value $s$, so $T_2(O) = O$. $\blacksquare$
