---
title: Contrast stretching finds the percentile ends and maps them linearly onto the full range
proves: [correctness]
status: full
---

The image $I$ has $N = WH \ge 1$ pixels with values in $\{0, \ldots, L-1\}$, $L \ge 2$. The fractions satisfy $p_{lo} \ge 0$, $p_{hi} \ge 0$ and $p_{lo} + p_{hi} < 1$. We write $h$ for the histogram, $c(k) = \sum_{j \le k} h[j]$, $c(-1) = 0$, and $s_0 \le s_1 \le \cdots \le s_{N-1}$ for the pixel values in sorted order.

**Claim 1 (the ends).** After the loop of lines L3 to L6, $lo$ is the smallest $k$ with $c(k) > p_{lo}N$ and $hi$ is the smallest $k$ with $c(k) \ge (1 - p_{hi})N$. Both exist, $lo \le hi$, $lo = s_{\lfloor p_{lo} N \rfloor}$ and $hi = s_{\lceil (1 - p_{hi})N \rceil - 1}$.

*Proof.* Line L1 builds $h$ with total $N$. By the same invariant as in [histogram equalization](/histogram-equalization/), $c = c(k)$ at lines L5 and L6 in the step for $k$. Line L5 sets $lo$ at the first $k$ where $c(k) > p_{lo}N$ and never again, because after that $lo \ge 0$; line L6 does the same for $hi$. Both conditions hold at $k = L - 1$, where $c = N$: $N > p_{lo}N$ because $p_{lo} < 1$, and $N \ge (1 - p_{hi})N$ because $p_{hi} \ge 0$. So both ends are set. At $k = hi$, $c(hi) \ge (1 - p_{hi})N > p_{lo}N$, so the condition of line L5 holds at $hi$, and $lo \le hi$.

For the order statistics: $c(k)$ is the number of indices $i$ with $s_i \le k$, and the sorted order gives $c(k) \ge m + 1$ if and only if $s_m \le k$. With $m = \lfloor p_{lo}N \rfloor$, the integer $c(k)$ is greater than $p_{lo}N$ if and only if $c(k) \ge m + 1$, so the smallest such $k$ is $s_m$. With $m = \lceil (1 - p_{hi})N \rceil - 1 \ge 0$, $c(k) \ge (1 - p_{hi})N$ if and only if $c(k) \ge m + 1$, so the smallest such $k$ is $s_m$. $\square$

**Claim 2 (few pixels are clipped).** At most $p_{lo}N$ pixels have a value below $lo$, and at most $p_{hi}N$ pixels have a value above $hi$.

*Proof.* The number of pixels below $lo$ is $c(lo - 1)$. If $lo = 0$ it is 0. Otherwise $lo - 1$ does not meet the condition of line L5, so $c(lo - 1) \le p_{lo}N$. The number above $hi$ is $N - c(hi) \le N - (1 - p_{hi})N = p_{hi}N$. $\square$

**Claim 3 (the map).** If $lo < hi$, the table of lines L8 to L11 is

$$T(k) = \operatorname{round}\Big(\operatorname{clamp}\Big(\frac{(L-1)(k - lo)}{hi - lo}, 0, L-1\Big)\Big)$$

with halves up. $T$ is nondecreasing, $T(k) = 0$ for $k \le lo$, $T(k) = L - 1$ for $k \ge hi$, and $T$ is injective on $\{lo, \ldots, hi\}$.

*Proof.* Let $d = hi - lo \ge 1$ and $x_k = (L-1)(k - lo)/d$. For $k \le lo$, $x_k \le 0$ and the clamp gives 0, which line L9 stores. For $k \ge hi$, $x_k \ge L - 1$ and the clamp gives $L - 1$, which line L10 stores. For $lo < k < hi$, $0 < x_k < L - 1$, and line L11 stores $\lfloor (2(L-1)(k - lo) + d)/(2d) \rfloor = \lfloor x_k + 1/2 \rfloor$. So $T$ is the formula.

The clamp of $x_k$ is nondecreasing in $k$, and so is rounding, so $T$ is nondecreasing. Both ends are levels, so $d \le L - 1$, and for $lo \le k < k' \le hi$ we get $x_{k'} - x_k \ge (L-1)/d \ge 1$. Then $\lfloor x_{k'} + 1/2 \rfloor \ge \lfloor x_k + 1/2 + 1 \rfloor > \lfloor x_k + 1/2 \rfloor$. At the ends, $x_{lo} = 0$ and $x_{hi} = L - 1$ are already in range, so the clamp does not change them, and $T$ is injective on $\{lo, \ldots, hi\}$. $\square$

**Claim 4 (the output).** If $lo < hi$, line L12 gives $O = T(I)$, a valid image whose values include 0 and $L - 1$. If $lo = hi$, line L7 returns $I$ unchanged.

*Proof.* Line L12 reads the table at each pixel, and $T$ takes values in $\{0, \ldots, L-1\}$ by Claim 3. The pixel with value $s_{\lfloor p_{lo}N \rfloor} = lo$ maps to 0, and the pixel with value $hi$ maps to $L - 1$, by Claims 1 and 3. If $lo = hi$, the stretch would divide by zero, and line L7 returns a copy instead. $\blacksquare$
