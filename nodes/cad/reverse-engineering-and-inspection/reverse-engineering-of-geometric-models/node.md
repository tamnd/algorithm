---
tag: RTQQXS
kind: problem
slug: reverse-engineering-of-geometric-models
name: Reverse engineering of geometric models
aliases:
- CAD reverse engineering
- scan-to-CAD
area: cad/reverse-engineering-and-inspection
level: core
summary: Build a CAD model, usually a B-rep of simple and free-form faces, from measured points of a physical part, by segmentation, fitting and stitching.
prereqs: [point-cloud, boundary-representation, least-squares-approximation]
see_also: [primitive-segmentation, geometric-primitive-fitting, brep-reconstruction-from-scans, point-cloud-registration, b-spline-fitting, surface-reconstruction, cad-based-inspection, feature-recognition]
sources:
  - paper: doi:10.1016/S0010-4485(96)00054-1
    title: Tamás Várady, Ralph R. Martin and Jordan Cox, Reverse engineering of geometric models, an introduction, Computer-Aided Design 29(4), 1997, 255 to 268
    locator: the whole survey, with the phases of data capture, preprocessing, segmentation and surface fitting, and the creation of B-rep models, and the discussion of the open problems
  - paper: doi:10.1016/S0010-4485(01)00100-2
    title: Pál Benkő, Ralph R. Martin and Tamás Várady, Algorithms for reverse engineering boundary representation models, Computer-Aided Design 33(11), 2001, 839 to 851
    locator: the whole paper, which summarizes the phases of a procedure for conventional engineering objects and the computational difficulties of each (general locator; section numbers not confirmed)
  - paper: doi:10.1109/34.121791
    title: Paul J. Besl and Neil D. McKay, A method for registration of 3-D shapes, IEEE Transactions on Pattern Analysis and Machine Intelligence 14(2), 1992, 239 to 256
    locator: the iterative closest point algorithm for the alignment of a measured point set to a model or to another point set
  - paper: doi:10.1109/CVPR.2019.00983
    title: Sebastian Koch, Albert Matveev, Zhongshi Jiang, Francis Williams, Alexey Artemov, Evgeny Burnaev, Marc Alexa, Denis Zorin and Daniele Panozzo, ABC, a big CAD model dataset for geometric deep learning, CVPR 2019
    locator: the collection of one million CAD models with their exact B-rep geometry and the benchmarks built from it
  - paper: arxiv:1605.04797
    title: Qingnan Zhou and Alec Jacobson, Thingi10K, a dataset of 10,000 3D-printing models, 2016
    locator: the collection of meshes from Thingiverse and their geometric and topological statistics
---

Reverse engineering of geometric models is the problem of building a CAD model of a physical part from points measured on its surface. The usual target is a [boundary representation](/boundary-representation/) whose faces are simple surfaces, planes, spheres, cylinders, cones and tori, together with swept and free-form faces where nothing simple fits, so that the model is accurate, valid as a solid, and editable like a model a designer made. Várady, Martin and Cox (1997) described the problem and its steps: capture the data, register and clean it, cut it into regions, fit a surface to each region, and build the B-rep from the fitted faces. Each step has its own page; this page states the whole problem and links the steps.

## In plain words

A company has a part but no drawing of it, perhaps because the part is old, or was shaped by hand, or comes from another firm. A scanner measures many points on its surface. From these points a computer must make a model that a designer can open and change.

A cloud of points is not yet a model. The computer must find out which points belong to which face, what shape each face has, such as flat or round, and where the faces meet. It must also keep the intent of the design: faces that look parallel should be exactly parallel, and holes that look the same size should have the same size. The result must be a closed solid with no gaps, close to the measured points.

## Definition

**Input.** Points $p_1, \dots, p_m$ in $\mathbb{R}^3$, measured on the surface of a part, often in several views with their own coordinate frames; a measure of the noise, or a tolerance $\varepsilon$; a set of allowed surface types, such as planes, quadrics, tori, swept surfaces and [B-spline](/b-spline/) or [NURBS](/nurbs/) patches.

