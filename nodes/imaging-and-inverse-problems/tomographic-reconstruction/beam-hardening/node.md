---
tag: 94KWMW
kind: concept
slug: beam-hardening
name: Beam hardening
aliases:
- beam hardening artifact
area: imaging-and-inverse-problems/tomographic-reconstruction
level: advanced
summary: "The rise in mean energy of a polychromatic X-ray beam as it passes through matter, which breaks the linear model and causes cupping and streaks."
prereqs: [beer-lambert-law, x-ray-transform]
see_also: [metal-artifact-reduction, filtered-back-projection, tomographic-reconstruction-problem, sinogram, radon-transform, polynomial-interpolation, sirt, separable-paraboloidal-surrogates]
sources:
  - paper: "R. A. Brooks and G. Di Chiro, Beam hardening in X-ray reconstructive tomography, Physics in Medicine and Biology, 1976"
    locator: the polychromatic model, the cupping of uniform objects and the correction by a water calibration (general locator)
  - book: isbn:9780898714944
    title: A. C. Kak and M. Slaney, Principles of Computerized Tomographic Imaging, SIAM Classics in Applied Mathematics 33, 2001
    locator: Chapter 4 (measurement of projection data with polychromatic X-rays, and beam hardening artifacts)
---

Beam hardening is the shift of the energy spectrum of an X-ray beam toward higher energies as it passes through matter. Low energies are absorbed more strongly than high ones, so the beam that leaves a thick object is "harder" than the beam that entered it. CT reconstruction assumes the [Beer-Lambert law](/beer-lambert-law/) for one energy, where the log data $p = -\ln(I/I_0)$ are line integrals of one attenuation map $\mu$. A real tube emits a spectrum, and then $p$ grows more slowly than linearly with the path length. [Filtered back-projection](/filtered-back-projection/) of such data gives two typical artifacts: cupping, where a uniform object looks darker in its center, and dark streaks between dense objects such as bones or metal. Brooks and Di Chiro analyzed the effect for CT in 1976.

## In plain words

An X-ray tube does not send light of one color. It sends a mix of weak (soft) and strong (hard) X-rays. Matter stops the soft rays more easily. So a ray that crosses a lot of tissue loses most of its soft part, and what is left is mostly hard and passes the rest of the tissue easily.

The scanner assumes that each centimeter of tissue weakens the ray by the same factor. Because of the hardening, the later centimeters weaken it less than the first ones. So long paths look shorter than they are. The center of a round object, crossed by the longest paths, comes out too dark, and the space between two bones gets dark streaks.

## The idea

**The polychromatic model.** Let $S(E) \ge 0$ be the normalized spectrum of the detected beam, with $\int S(E)\, dE = 1$, and $\mu(x, E)$ the attenuation at the point $x$ and the energy $E$. For the ray $L$, the detector measures
$$\frac{I}{I_0} = \int S(E) \exp\Big(-\int_L \mu(x, E)\, dx\Big)\, dE, \qquad p = -\ln \frac{I}{I_0}.$$
With one energy, $S$ is a point mass and $p = \int_L \mu$, the [X-ray transform](/x-ray-transform/) of $\mu$. With a spectrum, $p$ is not a line integral of any single map.

**One material.** Let the ray cross the length $\ell$ of one material with attenuation $\mu(E)$. Then $p(\ell) = -\ln \int S(E) e^{-\mu(E)\ell}\, dE$. Two facts follow (theorems, by differentiation under the integral):

- $p'(\ell) = \bar\mu(\ell)$, the mean of $\mu(E)$ over the spectrum after filtering, $S(E) e^{-\mu(E)\ell}$ normalized. At $\ell = 0$ this is the mean of $\mu$ over the source spectrum.
- $p''(\ell) = -\operatorname{Var}_\ell(\mu) \le 0$, minus the variance of $\mu(E)$ over the same filtered spectrum. So $p$ is concave, and its slope falls toward the smallest $\mu(E)$ in the spectrum as $\ell$ grows. This is the hardening: the filtered spectrum gives more weight to the energies with small $\mu$.

