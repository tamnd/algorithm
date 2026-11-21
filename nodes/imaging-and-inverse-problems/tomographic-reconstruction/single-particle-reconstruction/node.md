---
tag: MEJT41
kind: problem
slug: single-particle-reconstruction
name: Single-particle reconstruction
aliases:
- cryo-EM reconstruction
area: imaging-and-inverse-problems/tomographic-reconstruction
level: advanced
summary: Recover a 3D molecule density from many noisy 2D cryo-electron microscope projections taken at unknown orientations.
model: real-ram
prereqs: [fourier-slice-theorem, tomographic-reconstruction-problem, radon-transform]
see_also: [common-lines-method, expectation-maximization, maximum-likelihood-estimation, direct-fourier-reconstruction, nonuniform-fft, wiener-filter, rotation-averaging, method-of-moments]
sources:
  - book: isbn:9780195182187
    title: J. Frank, Three-Dimensional Electron Microscopy of Macromolecular Assemblies, Oxford University Press, 2006
    locator: general locator (the image formation model, the single-particle methods and the resolution measures)
  - paper: doi:10.1016/0304-3991(87)90078-7
    title: M. van Heel, Angular reconstitution, a posteriori assignment of projection directions for 3D reconstruction, Ultramicroscopy 21(2), 1987
    locator: pp. 111 to 123 (orientations of unknown projections from their common lines)
  - paper: doi:10.1137/090767777
    title: A. Singer and Y. Shkolnisky, Three-dimensional structure determination from common lines in cryo-EM by eigenvectors and semidefinite programming, SIAM Journal on Imaging Sciences 4(2), 2011
    locator: pp. 543 to 572 (all orientations at once from the common lines)
  - paper: doi:10.1006/jsbi.1998.4014
    title: F. J. Sigworth, A maximum-likelihood approach to single-particle image refinement, Journal of Structural Biology 122(3), 1998
    locator: pp. 328 to 339 (the orientations and shifts as hidden variables, integrated out in a likelihood)
  - paper: doi:10.1016/j.jsb.2012.09.006
    title: S. H. W. Scheres, RELION, implementation of a Bayesian approach to cryo-EM structure determination, Journal of Structural Biology 180(3), 2012
    locator: pp. 519 to 530 (maximum a posteriori estimation of the map by expectation maximization over the orientations)
  - paper: doi:10.1038/nmeth.4169
    title: A. Punjani, J. L. Rubinstein, D. J. Fleet and M. A. Brubaker, cryoSPARC, algorithms for rapid unsupervised cryo-EM structure determination, Nature Methods 14(3), 2017
    locator: pp. 290 to 296 (a first model from random starts by stochastic gradient descent, and branch and bound over the orientations)
  - paper: doi:10.1016/0022-5193(80)90088-0
    title: Z. Kam, The reconstruction of structure from electron micrographs of randomly oriented particles, Journal of Theoretical Biology 82(1), 1980
    locator: pp. 15 to 39 (the structure from the averaged correlations of many images, without the orientations)
  - paper: doi:10.1137/18M1214317
    title: A. Perry, J. Weed, A. S. Bandeira, P. Rigollet and A. Singer, The sample complexity of multireference alignment, SIAM Journal on Mathematics of Data Science 1(3), 2019
    locator: pp. 497 to 517 (the number of observations grows like 1/SNR at high SNR and like 1/SNR^3 at low SNR)
---

Single-particle reconstruction asks for the 3D density of a molecule from many 2D images taken in a cryo-electron microscope. Each image shows one copy of the molecule, frozen in ice in a random and unknown orientation. By the [Fourier slice theorem](/fourier-slice-theorem/), each image gives one central plane of the 3D Fourier transform of the density. If the orientations were known, the problem would be the linear [tomographic reconstruction problem](/tomographic-reconstruction-problem/). They are not known, and the images are very noisy, because the electron dose must be low to keep the molecule intact. So the problem is to estimate the density and the orientations together, from tens of thousands to millions of images. The answer is fixed only up to a global rotation and a reflection: the mirror image of the molecule gives the same images.

## In plain words

You want the 3D shape of a molecule. You cannot photograph one molecule from all sides. Instead, you freeze many copies, each lying in a random direction, and take one flat shadow picture of each copy with an electron microscope.

Two things make this hard. First, nobody knows which way each copy was facing. Second, each picture is mostly noise, because a stronger beam would destroy the molecule.

So you must work out the shape and the directions at the same time. Methods compare the pictures with each other or with guesses of the shape, and improve both step by step. With enough pictures the noise averages out, and the shape can come out sharp enough to show single atoms. One thing always stays open: a mirror copy of the molecule gives the same pictures.

