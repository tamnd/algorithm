---
tag: R1NZQT
kind: algorithm
slug: cotton-schwab-clean
name: Cotton-Schwab CLEAN
aliases:
- major-minor cycle CLEAN
- Cotton-Schwab algorithm
area: imaging-and-inverse-problems/deconvolution-and-astronomical-imaging
level: advanced
summary: "Run fast CLEAN minor cycles on an image with a cut beam, then subtract the model from the ungridded visibilities in a major cycle, which removes the errors the minor cycles built up."
solves: [image-deblurring]
model: real-ram
complexity:
  vars: {n: the number of pixels, m: the number of visibilities, C: the number of major cycles, K: the total number of minor steps, b: the number of pixels in the beam patch}
  time: {worst: Θ(C m n + K (n + b)), average: Θ(C m n + K (n + b)), best: Θ(C m n + K (n + b))}
  space: {extra: Θ(m + n)}
properties: {deterministic: true, iterative: true, linear: false, greedy: true, nonnegative: false, exact_residual_each_major_cycle: true, monotone_misfit: false}
history:
  year: 1984
  people: [Fred R. Schwab, William D. Cotton]
  note: "Schwab (1984) described major cycles that subtract the CLEAN model from the measured visibilities, after Clark (1980) had split CLEAN into minor and major cycles on images."
prereqs: [hogbom-clean, dirty-image, aperture-synthesis]
see_also: [multiscale-clean, w-projection, van-cittert-zernike-theorem, nonuniform-fft, density-compensation, maximum-entropy-method-imaging, coordinate-descent]
sources:
  - paper: doi:10.1086/113605
    title: "F. R. Schwab, Relaxing the isoplanatism assumption in self-calibration; applications to low-frequency radio interferometry, The Astronomical Journal 89, 1984"
    locator: the article from page 1076 (the CLEAN variant whose major cycles subtract the model from the ungridded visibilities)
  - paper: "B. G. Clark, An efficient implementation of the algorithm CLEAN, Astronomy and Astrophysics 89(3), 1980"
    title: "Clark, An efficient implementation of the algorithm CLEAN, 1980"
    locator: "the article (minor cycles with a beam patch and the brightest pixels, major cycles with the FFT)"
  - book: isbn:9783319444314
    title: "A. Richard Thompson, James M. Moran and George W. Swenson Jr., Interferometry and Synthesis in Radio Astronomy, third edition, Springer, 2017"
    locator: "Chapter 11, Further Imaging Techniques (the CLEAN variants)"
  - paper: doi:10.1093/mnras/stu1368
    title: "A. R. Offringa et al., WSClean, an implementation of a fast, generic wide-field imager for radio astronomy, Monthly Notices of the Royal Astronomical Society 444(1), 2014"
    locator: pages 606 to 619 (a modern imager built on major and minor cycles)
---

Cotton-Schwab CLEAN runs [Hogbom CLEAN](/hogbom-clean/) in short, cheap *minor cycles* on an image with only a small patch of the dirty beam, and between them runs a *major cycle* that predicts the visibilities of the model, subtracts them from the measured, ungridded visibilities and makes a new exact residual image. The minor cycles are fast but drift, because the cut beam and the gridding are approximate; each major cycle wipes the drift out. Hogbom CLEAN never goes back to the data, and [multiscale CLEAN](/multiscale-clean/) changes the components, not the cycles: in practice multiscale steps run as the minor cycles of this frame. Because the major cycle works on the visibilities, it is also where wide-field corrections such as [W-projection](/w-projection/) enter.

## In plain words

Cleaning a big picture one point at a time is slow if each step has to touch every pixel. So this method cheats a little. For a while it removes only the bright center of the known pattern around each point, which is fast. The picture it works on slowly goes wrong, because the far parts of the pattern were not removed. Then it stops and goes back to the raw measurements. It computes what its list of points should have measured, takes that away from the real measurements, and makes a fresh and exact leftover picture. Then it cheats again for a while. The fresh start wipes out the errors of the fast part.

## The problem

An interferometer measures visibilities $V_j$ at points $(u_j, v_j)$ of the uv plane, with weights $w_j > 0$ and $W = \sum_j w_j$; see [aperture synthesis](/aperture-synthesis/). For a model $M$ on an image of $n$ pixels at directions $(l_q, m_q)$, the predicted visibilities are