**Output.** A valid solid model $M$, a closed and oriented boundary made of faces of the allowed types with edges and vertices where they meet, such that:

- **fidelity:** every measured point lies within $\varepsilon$ of the boundary $\partial M$;
- **coverage:** where data exist, $\partial M$ lies within $\varepsilon$ of the data, so that the model does not add surface that was not measured;
- **simplicity and intent:** among such models, one with few faces, simple types and the relations of the design, such as parallel faces, coaxial cylinders and equal radii.

The trade between fidelity and simplicity has no standard form. Some methods fix $\varepsilon$ and ask for few faces; others minimize the sum of squared distances plus a cost for each face or parameter. The problem is not fully posed: parts of the surface that the scanner did not see must be guessed, and different designs can fit the same points within $\varepsilon$.

## Variants

- **Output type.** A B-rep with analytic and free-form faces, the classic target; a triangle mesh from [surface reconstruction](/surface-reconstruction/), such as [Poisson reconstruction](/poisson-surface-reconstruction/), when no editable model is needed; a [CSG](/constructive-solid-geometry/) tree; or a [feature-based model](/feature-based-modeling/) with the construction history.
- **Input type.** [Range images](/range-image/) with a grid of pixels; unordered [point clouds](/point-cloud/) from several views; meshes; or touch probe points from a coordinate measuring machine.
- **Primitives only, or free-form.** Conventional engineering parts need only simple surfaces and blends; styled or organic parts need B-spline surfaces fitted to the regions.
- **With constraints.** The model may have to keep relations of the design, which turns the separate fits into one [constrained fit](/constrained-primitive-fitting/).
- **Curves and profiles.** The same steps in the plane fit lines, circles and splines to sections and profiles, for example with [circle fitting](/circle-fitting/) and [curve fitting](/curve-fitting/).
- **Learned methods.** Networks trained on CAD models predict segments, types and topology; ABC (Koch and others, 2019) gives exact B-rep models for training and tests, and Thingi10K (Zhou and Jacobson, 2016) a set of real-world meshes.

## Examples

**A box.** The points of a scanned block fall into six regions; each gets a plane; the planes of neighboring regions meet in $12$ edges and $8$ corners, and the faces close into a solid with $V - E + F = 8 - 12 + 6 = 2$. The [B-rep reconstruction](/brep-reconstruction-from-scans/) page works this example step by step.

**A plate with a through hole.** The six planes of the plate and one cylinder for the hole give seven faces; the top and the bottom face each have an inner loop around the hole, and the solid has one handle. So the faces are not all disks, and the check of the model uses the [Euler-Poincaré formula](/euler-poincare-formula/) $V - E + F - (L - F) - 2(S - H) = 0$, which counts the loops $L$, the shells $S$ and the handles $H$.

**Why fitted faces are better than raw points.** If a plane with a known normal is fitted to $m$ points by least squares, its offset is the mean of the offsets of the points. With independent errors of standard deviation $\sigma$ along the normal, the mean has the standard deviation $\sigma / \sqrt m$: for $\sigma = 0.05$ mm and $m = 2500$ points this is $0.001$ mm. So the faces, and the edges where they meet, are much more accurate than single points, which is why the model is built from fitted faces and not from the points along the edges.

## Known algorithms

The steps, in the usual order, with the pages that treat them:

1. **Registration.** Views taken from different places are brought into one frame with [point cloud registration](/point-cloud-registration/), usually [ICP](/iterative-closest-point/) of Besl and McKay (1992) or [point-to-plane ICP](/point-to-plane-icp/).
2. **Cleaning and normals.** Stray points are removed, for example by [statistical outlier removal](/statistical-outlier-removal/), and each point gets a normal by [normal estimation](/point-cloud-normal-estimation/); curvature comes from [curvature tensor estimation](/curvature-tensor-estimation/).
3. **Segmentation.** The points are divided into regions that each follow one surface; this is the problem of [segmentation into primitives](/primitive-segmentation/). Methods include [efficient RANSAC](/efficient-ransac-shape-detection/), [variable-order surface fitting](/variable-order-surface-fitting/), [slippage analysis](/slippage-analysis/), [region growing](/region-growing/) and the [Hough transform](/hough-transform/).
4. **Fitting of simple surfaces.** Each region gets its surface. The fits differ in the distance that they minimize:

