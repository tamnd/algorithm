---
title: What spectral subtraction preserves, what it estimates without bias, and the noise it leaves
proves: [correctness]
status: full
---

Spectral subtraction is a heuristic: it does not minimize a stated error. Its correctness consists of three facts, which this page proves. The framing loses nothing; the subtraction estimates the signal power in each bin without bias; and on noise alone, the output power and the fraction of bins that survive are given by a closed formula. We work in exact real arithmetic, as in the real RAM.

**Setting.** The frame length is an even $L$, the hop is $H = L/2$, and $w[n] = \frac12 - \frac12 \cos(2\pi n / L)$ for $0 \le n < L$ is the periodic Hann window. The implementation pads $y$ with $H$ zeros in front, and at the end with enough zeros to make the length of $y$ a multiple of $H$ and then $H$ more. Frame $j$ covers the padded indices $jH, \ldots, jH + L - 1$.

**Lemma 1 (the window adds up to one).** $w[n] + w[n + H] = 1$ for $0 \le n < H$.

*Proof.* $\cos(2\pi (n + H)/L) = \cos(2\pi n / L + \pi) = -\cos(2\pi n/L)$, so the sum is $\frac12 + \frac12 = 1$. $\square$

**Theorem 1 (perfect reconstruction).** If lines L6 to L8 leave every DFT coefficient unchanged, which is the case for $\alpha = 0$ when $\beta N̂[m] \le |Y[m]|^\gamma$ in every bin of every frame, and in particular for $\alpha = \beta = 0$, then the output equals $y$.

*Proof.* With unchanged coefficients, line L9 adds the inverse DFT of the DFT of $w \cdot (\text{frame } j)$, which is $w[n]\, y_p[jH + n]$, to position $jH + n$. So the output at padded index $i$ is $y_p[i] \sum_j w[i - jH]$, summed over the frames with $0 \le i - jH < L$. For an index $i$ of the original signal, $H \le i < H + |y|$, these are the two frames $j = \lfloor i/H \rfloor - 1$ and $j = \lfloor i/H \rfloor$; the second exists because the end padding makes the number of frames $\lceil |y|/H \rceil + 1$. Their offsets are $n + H$ and $n$ with $n = i \bmod H$, so the sum of the weights is $w[n] + w[n + H] = 1$ by Lemma 1. For $\alpha = 0$ the rule of line L7 is $P = \max(|Y|^\gamma, \beta N̂) = |Y|^\gamma$ under the stated condition, and line L8 gives $|Y| \cdot Y/|Y| = Y$, or $0 = Y$ when $Y = 0$. $\square$

**Theorem 2 (unbiased power).** In one bin, let $Y = X + V$ with $X$ fixed and $V$ a random variable with $E[V] = 0$ and $E|V|^2 = N$. Then $E[|Y|^2 - N] = |X|^2$. So for $\gamma = 2$, $\alpha = 1$ and an exact noise estimate $N̂ = N$, the subtraction in line L7, before the maximum, is an unbiased estimate of the signal power.

*Proof.* $|Y|^2 = |X|^2 + 2\,\mathrm{Re}(\bar X V) + |V|^2$, and $E[\mathrm{Re}(\bar X V)] = \mathrm{Re}(\bar X\, E[V]) = 0$. $\square$

The maximum with $\beta N̂$ in line L7 makes the estimate biased upward, because it replaces negative values, and this is the price for a valid power.

**Theorem 3 (the noise left on noise alone).** Let $\gamma = 2$ and let $Y$ be a circular complex Gaussian with $E|Y|^2 = \sigma^2$, and $N̂ = \sigma^2$. For $\alpha \ge 0$ and $\beta \ge 0$, the output $\hat X$ of lines L7 and L8 satisfies

$$\Pr\big[|\hat X|^2 > \beta \sigma^2\big] = e^{-(\alpha + \beta)}, \qquad E|\hat X|^2 = \sigma^2 \big(\beta + e^{-(\alpha + \beta)}\big).$$

*Proof.* For a circular complex Gaussian, $E = |Y|^2/\sigma^2$ has the density $e^{-e}$ on $e \ge 0$, the exponential law with mean one, because the real and imaginary parts are independent $\mathcal N(0, \sigma^2/2)$ and $|Y|^2$ is $\sigma^2/2$ times a chi-square variable with two degrees of freedom. Line L7 gives $|\hat X|^2 = \sigma^2 \max(E - \alpha, \beta)$, which is above $\beta\sigma^2$ exactly when $E > c$ with $c = \alpha + \beta$, an event of probability $e^{-c}$. For the mean,

$$E[\max(E - \alpha, \beta)] = \beta \Pr[E \le c] + \int_c^\infty (e - \alpha)\, e^{-e}\, de = \beta (1 - e^{-c}) + (c + 1 - \alpha)\, e^{-c} = \beta + e^{-c},$$

using $\int_c^\infty e\, e^{-e}\, de = (c + 1) e^{-c}$ and $c + 1 - \alpha = \beta + 1$. $\blacksquare$

**Remarks.** In a frame of noise alone, each bin survives with probability $e^{-(\alpha + \beta)}$, about $37\%$ for $\alpha = 1$ and $\beta = 0$, and in the next frame a different random set survives. These short tones at random places are the musical noise. For white Gaussian noise $v$ with variance $\sigma_v^2$, the bin $m$ of the windowed frame has $E[Y^2] = \sigma_v^2 \sum_n w[n]^2 e^{-4\pi i m n / L}$. The square $w^2$ has Fourier components only at the frequencies $0, \pm 1, \pm 2$, so this is zero, and $Y$ is circular, for every bin except $m \in \{0, 1, L/2 - 1, L/2, L/2 + 1, L - 1\}$. Theorem 3 is exact for the other bins and approximate for these six. Bins next to each other are correlated by the window, so the survivors are not independent across bins. Overlap-add mixes two frames, so the output power per sample of the full method on white noise is near the per-bin value but not equal to it. The tests check the per-bin formula to two decimals and the full method to the right order.