## Definition

Let $f$ be a density on $\mathbb{R}^3$ with support in the unit ball. For a rotation $R$, the projection of $f$ along the beam $R e_3$ is the image
$$(\mathcal{P}_R f)(x, y) = \int f\big(R (x, y, z)^T\big)\, dz.$$
An image covers $[-1, 1]^2$ and is sampled on an $n \times n$ grid with the pixel centers $x_j = -1 + (2j+1)/n$ and $y_i = 1 - (2i+1)/n$. The data are $m$ images
$$I_i = h_i * \big(\mathcal{P}_{R_i} f\big)(\cdot - t_i) + \varepsilon_i, \qquad i = 1, \dots, m,$$
where the rotations $R_i$ are unknown and drawn from some distribution on the rotation group, often close to uniform, the shifts $t_i \in \mathbb{R}^2$ are unknown, $h_i$ is the point spread function of the microscope (its Fourier transform is the contrast transfer function, which has zeros and changes sign), and $\varepsilon_i$ is noise, usually modeled as Gaussian. With $\mathcal{F} g(\xi) = \int g(x) e^{-2\pi i x \cdot \xi}\, dx$, the slice theorem gives
$$\mathcal{F} I_i(k) = \mathcal{F} h_i(k)\, e^{-2\pi i k \cdot t_i}\, \mathcal{F} f\big(R_i (k_1, k_2, 0)^T\big) + \mathcal{F} \varepsilon_i(k), \qquad k \in \mathbb{R}^2.$$
The task is to estimate $f$. The orientations and shifts are nuisance parameters; most methods estimate them too.

**What the data can determine.** For any rotation $G$, the density $f(G^T x)$ with the rotations $G R_i$ gives the same images as $f$ with $R_i$. For the reflection $J = \mathrm{diag}(1, 1, -1)$, the density $f(J x)$ with the rotations $J R_i J$ also gives the same images, because $\int f(R_i (x, y, -z)^T)\, dz = \int f(R_i (x, y, z)^T)\, dz$ (a theorem). So $f$ can at best be found up to a rotation and a reflection, and the handedness must come from other information. Shifts add a translation of $f$ when the centers are not known.

**The signal-to-noise ratio.** The SNR of an image is the energy of the clean projection over the energy of the noise. In cryo-EM it is often well below 1 (a heuristic about the practice, not a fixed number).

## Variants

- **Known orientations.** If the $R_i$ are known, the problem is linear: 3D reconstruction from projections, solved by [direct Fourier reconstruction](/direct-fourier-reconstruction/) on a nonuniform grid, weighted back-projection or iterative methods.
- **Orientation estimation alone.** Find the $R_i$ up to a global rotation and the reflection, as in the [common lines method](/common-lines-method/). This is a synchronization problem over the rotation group, close to [rotation averaging](/rotation-averaging/).
- **Cryo-electron tomography.** One object is imaged in a tilt series with known tilt angles about one axis, and the tilt range is limited, so a wedge of Fourier space is missing. Averaging many copies cut out of such tomograms (subtomogram averaging) brings back the unknown orientations.
- **Symmetric particles.** If the molecule has a point group symmetry, such as an icosahedral virus, the orientations are fixed only up to the symmetry, and each image gives several central planes.
- **Heterogeneity.** The copies are in several states or move continuously. Then the data are a mixture, and the task is to find several densities, or a family of them, and assign the images.
- **2D classification.** Group the images by view and average each group, which raises the SNR. The averages are the input of many orientation methods.
- **Multi-reference alignment.** The model problem in one dimension: copies of a signal under random cyclic shifts with noise. It keeps the unknown group element and the noise and drops the projection.

## Examples

**A sphere has no orientation.** Let $f$ be a centered Gaussian, $f(x) = \exp(-|x|^2/(2s^2))$. Then every projection is $\sqrt{2\pi}\, s\, \exp(-(x^2 + y^2)/(2s^2))$, the same for every $R$. The images carry no information about the orientations, and the problem is solved by any orientations. For a density made of two Gaussian blobs on one axis, the images do not change under a rotation about that axis, so each orientation is fixed only up to that rotation. Both are theorems, from the projection of a Gaussian.

**The mirror image.** In the tests of the common lines page, a density of three Gaussian blobs and the same blobs with their third coordinates negated give images that agree to $10^{-12}$ at the rotations $R$ and $J R J$ (a measurement that checks the theorem above).

