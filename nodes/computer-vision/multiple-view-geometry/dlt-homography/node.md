---
tag: 12XVFY
kind: algorithm
slug: dlt-homography
name: Direct linear transformation for homography
aliases:
- DLT
- DLT algorithm
- normalized DLT for homographies
area: computer-vision/multiple-view-geometry
level: core
summary: Stack two linear equations per point pair into a system Ah = 0 and take h as the right singular vector of A of least singular value.
solves: [homography-estimation]
model: floating-point-model
complexity:
  vars: {n: the number of point pairs}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1971
  people: [Y. I. Abdel-Aziz, H. M. Karara, Richard Hartley]
  note: Abdel-Aziz and Karara named the direct linear transformation in close-range photogrammetry in 1971. Hartley showed in 1997 that normalizing the points first makes linear estimates of this kind accurate.
prereqs: [homography, homography-estimation, singular-value-decomposition]
see_also: [hartley-normalization, algebraic-and-geometric-error, homography-decomposition, dlt-camera-resectioning, eight-point-algorithm, ransac, condition-number, image-stitching]
sources:
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Section 4.1, The Direct Linear Transformation (DLT) algorithm, and Section 4.4, Transformation invariance and normalization (the normalized DLT, Algorithm 4.2)"
  - paper: doi:10.1109/34.601246
    title: "Richard I. Hartley, In defense of the eight-point algorithm, IEEE Transactions on Pattern Analysis and Machine Intelligence 19(6), 1997, 580-593"
    locator: the normalization of the points and why it improves the condition of the linear system
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 8.1, Pairwise alignment (the linear least squares estimate of a homography)"
---

The direct linear transformation (DLT) for homographies estimates the $3 \times 3$ matrix $H$ with $\mathbf{x}'_i \sim H\mathbf{x}_i$ from $n \ge 4$ point pairs. Each pair gives two equations that are linear in the nine entries of $H$. The algorithm stacks them into a $2n \times 9$ matrix $A$ and returns the unit vector $\mathbf{h}$ that makes $\|A\mathbf{h}\|$ smallest, which is a right singular vector of $A$. This page gives the normalized form (Hartley and Zisserman, Algorithm 4.2): it first moves and scales the points of each image with [Hartley normalization](/hartley-normalization/), and without that step the result on pixel data is poor. The problem it solves, with its other costs and methods, is on the page [homography estimation](/homography-estimation/); the same linear idea for a $3 \times 4$ camera matrix is [DLT resectioning](/dlt-camera-resectioning/).

## In plain words

The rule $\mathbf{x}' \sim H\mathbf{x}$ says that $H\mathbf{x}$ points in the same direction as $\mathbf{x}'$. Two vectors point in the same direction when their cross product is zero, and that gives equations in which the unknown entries of $H$ appear only to the first power. Each pair of points gives two useful equations, so four pairs give eight equations for the nine entries, which fixes $H$ up to its overall size. With more pairs and noisy points no $H$ fits all equations, so the algorithm takes the $H$ that leaves the smallest total leftover. Pixel coordinates are large numbers, and the equations mix them with 1, which makes the leftover depend on the units. Moving the points to the origin and shrinking them first fixes this.

## The problem

