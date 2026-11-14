---
tag: GTWEA2
kind: technique
slug: slippage-analysis
name: Slippage analysis
aliases:
- slippable motion analysis
area: cad/reverse-engineering-and-inspection
level: research
summary: Gelfand and Guibas's test of which rigid motions slide a surface patch along itself, from a 6 by 6 eigenproblem, to find planes, cylinders and other kinematic surfaces.
prereqs: [point-cloud-normal-estimation, screw-motion, rayleigh-quotient]
see_also: [primitive-segmentation, point-to-plane-icp, surface-of-revolution, efficient-ransac-shape-detection, geometric-primitive-fitting, region-growing, jacobi-eigenvalue-algorithm, reverse-engineering-of-geometric-models]
sources:
  - paper: doi:10.1145/1057432.1057461
    title: Natasha Gelfand and Leonidas J. Guibas, Shape segmentation using local slippage analysis, Proceedings of the Eurographics/ACM SIGGRAPH Symposium on Geometry Processing (SGP 2004), also doi:10.2312/SGP/SGP04/219-228
    locator: the definition of slippable motions, the 6 by 6 matrix of points and normals and its small eigenvalues, the slippage signatures of local patches, and the segmentation by merging regions with matching slippable motions
  - paper: doi:10.1109/IM.2003.1240258
    title: Natasha Gelfand, Leslie Ikemoto, Szymon Rusinkiewicz and Marc Levoy, Geometrically stable sampling for the ICP algorithm, Fourth International Conference on 3-D Digital Imaging and Modeling (3DIM 2003), 260 to 267
    locator: the covariance matrix of the linearized point-to-plane error, its eigenvectors as the unstable transformations, and the normalization of rotations and translations
  - paper: doi:10.1007/BF02684378
    title: Helmut Pottmann and Thomas Randrup, Rotational and helical surface approximation for reverse engineering, Computing 60(4), 1998, 307 to 322
    locator: the recognition of cylindrical surfaces, surfaces of revolution and helical surfaces from the surface normals, by line geometry and a linear complex of normal lines
---

Slippage analysis is a technique that finds the rigid motions that slide a surface along itself, from sample points and their normals, and uses them to tell which kind of surface a patch of a scan is. A rigid motion with angular velocity $r$ and linear velocity $t$ moves a point $p$ with velocity $r \times p + t$. The motion is slippable for a surface when this velocity is tangent to the surface at every point, $(r \times p + t) \cdot n = 0$. Since $(r \times p) \cdot n = r \cdot (p \times n)$, this is one linear equation in the six numbers $x = (r, t)$ per sample, with the coefficient vector $a_i = (p_i \times n_i, n_i)$. So the slippable motions are the null space of the $6 \times 6$ matrix $C = \sum_i a_i a_i^{\mathsf T}$, and on real data the eigenvectors with small eigenvalues. A plane and a sphere have three slippable motions, a cylinder two, a surface of revolution, a helical surface and a general cylinder one, and a generic free-form surface none. These are the kinematic surfaces, the surfaces that a one-parameter group of rigid motions maps into themselves. Gelfand and Guibas (2004) built a [segmentation](/primitive-segmentation/) of scans on this test; the same matrix had appeared in 2003 as a measure of stability for [point-to-plane ICP](/point-to-plane-icp/).

## In plain words

Put a surface against a copy of itself and try to move it without making a gap. A flat plate can slide in two directions and turn on the spot. A ball in a socket can turn in any direction. A shaft in a hole can turn and slide along its axis. A screw in a nut can only move by turning and advancing together. A vase can only turn about its axis. A shape like a face cannot move at all.

Slippage analysis does this test with numbers. From the points and the surface directions at the points, it finds all the ways that the patch can slide. The count and the kind of these motions say what the patch is: a plane, a sphere, a cylinder, or something else. It does not fit a radius, but an axis can be read from the motions.

## When it applies

- The data are points with unit normals, from a mesh or from [normal estimation](/point-cloud-normal-estimation/) on a point cloud, and the normals are reliable.
- The surfaces of interest are kinematic: planes, spheres, cylinders, surfaces of revolution (cones and tori among them), helical surfaces and extrusions. Many machined parts are made of such surfaces.
- The question is about the type of a surface or about the regions that share a type, as in a segmentation, or about which motions a registration cannot determine.
- Each patch is large enough, compared with its radius of curvature, for the motions that are not slippable to cost something.

