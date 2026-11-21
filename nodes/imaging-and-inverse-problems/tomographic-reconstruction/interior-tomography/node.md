---
tag: S7SZ2R
kind: problem
slug: interior-tomography
name: Interior tomography
aliases:
- region of interest tomography
- interior problem
area: imaging-and-inverse-problems/tomographic-reconstruction
level: advanced
summary: "Reconstruct a region inside the object from the rays that pass through it only, which is not unique without extra prior information."
model: real-ram
prereqs: [radon-transform, radon-inversion-formula, hilbert-transform]
see_also: [lambda-tomography, limited-angle-tomography, tuy-condition, katsevich-algorithm, filtered-back-projection, tomographic-reconstruction-problem, asd-pocs, sparse-view-ct-reconstruction]
sources:
  - book: isbn:9780898714937
    title: F. Natterer, The Mathematics of Computerized Tomography, SIAM Classics in Applied Mathematics 32, 2001
    locator: Chapter VI, Incomplete Data, pp. 158 to 179
  - paper: doi:10.1088/0266-5611/22/3/019
    title: M. Defrise, F. Noo, R. Clackdoyle and H. Kudo, Truncated Hilbert transform and image reconstruction from limited tomographic data, Inverse Problems 22(3), 2006
    locator: pp. 1037 to 1053
  - paper: doi:10.1155/2007/63634
    title: Y. Ye, H. Yu, Y. Wei and G. Wang, A general local reconstruction approach based on a truncated Hilbert transform, International Journal of Biomedical Imaging, 2007
    locator: article 63634
  - paper: doi:10.1088/0031-9155/53/9/001
    title: H. Kudo, M. Courdurier, F. Noo and M. Defrise, Tiny a priori knowledge solves the interior problem in computed tomography, Physics in Medicine and Biology 53(9), 2008
    locator: pp. 2207 to 2231
  - paper: doi:10.1088/0031-9155/54/9/014
    title: H. Yu and G. Wang, Compressed sensing based interior tomography, Physics in Medicine and Biology 54(9), 2009
    locator: pp. 2791 to 2805
---

Interior tomography asks for the image inside a region of interest when only the rays that pass through that region are measured. The rays through the rest of the object are missing, so every projection is truncated on both sides. The [Radon inversion formula](/radon-inversion-formula/) in the plane is not local, because its [Hilbert transform](/hilbert-transform/) uses the whole projection, so [filtered back-projection](/filtered-back-projection/) of the truncated data gives a wrong image. The loss is not only a matter of the method: the data do not determine the image. There are functions that are not zero inside the region and whose line integrals are zero on every line through the region. With a small piece of extra knowledge, for example the values of the image on a small subregion, or an image that is piecewise constant, the solution is unique again. [Lambda tomography](/lambda-tomography/) gives a local image with the right edges but not the right values.

## In plain words

A scanner can save dose and detector size by sending rays only through a small part of the body, the part the doctor wants to see. Each ray still passes through the tissue around that part, so each measured value mixes the inside with the outside. The standard method needs every ray through the whole body, and it fails with the short set. Worse, the short set cannot tell some objects apart. A smooth ring of material around the region can be shaped so that it adds a smooth bump inside the region and changes no measured ray at all. So some extra fact is needed: a small area where the true values are known, or the knowledge that the image is made of flat patches. With such a fact the region is fixed again.

## Definition

Let $f \in L^2(\mathbb{R}^2)$ be zero outside the unit disk, the object, and let $D_r = \{x : |x| < r\}$ with $0 < r < 1$ be the region of interest. With $\omega(\theta) = (\cos\theta, \sin\theta)$, the data are the [Radon transform](/radon-transform/)
$$\mathcal{R}f(\theta, s) = \int f(s\,\omega(\theta) + t\,\omega(\theta)^\perp)\,dt, \qquad \theta \in [0, \pi), \quad |s| < r,$$
which are the integrals of $f$ along all lines that meet $D_r$, plus noise. In practice the data are samples on a grid of $(\theta, s)$ with additive noise, or the same lines in a fan-beam geometry with a small detector. The task is to find $f$ on $D_r$. The values of $f$ outside $D_r$ are not asked for.

