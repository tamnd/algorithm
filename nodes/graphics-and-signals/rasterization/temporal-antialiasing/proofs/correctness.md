---
title: TAA computes an exponentially weighted mean of jittered samples, equals supersampling with Halton samples when the weight is 1/t, follows exact integer motion, and the clamp keeps each output inside the range of its neighborhood
proves: [correctness]
status: full
---

Write $x_t[p]$ for the sample of frame $t$ at pixel $p = (i, j)$, taken at the point $(i + o_t, j + o'_t)$ with $(o_t, o'_t) = (h_2(t), h_3(t))$, the radical inverses of $t$ in bases 2 and 3; both lie in $[0, 1)$, so each sample lies inside its pixel. Write $S_t$ for the image that frame $t$ returns, and $\alpha_t \in (0, 1]$ for the blend weight of frame $t$. Line L4 sets $S_1 = x_1$, and line L9 sets $S_t[p] = \alpha_t x_t[p] + (1 - \alpha_t) \tilde h_t[p]$ for $t \ge 2$, where $\tilde h_t[p]$ is the history value after lines L5 to L8.

**Lemma 1 (the fetch at a pixel center).** If the motion at $p$ is an integer vector $v$ and $p - v$ is a pixel of the image, then line L6 returns $S_{t-1}[p - v]$.

*Proof.* Line L5 gives the point $q = p + (1/2, 1/2) - v$, the center of pixel $p - v$. The bilinear fetch subtracts $1/2$, which gives the integer point $p - v$, so the fractional offsets are 0 and the weight of the texel $p - v$ is 1. $\square$

**Theorem 1 (a static scene).** Let the scene and the camera be still, so the motion is zero, and turn the clamp off. Then for $t \ge 1$,

$$S_t[p] = \Big(\prod_{k=2}^{t} (1 - \alpha_k)\Big) x_1[p] + \sum_{k=2}^{t} \alpha_k \Big(\prod_{l=k+1}^{t} (1 - \alpha_l)\Big) x_k[p],$$

and the weights are nonnegative and sum to 1. For a constant $\alpha$, the weight of frame $k \ge 2$ is $\alpha (1 - \alpha)^{t-k}$ and that of frame 1 is $(1 - \alpha)^{t-1}$.

*Proof.* By Lemma 1 with $v = 0$, the history value is $S_{t-1}[p]$. For $t = 1$ the formula is $x_1[p]$. If it holds for $t - 1$, then $S_t[p] = \alpha_t x_t[p] + (1 - \alpha_t) S_{t-1}[p]$, which multiplies every old weight by $1 - \alpha_t$ and adds the weight $\alpha_t$ for frame $t$; this is the formula for $t$. The weights sum to 1 by the same induction: $\alpha_t + (1 - \alpha_t) \cdot 1 = 1$. $\square$

**Theorem 2 (the weight 1/t is supersampling).** Under the conditions of Theorem 1 with $\alpha_t = 1/t$, $S_t[p] = \frac1t \sum_{k=1}^{t} x_k[p]$: the mean of the samples at the first $t$ points of the Halton sequence, which is [supersampling](/supersampling-antialiasing/) of pixel $p$ with this sample pattern.

*Proof.* For $t = 1$ both sides are $x_1[p]$. If $S_{t-1}[p]$ is the mean of $t - 1$ samples, then $S_t[p] = \frac1t x_t[p] + \frac{t-1}{t} \cdot \frac{1}{t-1} \sum_{k<t} x_k[p]$, the mean of $t$ samples. $\square$

The Halton points in bases 2 and 3 are equidistributed in the unit square, so for a scene whose color is a Riemann integrable function on each pixel, this mean tends to the box-filtered pixel value as $t \to \infty$.

**Theorem 3 (integer motion).** Let frame $t$ show a fixed picture $F$ moved by $t v$ for an integer vector $v$, so that $x_t[p] = F((i, j) + (o_t, o'_t) - t v)$, and let the motion be $v$ at every pixel. Turn the clamp off and take $\alpha_t = 1/t$. If the pixels $p - (t - k) v$ lie in the image for all $1 \le k \le t$, then $S_t[p] = \frac1t \sum_{k=1}^{t} F(p + (o_k, o'_k) - t v)$, the supersampled value of frame $t$ at $p$ with the first $t$ Halton points.

*Proof.* By induction on $t$, for all pixels that satisfy the condition. For $t = 1$ it is the definition. For $t \ge 2$, the pixel $p - v$ satisfies the condition for $t - 1$, and by Lemma 1 the history value is $S_{t-1}[p - v] = \frac{1}{t-1} \sum_{k<t} F(p - v + (o_k, o'_k) - (t-1) v)$, which is $\frac{1}{t-1} \sum_{k<t} F(p + (o_k, o'_k) - t v)$. The new sample is $x_t[p] = F(p + (o_t, o'_t) - t v)$, and line L9 with $\alpha_t = 1/t$ forms the mean of the $t$ terms, as in Theorem 2. $\square$

**Lemma 4 (the clamp).** With the clamp on, each channel of $S_t[p]$ lies between the smallest and the largest value of that channel among the current samples $x_t$ in the $3 \times 3$ neighborhood of $p$.

*Proof.* Lines L7 and L8 clamp each channel of the history value into $[\mathrm{lo}, \mathrm{hi}]$, the range of the neighborhood, which contains $x_t[p]$ itself. Line L9 forms a convex combination of two values in this interval, since $0 < \alpha_t \le 1$. $\square$

**The noise of a constant weight.** Let the samples $x_k[p]$ of a still pixel be independent with the same mean $\mu$ and variance $\sigma^2$, as with random jitter. By Theorem 1 with a constant $\alpha$, $S_t[p]$ has mean $\mu$, and its variance $\sigma^2 \big((1-\alpha)^{2(t-1)} + \sum_{k=2}^{t} \alpha^2 (1-\alpha)^{2(t-k)}\big)$ tends to $\sigma^2 \alpha^2 / (1 - (1-\alpha)^2) = \sigma^2 \alpha / (2 - \alpha)$. So a constant weight $\alpha$ gives, in the limit, the noise of a mean of $(2 - \alpha)/\alpha$ independent samples, and it never converges further: the variance does not tend to zero. For $\alpha = 1/10$ this is the noise of 19 samples.

These statements are the whole guarantee. With motion that is not an integer vector, the bilinear fetch blurs the history a little in every frame; with the clamp, history that the clamp cuts is lost; and with wrong or missing motion vectors, the output can show old colors. TAA is a heuristic outside the conditions above. $\blacksquare$