**Noise breaks pairwise methods.** On the example of the common lines page (5 images of $32 \times 32$ pixels of a density of 6 blobs), the common lines are found within 1.4 degrees without noise. With Gaussian noise of standard deviation 3 percent of the image peak, 28 of 30 lines are within 5 degrees; with 10 percent, only 7 of 30 are, and the orientations are wrong by more than 68 degrees (a measurement). Real cryo-EM images are much noisier, which is why practical methods average many images or use the whole data set at once.

## Known algorithms

| Method | Idea | Guarantee |
|---|---|---|
| [Common lines](/common-lines-method/) (van Heel 1987) | the common line of each pair of images, then the orientations of triples | exact on exact lines, up to rotation and reflection; breaks down at low SNR |
| Eigenvectors and semidefinite programming (Singer and Shkolnisky 2011) | all common lines at once, as a synchronization problem | uses all pairs; works at lower SNR than pairwise methods |
| Projection matching | compare each image with projections of the current model at many orientations, take the best, reconstruct | needs a start model; converges locally at best |
| Maximum likelihood (Sigworth 1998) | treat the orientations and shifts as hidden variables and integrate them out | a [maximum likelihood](/maximum-likelihood-estimation/) estimate; found by [expectation maximization](/expectation-maximization/), so a local optimum |
| Bayesian MAP, RELION (Scheres 2012) | maximum a posteriori with a smoothness prior on $\mathcal{F} f$, which acts like a [Wiener filter](/wiener-filter/) in each shell | expectation maximization, local optimum; the standard tool |
| cryoSPARC (Punjani et al. 2017) | [stochastic gradient descent](/stochastic-gradient-descent/) from random starts for a first model, branch and bound over orientations for refinement | no global guarantee; fast in practice |
| Kam's method (1980) | the autocorrelations of the images averaged over all of them do not depend on the orientations; solve for $f$ from these averages | a [method of moments](/method-of-moments/); needs no orientations |

Each step that rebuilds the density from images with given orientations is a linear tomographic reconstruction, done by gridding in Fourier space with a [nonuniform FFT](/nonuniform-fft/) or a similar interpolation.

## Bounds

- **Identifiability.** The images determine $f$ at most up to a global rotation and a reflection (a theorem, shown above). For a density without symmetry and exact data, three images in general position fix their orientations up to these two (a theorem, proved on the [common lines page](/common-lines-method/)).
- **Number of images at low SNR.** For the multi-reference alignment model, Perry, Weed, Bandeira, Rigollet and Singer (2019) proved that the number of observations needed for a generic signal grows like $1/\mathrm{SNR}$ at high SNR and like $1/\mathrm{SNR}^3$ at low SNR (a theorem for that model). The reason is that the first two moments of the data do not fix the signal, and the third moment does. For cryo-EM itself, bounds of this kind are a research subject.
- **Resolution.** The resolution is limited by the number of images, the SNR, the zeros of the contrast transfer function, and errors in the orientations. In practice it is measured by comparing two maps built from two halves of the data, shell by shell in Fourier space (a heuristic measure, the Fourier shell correlation).
- **Cost.** A search over orientations with angular step $\delta$ has about $8\pi^2/\delta^3$ points on the rotation group (its volume is $8\pi^2$ in the usual measure; a heuristic count), so a fine step is costly. Expectation maximization over all orientations and shifts of all images is the main cost of current methods.

## Reductions

- **With known orientations to tomography.** Fixing the $R_i$ and $t_i$ leaves a linear inverse problem, the [tomographic reconstruction problem](/tomographic-reconstruction-problem/) in 3D, by the slice theorem.
- **Orientations to synchronization.** The relative rotations $R_i^T R_j$ from common lines turn the orientation problem into finding rotations from noisy ratios, the same problem as [rotation averaging](/rotation-averaging/) in structure from motion.
- **Maximum likelihood to expectation maximization.** With the orientations as hidden variables, each step of [expectation maximization](/expectation-maximization/) weights every orientation of every image by its probability under the current model and then solves a weighted linear reconstruction.
- **Moments.** Averaging over the unknown orientations turns the problem into recovering $f$ from rotation-invariant moments, which is related to [phase retrieval](/phase-retrieval/): the second moment alone does not fix the phases of $\mathcal{F} f$.

## Applications

- **Structural biology.** Atomic models of proteins and protein complexes that do not crystallize, such as membrane proteins, large complexes and flexible machines like the ribosome.
- **Viruses.** Structures of virus capsids, often with icosahedral symmetry, and of viral proteins as targets for vaccines and drugs.
- **Drug design.** Maps of a protein with a bound drug candidate.
- **Conformational change.** Several states of one molecule from one data set, through the heterogeneity variants.

## References