The slope stays positive when $\mu(E) > 0$ for all $E$, so $p$ is strictly increasing in $\ell$. For an object of one material, the data therefore still determine the path lengths.

**Why cupping.** For a uniform disk of radius $R$, the path at distance $s$ from the center has the length $2\sqrt{R^2 - s^2}$. The longest paths, through the center, lose the most from the concavity of $p$. Filtered back-projection treats the reduced values as line integrals of a smaller attenuation near the center, so the profile of the image sags in the middle.

**Why streaks.** With two materials, such as water and bone, the value of $p$ depends on both path lengths separately, not on one weighted sum of them. No single correction of each $p$ can make all rays consistent with one attenuation map. The rays that pass through two dense objects are hardened the most, and their error is not shared by the nearby rays, so the back-projection spreads it as dark streaks along these rays.

**Water correction (a heuristic for mixed objects).** Measure or compute $p$ for known water thicknesses, fit the inverse map $\ell \approx \sum_k a_k p^k$ by a low-degree polynomial, and replace each measured $p$ by $\mu_0\, \ell(p)$, where $\mu_0$ is a reference attenuation of water. For an object made only of water, an exact inverse map removes the cupping, because $p$ is strictly increasing (a theorem); the polynomial is an approximation of that map. For objects with bone or metal, the correction is a heuristic, and two-pass methods first segment the bone, estimate its path lengths by reprojection, and correct again.

## Examples

**A two-energy spectrum.** Take two energies of equal weight, and a water-like material with $\mu = 0.4$ and $0.2$ per cm at the two energies. Then
$$p(\ell) = -\ln\big(\tfrac12 e^{-0.4\ell} + \tfrac12 e^{-0.2\ell}\big),$$
with the initial slope $\bar\mu(0) = 0.3$. The linear model would give $0.3\,\ell$. The values are (computed):

| $\ell$ (cm) | 1 | 2 | 5 | 10 | 20 |
|---|---|---|---|---|---|
| $p(\ell)$ | 0.295 | 0.580 | 1.380 | 2.566 | 4.675 |
| $0.3\,\ell$ | 0.3 | 0.6 | 1.5 | 3.0 | 6.0 |

You can check the case $\ell = 10$ by hand: $\tfrac12(e^{-4} + e^{-2}) = \tfrac12(0.01832 + 0.13534) = 0.07683$, and $-\ln 0.07683 = 2.566$. A path of 10 cm looks like 8.55 cm of water at the slope 0.3. As $\ell$ grows, the slope of $p$ falls toward 0.2.

**Water correction fails on mixed rays.** Add a bone-like material with $\mu = 1.2$ and $0.4$ per cm, so the ideal linear value is $0.8$ per cm. Correct each $p$ with the exact water inverse map, and then multiply by 0.3 (computed values):

- 1 cm of bone alone: $p = 0.722$, corrected to $0.753$, while the ideal value is $0.8$.
- 10 cm of water and 1 cm of bone on the same ray: $p = 3.034$, corrected to $3.639$, while the ideal value is $3.8$.
- The water part alone corrects to exactly $3.0$, so the bone adds $0.639$ on the mixed ray but $0.753$ on its own.

The error of the bone depends on the other matter on the ray. This is the inconsistency that produces streaks, and the reason why a one-material correction cannot remove them.

## Where it is used

- **Medical CT.** Every clinical scanner applies a water correction, often with a bowtie filter and a flat filter that pre-harden the beam. Bone correction by two-pass methods reduces the dark bands in head scans.
- **Metal artifacts.** Metal hardens the beam far more than bone and also starves the detector, so beam hardening is one of the causes treated in [metal artifact reduction](/metal-artifact-reduction/).
- **Dual-energy and spectral CT.** Two spectra or energy-resolving detectors measure enough data to separate two basis materials, which removes the beam hardening of these materials in principle and gives material maps.
- **Polychromatic statistical reconstruction.** Model-based methods put the polychromatic model into the likelihood and solve for the material fractions with iterative methods, at a higher cost than FBP.
- **Industrial CT.** Metal parts cause strong cupping; correction curves are measured on step wedges of the same material.

## References
