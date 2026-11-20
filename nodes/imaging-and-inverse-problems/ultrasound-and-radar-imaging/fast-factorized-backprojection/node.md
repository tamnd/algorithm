---
tag: NKKE4Y
kind: algorithm
slug: fast-factorized-backprojection
name: Fast factorized backprojection
aliases:
- FFBP
area: imaging-and-inverse-problems/ultrasound-and-radar-imaging
level: advanced
summary: "Speed up SAR backprojection of N pulses to an N x N image from O(N^3) to O(N^2 log N) by merging subaperture images on polar grids of growing angular resolution."
solves: [sar-image-formation]
model: real-ram
complexity:
  vars: {N: the number of pulses and the number of pixels along one side of the image}
  time: {worst: O(N^2 log N)}
  space: {extra: O(N^2), data: O(N^2)}
properties: {deterministic: true, linear_in_data: true, recursive: false, exact: false}
history:
  year: 2003
  people: [Lars M. H. Ulander, Hans Hellsten, Gunnar Stenstrom]
  note: "Ulander, Hellsten and Stenstrom described fast factorized backprojection in 2003, for the low-frequency airborne systems with wide apertures for which frequency-domain algorithms are not accurate."
prereqs: [sar-backprojection]
see_also: [sar-image-formation, fast-fourier-transform, polar-format-algorithm, omega-k-algorithm, bilinear-interpolation, back-projection-operator, filtered-back-projection, sampling-theorem]
sources:
  - paper: doi:10.1109/TAES.2003.1238734
    title: "Lars M. H. Ulander, Hans Hellsten and Gunnar Stenstrom, Synthetic-aperture radar processing using fast factorized back-projection, IEEE Transactions on Aerospace and Electronic Systems 39(3), 2003, 760 to 776"
    locator: "the factorization of the backprojection sum over subapertures, the polar subimages and their sampling, and the O(N^2 log N) cost (general locator)"
  - paper: doi:10.1109/83.199920
    title: "Mita D. Desai and W. Kenneth Jenkins, Convolution backprojection image reconstruction for spotlight mode synthetic aperture radar, IEEE Transactions on Image Processing 1(4), 1992, 505 to 517"
    locator: "the direct backprojection of O(N^3) cost that the fast algorithm replaces (general locator)"
---

Fast factorized backprojection (FFBP) computes nearly the same image as [time-domain backprojection](/sar-backprojection/) for [synthetic aperture radar](/synthetic-aperture-radar/), at a much lower cost. Direct backprojection adds every pulse to every pixel, which for $N$ pulses and an $N \times N$ image costs $O(N^3)$. FFBP splits the aperture into short subapertures and first forms an image for each, on a polar grid centered on the subaperture. A short subaperture has a wide beam and so a coarse resolution in angle, and its image needs only a few angle samples. Pairs of neighboring subimages are then merged into the images of subapertures twice as long, which need twice as many angle samples, and so on. Each stage costs about $N^2$, there are about $\log_2 N$ stages, and the total is $O(N^2 \log N)$. The only approximation is the interpolation from one polar grid to the next.

## In plain words

Adding every echo to every point of a large picture takes a long time. But a few echoes recorded close together cannot tell directions apart well, so their sum only changes slowly from one direction to the next. You can store that sum at a few directions only. Merge two such neighbor sums into one: the result can tell directions apart twice as well, so you store it at twice as many directions. Keep merging until one sum covers the whole flight. Each round of merging takes about as much work as one pass over the picture, and there are only a few rounds.

## The problem

The input is as for [backprojection](/sar-backprojection/): $P$ range compressed pulses $d_p$ sampled at the delays $t_0 + j/f_s$, the antenna positions $(x_p, 0)$ on a straight track with an even spacing $\Delta x$, the carrier frequency $f_0$ with the wavelength $\lambda = c/f_0$, and the pixels $q$ in the half plane $y > 0$. The output is an approximation of the backprojection image
$$I(q) = \sum_{p} d_p\big(2R_p(q)/c\big)\, e^{+i 4\pi f_0 R_p(q)/c}, \qquad R_p(q) = |q - (x_p, 0)|.$$
The Fourier sign is $e^{-i 2\pi f t}$, as for the DFT; radar books often use $e^{+j\omega t}$ and so the opposite signs.

