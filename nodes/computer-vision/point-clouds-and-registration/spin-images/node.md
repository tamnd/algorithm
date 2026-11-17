---
tag: 9YPF70
kind: algorithm
slug: spin-images
name: Spin images
aliases:
- spin image descriptor
area: computer-vision/point-clouds-and-registration
level: core
summary: Describe an oriented point by the 2D histogram of its neighbors' distance from the normal axis and height along it, invariant to rotation about the normal.
model: real-ram
complexity:
  vars: {n: the number of points, W: the image width in cells, k: the number of points in the support region}
  time: {worst: O(n (n + W^2)), average: O(n (log n + k + W^2)), best: Ω(n (k + W^2))}
  space: {extra: Θ(n W^2)}
properties: {deterministic: true, exact: true, online: false, recursive: false, rigid_motion_invariant: true, needs_normals: true}
history:
  year: 1999
  people: [Andrew E. Johnson, Martial Hebert]
  note: "Johnson and Hebert described each oriented point of a surface by a 2D histogram of the cylindrical coordinates of the other points around its normal, and used these spin images to recognize objects in cluttered 3D scenes."
prereqs: [point-cloud-normal-estimation, bilinear-interpolation]
see_also: [point-feature-histograms, shot-descriptor, shape-context, geometric-hashing, feature-matching, principal-component-analysis, point-cloud-registration, iterative-closest-point]
sources:
  - paper: "Andrew E. Johnson and Martial Hebert, Using spin images for efficient object recognition in cluttered 3D scenes, IEEE Transactions on Pattern Analysis and Machine Intelligence 21(5), 1999"
    locator: "The spin map to the coordinates alpha and beta, the bin size, image width and support angle, the bilinear binning, the comparison of spin images, and the recognition pipeline"
  - paper: "Andrew E. Johnson, Spin-images: a representation for 3-D surface matching, PhD thesis, Carnegie Mellon University, 1997"
    locator: "The full account of the representation and of its parameters"
---

A spin image describes the shape of a surface around one point with a normal, an oriented point, by a small 2D picture. For every other point it records two numbers: $\alpha$, the distance from the line through the point along the normal, and $\beta$, the height along that line. It then counts the points in a grid of $(\alpha, \beta)$ cells, spreading each point over four cells by [bilinear interpolation](/bilinear-interpolation/). The picture is what one would get by spinning a sheet of paper about the normal and letting the surface leave marks on it, hence the name. Johnson and Hebert (1999) introduced spin images for object recognition in cluttered 3D scenes. They are simple to compute and need only the normal of the point, not a full local frame; the price is that turning parts of the surface about the normal does not change the picture.

## In plain words

Stand at a point of a surface and look along its normal. Every other point is at some distance from the normal line and at some height above or below the point. Forget in which direction around the line it lies, and keep only these two numbers. Then put a grid on the two numbers and count how many points fall in each cell, with a point near a cell border shared between the cells around it.

The grid is the spin image. If you turn the object or move it, the distances and heights stay the same, so the picture stays the same. Two points on two scans of the same object get similar pictures, which lets you find which points match.

## The problem

The input is a cloud of points with unit normals, an oriented point $(p, \mathbf{n})$, a bin size $b$, an image width $W$ in cells and a support angle $A$. The output is a $W \times W$ array of nonnegative numbers that describes the cloud around $p$, does not change when the cloud and the oriented point move together by a rotation and translation, and changes little when the points move a little. As for every local descriptor, there is no single correct output; the requirements are the invariance, the robustness to noise, clutter and occlusion, and the power to tell shapes apart.

## The algorithm

```pseudo id=main
SPIN-IMAGE(P, N, p, n, b, W, A)
L1  img ← a W × W array of zeros; β_max ← (W - 1) b / 2; α_max ← (W - 1) b
L2  for each point x of P, with normal n_x do
L3      if n · n_x < cos A then skip x
L4      β ← n · (x - p); α ← sqrt(‖x - p‖² - β²)
L5      if α > α_max or |β| > β_max then skip x
L6      u ← (β_max - β) / b; s ← α / b
L7      i ← ⌊u⌋; j ← ⌊s⌋; a ← u - i; c ← s - j
L8      add (1 - a)(1 - c) to img[i][j], a(1 - c) to img[i+1][j], (1 - a) c to img[i][j+1] and a c to img[i+1][j+1]
L9  return img
```

