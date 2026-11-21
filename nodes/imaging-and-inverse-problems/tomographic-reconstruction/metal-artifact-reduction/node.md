---
tag: CKBSPQ
kind: problem
slug: metal-artifact-reduction
name: Metal artifact reduction
aliases:
- MAR
area: imaging-and-inverse-problems/tomographic-reconstruction
level: advanced
summary: "Remove the streaks that metal implants cause in CT, usually by finding the corrupted rays and replacing or reweighting them before reconstruction."
model: real-ram
prereqs: [tomographic-reconstruction-problem, sinogram, beam-hardening]
see_also: [beam-hardening, image-inpainting, filtered-back-projection, osem, mlem-reconstruction, sparse-view-ct-reconstruction, limited-angle-tomography, sirt]
sources:
  - paper: "W. A. Kalender, R. Hebel and J. Ebersberger, Reduction of CT artifacts caused by metallic implants, Radiology, 1987"
    locator: replacing the projection values in the metal trace by interpolation from the neighboring values (general locator)
  - paper: "Esther Meyer, Rainer Raupach, Michael Lell, Bernhard Schmidt and Marc Kachelriess, Normalized metal artifact reduction (NMAR) in computed tomography, Medical Physics, 2010"
    locator: normalization of the sinogram by the projection of a prior image before interpolation (general locator)
  - book: isbn:9780898714944
    title: A. C. Kak and M. Slaney, Principles of Computerized Tomographic Imaging, SIAM Classics in Applied Mathematics 33, 2001
    locator: Chapter 4 (polychromaticity and other sources of error in projection data) and Chapter 5 (artifacts in reconstructed images)
---

Metal artifact reduction (MAR) asks for a CT image of a patient with metal implants, such as hip prostheses, dental fillings or surgical clips, without the dark and bright streaks that metal causes in a standard reconstruction. Metal attenuates X-rays so strongly that the rays through it violate the linear model of [tomographic reconstruction](/tomographic-reconstruction-problem/): the beam hardens strongly ([beam hardening](/beam-hardening/)), few photons reach the detector, scatter adds a large relative error, and the edges of the metal fall partly inside pixels. [Filtered back-projection](/filtered-back-projection/) spreads the errors of these rays across the whole image as streaks. The rays that cross the metal form the metal trace in the [sinogram](/sinogram/). Most methods find this trace, and then either replace its values, as in the linear interpolation of Kalender, Hebel and Ebersberger (1987) and the normalized method NMAR of Meyer and others (2010), or give them a low weight in an iterative reconstruction. All practical methods are heuristics.

## In plain words

A CT scanner measures how much each X-ray is weakened on its way through the body. Metal weakens the rays so much that almost nothing arrives, and the little that arrives is measured badly. The computer does not know this. It spreads the bad values back over the image, and the image gets long dark and bright stripes that start at the metal.

Most fixes work in two steps. First, find the metal in a first image and mark all rays that pass through it. Then do not trust these rays: fill in their values from their neighbors, or from a rough guess of what the body looks like, or let the reconstruction ignore them. The stripes mostly go away, but the tissue right next to the metal stays hard to see.

## Definition

Let $y_i = -\ln(I_i / I_0)$ be the log data of the rays $i = 1, \dots, m$ of a scan, and $A$ the system matrix of the linear model $y = A x + e$. Let $K$ be the set of pixels covered by metal, and the **metal trace** $T = \{ i : a_{ij} > 0 \text{ for some } j \in K \}$ the set of rays that cross it. The data on $T$ do not follow the linear model, and their error is large and not random: it depends on the metal and on the other matter on the ray.

The problem is: given $y$ and the scanner geometry, find an image $x$ that is close to the true attenuation outside $K$ and has no streaks, together with an estimate of $K$. Two standard formulations are:

- **Sinogram completion.** Replace $y_i$ for $i \in T$ by values $\hat y_i$ computed from the data outside $T$ (and possibly from a prior image), reconstruct from the completed sinogram, and insert the metal back.
- **Weighted fit.** Solve $\min_x \sum_{i \notin T} w_i (\langle a_i, x\rangle - y_i)^2 + R(x)$, or a weighted likelihood, with low or zero weights on the trace and a regularizer $R$.

The metal set $K$ is usually found by thresholding a first FBP image, because metal has far higher attenuation than bone.

## Variants

- **Projection domain or image domain.** Methods change the sinogram (interpolation, inpainting), the image (filtering the streaks), or both in turn.
- **Physics correction.** Model the polychromatic beam, scatter and noise in a statistical reconstruction, and keep the metal rays with their correct, low weights.
- **Dual-energy CT.** Combine two spectra into a virtual monoenergetic image at a high energy, where beam hardening is smaller.
- **Learned methods.** Networks trained on simulated metal in clinical images complete the sinogram, clean the image, or both.
- **Known implant.** If the shape and material of the implant are known, such as a prosthesis from a catalog, the method can model it exactly and solve only for the patient.

## Examples