## The algorithm

A subaperture $s$ is a set of neighboring pulses with the center $(x_s, 0)$ and the length $l_s$. Its subimage is stored in the polar coordinates $(r, \beta)$ about the center, with $r$ the range and $\beta = (x - x_s)/r$ the direction cosine; the point $(r, \beta)$ is $(x_s + r\beta,\ r\sqrt{1 - \beta^2})$. The stored value is
$$J_s(r, \beta) = \sum_{p \in s} d_p\big(2R_p/c\big)\, e^{+i 4\pi f_0 (R_p - r)/c},$$
where $R_p$ is the range from pulse $p$ to that point. The factor $e^{-i 4\pi f_0 r/c}$ removes the fast phase in $r$ and leaves a function that is smooth in $\beta$, sampled with the step $\Delta\beta_s = \lambda/(O\, l_s)$ for an oversampling factor $O$.

```pseudo id=main
FFBP(d, x, pixels, f_0, f_s, t_0, F, O)    ▷ d[p]: range compressed pulses on an even straight track
L1  for every pulse p: e_p ← UPSAMPLE(d[p], F)                   ▷ zero padding of the DFT
L2      J_p(r) ← e_p read at the range r, on a range grid covering the scene    ▷ one pulse: no β dependence
L3  while more than n_final subapertures remain:                  ▷ merge neighbors in pairs
L4      for each pair (a, b): polar grid of the merged s with Δβ_s = λ / (O l_s) covering the scene
L5          for each grid point q of s, at (r, β), and each child h in {a, b}: r_h ← |q - (x_h, 0)|
L6              v_h ← J_h(r_h, (q_x - x_h) / r_h)                         ▷ bilinear interpolation
L7          J_s(r, β) ← Σ_h v_h e^{+i 4π f_0 (r_h - r) / c}
L8      replace the subapertures by the merged ones
L9  I(q) ← Σ_s J_s(|q - (x_s, 0)|, β_s(q)) e^{+i 4π f_0 |q - (x_s, 0)| / c} for every pixel q
```

Line L1 upsamples each pulse, as in direct backprojection. In L2 a single pulse is its own subaperture and its subimage depends on the range only, because $R_p = r$. Lines L3 to L8 are the merging stages: L4 sets up the polar grid of the merged subaperture, with a $\beta$ step half that of its children; L5 and L6 read each child at the point; and L7 moves each child value from the phase reference of its center to the new center. Line L9 reads the last few subimages at every pixel and adds them; the test uses $n_{\text{final}} = 4$. The implementation needs $P$ to be $n_{\text{final}}$ times a power of 2, and merges in pairs; larger factors per stage, such as 4 or 8, are common too.

## Example

The test uses the setup of the backprojection page: $f_0 = 300$ MHz ($\lambda = 1$ m), $B = 100$ MHz, $f_s = 120$ MHz, $P = 64$ pulses at 1.25 m spacing, targets of amplitude 1, 0.5 and 0.7 near the range of 400 m, and a $17 \times 17$ image of 0.625 m pixels, with the upsampling factor $F = 8$.

| oversampling $O$ | 4 | 8 | 16 | 32 |
|---|---|---|---|---|
| largest difference from direct backprojection, in units of its peak | 0.183 | 0.065 | 0.025 | 0.015 |

With $O = 16$, the three targets give 0.992, 0.506 and 0.693 of 64 at their pixels. The error falls by nearly 3 for each doubling of $O$ up to 16, as for the linear interpolation in $\beta$, whose error falls with the square of the step.

