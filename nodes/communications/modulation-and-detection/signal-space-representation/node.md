---
tag: 39MBDH
kind: concept
slug: signal-space-representation
name: Signal space representation
aliases:
- signal space
- geometric representation of signals
area: communications/modulation-and-detection
level: intro
summary: Writes each transmitted waveform as a vector of coefficients on an orthonormal basis, so detection becomes geometry in a low-dimensional space.
prereqs: [digital-modulation, gram-schmidt-process]
see_also: [signal-constellation, symbol-detection, sufficient-statistic, matched-filter, minimum-distance-detector, additive-white-gaussian-noise-channel, sampling-theorem, union-bound]
sources:
  - book: isbn:9780072957167
    title: John G. Proakis and Masoud Salehi, Digital Communications, fifth edition, McGraw-Hill, 2008
    locator: Section 2.2, Signal Space Representation of Waveforms (vector space and signal space concepts, orthogonal expansions and the Gram-Schmidt procedure), and Section 4.1, Waveform and Vector Channel Models
  - book: isbn:9780881335545
    title: John M. Wozencraft and Irwin M. Jacobs, Principles of Communication Engineering, Wiley, 1965 (reissued by Waveland Press, 1990)
    locator: Chapter 4, Optimum receiver principles (the vector representation of signals and noise, and the irrelevance of the noise outside the signal space)
  - book: isbn:9780521845274
    title: David Tse and Pramod Viswanath, Fundamentals of Wireless Communication, Cambridge University Press, 2005
    locator: Appendix A, Detection and estimation in additive Gaussian noise (the vector Gaussian channel and sufficient statistics)
  - paper: doi:10.1109/JRPROC.1949.232969
    title: Claude E. Shannon, Communication in the presence of noise, Proceedings of the IRE 37(1), 10-21, 1949
    locator: the geometric representation of signals of bandwidth W and duration T as points in a space of 2TW dimensions
  - book: Vladimir A. Kotelnikov, The Theory of Optimum Noise Immunity, McGraw-Hill, 1959
    title: Vladimir A. Kotelnikov, The Theory of Optimum Noise Immunity, translated by R. A. Silverman, McGraw-Hill, 1959
    locator: the whole book, a translation of the 1947 doctoral dissertation on optimum reception in noise
---

The signal space representation writes each waveform of a modulation scheme as a vector of its coefficients on an orthonormal basis of the signal set. Energies become squared lengths, correlations become inner products, and in white Gaussian noise the noise becomes a Gaussian vector with independent coordinates. So [symbol detection](/symbol-detection/) becomes a question of distances between points. This page gives the geometry; the [signal constellation](/signal-constellation/) is the point set that a scheme uses in it, and [digital modulation](/digital-modulation/) is the wider concept.

## In plain words

Each signal that a sender can send is a curve over a short time. If all the curves are built from a few basic shapes, added with different weights, then each curve is fully described by its list of weights. That list is a point in a space with one axis per basic shape.

The point of this view is that useful facts about the curves become facts about the points. How strong a signal is becomes how far its point is from the origin. How hard it is to confuse two signals becomes the distance between their points. The noise also gets a simple picture: a random push of the same size, on average, along every axis. The noise that lies outside the space of the basic shapes does not help to tell the signals apart, so the receiver may ignore it.

## The idea

**Waveforms as vectors.** Take real finite-energy waveforms on an interval, with the inner product $\langle f, g \rangle = \int f(t) g(t)\, dt$ and the norm $\|f\| = \sqrt{\langle f, f\rangle}$. The [Gram-Schmidt process](/gram-schmidt-process/) applied to a signal set $s_1, \ldots, s_M$ gives an orthonormal basis $\phi_1, \ldots, \phi_N$ of the space that the signals span, with $N \le M$. Each signal is then

$$s_m(t) = \sum_{n=1}^{N} s_{mn}\, \phi_n(t), \qquad s_{mn} = \langle s_m, \phi_n \rangle,$$

and the vector $\mathbf{s}_m = (s_{m1}, \ldots, s_{mN})$ describes it exactly. Since the basis is orthonormal, $\langle s_m, s_k \rangle = \mathbf{s}_m \cdot \mathbf{s}_k$. In particular, the energy is $E_m = \|\mathbf{s}_m\|^2$ and the squared distance is $\int (s_m - s_k)^2\, dt = \|\mathbf{s}_m - \mathbf{s}_k\|^2$. These are identities of the expansion, not approximations.

**Noise in signal space.** Let the received waveform be $r(t) = s_m(t) + n(t)$, where $n$ is white Gaussian noise of two-sided power spectral density $N_0/2$. Its projections $n_k = \langle n, \phi_k \rangle$ are Gaussian with $\mathbb{E}[n_k n_l] = (N_0/2)\,\delta_{kl}$, so they are independent with variance $N_0/2$. The projection of $r$ is the vector channel

$$\mathbf{r} = \mathbf{s}_m + \mathbf{n}, \qquad \mathbf{n} \sim \mathcal{N}(0, (N_0/2) I_N).$$

