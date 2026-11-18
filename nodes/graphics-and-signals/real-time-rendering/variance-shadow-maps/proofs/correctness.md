---
title: The variance shadow map value is a sharp upper bound on the filtered lit fraction, by the one-sided Chebyshev (Cantelli) inequality
proves: [correctness]
status: full
---

We use the notation of the page. A filter is a set of texels $T$ with weights $w_k \ge 0$ that sum to 1. The filter defines a discrete distribution: the random depth $Z$ takes the depth $d_k$ of texel $k$ with probability $w_k$. A texel is lit for the receiver depth $t$ when $d_k \ge t$, so the true filtered lit fraction is $\Pr[Z \ge t]$. This is the value that [percentage-closer filtering](/percentage-closer-filtering/) computes with the same weights and the bias 0. The arithmetic is exact.

## Filtering the moments

**Lemma 1.** After lines L1 and L2, the texel $(i, j)$ of the filtered map holds $(\mu, \mu_2) = (E[Z], E[Z^2])$ for the box filter: the uniform weights on the texels of the $(2r + 1) \times (2r + 1)$ square around $(i, j)$ that lie inside the map.

*Proof.* Line L1 stores $(d, d^2)$ at each texel. The summed-area table holds at $(j', i')$ the sum of a moment over the texels with row less than $j'$ and column less than $i'$. The sum over the rectangle of rows $[y_0, y_1)$ and columns $[x_0, x_1)$ is then $t[y_1][x_1] - t[y_0][x_1] - t[y_1][x_0] + t[y_0][x_0]$, by inclusion and exclusion: a texel inside the rectangle is counted once, and a texel outside is counted by an equal number of plus and minus terms. Dividing by the number of texels in the rectangle gives the mean of $d$ and of $d^2$ over it. $\square$

The same holds for any linear filter with nonnegative weights that sum to 1, such as a Gaussian or a mipmap level, because a weighted mean of $d$ and of $d^2$ is the first and second moment of the weighted distribution. This is the property that the binary depth test does not have and that makes the map filterable.

## The bound

**Theorem 2 (Cantelli).** Let $Z$ have mean $\mu$ and variance $\sigma^2 = \mu_2 - \mu^2$. For $t > \mu$,

$$\Pr[Z \ge t] \le p_{\max}(t) = \frac{\sigma^2}{\sigma^2 + (t - \mu)^2}.$$

*Proof.* Let $a = t - \mu > 0$. For every $u \ge 0$, the event $Z - \mu \ge a$ implies $Z - \mu + u \ge a + u > 0$, so it implies $(Z - \mu + u)^2 \ge (a + u)^2$. By [Markov's inequality](/markov-inequality/) applied to the nonnegative variable $(Z - \mu + u)^2$,

$$\Pr[Z \ge t] \le \frac{E[(Z - \mu + u)^2]}{(a + u)^2} = \frac{\sigma^2 + u^2}{(a + u)^2}.$$

Take $u = \sigma^2 / a$. The numerator is $\sigma^2 (a^2 + \sigma^2) / a^2$ and the denominator is $(a^2 + \sigma^2)^2 / a^2$, so the bound is $\sigma^2 / (\sigma^2 + a^2)$. If $\sigma^2 = 0$, then $Z = \mu < t$ with probability 1, and both sides are 0. $\square$

**Corollary 3.** With the minimum variance 0 and no bleeding reduction, the lookup (lines L3 to L6) returns a value $p$ with $\Pr[Z \ge t] \le p \le 1$.

*Proof.* If $t \le \mu$, line L4 returns 1, which is an upper bound on any probability. Otherwise line L5 computes $\sigma^2 \ge 0$ (the variance of a distribution is nonnegative, and in exact arithmetic $\mu_2 - \mu^2$ is that variance), and line L6 returns $p_{\max}(t)$, which is at most 1 and at least $\Pr[Z \ge t]$ by Theorem 2. $\square$

This is a proved property, and it is the claim of the method. The inequality in the paper of Donnelly and Lauritzen is on $\Pr[x \ge t]$, the fraction that is not occluded, although their abstract calls it a bound on the fraction occluded. The occluded fraction gets the lower bound $1 - p_{\max}$.

## The bound is sharp

**Proposition 4.** For every $\mu$, every $\sigma^2 > 0$ and every $t > \mu$, the two-point distribution with $Z = t$ with probability $q = \sigma^2 / (\sigma^2 + a^2)$ and $Z = \mu - \sigma^2 / a$ otherwise, $a = t - \mu$, has mean $\mu$, variance $\sigma^2$ and $\Pr[Z \ge t] = q = p_{\max}(t)$. So no function of $(\mu, \mu_2)$ alone gives a smaller upper bound.

*Proof.* The mean is $\mu + q a - (1 - q) \sigma^2 / a = \mu + \sigma^2 a / (\sigma^2 + a^2) - \sigma^2 a / (\sigma^2 + a^2) = \mu$. The variance is $q a^2 + (1 - q) \sigma^4 / a^2 = \sigma^2 a^2 / (\sigma^2 + a^2) + \sigma^4 / (\sigma^2 + a^2) = \sigma^2$. The point $\mu - \sigma^2 / a$ is less than $t$, so $\Pr[Z \ge t] = q$. $\square$

**Proposition 5.** For one planar occluder at depth $d_1$ with weight $w_1$ and one planar receiver at depth $d_2 > d_1$ with weight $w_2 = 1 - w_1$, the lookup at $t = d_2$ returns the true lit fraction $w_2$.

*Proof.* With $\Delta = d_2 - d_1$: $\mu = d_2 - w_1 \Delta$, so $t - \mu = w_1 \Delta$, and $\sigma^2 = w_1 w_2 \Delta^2$. Then $p_{\max} = w_1 w_2 \Delta^2 / (w_1 w_2 \Delta^2 + w_1^2 \Delta^2) = w_2 / (w_2 + w_1) = w_2$. $\square$

The gap between $p_{\max}$ and the true fraction is light bleeding. It is large when a filter region holds two occluders at different depths over a receiver: the depths $\{1, 2\}$ with the receiver at 3 give $1/10$, and $\{1, 9\}$ with the receiver at 10 give $16/41$, while the true lit fraction is 0 in both cases.

## The two tunings

**Proposition 6.** (a) A minimum variance $v_{\min}$ in line L5 keeps the upper bound. (b) The bleeding reduction of line L7 with an amount $c \in (0, 1)$ can return less than the true lit fraction, so it does not keep the bound.

*Proof.* (a) For a fixed $t > \mu$, the map $v \mapsto v / (v + a^2)$ increases in $v$, so replacing $\sigma^2$ by $\max(\sigma^2, v_{\min})$ does not decrease $p$; it stays at least $\Pr[Z \ge t]$. (b) Take the planar case of Proposition 5 with $w_2 = 2/3$ and $c = 1/5$. The lookup gives $p = 2/3$, and line L7 gives $(2/3 - 1/5)/(4/5) = 7/12 < 2/3$. $\square$

The minimum variance is there to avoid a zero or negative variance from rounding in floating point, which shows as acne. Both values are tunings, not derived quantities.
