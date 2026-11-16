---
tag: 9B2YVJ
kind: technique
slug: hartley-normalization
name: Hartley normalization
aliases:
- isotropic point normalization
- data normalization for DLT
area: computer-vision/multiple-view-geometry
level: core
summary: Translate and scale the points of each image so that their centroid is the origin and their mean distance is sqrt(2) before a linear estimate, which makes it stable.
model: floating-point-model
prereqs: [dlt-homography, condition-number]
see_also: [normalized-eight-point-algorithm, eight-point-algorithm, dlt-camera-resectioning, homography-estimation, algebraic-and-geometric-error, trifocal-tensor, singular-value-decomposition, floating-point-model]
sources:
  - paper: doi:10.1109/34.601246
    title: "Richard I. Hartley, In defense of the eight-point algorithm, IEEE Transactions on Pattern Analysis and Machine Intelligence 19(6), 1997, 580-593"
    locator: the isotropic scaling of the points, the analysis of the condition number of the linear system, and the experiments on real images
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Section 4.4, Transformation invariance and normalization (Section 4.4.4, Normalizing transformations, and the normalized DLT); Chapter 11 (the normalized 8-point algorithm for the fundamental matrix)"
---

Hartley normalization is a preparation step for linear estimates in multiple view geometry. Before the estimate, it moves the points of each image so that their centroid is at the origin, and scales them so that their mean distance from the origin is $\sqrt2$; after the estimate, it undoes the change on the result. On raw pixel coordinates the linear systems of the [DLT](/dlt-homography/) and the [eight-point algorithm](/eight-point-algorithm/) are badly conditioned, and this step makes them well conditioned and their answer independent of the choice of the pixel frame. This page is about the step itself and where it applies; the full homography method that uses it is [DLT for homographies](/dlt-homography/), and the cost that the linear methods minimize is discussed in [algebraic and geometric error](/algebraic-and-geometric-error/).

## In plain words

The equations of a linear estimate mix very different numbers: a 1, pixel coordinates of a few hundred, and products of two coordinates of a few hundred thousand. When numbers of such different sizes sit in one table, small errors in the large numbers swamp the small ones, and the answer can be poor even when the points are good. The fix is to change units first. Move each image's points so that they sit around the origin, and shrink them so that a typical point is about one unit away. Now all numbers in the table have the same size. Solve, and then convert the answer back to pixels. It costs almost nothing and often turns a bad answer into a good one.

## When it applies

- The estimate is linear in the unknown entries of a matrix, and each equation is a product of point coordinates in homogeneous form $(x, y, 1)$: the DLT for a [homography](/homography/), the [eight-point algorithm](/eight-point-algorithm/) for the fundamental matrix, [DLT resectioning](/dlt-camera-resectioning/) of a camera matrix, and the linear estimate of a [trifocal tensor](/trifocal-tensor/).
- The coordinates are far from the origin or large compared with 1, as pixel coordinates always are.
- The method minimizes an [algebraic error](/algebraic-and-geometric-error/), which changes with the coordinate frame. A method that minimizes a distance in pixels does not change its minimizer under a similarity of the frame, so it needs the step only for the numerical behavior of its iterations, not for its answer.

## The template

```pseudo id=main
NORMALIZE(p_1 .. p_n)
L1  c <- (1/n) sum_i p_i
L2  m <- (1/n) sum_i ||p_i - c||
L3  s <- sqrt(2) / m
L4  T <- [ s 0 -s c_x ; 0 s -s c_y ; 0 0 1 ]
L5  return T

ESTIMATE-WITH-NORMALIZATION(x_1 .. x_n, x'_1 .. x'_n)
L6  T <- NORMALIZE(x_1 .. x_n) ; T' <- NORMALIZE(x'_1 .. x'_n)
L7  y_i <- T x_i ; y'_i <- T' x'_i for every i
L8  M~ <- the linear estimate from the pairs (y_i, y'_i)
L9  undo the change: H = T'^-1 H~ T for a homography, F = T'^T F~ T for a fundamental matrix
L10 return the result
```

Each image gets its own $T$ (line L6). Line L9 depends on how the matrix acts. A homography maps points to points, $\mathbf{y}' \sim \tilde H\mathbf{y}$, so $\mathbf{x}' \sim T'^{-1}\tilde H T\mathbf{x}$. A fundamental matrix gives a bilinear form, $\mathbf{y}'^{\mathsf T}\tilde F\mathbf{y} = \mathbf{x}'^{\mathsf T}T'^{\mathsf T}\tilde F T\mathbf{x}$, so $F = T'^{\mathsf T}\tilde F T$. For a camera matrix $P$ from 3D to 2D, the 3D points get a similarity $U$ that gives centroid 0 and mean distance $\sqrt3$, and $P = T^{-1}\tilde P U$.

