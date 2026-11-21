---
title: Correctness of lambda tomography
proves: [correctness]
status: full
---

We use the conventions of the page. $\omega(\theta) = (\cos\theta, \sin\theta)$, the Radon transform is $p(\theta, s) = \mathcal{R}f(\theta, s) = \int f(s\,\omega + t\,\omega^\perp)\,dt$, the back-projection is $\mathcal{R}^\# q(x) = \int_0^\pi q(\theta, x\cdot\omega(\theta))\,d\theta$, and the Fourier transform is $\hat f(\xi) = \int f(x)e^{-2\pi i x\cdot\xi}\,dx$. The operator $\Lambda = (-\Delta)^{1/2}$ has the multiplier $2\pi|\xi|$, so $\widehat{\Lambda f}(\xi) = 2\pi|\xi|\hat f(\xi)$, and $\Lambda^{-1}$ has the multiplier $1/(2\pi|\xi|)$.

The proof has four parts. Part 1 proves the formula that the algorithm discretizes. Part 2 proves that it is local. Part 3 says what the algorithm computes in the discrete case and why the computed value at a point uses only the data near the lines through it. Part 4 proves that $\Lambda f$ has the same singular support as $f$, which is why the method shows the edges.

## Part 1. The formula

**Lemma 1 (filtered back-projection with a general filter).** Let $f \in C^\infty_c(\mathbb{R}^2)$, and let $m$ be an even continuous function on $\mathbb{R}$ with $|m(\sigma)| \le C(1 + |\sigma|)^2$. Put $q(\theta, s) = \int m(\sigma)\,\hat p_\theta(\sigma)\,e^{2\pi i s\sigma}\,d\sigma$, where $\hat p_\theta$ is the 1D transform of $p(\theta, \cdot)$. If $\int |m(|\xi|)|\,|\hat f(\xi)|\,|\xi|^{-1}\,d\xi < \infty$, then
$$\mathcal{R}^\# q(x) = \int_{\mathbb{R}^2} \frac{m(|\xi|)}{|\xi|}\,\hat f(\xi)\,e^{2\pi i x\cdot\xi}\,d\xi.$$

*Proof.* By the [Fourier slice theorem](/fourier-slice-theorem/), $\hat p_\theta(\sigma) = \hat f(\sigma\,\omega(\theta))$. So
$$\mathcal{R}^\# q(x) = \int_0^\pi \int_{\mathbb{R}} m(\sigma)\,\hat f(\sigma\omega)\,e^{2\pi i\sigma\,x\cdot\omega}\,d\sigma\,d\theta.$$
The map $(\theta, \sigma) \mapsto \xi = \sigma\omega(\theta)$ from $[0, \pi) \times \mathbb{R}$ covers the plane once up to a null set, with $d\xi = |\sigma|\,d\sigma\,d\theta$. Since $m$ is even, $m(\sigma) = m(|\xi|)$, and the integral becomes the right side. It converges absolutely by the hypothesis, so Fubini applies. $\square$

**Theorem 1.** For $f \in C^\infty_c(\mathbb{R}^2)$,
$$\Lambda f = \frac{1}{2\pi}\,\mathcal{R}^\#\left(-\partial_s^2\,\mathcal{R}f\right), \qquad \Lambda^{-1} f = \frac{1}{2\pi}\,\mathcal{R}^\#\mathcal{R}f.$$

*Proof.* The function $\hat f$ decays faster than any power. For the first formula take $m(\sigma) = 4\pi^2\sigma^2$, which is the multiplier of $-\partial_s^2$. Lemma 1 gives $\mathcal{R}^\#(-\partial_s^2 p)(x) = \int 4\pi^2|\xi|\,\hat f(\xi)\,e^{2\pi i x\cdot\xi}\,d\xi = 2\pi\,\Lambda f(x)$. For the second take $m = 1$. The integral $\int |\hat f(\xi)|\,|\xi|^{-1}\,d\xi$ converges in 2D, because $|\xi|^{-1}$ is integrable near 0 in the plane. Lemma 1 gives $\mathcal{R}^\# p(x) = \int |\xi|^{-1}\hat f(\xi)\,e^{2\pi i x\cdot\xi}\,d\xi = 2\pi\,\Lambda^{-1}f(x)$. $\square$

Compare with filtered back-projection, which uses $m(\sigma) = |\sigma|$ and gives $f$ itself. Lambda tomography uses $m(\sigma) = 4\pi^2\sigma^2/(2\pi) = 2\pi\sigma^2$, which is $|\sigma|$ times $2\pi|\sigma|$, so its output is $f$ filtered by $2\pi|\xi|$.

