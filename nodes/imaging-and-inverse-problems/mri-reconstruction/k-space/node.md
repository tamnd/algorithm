---
tag: 0GZN94
kind: concept
slug: k-space
name: k-space
aliases:
- MRI Fourier domain
area: imaging-and-inverse-problems/mri-reconstruction
level: intro
summary: The spatial frequency domain in which MRI samples the image. The gradients move the sample point k(t) over time, and the spacing and extent of the samples set the field of view and the resolution.
prereqs: [mri-signal-equation]
see_also: [k-space-trajectory, partial-fourier-reconstruction, mri-reconstruction-problem, discrete-fourier-transform, aliasing, sampling-theorem, variable-density-sampling, sense]
sources:
  - paper: doi:10.1016/0022-2364(83)90060-4
    title: Stig Ljunggren, A simple graphical representation of Fourier-based imaging methods, Journal of Magnetic Resonance 54(2), 1983, 338 to 343
    locator: the graphical representation of imaging sequences as paths in the Fourier domain (general locator)
  - paper: doi:10.1118/1.595331
    title: Donald B. Twieg, The k-trajectory formulation of the NMR imaging process with applications in analysis and synthesis of imaging methods, Medical Physics 10(5), 1983, 610 to 621
    locator: the k-trajectory formulation (general locator)
  - book: isbn:9780780347236
    title: Zhi-Pei Liang and Paul C. Lauterbur, Principles of Magnetic Resonance Imaging, A Signal Processing Perspective, IEEE Press, 2000
    locator: the chapter on signal localization (the k-space interpretation of frequency and phase encoding; chapter number not confirmed)
---

k-space is the domain of spatial frequencies in which an MRI scanner takes its measurements. By the [MRI signal equation](/mri-signal-equation/), the signal at time $t$ is the Fourier transform of the image at the point $k(t) = \bar\gamma \int_0^t G(\tau)\, d\tau$, and the gradients move that point. A scan is a path through k-space, and the image is the inverse Fourier transform of the samples taken along it. Ljunggren and Twieg introduced the picture in 1983. The spacing of the samples sets the field of view, their extent sets the resolution, and the path, the [k-space trajectory](/k-space-trajectory/), sets the speed and the artifacts.

## In plain words

Any picture can be built by adding stripe patterns of different widths and directions, each with its own strength. k-space is the list of all those strengths, laid out on a plane: the middle holds the wide, gentle stripes, and the edges hold the fine ones.

An MRI scanner does not take a photo of the body. It measures the strengths of the stripe patterns one at a time, and the magnetic gradients choose which pattern comes next. The middle of the list gives the overall brightness and contrast of the picture. The edges give the sharp details. A computer adds the patterns up to make the picture.

## The idea

**Position in k-space.** A gradient $G$ makes the precession frequency depend on position, so after a time $t$ the spins at $r$ have the extra phase $-2\pi k(t) \cdot r$, with $k(t) = \bar\gamma \int_0^t G$. The coil signal is then $s(t) = \int c\, m\, e^{-2\pi i k(t) \cdot r} dr$, the Fourier transform of $c\, m$ at $k(t)$. The unit of $k$ is cycles per meter.

**Moving through k-space.**

- A gradient on for a time moves $k$ along a straight line, at the speed $\bar\gamma G$.
- A short gradient pulse before the readout moves $k$ to a starting point; this is phase encoding.
- A gradient during the readout moves $k$ along a line while samples are taken; this is frequency encoding.
- A 180 degree refocusing pulse reflects the point: $k \to -k$.
- An echo is the time when $k$ comes back to the center.

**Sampling rules.** On a Cartesian grid with spacing $\Delta k$ and $n$ samples per axis:

- The image repeats with the period $1/\Delta k$, so the field of view is $L = 1/\Delta k$. If the object is larger, it folds over (aliasing).
- The pixel size is $1/(n \Delta k) = L/n$. The image is the inverse DFT of the samples; this area uses the unitary DFT $F_u = n^{-1/2} F$.
- Keeping every $R$-th line shrinks the field of view by $R$, and the image folds $R$ times; this is a theorem on the [signal equation](/mri-signal-equation/) page.

**What each region holds.** The center holds the low spatial frequencies, which carry most of the energy and the contrast. The outer part holds the edges and fine detail. Each sample affects every pixel, so one bad sample causes a stripe pattern over the whole image.

**Symmetry.** If the image is real, $s(-k) = \overline{s(k)}$, so half of k-space is enough. Real MR images have a phase, and [partial Fourier reconstruction](/partial-fourier-reconstruction/) uses the symmetry together with a model of that phase.

## Examples

- **Field of view and resolution.** For a field of view of 256 mm and a $256 \times 256$ matrix, $\Delta k = 3.906$ cycles per meter, the samples reach $k_{\max} = 500$ cycles per meter, and the pixels are 1 mm.
- **A small 1D check.** The image $x = [0, 0, 1, 1, 1, 1, 0, 0]$ with $n = 8$ has the unitary DFT value $X(0) = 4/\sqrt{8} = 1.414$ at the center, $\sqrt{8}$ times the mean of $x$. Its value at the highest frequency $f = -4$ is $(1 - 1 + 1 - 1)/\sqrt{8} = 0$.
- **Center and edge.** An image made from the central $32 \times 32$ samples of a $256 \times 256$ scan keeps the contrast and loses the detail; an image made from the rest shows only edges. Keyhole and view sharing methods reuse the outer part of k-space between frames for this reason.
- **A spike.** One corrupted sample at $k_0$ adds a plane wave $e^{2\pi i k_0 \cdot r}$ to the whole image, seen as a pattern of stripes.
- **Folding.** A scan with every second phase encoding line removed shows the object and a copy shifted by half the field of view, overlapped. [SENSE](/sense/) undoes this fold with the coil sensitivities.

## Where it is used

- **Sequence design.** Every pulse sequence is drawn as a path in k-space; the [k-space trajectory](/k-space-trajectory/) page lists the common ones.
- **Reconstruction.** Cartesian data need an inverse FFT; non-Cartesian data need gridding or the [nonuniform FFT](/nonuniform-fft/) with [density compensation](/density-compensation/).
- **Faster scans.** Partial Fourier skips part of k-space; parallel imaging and [compressed sensing MRI](/compressed-sensing-mri/) skip lines spread over k-space, often with [variable density sampling](/variable-density-sampling/) that keeps the center.
- **Motion correction.** [PROPELLER](/propeller-mri/) samples the center many times and compares the copies.
- **Artifacts.** Stripes, ghosts and folds are explained by errors at points or lines of k-space.

## References
