---
tag: DG68QC
kind: concept
slug: minimum-phase
name: Minimum-phase system
aliases:
- minimum-phase filter
area: graphics-and-signals/signal-processing
level: advanced
summary: "A causal stable system whose zeros are all strictly inside the unit circle, so its inverse is causal and stable too. Among systems with its magnitude response, it has the least energy delay."
prereqs: [transfer-function, frequency-response, bibo-stability]
see_also: [cepstrum, hilbert-transform, linear-prediction, levinson-durbin-algorithm, wiener-filter, polynomial-root-finding, autocorrelation, digital-filter-design]
sources:
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Section 5.5, All-Pass Systems, and Section 5.6, Minimum-Phase Systems (5.6.1 the minimum-phase and all-pass decomposition, 5.6.3 the minimum phase-lag, minimum group-delay and minimum energy-delay properties)
  - book: isbn:9780131873742
    title: John G. Proakis and Dimitris G. Manolakis, Digital Signal Processing, Principles, Algorithms, and Applications, fourth edition, Pearson Prentice Hall, 2007
    locator: Chapter 5, Frequency-Domain Analysis of LTI Systems (minimum-phase, maximum-phase and mixed-phase systems, and inverse systems)
---

A minimum-phase system is a causal, stable LTI system whose zeros, like its poles, all lie strictly inside the unit circle. The condition is the same as asking that the inverse system $1/H(z)$ be causal and stable too, which is what makes such a filter invertible in real time. Many systems share one magnitude response $|H(e^{i\omega})|$, because a zero can be flipped from $c$ to $1/\bar c$ without changing the magnitude. Among them the minimum-phase one has the least phase lag, the least group delay and the least energy delay: for every $N$, its first $N + 1$ samples hold the most energy.

## In plain words

Think of a filter as a set of points, its zeros, placed around a circle. You can move a zero from inside the circle to its mirror place outside, and the filter still lets each frequency through with the same strength. What changes is the timing: how long the filter takes to give out its response.

When all zeros are inside, the filter answers as early as it can. Its response puts as much energy as possible at the start. Such a filter is called minimum phase. It has a second good property: you can undo it with another filter that is also stable and does not need future input. Filters with zeros outside the circle cannot be undone in real time.

## The idea

**Setting.** $H(z) = B(z)/A(z)$ is a rational [transfer function](/transfer-function/) in lowest terms, with the causal region of convergence; frequencies $\omega$ are in radians per sample. By the [BIBO stability](/bibo-stability/) criterion, the system is stable if and only if every pole is strictly inside the unit circle.

**Definition.** $H$ is *minimum phase* if it is causal and stable and every zero $c$ satisfies $|c| < 1$. Equivalently, $H$ and $1/H$ are both causal and stable, since the zeros of $H$ are the poles of $1/H$. A zero on the unit circle is excluded: then $1/H$ is not stable, although some books still call such a system minimum phase. A causal stable system with all zeros outside the circle is *maximum phase*, and one with zeros on both sides is *mixed phase*.

**Flipping a zero keeps the magnitude.** For $|c| \ne 1$, the factors $1 - c z^{-1}$ and $z^{-1} - \bar c$ have the same magnitude on the unit circle:

$$|e^{-i\omega} - \bar c| = |1 - \bar c e^{i\omega}| = |\overline{1 - c e^{-i\omega}}| = |1 - c e^{-i\omega}|.$$

The second factor has its zero at $1/\bar c$. For real coefficients this is the reversal of the coefficients of a real factor, $(c_0, c_1) \mapsto (c_1, c_0)$, or of a quadratic factor with a complex pair. An FIR filter with $k$ zeros off the circle, not paired by flipping, thus has $2^k$ variants with the same magnitude response, and these are all the FIR filters of that length with that magnitude, up to a constant of modulus $1$. They all have the same autocorrelation $\sum_n h[n] \overline{h[n+m]}$.

**All-pass decomposition.** Every causal stable rational $H$ with no zeros on the unit circle factors as

$$H(z) = H_{\min}(z)\, H_{\mathrm{ap}}(z),$$

where $H_{\min}$ is minimum phase and $H_{\mathrm{ap}}(z) = \prod_{|c| > 1} \frac{z^{-1} - 1/c}{1 - z^{-1}/\bar c}$, over the zeros $c$ of $H$ outside the circle, is a causal stable all-pass system with $|H_{\mathrm{ap}}(e^{i\omega})| = 1$. A constant of modulus $1$ goes into $H_{\min}$. To get it, flip each zero $c$ outside the circle to $1/\bar c$ in $H_{\min}$, and put the pair of the old zero $c$ and the new pole $1/\bar c$ in $H_{\mathrm{ap}}$.

**Three minimum properties.** Let $G$ be causal and stable with $|G(e^{i\omega})| = |H_{\min}(e^{i\omega})|$, so $G = H_{\min} H_{\mathrm{ap}}$ for some causal stable all-pass $H_{\mathrm{ap}}$.

