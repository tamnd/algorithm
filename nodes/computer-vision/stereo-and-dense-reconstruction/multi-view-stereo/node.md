---
tag: EDFG84
kind: problem
slug: multi-view-stereo
name: Multi-view stereo
aliases:
- MVS
- dense multi-view reconstruction
area: computer-vision/stereo-and-dense-reconstruction
level: core
summary: Reconstruct a dense 3D surface, depth maps or point set from many images of a scene whose cameras are known, by finding the shape on which the images agree.
model: real-ram
complexity:
  vars: {N: the number of images, W: the image width in pixels, H: the image height in pixels}
  time: {worst: Ω(N W H)}
prereqs: [stereo-matching, photo-consistency, epipolar-geometry, pinhole-camera-model]
see_also: [plane-sweep-stereo, patch-based-multi-view-stereo, patchmatch-stereo, depth-map-fusion, space-carving, structure-from-motion-problem, neural-radiance-field, gaussian-splatting]
sources:
  - paper: doi:10.1109/CVPR.2006.19
    title: Steven M. Seitz, Brian Curless, James Diebel, Daniel Scharstein and Richard Szeliski, A comparison and evaluation of multi-view stereo reconstruction algorithms, IEEE Conference on Computer Vision and Pattern Recognition 2006
    locator: Section 2 (the taxonomy of scene representation, photo-consistency measure, visibility model, shape prior, reconstruction algorithm and initialization) and the sections on the data sets and on the accuracy and completeness measures
  - paper: doi:10.1561/0600000052
    title: "Yasutaka Furukawa and Carlos Hernández, Multi-view stereo: a tutorial, Foundations and Trends in Computer Graphics and Vision 9(1-2), pages 1 to 148, 2015"
    locator: the chapters on photo-consistency, on algorithms for depth maps, point clouds and volumes, and on large photo collections
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 12, Depth estimation (the sections on multi-view stereo)
---

Multi-view stereo, or MVS, is the problem of computing a dense 3D model of a scene from many photographs whose cameras are known. "Dense" means a depth for almost every pixel, or a surface that covers the visible scene, not only a few hundred matched corners. Two-view [stereo matching](/stereo-matching/) is the special case with two images. With more images, each surface point is seen from several directions, so a wrong match is easier to detect and occluded parts of one view are seen in another. The cameras usually come from [structure from motion](/structure-from-motion-problem/), which gives sparse points and camera poses; MVS then fills in the dense shape. The main tool is [photo-consistency](/photo-consistency/): a point on the true surface looks the same in all images that see it.

## In plain words

You walk around a statue and take thirty photos, and you know exactly where the camera was for each one. Now you want a full 3D model of the statue, not just a few points. For any guess of a point in space, you can look at where it would appear in every photo. If the guess is on the statue, all photos show the same color there. If the guess is in the air or inside the stone, the photos show different things. Multi-view stereo is the search for the surface where all the photos agree, done for millions of points.

## Definition

**Input.**

- Images $I_1, \dots, I_N$ of a static scene, each $W \times H$ pixels.
- For each image a camera, with intrinsic matrix $K_i$ and pose $(R_i, t_i)$, so that a point $X$ maps to the pixel $\pi_i(X) \sim K_i (R_i X + t_i)$ of the [pinhole model](/pinhole-camera-model/).
- Often a bounding volume or a depth range, and sometimes silhouettes.

**Output.** One of these scene representations (Seitz et al. 2006 list voxels, level sets, polygon meshes and depth maps; point and patch sets are also common):

- a depth map $Z_i(u, v)$ for each image, or for chosen reference images;
- a set of 3D points, often with normals;
- an occupancy or signed distance function on a grid, with a surface extracted from it;
- a triangle mesh.

**Goal.** A surface $S$ such that for every point $X \in S$ and every image $i$ that sees $X$ (no other part of $S$ lies between $X$ and the center of camera $i$), the values of $I_i$ near $\pi_i(X)$ agree. Real images are noisy, the surface is not exactly Lambertian, and parts of it have no texture, so the problem is posed as an optimization: minimize a photo-consistency cost plus a smoothness or shape prior. There is no single correct output, and methods are compared on benchmarks.

**Measures.** Seitz et al. (2006) compare a reconstruction $R$ with a ground truth surface $G$ from a laser scan. The *accuracy* is the distance $d$ such that 90 percent of $R$ lies within $d$ of $G$. The *completeness* is the fraction of $G$ that lies within 1.25 mm of $R$. Both thresholds are choices of the benchmark.

## Variants

