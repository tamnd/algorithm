---
tag: 9V80CG
kind: technique
slug: subpixel-disparity-refinement
name: Subpixel disparity refinement
aliases:
- parabola fitting of matching cost
area: computer-vision/stereo-and-dense-reconstruction
level: core
summary: Fit a curve to the costs at the best integer disparity and its two neighbors and take the minimum of the curve as a fractional disparity.
prereqs: [cost-volume, disparity]
see_also: [depth-from-disparity, block-matching-stereo, semi-global-matching, left-right-consistency-check, stereo-matching-cost, polynomial-interpolation, phase-correlation, lucas-kanade-method]
sources:
  - paper: doi:10.1007/s11263-005-6878-5
    title: Masao Shimizu and Masatoshi Okutomi, Sub-pixel estimation error cancellation on area-based matching, International Journal of Computer Vision 63(3), 2005, 207-224
    locator: the analysis of the error of parabola and equiangular line fitting, its bias toward integer shifts, and the cancellation with a half pixel shifted image
  - paper: doi:10.1023/A:1014573219977
    title: Daniel Scharstein and Richard Szeliski, A taxonomy and evaluation of dense two-frame stereo correspondence algorithms, International Journal of Computer Vision 47(1-3), 2002, 7-42
    locator: the part on subpixel refinement by fitting a curve to the aggregated costs
  - paper: doi:10.1109/TPAMI.2007.1166
    title: Heiko Hirschmüller, Stereo processing by semiglobal matching and mutual information, IEEE Transactions on Pattern Analysis and Machine Intelligence 30(2), 2008, 328-341
    locator: the part on subpixel estimation by a quadratic curve through the neighboring costs
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 12, Depth estimation (subpixel estimation and refinement of disparities)
---

Subpixel disparity refinement turns the integer disparity $d$ chosen for a pixel into a fractional one by fitting a curve to the costs $C_- = C(d - 1)$, $C_0 = C(d)$ and $C_+ = C(d + 1)$ of the [cost volume](/cost-volume/) and taking the position of its minimum. With a parabola the offset is

$$\delta = \frac{C_- - C_+}{2\,(C_- - 2 C_0 + C_+)}, \qquad \hat d = d + \delta, \qquad |\delta| \le \tfrac12 \text{ when } C_0 \le C_-, C_+ .$$

Integer disparities give depth in layers, and by [depth from disparity](/depth-from-disparity/) the gap between layers grows with the square of the depth, so far points need fractions of a pixel. The fit costs $O(1)$ per pixel. It is not unbiased: the estimates are pulled toward integers, which is called pixel locking, and Shimizu and Okutomi (2005) analyzed this error and proposed a way to cancel it.

## In plain words

A stereo matcher tries whole pixel shifts only, so it can say "the match is 20 pixels to the left" but not "20.3 pixels". The cost at shift 20 is the lowest, and the costs at 19 and 21 are higher. If the cost at 21 is only a little higher than at 20 while the cost at 19 is much higher, the true lowest point is probably a bit past 20, toward 21. Draw a smooth bowl through the three costs and read where its bottom is. That is the refined disparity.

## When it applies

- A method has chosen an integer disparity $d$ with $0 < d < D - 1$, so both neighbors exist, and $C_0$ is a strict local minimum of the cost column: $C_0 < C_-$ or $C_0 < C_+$, and $C_0 \le$ both.
- The costs near the minimum vary smoothly with the shift, which holds when the images are smooth enough at the scale of a pixel and the cost is aggregated over a window. This is an assumption about the data.
- The depth accuracy matters at a scale finer than one disparity step, as for far points, 3D models and measurements.

## The template

```pseudo id=main
SUBPIXEL(C, d, fit)
L1  if d = 0 or d = D - 1 then return d                 ▷ no neighbor on one side
L2  c₋ ← C(d - 1);  c₀ ← C(d);  c₊ ← C(d + 1)
L3  if fit = parabola then
L4      a ← c₋ - 2c₀ + c₊
L5      if a ≤ 0 then return d                         ▷ flat or not a minimum
L6      δ ← (c₋ - c₊) / (2a)
L7  else                                                ▷ equiangular lines
L8      m ← max(c₋, c₊) - c₀
L9      if m ≤ 0 then return d
L10     δ ← (c₋ - c₊) / (2m)
L11 return d + δ
```

The hole is the curve. Two choices are common, and Shimizu and Okutomi (2005) relate each to a cost: the parabola fits SSD-like costs, which are quadratic in a small shift, and two lines of equal and opposite slope fit SAD-like costs, which are close to $|s|$ in a small shift.

