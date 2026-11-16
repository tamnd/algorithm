---
tag: 3HRWHK
kind: technique
slug: stratified-reconstruction
name: Stratified reconstruction
aliases:
- projective to metric upgrade
area: computer-vision/multiple-view-geometry
level: advanced
summary: "Upgrade a projective reconstruction to an affine one by finding the plane at infinity, then to a metric one by finding the absolute conic."
prereqs: [projective-reconstruction-theorem, homogeneous-coordinates, image-of-the-absolute-conic]
see_also: [self-calibration, kruppa-equations, affine-camera-model, vanishing-point-calibration, sturm-triggs-factorization, tomasi-kanade-factorization, planar-transformation-hierarchy, cholesky-decomposition]
sources:
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Section 10.4, Stratified reconstruction; Chapter 19, Auto-calibration"
  - paper: doi:10.1364/JOSAA.12.000465
    title: "Olivier Faugeras, Stratification of three-dimensional vision, projective, affine, and metric representations, Journal of the Optical Society of America A 12(3), 1995"
    locator: the projective, affine and metric strata and the objects that separate them
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Sections 11.3.3 and 11.3.4, on projective reconstruction and self-calibration"
---

Stratified reconstruction is the method of building a metric 3D reconstruction from uncalibrated views in three layers. First, a projective reconstruction is made from the image matches; by the [projective reconstruction theorem](/projective-reconstruction-theorem/) this is all that the matches alone give. Second, the plane at infinity is found in that frame and moved to its standard place, which gives an affine reconstruction, where parallel lines are parallel again. Third, the absolute conic, a conic on the plane at infinity, is found and moved to its standard place, which gives a metric reconstruction, correct up to a similarity. Each step is a $4 \times 4$ change of frame with few unknowns, and each needs its own extra knowledge: parallel lines, a known motion or constraints on the cameras.

## In plain words

From uncalibrated photos you first get a 3D model that keeps only straight lines: lengths, angles and even parallel lines may come out wrong. The method repairs the model in two steps. First it finds where parallel lines should meet, far away, and moves that place to infinity, so parallel lines become parallel again. Then it fixes the angles, using what is known about the cameras, for example that the pixels are square. After both steps the model is right except for its size and where it is placed.

## When it applies

- The cameras are not calibrated, or their calibration is not trusted, so the first reconstruction is projective.
- There is extra knowledge to fix the plane at infinity: three vanishing points from sets of parallel scene lines, a known ratio of lengths on lines, a camera that only translates with fixed intrinsics, or constant intrinsics over several views.
- There is extra knowledge to fix the absolute conic: known intrinsics in at least one view, orthogonal scene directions, zero skew and square pixels, or constant intrinsics over three or more views.
- Affine cameras, such as in [Tomasi-Kanade factorization](/tomasi-kanade-factorization/), give an affine reconstruction directly, and only the metric step is needed.

## The template

All changes of frame act on the cameras as $P_j \leftarrow P_jH^{-1}$ and on the points as $\mathbf{X}_i \leftarrow H\mathbf{X}_i$, so the images do not change. Planes change as $\boldsymbol{\pi} \leftarrow H^{-\mathsf T}\boldsymbol{\pi}$.

