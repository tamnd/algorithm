---
title: The search curve has uniform marginals, the spectrum splits the variance, and eFAST is exact for band-limited models
proves: [correctness]
status: full
---

We assume exact arithmetic. The inputs are independent and uniform on $[0, 1]$; other laws are reached by a map of each component. For input $i$, the algorithm uses the frequency $\omega_i = \omega_{\max}$ for $x_i$ and integer frequencies $\omega_k \le \omega_{\max}/(2M)$ for the other inputs, random phases $\varphi_k$, and the curve

$$x_k(s) = \frac{1}{2} + \frac{1}{\pi} \arcsin\big(\sin(\omega_k s + \varphi_k)\big), \qquad k = 1, \ldots, d.$$

It evaluates $y(s) = f(x(s))$ at the $n$ points $s_j = \pi(2j - n - 1)/n$, $j = 1, \ldots, n$, with $n$ odd and $n \ge 2M\omega_{\max} + 1$. The power at the frequency $p$ is $\Lambda_p = (A_p^2 + B_p^2)/2$ with $A_p = \frac{2}{n}\sum_j y(s_j) \cos(p s_j)$ and $B_p = \frac{2}{n}\sum_j y(s_j) \sin(p s_j)$. With $H = (n - 1)/2$, line L7 sets $\widehat{D} = \sum_{p=1}^{H} \Lambda_p$, line L8 sets $\widehat{D}_i = \sum_{q=1}^{M} \Lambda_{q \omega_{\max}}$, and line L9 sets $\widehat{D}_{\sim i} = \sum_{p=1}^{\omega_{\max}/2} \Lambda_p$. The estimates are $\widehat{S}_i = \widehat{D}_i / \widehat{D}$ and $\widehat{S}_{Ti} = 1 - \widehat{D}_{\sim i} / \widehat{D}$.

**Lemma 1 (uniform marginals).** If $s$ is uniform on $(-\pi, \pi)$, each $x_k(s)$ is uniform on $[0, 1]$, for every integer $\omega_k \ge 1$ and every phase.

*Proof.* The angle $\theta = \omega_k s + \varphi_k$ modulo $2\pi$ is uniform on one period, because $\omega_k s$ covers $\omega_k$ full periods at constant speed. The map $t(\theta) = \arcsin(\sin \theta)$ is the triangle wave: $t = \theta$ on $[-\pi/2, \pi/2]$ and $t = \pi - \theta$ on $[\pi/2, 3\pi/2]$. On each half period it is a bijection onto $[-\pi/2, \pi/2]$ with slope $\pm 1$, so $t$ is uniform on $[-\pi/2, \pi/2]$, and $x_k = 1/2 + t/\pi$ is uniform on $[0, 1]$. $\square$

**Lemma 2 (discrete Parseval).** For odd $n$, $\widehat{D}$ is the population variance $\frac{1}{n}\sum_j (y(s_j) - \bar{y})^2$ of the $n$ values.

*Proof.* With $s_j = -\pi + \pi(2j - 1)/n$, $\sum_{j=1}^{n} e^{\mathrm{i} p s_j} = e^{-\mathrm{i}\pi p (1 - 1/n)} \sum_{j=0}^{n-1} e^{2\pi \mathrm{i} p j / n}$, which is zero unless $p$ is a multiple of $n$. For $p, q \in \{0, \ldots, H\}$, the numbers $p \pm q$ are multiples of $n$ only when $p = q$ (or $p = q = 0$), so the $n$ functions $1, \cos(p s), \sin(p s)$, $1 \le p \le H$, are orthogonal on the points, with the squared norms $n, n/2, n/2$. They are $n$ orthogonal vectors in $\mathbb{R}^n$, so they are a basis, and $y(s_j) = \bar{y} + \sum_{p=1}^{H} (A_p \cos p s_j + B_p \sin p s_j)$. Then $\frac{1}{n}\sum_j (y_j - \bar{y})^2 = \sum_p (A_p^2 + B_p^2)/2$. $\square$

So line L7 needs no second pass over the data, and the [Parseval theorem](/parseval-theorem/) of the [discrete Fourier transform](/discrete-fourier-transform/) is the reason why the spectrum splits the variance.

**Lemma 3 (cosine inputs are pure harmonics).** For an integer $m \ge 1$, $\cos(2\pi m\, x_k(s)) = (-1)^m \cos\big(2m(\omega_k s + \varphi_k)\big)$.

*Proof.* With $x_k = 1/2 + t/\pi$, $2\pi m x_k = \pi m + 2m t$, so $\cos(2\pi m x_k) = (-1)^m \cos(2mt)$. On the half period where $t = \theta$ this is $(-1)^m \cos(2m\theta)$. On the other one $t = \pi - \theta$ and $\cos(2m\pi - 2m\theta) = \cos(2m\theta)$. $\square$

