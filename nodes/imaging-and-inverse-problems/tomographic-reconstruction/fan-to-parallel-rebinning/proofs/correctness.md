---
title: Correctness of fan-to-parallel rebinning
proves: [correctness]
status: full
---

We use the conventions of the page. $\omega(\theta) = (\cos\theta, \sin\theta)$ and $\omega^\perp(\theta) = (-\sin\theta, \cos\theta)$. The Radon transform is $p(\theta, s) = \mathcal{R}f(\theta, s) = \int f(s\,\omega + t\,\omega^\perp)\,dt$ for all real $\theta$, so $p(\theta + \pi, -s) = p(\theta, s)$ and $p$ has the period $2\pi$ in $\theta$. The source at the angle $\beta$ is $S(\beta) = D\,\omega^\perp(\beta)$, and the fan data is $g(\beta, \gamma) = p(\beta + \gamma, D\sin\gamma)$ for $|\gamma| < \pi/2$.

The proof has three parts. Part 1 shows that the map of line L6 finds a fan ray that is the wanted parallel ray, so with exact interpolation the rebinned sinogram is exact. Part 2 bounds the error of the bilinear interpolation of line L8 and proves that it is exact on data that is linear in the fan angle and does not depend on the source angle. Part 3 joins the result with the correctness of parallel-beam filtered back-projection.

## Part 1. The rebinning map

**Lemma 1.** Let $|s| < D$ and $\theta \in \mathbb{R}$. Put $\gamma = \arcsin(s/D)$ and $\beta = \theta - \gamma$, reduced modulo $2\pi$. Then $g(\beta, \gamma) = p(\theta, s)$. The pair $(\beta, \gamma)$ with $\beta \in [0, 2\pi)$ and $|\gamma| < \pi/2$ is the only fan ray that is the oriented line $(\theta, s)$. The fan ray $(\beta + \pi + 2\gamma, -\gamma)$ is the same line with the other orientation, $(\theta + \pi, -s)$.

*Proof.* By definition $g(\beta, \gamma) = p(\beta + \gamma, D\sin\gamma) = p(\theta - 2\pi m, s)$ for some integer $m$, and $p$ has the period $2\pi$ in $\theta$. For uniqueness, $D\sin\gamma = s$ has the single solution $\gamma = \arcsin(s/D)$ in $(-\pi/2, \pi/2)$, and then $\beta \equiv \theta - \gamma$ modulo $2\pi$. For the last claim, $(\beta + \pi + 2\gamma) + (-\gamma) = \theta + \pi$ and $D\sin(-\gamma) = -s$. $\square$

This is what lines L5 to L7 compute. For a flat detector the column of the ray is $t = D\tan\gamma$ in place of $\gamma$, and the lemma is the same. With `average=True` the code takes the mean of the two copies $(\theta, s)$ and $(\theta + \pi, -s)$. By the lemma both copies equal $p(\theta, s)$ for exact data, so the mean changes nothing for exact data and halves the variance of independent noise in the two readings.

If the fan covers the support of $f$, that is, $f$ is zero outside the disk of radius $r$ with $r \le D\sin\gamma_{\max}$ where $\gamma_{\max} = (d-1)\alpha/2$, then every parallel sample with $|s| > r$ is 0, and the samples with $|s| \le r$ map to fan angles inside the detector.

## Part 2. Bilinear interpolation

Line L8 reads the fan data $g[k][j] = g(\beta_k, \gamma_j)$ at the fractional indices $u = \beta/\Delta\beta$ and $v = \gamma/\alpha + (d-1)/2$, where $\Delta\beta = 2\pi/a$. The rows are periodic: row $a$ is row 0. This matches the period $2\pi$ of $g$ in $\beta$.

**Lemma 2 (exact cases).** If $g(\beta, \gamma) = c + e\gamma$ for constants $c$ and $e$, then line L8 returns $c + e\gamma$ at each point with $0 \le v \le d - 1$.

*Proof.* The value does not depend on $k$, and the two row weights $1 - w_u$ and $w_u$ add to 1, so the result is the linear interpolation in $j$. Linear interpolation between $c + e\gamma_{j_0}$ and $c + e\gamma_{j_0 + 1}$ at the fraction $w_v$ gives $c + e(\gamma_{j_0} + w_v\alpha) = c + e\gamma$. $\square$

So for such data the rebinned value at $(\theta, s)$ is exactly $c + e\arcsin(s/D)$, which the test checks.

**Lemma 3 (error bound).** Let $g$ be $C^2$ on the cell $[\beta_k, \beta_{k+1}] \times [\gamma_j, \gamma_{j+1}]$, with $|\partial_\beta^2 g| \le M_1$ and $|\partial_\gamma^2 g| \le M_2$ there. Then at each point of the cell the bilinear interpolant $I g$ satisfies
$$|g - I g| \le \frac{\Delta\beta^2}{8}M_1 + \frac{\alpha^2}{8}M_2.$$

*Proof.* Let $I_\beta$ be linear interpolation in $\beta$ at a fixed $\gamma$, and $I_\gamma$ linear interpolation in $\gamma$ at a fixed $\beta$. Then $I = I_\gamma I_\beta$ and $g - Ig = (g - I_\gamma g) + I_\gamma(g - I_\beta g)$. The 1D error of linear interpolation on an interval of length $\ell$ is at most $\ell^2\max|q''|/8$, since $q - Iq$ vanishes at both ends and equals $-\frac{1}{2}q''(\xi)(x - x_0)(x_1 - x)$ for some $\xi$, and $(x - x_0)(x_1 - x) \le \ell^2/4$. So $|g - I_\gamma g| \le \alpha^2 M_2/8$. The function $g - I_\beta g$ is at most $\Delta\beta^2 M_1/8$ at both nodes in $\gamma$, and $I_\gamma$ is a convex combination of these node values. $\square$

For a smooth $f$ the fan data is smooth, and the rebinned sinogram has the error $O(\Delta\beta^2 + \alpha^2)$. At the edge of an object of constant density, $p$ has a square-root singularity in $s$, the second derivative is not bounded, and the bound does not hold. The measured errors at such edges on the page are much larger than in the smooth case.

## Part 3. The reconstruction

Let $P$ be the rebinned sinogram and $P^\star$ the exact parallel sinogram on the same grid. Parallel-beam FBP is linear, so its output on $P$ is its output on $P^\star$ plus its output on $P - P^\star$. The first term is analyzed on the page [filtered back-projection](/filtered-back-projection/), whose proof shows that the method is exact for band-limited data up to the angular quadrature and the linear interpolation of the back-projection. The second term is bounded by the norm of the discrete FBP operator times $\max|P - P^\star|$. The discrete operator is a fixed linear map. Its norm in the maximum norm is at most $(\pi/a_p)\,a_p\,\tau\sum_m |h(m\tau)| \le \pi\,\tau\,(1/(4\tau^2) + 2\sum_{m \text{ odd}} 1/(m^2\pi^2\tau^2)) = \pi/(2\tau)$, using $\sum_{m \ge 1,\ m \text{ odd}} 1/m^2 = \pi^2/8$. So the error that the interpolation adds to the image is at most $\pi/(2\tau)$ times the largest rebinning error. The bound grows as the detector spacing shrinks, which is the usual amplification of data errors by the ramp filter.

With the values of the test, $\tau = 2\sqrt{2}/47 = 0.0602$ and the largest rebinning error on the smooth blob is $0.0030$, so the bound is $0.079$. In the measurement on the page, the largest image error grows from $0.0153$ for exact parallel data to $0.0243$ after rebinning, a change of $0.009$, well below the bound.
