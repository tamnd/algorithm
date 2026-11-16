---
title: Correctness of block matching stereo
proves: [correctness]
status: full
---

We prove that BLOCK-MATCH returns, for each left pixel $p$, the least disparity $d^*(p)$ in $[0, D)$ with the least window cost $S_d(p)$, where $S_d(u, v) = \sum_{|i|, |j| \le r} e_d(\operatorname{cl}_W(u + i), \operatorname{cl}_H(v + j))$, $\operatorname{cl}_N(x) = \min(\max(x, 0), N - 1)$, and $e_d$ is the pixel cost of line L3.

## Lemma 1. Line L6 returns $S_d(u, v)$

Let $P$ be the padded image of line L4: it has $H + 2r$ rows and $W + 2r$ columns, and $P(x, y) = e_d(\operatorname{cl}_W(x - r), \operatorname{cl}_H(y - r))$. Let $S[y][x] = \sum_{y' < y} \sum_{x' < x} P(x', y')$ for $0 \le y \le H + 2r$ and $0 \le x \le W + 2r$.

The code builds $S$ row by row: with $a_y(x) = \sum_{x' < x} P(x', y)$ the running sum of row $y$, it sets $S[y + 1][x] = S[y][x] + a_y(x)$ and $S[0][x] = S[y][0] = 0$. By induction on $y$, this is the sum above.

For any $0 \le y_0 \le y_1$ and $0 \le x_0 \le x_1$, the block of rows $y_0 \le y' < y_1$ and columns $x_0 \le x' < x_1$ has the sum $S[y_1][x_1] - S[y_0][x_1] - S[y_1][x_0] + S[y_0][x_0]$, by inclusion and exclusion: the first term counts the block together with the rows above it and the columns left of it, the next two terms remove those, and the last term adds back the corner that was removed twice.

With $k = 2r + 1$, $y_0 = v$, $y_1 = v + k$, $x_0 = u$, $x_1 = u + k$, the block is $P(u + r + i, v + r + j)$ for $|i|, |j| \le r$, and

$$P(u + r + i, v + r + j) = e_d(\operatorname{cl}_W(u + i), \operatorname{cl}_H(v + j)).$$

So line L6 returns exactly $S_d(u, v)$. $\square$

## Lemma 2. The loop invariant of line L2

**Invariant.** Before the iteration for disparity $d$, for every pixel $p$: $\textit{best}[p] = \min_{0 \le d' < d} S_{d'}(p)$ (or $\infty$ if $d = 0$), and $\textit{disp}[p]$ is the least $d' < d$ with $S_{d'}(p) = \textit{best}[p]$ (or 0 if $d = 0$).

**Start.** Line L1 sets $\textit{best}[p] = \infty$ and $\textit{disp}[p] = 0$, which is the claim for $d = 0$.

**Step.** In the iteration for $d$, line L6 gives $c = S_d(p)$ by Lemma 1. If $c < \textit{best}[p]$, then $c$ is the new least value and $d$ is the only disparity so far that reaches it, so the update of line L7 restores the invariant for $d + 1$. If $c \ge \textit{best}[p]$, the least value does not change, and the least disparity that reaches it is still $\textit{disp}[p]$, because any earlier disparity is less than $d$. So the invariant holds for $d + 1$ without a change. The pixels are independent of each other, so the order of line L5 does not matter.

**End.** After the iteration for $D - 1$, $\textit{disp}[p]$ is the least $d$ in $[0, D)$ with $S_d(p) = \min_{d'} S_{d'}(p)$, which is $d^*(p)$. $\square$

## Theorem

BLOCK-MATCH returns $d^*$ for every pixel. This follows from Lemma 2 at the end of the loop. It holds for SAD and SSD alike, because the proof uses only the values of $e_d$, and for any other pixel cost put in line L3. $\square$

## What the theorem does not say

The theorem says that the code returns the minimizer of the window cost. It does not say that this minimizer is the true disparity. Where a window holds two depths, where the image has no texture, or where the true match is hidden or outside the right image, the minimizer can be wrong while the code is correct. The tests show both: the code equals the brute force definition on random images, and it recovers the true disparity away from depth edges and borders on synthetic scenes.

## Exactness

All quantities are integers. The largest value is an entry of $S$, at most $(W + 2r)(H + 2r) \max e_d$. On the word RAM with words of $w$ bits it fits if $(W + 2r)(H + 2r) \max e_d < 2^w$, so the computation is exact, with no rounding.