## The template

```pseudo id=main
SLIPPAGE(points p_1..p_m, unit normals n_1..n_m, ratio τ)
L1  c ← the centroid of the p_i; s ← the mean of |p_i − c|; p_i ← (p_i − c) / s
L2  C ← Σ_i a_i a_iᵀ with a_i = (p_i × n_i, n_i), a 6 by 6 matrix
L3  λ_1 ≤ … ≤ λ_6 and unit eigenvectors x_1, …, x_6 of C
L4  k ← the number of i with λ_6 > τ λ_i
L5  return the space spanned by x_1, …, x_k, the slippable motions
```

**Why it works.** For a unit vector $x = (r, t)$, $x^{\mathsf T} C x = \sum_i \bigl( (r \times p_i + t) \cdot n_i \bigr)^2$, the sum of the squared normal velocities of the samples. So $C$ is positive semidefinite, its eigenvalues are the stationary values of this [Rayleigh quotient](/rayleigh-quotient/), and $x$ is an exact slippable motion of the samples exactly when $C x = 0$. A small eigenvalue is a motion that moves the samples almost only along the surface.

**Line L1.** A rotation and a translation have different units: $r$ is in radians per unit time, $t$ in length per unit time, and $p \times n$ grows with the distance from the origin. Moving the centroid to the origin and scaling to a mean distance of $1$ makes the eigenvalues comparable and the result independent of position and size.

**Line L4.** On noisy data no eigenvalue is exactly $0$, so a threshold decides which are small. Comparing with the largest eigenvalue, as a [condition number](/condition-number/) does, makes the test independent of the number of samples. The threshold is a parameter of the method.

**Reading the motions.** For $r \ne 0$, $x = (r, t)$ is an infinitesimal [screw motion](/screw-motion/) with axis direction $r$, the point $q = (r \times t) / \lvert r \rvert^2$ on the axis, and the pitch $h = (r \cdot t) / \lvert r \rvert^2$: the velocity at $q$ is $h r$, along the axis. For $r = 0$ the motion is a translation in the direction $t$. The table gives the classic cases.

| $k$ | slippable motions | surface |
| --- | --- | --- |
| 3 | two translations in the plane, the rotation about the normal | plane |
| 3 | the three rotations about the center | sphere |
| 2 | the rotation about the axis and the translation along it | circular cylinder |
| 1 | one rotation, pitch $0$ | surface of revolution, including the cone |
| 1 | one screw motion, pitch $h \ne 0$ | helical surface |
| 1 | one translation | general cylinder, an extrusion |
| 0 | none | free-form |

When $k \ge 2$, line L5 returns a space, not single motions. For a cylinder, every combination of the rotation and the translation is slippable, and an eigen solver may return two screws instead of the pure rotation and the pure translation. The type is read from the space: it has a pure translation and a pure rotation with the same axis direction, for example.

**Example.** Take the unit cylinder about the $z$ axis, sampled at the four angles $0$, $90$, $180$ and $270$ degrees and the heights $z = \pm 1$: eight points $p = (\cos \theta, \sin \theta, z)$ with the normals $n = (\cos \theta, \sin \theta, 0)$. The centroid is the origin and the mean distance is $\sqrt 2$, so line L1 divides the points by $\sqrt 2$. Then $p \times n = (-z \sin \theta, z \cos \theta, 0) / \sqrt 2$, and line L2 gives, in the order $(r_x, r_y, r_z, t_x, t_y, t_z)$,
$$ C = \operatorname{diag}(2, 2, 0, 4, 4, 0) , $$
since all mixed sums vanish by the symmetry of the samples. The eigenvalues are $0, 0, 2, 2, 4, 4$, so $k = 2$ for any $\tau$, and the slippable motions are spanned by the rotation $(0, 0, 1, 0, 0, 0)$ and the translation $(0, 0, 0, 0, 0, 1)$: a cylinder with the $z$ axis. If the samples are only the four points at $z = 0$, then $p \times n = 0$ and the rotations about the $x$ and $y$ axes become slippable too: one ring of points with radial normals is also a ring on a sphere, and the samples cannot tell the two apart.

**Cost.** Lines L1 and L2 take $\Theta(m)$ time; the eigenproblem has a fixed size $6$ and takes constant time, by the [Jacobi method](/jacobi-eigenvalue-algorithm/) for example.

