---
tag: D7EB05
kind: algorithm
slug: phase-correlation
name: Phase correlation
aliases:
- Fourier shift estimation
area: graphics-and-signals/image-processing
level: advanced
summary: Find the shift between two images from the peak of the inverse DFT of their cross-power spectrum, with each frequency scaled to unit magnitude.
solves: [image-registration]
model: real-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels}
  time: {worst: O(W H log(W H)), average: O(W H log(W H)), best: O(W H log(W H))}
  space: {extra: Θ(W H)}
properties: {deterministic: true, exact_for_circular_shifts: true, invariant_to_gain_and_offset: true, heuristic: false}
history:
  year: 1975
  people: [C. D. Kuglin, D. C. Hines]
  note: Kuglin and Hines presented the method at the 1975 IEEE conference on cybernetics and society. Reddy and Chatterji (1996) added rotation and scale with log-polar coordinates, and Foroosh, Zerubia and Berthod (2002) gave a subpixel estimate.
prereqs: [discrete-fourier-transform, fast-fourier-transform, convolution-theorem]
see_also: [normalized-cross-correlation, cross-correlation, template-matching, multidimensional-fft, circular-convolution, optical-flow, lucas-kanade-method]
sources:
  - paper: "C. D. Kuglin and D. C. Hines, The phase correlation image alignment method, Proceedings of the IEEE 1975 International Conference on Cybernetics and Society, San Francisco, 163-165, 1975"
    title: C. D. Kuglin and D. C. Hines, The phase correlation image alignment method, 1975
    locator: pages 163-165, the whole paper
  - paper: doi:10.1109/83.988953
    title: H. Foroosh, J. B. Zerubia and M. Berthod, Extension of phase correlation to subpixel registration, IEEE Transactions on Image Processing 11(3), 2002
    locator: the whole paper (the surface of a subpixel shift and the estimate from the peak and its neighbours)
  - paper: doi:10.1109/83.506761
    title: B. S. Reddy and B. N. Chatterji, An FFT-based technique for translation, rotation, and scale-invariant image registration, IEEE Transactions on Image Processing 5(8), 1996
    locator: the whole paper (log-polar resampling of the Fourier magnitude)
  - paper: doi:10.1016/S0262-8856(03)00137-9
    title: B. Zitová and J. Flusser, Image registration methods, a survey, Image and Vision Computing 21(11), 2003
    locator: the part on area-based methods, Fourier methods
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 9, Motion estimation (translational alignment, Fourier-based alignment)
---

Phase correlation finds the translation between two images of the same size. It takes the [2D DFT](/discrete-fourier-transform/) of both images, multiplies one by the complex conjugate of the other, and scales each frequency of this cross-power spectrum to magnitude 1. Only the phase differences are left, and by the shift theorem they are the phases of a pure translation. The inverse DFT of the result is then a single peak at the shift. For an exact circular shift and a spectrum without zero bins the peak is a unit impulse: it is $1$ at the shift and $0$ at every other pixel. With the [FFT](/fast-fourier-transform/) the cost is $O(WH\log(WH))$ for a $W \times H$ image. Kuglin and Hines described the method in 1975. It does not need a template, it finds large shifts as fast as small ones, and a brightness change $af + b$ with $a > 0$ does not move the peak. It finds only one global translation; rotation and scale need an extra step.

## In plain words

You have two photos of the same scene, and the second one is moved sideways and up or down. You want to know by how much. Phase correlation describes each photo as a sum of waves of different sizes and directions. Moving a photo does not change how strong each wave is. It only slides each wave by an amount that depends on the move. The method throws away the strength of every wave and keeps only how far it slid, then puts the waves back together. All the waves then line up at one point, which is the move. The result looks like a black picture with one bright dot, and the place of the dot is the answer.

## The problem

