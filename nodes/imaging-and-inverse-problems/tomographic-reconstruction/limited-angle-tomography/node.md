---
tag: 8FFBQS
kind: problem
slug: limited-angle-tomography
name: Limited-angle tomography
aliases:
- limited-view tomography
area: imaging-and-inverse-problems/tomographic-reconstruction
level: advanced
summary: "Reconstruct from projections over an angular range less than 180 degrees, which leaves a wedge of Fourier space unmeasured and only edges in some directions stable."
model: real-ram
prereqs: [radon-transform, fourier-slice-theorem]
see_also: [interior-tomography, lambda-tomography, sparse-view-ct-reconstruction, asd-pocs, truncated-svd, degree-of-ill-posedness, fan-beam-filtered-back-projection, tikhonov-regularization]
sources:
  - paper: doi:10.1137/0143028
    title: M. E. Davison, The ill-conditioned nature of the limited angle tomography problem, SIAM Journal on Applied Mathematics 43(2), 1983
    locator: pp. 428 to 448
  - paper: doi:10.1137/0524069
    title: E. T. Quinto, Singularities of the X-ray transform and limited data tomography in R^2 and R^3, SIAM Journal on Mathematical Analysis 24(5), 1993
    locator: pp. 1215 to 1225 (which singularities of the object the limited data show stably)
  - book: isbn:9780898714937
    title: F. Natterer, The Mathematics of Computerized Tomography, SIAM Classics in Applied Mathematics 32, 2001
    locator: Chapter VI, Incomplete Data, pp. 158 to 179
---

Limited-angle tomography asks for an image when the projections cover only a part of the half turn of directions. Each parallel projection gives one line of the 2D Fourier transform of the object, by the [Fourier slice theorem](/fourier-slice-theorem/), so a missing range of angles leaves a double wedge of Fourier space without data. For an object of compact support the data still determine the object, because its Fourier transform is analytic, but the problem is severely ill-posed: there are images of unit size whose projections over the measured angles are smaller than $10^{-5}$. Edges whose normal is in the measured range of angles are stably visible in the data; edges whose normal is in the missing range are smoothed away. Regularization with prior knowledge, such as positivity, a known support or a small total variation, fills in the wedge in a plausible way but not in a guaranteed way.

## In plain words

A scanner normally takes pictures of the object from every direction around half a circle. Sometimes the machine or the object blocks part of that arc, so some directions are never seen. Each picture holds the detail of the object that runs across the picture direction, so the detail that runs only in the unseen directions is very weak in the data. In theory a compact object is still fixed by the pictures, but recovering the weak part means amplifying noise by huge factors. In practice the result keeps the edges that the scanner saw side on and blurs the edges that it would only see from the missing directions. Long streaks appear along the last directions that were measured.

## Definition

Let $f \in L^2(\mathbb{R}^2)$, with $\omega(\theta) = (\cos\theta, \sin\theta)$ and the [Radon transform](/radon-transform/) $\mathcal{R}f(\theta, s) = \int f(s\,\omega(\theta) + t\,\omega(\theta)^\perp)\,dt$. Let $A \subset [0, \pi)$ be the set of measured angles, an interval of length less than $\pi$, or a union of such intervals. The data are $\mathcal{R}f(\theta, s)$ for $\theta \in A$ and all $s$, in practice sampled in $\theta$ and $s$ with additive noise. The task is to find $f$, usually with the extra knowledge that $f$ is zero outside a known disk.

By the Fourier slice theorem the data give $\mathcal{F}f(\sigma\,\omega(\theta))$ for $\theta \in A$ and $\sigma \in \mathbb{R}$. The other directions, the missing wedge, are not measured.

**Uniqueness (theorem).** If $f$ has compact support and $A$ contains an open interval, the data determine $f$. Proof: $\mathcal{F}f$ extends to an entire function on $\mathbb{C}^2$ (Paley-Wiener), so it is real analytic on $\mathbb{R}^2$. The data give $\mathcal{F}f$ on an open double cone, and a real analytic function that is zero on an open set is zero everywhere. Apply this to the difference of two functions with the same data. $\square$

**No stability of any Sobolev order (theorem).** Let $A$ miss the open interval $|\theta - \varphi| < \delta$, with $\nu = \omega(\varphi)$, and put $f_K(x) = e^{-\pi|x|^2}\cos(2\pi K\,x\cdot\nu)$. Then
$$\mathcal{R}f_K(\theta, s) = e^{-\pi K^2\sin^2(\theta - \varphi)}\;e^{-\pi s^2}\cos\big(2\pi K\cos(\theta - \varphi)\,s\big).$$
Proof: $\mathcal{F}f_K(\xi) = \frac{1}{2}\big(e^{-\pi|\xi - K\nu|^2} + e^{-\pi|\xi + K\nu|^2}\big)$, and $|\sigma\omega(\theta) \mp K\nu|^2 = (\sigma \mp K\cos(\theta - \varphi))^2 + K^2\sin^2(\theta - \varphi)$. The inverse 1D transform of the slice gives the formula. $\square$

For $\theta \in A$ the first factor is at most $e^{-\pi K^2\sin^2\delta}$. So every Sobolev norm $\|\cdot\|_{H^t}$ of the data in $s$, integrated over $A$, is at most a polynomial in $K$ times $e^{-\pi K^2\sin^2\delta}$, while $\|f_K\|_{L^2}^2 \to \frac{1}{2}\int e^{-2\pi|x|^2}dx = \frac{1}{4}$ as $K \to \infty$. No estimate $\|f\|_{L^2} \le C\,\|\mathcal{R}f|_A\|_{H^t}$ can hold, for any $t$. With full data the inversion is mildly ill-posed of [degree](/degree-of-ill-posedness/) $1/2$; with a missing wedge it is severely ill-posed. The functions $f_K$ do not have compact support, but they are Schwartz functions, and multiplying by a smooth cutoff changes the data only by a tiny amount (heuristic).

