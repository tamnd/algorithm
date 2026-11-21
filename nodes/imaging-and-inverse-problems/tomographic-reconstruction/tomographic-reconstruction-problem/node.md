---
tag: JDNNZ7
kind: problem
slug: tomographic-reconstruction-problem
name: Tomographic reconstruction
aliases:
- image reconstruction from projections
area: imaging-and-inverse-problems/tomographic-reconstruction
level: intro
summary: Recover a function on the plane or in space from its integrals along many lines or planes, such as the X-ray attenuation map from CT projections.
model: real-ram
prereqs: [radon-transform, inverse-problem]
see_also: [inverse-problem, fredholm-integral-equation-first-kind, emission-tomography-model, discrete-tomography, single-particle-reconstruction, mri-reconstruction-problem, calderon-problem, phase-retrieval]
sources:
  - paper: "J. Radon, Über die Bestimmung von Funktionen durch ihre Integralwerte längs gewisser Mannigfaltigkeiten, Berichte über die Verhandlungen der Königlich-Sächsischen Gesellschaft der Wissenschaften zu Leipzig, Math.-Phys. Klasse 69, 1917, pages 262 to 277"
    locator: the recovery of a function on the plane from its integrals along all lines
  - paper: doi:10.1063/1.1729798
    title: A. M. Cormack, Representation of a function by its line integrals, with some radiological applications, Journal of Applied Physics 34(9), 1963
    locator: pp. 2722 to 2727 (the reconstruction problem for radiology and a solution by circular harmonic expansions)
  - paper: doi:10.1259/0007-1285-46-552-1016
    title: G. N. Hounsfield, Computerized transverse axial scanning (tomography), Part 1, Description of system, British Journal of Radiology 46(552), 1973
    locator: pp. 1016 to 1022 (the first clinical CT scanner)
  - paper: doi:10.1090/S0002-9904-1977-14406-6
    title: K. T. Smith, D. C. Solmon and S. L. Wagner, Practical and mathematical aspects of the problem of reconstructing objects from radiographs, Bulletin of the American Mathematical Society 83(6), 1977
    locator: pp. 1227 to 1270 (finitely many projections do not determine an object; uniqueness from infinitely many)
  - book: isbn:9780898714937
    title: F. Natterer, The Mathematics of Computerized Tomography, SIAM Classics in Applied Mathematics 32, 2001
    locator: Chapter II (uniqueness, inversion and Sobolev estimates), Chapter III (sampling and resolution), Chapter IV (ill-posedness and the singular value decomposition) and Chapter V (reconstruction algorithms)
  - book: isbn:9780898714944
    title: A. C. Kak and M. Slaney, Principles of Computerized Tomographic Imaging, SIAM Classics in Applied Mathematics 33, 2001
    locator: Chapter 3 (parallel and fan-beam projections, the Fourier slice theorem and filtered back-projection) and Chapter 7 (algebraic reconstruction algorithms)
---

Tomographic reconstruction is the problem of recovering a function $f$ from its integrals along lines, or in some settings along planes. In X-ray computed tomography (CT), $f$ is the attenuation coefficient of a slice of the body, and each detector reading gives the integral of $f$ along one ray, by the [Beer-Lambert law](/beer-lambert-law/). The complete set of line integrals in the plane is the [Radon transform](/radon-transform/) $\mathcal{R}f$, and the problem is to invert it from finitely many noisy samples. With all lines the answer is unique and has an explicit formula. With finitely many lines it is not unique in theory, and in practice it is mildly ill-posed: noise at high frequencies grows in the reconstruction. Methods trade speed, accuracy and robustness to noise and missing data.

## In plain words

Shine a thin X-ray beam through an object and measure how much of it comes out. The loss tells you the total density along the path of the beam, but not where on the path the dense parts are. Now repeat this for many parallel beams, and then turn the object a little and repeat again, until the beams have crossed the object from every side. Each point of the object lies on many beams, and the task is to find the density at each point that explains all the measured totals.

A doctor's CT scanner does this for one thin slice at a time, and a computer turns the totals into the image. The same puzzle appears whenever a measurement adds up a quantity along a path: in nuclear medicine, in electron microscopes, in radio astronomy and in seismology.

