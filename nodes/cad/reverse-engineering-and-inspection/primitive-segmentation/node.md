---
tag: 2CVPE0
kind: problem
slug: primitive-segmentation
name: Segmentation into surface primitives
aliases:
- point cloud primitive segmentation
area: cad/reverse-engineering-and-inspection
level: core
summary: Partition a point cloud or mesh into regions each well fit by a plane, sphere, cylinder, cone, torus or free-form patch, the first step of scan-to-CAD.
prereqs: [geometric-primitive-fitting, point-cloud-normal-estimation, ransac]
see_also: [efficient-ransac-shape-detection, variable-order-surface-fitting, slippage-analysis, region-growing, mesh-segmentation, j-linkage, brep-reconstruction-from-scans, reverse-engineering-of-geometric-models]
sources:
  - paper: doi:10.1016/S0010-4485(96)00054-1
    title: Tamás Várady, Ralph R. Martin and Jordan Cox, Reverse engineering of geometric models, an introduction, Computer-Aided Design 29(4), 1997, 255 to 268
    locator: the section on segmentation and surface fitting, with edge-based and face-based segmentation and the classification of points and regions into surface types
  - paper: doi:10.1109/34.3881
    title: Paul J. Besl and Ramesh C. Jain, Segmentation through variable-order surface fitting, IEEE Transactions on Pattern Analysis and Machine Intelligence 10(2), 1988, 167 to 192
    locator: the segmentation of range images into regions of the eight surface types of the signs of mean and Gaussian curvature, and the region growing by surface fits of increasing order
  - paper: doi:10.1111/j.1467-8659.2007.01016.x
    title: Ruwen Schnabel, Roland Wahl and Reinhard Klein, Efficient RANSAC for point-cloud shape detection, Computer Graphics Forum 26(2), 2007, 214 to 226
    locator: the detection of planes, spheres, cylinders, cones and tori by RANSAC with local sampling, the score with distance and normal tolerances and connected components, and the extraction loop
  - paper: doi:10.1007/s11263-011-0474-7
    title: Hossam Isack and Yuri Boykov, Energy-based geometric multi-model fitting, International Journal of Computer Vision 97(2), 2012, 123 to 147
    locator: multi-model fitting as a labeling problem with a geometric error term, a smoothness term on neighbors and a cost per model, minimized by alternating alpha-expansion and refitting (PEaRL)
  - paper: doi:10.1016/0167-6377(82)90039-6
    title: Nimrod Megiddo and Arie Tamir, On the complexity of locating linear facilities in the plane, Operations Research Letters 1(5), 1982, 194 to 197
    locator: the NP-completeness of covering given points in the plane by a minimum number of lines
  - paper: doi:10.1109/CVPR.2019.00983
    title: Sebastian Koch, Albert Matveev, Zhongshi Jiang, Francis Williams, Alexey Artemov, Evgeny Burnaev, Marc Alexa, Denis Zorin and Daniele Panozzo, ABC, a big CAD model dataset for geometric deep learning, CVPR 2019
    locator: the collection of one million CAD models with their exact B-rep geometry and the benchmarks built from it
  - paper: arxiv:1605.04797
    title: Qingnan Zhou and Alec Jacobson, Thingi10K, a dataset of 10,000 3D-printing models, 2016
    locator: the collection of meshes from Thingiverse and their geometric and topological statistics
---

Segmentation into surface primitives is the problem of dividing a scanned point cloud or mesh into regions so that each region is fitted well by one simple surface: a plane, a sphere, a circular cylinder, a cone, a torus, or, where nothing simple fits, a free-form patch. It is the step of [reverse engineering](/reverse-engineering-of-geometric-models/) between the measured points and the surface model. A segmentation must decide two things at once: which points belong together, and which surface each group follows. Neither can be done first: the fit needs the region, and the region needs the fit. Várady, Martin and Cox (1997) describe the two classic approaches: edge-based methods, which find sharp edges and regions of high curvature first and take the parts between them, and face-based methods, which grow regions of points that fit one surface. No single objective is standard; the methods differ in the error they allow, how they count regions, and how they treat points near edges.

## In plain words

A scanner gives a cloud of points on the outside of a part, with no structure. A designer thinks of the same part as a set of faces: this flat face, that hole, this rounded edge. Segmentation finds those faces in the points.

Each point gets a label that says which face it is on, and each face gets a shape, such as a plane or a cylinder, that the points of the face follow closely. Some points, such as noise or points on tiny details, may get no label. The hard parts are the points near an edge, where two faces meet, and the faces that are almost flat or almost round, where more than one shape fits well enough.

## Definition

**Input.** Points $p_1, \dots, p_m$ in $\mathbb{R}^3$, usually with unit normals $n_i$ and a neighbor graph $G$ (the mesh edges, or the $k$ nearest neighbors); a list of surface types, for example plane, sphere, cylinder, cone and torus; a distance tolerance $\varepsilon$, an angle tolerance $\alpha$, and a minimum region size $s$.

**Output.** A number $K$, labels $\ell : \{1, \dots, m\} \to \{0, 1, \dots, K\}$, and a surface $S_j$ of one of the types for each $j \ge 1$, such that, for the region $R_j = \{ i : \ell(i) = j \}$:

- every $i \in R_j$ has $\operatorname{dist}(p_i, S_j) \le \varepsilon$, and the angle between $n_i$ and the normal of $S_j$ at the nearest point is at most $\alpha$;
- $R_j$ is connected in $G$ and has at least $s$ points.

Label $0$ marks points left out. Among the valid segmentations the goal is a good one, and the measure differs between formulations: few regions and few points left out; a small total of squared distances plus a cost per region, as in [minimum description length](/minimum-description-length/) or [information criteria](/bayesian-information-criterion/); or an energy that also charges neighbor pairs with different labels.