Line L4 is the spin map: $\beta$ is the height of $x$ along the normal, and $\alpha$ is its distance from the normal line, the length of the part of $x - p$ orthogonal to $\mathbf{n}$. These are cylindrical coordinates about the normal line without the angle. Line L3 is the support angle test: a point whose normal turns away from $\mathbf{n}$ by more than $A$ is likely on the other side of the object or a self occluding part, and it is left out. Line L5 is the support distance test, which keeps the description local. Line L6 puts $\beta = \beta_{\max}$ in row 0 and $\alpha = 0$ in column 0, so that the rows go down as the height goes down. Lines L7 and L8 split the unit weight of the point over its four nearest cells, by how near the point is to each. At the far border of the grid one of the four cells is outside it, and its weight is then 0, so the code leaves it out.

The point $p$ is a point of the cloud and adds weight 1 at $\alpha = 0$, $\beta = 0$. Images are compared by their correlation coefficient; Johnson and Hebert compare only the cells where both images have data, and combine the correlation with the number of such cells.

## Example

Take $p = (0, 0, 0)$ with $\mathbf{n} = (0, 0, 1)$, the bin size $b = 1$, the width $W = 5$ and the support angle $A = 60°$. Then $\beta_{\max} = 2$ and $\alpha_{\max} = 4$. The cloud has six points:

| point $x$ | normal $\mathbf{n}_x$ | angle to $\mathbf{n}$ | $(\alpha, \beta)$ | $(u, s)$ | cells and weights |
|---|---|---|---|---|---|
| $(0, 0, 0)$ | $(0, 0, 1)$ | 0° | $(0, 0)$ | $(2, 0)$ | $[2][0]$: 1 |
| $(1, 0, 0)$ | $(0, 0, 1)$ | 0° | $(1, 0)$ | $(2, 1)$ | $[2][1]$: 1 |
| $(0, 1.5, 0.5)$ | $(0, 0, 1)$ | 0° | $(1.5, 0.5)$ | $(1.5, 1.5)$ | $[1][1]$, $[1][2]$, $[2][1]$, $[2][2]$: 0.25 each |
| $(-2.4, 0, -1)$ | $(1, 0, 1)/\sqrt 2$ | 45° | $(2.4, -1)$ | $(3, 2.4)$ | $[3][2]$: 0.6, $[3][3]$: 0.4 |
| $(3, 4, 0)$ | $(0, 0, 1)$ | 0° | $(5, 0)$ | | out of support, $\alpha > 4$ |
| $(0.5, 0, 0)$ | $(0, 0, -1)$ | 180° | | | out of support, angle above 60° |

The spin image, with row 0 at $\beta = 2$ and column 0 at $\alpha = 0$:

| row | $\alpha = 0$ | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| $\beta = 2$ | 0 | 0 | 0 | 0 | 0 |
| $\beta = 1$ | 0 | 0.25 | 0.25 | 0 | 0 |
| $\beta = 0$ | 1 | 1.25 | 0.25 | 0 | 0 |
| $\beta = -1$ | 0 | 0 | 0.6 | 0.4 | 0 |
| $\beta = -2$ | 0 | 0 | 0 | 0 | 0 |

The entries sum to 4, the number of supported points. The point $(1, 0, 0)$ and any point $(\cos t, \sin t, 0)$ would give the same contribution, because the image does not see the angle about the normal.

## Correctness

By Pythagoras, $\alpha$ is the distance from $x$ to the normal line and $\beta$ the height along it, and two points have the same $(\alpha, \beta)$ exactly when a rotation about the normal line maps one to the other. A rigid motion of the cloud together with the oriented point keeps $\mathbf{n} \cdot (x - p)$, $\lVert x - p \rVert$ and $\mathbf{n} \cdot \mathbf{n}_x$, so the same points pass lines L3 and L5 with the same coordinates, and the image does not change. The bilinear weights of line L8 are nonnegative and sum to 1, and each cell gets the product of two tent functions, so the entries sum to the number of supported points and change continuously as a supported point moves. The full proof is below.

## Complexity

