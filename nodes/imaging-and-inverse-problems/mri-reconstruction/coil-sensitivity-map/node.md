---
tag: XC3VNA
kind: definition
slug: coil-sensitivity-map
name: Coil sensitivity map
aliases:
- coil sensitivity profile
area: imaging-and-inverse-problems/mri-reconstruction
level: core
summary: "The complex weight s_k(r) with which receive coil k sees the magnetization at the point r, so that coil k records the image s_k x. Parallel imaging uses the maps to replace skipped k-space lines."
prereqs: [mri-signal-equation]
see_also: [sense, espirit, root-sum-of-squares-coil-combination, g-factor, cg-sense, grappa, mri-reconstruction-problem, k-space]
sources:
  - paper: doi:10.1016/0022-2364(76)90233-X
    title: D. I. Hoult and R. E. Richards, The signal-to-noise ratio of the nuclear magnetic resonance experiment, Journal of Magnetic Resonance 24(1), 1976, 71 to 85
    locator: the principle of reciprocity, which relates the received signal to the field the coil makes per unit current (general locator)
  - paper: doi:10.1002/mrm.1910160203
    title: P. B. Roemer, W. A. Edelstein, C. E. Hayes, S. P. Souza and O. M. Mueller, The NMR phased array, Magnetic Resonance in Medicine 16(2), 1990, 192 to 225
    locator: the coil array with separate receivers and the combination of the coil images with the sensitivities and the noise matrix (general locator)
  - paper: doi:10.1002/(SICI)1522-2594(199911)42:5<952::AID-MRM16>3.0.CO;2-S
    title: Klaas P. Pruessmann, Markus Weiger, Markus B. Scheidegger and Peter Boesiger, SENSE, sensitivity encoding for fast MRI, Magnetic Resonance in Medicine 42(5), 1999, 952 to 962
    locator: the sensitivity assessment from a reference scan, as the ratio of the coil images to a body coil image (general locator)
  - paper: doi:10.1002/(SICI)1522-2594(200005)43:5<682::AID-MRM10>3.0.CO;2-G
    title: David O. Walsh, Arthur F. Gmitro and Michael W. Marcellin, Adaptive reconstruction of phased array MR imagery, Magnetic Resonance in Medicine 43(5), 2000, 682 to 690
    locator: the map estimate from the dominant eigenvector of the local signal correlation matrix (general locator)
  - paper: doi:10.1002/mrm.24751
    title: Martin Uecker, Peng Lai, Mark J. Murphy, Patrick Virtue, Michael Elad, John M. Pauly, Shreyas S. Vasanawala and Michael Lustig, ESPIRiT, an eigenvalue approach to autocalibrating parallel MRI, where SENSE meets GRAPPA, Magnetic Resonance in Medicine 71(3), 2014, 990 to 1001
    locator: the maps as eigenvectors with eigenvalue 1 of an operator built from the calibration data (general locator)
---

A coil sensitivity map describes how strongly, and with which phase, one receive coil of an MRI scanner sees each point of the body. A coil records the magnetization weighted by its map, so each coil gives a different weighted copy of the same image. [SENSE](/sense/), [CG-SENSE](/cg-sense/) and [ESPIRiT](/espirit/) use the maps to rebuild an image from fewer k-space samples; [GRAPPA](/grappa/) and [SPIRiT](/spirit/) use them only through the calibration data. The idea of combining coil images with their sensitivities goes back to the phased array of Roemer and colleagues (1990).

## Definition

Let $x(r)$ be the transverse magnetization at the point $r$ at the echo time, a complex function on the field of view. A receive coil $k$ has a complex function $s_k(r)$, its **sensitivity map**, such that the noiseless signal of coil $k$ is

$$y_k(t) = \int s_k(r)\, x(r)\, e^{-2\pi i\, k(t) \cdot r}\, dr,$$

the [MRI signal equation](/mri-signal-equation/) with the image $s_k x$ in place of $x$. The image of coil $k$ is $m_k = s_k x$. On an $n \times n$ grid the map is an $n \times n$ complex array, and the discrete model is $y_k = M F_u (s_k x)$ with the sampling mask $M$ and the unitary DFT $F_u$.

This is a model. By the principle of reciprocity (Hoult and Richards 1976), $s_k(r)$ is set by the transverse magnetic field that coil $k$ would make at $r$ per unit current. At low field strength and for a body much smaller than the wavelength, that field is smooth. At high field the wavelength in tissue is comparable to the body, and the maps show more structure.

A set of maps is determined only up to a common factor at each point: for any function $\phi(r) \ne 0$, the maps $s_k \phi$ and the image $x/\phi$ give the same data. Algorithms fix this freedom by a convention, for example $\sum_k |s_k(r)|^2 = 1$ with the phase of one coil set to zero, or the maps divided by a body coil image. The image a method returns is then $x$ times the matching factor.

## Examples and non-examples

- **Ring of coils.** The tests of the pages in this group use four Gaussian profiles $s_k(r) = e^{-\lvert r - r_k\rvert^2/1.2}\, e^{i(0.9k + 0.4 r_x - 0.3 r_y)}$ on $[-1, 1]^2$, with the coil centers $r_k$ at distance 1.2 from the center at 20, 110, 200 and 290 degrees. Each coil sees the side near it brightly. The phase ramp is shared by all coils, and the offset $0.9k$ differs between them.
- **Maps of two frequencies.** The maps $s_k(i, j) = e^{i\psi_k}(1 + a_k e^{i(2\pi j/n - u_k)})(1 + b_k e^{i(2\pi i/n - v_k)})$ have only the image frequencies 0 and 1 on each axis, so in k-space each coil image is the object convolved with a $2 \times 2$ kernel. For such maps a small k-space kernel is exact, which is why the tests of [GRAPPA](/grappa/), [SPIRiT](/spirit/) and [ESPIRiT](/espirit/) use them.
- **Ratio maps.** Dividing each coil image by a body coil image, or by the [root-sum-of-squares](/root-sum-of-squares-coil-combination/) image, gives an estimate of $s_k$ up to the common factor above. The estimate is undefined where the object has no signal.
- **Eigenvector maps.** Walsh, Gmitro and Marcellin (2000) take the dominant eigenvector of the local $c \times c$ correlation matrix of the coil images. ESPIRiT takes the eigenvector with eigenvalue 1 of a matrix built from the calibration k-space.
- **Non-example: the magnitude alone.** The map $|s_k|$ without its phase is not a sensitivity map in this sense. With $|s_k|$ in place of $s_k$, [SENSE](/sense/) solves the wrong equations whenever the phases of the coils differ.
- **Non-example: the coil image.** The coil image $m_k = s_k x$ contains the object. With the coil images as maps, fully sampled data give the value 1 at every pixel with signal: the contrast moves into the maps, and the result shows no object.

## Related definitions

- The [g-factor](/g-factor/) is a function of the maps, the noise covariance and the sampling pattern, and measures the noise amplification of SENSE.
- The [root-sum-of-squares coil combination](/root-sum-of-squares-coil-combination/) needs no maps and returns $|x| \lVert s \rVert$ without noise.
- The coil images $m_k$, the maps and the object are linked by $m_k = s_k x$; the encoding operator of [CG-SENSE](/cg-sense/) is $x \mapsto (M F_u(s_k x))_k$.
- [k-space](/k-space/) of a coil image is the k-space of the object convolved with the k-space of the map. Smooth maps have a small k-space support, the basis of [GRAPPA](/grappa/) and [SPIRiT](/spirit/).

## References