## Variants

- **Fixed types or free-form.** Some methods allow only the primitive types; others also allow polynomial or [B-spline](/b-spline/) patches for the regions that no primitive fits.
- **Exact cover or energy.** The cover form asks for few regions within the tolerance. The energy form, as in Isack and Boykov (2012), minimizes $\sum_i \operatorname{dist}(p_i, S_{\ell(i)})^2 + \lambda \sum_{(i, i') \in G} [\ell(i) \ne \ell(i')] + h K$, a fitting term, a [Potts](/potts-model/) smoothness term and a cost per model.
- **Input type.** Range images, with a grid as the neighbor graph, as in Besl and Jain (1988); meshes, where the triangles are labeled, as in [mesh segmentation](/mesh-segmentation/); or unordered point clouds.
- **Planar curves.** The same problem in the plane, with lines, circles and free-form curves, segments 2D profiles and sections.
- **With or without edges and blends.** Some methods also label the thin strips of fillets and rounds between the main faces, or the sharp edges themselves.
- **Supervised.** Learned methods predict the labels and the types from examples; the ABC dataset of CAD models with exact faces (Koch et al., 2019) is a common source of training and test data, and Thingi10K (Zhou and Jacobson, 2016) is a collection of real-world meshes used for tests.

## Examples

**A box.** A scan of a rectangular block has six regions, each a plane. Points within $\varepsilon$ of two faces, along an edge, can go to either; a good method gives each to the face with the closer fit or leaves it out.

**Plane or cylinder.** Points on a cylinder of radius $R = 100$ mm across a strip of width $L = 20$ mm deviate from the chord plane by at most the sagitta
$$ R - \sqrt{R^2 - (L/2)^2} = 100 - \sqrt{9900} \approx 0.501 \text{ mm} . $$
With $\varepsilon = 1$ mm both a plane and a cylinder are valid, and the cover form prefers neither. A cost per parameter (a plane has $3$, a cylinder $5$) favors the plane, while the sum of squared distances favors the cylinder; the formulation decides.

**An L shape in the plane.** The points $(k, 0)$ and $(0, k)$ for $k = 0, \dots, 4$ are covered by two lines with $\varepsilon = 0$. The point $(0, 0)$ lies on both, so the labels are not unique even when the surfaces are.

## Known algorithms

- **Region growing.** Start from a seed with low curvature and add neighbors that fit the current surface, refitting as the region grows; [region growing](/region-growing/) on normals and curvature, with curvature from [curvature tensor estimation](/curvature-tensor-estimation/).
- **Variable-order fitting.** [Besl and Jain](/variable-order-surface-fitting/) label points by the signs of the mean and Gaussian curvature and grow regions with polynomial surfaces of increasing order.
- **RANSAC.** [RANSAC](/ransac/) samples minimal sets, fits candidates, keeps the one with the largest connected set of inliers, removes those points and repeats. [Efficient RANSAC](/efficient-ransac-shape-detection/) does this for planes, spheres, cylinders, cones and tori with local sampling and an octree.
- **Hough transform.** The [Hough transform](/hough-transform/) votes in the parameter space of one type, which works well for planes and less well for types with many parameters.
- **Slippage.** [Slippage analysis](/slippage-analysis/) classifies local patches by their slippable motions and merges regions that share them.
- **Multi-model fitting.** [J-linkage](/j-linkage/) clusters points by the sets of candidate models they agree with; PEaRL minimizes the energy form by [alpha-expansion](/alpha-expansion/), alternating with refits.
- **Clustering of normals and curvature.** [Mean shift](/mean-shift/) or [DBSCAN](/dbscan/) on normals, positions and curvature give regions, which are then fitted.

After any of these, each region goes to [geometric primitive fitting](/geometric-primitive-fitting/), and often the whole model to [constrained primitive fitting](/constrained-primitive-fitting/).

## Bounds

Every algorithm must read all $m$ points, so $\Omega(m)$ time is needed. For the cover form the problem is hard in general: the planar variant with lines only, $\varepsilon = 0$, no connectivity condition and the goal of the fewest regions is exactly the problem of covering points by the fewest lines, which Megiddo and Tamir (1982) showed to be NP-complete. So no polynomial algorithm is known for the exact cover form, and practical methods are heuristics with no guarantee on the number of regions. The energy form with a fixed set of candidate models contains the minimization of a Potts energy with three or more labels, which is NP-hard as well; this is why PEaRL uses alpha-expansion, an approximation with a bounded factor for the Potts term.

## Reductions

- **To set cover.** With a finite set of candidate surfaces, each covering the points within the tolerance, the cover form is a [set cover](/set-cover/) problem; the greedy rule of taking the candidate with the most uncovered points, which sequential RANSAC follows with random candidates, has the logarithmic factor of greedy set cover when all candidates are tried.
- **To labeling.** The energy form is a labeling problem with label costs, a Potts model over the neighbor graph.
- **From line cover.** As above, minimum line cover in the plane is the special case that makes the cover form NP-hard.
- **To primitive fitting.** Once the regions are fixed, the remaining problem is a separate least-squares fit per region.

## Applications

- **Scan-to-CAD.** Segmentation is the first modeling step of reverse engineering; the regions and their surfaces become the faces of a [B-rep reconstruction](/brep-reconstruction-from-scans/).
- **Inspection.** Measured points of a manufactured part are split into the features of the design before each feature is compared with its tolerance.
- **Buildings and plants.** Laser scans of buildings, pipes and plants are segmented into planes and cylinders for models of existing structures.
- **Robotics.** Planes and cylinders found in depth images serve for grasping, for placing objects on tables, and for registration with few features.

## References