The model is the [real RAM](/real-ram/), with $n$ points, an image of $W \times W$ cells, and $k$ points in the support region of a point.

- **One image.** Line L1 costs $\Theta(W^2)$. By brute force, lines L2 to L8 cost $\Theta(n)$. With a [k-d tree](/kd-tree/) and a range query for the ball of radius $\sqrt{\alpha_{\max}^2 + \beta_{\max}^2}$, they cost $O(\log n + k)$ on average on well spread points.
- **All points.** $O(n (n + W^2))$ by brute force and $O(n (\log n + k + W^2))$ with a tree.
- **Space.** $\Theta(W^2)$ for one image, $\Theta(n W^2)$ to keep the images of all points for matching.
- **Matching.** Comparing two images costs $\Theta(W^2)$. Johnson and Hebert compress the images of a model with [principal component analysis](/principal-component-analysis/) to make the search for the best match faster.

## Properties

- **Rigid motion invariant.** The image depends only on distances and dot products with the normal.
- **Needs only a normal.** No full local reference frame is needed, unlike [SHOT](/shot-descriptor/); the normal line has no sign problem about its own axis.
- **Loses the angle.** Turning parts of the surface about the normal line does not change the image, so some different shapes look the same.
- **Depends on the normal sign.** Flipping $\mathbf{n}$ flips the image upside down; the normals must be oriented consistently.
- **Not scale invariant.** The bin size sets the scale, and two scans must use the same one.
- **Depends on sampling density.** The counts grow with the density; the original works on meshes with a uniform resolution, and the correlation coefficient removes a global scale of the counts.

## Variants and improvements

- **Mesh resampling.** The original resamples the mesh to an even resolution and sets the bin size near that resolution, so that counts on two scans are comparable.
- **Compressed spin images.** Projecting the images on their principal components gives short vectors for a fast nearest neighbor search.
- **Face based spin images.** Spreading the area of each mesh face, not its vertices, over the image makes it less dependent on the sampling.
- **Learned and frame based descriptors.** [FPFH](/point-feature-histograms/) and [SHOT](/shot-descriptor/) keep more of the shape and are now more common baselines.

## When to use it

Use spin images for 3D keypoint matching when the normals are reliable but a full local frame is not, for example on surfaces with near symmetric patches, and when a simple, well understood descriptor is enough. They are a classic choice for object recognition in range data and for the coarse alignment before [ICP](/iterative-closest-point/). On scans with very different densities, or when the patches are rich in detail, FPFH or SHOT usually match better.

## Pitfalls

- **Missing support angle.** Without line L3, points on the back of a thin object, with normals that point away, fall in the image and make it depend on the view.
- **Unoriented normals.** Line L4 uses the sign of $\mathbf{n}$. Normals from PCA have random signs, and an image from a flipped normal is the original upside down, so orient the normals first.
- **Rows and columns swapped.** Line L6 sets rows by $\beta$ and columns by $\alpha$. Mixing them up still gives an image, but one that does not match images from other code.
- **Cells out of the grid.** At $u = W - 1$ or $s = W - 1$, line L8 refers to a row or column outside the grid. Its weight is 0, but the code must check the index, not write past the end of the array.
- **Bin size against density.** With a bin size much smaller than the point spacing, line L8 gives a sparse, noisy image; with a much larger one, all detail is lost.
- **Negative values under the root.** Rounding can make $\lVert x - p \rVert^2 - \beta^2$ slightly negative at line L4 when $x$ is on the normal line. Clamp it to 0.

## Implementations

## History

Andrew Johnson developed spin images in his 1997 thesis at Carnegie Mellon, with Martial Hebert, for matching surfaces from range sensors. Johnson and Hebert (1999) gave the method its best known form: the spin map to $(\alpha, \beta)$, the bin size, image width and support angle as parameters, bilinear binning, a similarity measure built on the correlation coefficient, compression of the model images by principal component analysis, and a recognition pipeline that groups point matches by geometric consistency and checks each pose with ICP. The name comes from the picture of a sheet of paper spinning about the normal. Spin images were among the first local 3D descriptors in wide use, and they are still a standard baseline, next to the later [point feature histograms](/point-feature-histograms/) and [SHOT](/shot-descriptor/), and they are part of the Point Cloud Library.

## References
