---
tag: 7RKRH0
kind: technique
slug: propeller-mri
name: PROPELLER
aliases:
- BLADE
area: imaging-and-inverse-problems/mri-reconstruction
level: advanced
summary: Acquire k-space in rotated strips that each cover the center, so that rotation and shift between strips can be estimated and corrected.
prereqs: [k-space, k-space-trajectory, density-compensation]
see_also: [image-registration, cross-correlation, phase-correlation, nonuniform-fft, fourier-slice-theorem, mri-reconstruction-problem, sense, fast-fourier-transform]
sources:
  - paper: doi:10.1002/(SICI)1522-2594(199911)42:5<963::AID-MRM17>3.0.CO;2-L
    title: "James G. Pipe, Motion correction with PROPELLER MRI: application to head motion and free-breathing cardiac imaging, Magnetic Resonance in Medicine 42(5), 1999, 963 to 969"
    locator: the strip geometry, the phase correction, the rotation and translation estimates and the correlation weighting (general locator; equation numbers not confirmed)
  - paper: doi:10.1002/mrm.10014
    title: James G. Pipe, Victoria G. Farthing and Kirsten P. Forbes, Multishot diffusion-weighted FSE using PROPELLER MRI, Magnetic Resonance in Medicine 47(1), 2002, 42 to 52
    locator: the use of the per-strip phase correction for diffusion-weighted fast spin echo (general locator)
  - paper: doi:10.1002/(SICI)1522-2594(199901)41:1<179::AID-MRM25>3.0.CO;2-V
    title: James G. Pipe and Padmanabhan Menon, Sampling density compensation in MRI, rationale and an iterative numerical solution, Magnetic Resonance in Medicine 41(1), 1999, 179 to 186
    locator: the density weights used before gridding (general locator)
---

PROPELLER (periodically rotated overlapping parallel lines with enhanced reconstruction) is a way to acquire and reconstruct MR data so that patient motion between shots can be measured from the data and removed. James Pipe published it in 1999. Each shot, usually one echo train of a fast spin echo sequence, acquires a strip of $L$ parallel lines of $n$ samples through the center of [k-space](/k-space/). The next shot acquires the same strip rotated by $\pi/B$, and $B$ shots cover a disk. Every strip contains the central disk of diameter $L$, so every strip gives its own low resolution image of the object. The reconstruction compares these to estimate the in-plane rotation and shift of each strip, corrects the strip data, gives less weight to strips that still disagree, and then grids all samples with [density compensation](/density-compensation/). The price is a scan about $\pi/2$ times as long as a Cartesian scan of the same resolution.

## In plain words

A normal scan collects the image data in many short pieces over a few minutes. If the patient moves between pieces, the pieces do not fit together, and the image has ghosts and blur.

PROPELLER collects each piece as a wide strip through the middle of the data, and turns each new strip by a small angle, like a slowly turning propeller. Because every strip passes through the middle, every strip alone gives a rough picture of the whole object. The method compares the rough pictures to find how far each one has turned and moved. It then turns and moves each strip back before it combines them. Strips that still do not match well, for example because the patient moved out of the slice, count less in the final picture.

## When it applies

- **Multi-shot scans with motion between shots.** Each strip must be acquired fast enough that the object does not move during it. Motion between strips is the target.
- **Rigid in-plane motion.** The correction models a rotation and a shift in the image plane, which fits head motion well. Motion out of the slice and nonrigid motion are not corrected; the correlation weighting only reduces their effect.
- **Enough strip width.** The estimates use the central disk of diameter $L$, so $L$ must give a low resolution image that shows the object.
- **Time for extra lines.** Full coverage needs about $\pi n/2$ lines instead of $n$.

## The template