**Lemma 4 (the main effect along the curve).** Let $f_i(x_i) = \mathbb{E}[f \mid x_i] - \mathbb{E}[f]$ be the first order term of the [Hoeffding-Sobol decomposition](/hoeffding-sobol-decomposition/). Along the curve, $f_i(x_i(s))$ is a function of $\omega_{\max} s$ alone, so its Fourier series has only the frequencies $q\omega_{\max}$, and, for $s$ uniform on $(-\pi, \pi)$, its total power is $V_i = \mathrm{Var}(f_i)$.

*Proof.* $x_i(s)$ depends on $s$ only through $\omega_{\max} s$, so $f_i(x_i(s))$ has the period $2\pi/\omega_{\max}$, and a function with this period has Fourier modes only at multiples of $\omega_{\max}$. By Lemma 1, the mean square of $f_i(x_i(s))$ over $s$ is $\mathbb{E}[f_i(x_i)^2] = V_i$, and its mean is zero. The total power is the mean square, by the Parseval theorem for Fourier series. $\square$

**Theorem (exact for band-limited models).** Let $M$ be even and

$$f(x) = c_0 + \sum_{k=1}^{d} \sum_{m=1}^{M/2} a_{k, m} \cos(2\pi m x_k).$$

Assume that the numbers $2m\omega_k$, $k \ne i$, $1 \le m \le M/2$, are distinct. Then $\widehat{S}_i = \widehat{S}_{Ti} = S_i = S_{Ti}$ exactly, for every choice of phases.

*Proof.* By Lemma 3, along the curve $y(s) = c_0 + \sum_k \sum_m (-1)^m a_{k, m} \cos(2m\omega_k s + 2m\varphi_k)$. The terms of input $i$ sit at the frequencies $2m\omega_{\max}$, $2m \le M$, which are among the harmonics $q\omega_{\max}$, $q \le M$, of line L8. The terms of the other inputs sit at $2m\omega_k \le M \omega_{\max}/(2M) = \omega_{\max}/2$, so they are inside the band of line L9 and below $\omega_{\max}$. All the frequencies are at most $M\omega_{\max} \le H$. By the distinctness assumption and Lemma 2, each term contributes exactly its own power $a_{k, m}^2/2$ to one $\Lambda_p$. So $\widehat{D}_i = \sum_m a_{i, m}^2/2$, $\widehat{D}_{\sim i} = \sum_{k \ne i}\sum_m a_{k, m}^2/2$ and $\widehat{D} = \widehat{D}_i + \widehat{D}_{\sim i}$. By Lemma 1 and the orthogonality of $\cos(2\pi m x)$ on $[0, 1]$, these are the exact variance $V_i$ of the terms of input $i$, the exact variance of the other terms and the exact total variance. The model is additive, so $S_i = S_{Ti} = V_i / D$, and the estimates are equal to it. $\blacksquare$

**The general case.** For a model that is not band-limited, three errors appear, and none of them goes to zero as the number $n_r$ of random phases grows.

- **Truncation.** Lemma 4 puts all of $V_i$ at the harmonics $q\omega_{\max}$, but line L8 keeps only $q \le M$. The power at $q > M$ is lost from $\widehat{D}_i$ and aliases into other frequencies. For a smooth $f_i$ the lost part decays fast in $M$.
- **Interference.** The harmonics of the low frequencies of the other inputs, and their sums and differences, can land on a frequency $q\omega_{\max}$ and change $\widehat{D}_i$ in either direction. With the cut $\omega_k \le \omega_{\max}/(2M)$, the first $M$ harmonics of each other input stay below $\omega_{\max}/2$; higher harmonics and combinations of several inputs can still reach $\omega_{\max}$.
- **The band of the other inputs.** Line L9 assumes that all power of the terms without $x_i$ is at frequencies up to $\omega_{\max}/2$ and that all terms with $x_i$ are above it. A term with $x_i$ has frequencies $q\omega_{\max} \pm (\text{combinations of the } \omega_k)$, which are above $\omega_{\max}/2$ if the combinations are small. Power of the other inputs above $\omega_{\max}/2$ counts as part of the total effect of $x_i$, so $\widehat{S}_{Ti}$ tends to be too large in that case.

The random phases average the interference over different curves. They do not remove the band errors, which come from the frequencies themselves. So eFAST is a consistent method only in the band-limited sense of the theorem. For a general model it has a bias that depends on $\omega_{\max}$, $M$ and the frequency choice, and it gives no error bar.

**What is not proved.** The code places the low frequencies evenly in $1, \ldots, \lfloor \omega_{\max}/(2M) \rfloor$. This choice is a heuristic, as is the choice $M = 4$. If two other inputs get the same frequency, which happens when there are more than $\omega_{\max}/(2M)$ of them, their terms share a frequency and add with phases that depend on the curve, so the variance along one curve can differ from $D$, and both estimates of input $i$ change with it.