## Variants

- **Limited-angle fan beam.** A fan-beam scan needs the source angles over $\pi$ plus the fan angle for complete data, the short scan of [fan-beam filtered back-projection](/fan-beam-filtered-back-projection/). Fewer source angles leave a missing wedge, as in the parallel case.
- **Missing wedge and missing cone in 3D.** Tilt series in electron tomography stop short of the full range, which leaves a wedge of the 3D Fourier space empty. With tilts about two perpendicular axes the empty set shrinks to a pyramid, and with a conical tilt it is a cone.
- **Tomosynthesis.** A few projections over a small arc, with a reconstruction in planes parallel to the detector. It is a limited-angle problem with a very small $A$.
- **Few views.** Many angles missing but spread over the half turn is a different problem, [sparse-view CT](/sparse-view-ct-reconstruction/), where the loss is aliasing rather than a wedge.

## Examples

**An invisible pattern (theorem plus measurement).** Take $\varphi = \pi/2$, $\delta = \pi/6$ and $K = 4$, so the measured angles are $\theta \in [0, \pi/3] \cup [2\pi/3, \pi)$, a range of 120 degrees. The function $f_4$ is a Gaussian with stripes along $x_2$, and $f_4(0) = 1$. By the formula above its data are at most $e^{-4\pi} = 3.49 \times 10^{-6}$ on the measured angles. At the missing angle $\theta = \pi/2$ and $s = 0.1$ the projection is $-0.78400$. A Python check with the midpoint rule along the line gave $3.4873424 \times 10^{-6}$ at $\theta = \pi/3$, $s = 0$, and $-0.7839961$ at $\theta = \pi/2$, $s = 0.1$, as the formula gives. With $K = 8$ the data are at most $e^{-16\pi} = 1.5 \times 10^{-22}$. So a stripe pattern of unit size, with its normal in the missing wedge, is invisible to any instrument with a relative noise above these levels.

**Which edges survive (cited, with a heuristic explanation).** A disk with a sharp edge, scanned over $A = [0, 2\pi/3]$: the parts of the edge whose normal is $\omega(\theta)$ with $\theta \in A$ are reconstructed sharp, and the parts whose normal points into the missing range come out blurred. Each measured projection has a jump where its lines are tangent to the edge, and those are exactly the lines whose normal is the normal of the edge (Quinto 1993 gives the precise statement for the X-ray transform).

## Known algorithms

| Method | Extra knowledge | What it gives |
|---|---|---|
| [Filtered back-projection](/filtered-back-projection/) over $A$ | none | the visible edges sharp; streaks along the two end directions of $A$; the missing wedge set to zero |
| [Truncated SVD](/truncated-svd/) or [Tikhonov regularization](/tikhonov-regularization/) | a noise level | a stable image that keeps only the components with large singular values; the missing wedge stays nearly empty |
| Iterative extrapolation with constraints | support, positivity | alternating projections between the data and the constraints fill part of the wedge; convergence is slow and the result depends on the start (heuristic) |
| Total variation regularization, for example [ASD-POCS](/asd-pocs/) | a piecewise constant image | fills the wedge with the image of least total variation that fits the data; good results in practice, no general guarantee for limited angles (heuristic) |
| Learned methods | a training set | fill the wedge with patterns learned from similar images; no guarantee, and the filled part can be wrong without any sign in the data (heuristic) |

## Bounds

- **Uniqueness (theorem).** Compact support and an open set of angles determine $f$ (Definition).
- **Instability (theorem).** No Sobolev stability estimate holds, by the family $f_K$. The loss is exponential in $K^2\sin^2\delta$ for detail of frequency $K$ with its direction at the angle $\delta$ from the measured range. Davison 1983 shows the ill-conditioning through the structure of the limited-angle operator on the disk.
- **Visible singularities (theorem, cited).** Quinto 1993: a singularity of $f$ at the point $x$ in the direction $\xi$ is stably visible from the data when the line through $x$ perpendicular to $\xi$ is a measured line, that is, when $\xi$ is parallel to $\omega(\theta)$ for some $\theta$ in the interior of $A$. Singularities with directions outside $A$ cannot be recovered stably. This is a statement about the location of edges, not about the values of $f$.

## Reductions

- **Limited angle to Fourier extrapolation.** By the [Fourier slice theorem](/fourier-slice-theorem/), the problem is to extend $\mathcal{F}f$ from a double wedge to the plane, using that $\mathcal{F}f$ is entire for an $f$ of compact support. This is the analytic continuation behind the uniqueness proof, and the source of the instability.
- **Limited angle to local tomography.** The visible edges can be found with a local filter, as in [lambda tomography](/lambda-tomography/), restricted to the measured angles. This gives the edges without trying to fill the wedge.
- **Limited angle to a regularized least squares problem.** Discretize the projections, add a penalty, and solve with an iterative method; the penalty decides how the wedge is filled.

## Applications

- **Electron tomography.** The specimen holder blocks the beam at high tilt angles, so every tilt series has a missing wedge.
- **Breast tomosynthesis and other X-ray tomosynthesis.** The source moves over a small arc above the detector, so the data cover only a small range of angles.
- **Flat objects.** When a large flat object or the scanner frame blocks part of the arc of directions, only the remaining arc is measured.
- **Short-scan CT with a reduced arc.** Scans shorter than the short scan of [fan-beam filtered back-projection](/fan-beam-filtered-back-projection/), for example to reduce motion, become limited-angle problems.

## References