- **Two views or many.** With $N = 2$ and rectified images, the problem is stereo matching along rows. With $N > 2$ there is no common rectification, so methods work in 3D or with plane-induced warps.
- **Object or scene.** Small objects inside a known volume can use volumetric methods and silhouettes. Large outdoor scenes and internet photo collections need methods that work per view or per cluster of views.
- **Known or unknown cameras.** MVS assumes the cameras are known. When they are not, structure from motion and [bundle adjustment](/bundle-adjustment/) come first.
- **Passive or active.** MVS uses the light that is already there. [Structured light scanning](/structured-light-scanning/) projects patterns, and [photometric stereo](/photometric-stereo/) changes the lighting; they are other problems with other assumptions.
- **Reconstruction or view synthesis.** [Neural radiance fields](/neural-radiance-field/) and [3D Gaussian splatting](/gaussian-splatting/) fit a scene model whose purpose is to render new views. The geometry they give is a side product, not the target of the fit.

## Examples

**Depth from two rectified views.** A camera with focal length $f = 500$ pixels and a second camera $b = 0.1$ m to its right see a point with disparity $d = 20$ pixels. Then $Z = f b / d = 500 \cdot 0.1 / 20 = 2.5$ m, as on [depth from disparity](/depth-from-disparity/).

**A third view removes the doubt.** Add a third camera at $0.2$ m on the same line. A point at depth $Z$ has disparity $f b / Z$ in each camera, so the true depth 2.5 m gives 20 pixels in the second camera and 40 pixels in the third. Suppose the texture repeats so that the second camera also shows the same color at disparity 25, which is the depth $500 \cdot 0.1 / 25 = 2.0$ m. With two views the two depths cannot be told apart. At $Z = 2.0$ the third camera must show the point at disparity $500 \cdot 0.2 / 2.0 = 50$ pixels, not 40. Unless the texture also repeats there, the third view rejects the wrong depth. This is the reason that more views make matching more reliable.

**Scoring a reconstruction.** A reconstruction has 10 points whose distances to the ground truth, in mm, are 0.1, 0.1, 0.2, 0.2, 0.3, 0.3, 0.4, 0.5, 0.6 and 2.0. The accuracy at 90 percent is the least $d$ that covers 9 of the 10 points, $d = 0.6$ mm. If 8 of 10 ground truth points have a reconstructed point within 1.25 mm, the completeness is 80 percent.

## Known algorithms

Seitz et al. (2006) sort algorithms into four classes by how they reconstruct. The pages of this area fall into them as follows.

| Class | Method | Output | Note |
|---|---|---|---|
| Volume cost, then surface | [space carving](/space-carving/), [voxel coloring](/voxel-coloring/) | voxels | carve voxels that are not photo-consistent |
| Volume cost, then surface | [TSDF fusion](/tsdf-fusion/) | signed distance grid | averages depth maps; the surface by [marching cubes](/marching-cubes/) |
| Depth maps | [plane sweep stereo](/plane-sweep-stereo/) | depth map per view | sweeps planes and keeps the best per pixel |
| Depth maps | [PatchMatch stereo](/patchmatch-stereo/) | depth and normal per pixel | random search with propagation |
| Depth maps | [depth map fusion](/depth-map-fusion/) | merged model | removes conflicts between depth maps |
| Feature growing | [patch-based MVS](/patch-based-multi-view-stereo/) | oriented patches | match, expand, filter |
| Surface evolution | (no page yet) | mesh or level set | moves a surface to lower a cost |

Methods of the depth map class scale well, since each view is handled on its own, and they are common in large systems. The [visual hull](/visual-hull/) from silhouettes is often the start of the volumetric methods. Neural scene models are a newer, separate approach.

## Bounds

- **Input size.** A method that gives a depth for every pixel must, in the worst case, read every pixel: the value of a pixel that it does not read can change its answer. So the time is $\Omega(N W H)$ on the real RAM. Plane sweep with $D$ planes takes $\Theta(D N W H)$ for one reference view.
- **No unique answer.** On a surface with no texture, many shapes give the same images, so the images do not decide the shape. Kutulakos and Seitz (2000) proved that, for a fixed photo-consistency test of the monotone kind they define and a volume that contains the scene, the union of all photo-consistent shapes is itself photo-consistent. They call it the *photo hull*, and space carving computes it. The photo hull contains the true scene, but it can be larger.
- **Benchmarks, not guarantees.** Accuracy and completeness numbers are measured on given data (the Middlebury data of Seitz et al., and later sets such as DTU and ETH3D). They depend on the data set and the version of the benchmark and are not properties of an algorithm.

## Reductions

- **To stereo matching.** For $N = 2$, rectify the pair with [stereo rectification](/stereo-rectification/) and solve stereo matching along rows; the depth is $f b / d$.
- **To many depth problems and a fusion.** Pick each image in turn as the reference, compute its depth map from its neighbors with plane sweep or PatchMatch, then merge the maps by depth map fusion. Most large systems use this reduction.
- **To labeling.** Over a fixed set of depths or voxels, the problem becomes a labeling with a data term from photo-consistency and a smoothness term. This is the same form as in [graph cut stereo](/graph-cut-stereo/) and can be solved with the same methods.

## Applications

- 3D models of buildings, cities and cultural heritage from photographs, after structure from motion.
- Surveying and mapping from aerial images and drones.
- Models for visual effects, games and virtual reality.
- Dense geometry for robots and for inspection, where active sensors are not available.

## References