**Why the parabola formula.** Put $q(t) = \alpha t^2 + \beta t + \gamma$ through $(-1, C_-)$, $(0, C_0)$, $(1, C_+)$. Then $\gamma = C_0$, $\alpha - \beta + \gamma = C_-$ and $\alpha + \beta + \gamma = C_+$, so $\alpha = \frac12 (C_- - 2 C_0 + C_+)$ and $\beta = \frac12 (C_+ - C_-)$. If $\alpha > 0$, the minimum is at $t = -\beta / (2 \alpha) = (C_- - C_+) / (2 (C_- - 2 C_0 + C_+))$, which is $\delta$. If $C_0 \le C_-$ and $C_0 \le C_+$, then $|C_- - C_+| \le (C_- - C_0) + (C_+ - C_0) = 2\alpha$, so $|\delta| \le \frac12$: the refined value stays within half a pixel of $d$, and refinement never moves a pixel past a neighbor. The minimum value is $C_0 - (C_- - C_+)^2 / (8 \alpha)$.

**Why the equiangular formula.** Take the line through $(-1, C_-)$ and $(0, C_0)$ when $C_- \ge C_+$, with slope $-(C_- - C_0) = -m$, and the line of slope $+m$ through $(1, C_+)$. They meet where $C_0 - m t = C_+ + m (t - 1)$, at $t = (C_- - C_+) / (2m)$ since $C_0 - C_+ + m = C_- - C_+$. The case $C_+ > C_-$ is the mirror image, and both are the formula of line L10.

## Classic examples

**Check value.** For the costs $C_- = 4$, $C_0 = 1$, $C_+ = 2$, the parabola gives $a = 4 - 2 + 2 = 4$ and $\delta = (4 - 2) / 8 = +0.25$, with the minimum value $1 - 4 / 32 = 0.875$. The equiangular lines give $m = 4 - 1 = 3$ and $\delta = 2 / 6 = 1/3$. Both move toward $d + 1$, the side with the lower neighbor; the lines move further.

**Pixel locking.** A small experiment shows the bias. A 1D signal is a sum of sines; the right signal is the left one shifted by a known $s$, evaluated exactly. Costs are summed over 7 pixels, and the estimates are averaged over 30 positions. For a smooth signal (frequencies up to 0.6 radian per pixel):

| true $s$ | SSD, parabola | SAD, parabola | SAD, lines |
|---|---|---|---|
| 0.10 | 0.101 | 0.058 | 0.101 |
| 0.25 | 0.246 | 0.168 | 0.249 |
| 0.40 | 0.395 | 0.333 | 0.398 |

Each cost fits its own curve well, and the parabola on SAD costs is pulled toward 0. For a rough signal (frequencies from 0.8 to 2.5 radians per pixel) every fit is pulled toward the integer: at $s = 0.25$ the three columns give 0.182, 0.132 and 0.198. A histogram of the refined disparities of a real scene then shows peaks at the integers. These numbers come from this one experiment, not from a theorem.

**In stereo methods.** [Semi-global matching](/semi-global-matching/) fits a parabola to the summed path costs. [Block matching](/block-matching-stereo/) in OpenCV refines its SAD costs the same way. The refined map is what [depth from disparity](/depth-from-disparity/) converts, and it is where the $Z^2$ error law of that page starts.

## Variations

- **Error cancellation.** Shimizu and Okutomi (2005) match a second time with an image interpolated at half a pixel shift, so that the bias of the second estimate is roughly opposite to that of the first, and average the two.
- **Other curves.** Higher order polynomials through more costs, or the curve that the cost would have for a known signal model. A [polynomial interpolation](/polynomial-interpolation/) through five costs has its own bias.
- **Direct refinement.** Optimize the fractional disparity directly by minimizing the cost over a continuous shift, with images interpolated by [bilinear interpolation](/bilinear-interpolation/) or better, as in a 1D [Lucas-Kanade](/lucas-kanade-method/) step. This avoids the bias of the curve but costs more.
- **Phase-based methods.** The shift of a window can be read from the phase of its Fourier transform, as in [phase correlation](/phase-correlation/), which is fractional by nature.
- **Soft argmin.** Learned methods take the expected disparity under a softmax of the negative costs, which is fractional and differentiable but averages over all disparities.

## Pitfalls

- **Wrong curve for the cost.** A parabola on SAD costs or on census costs is biased toward integers. Use the lines, or a cost that is quadratic near its minimum.
- **Ends of the range.** At $d = 0$ or $d = D - 1$ there is no neighbor on one side. Do not refine, and treat the disparity as unreliable, because the true minimum may be outside the range.
- **Flat or non-convex triples.** If $C_- - 2 C_0 + C_+ \le 0$, the parabola has no minimum, and the formula divides by zero or a negative number. Return the integer.
- **Sign.** $C_-$ belongs to $d - 1$. Swapping the neighbors flips $\delta$ and doubles the error.
- **Refine after the check.** A [left-right consistency check](/left-right-consistency-check/) with $\tau = 0$ on refined maps rejects almost everything. Check on integer maps, or use $\tau \ge 1$.
- **Smoothing before fitting.** Smoothness terms, like the penalties of semi-global matching, change the shape of the cost near its minimum. The fit is then a heuristic.

## References