- *Minimum group delay.* Each all-pass factor has a positive group delay, $\tau_{\mathrm{ap}}(\omega) = \frac{1 - |a|^2}{|1 - a e^{-i\omega}|^2} > 0$ for the pole $a$, $|a| < 1$. So $\tau_G = \tau_{\min} + \tau_{\mathrm{ap}} \ge \tau_{\min}$ at every $\omega$.
- *Minimum phase lag.* The unwrapped phase of a causal stable all-pass factor is $0$ at $\omega = 0$ and decreases on $[0, \pi]$, so the phase lag $-\arg G(e^{i\omega})$ is at least that of $H_{\min}$ on $[0, \pi]$, when both phases are normalized to agree at $\omega = 0$.
- *Minimum energy delay.* For every $N \ge 0$, $\sum_{n=0}^{N} |g[n]|^2 \le \sum_{n=0}^{N} |h_{\min}[n]|^2$, and the totals are equal by [Parseval's theorem](/parsevals-theorem/). In particular $|g[0]| \le |h_{\min}[0]|$.

**Proof of the energy property for one flip.** Let $H = Q (1 - c z^{-1})$ and $G = Q (z^{-1} - \bar c)$ with $|c| < 1$ and $Q$ causal. Then $h[n] = q[n] - c\, q[n-1]$ and $g[n] = q[n-1] - \bar c\, q[n]$, and expanding the squares gives

$$|h[n]|^2 - |g[n]|^2 = (1 - |c|^2)\left(|q[n]|^2 - |q[n-1]|^2\right).$$

The right side telescopes: $\sum_{n=0}^{N} \left(|h[n]|^2 - |g[n]|^2\right) = (1 - |c|^2)\, |q[N]|^2 \ge 0$. Each flip of a zero from inside to outside lowers every partial energy or keeps it, so the variant with all zeros inside has the largest partial energies.

**Phase and magnitude are tied.** For a minimum-phase $H$, $\log H(z)$ is analytic on a region $|z| > r$ with $r < 1$, including $z = \infty$, so its complex [cepstrum](/cepstrum/) is causal. The log magnitude then fixes the phase: the two are a [Hilbert transform](/hilbert-transform/) pair on the unit circle. This is the base of the cepstral method to build a minimum-phase filter from a magnitude response.

**Spectral factorization.** Given a nonnegative trigonometric polynomial $R(e^{i\omega}) = \sum_{|m| < M} r[m] e^{-i\omega m}$, the Fejér-Riesz theorem gives an FIR $H$ of length $M$ with $|H(e^{i\omega})|^2 = R(e^{i\omega})$, and the minimum-phase one is unique up to a constant of modulus $1$. To compute it, find the roots of $z^{M-1} R(z)$ by [polynomial root finding](/polynomial-root-finding/); they come in pairs $c$, $1/\bar c$, and the factor takes the root of each pair inside the circle. Roots on the circle have even multiplicity and are shared.

## Examples

- **Zeros at $\frac{1}{2}$ and $3$.** Let $2H(z) = (2 - z^{-1})(1 - 3z^{-1})$, so $2h = [2, -7, 3]$. Flipping either zero gives four filters with the same magnitude response and the same energy $62$:

| zeros | $2h$ | partial energies of $2h$ |
|---|---|---|
| $\frac{1}{2}, 3$ (mixed) | $[2, -7, 3]$ | $4, 53, 62$ |
| $2, 3$ (maximum phase) | $[-1, 5, -6]$ | $1, 26, 62$ |
| $\frac{1}{2}, \frac{1}{3}$ (minimum phase) | $[-6, 5, -1]$ | $36, 61, 62$ |
| $\frac{1}{3}, 2$ (mixed) | $[3, -7, 2]$ | $9, 58, 62$ |

The minimum-phase filter has the largest partial energy at every length, and the maximum-phase filter is its time reverse, with the smallest. The minimum-phase filter has the causal stable inverse $1/(-3 + \frac{5}{2} z^{-1} - \frac{1}{2} z^{-2})$; the inverse of the first filter, taken causal, has a pole at $3$ and grows like $3^n$.

- **One zero outside.** $H(z) = 1 - 2z^{-1}$ is causal and stable but not minimum phase. Its decomposition is $H = H_{\min} H_{\mathrm{ap}}$ with $H_{\min}(z) = -2 + z^{-1} = -2(1 - \frac{1}{2} z^{-1})$ and $H_{\mathrm{ap}}(z) = \frac{z^{-1} - \frac{1}{2}}{1 - \frac{1}{2} z^{-1}}$. Both $H$ and $H_{\min}$ have the gain $|1 - 2e^{-i\omega}|$, from $1$ at $\omega = 0$ to $3$ at $\omega = \pi$.
- **Linear-phase filters are not minimum phase.** A real symmetric FIR filter with $h[n] = h[M-1-n]$ has its zeros in pairs $c$, $1/\bar c$ or on the circle. So, except for the trivial case of no zeros off the circle, it is mixed phase, and its group delay $(M-1)/2$ is not the least possible for its magnitude.
- **A delay.** $z^{-1}$ has $|H| = 1$ like the identity, but it is not minimum phase in the sense of this page: its inverse $z$ is not causal. Delays are all-pass factors that the decomposition sets aside.

## Where it is used

- **Inverse filtering and equalization.** Only a minimum-phase channel can be undone by a causal stable filter. For a mixed-phase channel, one inverts $H_{\min}$ and accepts the all-pass part, or adds a delay.
- **Linear prediction.** The prediction-error filter of the autocorrelation method of [linear prediction](/linear-prediction/) is minimum phase, because the [Levinson-Durbin algorithm](/levinson-durbin-algorithm/) gives reflection coefficients of modulus below $1$. So the all-pole synthesis filter is stable.
- **Causal Wiener filters.** The causal [Wiener filter](/wiener-filter/) needs the spectral factorization of the power spectrum into a minimum-phase factor and its reverse.
- **Filter design.** A minimum-phase FIR filter with a given magnitude has less delay than the linear-phase one, which matters for audio with low latency. It is built from a linear-phase design by spectral factorization, or with the [cepstrum](/cepstrum/); see [digital filter design](/digital-filter-design/).
- **[Phase retrieval](/phase-retrieval/).** For a minimum-phase signal, the magnitude of the Fourier transform fixes the phase, so the signal can be found from its magnitude alone.

## References