## Classic examples

- **Segmentation into kinematic surfaces.** Gelfand and Guibas compute the slippable motions of a small patch around many sample points, the slippage signature, and merge neighboring regions whose points are compatible with the same motions, in the manner of [region growing](/region-growing/). The result is a segmentation into primitives where each region is a kinematic surface, without fitting each type separately.
- **Stability of registration.** In point-to-plane ICP, the linearized error of a small motion $x$ is $x^{\mathsf T} C x$, so the slippable motions are the motions that [registration](/point-cloud-registration/) cannot determine: two scans of a cylinder can slide along the axis. Gelfand, Ikemoto, Rusinkiewicz and Levoy choose samples that make the small eigenvalues of $C$ large.
- **Recognition of surfaces of revolution and helical surfaces.** Pottmann and Randrup test whether the normal lines of the data lie in a linear complex, which is the same equation $(p \times n) \cdot r + n \cdot t = 0$ seen in line geometry, and recover the axis and the pitch of a [surface of revolution](/surface-of-revolution/) or a helical surface from the eigenvector of the smallest eigenvalue.
- **Detection of primitives.** [Efficient RANSAC](/efficient-ransac-shape-detection/) fits a fixed list of primitive types; slippage analysis gives an independent check of the type of a region before the [geometric fit](/geometric-primitive-fitting/).

## Variations

- **Normalized eigenproblem.** Pottmann and Randrup minimize $\sum_i \bigl( (p_i \times n_i) \cdot r + n_i \cdot t \bigr)^2$ under the normalization $\lvert r \rvert = 1$, which leads to a [generalized eigenvalue problem](/generalized-eigenvalue-problem/) and gives the axis of a surface of revolution or a helical surface directly.
- **Weights.** Weighting the samples by area, or by the confidence of the normal, makes the matrix less dependent on the sampling density.
- **Translations only.** With $r = 0$, the matrix is $\sum_i n_i n_i^{\mathsf T}$, and its null space gives the extrusion directions, the directions of a general cylinder.
- **Curves in the plane.** For planar curves the motions have three parameters, the matrix is $3 \times 3$, and the slippable curves are lines and circles.
- **Point to point.** If the vectors $a_i$ are built for all three directions instead of the normal only, nothing is slippable: the analysis needs the normal to separate sliding from moving off the surface.

## Pitfalls

- **Bad normals.** The test is only as good as the normals. Near edges, normal estimation mixes two faces, and the patch looks like neither; use estimators that respect sharp features, or patches away from edges.
- **Patch too small.** A small piece of a cylinder, compared with its radius, is almost flat, and the rotations about axes in the tangent plane are almost slippable. The count $k$ then depends on the patch size and on $\tau$; choose the patch size from the scale of the features.
- **Narrow sampling.** Samples that miss a direction create false slippable motions, as in the ring example. A patch that is long in one direction and narrow in another has the same problem in a weaker form.
- **Threshold.** No threshold is right for all noise levels. With the test of line L4, too large a $\tau$ finds no slippable motions on noisy data, and too small a $\tau$ adds motions that are not there.
- **Single eigenvectors.** For $k \ge 2$ the eigenvectors of a repeated eigenvalue are not unique. Classify the space, not the individual vectors.
- **Cones.** A cone has only one slippable motion, the rotation about its axis, so slippage alone does not separate a cone from other surfaces of revolution; a fit is needed for that.
- **Boundaries.** The test sees only the samples, not the boundary of the face. A disc, a strip and an infinite plane all have three slippable motions.

## Exercises

1. Show that for samples on the plane $z = 0$ with normal $(0, 0, 1)$, every row is $a_i = (y_i, -x_i, 0, 0, 0, 1)$, and that the null space of $C$ contains the translations along $x$ and $y$ and the rotation about $z$. When is it exactly these three?
2. Show that for samples on a sphere about the origin, $p_i \times n_i = 0$, and that the null space of $C$ contains the three rotations. Why does a translation not slip?
3. For a helical surface with axis $z$ and pitch $h$, show that $(r, t) = (e_z, h e_z)$ is slippable, and that the axis formula of the template gives a point on the $z$ axis.
4. Show that the eigenvalues of $C$ do not change under a rigid motion of the data, if $C$ is computed after line L1. What happens without line L1?

## References