## Part 2. Locality

**Corollary 1.** $\Lambda f(x)$ depends only on the values of $\mathcal{R}f$ on any open set of lines that contains all lines through $x$.

*Proof.* By Theorem 1, $2\pi\Lambda f(x) = -\int_0^\pi \partial_s^2 p(\theta, s)|_{s = x\cdot\omega(\theta)}\,d\theta$. For each $\theta$, the second derivative at $s = x\cdot\omega(\theta)$ depends only on $p(\theta, \cdot)$ in a neighborhood of $x\cdot\omega(\theta)$, and the line $(\theta, x\cdot\omega(\theta))$ passes through $x$. $\square$

So if the data is known only for the lines that meet a disk $B$, then $\Lambda f$ is known on the open disk $B$. In particular, truncated projections give $\Lambda f$ exactly inside the region of interest, while $f$ itself is not determined there ([interior tomography](/interior-tomography/)). The operator $\Lambda^{-1}$ is not local: $\mathcal{R}^\# p(x)$ uses $p$ on the lines through $x$, but these lines leave the region of interest.

## Part 3. The discrete algorithm

Line L2 replaces $-\partial_s^2 p$ by the central second difference
$$q_j = -\frac{p_{j+1} - 2p_j + p_{j-1}}{\tau^2} + \mu\,p_j,$$
with $p_{-1} = p_d = 0$. For $p \in C^4$ Taylor expansion gives $-(p(s + \tau) - 2p(s) + p(s - \tau))/\tau^2 = -p''(s) - \tau^2 p''''(\xi)/12$ for some $\xi$, so the error is at most $\tau^2\max|p''''|/12$. Line L4 reads $q$ at $x\cdot\omega(\theta_k)$ by linear interpolation, with the error at most $\tau^2\max|q''|/8$ for a smooth $q$, and line L5 replaces $\frac{1}{2\pi}\int_0^\pi\,d\theta$ by $\frac{1}{2\pi}\cdot\frac{\pi}{a}\sum_k = \frac{1}{2a}\sum_k$. The integrand has the period $\pi$ in $\theta$, so this is the trapezoidal rule for a periodic function, which converges faster than any power of $1/a$ for smooth $f$. With $\mu = 0$ the output is therefore $\Lambda f(x) + O(\tau^2) + O(a^{-k})$ for every $k$ and smooth $f$. With $\mu \ne 0$ it is $\Lambda f + \mu\Lambda^{-1}f$ up to the same errors, by the second formula of Theorem 1.

The discrete method is local in the same way as the continuous formula. The value at $x$ uses, for each $k$, two interpolation nodes $b$ and $b + 1$ around the fractional index $u = x\cdot\omega(\theta_k)/\tau + (d-1)/2$, and $q_b$ and $q_{b+1}$ use $p_{b-1}, \ldots, p_{b+2}$. All of these bins have centers within $2\tau$ of $x\cdot\omega(\theta_k)$. So with $\mu = 0$ the output at $x$ does not change when the data changes only at bins with $|s_j - x\cdot\omega(\theta_k)| > 2\tau$ in row $k$. The test checks this with random changes outside $|s| \le |x| + 2\tau$, which is a smaller set since $|x\cdot\omega| \le |x|$.

## Part 4. Edges

**Theorem 2.** For a distribution $f$ with compact support, $\Lambda f$ and $f$ have the same singular support, that is, $\Lambda f$ is smooth near a point if and only if $f$ is.

*Proof sketch with the standard tools.* $\Lambda$ is a classical pseudodifferential operator of order 1 with the principal symbol $2\pi|\xi|$, after a smooth cutoff of the symbol near $\xi = 0$, which changes $\Lambda f$ only by a smooth function. Every pseudodifferential operator is pseudolocal, so the singular support of $\Lambda f$ lies in that of $f$. The symbol $2\pi|\xi|$ does not vanish for $\xi \ne 0$, so $\Lambda$ is elliptic and has a parametrix $Q$ of order $-1$ with $Q\Lambda f - f$ smooth. Pseudolocality of $Q$ gives the other inclusion. $\square$

This is the theorem that justifies the method: the jumps of $f$ show up in $\Lambda f$ at the same places. The values are not the same. $\Lambda$ multiplies the Fourier transform by $2\pi|\xi|$, so it removes the mean and changes the size of each feature. At a jump of a piecewise smooth $f$, $\Lambda f$ is not bounded: for the disk of radius $R$ it grows like $1/(R - |x|)$ near the edge from inside. The page computes this case in closed form.