**Non-uniqueness (theorem).** Let $p$ be an even $C^1$ function of $s$ that is zero for $|s| \le r$ and for $|s| \ge 1$, positive for $r < |s| < 1$, and let $g$ be the radial function
$$g(x) = G(|x|), \qquad G(\rho) = -\frac{1}{\pi}\int_{\max(\rho, r)}^{1} \frac{p'(s)}{\sqrt{s^2 - \rho^2}}\,ds$$
for $\rho < 1$, and $G(\rho) = 0$ for $\rho \ge 1$. This is the inverse Abel transform, so $\mathcal{R}g(\theta, s) = p(s)$ for every $\theta$. Then $g$ is zero outside the unit disk, $\mathcal{R}g = 0$ on every line that meets $D_r$, and
$$G(0) = -\frac{1}{\pi}\int_r^1 \frac{p'(s)}{s}\,ds = -\frac{1}{\pi}\int_r^1 \frac{p(s)}{s^2}\,ds < 0,$$
by integration by parts with $p(r) = p(1) = 0$. So $f$ and $f + g$ have the same data and differ at the center of the region. Every $p$ of this kind gives a different $g$, so the null space of the interior problem has infinite dimension.

**The null functions are analytic in the region (theorem, radial case).** For $\rho < r$ the integral for $G(\rho)$ runs over $s \in [r, 1]$, where $s^2 - \rho^2 \ge r^2 - \rho^2 > 0$, so $G$ is a real analytic function of $\rho^2$ on $[0, r)$. A nonzero $G$ of this kind cannot be zero on an interval inside $[0, r)$. This is the mechanism behind the uniqueness results below: a null function that is zero on a small subregion is zero on the whole region.

## Variants

- **A known subregion.** The values of $f$ are known on a small open set inside $D_r$, for example air or a calibrated insert. Then the interior data determine $f$ on $D_r$ (Kudo, Courdurier, Noo and Defrise 2008; Ye, Yu, Wei and Wang 2007, cited). Stability decreases away from the known set (heuristic).
- **Piecewise constant images.** If $f$ is piecewise constant on $D_r$, the interior data determine $f$ on $D_r$, and total variation minimization finds it (Yu and Wang 2009, cited). Results of the same kind for piecewise polynomial images with a total variation of higher order are reported in later work, which this page has not checked.
- **The exterior problem.** The data are the lines that miss a disk, and $f$ is asked for outside the disk. For an $f$ with compact support, Helgason's support theorem gives uniqueness outside the disk (theorem). The inversion is much less stable than the full problem (heuristic).
- **Cone-beam ROI scans.** In helical CT the detector covers only a part of the object along the axis, the long object problem. The [Katsevich algorithm](/katsevich-algorithm/) handles this kind of truncation along the axis, because its filter lines need data only in a band of detector rows near the source position. The truncation across the axis is the 2D interior problem of this page.

## Examples

**A null function.** Take $r = 1/2$ and $p(s) = (s^2 - r^2)^2(1 - s^2)^2$ for $r < |s| < 1$, zero elsewhere. This $p$ is $C^1$. A Python check with Simpson's rule after the substitution $s = \sqrt{\rho^2 + w^2}$, which removes the square root singularity, gives these values (measurement):

| $\rho$ | 0 | 0.1 | 0.25 | 0.4 | 0.7 | 0.9 |
|---|---|---|---|---|---|---|
| $G(\rho)$ | -0.002842 | -0.002924 | -0.003432 | -0.004978 | 0.000374 | 0.018981 |

The forward Abel transform $\mathcal{R}g(s) = 2\int_0^{\sqrt{1 - s^2}} G(\sqrt{s^2 + w^2})\,dw$ of these values gives at most $3.1 \times 10^{-8}$ for $s = 0, 0.2, 0.45$, and $0.0049562$, $0.0186920$, $0.0113210$ for $s = 0.6, 0.75, 0.9$, against $p(s) = 0.0049562$, $0.0186920$, $0.0113210$. So the ring $0.5 < |x| < 1$ carries a function that is invisible to every line through $D_{1/2}$ and that changes the image inside by about $-0.003$ to $-0.009$.

**What filtered back-projection does with the truncated data (heuristic).** Setting the missing part of each projection to zero puts a jump at $|s| = r$ in every projection. The ramp filter turns each jump into a large tail, and the back projection adds these tails into a bright ring at the edge of $D_r$ and a smooth wrong offset inside. Extrapolating the projections smoothly beyond $|s| = r$ removes most of the ring, but not the offset, which is the null space at work.

## Known algorithms

| Method | Extra knowledge | What it gives |
|---|---|---|
| [Filtered back-projection](/filtered-back-projection/) with extrapolated projections | none | a fast image with a smooth error inside the region; no guarantee |
| [Lambda tomography](/lambda-tomography/) | none | $\Lambda f$ on $D_r$ from the interior data only: the right edges and singularities, not the values of $f$ |
| Differentiated back projection and the truncated Hilbert transform (Defrise et al. 2006) | $f$ known on a part of each chord, or the chord leaves the support inside the data | the Hilbert transform of $f$ along chords from the data, then $f$ on the chords by inverting a truncated Hilbert transform |
| Known subregion (Ye et al. 2007; Kudo et al. 2008) | $f$ on a small subregion | $f$ on the whole region, through the truncated Hilbert transform on chords that pass through the known set; exact in theory, the conditioning gets worse far from the known set |
| Total variation minimization (Yu and Wang 2009) | $f$ piecewise constant | $f$ by an iterative fit with a total variation penalty; solvers such as [ASD-POCS](/asd-pocs/) |

## Bounds

- **Information (theorem).** The null space of the interior data has infinite dimension and contains smooth radial functions that are not zero at the center of the region (the Definition). No method can recover $f$ on $D_r$ from the data alone. This is a worst case statement over all $f$.
- **Singularities are determined (theorem plus a cited fact).** $\Lambda f = \mathcal{R}^\#(-\partial_s^2\mathcal{R}f)$ on $D_r$ uses only the lines that meet $D_r$, so it is computable from the data. The [lambda tomography](/lambda-tomography/) page shows that $\Lambda f$ has the same singularities as $f$. So the edges of $f$ inside the region are determined, and the null functions are smooth inside the region.
- **Prior knowledge restores uniqueness (theorem, cited).** A known subregion gives uniqueness (Kudo et al. 2008), and so does a piecewise constant $f$ (Yu and Wang 2009). Uniqueness does not give a stability constant. Inversion of the truncated Hilbert transform is severely ill-posed, so the error grows quickly away from the known set (heuristic).

## Reductions

- **Interior data to the truncated Hilbert transform (cited).** Differentiate each projection in $s$ and back-project over a half turn of angles. In the plane this gives the Hilbert transform of $f$ along lines, at the points where the data cover all angles (Defrise et al. 2006). So the interior problem becomes the inversion of a Hilbert transform on a chord from its values on a part of the chord.
- **Interior data to lambda tomography.** Drop the Hilbert transform of the inversion formula and keep the second derivative, which is local. The result is $\Lambda f$, not $f$ ([lambda tomography](/lambda-tomography/)).
- **Interior tomography to a regularized fit.** With a total variation penalty, the interior problem becomes a convex optimization over images, and the solvers of [sparse-view CT](/sparse-view-ct-reconstruction/) apply.

## Applications

- **Dose reduction (heuristic).** Rays only through the region of interest reduce the dose to the tissue that is not of interest.
- **Large objects and small detectors.** When the object is larger than the field of view of the detector, every projection is truncated, and the inside of the field of view is an interior problem.
- **Helical cone-beam CT.** Truncation along the axis, the long object problem, is solved by the [Katsevich algorithm](/katsevich-algorithm/) and related exact methods; the [Tuy condition](/tuy-condition/) page explains which planes the source must meet.

## References