**Why it works.** A row of the homography DLT for a pixel pair contains entries of size 1, of the size of a coordinate $x \approx 10^2$ to $10^3$, and of the size of a product $x x' \approx 10^5$ to $10^6$. The matrix $A^{\mathsf T}A$ then has a very large [condition number](/condition-number/), and the right singular vector of the smallest singular value, which is the answer, is very sensitive to rounding and to noise in the large entries. Hartley (1997) showed that after normalization the condition number is small and that the linear result becomes close to the result of iterative methods. A second gain is invariance: the normalized DLT gives the same homography (moved accordingly) when either image is moved, turned or scaled, which the plain DLT does not (see the remark in the proof of the [DLT page](/dlt-homography/)).

**A measured example.** Take the five pixel points $(100, 100)$, $(500, 120)$, $(520, 400)$, $(90, 380)$, $(300, 250)$ and their images under $H = \begin{pmatrix} 1 & 0.1 & 5 \\ -0.05 & 1 & 10 \\ 0.0002 & 0.0001 & 1 \end{pmatrix}$. The $10 \times 9$ DLT matrix of the raw points has largest singular value about $4.9 \cdot 10^5$ and eighth singular value about $0.65$, a ratio of about $7.5 \cdot 10^5$. After normalization the same two values are about $5.46$ and $1.44$, a ratio of about $3.8$. The ninth singular value is 0 in both cases, since the data are exact. The ratio of the largest to the eighth singular value measures how well the null vector is separated from the rest: it governs how much noise moves the answer. In a run of 200 trials with 20 random points in a $640 \times 480$ image, Gaussian noise of 1 pixel in both images and a fixed seed, the median root mean square error of the transferred points over a grid was 1.07 pixels with normalization and 2.35 pixels without; the worst trial gave 2.7 and 13.7 pixels.

## Classic examples

- **[DLT for homographies](/dlt-homography/).** HZ Algorithm 4.2, the normalized DLT, is the plain DLT between two normalizations.
- **[Normalized eight-point algorithm](/normalized-eight-point-algorithm/).** The case that Hartley's 1997 paper is about. Without normalization the [eight-point algorithm](/eight-point-algorithm/) was thought to be too sensitive to noise for practical use.
- **[DLT resectioning](/dlt-camera-resectioning/).** The camera matrix from 2D to 3D pairs, with a 2D normalization of the image points and a 3D normalization, mean distance $\sqrt3$, of the scene points.
- **[Trifocal tensor](/trifocal-tensor/).** The linear estimate from point and line matches in three views normalizes each view in the same way.
- **[Zhang's calibration method](/zhang-calibration-method/).** It estimates one homography per view of a planar target, and each of them is a normalized DLT.

## Variations

- **Root mean square instead of the mean.** Some code scales so that the root mean square distance is $\sqrt2$, which means that the mean of the squared coordinates is 1 in each axis on average. The effect on the conditioning is the same.
- **Anisotropic scaling.** Scale each axis, or each principal axis of the point cloud, to unit spread. Hartley (1997) considered this and found that it gives little gain over the isotropic version.
- **Fixed normalization by the image size.** Move the origin to the image center and divide by the larger image side. This needs no statistics of the points and is enough in many applications, but it is less good when the points cover only a small part of the image.
- **Normalization of lines.** Lines transform with $T^{-\mathsf T}$, so a method that uses matched lines applies the same $T$ to them in that form.

## Pitfalls

- **One $T$ for both images.** The two point sets have different centroids and spreads. Normalize each image with its own statistics.
- **The wrong undo.** A homography and a fundamental matrix undo the change in different ways (line L9). Using $T'^{-1}\tilde F T$ for a fundamental matrix gives a wrong matrix.
- **Thresholds in the wrong units.** A residual computed in normalized coordinates is in units of about $1/s$ pixels. Convert it before comparing it with a threshold in pixels, for example in [RANSAC](/ransac/).
- **Outliers in the statistics.** One gross outlier far away can make $m$ large and shrink the good points to a small cluster. Compute $T$ on the inliers after a robust step, or on the sample.
- **Equal points.** If all points of one image coincide, $m = 0$ and the step fails; the estimate is then degenerate anyway.
- **Not a cure for degeneracy.** The step improves conditioning, not geometry. If the points are near one line, the normalized system is still near singular.

## References