The work of FFBP and of direct backprojection can be counted from the grid sizes alone. For $P$ pulses and an $n \times n$ image with $n = P/4$, the ratio of the direct cost $P n^2$ to the number of interpolations of FFBP is 0.22, 0.79, 2.89, 10.55 and 38.78 for $P = 64$, 256, 1024, 4096 and 16384. The ratio grows by a factor of about 3.7 for each factor of 4 in $P$, a little faster than the ratio $P / \log P$ of the two cost bounds, because fixed overheads matter less at larger sizes. At small sizes FFBP is slower, and at large sizes it is much faster. All values in this section are measurements.

## Correctness

Before interpolation the algorithm is exact. If $J_a$ and $J_b$ are read exactly at the point $q$, then $J_a e^{+i 4\pi f_0 r_a/c} + J_b e^{+i 4\pi f_0 r_b/c}$ is the backprojection sum of the pulses of $a$ and $b$ at $q$, so L7 gives $J_s$ at $q$ exactly, and L9 gives $I(q)$ exactly. The approximation is the interpolation of L6 and L9. Under the far-field approximation, the phase of a term of $J_s$ varies in $\beta$ at a rate of at most $2\pi l_s/\lambda$, so $J_s$ is band-limited in $\beta$ with a Nyquist step of $\lambda/(2 l_s)$; a step of $\lambda/(O\, l_s)$ with $O > 2$ oversamples it. The proofs are in proofs/correctness.md.

## Complexity

Take $P = \Theta(N)$ pulses and an $N \times N$ image. A subimage of length $l_s$ needs $O(N)$ range samples and $O(l_s / l_{\text{full}} \cdot N)$ angle samples to cover the scene, so all subimages of one stage hold $O(N^2)$ samples together, and each costs $O(1)$ to compute. There are $\log_2(P/n_{\text{final}})$ stages, and L9 costs $O(n_{\text{final}} N^2)$. With the upsampling of L1, $O(N \cdot F N \log(F N))$, the total is $O(N^2 \log N)$ for fixed $F$, $O$ and $n_{\text{final}}$, in the real-RAM model. The extra space is $O(N^2)$ for the subimages of two stages.

## Properties

- Linear in the data.
- Exact before interpolation; the error is set by the oversampling in $\beta$ and in range.
- Not limited to a straight track in principle: the factorization holds for any path, and only the polar grids need care.
- The trade between speed and accuracy is set by $O$, the merge factor and the number of final subimages.

## Variants and improvements

- **Larger merge factors.** Merging 4 or 8 subapertures at a time lowers the number of stages; the cost is still $O(N^2 \log N)$.
- **Better interpolators.** A short sinc or spline kernel in $\beta$ allows a smaller $O$ for the same error.
- **Other paths.** Versions for curved paths and for 3D scenes use local coordinates that follow the track.
- **Local backprojection.** Simpler fast schemes split the aperture and the image only once, which lowers the cost below $O(N^3)$ but not to $O(N^2 \log N)$.

## When to use it

Use FFBP when backprojection is the right model, as for wide apertures, low frequencies or nonlinear paths, and the image is too large for direct backprojection. For small images the overhead of the polar grids makes direct backprojection faster, as the cost counts above show.

## Pitfalls

- **Phase reference.** The subimages must carry the factor $e^{-i 4\pi f_0 r/c}$ about their own center, and L7 must use the child range $r_h$ and the new range $r$. Without this the subimages oscillate quickly in $\beta$ and interpolation fails.
- **Too few angle samples.** A step near the Nyquist value $\lambda/(2l_s)$ is not enough for linear interpolation; the test shows an error of 18% of the peak with $O = 4$.
- **Grids that do not cover the scene.** Each polar grid must cover the whole scene plus a margin of a few samples, or pixels near the edges read zeros.
- **Errors add over stages.** Each stage interpolates again, so the error grows with the number of stages; use a better interpolator or a larger $O$ for long apertures.

## Implementations

## History

Fast versions of SAR backprojection were developed in the 1990s for ultra-wideband, low-frequency airborne radar, where the aperture is wide and frequency-domain algorithms are not accurate. Ulander, Hellsten and Stenstrom (2003) described the fully factorized version, with polar subimages, the $O(N^2 \log N)$ cost and an analysis of its errors, and it has since become a standard method for such systems.

## References
