---
title: Geohash encodes the interleaved bits of the cell that holds the point
proves: [correctness, termination]
status: full
---

We use the names of the pseudocode GEOHASH-ENCODE$(\varphi, \lambda, p)$, with $\varphi \in [-90, 90]$ and $\lambda \in [-180, 180]$. Let $t$ be the number of passes of the loop of line L3 so far, so $t = 5|s| + bits$. Write $a(t) = \lceil t/2 \rceil$ and $e(t) = \lfloor t/2 \rfloor$ for the numbers of longitude and latitude bits among the first $t$ bits. For an integer $m \ge 0$ and a value $z$ in a range $[L, H]$, let
$$\operatorname{idx}_m(z) = \min\!\Big(\Big\lfloor \frac{z - L}{H - L}\, 2^m \Big\rfloor,\ 2^m - 1\Big),$$
the index of the part of $[L, H]$ that holds $z$ when the range is cut into $2^m$ equal parts, with the top value $z = H$ in the top part. Write $X_t = \operatorname{idx}_{a(t)}(\lambda)$ over $[-180, 180]$ and $Y_t = \operatorname{idx}_{e(t)}(\varphi)$ over $[-90, 90]$.

**Claim.** The output $s$ has $p$ characters, and its $5p$ bits are $b_1 \ldots b_{5p}$, where the subsequence $b_1 b_3 b_5 \ldots$ is the binary form of $X_{5p}$ with $a(5p)$ digits and $b_2 b_4 \ldots$ is the binary form of $Y_{5p}$ with $e(5p)$ digits. The point lies in the cell given by the final intervals.

**Invariant.** At the test of line L3, after $t$ passes:

1. $\lambda_{lo} = -180 + 360\, X_t / 2^{a(t)}$ and $\lambda_{hi} = \lambda_{lo} + 360 / 2^{a(t)}$, and $\lambda_{lo} \le \lambda \le \lambda_{hi}$, with $\lambda < \lambda_{hi}$ unless $\lambda_{hi} = 180$.
2. The same holds for $\varphi$, with $-90$, $180$, $e(t)$ and $Y_t$.
3. The longitude bits produced so far, in order, are the binary form of $X_t$ with $a(t)$ digits, and the latitude bits are the binary form of $Y_t$ with $e(t)$ digits.
4. $ch$ is the number whose binary form is the last $bits$ bits produced, $0 \le bits \le 4$, and $s$ holds the first $5|s|$ bits, five per character, as the indices of its characters in $\Sigma$.
5. $even$ is true exactly when $t$ is even.

*Initialization.* At $t = 0$, line L1 sets the full ranges, $a(0) = e(0) = 0$ and $X_0 = Y_0 = 0$, so parts 1 and 2 hold, with $\lambda < 180$ or $\lambda_{hi} = 180$. No bits exist, so part 3 holds. Line L2 sets $s$ empty, $bits = 0$, $ch = 0$ and $even$ true, so parts 4 and 5 hold.

*Maintenance.* Take a pass with $t$ even, so by part 5 line L4 runs and cuts the longitude interval; the odd case is the same with line L5 and the latitude. The pass makes bit $b_{t+1}$, an odd position, and $a(t+1) = a(t) + 1$, $e(t+1) = e(t)$. Let $w = 360 / 2^{a(t)}$ and $mid = \lambda_{lo} + w/2$.

- If $\lambda \ge mid$, the bit is 1 and the new interval is $[mid, \lambda_{hi}]$. Then $(\lambda - (-180))/360 \cdot 2^{a(t)+1}$ lies in $[2X_t + 1, 2X_t + 2]$, and it equals $2X_t + 2$ only when $\lambda = \lambda_{hi}$, which by part 1 happens only when $\lambda_{hi} = 180$, where the minimum in $\operatorname{idx}$ caps the index. So $X_{t+1} = 2X_t + 1$.
- If $\lambda < mid$, the bit is 0, the new interval is $[\lambda_{lo}, mid]$, and the same computation gives a value in $[2X_t, 2X_t + 1)$, so $X_{t+1} = 2X_t$, and $\lambda$ is strictly below the new upper end.

In both cases the new interval has the form of part 1 for $X_{t+1}$ and $a(t+1)$, it holds $\lambda$, and the upper end stays strict unless it is $180$. The latitude is not changed and $e$ is not changed, so part 2 holds. Appending a bit $\beta$ to the binary form of $X_t$ gives $2X_t + \beta = X_{t+1}$, so part 3 holds. Line L4 sets $ch \leftarrow 2ch + \beta$, which appends the bit to the binary form of $ch$, and line L6 adds 1 to $bits$. If $bits$ becomes 5, line L7 appends the character of index $ch$, which holds the last five bits, and resets $bits$ and $ch$ to 0. So part 4 holds. Line L6 flips $even$, and $t + 1$ is odd, so part 5 holds.

*Termination.* Each pass adds 1 to $t = 5|s| + bits$. Since $bits \le 4$ by part 4, $|s|$ grows by one every five passes, so after exactly $5p$ passes $|s| = p$ and the loop stops. At that point $bits = 0$, so all $5p$ bits are in $s$. By part 3 they are the bits of the claim, and by parts 1 and 2 the point lies in the final intervals. $\blacksquare$

**Prefix property.** The bits of a pass do not depend on $p$: the loop for length $p$ runs the same passes as the loop for length $q < p$ and then more. So the geohash of length $q$ is the prefix of length $q$ of the geohash of length $p$, and the cell of the longer string lies inside the cell of the shorter one, since each pass keeps half of an interval.
