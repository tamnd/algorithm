---
title: "Comb pilot interpolation keeps the pilots, wraps around the band correctly, and has a bounded error on a short channel"
proves: [correctness]
status: full
---

Notation. $N$ subcarriers, pilots on $p_i = k_0 + iD$ for $i = 0, \ldots, P - 1$ with $P = N / D$, and $Y[k] = H[k] X[k] + W[k]$ after the DFT. The channel has taps $h_0, \ldots, h_{L-1}$, and $H[k] = \sum_l h_l e^{-j 2\pi l k / N}$, the unnormalized DFT of the taps, as on the OFDM page. Write $H(f)$ for the same sum at a real argument $f$; it is smooth and has period $N$ in $f$.

**Lemma 1 (least squares at the pilots).** Line L1 gives $\hat H_{p_i} = H[p_i] + W[p_i] / X[p_i]$. Without noise it is exact.

*Proof.* Divide $Y[p_i]$ by the known nonzero $X[p_i]$. $\square$

**Lemma 2 (the interpolant).** For every $k$, lines L2 to L5 return $(1 - t)\hat H_{p_i} + t\, \hat H_{p_{i+1}}$, where $p_i$ is the last pilot at or before $k$ on the circle, $t = (k - p_i)/D \in [0, 1)$, and $p_P$ means $p_0 + N$. On the pilots ($t = 0$) it returns the pilot estimate.

*Proof.* Line L2 writes $(k - k_0) \bmod N = iD + \text{rem}$ with $0 \le \text{rem} < D$, so $p_i = k_0 + iD$ is the last pilot at or before $k$, counting around the circle, and $\text{rem}$ is the distance from it. Line L3 sets $t = \text{rem}/D$. Line L4 takes the pilot $i$ and the next one, index $(i + 1) \bmod P$, which for $i = P - 1$ is $p_0$, the first pilot of the next period. Line L5 is the linear formula. $\square$

Because $H(f)$ has period $N$, the value at $p_0 + N$ is $H[p_0]$, so the wrap of line L4 interpolates the periodic function $H(f)$ on an unrolled axis, with no edge effect at the band ends.

**Theorem 1 (error bound without noise).** Without noise, for every $k$,

$$|\hat H[k] - H[k]| \le \frac{D^2}{8} \max_f |H''(f)| \le \frac{\pi^2 D^2}{2 N^2} \sum_{l=0}^{L-1} l^2 |h_l|.$$

*Proof.* By Lemmas 1 and 2, $\hat H[k]$ is the linear interpolant of $H(f)$ between $a = p_i$ and $b = a + D$, evaluated at $x = k$. For a twice differentiable complex function $g$ on $[a, b]$, the Peano kernel form of the linear interpolation error is

$$g(x) - \left( \tfrac{b - x}{b - a} g(a) + \tfrac{x - a}{b - a} g(b) \right) = -\int_a^b K(x, s)\, g''(s)\, ds,$$

with $K(x, s) = \frac{(s - a)(b - x)}{b - a}$ for $s \le x$ and $\frac{(x - a)(b - s)}{b - a}$ for $s \ge x$. The kernel is nonnegative and $\int_a^b K(x, s)\, ds = \frac{(x - a)(b - x)}{2} \le \frac{(b - a)^2}{8}$. Taking absolute values inside the integral gives the first bound with $b - a = D$; the argument applies to complex $g$ because it does not use the mean value theorem. For the second bound, $H''(f) = \sum_l (-j 2\pi l / N)^2 h_l e^{-j 2\pi l f / N}$, so $|H''(f)| \le (2\pi / N)^2 \sum_l l^2 |h_l|$. $\square$

The bound shows the design rule: the error scales as $(D \cdot \text{delay} / N)^2$, so the pilot spacing $D$ must be small compared with $N$ divided by the delay spread in samples.

**Theorem 2 (noise on a flat channel).** If $H[k] = H$ for all $k$, the pilot values have $|X[p]| = 1$ and the noise on the pilots is independent $\mathcal{CN}(0, N_0)$, then the linear estimate at fraction $t$ has the error $(1 - t) W_a + t W_b$ with variance $((1 - t)^2 + t^2) N_0$, and the mean over the $D$ positions $t = 0, 1/D, \ldots, (D-1)/D$ is

$$\frac{N_0}{D} \sum_{r=0}^{D-1} \left( \left(1 - \tfrac{r}{D}\right)^2 + \left(\tfrac{r}{D}\right)^2 \right),$$

which is $0.6875\, N_0$ for $D = 4$.

*Proof.* On a flat channel the interpolant of the true values is $H$ itself, so the error is the interpolant of the noise terms $W[p] / X[p]$, which are independent $\mathcal{CN}(0, N_0)$ because $|X[p]| = 1$. The variance of a weighted sum of independent terms is the sum of the squared weights times $N_0$. For $D = 4$ the four terms are $1$, $0.625$, $0.5$ and $0.625$, whose mean is $0.6875$. $\square$

**The quadratic option (closed form).** With order 2, the estimate is the Lagrange polynomial through the pilots at $t = -1, 0, 1$, with weights $t(t - 1)/2$, $(1 - t)(1 + t)$ and $t(t + 1)/2$. It reproduces every quadratic exactly, so its error term involves $H'''$ instead of $H''$, which makes it smaller on smooth channels. Its noise factor is the mean of the squared weights, $0.81543\, N_0$ for $D = 4$, larger than for the linear estimate, because the weights sum to 1 and one of them is negative, so the other two sum to more than 1.
