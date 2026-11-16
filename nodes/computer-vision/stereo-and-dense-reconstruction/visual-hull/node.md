---
tag: EW4AGR
kind: definition
slug: visual-hull
name: Visual hull
aliases:
- shape from silhouettes
area: computer-vision/stereo-and-dense-reconstruction
level: core
summary: "The largest shape with the same silhouettes as an object from every view in a region. The cones of finitely many views give an outer bound on it."
prereqs: [pinhole-camera-model, convex-hull]
see_also: [space-carving, photo-consistency, multi-view-stereo, octree, marching-cubes, background-subtraction, epipolar-geometry, constructive-solid-geometry]
sources:
  - paper: doi:10.1109/34.273735
    title: "Aldo Laurentini, The visual hull concept for silhouette-based image understanding, IEEE Transactions on Pattern Analysis and Machine Intelligence 16(2), 1994, pages 150 to 162"
    locator: "the definition of the visual hull relative to a viewing region, the external visual hull, and the result that the visual hull is the largest object with the same silhouettes"
  - paper: doi:10.1145/344779.344951
    title: "Wojciech Matusik, Chris Buehler, Ramesh Raskar, Steven J. Gortler and Leonard McMillan, Image-based visual hulls, Proceedings of SIGGRAPH 2000, pages 369 to 374"
    locator: "the computation of the visual hull along the viewing rays of a new view from the silhouettes of the reference views"
  - paper: doi:10.1023/A:1008191222954
    title: "Kiriakos N. Kutulakos and Steven M. Seitz, A theory of shape by space carving, International Journal of Computer Vision 38(3), 2000, pages 199 to 218"
    locator: "the photo hull, the largest shape that is consistent with the colors of the images and not only with their silhouettes"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 12.7.3, Shape from silhouettes"
---

The visual hull of an object is the largest shape that casts the same silhouettes as the object in all views from a given region. A calibrated camera that sees the object as a silhouette, a region of foreground pixels, knows that the object lies inside the cone of rays from the camera center through that region. The intersection of the cones of several cameras is a shape that surely contains the object, and adding cameras can only make it smaller. Laurentini (1994) named the limit of this process, over all viewpoints in a region, the visual hull, and showed what it can and cannot recover: it never shows a concavity that no silhouette shows, such as the inside of a bowl. In practice, "visual hull" also names the intersection of the cones of the given cameras, which is the method called shape from silhouettes. It needs only a foreground mask in each image, so it is fast and robust, and it is a common first shape for [space carving](/space-carving/) and other [multi-view stereo](/multi-view-stereo/) methods.

## Definition

Let the object $S \subset \mathbb{R}^3$ be closed and bounded, and let $R$ be a set of viewpoints outside $S$. For a viewpoint $V$, the **cone** of $S$ is

$$C_V(S) = \{P \ne V : \text{the half-line from } V \text{ through } P \text{ meets } S\}.$$

A [pinhole camera](/pinhole-camera-model/) with center $V$ sees $S$ as its silhouette, and $C_V(S)$ is the set of points that project into the silhouette. Then:

- The **visual hull** of $S$ relative to $R$ is $\mathrm{VH}(S, R) = \bigcap_{V \in R} C_V(S)$. In words, a point $P$ is in the visual hull if and only if every half-line from a viewpoint in $R$ through $P$ meets $S$.
- The **external visual hull** is $\mathrm{VH}(S, R)$ for $R$ the set of all points outside the [convex hull](/convex-hull/) $\mathrm{CH}(S)$, the viewpoints from which the whole object can be seen from outside.
- For finitely many cameras $V_1, \dots, V_N$, the **silhouette-cone intersection** is $H_N = \bigcap_{i=1}^{N} C_{V_i}(S)$. For an orthographic camera with view direction $d$, the cone is replaced by the cylinder of lines with direction $d$ that meet $S$.

Three facts follow from the definition.

1. **It keeps the silhouettes.** $S \subseteq \mathrm{VH}(S, R)$, and for each $V \in R$, a half-line from $V$ meets $\mathrm{VH}(S, R)$ if and only if it meets $S$. So the visual hull casts the same silhouettes as $S$ from all of $R$.
2. **It is the largest such shape.** If $S'$ casts the same silhouettes as $S$ from every $V \in R$, then every half-line from $V$ through a point of $S'$ meets $S$, so $S' \subseteq \mathrm{VH}(S, R)$.
3. **Finite views bound it from outside.** If $V_1, \dots, V_N \in R$, then $S \subseteq \mathrm{VH}(S, R) \subseteq H_N$, and $H_{N+1} \subseteq H_N$.