**Input.** Point pairs $(\mathbf{x}_i, \mathbf{x}'_i)$, $i = 1, \ldots, n$, $n \ge 4$, given as 2D points, which the algorithm extends to $(x, y, 1)^{\mathsf T}$.

**Output.** A $3 \times 3$ matrix $H$ with $\|H\|_F = 1$ and with its entry of largest absolute value positive. It minimizes the algebraic error of the normalized points, $\|A\mathbf{h}\|$ subject to $\|\mathbf{h}\| = 1$, and then is moved back to the original coordinates. If the pairs are exact images of the points under an invertible homography $H_0$, and four of the points have no three on a line, the output is $H_0$ scaled to this form.

## The algorithm

```pseudo id=main
DLT-HOMOGRAPHY(x_1 .. x_n, x'_1 .. x'_n)
L1  T <- the similarity that moves the centroid of the x_i to 0 and makes their mean distance to it sqrt(2)
L2  T' <- the same similarity for the x'_i
L3  for i <- 1 to n
L4      y_i <- T x_i ; (u', v', w') <- T' x'_i
L5      append the row [ 0^T , -w' y_i^T , v' y_i^T ] to A
L6      append the row [ w' y_i^T , 0^T , -u' y_i^T ] to A
L7  h <- the right singular vector of A for its smallest singular value
L8  H~ <- the 3 x 3 matrix with rows h[1..3], h[4..6], h[7..9]
L9  H <- T'^-1 H~ T
L10 return H / ||H||_F, with the sign that makes its entry of largest absolute value positive
```

Lines L1 and L2 are [Hartley normalization](/hartley-normalization/): each image gets its own similarity. The rows of L5 and L6 come from $\mathbf{y}'_i \times \tilde H \mathbf{y}_i = \mathbf{0}$. Write $\mathbf{h}^{j\mathsf T}$ for row $j$ of $\tilde H$; then $\tilde H\mathbf{y}_i = (\mathbf{h}^{1\mathsf T}\mathbf{y}_i, \mathbf{h}^{2\mathsf T}\mathbf{y}_i, \mathbf{h}^{3\mathsf T}\mathbf{y}_i)^{\mathsf T}$, and the first two entries of the cross product are $v'\,\mathbf{h}^{3\mathsf T}\mathbf{y}_i - w'\,\mathbf{h}^{2\mathsf T}\mathbf{y}_i$ and $w'\,\mathbf{h}^{1\mathsf T}\mathbf{y}_i - u'\,\mathbf{h}^{3\mathsf T}\mathbf{y}_i$. The third entry is a combination of these two when $w' \ne 0$, so it adds nothing and is left out. Line L7 is the minimizer of $\|A\mathbf{h}\|$ over unit vectors, found by the [singular value decomposition](/singular-value-decomposition/). Line L9 undoes the normalization: if $\mathbf{y}' \sim \tilde H\mathbf{y}$ with $\mathbf{y} = T\mathbf{x}$ and $\mathbf{y}' = T'\mathbf{x}'$, then $\mathbf{x}' \sim T'^{-1}\tilde H T\mathbf{x}$. Line L10 picks one of the matrices $\lambda H$ so that equal homographies give equal outputs.

## Example

Map the unit square $(0, 0)$, $(1, 0)$, $(1, 1)$, $(0, 1)$ to the trapezoid $(0, 0)$, $(4, 0)$, $(3, 2)$, $(1, 2)$.

| line | value |
|---|---|
| L1 | centroid $(\frac12, \frac12)$, mean distance $\frac{\sqrt2}{2}$, scale 2: $T = \begin{pmatrix} 2 & 0 & -1 \\ 0 & 2 & -1 \\ 0 & 0 & 1 \end{pmatrix}$, and the $\mathbf{y}_i$ are $(\pm 1, \pm 1)$ |
| L2 | centroid $(2, 1)$, mean distance $\frac{\sqrt5 + \sqrt2}{2} \approx 1.8251$, scale $s = 2\sqrt2/(\sqrt5 + \sqrt2) \approx 0.7749$: $T' = \begin{pmatrix} s & 0 & -2s \\ 0 & s & -s \\ 0 & 0 & 1 \end{pmatrix}$ |
| L3 to L6 | 8 rows; for the third pair, $\mathbf{y} = (1, 1, 1)$ and $T'(3, 2, 1)^{\mathsf T} = (s, s, 1)$, so the rows are $[0, 0, 0, -1, -1, -1, s, s, s]$ and $[1, 1, 1, 0, 0, 0, -s, -s, -s]$ |
| L7, L8 | $A$ has rank 8, and its null vector gives $\tilde H \sim \begin{pmatrix} 2s & 0 & 0 \\ 0 & 1.5s & 0.5s \\ 0 & 0.5 & 1.5 \end{pmatrix} \approx \begin{pmatrix} 1.5497 & 0 & 0 \\ 0 & 1.1623 & 0.3874 \\ 0 & 0.5 & 1.5 \end{pmatrix}$ |
| L9 | $T'^{-1}\tilde H T \sim \begin{pmatrix} 4 & 2 & 0 \\ 0 & 4 & 0 \\ 0 & 1 & 1 \end{pmatrix}$ |
| L10 | $\|H\|_F = \sqrt{38}$; the output is that matrix divided by $\sqrt{38} \approx 6.1644$, with largest entry $4/\sqrt{38} \approx 0.6489$ |

A check of one pair: $H(1, 1, 1)^{\mathsf T} = (6, 4, 2)^{\mathsf T} \sim (3, 2, 1)^{\mathsf T}$. For the third pair, the rows of the plain DLT without normalization would be $[0, 0, 0, -1, -1, -1, 2, 2, 2]$ and $[1, 1, 1, 0, 0, 0, -3, -3, -3]$, and both are orthogonal to $\mathbf{h} = (4, 2, 0, 0, 4, 0, 0, 1, 1)$.

## Correctness

Each pair of rows is equivalent to $\mathbf{y}'_i \times \tilde H\mathbf{y}_i = \mathbf{0}$, which is $\mathbf{y}'_i \sim \tilde H\mathbf{y}_i$ when $\tilde H\mathbf{y}_i \ne \mathbf{0}$. On exact data, four pairs with no three of the points on a line make $A$ of rank exactly 8. Then the null space of $A$ is spanned by the true normalized matrix, so line L7 returns it up to sign, and line L9 gives back the true $H$ up to scale. For noisy data, the right singular vector of the smallest singular value minimizes $\|A\mathbf{h}\|$ over unit vectors, by the [SVD](/singular-value-decomposition/). The full proof is below.

## Complexity

Counting arithmetic operations, lines L1 and L2 cost $\Theta(n)$, the loop costs $\Theta(n)$, and $A$ has $2n$ rows and a fixed number of 9 columns. The SVD of a $2n \times 9$ matrix costs $\Theta(n)$: for example, a QR decomposition reduces it to a $9 \times 9$ triangle in $\Theta(n)$ operations, and the SVD of that triangle takes a fixed amount of work. So the time is $\Theta(n)$. The matrix $A$ needs $\Theta(n)$ extra space; a version that only keeps $A^{\mathsf T}A$ needs $\Theta(1)$, at the price of squaring the [condition number](/condition-number/).

In [floating point](/floating-point-model/) the accuracy depends on the condition of $A$. Without normalization the entries of a row range from about 1 to the product of two pixel coordinates, around $10^5$ or $10^6$, and the gap between the smallest and the second smallest singular value is tiny compared with the largest one. Normalization makes all entries about 1. The page on [Hartley normalization](/hartley-normalization/) gives a measured example.

## Properties

- **Exact on exact data.** If $\mathbf{x}'_i \sim H_0\mathbf{x}_i$ for an invertible $H_0$ and four of the points are in general position, the output is $H_0$ in canonical form, for any number $n \ge 4$ of pairs.
- **Covariant under similarities.** If the points of the first image are moved by a similarity $S$ and those of the second by $S'$, the output becomes the canonical form of $S' H S^{-1}$. The plain DLT, without lines L1 and L2, does not have this property: its result depends on where the origin of the pixel frame is and on the unit.
- **Linear and non-iterative.** No starting point and no iterations; the cost is one SVD.
- **Algebraic, not geometric.** On noisy data the output minimizes the algebraic error of the normalized points, not a distance in pixels. See [algebraic and geometric error](/algebraic-and-geometric-error/).
- **Swap gives the inverse.** On exact data, exchanging the two images returns the canonical form of $H_0^{-1}$.

## Variants and improvements

- **Plain DLT.** Lines L1 and L2 with $T = T' = I$. It is HZ's basic algorithm and is fine only for small, centered coordinates.
- **Fix $h_{33} = 1$.** Solve an ordinary $2n \times 8$ [least squares problem](/least-squares-problem/) for the other eight entries. It fails when the true $h_{33}$ is 0 or near 0, which happens when the origin of image 1 maps to a point at or near infinity.
- **Normal equations.** Take the eigenvector of $A^{\mathsf T}A$ for its smallest [eigenvalue](/eigenvalue/). It needs only a $9 \times 9$ matrix, but squares the condition number.
- **Four points in closed form.** For exactly four pairs, map both quadruples to the canonical frame $(1, 0, 0)$, $(0, 1, 0)$, $(0, 0, 1)$, $(1, 1, 1)$ and compose; this is fast in a [minimal solver](/minimal-solver/) inside [RANSAC](/ransac/).
- **Lines and mixed data.** A matched pair of lines satisfies $\mathbf{l}_i \sim H^{\mathsf T}\mathbf{l}'_i$, so $\mathbf{l}_i \times H^{\mathsf T}\mathbf{l}'_i = \mathbf{0}$ gives two more rows that are linear in $\mathbf{h}$, and lines and points can share one matrix $A$.
- **Refinement.** Use the output as the starting point of a geometric fit, the Gold Standard method of [homography estimation](/homography-estimation/) or a [Sampson](/sampson-distance/) fit, with [Levenberg-Marquardt](/levenberg-marquardt/).

## When to use it

Use the normalized DLT whenever a homography must be found from point matches: as the minimal solver inside RANSAC, as the estimate on the inliers, and as the start of a nonlinear refinement. On its own it is accurate enough for many tasks, such as stitching previews or document rectification. When the best accuracy matters, for example in calibration or measurement, refine it with a geometric cost. If the matches contain outliers, do not run it on all of them: one gross outlier can move the result far.

## Pitfalls

- **No normalization.** On pixel coordinates the plain DLT can be wrong by many pixels, even with little noise.
- **One normalization for both images.** Each image needs its own $T$, computed from its own points.
- **Degenerate points.** Three of four points on a line, or all points near one line, make the two smallest singular values of $A$ both near 0. Check that the second smallest singular value is not close to the smallest one.
- **Direction.** The result maps image 1 to image 2. For the other direction use $H^{-1}$, not $H^{\mathsf T}$.
- **Comparing results.** $H$ and $-H$ are the same homography. Compare canonical forms, or compare the maps on test points.
- **Outliers.** The algebraic least squares fit has no robustness. Use it inside [RANSAC](/ransac/) or another robust method.

## Implementations

## History

The name direct linear transformation comes from photogrammetry, where Abdel-Aziz and Karara (1971) estimated the camera from linear equations in the entries of its matrix. In computer vision the same idea gives the homography from four or more point pairs. The method was long held to be inaccurate. Hartley (1997) showed, for the eight-point algorithm and for linear estimates in general, that the poor results came from the bad condition of the system on raw pixel coordinates, and that translating and scaling the points first makes the linear estimate nearly as good as iterative ones. Hartley and Zisserman (2000, second edition 2004) give the normalized DLT for homographies as their Algorithm 4.2.

## References
