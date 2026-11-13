---
tag: 08BW0E
kind: definition
slug: haar-wavelet
name: Haar wavelet
aliases:
- Haar basis
area: graphics-and-signals/signal-processing
level: core
summary: Simplest wavelet, a square pulse pair; basis of the first wavelet transform.
prereqs: [orthogonal-transform]
see_also: [haar-wavelet-transform, discrete-wavelet-transform, continuous-wavelet-transform, fast-wavelet-transform, walsh-hadamard-transform, haar-features, lifting-scheme, filter-bank]
sources:
  - paper: doi:10.1007/BF01456326
    title: Alfred Haar, Zur Theorie der orthogonalen Funktionensysteme, Mathematische Annalen 69(3), 1910
    locator: pages 331 to 371 (the orthogonal system of step functions on [0, 1] and the uniform convergence of its expansions of continuous functions)
  - book: isbn:9780898712742
    title: Ingrid Daubechies, Ten Lectures on Wavelets, SIAM, 1992
    locator: Chapter 5 (orthonormal wavelet bases from nested approximation spaces) and Chapter 8 (symmetry of compactly supported orthonormal wavelets)
  - book: isbn:9780123743701
    title: Stéphane Mallat, A Wavelet Tour of Signal Processing, The Sparse Way, third edition, Academic Press, 2009
    locator: Chapter 7 (orthogonal wavelet bases, with the Haar wavelet as the first example)
---

The Haar wavelet is the function $\psi$ on $\mathbb R$ that is $1$ on $[0, \tfrac12)$, $-1$ on $[\tfrac12, 1)$ and $0$ elsewhere. Its scaled and shifted copies $\psi_{j,k}(t) = 2^{j/2} \psi(2^j t - k)$ form an orthonormal basis of $L^2(\mathbb R)$, and together with the box function they give the Haar basis of $L^2[0,1]$, which Haar defined in 1910. It is the simplest wavelet, and the only real, compactly supported orthonormal wavelet with an axis of symmetry. This page is about the function and the basis on the real line; the transform of a finite vector by pairwise averages and differences is the [Haar wavelet transform](/haar-wavelet-transform/).

## Definition

**Scaling function and wavelet.** Let $\varphi(t) = 1$ for $0 \le t < 1$ and $\varphi(t) = 0$ otherwise. The Haar wavelet is

$$\psi(t) = \varphi(2t) - \varphi(2t - 1) = \begin{cases} 1, & 0 \le t < \tfrac12, \\ -1, & \tfrac12 \le t < 1, \\ 0, & \text{otherwise.} \end{cases}$$

The box function also satisfies $\varphi(t) = \varphi(2t) + \varphi(2t - 1)$. These two-scale relations say that $\varphi = \sqrt 2 \sum_l h_l \varphi(2 \cdot {} - l)$ and $\psi = \sqrt 2 \sum_l g_l \varphi(2 \cdot {} - l)$ with the filters $h = (\tfrac{1}{\sqrt 2}, \tfrac{1}{\sqrt 2})$ and $g = (\tfrac{1}{\sqrt 2}, -\tfrac{1}{\sqrt 2})$. These are the filters that the [discrete wavelet transform](/discrete-wavelet-transform/) uses for the Haar case.

**The family.** For integers $j$ (the scale) and $k$ (the position), let $\psi_{j,k}(t) = 2^{j/2}\psi(2^j t - k)$. It is supported on the dyadic interval $I_{j,k} = [k 2^{-j}, (k+1) 2^{-j})$, it is $+2^{j/2}$ on the left half of $I_{j,k}$ and $-2^{j/2}$ on the right half, and the factor $2^{j/2}$ gives it norm 1.

**Theorem (orthonormal basis).** (a) The functions $\varphi$ and $\psi_{j,k}$ for $j \ge 0$ and $0 \le k < 2^j$ form an orthonormal basis of $L^2[0,1]$. (b) The functions $\psi_{j,k}$ for all $j, k \in \mathbb Z$ form an orthonormal basis of $L^2(\mathbb R)$.