Notation: strip $b$ holds the samples $y_b(k)$ at the acquired positions $k$, which are the points of an $L \times n$ Cartesian grid with unit spacing (in units of $1/\text{FOV}$), rotated by $\theta_b = (b-1)\pi/B$. $R_\alpha$ is the rotation of the plane by the angle $\alpha$. The central disk is $|k| \le L/2$. If the object is rotated by $\alpha$ about the origin and then shifted by $d$, its transform is $F(R_{-\alpha} k)\, e^{-2\pi i k \cdot d}$, where $F$ is the transform of the object at rest. So the magnitude of the data does not depend on $d$, and the data at the acquired position $k$ are the object at rest at the position $R_{-\alpha} k$, times a phase.

```pseudo id=main
PROPELLER(y_1..y_B, k_1..k_B, L)
L1  for b <- 1 to B do
L2      p_b <- the phase of the low resolution image of strip b (triangle window)
L3      y_b <- the transform of (the image of strip b times conj(p_b))
L4  r <- the reference: the central disk data of all strips, gridded and averaged
L5  for b <- 1 to B do
L6      alpha_b <- argmax over alpha of corr(|y_b(k)|, |r(R_{-alpha} k)|) on the central disk
L7      k'_b <- R_{-alpha_b} k_b                          ▷ corrected positions
L8      d_b <- argmax over d of | sum over the central disk of y_b(k) conj(r(k')) e^{2 pi i k.d} |
L9      y_b <- y_b(k) e^{2 pi i k.d_b} at every acquired k of strip b
L10     c_b <- corr(y_b(k), r(k')) on the central disk
L11 w <- weights from c_1..c_B, small where c_b is small
L12 D <- density compensation weights for the positions k'_1..k'_B
L13 return the inverse FFT of GRID(w D y, k')
```

Line L2 builds the image of strip $b$ from its central part with a triangle window, and line L3 removes its phase, so that phase errors that differ from shot to shot do not corrupt the comparisons. Line L4 builds the reference from all strips; motion of a few strips changes it only a little. Line L6 estimates the rotation from magnitudes, which do not depend on the shift, and it searches over a small range of angles. Line L7 moves each sample to the position it has in the frame of the object at rest. Line L8 is the [cross-correlation](/cross-correlation/) of the strip image with the reference image, computed through k-space, and its peak gives the shift; the phase term uses the acquired positions $k$, not $k'$, because the shift acts on the object after the rotation. Line L9 undoes the shift. Lines L10 and L11 are the correlation weighting. Line L12 is needed because the center is sampled by every strip; Pipe and Menon's iteration is one choice. Line L13 grids onto a Cartesian grid, as in the [nonuniform FFT](/nonuniform-fft/), and applies the [FFT](/fast-fourier-transform/).

**Coverage.** Adjacent strips are $\pi/B$ apart. At the edge of k-space, radius $n/2$, the gap between them is about $(n/2)(\pi/B)$ wide, and the Nyquist condition asks for a gap of at most $L$. So $B \ge \pi n/(2L)$, and the total number of lines is $BL \ge \pi n/2$.

**Cost.** The phase correction, the reference and the estimates cost $O(B\, L n)$ for the data plus the cost of the searches in lines L6 and L8; an FFT on the central disk or a coarse to fine search keeps these small. The final gridding and FFT cost $O(BLn\, q^2 + n^2 \log n)$ for a kernel of width $q$.

## Classic examples

- **Head motion in brain imaging (Pipe 1999).** $T_2$-weighted fast spin echo scans of the brain, with one echo train per strip, where patients turn and shift their heads between shots.
- **Free-breathing cardiac imaging (Pipe 1999).** The same correction applied to heart images acquired without a breath hold.
- **Diffusion-weighted fast spin echo (Pipe, Farthing and Forbes 2002).** Motion during the diffusion gradients gives every shot a random phase. Line L2 removes it, so multi-shot diffusion images become possible without echo planar distortion.
- **A small simulation (measurement, not a bound).** Take $n = 32$ and $L = 8$, so $B = \lceil 6.28 \rceil = 7$ strips and 56 lines, 1.75 times the Cartesian 32. The object is three Gaussian blobs. Strip 4 is acquired after the object turned by $5°$ and moved by $(0.03, -0.02)$ of the field of view. Its central disk holds 48 samples. With the motion-free transform as the reference, the search of line L6 over $\pm 10°$ in steps of $0.1°$ found $5.0°$ (correlation 1.0, against 0.993 at $0°$), and a coarse to fine search for line L8 found the shift $(0.03, -0.02)$. The relative error of the strip data fell from 0.407 before the correction to $1.8 \times 10^{-4}$ after it.

