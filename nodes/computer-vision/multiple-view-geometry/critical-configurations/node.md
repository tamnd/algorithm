---
tag: C0D6SB
kind: concept
slug: critical-configurations
name: Critical configurations of two views
aliases:
- critical surfaces
- ambiguous configurations
area: computer-vision/multiple-view-geometry
level: advanced
summary: "Point and camera arrangements, such as points on a ruled quadric through the camera centers, for which the two-view reconstruction is not unique."
prereqs: [fundamental-matrix, projective-reconstruction-theorem]
see_also: [seven-point-algorithm, eight-point-algorithm, five-point-algorithm, homography, relative-pose-problem, ransac, self-calibration, minimal-solver]
sources:
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Chapter 22, Degenerate configurations"
  - paper: doi:10.1007/s11263-005-4796-1
    title: "Richard Hartley and Fredrik Kahl, Critical configurations for projective reconstruction from multiple views, International Journal of Computer Vision 71(1), 2007"
    locator: the critical configurations for two and more views and the ruled quadrics that contain them
  - url: https://arxiv.org/abs/2112.05074
    title: "Martin Bråtelund, Critical configurations for two projective views, a new approach, arXiv 2112.05074"
    locator: the classification of critical configurations for two projective views
  - url: https://arxiv.org/abs/2112.05478
    title: "Martin Bråtelund, Critical configurations for three projective views, arXiv 2112.05478"
    locator: the extension of the classification to three views
---

A critical configuration is an arrangement of scene points and cameras whose images can also be explained by a second arrangement that is not related to the first by a projective transformation. For such data the [projective reconstruction theorem](/projective-reconstruction-theorem/) does not apply: the matches do not fix the [fundamental matrix](/fundamental-matrix/), and no method can tell the true scene from the false one. For two uncalibrated views the critical configurations are those in which the scene points and both camera centers lie on one ruled quadric: a hyperboloid of one sheet, or one of its degenerate forms, such as a cone, or a pair of planes. A planar scene is the most common case in practice. Critical configurations matter mostly because data near them give unstable estimates.

## In plain words

Usually, two photos of a scene fix its 3D shape, up to a distortion that keeps straight lines straight. But for some special scenes this fails. Then a quite different scene, seen by quite different cameras, gives exactly the same two photos, and nothing in the photos can tell which one is real. These special scenes are the ones whose points, together with the two camera positions, lie on one curved surface of a certain kind, or on two flat planes. A scene that lies entirely on one flat wall is the most common example.

## The idea

**The definition.** A configuration $(P, P', \{\mathbf{X}_i\})$ is critical if there is another configuration $(Q, Q', \{\mathbf{Y}_i\})$ with the same images, $P\mathbf{X}_i \sim Q\mathbf{Y}_i$ and $P'\mathbf{X}_i \sim Q'\mathbf{Y}_i$ for all $i$, that is not of the form $(PH^{-1}, P'H^{-1}, \{H\mathbf{X}_i\})$ for any invertible $H$. The two configurations then have different fundamental matrices, both of which fit all matches.

**Why quadrics.** For any $F$, the set of points $\mathbf{X}$ with $(P'\mathbf{X})^{\mathsf T}F(P\mathbf{X}) = 0$ is the quadric surface $\mathbf{X}^{\mathsf T}(P'^{\mathsf T}FP)\mathbf{X} = 0$. For the true $F$ this holds for every point, so the symmetric part of $P'^{\mathsf T}FP$ is zero. For a second fundamental matrix $F_2$, the symmetric part of $S = P'^{\mathsf T}F_2P$ is not zero, so the scene points, whose images satisfy the second constraint too, lie on the quadric $\mathbf{X}^{\mathsf T}S\mathbf{X} = 0$. This quadric contains both camera centers, because $P\mathbf{C} = \mathbf{0}$ and $P'\mathbf{C}' = \mathbf{0}$. Hartley and Zisserman show that it is a ruled quadric, and that the converse also holds: points on a ruled quadric through both centers have a second reconstruction.

**The forms of the quadric.** The quadric can be a hyperboloid of one sheet, a cone, a pair of planes, or one of a few further degenerate cases. A pair of planes covers the planar scene: a scene plane together with any plane through the two centers. Recent work by Bråtelund gives a complete list for two and three uncalibrated views.

**Nearness matters.** Exactly critical data are rare. Data that lie near a critical surface are common, and the estimate of $F$ is then badly conditioned: small noise moves it a long way along the family of solutions. This is the practical reason to know these configurations.

**Calibrated cameras.** With known intrinsics the same idea applies to the [essential matrix](/essential-matrix/). Fewer configurations are critical, because the essential matrix has fewer degrees of freedom. In particular a planar scene is not critical for the [five-point algorithm](/five-point-algorithm/), although it is for the eight-point algorithm.

**More views.** Hartley and Kahl studied the configurations that remain critical for three and more views; they are much more special, and more views remove most ambiguities of two views.

## Examples

**A planar scene.** Let all points lie on the plane $Z = 4$, seen by $P_1 = [I \mid \mathbf{0}]$ and $P_2 = [I \mid (-1, 0, 0)^{\mathsf T}]$. Then the images are related by a [homography](/homography/) $H$: $\mathbf{x}'_i \sim H\mathbf{x}_i$. For any vector $\mathbf{e}'$ the matrix $F = [\mathbf{e}']_\times H$ satisfies
$$\mathbf{x}'^{\mathsf T}_i[\mathbf{e}']_\times H\mathbf{x}_i \sim \mathbf{x}'^{\mathsf T}_i(\mathbf{e}' \times \mathbf{x}'_i) = 0 .$$
So a two-parameter family of fundamental matrices fits all matches, and the matches fix only $H$. Here the quadric is the scene plane together with any plane through the two centers.

**A hyperboloid.** Take the hyperboloid of one sheet $x^2 + y^2 - z^2 = 1$ and put the two camera centers at $(1, 0, 0)$ and $(-1, 0, 0)$, which lie on it. Any set of scene points on this surface, however many, is critical: a second camera pair and a second point set give the same images. The hyperboloid is ruled: through each of its points pass two lines that lie on it, for example the lines $(1, s, s)$ and $(1, s, -s)$ through the first center.

**Not critical.** Points in general position, at least eight of them, with distinct camera centers, do not lie on one quadric through both centers, because a quadric has 9 degrees of freedom and the two centers and seven points in general position already fix one. So eight points in general position fix $F$ by the [eight-point algorithm](/eight-point-algorithm/).

**Seven points.** Through seven points and two centers there is always a quadric, and the [seven-point algorithm](/seven-point-algorithm/) indeed gives up to three fundamental matrices. These are not critical configurations in the usual sense, which asks for ambiguity whatever the number of points, but they show the same mechanism.

## Where it is used

- **Degeneracy in robust estimation.** A sample of points that lie mostly on one plane gives a wrong $F$ that many points support; robust methods such as [RANSAC](/ransac/) test samples for this case and fit a homography instead.
- **Model selection.** Pipelines decide between a homography and a fundamental matrix for each image pair, because a planar or almost planar scene is critical for $F$.
- **Choice of solver.** For calibrated cameras the five-point algorithm is preferred over the eight-point algorithm partly because it works on planar scenes.
- **Stability analysis.** Near-critical scenes explain large errors of [relative pose](/relative-pose-problem/) in some image pairs, and they guide the choice of views in [structure from motion](/incremental-structure-from-motion/).
- **Self-calibration.** A related notion, critical motion sequences, describes camera motions for which [self-calibration](/self-calibration/) has more than one solution.

## References