The input is two gray [digital images](/digital-image/) $f$ and $g$ with $W$ columns and $H$ rows, one real channel each. Pixel $(x, y)$ has its center at the integer point $(x, y)$, with $x$ to the right and $y$ down. The values can be linear or gamma encoded; the method uses them as they are, and the result does not change under $af + b$ with $a > 0$ as long as the mean stays positive (see Properties). The border rule is circular: index $x$ is taken mod $W$ and $y$ mod $H$, which is the model the DFT assumes. The ideal input is a circular shift, $g(x, y) = f((x - d_x) \bmod W, (y - d_y) \bmod H)$, and the output is $(d_x, d_y)$, read in $(-W/2, W/2] \times (-H/2, H/2]$. Real image pairs are not circular shifts: content enters at one side and leaves at the other. On them the method returns the highest peak, and how well that peak gives the true shift depends on the overlap and the content, which is an observed property and not a bound.

The DFT is $\hat f(k, l) = \sum_{y,x} f(x, y) \, e^{-2\pi i (kx/W + ly/H)}$ for $0 \le k < W$ and $0 \le l < H$. The shift theorem gives $\hat g(k, l) = \hat f(k, l) \, e^{-2\pi i (k d_x/W + l d_y/H)}$.

## The algorithm

```pseudo id=main
PHASE-CORRELATION(f, g)                             ▷ f and g are W × H
L1  F ← DFT2(f);  G ← DFT2(g)
L2  for each frequency (k, l) with 0 ≤ k < W and 0 ≤ l < H do
L3      P ← G[l][k] · conj(F[l][k])
L4      R[l][k] ← P / |P| if |P| > ε · max |P|, else 0
L5  r ← the real part of IDFT2(R)
L6  (dx, dy) ← the first (x, y) in row-major order with the largest r[y][x]
L7  peak ← r[dy][dx]
L8  if dx > ⌊W/2⌋ then dx ← dx − W
L9  if dy > ⌊H/2⌋ then dy ← dy − H
    return (dx, dy, peak)
```

Line L1 computes the two spectra with the [2D FFT](/multidimensional-fft/), rows first and then columns. Lines L2 to L4 form the normalized cross-power spectrum. A bin with $|P| = 0$ has no phase, so line L4 sets it to $0$; the relative threshold $\varepsilon$ (for example $10^{-12}$) also treats bins that are zero up to rounding in the same way. Line L5 takes the inverse DFT with the factor $1/(WH)$. Its imaginary part is zero up to rounding, because $R(-k, -l) = \overline{R(k, l)}$ for real images. Line L6 finds the peak, and lines L8 and L9 map the index to the shift of smallest size, because a shift of $W - 1$ and a shift of $-1$ are the same circular shift.

The order of the factors at line L3 fixes the sign. With $G \cdot \overline{F}$ the peak is at the shift that takes $f$ to $g$; with $F \cdot \overline{G}$ it is at the opposite shift.

## Example

Take $W = 4$, $H = 3$ and the image $f$ below. Move it by $(d_x, d_y) = (1, 2)$ with wrap around; this gives $g$. Row $y = 0$ is on top.

| $f$ | $x = 0$ | 1 | 2 | 3 | | $g$ | $x = 0$ | 1 | 2 | 3 |
|---|---|---|---|---|---|---|---|---|---|---|
| $y = 0$ | 1 | 2 | 0 | 0 | | $y = 0$ | 1 | 0 | 3 | 0 |
| $y = 1$ | 0 | 3 | 0 | 1 | | $y = 1$ | 0 | 4 | 0 | 0 |
| $y = 2$ | 4 | 0 | 0 | 0 | | $y = 2$ | 0 | 1 | 2 | 0 |

For example $g(1, 1) = f(0, (1 - 2) \bmod 3) = f(0, 2) = 4$. The DC term of both spectra is the pixel sum, $\hat f(0, 0) = \hat g(0, 0) = 11$. No bin of $\hat f$ is zero, so all twelve bins of $R$ have magnitude $1$. The inverse DFT $r$ is $1$ at $(1, 2)$ and $0$ at the other eleven pixels, up to rounding of order $10^{-15}$. Line L6 returns the index $(1, 2)$ with peak $1$. Lines L8 and L9 change $d_y = 2 > \lfloor 3/2 \rfloor = 1$ to $2 - 3 = -1$: moving down by two rows of three is the same as moving up by one.

