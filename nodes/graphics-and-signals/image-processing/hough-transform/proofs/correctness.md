---
title: The Hough accumulator counts the points of each line cell, and a segment fills at most two cells
proves: [correctness]
status: full
---

Let $P$ be the list of edge points, $\theta_k = k\pi/T$, and $\rho_k(p) = x \cos\theta_k + y \sin\theta_k$ for $p = (x, y)$. For an integer $j$, the cell $(k, j)$ is the set of lines at the angle $\theta_k$ with a distance in $B_j = [j - \tfrac{1}{2}, j + \tfrac{1}{2})$. The bins $B_j$ cover the real line and do not overlap, so every real $\rho$ is in exactly one of them, the bin $\operatorname{round}(\rho)$ with halves rounded up. Throughout, we treat $\cos\theta_k$, $\sin\theta_k$ and line L5 as exact, and we discuss the floating point form at the end.

**Lemma 1 (every vote has a cell).** For each point $p$ of the image and each $k$, $|\rho_k(p)| \le D$, so $-D \le \operatorname{round}(\rho_k(p)) \le D$.

*Proof.* By the inequality of Cauchy and Schwarz, $|\rho_k(p)| \le \sqrt{x^2 + y^2} \cdot \sqrt{\cos^2\theta_k + \sin^2\theta_k} = \sqrt{x^2 + y^2} \le \sqrt{(W - 1)^2 + (H - 1)^2} \le D$, because $0 \le x \le W - 1$ and $0 \le y \le H - 1$. Since $D$ is an integer, rounding a number in $[-D, D]$ gives an integer in $[-D, D]$. $\square$

**Theorem 1 (the accumulator is the brute force count).** At line L7, for every $k$ and every $j$ with $-D \le j \le D$,

$$\mathrm{acc}[k][j] = \left|\{\, p \in P : \rho_k(p) \in B_j \,\}\right|,$$

counted with multiplicity if $P$ has repeated points.

*Proof.* Line L2 sets every counter to 0, and line L6 is the only change. Lines L3 and L4 run line L6 exactly once for each pair of a point $p$ of $P$ and an angle index $k$, and that run adds 1 to the counter $(k, \operatorname{round}(\rho_k(p)))$, which exists by Lemma 1. So after the loop, the counter $(k, j)$ is the number of pairs $(p, k)$ with $\operatorname{round}(\rho_k(p)) = j$, that is, with $\rho_k(p) \in B_j$. $\blacksquare$

Summing over $j$ gives $\sum_j \mathrm{acc}[k][j] = N$ for each $k$: each point votes once per angle.

**Corollary 1 (a line on the grid gets all its votes).** Let $\ell$ be the line $x \cos\theta_k + y \sin\theta_k = \rho$ with $\rho \in B_j$, and let $m$ points of $P$ lie on $\ell$. Then $\mathrm{acc}[k][j] \ge m$.

*Proof.* Each of the $m$ points has $\rho_k(p) = \rho \in B_j$, so Theorem 1 counts it. $\square$

**Theorem 2 (the spread of a segment).** Let $S$ be a set of points on a segment of length $L$ of the line with the normal angle $\theta$, and let $k$ be an angle index with $|\theta - \theta_k| \le \delta$. Then the values $\rho_k(p)$ for $p \in S$ lie in an interval of length at most $L \sin\delta$. If $L \sin\delta \le 1$, the votes of $S$ in row $k$ fall in at most 2 adjacent cells, and one of them gets at least $|S| / 2$ votes.

*Proof.* Let $n = (\cos\theta, \sin\theta)$, $n_k = (\cos\theta_k, \sin\theta_k)$ and $u = (-\sin\theta, \cos\theta)$, the direction of the line. Every point of the segment is $c + s u$ for a fixed point $c$ and an $s$ in an interval of length $L$. Then $\rho_k(c + s u) = c \cdot n_k + s\, (u \cdot n_k)$ and $u \cdot n_k = -\sin\theta \cos\theta_k + \cos\theta \sin\theta_k = \sin(\theta_k - \theta)$. So the values form an interval of length at most $L\, |\sin(\theta_k - \theta)| \le L \sin\delta$, for $\delta \le \pi/2$. An interval of length at most 1 meets at most 2 of the bins $B_j$, since each bin has length 1, and these 2 bins are adjacent. The $|S|$ votes are split over at most 2 cells, so one of them gets at least half. $\blacksquare$

The nearest angle bin has $\delta \le \pi/(2T)$, where the angle is taken modulo $\pi$. If the nearest bin is the wrap to $\theta = \pi$, the line is the same as the line at $\theta_0 = 0$ with the sign of $\rho$ flipped, and the same bound holds in row 0. So with $L \sin(\pi/(2T)) \le 1$, a segment of length $L$ puts at least half of its points into one cell. This is why the angle step should be about $1/L$ for the longest lines of interest.

**Peaks.** PEAKS reports a cell exactly when it has at least $\tau$ votes and no cell of its $3 \times 3$ window has more votes, or as many votes and an earlier position in scan order. In a group of adjacent cells with equal votes that are larger than all the cells around them, this rule reports exactly the first cell in scan order. The argument is the one for the tie rule of non-maximum suppression: two cells of the group that are neighbors cannot both win, because the later one sees the earlier one with equal votes.

**Floating point.** The implementation computes $\rho$ in floating point. It rounds with $j = \lfloor \rho \rfloor$ and adds 1 if $\rho - j \ge \tfrac{1}{2}$. This test gives the same answer in floating point as in exact arithmetic on the computed $\rho$. If the exact difference is at least $\tfrac{1}{2}$, the rounded difference is too, because rounding is monotone and $\tfrac{1}{2}$ is a float. If the exact difference is below $\tfrac{1}{2}$, the subtraction is exact. For $j = 0$, $\rho - j = \rho$. For $j \ge 1$, $j \le \rho < j + 1 \le 2j$. For $j \le -1$, $|j| - \tfrac{1}{2} < |\rho| \le |j|$ and $|j| - \tfrac{1}{2} \ge |j|/2$. In the last two cases $\rho$ and $j$ have the same sign and $|j|/2 \le |\rho| \le 2|j|$, so Sterbenz's lemma makes the difference exact. So the rounding of the computed $\rho$ is its true rounding. The form $\lfloor \rho + \tfrac{1}{2} \rfloor$ is not: it rounds the sum first, and for $\rho = 0.5 - 2^{-54}$ the sum rounds to 1. The test computes the reference with exact rational arithmetic on the same floating point values of $\rho$, so the two counts agree exactly.