## Definition

**The continuous problem.** Let $f$ be a function on $\mathbb{R}^2$ with support in the unit disk. Use $\omega(\theta) = (\cos\theta, \sin\theta)$ and $\omega^\perp(\theta) = (-\sin\theta, \cos\theta)$. The line with normal $\omega(\theta)$ at signed distance $s$ from the origin is $\{s\,\omega + t\,\omega^\perp : t \in \mathbb{R}\}$, and the data are
$$\mathcal{R}f(\theta, s) = \int_{-\infty}^{\infty} f(s\,\omega(\theta) + t\,\omega^\perp(\theta))\,dt, \qquad \theta \in [0, \pi),\ s \in \mathbb{R}.$$
The task is to find $f$ from $g = \mathcal{R}f$, or from samples of $g$. In $\mathbb{R}^3$ the data are either the integrals along lines (the [X-ray transform](/x-ray-transform/), as in CT) or the integrals over planes (the 3D Radon transform).

**The measurement.** A monochromatic X-ray beam of intensity $I_0$ that crosses the object along the line $L_i$ comes out with the intensity $I_0\exp(-\int_{L_i} f)$. A photon-counting detector records a count
$$y_i \sim \mathrm{Poisson}\big(I_0\, e^{-\int_{L_i} f} + b_i\big),$$
with a known background $b_i \ge 0$, independently for each ray. The log data $p_i = -\ln(y_i/I_0)$ approximate the line integral. For high counts and $b_i = 0$, $p_i$ is close to Gaussian with mean $\int_{L_i} f$ and variance about $1/y_i$, which gives a weighted least squares data term. This is an approximation for high counts, not an exact change of model. It fails for rays through dense material, where $y_i$ is small or zero.

**The discrete problem.** Represent $f$ by $N$ pixel values $x \in \mathbb{R}^N$. Then $\int_{L_i} f \approx (Ax)_i$, where the system matrix $A$ has $m$ rows, one per ray, and $a_{ij}$ is the length of ray $i$ in pixel $j$ ([Siddon's algorithm](/siddon-algorithm/)) or an interpolation weight ([Joseph's projector](/joseph-projector/)). The problem is to find $x \ge 0$ from $p \approx Ax$, or from the counts $y$. Each row of $A$ has $O(\sqrt{N})$ nonzero entries, so $A$ is sparse, but it is too large to factor for real images.

**Parallel-beam sampling.** The standard data set is a [sinogram](/sinogram/): $a$ angles $\theta_k = k\pi/a$ and $d$ detector bins at $s_j = (j - (d-1)/2)\tau$ with spacing $\tau$. The output is an $n \times n$ image on $[-1, 1]^2$.

## Variants

- **Parallel beam.** One source direction at a time, as in the definition. This is the model of the analysis and of the first scanner generations.
- **Fan beam.** A point source and a line or arc of detectors, as in modern CT. The data can be reordered into parallel form by [fan-to-parallel rebinning](/fan-to-parallel-rebinning/) or inverted directly by [fan-beam filtered back-projection](/fan-beam-filtered-back-projection/).
- **Cone beam.** A point source and a 2D detector, for 3D volumes. A circular source orbit does not meet the [Tuy condition](/tuy-condition/), and the [Feldkamp-Davis-Kress](/feldkamp-davis-kress/) method is approximate. A helical orbit meets it, and the [Katsevich algorithm](/katsevich-algorithm/) is exact. The [Grangeat formula](/grangeat-formula/) links cone-beam data to the 3D Radon transform.
- **Limited angle.** The angles cover only part of $[0, \pi)$. The data still determine a compactly supported $f$, but the problem becomes severely ill-posed. See [limited-angle tomography](/limited-angle-tomography/).
- **Interior and truncated data.** Only the lines through a region of interest are measured. The data do not determine $f$ there in general. See [interior tomography](/interior-tomography/) and [lambda tomography](/lambda-tomography/), which recovers the edges but not the values.
- **Sparse view.** Far fewer angles than the sampling rule asks for, to lower the dose. See [sparse-view CT reconstruction](/sparse-view-ct-reconstruction/), where a prior such as total variation fills the gaps.
- **Emission tomography.** In PET and SPECT the unknown is the activity of a tracer and the data are Poisson counts of photons emitted inside the body. See the [emission tomography model](/emission-tomography-model/) and the [attenuated Radon transform](/attenuated-radon-transform/).
- **Discrete tomography.** The image takes only a few known values, such as 0 and 1, and the data are a few projections. See [discrete tomography](/discrete-tomography/).
- **Nonlinear effects.** A polychromatic beam breaks the linear model ([beam hardening](/beam-hardening/)), and metal blocks some rays ([metal artifact reduction](/metal-artifact-reduction/)).