**One view, by hand.** Consider one row of the sinogram with 6 bins. The bins 2 and 3 are in the metal trace, and the measured values of bins 1 and 4 are 2 and 3. A prior image (for example, the tissue classes air, soft tissue and bone, found by thresholding a first image) has the forward projection $q = (1, 2, 4, 4, 2, 1)$ in this view. Its value 4 in bins 2 and 3 says that a bone lies behind the metal in this view.

- **Linear interpolation** (Kalender, Hebel and Ebersberger) draws a straight line from bin 1 to bin 4: $\hat y_2 = 2 + \tfrac13 = \tfrac73$ and $\hat y_3 = 2 + \tfrac23 = \tfrac83$. The bone behind the metal disappears from this view.
- **NMAR** (Meyer and others) divides by the prior first: the normalized values at bins 1 and 4 are $2/2 = 1$ and $3/2 = \tfrac32$. It interpolates them, $\tfrac76$ and $\tfrac43$, and multiplies back by the prior: $\hat y_2 = \tfrac76 \cdot 4 = \tfrac{14}{3}$ and $\hat y_3 = \tfrac43 \cdot 4 = \tfrac{16}{3}$. The values keep the bump of the bone.

The completed row of NMAR is closer to the truth when the prior is right, and it can be worse when the prior misclassifies tissue (a heuristic).

**Why interpolation adds new streaks.** A completed sinogram is in general not the sinogram of any image: the interpolated values in different views do not agree on one image. So linear interpolation removes the streaks of the metal but often creates weaker new streaks that are tangent to the metal, and it blurs the tissue next to the metal. This is an observed behavior, not a theorem.

## Known algorithms

| Method | Idea | Status |
|---|---|---|
| Linear interpolation (Kalender, Hebel and Ebersberger 1987) | replace the trace by interpolation along the detector in each view | fast; removes strong streaks, adds weaker new ones; a heuristic |
| NMAR (Meyer and others 2010) | interpolate the sinogram after dividing it by the projection of a prior image | keeps more structure near the metal; depends on the prior; a heuristic |
| [Inpainting](/image-inpainting/) of the sinogram | fill the trace with smooth or TV-regularized inpainting | uses more of the sinogram structure; a heuristic |
| Weighted iterative reconstruction ([SIRT](/sirt/), [MLEM](/mlem-reconstruction/), [OSEM](/osem/)) | low or zero weights on the trace, then a regularized solve | slower; avoids inconsistent filled data; converges for the weighted model, which is itself an approximation |
| Polychromatic statistical reconstruction | model the spectrum and the noise of the metal rays | the most physically faithful; slow and needs a calibrated model |
| Dual-energy monoenergetic images | combine two spectra into a high-energy image | reduces beam hardening, not photon starvation |
| Learned sinogram or image completion | networks trained on simulated metal | strong results on data like the training set; no guarantee outside it |

## Bounds

- **Lost information (theorem).** If the rays of the trace are discarded, the data outside $T$ still determine the image outside the convex hull of the metal, for an image with compact support: this is the exterior problem of the Radon transform, which has uniqueness by Helgason's support theorem. The image inside the convex hull is not determined by these data, and the reconstruction outside it is severely unstable near the hull. So no method can recover the tissue between two implants from the remaining rays alone; it must use a prior or the corrupted rays.
- **Noise of the metal rays (theorem for a Poisson model, to first order).** If the detector counts $N$ photons with a Poisson distribution of mean $\bar N$, then the variance of $-\ln(N/N_0)$ is about $1/\bar N$ for large $\bar N$. Metal lowers $\bar N$ by orders of magnitude, so the noise of these rays grows by the same factor, and for $\bar N$ near 0 the log is not even defined.
- **No convergence theory for the heuristics.** Interpolation methods are one-shot maps, not solvers of a stated problem, so there is no sense in which they converge to a correct image. The quality of MAR methods is known from measurements on phantoms and clinical cases.

## Reductions

- **To sinogram inpainting.** With the trace treated as missing data, MAR becomes [inpainting](/image-inpainting/) on the sinogram, with the extra knowledge that the result should be a consistent sinogram.
- **To weighted least squares.** With weights 0 on the trace, the problem is the reconstruction from an incomplete data set, as in [limited-angle](/limited-angle-tomography/) and [sparse-view CT](/sparse-view-ct-reconstruction/), but with a missing set of rays shaped by the metal.
- **To beam hardening correction.** If the only error were beam hardening, a polychromatic model of metal and tissue would remove it; photon starvation and scatter make this reduction incomplete.

## Applications

- **Orthopedic CT.** Hip and knee prostheses, spinal screws and plates.
- **Dental and head CT.** Fillings, crowns and implants, including cone-beam CT for dental planning.
- **Radiotherapy planning.** The attenuation values of the CT image set the dose calculation, so streaks give dose errors near implants.
- **Interventional imaging.** Needles, coils and clips in images taken during a procedure.
- **Industrial CT.** Objects with dense metal parts next to light materials.

## References