Compare the plain circular [cross-correlation](/cross-correlation/) $c(u, v) = \sum_{y,x} g(x, y) f((x - u) \bmod W, (y - v) \bmod H)$, which is the same computation without the normalization at line L4:

| $c$ | $u = 0$ | 1 | 2 | 3 |
|---|---|---|---|---|
| $v = 0$ | 13 | 10 | 15 | 2 |
| $v = 1$ | 15 | 10 | 13 | 2 |
| $v = 2$ | 2 | 31 | 2 | 6 |

It also has its maximum at $(1, 2)$, where it is $\sum f^2 = 31$, but the next value is $15$, about half of the peak. On a smooth natural image, where most of the energy is at low frequencies, the plain correlation peak is wide and flat. Phase correlation gives every frequency the same weight, which makes the peak one pixel wide.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). For a circular shift the shift theorem gives $P(k, l) = |\hat f(k, l)|^2 e^{-2\pi i (k d_x/W + l d_y/H)}$, so on every bin where $\hat f \ne 0$ the normalized value is the pure phase $e^{-2\pi i (k d_x/W + l d_y/H)}$. If no bin is zero, the inverse DFT of this phase is the unit impulse at $(d_x, d_y)$ by the orthogonality of the [roots of unity](/roots-of-unity/). If a set $Z$ of $z$ bins is zero, the surface is the impulse minus $1/(WH)$ times a sum of $z$ unit terms: the value at the shift is $1 - z/(WH)$ and every other value has magnitude at most $z/(WH)$. So the peak is unique at the shift whenever $z < WH/2$. With $z \ge WH/2$ the shift can be not observable from the data; the tests show an image whose rows are all the same, where every vertical shift gives the same surface.

## Complexity

- Line L1 and line L5 are three 2D DFTs. With a radix-2 FFT, for $W$ and $H$ powers of two, each costs $\Theta(WH \log(WH))$: $H$ transforms of length $W$ and $W$ of length $H$.
- Lines L2 to L4 and lines L6 to L9 cost $\Theta(WH)$.
- The total is $\Theta(WH\log(WH))$ in the worst case, the same on every input. The extra space is $\Theta(WH)$ for the spectra and the surface.

For other sizes an FFT for any length (mixed radix, or a chirp transform) keeps the $O(WH \log(WH))$ bound. The implementation here falls back to the direct DFT on each row and column of a length that is not a power of two, which costs $\Theta(WH(W + H))$. Padding with zeros to a power of two is not a good way to reach the fast case here: it changes the circular model, and the shift is then no longer a circular shift of the padded images.

The cost does not depend on the size of the shift. A direct search over all shifts by [NCC](/normalized-cross-correlation/) on the whole image costs $\Theta(W^2H^2)$.

## Properties

- **Exact for circular shifts.** In exact arithmetic the surface is the unit impulse when no bin is zero, and the peak is $1 - z/(WH)$ with $z$ zero bins.
- **Gain and offset.** If $g$ is replaced by $ag + b$ with $a > 0$, every bin except $(0, 0)$ is multiplied by $a$, which the normalization removes. Bin $(0, 0)$ changes by a real amount, so its normalized value stays $1$ while $\hat f(0, 0)$ and $\hat g(0, 0)$ have the same sign, which holds when both means are positive. The surface then does not change at all.
- **Every frequency counts the same.** This makes the peak sharp. It also makes noise at high frequencies, where the signal is weak, count as much as the signal.
- **One translation only.** The method models one global translation. A rotation, a change of scale, or a scene with parts that move differently gives a lower peak or several peaks.
- **Several motions.** When two layers move by different amounts, the surface has a peak for each. This is a property that some motion estimators use on purpose.
- **Integer shifts.** The peak is at an integer pixel. A subpixel shift spreads the peak over the neighbours (see Variants).

