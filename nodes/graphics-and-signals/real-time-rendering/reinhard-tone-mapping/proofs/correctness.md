---
title: Properties of the Reinhard operator
proves: [correctness]
status: full
---

**Setting.** The input is an image of $p$ pixels with world luminances $L_w(i) \ge 0$, a constant $\delta \ge 0$ with $\delta + L_w(i) > 0$ for every $i$, and a key $a > 0$. Lines L1 to L5 compute

$$\bar L = \exp\Big(\frac1p \sum_i \log(\delta + L_w(i))\Big), \qquad L(i) = \frac{a}{\bar L} L_w(i), \qquad L_d(i) = g(L(i)),$$

with $g(L) = L (1 + L / W^2) / (1 + L)$ for a white point $W > 0$, or $g(L) = L / (1 + L)$ for $W = \infty$. Lines L6 to L14 compute the local operator. The claims are about this computation in exact arithmetic. They do not claim that the output matches what a person sees: that part of the method is a visual heuristic.

**Claim 1 (the log average).** $\bar L$ is the geometric mean of the values $\delta + L_w(i)$. If $\delta = 0$ and all $L_w(i) = c > 0$, then $\bar L = c$ and every $L(i) = a$.

*Proof.* $\exp(\frac1p \sum \log x_i) = (\prod x_i)^{1/p}$, because $\exp$ turns the sum of logarithms into a product. For a constant image the product is $c^p$, so $\bar L = c$ and $L(i) = a c / c = a$. $\square$

**Claim 2 (exposure invariance).** If $\delta = 0$ and all $L_w(i) > 0$, then the global operator gives the same output for the inputs $L_w$ and $c L_w$, for every $c > 0$.

*Proof.* The geometric mean of $c L_w(i)$ is $c \bar L$, so $L(i) = a\, c L_w(i) / (c \bar L)$ is the same value as before, and so is $g(L(i))$. $\square$

For $\delta > 0$ the claim holds only up to the change of $\delta$ relative to the luminances. The paper adds $\delta$ only to avoid $\log 0$ at black pixels.

**Claim 3 (the curve).** For $W = \infty$, $g$ is strictly increasing on $[0, \infty)$, $g(0) = 0$ and $g(L) < 1$ for every $L$. For $W < \infty$, $g$ is strictly increasing on $[0, \infty)$, $g(W) = 1$, $g(L) < 1$ for $L < W$ and $g(L) > 1$ for $L > W$. For every fixed $L \ge 0$, $g$ with white point $W$ tends to $L / (1 + L)$ as $W \to \infty$.

*Proof.* $L / (1 + L) = 1 - 1 / (1 + L)$ is strictly increasing and is below 1. The factor $1 + L / W^2$ is positive and increasing, so the product of the two factors is strictly increasing on $[0, \infty)$, where both are not negative and the first is strictly increasing. At $L = W$,

$$g(W) = \frac{W (1 + 1 / W)}{1 + W} = \frac{W + 1}{1 + W} = 1.$$

Strict monotonicity then gives the two inequalities. The limit holds because $L / W^2 \to 0$. $\square$

So the global operator keeps the order of the pixels: $L_w(i) < L_w(j)$ implies $L_d(i) < L_d(j)$, because $L$ is a positive multiple of $L_w$ and $g$ is strictly increasing. With $W$ set to the largest value of $L$, the brightest pixel maps to exactly 1 and no pixel goes above 1.

**Claim 4 (the separable blur).** Let $K(x, y) = c\, e^{-(x^2 + y^2) / w^2}$ on the square $|x|, |y| \le R$, scaled to sum to 1, and let the image be extended by clamping at the border. Then two 1D passes with the 1D kernel $k(t) = e^{-t^2 / w^2} / \sum_{|u| \le R} e^{-u^2 / w^2}$, first along the rows and then along the columns, give the 2D convolution with $K$.

*Proof.* $e^{-(x^2 + y^2) / w^2} = e^{-x^2 / w^2} e^{-y^2 / w^2}$, and the sum over the square is the product of the two 1D sums, so $K(x, y) = k(x) k(y)$. Clamping is done separately in $x$ and in $y$: the pixel at $(x + d_x, y + d_y)$ after clamping is the pixel at the clamped column and the clamped row. Then

$$\sum_{d_y} k(d_y) \sum_{d_x} k(d_x)\, I(\mathrm{cl}_x(x + d_x), \mathrm{cl}_y(y + d_y)) = \sum_{d_x, d_y} K(d_x, d_y)\, I(\mathrm{cl}_x(x + d_x), \mathrm{cl}_y(y + d_y)).$$

The inner sum is the row pass and the outer sum is the column pass. $\square$

Equation 5 of the paper has the factor $1 / (\pi (\alpha s)^2)$, which makes the kernel integrate to 1 over the plane. On a pixel grid and after the cut at radius $R$ the discrete sum is not exactly 1, so the code divides by the sum. Then a constant image stays constant, which Claim 5 uses.

**Claim 5 (the local operator).** (a) The scale index $m$ that lines L9 to L12 select is in $\{0, \dots, r - 1\}$, and it is the largest $k$ such that $|V_j| < \varepsilon$ for all $j \le k$, or 0 if $|V_0| \ge \varepsilon$. (b) The output is in $[0, 1]$. (c) If $B_m(i) > L(i)$, then $L_d(i) < L(i) / (1 + L(i))$, and if $B_m(i) < L(i)$, then $L_d(i) > L(i) / (1 + L(i))$, before the clip to 1. (d) On a constant image every $V_k$ is 0, $m = r - 1$, and the local operator equals the global operator with $W = \infty$.

*Proof.* (a) $m$ starts at 0, and line L12 sets $m \leftarrow k$ only while every earlier test passed, because the loop stops at the first failure. (b) Each $B_k$ is a weighted average of values $L \ge 0$ with weights that are not negative, so $B_k \ge 0$, and $L / (1 + B_m) \ge 0$; the clip gives at most 1. (c) $x \mapsto L / (1 + x)$ is strictly decreasing for $L > 0$. (d) By Claim 4 and the normalization, each blur of the constant $L$ is $L$, so $V_k = 0 < \varepsilon$ for every $k$, the loop never stops early, $m = r - 1$, and $L_d = L / (1 + L)$, which is below 1, so the clip does nothing. $\square$

Part (c) is the dodging and burning of the paper: a pixel darker than its neighborhood is pushed down and a pixel brighter than its neighborhood is pushed up, so local contrast increases. Which neighborhood is "right" is a visual heuristic of the paper, with $\varepsilon$ and $\varphi$ as tuning.

**Cost.** Lines L1 to L5 take $\Theta(p)$ time and $\Theta(p)$ space for the output. In the local operator, the scale loop of lines L8 to L12 does at most $r$ tests per pixel, $O(p r)$ in total. The $r + 1$ blurs dominate. The separable blur of width $w$ costs $\Theta(p w)$, so the direct method costs $\Theta(p \sum_k 1.6^k) = \Theta(p\, s_{\max})$, where $s_{\max}$ is the largest scale. With an FFT each blur costs $O(p \log p)$, for $O(r p \log p)$ in total. With a blur of constant cost per pixel, for example a recursive filter or a pyramid, the total is $O(p r)$. The memory is $\Theta(p r)$ if all blurs are kept, or $\Theta(p)$ if the scales are processed one after the other and each pixel keeps its current state.