## Variations

- **Strip shape.** Wider strips give better estimates and fewer strips, but each echo train is longer, so $T_2$ decay blurs the strip along its narrow axis. Some designs make the strips long along the phase encoding axis and short along the readout instead.
- **Parallel imaging inside a strip.** Undersampling the lines of a strip and unfolding them with coil sensitivities, as in [SENSE](/sense/), makes a strip wider for the same echo train length.
- **Other sequences.** The strip geometry also works with gradient echo and with mixed gradient and spin echo trains, which shorten the scan.
- **Iterative reconstruction.** Instead of density compensation and gridding, the corrected samples can enter a least squares [MRI reconstruction problem](/mri-reconstruction-problem/) solved with the nonuniform FFT.
- **Radial limit.** With $L = 1$ every strip is one line through the center, the radial trajectory of the [k-space trajectory](/k-space-trajectory/) page. Each line is then the 1D transform of a projection of the object, by the [Fourier slice theorem](/fourier-slice-theorem/). One line is too narrow to estimate a rotation, which is why PROPELLER uses wide strips.
- **Registration in the image domain.** The estimates of lines L6 and L8 are a form of [image registration](/image-registration/); [phase correlation](/phase-correlation/) can replace the plain cross-correlation for the shift.

## Pitfalls

- **Frame of the shift.** The shift acts on the rotated object, so the phase $e^{2\pi i k \cdot d}$ must use the acquired positions. Using the corrected positions gives a shift turned by the rotation angle; in the simulation above it gave $(0.028, -0.023)$ instead of $(0.03, -0.02)$.
- **Order of the estimates.** Estimate the rotation first, from magnitudes, and the shift second. A shift changes the phase of every sample, so a rotation search on complex data would mix the two.
- **Half-turn ambiguity.** For a real object $|F(-k)| = |F(k)|$, so magnitudes cannot tell $\alpha$ from $\alpha + \pi$. Search a small range of angles.
- **No density compensation.** The center is sampled $B$ times. Without weights, the image is blurred by the extra weight at low frequencies.
- **Through-plane motion.** A rotation and a shift in the plane cannot model it. The correlation weighting lowers the weight of such strips but does not correct them.
- **Narrow strips.** For small $L$ the central disk holds few samples, the low resolution images are poor, and the estimates become unreliable.

## Exercises

1. Show that the transform of an object rotated by $\alpha$ about the origin is $F(R_{-\alpha} k)$, and that a shift by $d$ multiplies the transform by $e^{-2\pi i k \cdot d}$. Conclude that the magnitude of the data does not depend on $d$.
2. Show that every strip, the set of points whose distance from a line through the origin is at most $L/2$, contains the disk $|k| \le L/2$.
3. Derive $B \ge \pi n/(2L)$. For $n = 256$ and $L = 16$, find $B$ and the number of lines, and compare with a Cartesian scan.
4. Let $y(k) = F(k) e^{-2\pi i k \cdot d_0}$ on a set of positions $k$. Show that $\bigl|\sum_k y(k)\, \overline{F(k)}\, e^{2\pi i k \cdot d}\bigr|$ is largest at $d = d_0$ among all $d$.
5. Explain why line L4 can use all strips, including the moved ones, and what happens to the reference if half of the strips are moved by the same amount.

## References