| page | distance minimized | under noise |
| --- | --- | --- |
| [algebraic distance fitting](/algebraic-distance-fitting/) | the value of the implicit equation at the points | biased, linear and fast |
| [Taubin fitting](/taubin-fitting/) | the algebraic distance divided by the gradient, a first-order approximation of the orthogonal distance | still biased, one eigenproblem |
| [geometric primitive fitting](/geometric-primitive-fitting/) | the orthogonal distance | iterative, started from one of the fits above |
| [constrained primitive fitting](/constrained-primitive-fitting/) | the total fitting error of several primitives, subject to relations among them | iterative |

5. **Fitting of free-form faces.** Regions without a simple surface get a B-spline curve or surface by [B-spline fitting](/b-spline-fitting/). [Parameter correction](/parameter-correction/) minimizes the distance to the current foot points and moves them to the orthogonal projections; [squared distance minimization](/squared-distance-minimization/) minimizes a quadratic model of the squared orthogonal distance that uses the curvature, and converges faster.
6. **Building the model.** The fitted faces are intersected into edges and vertices, blends are fitted between them, and the result is stitched into a closed solid by [B-rep reconstruction](/brep-reconstruction-from-scans/); remaining gaps are closed by [B-rep healing](/brep-healing/).
7. **Checking.** The model is compared with the points, or a new part with the model, by [CAD-based inspection](/cad-based-inspection/), after [localization](/inspection-localization/) of the points to the model.

Algebraic fits are biased: on noisy data their answer is pulled away from the best fit in a direction that depends on the normalization, and for circles on short arcs toward a radius that is too small. They are used as fast starting points, and the final faces come from the orthogonal distance.

## Bounds

Every method must read all $m$ points, so $\Omega(m)$ time is needed. The problem contains segmentation: with lines in the plane, a tolerance of $0$ and the goal of the fewest pieces, it is the problem of covering points by the fewest lines, which is NP-complete, as the [segmentation page](/primitive-segmentation/) explains. So no polynomial algorithm is known for the exact form with few faces, and practical systems are pipelines of heuristics. No method can recover the surface where nothing was measured, so guarantees are possible only for parts that are fully sampled; the [B-rep reconstruction](/brep-reconstruction-from-scans/) page proves one for polyhedra with exact samples.

## Reductions

- **To its steps.** With the regions fixed, the problem splits into one fitting problem per region and a model building problem, each with the pages above.
- **To least squares.** Every fit is a [least-squares problem](/least-squares-approximation/), linear for algebraic distances and nonlinear for orthogonal distances, solved by [Gauss-Newton](/gauss-newton-algorithm/) or [Levenberg-Marquardt](/levenberg-marquardt/) steps. A line or plane fit by orthogonal distance is [errors-in-variables regression](/errors-in-variables-regression/), solved by [principal component analysis](/principal-component-analysis/).
- **To registration.** Inspection against the result, and the merging of views before it, reduce to [point cloud registration](/point-cloud-registration/).
- **Relaxed to a mesh.** Without the demand for simple faces, the problem becomes [surface reconstruction](/surface-reconstruction/).

## Applications

- **Parts without a model.** Old parts, spare parts and parts from other firms get a CAD model for repair, manufacture and change.
- **Design from physical models.** Shapes that designers form by hand, for example in clay for cars, become CAD surfaces.
- **Inspection.** A manufactured part is compared with its design; the same fits give the measured features for [form error evaluation](/form-error-evaluation/).
- **Medicine and heritage.** Bones, implants and art objects are scanned and modeled, mostly as free-form surfaces or meshes.
- **Training data.** Large sets of CAD models, such as ABC, serve to train and test learned methods of scan-to-CAD.

## References
