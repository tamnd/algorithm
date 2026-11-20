---
tag: 7EK9T1
kind: definition
slug: patterson-function
name: Patterson function
aliases:
- Patterson map
area: imaging-and-inverse-problems/phase-retrieval-and-coherent-imaging
level: core
summary: The Fourier transform of the measured intensities of a crystal, equal to the autocorrelation of its electron density, with peaks at interatomic vectors.
prereqs: [autocorrelation, convolution-theorem, crystallographic-phase-problem]
see_also: [direct-methods-crystallography, charge-flipping, phase-retrieval, cross-correlation, parseval-theorem, discrete-fourier-transform, phase-retrieval-ambiguities, coherent-diffraction-imaging]
sources:
  - paper: doi:10.1103/PhysRev.46.372
    title: A. L. Patterson, A Fourier series method for the determination of the components of interatomic distances in crystals, Physical Review 46(5), 1934, 372 to 376
    locator: the Fourier series with the squared amplitudes as coefficients and its peaks at interatomic vectors (general locator)
  - paper: doi:10.1063/1.1749863
    title: David Harker, The application of the three-dimensional Patterson method and the crystal structures of proustite, Ag3AsS3, and pyrargyrite, Ag3SbS3, Journal of Chemical Physics 4(6), 1936, 381 to 390
    locator: the concentration of peaks between atoms related by symmetry on special planes and lines of the Patterson function (general locator)
  - book: isbn:9780198500728
    title: Carmelo Giacovazzo, Direct Phasing in Crystallography, Fundamentals and Applications, Oxford University Press, 1998
    locator: the Patterson function and its use in phasing (general locator)
---

The Patterson function of a crystal is the Fourier series whose coefficients are the measured intensities $|F(h)|^2$. It needs no phases, so it can be computed directly from the data. Patterson (1934) showed that it equals the autocorrelation of the electron density over one unit cell, so it has a peak at every vector between two atoms. It is the part of the structure that the intensities determine, and it is the starting point of the heavy atom method for the [crystallographic phase problem](/crystallographic-phase-problem/).

## Definition

Let $\rho(x)$ be the real electron density of a crystal, periodic in the unit cell of volume $V$, with structure factors $F(h) = \int_{\text{cell}} \rho(x)\, e^{2\pi i\, h \cdot x}\, dx$ for integer indices $h$, in the crystallographic sign convention. Here $dx$ is the volume element, so that $\int_{\text{cell}} dx = V$, and $h \cdot x$ uses the fractional coordinates of $x$. The **Patterson function** is
$$P(u) = \frac{1}{V} \sum_h |F(h)|^2\, e^{-2\pi i\, h \cdot u} = \frac{1}{V} \sum_h |F(h)|^2 \cos(2\pi\, h \cdot u),$$
where the second form uses $|F(-h)| = |F(h)|$ (Friedel's law for a real density).

**Autocorrelation (a theorem).** $P(u) = \int_{\text{cell}} \rho(x)\, \rho(x + u)\, dx$, with $\rho$ extended periodically.

*Proof.* Let $A(u) = \int_{\text{cell}} \rho(x) \rho(x + u)\, dx$. Its Fourier coefficient is $\int_{\text{cell}} A(u) e^{2\pi i\, h \cdot u} du = \int \rho(x) e^{-2\pi i\, h \cdot x} dx \int \rho(y) e^{2\pi i\, h \cdot y} dy = \overline{F(h)}\, F(h)$, after the change of variable $y = x + u$ over one period. So $A$ has the Fourier series of $P$. This is the [convolution theorem](/convolution-theorem/) for the [autocorrelation](/autocorrelation/) on the torus. $\square$

**On a grid.** For a density sampled on an $n_1 \times n_2 \times n_3$ grid with the DFT $F = \mathcal{D}\rho$, the inverse DFT of $|F|^2$ is the circular autocorrelation $\sum_x \rho(x)\rho(x + u)$, with indices taken modulo the grid.

**Properties** (all theorems from the definition):

- $P$ is real and centrosymmetric, $P(-u) = P(u)$, whatever the symmetry of the crystal.
- $P(0) = \int \rho^2 \ge |P(u)|$ for every $u$, by the Cauchy-Schwarz inequality.
- For a density of $N$ atoms, $\rho = \sum_j \rho_j(x - x_j)$, the function is the sum of $N^2$ terms $\int \rho_i(x - x_i)\rho_j(x + u - x_j)\,dx$, each a peak centered at $u = x_j - x_i$. The $N$ terms with $i = j$ pile up at the origin, and the other $N(N - 1)$ peaks lie at the interatomic vectors. The height of a peak grows with the product of the two atomic numbers, and the peak is wider than an atom, since it is a correlation of two atoms.
- Atoms related by a symmetry operation of the space group give peaks on special planes or lines, the Harker sections (Harker 1936). For example, for a twofold axis along $b$, the atoms at $(x, y, z)$ and $(-x, y, -z)$ give a peak at $(2x, 0, 2z)$, on the plane $v = 0$.

## Examples and non-examples

- **Two atoms in one dimension.** For point atoms of weight $f_1$ at $x_1$ and $f_2$ at $x_2$, $P(u) = (f_1^2 + f_2^2)\,\delta(u) + f_1 f_2\, [\delta(u - (x_2 - x_1)) + \delta(u + (x_2 - x_1))]$ on the circle. The distance is visible; the absolute positions are not.
- **A heavy atom among light ones.** If one atom has a much larger atomic number $Z$ than the rest, the peaks between its copies have height of order $Z^2$ and stand out above the many weak peaks between light atoms. This is how the heavy atom method finds its positions (a heuristic that works when the heavy atoms carry a large share of $\sum Z^2$).
- **A dense structure.** With $N = 100$ atoms, there are $9900$ non-origin peaks in one cell, and they overlap so much that individual vectors cannot be read. The Patterson function is still defined, but it is not useful as a list of vectors.
- **Non-example: the density itself.** The Patterson function is not a map of the atoms. It has the symmetry of the vector set, not of the structure, and it is the same for a structure, its shifts and its inverse.
- **Non-example: a unique fingerprint.** Different structures can have the same Patterson function. The one-dimensional point sets $\{0, 1, 3, 10, 11, 13, 30, 31, 33\}$ and $\{0, 1, 3, 20, 21, 23, 30, 31, 33\}$ have the same multiset of differences and so the same Patterson function for equal atoms, but neither is a shift or a reflection of the other. Such sets are called homometric.

## Related definitions

- **[Autocorrelation](/autocorrelation/).** The Patterson function is the autocorrelation of the density of one cell, made periodic. For an isolated object the intensity sampled finely gives the full autocorrelation without wrap around; this is the basis of [coherent diffraction imaging](/coherent-diffraction-imaging/).
- **Sharpened and origin-removed Patterson functions.** Replacing $|F(h)|^2$ by $|E(h)|^2$, the squared normalized structure factors of [direct methods](/direct-methods-crystallography/), makes the peaks sharper. Subtracting the mean of the coefficients removes most of the large origin peak.
- **Difference Patterson function.** The Fourier series of the differences of intensities between two related crystals, such as a native crystal and one with heavy atoms, has peaks mainly at the vectors between the heavy atoms.
- **Patterson symmetry.** The symmetry of $P$ is the point group of the crystal with a center of symmetry added and with the translations of glide planes and screw axes removed; the centering of the lattice stays.
- **[Phase retrieval ambiguities](/phase-retrieval-ambiguities/).** The trivial changes that keep the Patterson function fixed, a shift and the inversion, are the crystallographic form of these ambiguities.

## References