## Variants and improvements

- **Subpixel shift.** Foroosh, Zerubia and Berthod (2002) show that for a subpixel shift of a band limited image the surface is close to a sampled Dirichlet kernel, and they estimate the fractional part from the peak and its largest neighbour on each axis. A simpler approach fits a parabola through the peak and its two neighbours on each axis; that is a heuristic.
- **Rotation and scale.** The magnitude $|\hat f|$ does not depend on the shift. A rotation of the image rotates the magnitude spectrum, and a change of scale scales it by the inverse factor. Reddy and Chatterji (1996) resample the magnitude in log-polar coordinates, where both become translations, and find them with phase correlation. They then undo the rotation and scale and find the translation in a second pass.
- **Window first.** Multiply both images by a window that goes smoothly to zero at the border, such as the Hann window, before line L1. Real images are not periodic, and the jump at the border puts strong lines along the axes of the spectrum. The window reduces this effect, but it also gives less weight to the content near the border.
- **Weighted spectrum.** Use $P / (|P| + c)$ for a constant $c > 0$, or set the bins above a frequency limit to zero. This trades sharpness of the peak for less noise.
- **Local phase correlation.** Run the method on tiles to get one shift for each tile, which gives a coarse motion field like [optical flow](/optical-flow/).

## When to use it

Use phase correlation to align two images that differ mainly by a translation: frames of a video for stabilization, tiles of a microscope or scanner mosaic, satellite images of the same area, or the first coarse step of [image registration](/image-registration/) before a finer method such as [Lucas-Kanade](/lucas-kanade-method/). It is a good choice when the shift can be large, when the brightness changes by a gain and offset, and when the cost must be the same for every shift. Do not use it to find a small template in a large image; that is [template matching](/template-matching/), and NCC is the usual tool. When the images also differ by a large rotation, a change of view or a non-rigid change, match features such as [SIFT](/sift/) instead.

## Pitfalls

- **Sign.** $G \cdot \overline{F}$ and $F \cdot \overline{G}$ give opposite shifts. Test with a known shift once.
- **Wrap of the index.** The peak index is the shift mod $W$ and mod $H$. A shift of more than half the size is reported as a negative shift. With non-circular images the method cannot tell a shift of $d_x$ from a shift of $d_x - W$.
- **Division by zero.** A bin with $P = 0$ has no phase. Set it to $0$ as at line L4, or add a small constant. Dividing by a tiny $|P|$ turns rounding noise into a full unit term.
- **Border effects.** Without a window, the border jump of a non-periodic image can give a peak at $(0, 0)$ that is stronger than the true one.
- **Small overlap.** When the shift is a large part of the image, little content is common to both, and the peak can drop below the noise. The height of the peak is a useful measure of trust.
- **Not the same as the plain correlation.** Leaving out the division at line L4 gives the cross-correlation, whose peak is wide on natural images, as the example shows on a small scale.
- **Mean sign.** The invariance to $ag + b$ needs the image means to keep the same sign. An image of zero mean has $\hat f(0, 0) = 0$, and the DC bin is then a zero bin.

## Implementations

## History

C. D. Kuglin and D. C. Hines presented phase correlation at the 1975 IEEE International Conference on Cybernetics and Society in San Francisco, as a method to align images in the Fourier domain. The FFT of Cooley and Tukey, ten years older, made it fast. Later work extended the shift model. B. S. Reddy and B. N. Chatterji (1996) found rotation and scale with log-polar resampling of the Fourier magnitude. H. Foroosh, J. B. Zerubia and M. Berthod (2002) gave a closed form for the subpixel part of the shift. The method is now a standard tool for video stabilization, mosaics and the alignment of remote sensing images.

## References