$$(AM)_j = \sum_q M_q\, e^{-2\pi i (u_j l_q + v_j m_q)} .$$

The [dirty image](/dirty-image/) of a set of visibilities $X$ is $\mathcal I(X)_q = \frac1W \sum_j w_j\, \mathrm{Re}\big(X_j\, e^{2\pi i (u_j l_q + v_j m_q)}\big)$, and the dirty beam is $B(\Delta) = \frac1W \sum_j w_j \cos 2\pi (u_j \Delta l + v_j \Delta m)$, so $B(0) = 1$. For a sky $x$, $\mathcal I(Ax) = B \star x$, the ordinary (not periodic) convolution over pixel offsets.

The input is the list of visibilities, the pixel grid, a loop gain $g$, a threshold $\tau$, a beam patch half-width $P$ and a cycle factor $f$. The output is a model $M$ and the exact residual image $\mathcal I(V - AM)$.

## The algorithm

```pseudo id=main
COTTON-SCHWAB-CLEAN(V, g, τ, P, f, C)
L1  M ← 0, V_r ← V
L2  for c ← 1 to C do                              ▷ major cycles
L3      R ← I(V_r)                                 ▷ exact residual image
L4      if max_q |R_q| ≤ τ then break
L5      λ ← max(τ, f · max_q |R_q|)
L6      Hogbom steps on R until max_q |R_q| ≤ λ,   ▷ the minor cycle
          subtracting only B(Δ) with |Δ| ≤ P, and adding the components to M
L7      V_r ← V - A M                              ▷ predict and subtract
L8  return M, I(V_r)
```

Line L6 is lines L3 to L7 of Hogbom CLEAN, with the subtraction cut to the patch: $R_q \leftarrow R_q - c\,B(q - p)$ only for $|q - p| \le P$ in each coordinate. Line L7 is the step that names the method: it goes back to the measured, ungridded visibilities, so nothing that the minor cycle got wrong survives into the next residual image.

The cycle factor $f$ decides how far a minor cycle may go. The rule of Clark (1980) is to set $f$ to the largest beam value outside the patch: a sidelobe outside the patch can then hide at most a fraction $f$ of a peak. The code uses this rule by default. Production imagers grid the visibilities and use the FFT in lines L3 and L7, which costs much less than the direct sums here; the gridding error is one more thing that line L7 removes, because the prediction is subtracted from the visibilities and not from an image.

## Example

Take a $16 \times 16$ image with pixel size $1/16$ in direction cosine, and four point sources of flux $1.0$, $0.7$, $0.5$ and $0.4$ (total $2.6$). The array has 100 random baselines with $|u|, |v| \le 6$, each with its conjugate, so $m = 200$. The dirty peak is $1.0154$ and the misfit $Q(M) = \frac1W \sum_j w_j |V_j - (AM)_j|^2$ starts at $2.1052$. The beam has $B(0, \pm 1) = 0.2699$ and $B(\pm 1, 0) = 0.3646$, and its largest value outside a patch of half-width $P = 3$ is $0.2253$, which is the cycle factor. With $g = 0.2$ and at most 150 minor steps per cycle:

| major cycle | minor steps | $Q$ after | exact $\max_q \lvert R_q \rvert$ after | model flux |
|---|---|---|---|---|
| 1 | 31 | 0.0721 | 0.1505 | 2.2702 |
| 2 | 43 | 0.0213 | 0.0615 | 2.5374 |
| 3 | 81 | 0.0074 | 0.0363 | 2.5955 |
| 4 | 55 | 0.0040 | 0.0201 | 2.6317 |
| 6 | 69 | 0.0015 | 0.0070 | 2.6148 |
| 8 | 150 | 0.0008 | 0.0042 | 2.6079 |

Now run one minor cycle of 150 steps with the same patch and no major cycle. The minor cycle believes the residual peak is $0.1016$, but the exact residual has peak $0.3382$, and the misfit is still $0.4616$. The drift came from the sidelobes outside the patch. With the full beam as patch, 150 steps of one cycle bring $Q$ to $10^{-8}$, which is Hogbom CLEAN.

## Correctness

Three facts are proved, and one is not claimed.

