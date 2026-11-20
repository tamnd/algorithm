---
tag: 9QSDYX
kind: concept
slug: twin-image-problem
name: Twin image problem
aliases:
- twin image
area: imaging-and-inverse-problems/phase-retrieval-and-coherent-imaging
level: advanced
summary: In in-line holography the conjugate image is focused at the mirror distance and overlaps the true image, since the intensity loses the sign of the phase.
prereqs: [digital-holography-reconstruction, angular-spectrum-method]
see_also: [phase-retrieval-ambiguities, phase-retrieval, transport-of-intensity-equation, coherent-diffraction-imaging, error-reduction-algorithm, optical-transfer-function, phase-diversity, gerchberg-saxton-algorithm]
sources:
  - paper: doi:10.1038/161777a0
    title: D. Gabor, A new microscopic principle, Nature 161(4098), 1948, 777 to 778
    locator: in-line holography and the second, conjugate image of the reconstruction (general locator)
  - paper: doi:10.1364/JOSA.52.001123
    title: Emmett N. Leith and Juris Upatnieks, Reconstructed wavefronts and communication theory, Journal of the Optical Society of America 52(10), 1962, 1123 to 1130
    locator: the off-axis reference that separates the twin images (general locator)
  - paper: doi:10.1364/OL.22.001268
    title: Ichirou Yamaguchi and Tong Zhang, Phase-shifting digital holography, Optics Letters 22(16), 1997, 1268
    locator: the recovery of the complex wave from several holograms with shifted reference phase (general locator)
  - paper: doi:10.1103/PhysRevLett.98.233901
    title: Tatiana Latychevskaia and Hans-Werner Fink, Solution to the twin image problem in holography, Physical Review Letters 98(23), 2007, 233901
    locator: iterative reconstruction of in-line holograms with a constraint on the absorption that removes the twin image (general locator)
  - book: isbn:9780974707723
    title: Joseph W. Goodman, Introduction to Fourier Optics, third edition, Roberts and Company, 2005
    locator: the chapter on holography, the Gabor hologram and its twin images (general locator)
---

The twin image is the second image that appears when an in-line hologram is reconstructed. A hologram records the intensity of the sum of a reference wave and the wave scattered by the object. The intensity contains the object wave and also its complex conjugate. When the hologram is propagated back to the object plane, the object wave comes into focus, and the conjugate wave forms a second image, the twin, that is in focus at the mirror position on the other side of the hologram. In the object plane the twin is out of focus and lies on top of the true image. Gabor met this problem in his first holograms in 1948. It is a form of the conjugate ambiguity of [phase retrieval](/phase-retrieval/): the intensity cannot tell a wave from its conjugate.

## In plain words

A hologram is a photo of the light that comes from an object, mixed with a plain beam. When you send light back through the photo, you get the object again. But the photo stores brightness only, and brightness looks the same for a wave and its mirror wave, which bends the opposite way. So the photo sends back both. One wave rebuilds the object where it was. The mirror wave rebuilds a copy as far away on the other side. If the plain beam and the object light travel in the same direction, both copies lie on one line, and when you look at the real object, the other copy is a blur over it. That blur is the twin image.

## The idea

Take a plane reference wave of amplitude 1 along the axis and a thin object with transmission $t = 1 + s$, where $s$ is the scattered part. Write $H_z$ for propagation over the distance $z$ with the [angular spectrum method](/angular-spectrum-method/), and $S_z = H_z s$. The hologram at distance $z$ is
$$h = |1 + S_z|^2 = 1 + S_z + \overline{S_z} + |S_z|^2 .$$
For waves that propagate, the transfer function obeys $\overline{H_z(f)} = H_{-z}(-f)$, so $\overline{H_z s} = H_{-z}\overline{s}$. Propagating the hologram back by $-z$ gives
$$H_{-z} h = 1 + s + H_{-2z}\, \overline{s} + H_{-z}|S_z|^2 .$$
The second term is the object. The third is the twin: the conjugate of the object, defocused by $2z$. The last term is a small background when the object scatters weakly. This identity is a theorem for propagating waves; the proof on the page on [digital holography reconstruction](/digital-holography-reconstruction/) states it as a corollary for in-line holograms.

The Fourier view shows what is lost. With the paraxial transfer function $e^{-i\pi\lambda z |f|^2}$ and a weak phase object $s = i\varphi$ with real $\varphi$, the spectrum of $h - 1$ is, to first order in $\varphi$,
$$\hat h(f) - \delta(f) \approx 2\,\hat\varphi(f)\, \sin(\pi\lambda z |f|^2).$$
For a weak absorbing object $s = -a$ with real $a$ the factor is $-2\cos(\pi\lambda z |f|^2)$. So a weak object is seen through a transfer function with zeros on the rings where $\pi\lambda z |f|^2$ is a multiple of $\pi$ (for phase) or an odd multiple of $\pi/2$ (for absorption). At those frequencies the hologram holds no information, and a single in-line hologram cannot recover the object there. The twin image is the visible form of this loss: the hologram fixes only the real part of $S_z$, and the imaginary part, which would separate the object from its twin, is not measured.

The ways out all add information that breaks the symmetry between $S_z$ and $\overline{S_z}$:

- **An off-axis reference** (Leith and Upatnieks 1962). A tilted reference puts the object term and the twin term on opposite sides of the spectrum, so a filter can keep one. This is the method of [digital holography reconstruction](/digital-holography-reconstruction/).
- **Phase shifting** (Yamaguchi and Zhang 1997). Several holograms with known shifts of the reference phase give $S_z$ by a linear solve.
- **Several distances.** Holograms at several $z$ have different zeros of the transfer function and together cover all frequencies. This is the idea behind the [transport of intensity equation](/transport-of-intensity-equation/) and multi-distance phase retrieval.
- **Constraints on the object.** If the object is known to absorb, $|t| \le 1$, or to have a known support, an iterative method in the spirit of [error reduction](/error-reduction-algorithm/) can suppress the twin. Latychevskaia and Fink (2007) did this with a constraint on the absorption.

## Examples

- **A point scatterer.** For $s = \epsilon\,\delta(x - x_0)$, the object term is a point at $x_0$ and the twin is a spherical wave that would converge at distance $2z$ beyond the object plane, which spreads into a ring pattern over the reconstruction.
- **Gabor's experiment.** Gabor (1948) proposed holography to correct the aberrations of electron lenses. His in-line reconstructions with light showed the second image as an out of focus background.
- **Far field in-line holography of particles.** If the object is small and $z$ is large, the twin is spread over a large area and becomes a weak, nearly uniform background (a heuristic). Holography of small particles relies on this.
- **Pure phase object at a small distance.** For $\pi\lambda z |f|^2 \ll 1$, the factor $\sin(\pi\lambda z |f|^2)$ is close to $\pi\lambda z|f|^2$, and the hologram contrast $h - 1$ is close to $-\frac{\lambda z}{2\pi}\nabla^2\varphi$. This is the small distance limit in which the transport of intensity equation holds.

## Where it is used

- **Digital in-line holographic microscopy** of cells and particles, where the simple setup is attractive and the twin must be handled by computation.
- **Electron holography and X-ray in-line holography**, where off-axis setups are harder to build.
- **Propagation-based phase contrast imaging with X-rays**, where the image at a distance is an in-line hologram and phase retrieval must deal with the zeros of the transfer function.
- **[Coherent diffraction imaging](/coherent-diffraction-imaging/)**, where the conjugate reflection of the object fits the same data and causes stagnation in a mix of the object and its twin.

## References