For the external visual hull there is a test without viewpoints: a point $P$ is in it if and only if every line through $P$ meets $S$. If a line through $P$ misses $S$, choose $V$ on this line outside $\mathrm{CH}(S)$; the half-line from $V$ through $P$ misses $S$. If every line through $P$ meets $S$, then $P \in \mathrm{CH}(S)$, and for $V$ outside $\mathrm{CH}(S)$ the line through $V$ and $P$ meets the convex hull in a segment that holds $P$ but not $V$, so the half-line from $V$ through $P$ holds that segment and meets $S$. The same test shows that the external visual hull lies inside the convex hull.

## Examples and non-examples

**A convex object.** If $S$ is convex, its external visual hull is $S$ itself: it lies between $S$ and $\mathrm{CH}(S) = S$. Silhouettes recover a convex object exactly, given enough views.

**A sphere from two or three views.** A ball of radius $r$ seen by orthographic cameras along the $X$ and $Z$ axes has disks as silhouettes, and $H_2$ is the intersection of two cylinders, the Steinmetz solid, of volume $\tfrac{16}{3} r^3 \approx 5.333 r^3$. The ball has volume $\tfrac43 \pi r^3 \approx 4.189 r^3$, so the two views give a shape 27.3% too large. A third view along $Y$ gives the intersection of three cylinders, of volume $8 (2 - \sqrt2) r^3 \approx 4.686 r^3$, which is 11.9% too large. With views from all directions, the intersection is the ball.

**Non-example: the inside of a bowl.** Let $S$ be a bowl, and let $P$ be a point in its hollow below the rim. Every line through $P$ has a half that points down or sideways, and that half meets the wall or the bottom. So by the test above, $P$ is in the external visual hull: the visual hull of a bowl is filled up to the plane of the rim. No silhouette, from any viewpoint, can show the hollow. Color can: [space carving](/space-carving/) uses [photo-consistency](/photo-consistency/) to remove such points when the surface has texture. Its plus-shaped example shows the same effect on a grid: the silhouettes do not show the inner corners of the plus, so carving with silhouettes alone keeps 6 voxels there.

**Non-example: the convex hull.** The external visual hull can be much smaller than the convex hull. For a torus, the line along its axis misses the torus, so the center of the hole is not in the visual hull, though it is in the convex hull.

**Non-example: ghosts from few views.** Two balls of radius $r$ with centers $(d, 0, 0)$ and $(0, d, 0)$, $d > 2 r$, seen by orthographic cameras along the $X$ and $Y$ axes, give two disks in each image. The cylinders along $X$ lie at $y = 0$ and $y = d$, and the cylinders along $Y$ lie at $x = 0$ and $x = d$, so $H_2$ has four parts, at $(0, 0)$, $(d, 0)$, $(0, d)$ and $(d, d)$. Two of them are ghosts with no object in them. A third view, for example along $Z$, removes them. Scenes with several people seen by few cameras show this effect.

## Related definitions

- **Silhouette.** The set of image points whose rays meet the object. In practice it comes from [background subtraction](/background-subtraction/) or another [segmentation](/image-segmentation/), and an error in one mask cuts the object in every view. A missing foreground pixel removes a whole ray from the hull.
- **Photo hull.** Kutulakos and Seitz (2000) defined the photo hull as the largest shape whose rendering matches the colors of all images. If the background differs in color from the object, a photo-consistent shape also has the right silhouettes, so the photo hull lies inside the visual hull.
- **Voxel, polyhedral and image-based visual hulls.** A voxel version keeps the cells of a grid or an [octree](/octree/) whose projections fall inside every silhouette, and [marching cubes](/marching-cubes/) turns the result into a mesh. A polyhedral version intersects the cones of the silhouette polygons, as in [constructive solid geometry](/constructive-solid-geometry/). The image-based visual hull of Matusik et al. (2000) computes, for each pixel of a new view, the intervals of its ray that lie inside all cones, by intersecting the projection of the ray, an epipolar line ([epipolar geometry](/epipolar-geometry/)), with each silhouette. It needs no volume and runs in real time.
- **Space carving and voxel coloring.** [Space carving](/space-carving/) with only the background test gives the visual hull of the grid, and [voxel coloring](/voxel-coloring/) and space carving with color tests give shapes inside it.

## References