1. **Projective reconstruction.** Compute cameras $P_j$ and points $\mathbf{X}_i$ that fit the matches, for example from the [fundamental matrix](/fundamental-matrix/) with $P_1 = [I \mid \mathbf{0}]$ and $P_2 = [[\mathbf{e}']_\times F \mid \mathbf{e}']$, or by [Sturm-Triggs factorization](/sturm-triggs-factorization/) for many views.
2. **Find the plane at infinity.** Find the plane $\boldsymbol{\pi}_\infty = (\mathbf{p}, 1)$ of the projective frame that is the image of the true plane at infinity. Three points on it, for example the intersections of three sets of parallel lines in space, fix it.
3. **Affine upgrade.** Apply
$$H_A = \begin{pmatrix} I & \mathbf{0} \\ \mathbf{p}^{\mathsf T} & 1 \end{pmatrix},$$
which sends $\boldsymbol{\pi}_\infty$ to $(0, 0, 0, 1)$. The reconstruction is now affine: it differs from the true one by an affine map.
4. **Find the absolute conic.** Find the [image of the absolute conic](/image-of-the-absolute-conic/) $\omega = (KK^{\mathsf T})^{-1}$ in one view, from known intrinsics, from vanishing points of orthogonal directions, or by [self-calibration](/self-calibration/).
5. **Metric upgrade.** With the affine camera $P = [M \mid \mathbf{m}]$ of that view, find $A$ with $AA^{\mathsf T} = (M^{\mathsf T}\omega M)^{-1}$ by the [Cholesky decomposition](/cholesky-decomposition/), and apply
$$H_M = \begin{pmatrix} A^{-1} & \mathbf{0} \\ \mathbf{0}^{\mathsf T} & 1 \end{pmatrix}.$$
The reconstruction is now metric: it differs from the true one by a similarity.
6. **Refine.** Run [bundle adjustment](/bundle-adjustment/) in the metric frame, with the intrinsics as unknowns if needed.

Step 5 works because the true camera is $KR[I \mid -C]$: after the affine step $M = KRA^{-1}$ for some invertible $A$, so $M^{\mathsf T}\omega M = A^{-\mathsf T}R^{\mathsf T}K^{\mathsf T}K^{-\mathsf T}K^{-1}KRA^{-1} = (AA^{\mathsf T})^{-1}$. The Cholesky factor fixes $A$ up to a rotation, which is part of the similarity.

## Classic examples

**A worked upgrade.** The true cameras are $P_1 = [I \mid \mathbf{0}]$ and $P_2 = [I \mid (-1, 0, 0)^{\mathsf T}]$, so $K = I$ and $\omega = I$, and the point is $(1, 2, 4)$, with images $(0.25, 0.5)$ and $(0, 0.5)$. A projective reconstruction of it is
$$P_1 = \begin{pmatrix} 0.5 & 0 & 0 & 0 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \end{pmatrix}, \quad P_2 = \begin{pmatrix} 0.5 & 0 & 1 & -1 \\ 0 & 1 & 0 & 0 \\ 0 & 0 & 1 & 0 \end{pmatrix}, \quad \mathbf{X} = (0.4, 0.4, 0.8, 1).$$
Both cameras give the right images. In this frame the direction of the $z$ axis appears as the finite point $(0, 0, 1)$, and the plane at infinity is $\boldsymbol{\pi}_\infty = (0, 0, -1, 1)$, the plane $Z = 1$.

| step | result |
|---|---|
| affine upgrade, $\mathbf{p} = (0, 0, -1)$ | $P_1 = [\operatorname{diag}(0.5, 1, 1) \mid \mathbf{0}]$, $P_2 = [\operatorname{diag}(0.5, 1, 1) \mid (-1, 0, 0)^{\mathsf T}]$, $\mathbf{X} \sim (2, 2, 4, 1)$ |
| $M^{\mathsf T}\omega M$ | $\operatorname{diag}(0.25, 1, 1)$, so $A = \operatorname{diag}(2, 1, 1)$ |
| metric upgrade | $P_1 = [I \mid \mathbf{0}]$, $P_2 = [I \mid (-1, 0, 0)^{\mathsf T}]$, $\mathbf{X} = (1, 2, 4)$ |

The affine reconstruction is the true scene stretched by 2 along $x$: parallel lines are right, angles are not. The metric step removes the stretch.

**Vanishing points.** In a building scene, three sets of parallel edges give three vanishing points in each image. Triangulated in the projective frame, they give three points that fix $\boldsymbol{\pi}_\infty$. If the three directions are known to be orthogonal, their vanishing points also give constraints on $\omega$, as in [vanishing point calibration](/vanishing-point-calibration/).

**Pure translation.** If a camera with fixed intrinsics only translates between two views, the infinite homography between them is the identity, and this fixes $\boldsymbol{\pi}_\infty$ linearly.

## Variations

- **Direct metric upgrade.** The absolute dual quadric $Q^*_\infty$ holds both the plane at infinity (its null vector) and the absolute conic. Self-calibration methods that estimate $Q^*_\infty$ go from projective to metric in one step, through $\omega^*_j \sim P_jQ^*_\infty P_j^{\mathsf T}$.
- **Kruppa equations.** The [Kruppa equations](/kruppa-equations/) constrain $\omega$ from the fundamental matrices alone, without finding the plane at infinity first.
- **Affine start.** With [affine cameras](/affine-camera-model/) the reconstruction is already affine, and only the metric step remains.
- **Known calibration.** With known $K$, the [essential matrix](/essential-matrix/) gives a metric reconstruction directly, and no stratification is needed.
- **The 2D analog.** The same layers exist for the plane: projective, affine, similarity, as in the [hierarchy of planar transformations](/planar-transformation-hierarchy/), where the line at infinity and the circular points play the roles of the plane at infinity and the absolute conic.

## Pitfalls

- **Wrong direction of the change of frame.** Points use $H$, cameras use $H^{-1}$ and planes use $H^{-\mathsf T}$. Mixing them up gives a frame that still fits the images but is not the upgraded one.
- **Plane at infinity through the scene.** In a projective frame, $\boldsymbol{\pi}_\infty$ can cut through the scene. Before the affine step, the scene can look split in two; this is expected and is fixed by the step.
- **Matrix not positive definite.** With noise, $(M^{\mathsf T}\omega M)^{-1}$ can fail to be positive definite, and the Cholesky decomposition fails. This usually means that $\boldsymbol{\pi}_\infty$ or $\omega$ is wrong; refine them together instead of one after the other.
- **Critical motions.** Some camera motions, such as rotations that all have parallel axes or motion in a plane, do not fix the plane at infinity or the absolute conic from constant intrinsics alone. Self-calibration then has a family of solutions.
- **Error growth.** Errors in the affine step pass into the metric step. A final bundle adjustment in the metric frame is needed for an accurate result.

## References
