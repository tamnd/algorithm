---
title: SSIM computes the weighted local statistics, is symmetric, lies in (-1, 1], and equals 1 only for equal images
proves: [correctness]
status: full
---

The images $x$ and $y$ have $W \times H$ pixels with real values. The window is a list of $k$ weights $w_0, \ldots, w_{k-1} \ge 0$ with $\sum_a w_a = 1$, and the two-dimensional weight is $w_a w_b$. A valid window position is $(i, j)$ with $0 \le i \le H - k$ and $0 \le j \le W - k$, and there are $M = (W - k + 1)(H - k + 1) \ge 1$ of them. The constants are $C_1 = (K_1 L)^2 > 0$ and $C_2 = (K_2 L)^2 > 0$, where $L > 0$ is the dynamic range. For a position $P = (i, j)$ and an image $f$ we write

$$E_P[f] = \sum_{a=0}^{k-1} \sum_{b=0}^{k-1} w_a w_b\, f(i + a, j + b).$$

The weights $w_a w_b$ are nonnegative and sum to $(\sum_a w_a)^2 = 1$, so $E_P$ is the expectation of a probability distribution on the $k \times k$ window.

**Claim 1 (the sums).** Line L2 gives $F_f(P) = E_P[f]$ for $f \in \{x, y, x^2, y^2, xy\}$.

*Proof.* The row pass computes $R(r, j) = \sum_b w_b f(r, j + b)$ for each row $r$ and each $j \le W - k$. The column pass computes $\sum_a w_a R(i + a, j) = \sum_a \sum_b w_a w_b f(i + a, j + b) = E_P[f]$. $\square$

**Claim 2 (the statistics).** At position $P$, lines L5 and L6 give $\mu_x = E_P[x]$, $\mu_y = E_P[y]$, $\sigma_x^2 = E_P[(x - \mu_x)^2]$, $\sigma_y^2 = E_P[(y - \mu_y)^2]$ and $\sigma_{xy} = E_P[(x - \mu_x)(y - \mu_y)]$. So $\sigma_x^2, \sigma_y^2 \ge 0$.

*Proof.* Line L5 is Claim 1. $E_P$ is linear and $E_P[1] = 1$, so $E_P[(x - \mu_x)(y - \mu_y)] = E_P[xy] - \mu_x E_P[y] - \mu_y E_P[x] + \mu_x \mu_y = E_P[xy] - \mu_x \mu_y$, which is line L6. The variances are the case $y = x$, and they are expectations of squares under nonnegative weights. $\square$

**Claim 3 (the formula).** Line L7 gives $S = l \cdot cs$ with

$$l = \frac{2\mu_x\mu_y + C_1}{\mu_x^2 + \mu_y^2 + C_1}, \qquad cs = \frac{2\sigma_{xy} + C_2}{\sigma_x^2 + \sigma_y^2 + C_2},$$

and this is the product $l \cdot c \cdot s$ of the luminance, contrast and structure terms with $C_3 = C_2/2$.

*Proof.* The first part is the form of line L7. The denominators are positive because $C_1, C_2 > 0$ and the variances are nonnegative. With $\sigma_x = \sqrt{\sigma_x^2}$, the contrast and structure terms are $c = (2\sigma_x\sigma_y + C_2)/(\sigma_x^2 + \sigma_y^2 + C_2)$ and $s = (\sigma_{xy} + C_3)/(\sigma_x\sigma_y + C_3)$. With $C_3 = C_2/2$, $s = (2\sigma_{xy} + C_2)/(2\sigma_x\sigma_y + C_2)$, and the factor $2\sigma_x\sigma_y + C_2 > 0$ cancels in $c \cdot s$, which gives $cs$. $\square$

**Claim 4 (symmetry).** $S$ at each position, and so the mean, does not change when $x$ and $y$ are swapped.

*Proof.* The swap exchanges $\mu_x$ with $\mu_y$ and $\sigma_x^2$ with $\sigma_y^2$, and keeps $\mu_x\mu_y$ and $\sigma_{xy}$. Each of $l$ and $cs$ is unchanged. $\square$

**Claim 5 (the range).** $-1 < S \le 1$ at each position, and $-1 < \text{MSSIM} \le 1$.

*Proof.* The denominators are positive by Claim 3. $l \le 1$ is the same as $2\mu_x\mu_y \le \mu_x^2 + \mu_y^2$, that is $(\mu_x - \mu_y)^2 \ge 0$. $l > -1$ is the same as $2\mu_x\mu_y + C_1 > -(\mu_x^2 + \mu_y^2 + C_1)$, that is $(\mu_x + \mu_y)^2 + 2C_1 > 0$. In the same way, $cs \le 1$ is the same as $E_P[((x - \mu_x) - (y - \mu_y))^2] \ge 0$, and $cs > -1$ is the same as $E_P[((x - \mu_x) + (y - \mu_y))^2] + 2C_2 > 0$. So $l, cs \in (-1, 1]$. Then $|S| = |l|\,|cs| \le 1$, and $S = -1$ would need $|l| = |cs| = 1$ with opposite signs, so one of them equal to $-1$, which is not possible. MSSIM, the value of line L9, is the mean of $M$ numbers in $(-1, 1]$, so it is in $(-1, 1]$ too. $\square$

**Claim 6 (the maximum).** $S = 1$ at position $P$ if and only if $x = y$ at each pixel of the window with a positive weight. MSSIM $= 1$ if and only if this holds at every valid position; if every weight is positive, this means $x = y$ everywhere.

*Proof.* If $x = y$ wherever the weight is positive, then $E_P$ gives $\mu_x = \mu_y$, $\sigma_x^2 = \sigma_y^2 = \sigma_{xy}$, so $l = cs = 1$. Conversely, let $S = 1$. By Claim 5, $|l| \le 1$ and $|cs| \le 1$, so $|l| = |cs| = 1$, and since neither can be $-1$, $l = cs = 1$. $l = 1$ gives $\mu_x = \mu_y$. $cs = 1$ gives $E_P[(d - \mu_d)^2] = 0$ for $d = x - y$ and $\mu_d = \mu_x - \mu_y = 0$, so $d = 0$ at each pixel with a positive weight.

Each $S \le 1$, so the mean is 1 if and only if each $S$ is 1. With all weights positive, each pixel $(r, q)$ lies in the valid window at $i = \min(r, H - k)$, $j = \min(q, W - k)$, so $x(r, q) = y(r, q)$. $\blacksquare$