## Examples

**A disk.** For $f = 1$ on the unit disk, $\mathcal{R}f(\theta, s) = 2\sqrt{1 - s^2}$ for $|s| \le 1$ at each angle. Every reconstruction method should give back the constant 1 inside the disk, up to an error at the edge.

**Two directions are not enough.** Take the $2 \times 2$ images
$$x = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix}, \qquad x' = \begin{pmatrix} 0 & 1 \\ 1 & 0 \end{pmatrix}.$$
Both have the row sums $(1, 1)$ and the column sums $(1, 1)$, so the horizontal and vertical projections cannot tell them apart. The sum along the main diagonal is 2 for $x$ and 0 for $x'$, so a third direction does. The same thing happens for any finite set of directions in the continuous problem: Smith, Solmon and Wagner showed that for each finite set of directions there are nonzero smooth functions, with support in any given disk, whose projections in all of these directions are zero.

**The noise of one ray.** With $I_0 = 10^4$ photons and a line integral of 1.6, the expected count is $10^4 e^{-1.6} = 2019$. The log data then have a standard deviation of about $1/\sqrt{2019} = 0.022$, about 1.4 percent of the line integral. A ray with a line integral of 6 has an expected count of 25 and a standard deviation of 0.2 in the log data, and the Gaussian approximation is poor there.

**Data against unknowns.** A sinogram with $a = 32$ angles and $d = 47$ bins has 1504 values, and a $32 \times 32$ image has 1024 unknowns. More equations than unknowns does not make the system well conditioned: the small singular values of $A$ come from the decay of the singular values of $\mathcal{R}$.

## Known algorithms

| Method | Data | What it gives |
|---|---|---|
| [Filtered back-projection](/filtered-back-projection/) | full parallel-beam sinogram | the discrete form of the [Radon inversion formula](/radon-inversion-formula/): a [ramp filter](/ramp-filter/) and a [back projection](/back-projection-operator/); $O(a d \log d + a n^2)$ time |
| [Direct Fourier reconstruction](/direct-fourier-reconstruction/) | full parallel-beam sinogram | the [Fourier slice theorem](/fourier-slice-theorem/), interpolation from the polar grid and one inverse 2D FFT; $O(a d \log d + n^2 \log n)$ time, less accurate at high frequencies |
| [Fan-beam FBP](/fan-beam-filtered-back-projection/), [Feldkamp-Davis-Kress](/feldkamp-davis-kress/), [Katsevich](/katsevich-algorithm/) | fan-beam and cone-beam data | analytic inversion for the scanner geometry; FDK is approximate off the plane of the orbit |
| ART, the [Kaczmarz method](/kaczmarz-method/) | any rays, $p \approx Ax$ | projects onto one ray equation at a time; for a consistent system and the start $x = 0$ it converges to the solution of least norm |
| [SART](/sart/) and [SIRT](/sirt/) | any rays | weighted [Landweber iterations](/landweber-iteration/) with all rays of one view (SART) or all rays (SIRT); smoother than ART on noisy data |
| [CGLS](/cgls/) | any rays | conjugate gradients on the normal equations; the iteration count acts as a regularization parameter |
| [MLEM](/mlem-reconstruction/) and [OSEM](/osem/) | Poisson counts | MLEM increases the Poisson likelihood at each step and keeps $x \ge 0$; OSEM uses subsets of the data and is faster, but it is not monotone and does not converge in general |
| [Separable paraboloidal surrogates](/separable-paraboloidal-surrogates/) | transmission counts | penalized likelihood with a monotone update |
| [ASD-POCS](/asd-pocs/) | sparse or limited data | alternates data consistency and steps that lower the total variation |