*Proof of (a).* Take two different pairs $(j,k)$ and $(j',k')$ with $j \le j'$. If $j = j'$, the supports are disjoint. If $j < j'$, the interval $I_{j',k'}$ has length at most half the length of $I_{j,k}$, so it lies inside one half of $I_{j,k}$ or outside $I_{j,k}$. On it $\psi_{j,k}$ is constant, and $\int \psi_{j',k'} = 0$, so the inner product is $0$. The same argument with $\int \psi_{j,k} = 0$ shows that $\varphi$ is orthogonal to each $\psi_{j,k}$. So the system is orthonormal. For completeness, fix $J \ge 0$. The $2^J$ functions $\varphi$ and $\psi_{j,k}$ with $j < J$ are orthonormal, and they lie in the space $V_J$ of functions that are constant on each interval $[m 2^{-J}, (m+1)2^{-J})$, which has dimension $2^J$. So they span $V_J$. The union of the spaces $V_J$ holds all dyadic step functions, which are dense in $L^2[0,1]$. $\square$

Part (b) uses the same orthogonality argument. Its completeness needs two more facts: the dyadic step functions are dense in $L^2(\mathbb R)$, and the projection of $f$ onto the step functions on the intervals $[m 2^J, (m+1) 2^J)$ tends to $0$ in norm as $J \to \infty$. Daubechies (1992, Chapter 5) proves both in the general setting of nested approximation spaces.

**Partial sums.** The part of the expansion of $f$ with levels $j < J$ (and $\varphi$) is the orthogonal projection onto $V_J$. It replaces $f$ on each interval $[m2^{-J}, (m+1)2^{-J})$ by its average there. If $f$ is continuous on $[0,1]$, it is uniformly continuous, so these averages converge to $f$ uniformly as $J \to \infty$. This is the property that Haar's 1910 paper set out to give: the trigonometric system does not have it, because some continuous functions have a Fourier series that diverges at a point.

**Fourier transform.** With $\hat f(\omega) = \int f(t) e^{-i\omega t}\, dt$ and $\omega$ in radians per unit time,

$$\hat\psi(\omega) = \frac{(1 - e^{-i\omega/2})^2}{i\omega}, \qquad |\hat\psi(\omega)| = \frac{4 \sin^2(\omega/4)}{|\omega|}.$$

The first form comes from integrating $e^{-i\omega t}$ over the two halves, and $|1 - e^{-i\omega/2}| = 2|\sin(\omega/4)|$ gives the second. So $\hat\psi(0) = 0$, and $|\hat\psi|$ decays only like $1/|\omega|$, because $\psi$ has jumps.

**Moments and admissibility.** $\int \psi = 0$ and $\int t\,\psi(t)\,dt = \tfrac18 - \tfrac38 = -\tfrac14$, so $\psi$ has exactly one vanishing moment. The admissibility constant of the [continuous wavelet transform](/continuous-wavelet-transform/) is finite:

$$C_\psi = \int_{-\infty}^{\infty} \frac{|\hat\psi(\omega)|^2}{|\omega|}\, d\omega = 2 \int_0^\infty \frac{\sin^4 u}{u^3}\, du = 2 \ln 2.$$

The middle form follows from the substitution $\omega = 4u$. For the last step, write $8\sin^4 u = F(u) = 3 - 4\cos 2u + \cos 4u$. Then $F(u) = O(u^4)$ and $F'(u) = O(u^3)$ near $0$, so two integrations by parts have no boundary terms and give $\int_0^\infty F(u) u^{-3}\, du = \tfrac12 \int_0^\infty F''(u) u^{-1}\, du = 8 \int_0^\infty (\cos 2u - \cos 4u) u^{-1}\, du = 8 \ln 2$, by the Frullani integral. Divide by $8$.