**The remainder is irrelevant.** The rest of the noise, $n(t) - \sum_k n_k \phi_k(t)$, is Gaussian and uncorrelated with every $n_k$, so it is independent of them. It does not depend on which signal was sent. So $\mathbf{r}$ is a [sufficient statistic](/sufficient-statistic/) for $m$: an optimal receiver loses nothing by working with the $N$ numbers $r_k = \langle r, \phi_k \rangle$ instead of the whole waveform. Wozencraft and Jacobs call this the theorem of irrelevance. The receiver computes the $r_k$ with $N$ correlators or with filters matched to the $\phi_k$ (see [matched filter](/matched-filter/)).

**Complex baseband.** For a passband signal $\mathrm{Re}\{x\, g(t) \sqrt{2} e^{j2\pi f_c t}\}$, the two functions $\sqrt{2} g(t)\cos(2\pi f_c t)$ and $-\sqrt{2} g(t)\sin(2\pi f_c t)$ are close to orthonormal when $f_c$ is large compared with the bandwidth of $g$. The coefficients on them are $\mathrm{Re}\,x$ and $\mathrm{Im}\,x$. So one complex number per symbol gives two real dimensions, and the noise on each has variance $N_0/2$. This is the complex model $y = x + w$ with $w \sim \mathcal{CN}(0, N_0)$ that the area pages use.

**How many dimensions.** A signal set of $M$ waveforms has at most $M$ dimensions. A signal limited to about $W$ Hz of bandwidth and $T$ seconds has about $2WT$ degrees of freedom. This is a heuristic count, not an exact theorem, because no nonzero signal is limited in both time and frequency; Shannon used it in 1949 to picture signals as points in a space of $2TW$ dimensions. PAM uses 1 real dimension per symbol, PSK and QAM use 2, and $M$-ary orthogonal FSK uses $M$.

## Examples

**Three signals in two dimensions.** On $[0, 2)$ take $s_1 = 1$; $s_2 = 1$ on $[0, 1)$ and $-1$ on $[1, 2)$; and $s_3 = 1$ on $[0, 1)$ and $0$ on $[1, 2)$. Gram-Schmidt gives $\phi_1 = s_1/\sqrt{2}$. Then $\langle s_2, \phi_1 \rangle = 0$, so $\phi_2 = s_2/\sqrt{2}$. For $s_3$, $\langle s_3, \phi_1 \rangle = \langle s_3, \phi_2 \rangle = 1/\sqrt{2}$, and $s_3 - \phi_1/\sqrt{2} - \phi_2/\sqrt{2} = s_3 - s_1/2 - s_2/2 = 0$. So the dimension is 2, and the vectors are

$$\mathbf{s}_1 = (\sqrt{2}, 0), \quad \mathbf{s}_2 = (0, \sqrt{2}), \quad \mathbf{s}_3 = (1/\sqrt{2}, 1/\sqrt{2}).$$

As a check, $s_1 - s_3$ is 0 on $[0, 1)$ and 1 on $[1, 2)$, so $\int (s_1 - s_3)^2\, dt = 1$; and $\|\mathbf{s}_1 - \mathbf{s}_3\|^2 = (1/\sqrt{2})^2 + (1/\sqrt{2})^2 = 1$.

**QPSK.** The four signals $\pm\sqrt{E_s/2}\,\phi_1 \pm \sqrt{E_s/2}\,\phi_2$ with the cosine and sine basis above are the corners of a square. The distance between neighbors is $\sqrt{2E_s}$.

**Orthogonal signals.** $M$ orthogonal signals of energy $E$ are the points $\sqrt{E}\,\mathbf{e}_m$ of an $M$-dimensional space. Every pair is at the distance $\sqrt{2E}$, the same as for antipodal pairs of energy $E/2$.

**Non-example.** A set of signals in noise that is not white, or not Gaussian, still has the vector expansion, but the projection is no longer a sufficient statistic in general, and the noise coordinates are no longer independent. A whitening filter must come first.

## Where it is used

The representation is the base of the analysis of every memoryless modulation scheme: the optimum receiver is a correlator or [matched filter](/matched-filter/) bank followed by a decision on the vector, and the error probability depends only on the distances between points. The [minimum distance detector](/minimum-distance-detector/), the [union bound](/union-bound/) on the [symbol error rate](/symbol-error-rate/), the comparison of constellations by their minimum distance and energy, and the design of lattice constellations all start here. The same geometry, with $N$ antennas or users instead of $N$ basis functions, is the model of [MIMO detection](/mimo-detection/).

**History.** Kotelnikov's 1947 doctoral dissertation on optimum reception in Gaussian noise, published in English in 1959, is an early source of this approach. Shannon represented band-limited signals as points in a space of many dimensions in 1949. Wozencraft and Jacobs made the vector channel and the theorem of irrelevance the base of their 1965 textbook, and their treatment became the standard one.

## References