- **Exact residual.** Line L3 makes $R = \mathcal I(V - AM)$, and this equals $D - B \star M$. So every major cycle starts from the true residual, whatever the minor cycles did.
- **Bounded drift.** During a minor cycle that adds the components $\Delta M$, the image $R$ it keeps differs from the exact residual by at most $\beta_P \|\Delta M\|_1$ at each pixel, where $\beta_P$ is the largest beam value outside the patch.
- **When a minor step helps.** If the drift at the chosen pixel is at most $e$, the step lowers the true misfit as long as the peak it sees exceeds $2e/(2 - g)$. With the full beam as patch, $e = 0$, and the minor cycle is Hogbom CLEAN on the exact convolution, with the proved descent.
- **Not claimed: convergence for a cut beam.** If a minor cycle goes too far, the true misfit can rise. On the data of the example with a patch of half-width 1, no cycle factor and 150 minor steps per cycle, the misfit after 1, 2, 4 and 8 major cycles is $0.640$, $0.328$, $0.310$ and $1.036$. With Clark's factor for that patch, $0.2672$, it is $0.129$, $0.0175$, $0.0016$ and $0.0003$. Clark's rule is a heuristic that works in practice, not a theorem.

The full proof is below.

## Complexity

With $m$ visibilities and $n$ pixels, the direct sums of lines L3 and L7 take $\Theta(mn)$ time per major cycle. A minor step takes $\Theta(n)$ for the peak search and $\Theta(b)$ for the patch, where $b = (2P + 1)^2$. So $C$ major cycles and $K$ minor steps take $\Theta(Cmn + K(n + b))$. Imagers replace the direct sums by gridding and the [FFT](/fast-fourier-transform/), or by the [nonuniform FFT](/nonuniform-fft/), which cost $\Theta(m s^2 + n \log n)$ per cycle with a kernel of $s \times s$ cells. Because a major cycle is expensive, the art is in doing as few as possible: Clark's cycle factor lets each minor cycle go as far as it safely can.

## Properties

- **The residual is exact after each major cycle.** Errors of the minor cycle do not build up across cycles.
- **Model on the visibilities.** The model is subtracted from the data themselves, so gridding errors, a beam that changes over the field and the $w$ term can be handled in the prediction step.
- **The same answer as Hogbom CLEAN in the limit of a full patch.**
- **Not monotone in general.** A minor cycle with a cut beam can raise the misfit; see the correctness section.
- **The usual CLEAN behavior.** Greedy, nonlinear, and no noise model; the threshold $\tau$ guards against fitting the noise.

## Variants and improvements

- **Clark CLEAN.** Major cycles on images: the residual image is recomputed by an FFT convolution of the model with the full beam, not from the visibilities. It removes the drift of the cut beam but not gridding errors.
- **Multiscale minor cycles.** The minor cycle is [multiscale CLEAN](/multiscale-clean/) in place of point CLEAN.
- **Wide-field prediction.** Line L7 predicts with a $w$ correction, such as [W-projection](/w-projection/), so that sources far from the field center are subtracted correctly.
- **Self-calibration.** Between major cycles, the model visibilities are used to solve for antenna gain errors; this was the setting of Schwab (1984).

## When to use it

Use Cotton-Schwab CLEAN for any real interferometer data set: it is the standard frame of radio imaging software. Use it when the data are not on a grid, when the field is wide, or when calibration is still being refined. Use plain [Hogbom CLEAN](/hogbom-clean/) only for a small image with a known beam, or for teaching.

## Pitfalls

- **Minor cycles that go too far.** With a small patch and a cycle factor below the outside sidelobe level, the minor cycle cleans sidelobes that it never subtracted, and the true misfit can rise. Use Clark's rule or a larger patch.
- **Too many major cycles.** Each one costs a full pass over the visibilities. A cycle factor that is too high wastes them.
- **A model that is not on the image grid.** The prediction in line L7 must use the same pixel positions and the same sign convention as the imaging in line L3, or the residual will not go down.
- **A threshold below the noise.** As for every CLEAN, the components then fit the noise.

## Implementations

## History

Hogbom (1974) cleaned the dirty image with the full beam. Clark (1980) made this faster with minor cycles that use a small patch of the beam and only the brightest pixels, and major cycles that recompute the residual image with the FFT. Schwab (1984), in a paper on self-calibration, moved the major cycle to the visibilities: subtract the model from the ungridded data and image the result again. The method carries his name and that of W. D. Cotton. This form became the standard frame of radio imaging, and modern imagers such as WSClean are built around it.

## References