## Examples and non-examples

**A ramp.** Let $f(t) = t$ on $[0,1]$. Then $\langle f, \varphi \rangle = \tfrac12$. With the substitution $u = 2^j t - k$,

$$\langle f, \psi_{j,k} \rangle = 2^{-3j/2} \int_0^1 (u + k)\, \psi(u)\, du = 2^{-3j/2} \int_0^1 u\, \psi(u)\, du = -\frac{2^{-3j/2}}{4}$$

for every $k$, because $\int \psi = 0$ removes the $k$ term. The coefficients of this smooth function shrink by $2^{-3/2}$ per level. The energy checks out: $\tfrac14 + \sum_{j \ge 0} 2^j \cdot \tfrac{2^{-3j}}{16} = \tfrac14 + \tfrac1{16} \cdot \tfrac43 = \tfrac13 = \int_0^1 t^2\, dt$.

**A jump.** Let $f = \mathbf 1_{[0, 1/3)}$. If $I_{j,k}$ lies inside $[0, \tfrac13)$ or outside it, then $\langle f, \psi_{j,k} \rangle = 0$. The point $\tfrac13$ is not a dyadic rational, so at each level $j \ge 0$ exactly one interval $I_{j,k}$ has it in its interior, and that coefficient is not zero. It equals $2^{j/2}$ times the length of the part of $[0,\tfrac13)$ in the left half minus the length in the right half, so its size is at most $2^{-j/2}/2$. The jump costs one coefficient per level, and these shrink only by $2^{-1/2}$ per level, more slowly than for the ramp.

**Non-example: a half-step shift.** The function $\psi(t - \tfrac12)$ is not in the family at scale $j = 0$, and $\langle \psi, \psi(\cdot - \tfrac12) \rangle = -\tfrac12$, from the overlap $[\tfrac12, 1)$ where the two functions are $-1$ and $1$. Orthogonality needs shifts by whole multiples of $2^{-j}$ at scale $j$.

**Non-example: the box.** The box $\varphi$ is not a wavelet. $\int \varphi = 1$, so $\hat\varphi(0) = 1$ and the integral of $|\hat\varphi(\omega)|^2/|\omega|$ diverges at $\omega = 0$.

**Non-example: a missing factor.** The function $\psi(2t)$ is orthogonal to $\psi(2t - 1)$, but its norm is $1/\sqrt 2$. Without the factor $2^{j/2}$ the family is orthogonal but not orthonormal, and the expansion needs a weight at each level.

## Related definitions

- **[Haar wavelet transform](/haar-wavelet-transform/).** The finite version: the coefficients of a vector of length $2^t$ in the discrete Haar basis, computed by averages and differences. That page gives the algorithm, its example and its error analysis.
- **[Discrete wavelet transform](/discrete-wavelet-transform/).** The same cascade with longer filters. Daubechies (1988) found compactly supported orthonormal wavelets with more vanishing moments and more smoothness. Among all real, compactly supported orthonormal wavelets, only the Haar wavelet is symmetric or antisymmetric (Daubechies 1992, Chapter 8); here $\psi(1 - t) = -\psi(t)$ and $\varphi(1 - t) = \varphi(t)$. Symmetric filters with compact support need the biorthogonal form of the transform.
- **[Continuous wavelet transform](/continuous-wavelet-transform/).** The inner products with $a^{-1/2}\psi((t - b)/a)$ for all real $a > 0$ and $b$. The Haar wavelet is admissible, with $C_\psi = 2 \ln 2$, but smooth wavelets are more common there.
- **[Walsh-Hadamard transform](/walsh-hadamard-transform/).** The Walsh functions also take only the values $\pm 1$ on $[0,1]$, but each one is spread over the whole interval. The Haar functions are local.
- **[Haar features](/haar-features/).** The rectangle features of the Viola-Jones detector are sums and differences of image boxes, named after this wavelet.

## References
