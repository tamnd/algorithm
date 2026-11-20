---
title: The coherence factor lies in [0, 1], is 1 only for equal samples, has mean 1/M for independent noise, and is near 2/3 for the triangular coherence of speckle
proves: [correctness]
status: full
---

We prove the facts behind the definition and lines L1 to L5 of the main page. The input is a complex vector $s = (s_1, \ldots, s_M)$ of delayed channel samples at one pixel, and

$$\operatorname{CF}(s) = \frac{|\sum_i s_i|^2}{M \sum_i |s_i|^2}$$

for $s \ne 0$, with $\operatorname{CF}(0) = 0$ by convention (line L3).

**Theorem 1 (range).** For $s \ne 0$, $0 \le \operatorname{CF}(s) \le 1$. The value is $1$ if and only if all $s_i$ are equal, and $0$ if and only if $\sum_i s_i = 0$.

*Proof.* The numerator and the denominator are nonnegative and the denominator is positive. By the Cauchy-Schwarz inequality, $|\sum_i 1 \cdot s_i|^2 \le (\sum_i 1)(\sum_i |s_i|^2) = M \sum_i |s_i|^2$, with equality if and only if $s$ is a multiple of $(1, \ldots, 1)$. The numerator is $0$ exactly when the sum is $0$. $\square$

**Theorem 2 (mean and spread).** Let $\bar s = \frac1M \sum_i s_i$ and $v = \frac1M \sum_i |s_i - \bar s|^2$. Then for $s \ne 0$

$$\operatorname{CF}(s) = \frac{|\bar s|^2}{|\bar s|^2 + v}.$$

*Proof.* $\frac1M \sum_i |s_i|^2 = |\bar s|^2 + v$, the usual split of the mean square into the square of the mean and the variance. Divide the numerator and the denominator of CF by $M^2$. $\square$

So CF is the fraction of the channel energy that lies in the mean, the part that delay-and-sum keeps. A spread of the samples around their mean, from clutter, noise or a focusing error, lowers it.

**Theorem 3 (scale invariance).** For every complex $a \ne 0$, $\operatorname{CF}(a s) = \operatorname{CF}(s)$.

*Proof.* The numerator and the denominator are both multiplied by $|a|^2$. $\square$

So CF does not depend on the echo strength, only on how well the channels agree, and the weighted output $\operatorname{CF}^p \sum_i s_i$ of line L5 is homogeneous of degree one in $s$.

**Theorem 4 (independent noise).** Let $s_1, \ldots, s_M$ be independent circular complex Gaussian variables with mean $0$ and the same variance. Then $\mathbb{E}[\operatorname{CF}(s)] = 1/M$.

*Proof.* Let $e = (1, \ldots, 1)/\sqrt{M}$, so $\operatorname{CF}(s) = |e^H s|^2 / \|s\|^2$, and $s \ne 0$ with probability one. Choose a unitary matrix $U$ with $U e = e_1$, the first unit vector. Then $e^H s = e_1^H U s$ and $\|s\| = \|U s\|$, and $U s$ has the same distribution as $s$, because the distribution of $s$ is invariant under unitary maps. So $\mathbb{E}[\operatorname{CF}(s)] = \mathbb{E}[|s_1|^2 / \|s\|^2]$. The entries are exchangeable, so this expectation is the same for every index, and the $M$ expectations add to $\mathbb{E}[\|s\|^2/\|s\|^2] = 1$. $\square$

The test measures a mean of $1/8$ within $0.01$ for $M = 8$ and 3000 trials. Independent channels are a model of electronic noise; clutter and speckle are correlated across the aperture.

**Theorem 5 (triangular coherence).** Let the samples have mean $0$ and the correlation $\mathbb{E}[s_i \bar s_j] = \sigma^2 (1 - |i - j|/M)$ with $\sigma^2 > 0$. Then

$$\frac{\mathbb{E}\,|\sum_i s_i|^2}{M\, \mathbb{E} \sum_i |s_i|^2} = \frac{2 M^2 + 1}{3 M^2},$$

which tends to $2/3$ as $M$ grows.

*Proof.* The denominator is $M \cdot M \sigma^2$. The numerator is $\sigma^2 \sum_{i,j} (1 - |i - j|/M)$. There are $M$ pairs with $i = j$ and $2(M - d)$ pairs at distance $d \ge 1$, so the sum is $M^2 - \frac{2}{M} \sum_{d=1}^{M-1} d (M - d)$. Since $\sum_{d=1}^{M-1} d(M - d) = \frac{M(M^2 - 1)}{6}$, the sum is $M^2 - \frac{M^2 - 1}{3} = \frac{2M^2 + 1}{3}$. Divide by $M^2$. $\square$

This is a ratio of expectations, not the expectation of CF. The triangular correlation is what the pulse-echo form of the van Cittert-Zernike theorem predicts for fully developed speckle from a uniform transmit aperture of the same width as the receive aperture, at the focus (Mallart and Fink 1994). Under that model, speckle has a coherence near $2/3$, between the $1/M$ of noise and the $1$ of a point target. The test checks the closed form directly for several $M$ and by a simulation with moving sums of independent samples, which have exactly this correlation, within $0.03$ for $M = 8$.

**Theorem 6 (cost).** Lines L1 to L5 cost $O(M)$ per pixel.

*Proof.* Each line is one pass over the samples or $O(1)$ work. $\square$
