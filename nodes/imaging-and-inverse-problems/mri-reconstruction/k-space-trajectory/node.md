---
tag: Y8C0EG
kind: concept
slug: k-space-trajectory
name: k-space trajectory
aliases:
- radial and spiral sampling
area: imaging-and-inverse-problems/mri-reconstruction
level: core
summary: The path of the sampled spatial frequencies k(t) during a scan, set by the gradient waveforms. Cartesian lines, echo planar, radial and spiral paths differ in speed, reconstruction and artifacts.
prereqs: [k-space]
see_also: [density-compensation, nonuniform-fft, conjugate-phase-reconstruction, propeller-mri, variable-density-sampling, fourier-slice-theorem, aliasing, mri-signal-equation]
sources:
  - book: isbn:9780120928613
    title: Matt A. Bernstein, Kevin F. King and Xiaohong Joe Zhou, Handbook of MRI Pulse Sequences, Elsevier Academic Press, 2004
    locator: Section 16.1, Echo Planar Imaging; Section 17.5, Projection Acquisition; Section 17.6, Spiral
  - paper: doi:10.1088/0022-3719/10/3/004
    title: Peter Mansfield, Multi-planar image formation using NMR spin echoes, Journal of Physics C, Solid State Physics 10(3), 1977, L55 to L58
    locator: the echo planar principle, many lines of the image from one excitation (general locator)
  - paper: doi:10.1002/mrm.1910280204
    title: Craig H. Meyer, Bob S. Hu, Dwight G. Nishimura and Albert Macovski, Fast spiral coronary artery imaging, Magnetic Resonance in Medicine 28(2), 1992, 202 to 213
    locator: interleaved spiral trajectories and their reconstruction (general locator)
  - paper: doi:10.1002/mrm.1910280209
    title: Gary H. Glover and John M. Pauly, Projection reconstruction techniques for reduction of motion effects in MRI, Magnetic Resonance in Medicine 28(2), 1992, 275 to 289
    locator: radial (projection) acquisition and its behavior under motion (general locator)
---

A k-space trajectory is the path $k(t) = \bar\gamma \int_0^t G(\tau)\, d\tau$ that the sample point follows through [k-space](/k-space/) during a scan, together with the times at which samples are taken. The gradient waveforms $G(t)$ set it, within the limits of the hardware on gradient strength and slew rate. The common paths are Cartesian lines, echo planar zigzags, radial spokes and spirals. The choice decides how fast the scan is, how the image is reconstructed and which artifacts appear. Cartesian data need only an FFT; the other paths need gridding or a [nonuniform FFT](/nonuniform-fft/) with [density compensation](/density-compensation/).

## In plain words

An MRI scan collects its measurements one after another while the magnetic gradients steer a point across a map of frequencies. The path of that point is the trajectory. The scanner can steer only so fast and turn only so sharply.

Some paths go line by line, like reading a page. Some zigzag across the whole map after one start, which is fast but sensitive to small field errors. Some go out from the center like the spokes of a wheel, and some spiral outward. Paths that visit the center often cope better with motion, but the computer needs more work to make the picture, because the points do not sit on a square grid.

## The idea

**The hardware limits.** The speed of the point is $|\dot k| = \bar\gamma |G| \le \bar\gamma G_{\max}$, and its acceleration is $|\ddot k| = \bar\gamma |\dot G| \le \bar\gamma S_{\max}$, with the largest gradient $G_{\max}$ (tens of mT/m) and the largest slew rate $S_{\max}$ (about 100 to 200 T/m/s on clinical scanners). Peripheral nerve stimulation can set a lower practical limit on the slew rate.

**The sampling rule.** To reconstruct a field of view $L$ without folding, neighbouring samples must be at most $1/L$ apart, in the sense of the [sampling theorem](/sampling-theorem/). To get the pixel size $\delta$, the samples must reach $k_{\max} = 1/(2\delta)$.

**The common paths.**

| trajectory | path | per excitation | reconstruction | typical weakness |
|---|---|---|---|---|
| Cartesian | one line per repetition | one line | FFT | slow |
| echo planar (EPI) | all lines in a zigzag | many or all lines | FFT after reordering | distortion from field errors, ghosts |
| radial | spokes through the center | one or more spokes | gridding or NUFFT | streaks when undersampled |
| spiral | outward spirals, often interleaved | one interleaf | gridding or NUFFT | blur from field errors |
| PROPELLER | rotated strips of lines | one strip | gridding after motion correction | longer scan |

**Time along the path matters.** The signal equation holds at each sample time. Relaxation and field errors act through time, so their effect follows the order in which k-space is visited. In EPI the time between lines is long, so a field error shifts the image along the phase encoding axis. In a spiral, time grows with the radius, so a field error blurs the image in all directions.

**Radial sampling.** By the [Fourier slice theorem](/fourier-slice-theorem/), each spoke is the 1D Fourier transform of a projection of the image. With $n$ samples per spoke over the diameter, the spacing between spokes at the edge is $\pi k_{\max} / N$ for $N$ spokes over 180 degrees. Setting it to $1/L$ gives $N = \pi n / 2$ spokes, about 1.57 times the number of lines of a Cartesian scan. Fewer spokes give streaks, not folds, which is why radial undersampling degrades gently.

**Spiral sampling.** An Archimedean spiral with $N_i$ interleaves has $k(\theta) = N_i \theta / (2\pi L)$ in polar form, so neighbouring turns of all interleaves are $1/L$ apart. Each interleaf makes $k_{\max} L / N_i = n/(2 N_i)$ turns.

## Examples

- **Radial count.** For a $256 \times 256$ image, full sampling needs $\pi \cdot 256 / 2 = 402$ spokes, against 256 Cartesian lines.
- **Spiral count.** For the same matrix with 16 interleaves, each interleaf makes $256 / 32 = 8$ turns.
- **EPI shift.** With 64 phase encoding lines and an echo spacing of 0.5 ms, the lines span 32 ms, so the bandwidth along the phase encoding axis is $1/(64 \cdot 0.5\ \text{ms}) = 31.25$ Hz per pixel. A region that is 100 Hz off resonance moves by $100/31.25 = 3.2$ pixels along that axis. Along the readout axis, with a bandwidth of about 1 kHz per pixel or more, the shift is below a tenth of a pixel.
- **Gradient for a Cartesian readout.** A field of view of 256 mm with a dwell time of 4 microseconds needs a readout gradient of 22.9 mT/m (see the [signal equation](/mri-signal-equation/) page).

## Where it is used

- **Fast imaging.** EPI acquires a whole slice from one excitation, the basis of functional and diffusion MRI.
- **Cardiac and abdominal imaging.** Radial and spiral paths visit the center of k-space often and tolerate motion and flow better.
- **Short echo times.** Center-out radial and spiral paths start sampling right after excitation, for tissues with short $T_2$.
- **Undersampled reconstruction.** Radial and random paths give incoherent artifacts, which suits [compressed sensing MRI](/compressed-sensing-mri/); [variable density sampling](/variable-density-sampling/) chooses the density.
- **Motion correction.** [PROPELLER](/propeller-mri/) uses strips that all cover the center.
- **Off-resonance correction.** Non-Cartesian data with a field map need [conjugate phase reconstruction](/conjugate-phase-reconstruction/) or an iterative solver.

## References
