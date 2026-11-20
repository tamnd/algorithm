---
tag: VE5MC5
kind: concept
slug: oversampling-in-phase-retrieval
name: Oversampling in phase retrieval
aliases:
- oversampling ratio
area: imaging-and-inverse-problems/phase-retrieval-and-coherent-imaging
level: core
summary: "Sampling the diffraction intensity more finely than the object's own Nyquist spacing. The ratio of measured intensities to unknown pixels must be above 2 for the data to hold enough information."
prereqs: [phase-retrieval, autocorrelation, nyquist-rate]
see_also: [coherent-diffraction-imaging, bruck-sodin-uniqueness, phase-retrieval-ambiguities, hybrid-input-output, shrinkwrap, patterson-function, crystallographic-phase-problem, aliasing]
sources:
  - paper: doi:10.1364/JOSAA.15.001662
    title: Jianwei Miao, David Sayre and Henry N. Chapman, Phase retrieval from the magnitude of the Fourier transforms of nonperiodic objects, Journal of the Optical Society of America A 15(6), 1998, from page 1662
    locator: the abstract, which states that the phase problem is underdetermined by a factor of 2 in 1D, 2D and 3D, that oversampling by 2 in each dimension is not necessary, and the phasing tests with loose supports
  - paper: doi:10.1107/S0365110X52002276
    title: D. Sayre, Some implications of a theorem due to Shannon, Acta Crystallographica 5(6), 1952, page 843
    locator: the one page note that the intensity between the Bragg peaks carries information on the phase
  - paper: doi:10.1109/MSP.2014.2352673
    title: Yoav Shechtman, Yonina C. Eldar, Oren Cohen, Henry N. Chapman, Jianwei Miao and Mordechai Segev, Phase retrieval with application to optical imaging, a contemporary overview, IEEE Signal Processing Magazine 32(3), 2015, 87 to 109
    locator: Section II (Sayre 1952, and oversampling in coherent diffraction imaging), Section III.A (the oversampled DFT and the autocorrelation) and Section III.B (M of at least 2N - 1 in every dimension)
---

Oversampling in [phase retrieval](/phase-retrieval/) means that the intensity of a diffraction pattern is measured on a grid that is finer than the Nyquist spacing of the object itself. The intensity is the Fourier transform of the [autocorrelation](/autocorrelation/) of the object, and the autocorrelation is twice as wide as the object along each axis. So the samples at the object's own spacing alias the autocorrelation, and samples twice as fine hold all of it. The **oversampling ratio** $\sigma$ is the number of measured intensities divided by the number of unknown pixels. Miao, Sayre and Chapman (1998) argued that $\sigma > 2$ in total is the condition, not a factor of 2 along each axis.

## In plain words

A diffraction pattern records how bright the light is in each direction, but not the timing of its waves. Half of the information is lost, so the pattern alone does not give the object back.

Suppose you know that the object is small and sits inside a dark frame. If you measure the pattern at many more points than the object has pixels, you get more numbers than unknowns, and the known dark frame around the object becomes a strong clue. When the measured numbers are at least about twice the unknowns, the clue is usually enough for the iterative methods to find the object.

A crystal repeats the same cell many times, and its pattern has bright spots only at fixed places. That is like measuring too coarsely, and it is the reason why crystallography needs extra tricks.

## The idea

**What the samples hold.** Let $x$ have support in a box of $n_1 \times \cdots \times n_d$ pixels, and let $r[k] = \sum_t x[t + k]\, \overline{x[t]}$ be its autocorrelation, with support in a box of $(2n_1 - 1) \times \cdots \times (2n_d - 1)$ lags. The intensity is

$$I(\omega) = |X(\omega)|^2 = \sum_k r[k]\, e^{-i k \cdot \omega}.$$

Sample $I$ on the grid $\omega_k = 2\pi j / M_k$. The inverse DFT of the samples is the autocorrelation folded with period $M_k$ along each axis. With $M_k = n_k$, the folding adds lag $k$ to lag $k \pm n_k$, and the data hold only the circular autocorrelation. With $M_k \ge 2n_k - 1$, there is no overlap and the data hold $r$ exactly (Shechtman et al. 2015, Section III.A). This is [aliasing](/aliasing/), with the autocorrelation as the signal. The same samples are the $M$ point DFT of $x$ padded with zeros to $M_1 \times \cdots \times M_d$ pixels.

**The oversampling ratio.** For the padded array,

$$\sigma = \frac{M_1 \cdots M_d}{n_1 \cdots n_d} = \frac{\text{number of measured intensities}}{\text{number of unknown pixels}}.$$

Sampling at $2n_k - 1$ along each axis gives $\sigma$ near $2$ in 1D, $4$ in 2D and $8$ in 3D.