## Bounds

- **Uniqueness from all lines.** If $f$ is integrable with compact support, $\mathcal{R}f$ determines $f$. By the Fourier slice theorem, the 1D transforms of the projections give the 2D Fourier transform of $f$ on every line through the origin, so on the whole plane. The Radon inversion formula gives $f$ explicitly.
- **Non-uniqueness from finitely many lines.** Finitely many projections never determine $f$ (Smith, Solmon and Wagner 1977), as in the example above. Projections in infinitely many directions do determine a compactly supported $f$. So any finite scanner relies on a band limit or another prior, such as the pixel model.
- **Stability.** For $f$ with support in the unit disk, the Radon transform gains half a derivative: $\|f\|_{H^\alpha}$ and $\|\mathcal{R}f\|_{H^{\alpha + 1/2}}$ bound each other up to constants (Natterer, Chapter II). On the disk its distinct singular values decay like $m^{-1/2}$ (Natterer, Chapter IV). So the inversion is mildly ill-posed, of [degree](/degree-of-ill-posedness/) $1/2$ in the Sobolev sense. Limited-angle data make it severely ill-posed.
- **Sampling.** To resolve an image of bandwidth $b$ on the unit disk, the detector spacing must be about $1/(2b)$ and the number of angles about $\pi d/2$ for $d$ bins (Natterer, Chapter III). The derivation of $a \approx \pi d/2$ is on the [filtered back-projection](/filtered-back-projection/) page.
- **Cost.** Reading the data takes $\Omega(a d)$ time and writing the image $\Omega(n^2)$. Filtered back-projection takes $O(a n^2)$ for the back projection, and direct Fourier reconstruction reaches $O(n^2 \log n)$ when $a d = O(n^2)$. An iterative method costs one application of $A$ and one of $A^T$ per sweep, each $O(a d n)$ for ray-driven projectors, times the number of sweeps.

## Reductions

- **To Fourier interpolation.** By the Fourier slice theorem, reconstruction from a full sinogram is the same as interpolating the 2D Fourier transform from samples on radial lines and inverting it.
- **To a linear integral equation.** $\mathcal{R}f = g$ is a [Fredholm integral equation of the first kind](/fredholm-integral-equation-first-kind/), so the general theory of regularization applies: truncated SVD, Tikhonov and iterative methods with early stopping.
- **To a sparse linear system.** The pixel model gives $Ax = p$, a large sparse system that row-action methods such as the Kaczmarz method solve without forming $A^T A$.
- **To likelihood maximization.** With Poisson counts, the problem is to maximize a concave log-likelihood over $x \ge 0$, as in MLEM for emission data.
- **Cone beam to the 3D Radon transform.** The Grangeat formula turns cone-beam data into derivatives of plane integrals, so 3D CT reduces to the inversion of the 3D Radon transform where the data cover the planes.

## Applications

- **Medical CT.** Cormack (1963) found an inversion by circular harmonic expansions and applied it to the attenuation map of radiology, without knowing Radon's work. Hounsfield (1973) described the first clinical CT scanner. The two shared the 1979 Nobel Prize in Physiology or Medicine. Radon had solved the mathematical problem in 1917, without the application.
- **Nuclear medicine.** PET and SPECT reconstruct the activity of a tracer from emission counts, with MLEM and OSEM as the standard methods.
- **Industrial and scientific CT.** Nondestructive testing of parts, and micro-CT of materials and fossils at synchrotrons.
- **Electron microscopy.** Electron tomography of tilted specimens is a limited-angle problem, and [single-particle reconstruction](/single-particle-reconstruction/) finds the angles of the projections as part of the problem.
- **Radio astronomy.** Bracewell reconstructed the brightness of radio sources from strip scans in 1956, through the Fourier slice relation.
- **Geophysics.** Travel-time tomography finds the slowness of the Earth from integrals along ray paths, which bend, so the problem is nonlinear.

## References