**The count.** At $\sigma = 1$ the data are half of what is needed. A complex image of $N$ pixels has $2N$ real unknowns and gives $N$ intensities. A real image has $N$ unknowns, but its intensity has the symmetry $I(-\omega) = I(\omega)$, so only about $N/2$ intensities are independent. In both cases the problem is underdetermined by a factor of $2$, as Miao, Sayre and Chapman state. Their conclusion is that a total ratio $\sigma > 2$ should be enough, and that a factor of 2 along each axis, which gives $\sigma = 4$ or $8$, is not necessary. A count of equations is not a proof of uniqueness: in 1D, even $\sigma = 2$ leaves up to $2^{n-2}$ solutions.

**The link to the support.** In the padded array, $\sigma - 1$ times as many pixels as the object has are known to be zero. The support constraint of [error reduction](/error-reduction-algorithm/), [hybrid input-output](/hybrid-input-output/) and [shrinkwrap](/shrinkwrap/) forces these pixels to zero. So oversampling and the support constraint are the same information seen in two domains: more samples in Fourier space means a larger known zero region in object space. The support of the autocorrelation is the set of differences of points of the object support, which gives a first, loose support for these methods.

## Examples

- **1D, without and with oversampling.** Take $x = [1, 5, 6]$ with $n = 3$. Its autocorrelation is $r = [6, 35, 62, 35, 6]$ for lags $-2$ to $2$, so $I(\omega) = 62 + 70 \cos\omega + 12 \cos 2\omega$. With $M = 3$ ($\sigma = 1$), the samples are $I(0) = 144$ and $I(2\pi/3) = I(4\pi/3) = 62 - 35 - 6 = 21$. Their inverse DFT is the circular autocorrelation $[62, 41, 41]$, where $41 = 35 + 6$ mixes lags $1$ and $-2$. A real $y$ with these data must have $\sum y^2 = 62$ and $\sum_t y_t y_{t+1 \bmod 3} = 41$, so $(\sum y)^2 = 62 + 2 \cdot 41 = 144$. With $\sum y = 12$ these are all points on a circle of radius $\sqrt{14}$ around $(4, 4, 4)$ in the plane $\sum y = 12$. One of them is $(4 + \sqrt 7, 4 - \sqrt 7, 4)$, with squares adding to $(23 + 8\sqrt7) + (23 - 8\sqrt7) + 16 = 62$. So a whole curve of signals fits. With $M = 5$ ($\sigma = 5/3$, which is $(2n - 1)/n$), the data give all of $r$, and only finitely many signals fit: the 8 listed on the [phase retrieval](/phase-retrieval/) page, $\pm[1, 5, 6]$, $\pm[6, 5, 1]$, $\pm[2, 7, 3]$ and $\pm[3, 7, 2]$.
- **2D, less than 2 along each axis.** A $16 \times 16$ object in a $23 \times 23$ array has $\sigma = 529 / 256 \approx 2.07$. That is above 2 in total, but $23 < 31 = 2 \cdot 16 - 1$ along each axis, so the data do not hold the full autocorrelation. The count of Miao, Sayre and Chapman covers this case; the [uniqueness theorem](/bruck-sodin-uniqueness/), which uses the full autocorrelation, does not. A $31 \times 31$ array gives $\sigma = 961 / 256 \approx 3.75$ and the full autocorrelation.
- **A crystal.** A crystal with a unit cell of $n$ pixels per axis has its diffraction only at the Bragg peaks, $n$ samples per axis, so $\sigma = 1$. The data give the circular autocorrelation of the cell, the [Patterson function](/patterson-function/), and the phases must come from other knowledge (see the [crystallographic phase problem](/crystallographic-phase-problem/)). Sayre (1952) noted that the intensity between the Bragg peaks would carry the missing information, but a crystal does not give it.

## Where it is used

- **Coherent diffraction imaging.** [Coherent diffraction imaging](/coherent-diffraction-imaging/) of a single, nonperiodic object records a continuous pattern, so the detector can sample it as finely as needed. The pixel size and the distance to the detector are chosen so that $\sigma$ is above 2. Shechtman et al. (2015, Section II) describe the combination of X-ray diffraction, oversampling and phase retrieval as the start of this field.
- **Iterative phase retrieval.** Error reduction, hybrid input-output, the [difference map](/difference-map/), [RAAR](/raar/) and shrinkwrap all use the zero region that the oversampling gives. With $\sigma$ near $1$ they have little to work with.
- **Ptychography.** [Ptychography](/ptychography/) records many patterns from overlapping positions of the illumination, so the data are redundant across patterns as well as within each one.

## References
