---
tag: 6HV01C
kind: algorithm
slug: normalized-eight-point-algorithm
name: Normalized eight-point algorithm
aliases:
- Hartley's eight-point algorithm
area: computer-vision/multiple-view-geometry
level: core
summary: "The eight-point algorithm run on Hartley-normalized points and mapped back by F = T2^T G T1. The normalization makes the linear system well conditioned and the result stable."
solves: [relative-pose-problem]
model: floating-point-model
complexity:
  vars: {n: the number of point pairs}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1997
  people: [Richard Hartley]
  note: Hartley showed in 1997 that the eight-point algorithm becomes accurate when the points of each image are first translated and scaled.
prereqs: [eight-point-algorithm, hartley-normalization]
see_also: [fundamental-matrix, seven-point-algorithm, sampson-distance, algebraic-and-geometric-error, condition-number, ransac, dlt-homography, essential-matrix-decomposition]
sources:
  - paper: doi:10.1109/34.601246
    title: "Richard I. Hartley, In defense of the eight-point algorithm, IEEE Transactions on Pattern Analysis and Machine Intelligence 19(6), 1997, 580-593"
    locator: "the isotropic normalization of the points, the condition of the linear system, and the comparison with iterative methods"
  - book: isbn:9780521540513
    title: "Richard Hartley and Andrew Zisserman, Multiple View Geometry in Computer Vision, second edition, Cambridge University Press, 2004"
    locator: "Section 11.2, The normalized 8-point algorithm"
  - book: isbn:9783030343712
    title: "Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022"
    locator: "Section 11.3, Two-frame structure from motion (the normalized eight-point algorithm)"
---

The normalized eight-point algorithm estimates the [fundamental matrix](/fundamental-matrix/) from $n \ge 8$ point matches in pixels. It first gives each image its own similarity $T_1$ or $T_2$ that moves the centroid of its points to the origin and makes their mean distance to it $\sqrt2$, which is [Hartley normalization](/hartley-normalization/). Then it runs the [eight-point algorithm](/eight-point-algorithm/) on the moved points, forces rank 2 there, and maps the result back by $F = T_2^{\mathsf T}GT_1$. Hartley (1997) showed that this cheap change turns a method thought to be useless on real images into a good one. It is the standard linear estimate of $F$ and the usual start of a geometric refinement.

## In plain words

Pixel coordinates are numbers of a few hundred, and the equations of the eight-point algorithm multiply them together, so the table of equations mixes numbers near 1 with numbers near a hundred thousand. In such a table small errors in the big numbers hide the information in the small ones. The fix is to change units in each image before solving. Move the points so that they sit around the origin, and shrink them so that a typical point is about one unit away. Solve in these units, make the answer have the right form, and then convert it back to pixels. The extra work is tiny, and the answer becomes much more accurate.

## The problem

**Input.** Point pairs $(\mathbf{x}_{1,i}, \mathbf{x}_{2,i})$, $i = 1, \ldots, n$, $n \ge 8$, as 2D pixel points $(u, v)$ that the algorithm extends to $(u, v, 1)^{\mathsf T}$. The points of each image must not all be equal.

**Output.** A $3 \times 3$ matrix $F$ of rank 2 with $\|F\|_F = 1$ and with its entry of largest absolute value positive. If the pairs are exact images of points in general position seen by two cameras with different centers, the output is the true fundamental matrix in this form.

## The algorithm

```pseudo id=main
NORMALIZED-EIGHT-POINT(x1_1 .. x1_n, x2_1 .. x2_n)
L1  T1 <- the similarity that moves the centroid of the x1_i to 0 and makes their mean distance to it sqrt(2)
L2  T2 <- the same similarity for the x2_i
L3  for i <- 1 to n
L4      y1 <- T1 x1_i ; y2 <- T2 x2_i
L5      append the row (y2[1] y1^T, y2[2] y1^T, y2[3] y1^T) to A
L6  g <- the right singular vector of A for its smallest singular value
L7  G <- the 3 x 3 matrix with rows g[1..3], g[4..6], g[7..9]
L8  (U, diag(s1, s2, s3), V) <- the SVD of G
L9  G <- U diag(s1, s2, 0) V^T
L10 F <- T2^T G T1
L11 return F / ||F||_F, with the sign that makes its entry of largest absolute value positive
```

Lines L1 and L2 compute each similarity from its own points: $T = \begin{pmatrix} s & 0 & -s\bar u \\ 0 & s & -s\bar v \\ 0 & 0 & 1 \end{pmatrix}$, with $(\bar u, \bar v)$ the centroid and $s = \sqrt2/d$ for the mean distance $d$ to it. Lines L3 to L9 are the eight-point algorithm on the moved points: line L5 is the row with $(A\mathbf{g})_i = \mathbf{y}_2^{\mathsf T}G\mathbf{y}_1$, line L6 minimizes $\|A\mathbf{g}\|$ over unit vectors by the [SVD](/singular-value-decomposition/), and line L9 forces rank 2. The rank step is done before line L10, so it acts on the well scaled matrix. Line L10 undoes the change: if $\mathbf{y}_2^{\mathsf T}G\mathbf{y}_1 = 0$ with $\mathbf{y}_1 = T_1\mathbf{x}_1$ and $\mathbf{y}_2 = T_2\mathbf{x}_2$, then $\mathbf{x}_2^{\mathsf T}(T_2^{\mathsf T}GT_1)\mathbf{x}_1 = 0$. Since $T_1$ and $T_2$ are invertible, $F$ has rank 2 as $G$ has.

## Example

Take the eight points of the [eight-point example](/eight-point-algorithm/) seen by two cameras with $K = \begin{pmatrix} 500 & 0 & 320 \\ 0 & 500 & 240 \\ 0 & 0 & 1 \end{pmatrix}$. The pixel points of image 1 are $(320, 240)$, $(445, 365)$, $(236.67, 406.67)$, $(520, 140)$, $(195, 115)$, $(445, -10)$, $(220, 140)$ and $(486.67, 406.67)$; those of image 2 are $(820, 240)$, $(1127.692, 432.308)$, $(671.852, 425.185)$, $(1320, 61.429)$, $(596.316, 108.421)$, $(1127.692, -144.615)$, $(667.826, 131.304)$ and $(1181.111, 517.778)$.

| line | value |
|---|---|
| L1 | scale $0.0078605$, translation $(-2.81832, -1.77189)$ |
| L2 | scale $0.0043619$, translation $(-4.09608, -0.96606)$ |
| L3 to L5 | 8 rows with entries of size about 1 |
| L6 | the singular values of $A$ are $5.515, 4.766, 4.321, 3.260, 2.215, 0.863, 0.154, 0.0849$ and 0; the ratio of the largest to the smallest nonzero one is 65.0 |
| L7 to L9 | $G$ has rank 2 already, so line L9 changes it only by rounding |
| L10, L11 | $F = \begin{pmatrix} 0 & 0 & 0 \\ 2.7157 \times 10^{-5} & 0 & -0.0267945 \\ -0.0065176 & 0.0226305 & 0.9993635 \end{pmatrix}$ |

The output is the canonical form of $K^{-\mathsf T}EK^{-1} \sim \begin{pmatrix} 0 & 0 & 0 \\ 0.6 & 0 & -592 \\ -144 & 500 & 22080 \end{pmatrix}$. The epipolar distances of the eight points are about $10^{-13}$ pixels. Without lines L1 and L2, the nonzero singular values of $A$ run from $1.407 \times 10^6$ down to $1.133$, a ratio of $1.24 \times 10^6$. On these exact data both forms still give the true $F$, but the difference shows with noise. In a test with 30 points, 10 random scenes and Gaussian noise of 1 pixel, the mean distance of the points to their epipolar lines was about 0.67 pixels for the normalized form and about 3.5 pixels for the plain form, and the normalized form was better in 8 of the 10 scenes.

## Correctness

Line L10 is a change of coordinates: $\mathbf{y}_2^{\mathsf T}G\mathbf{y}_1 = \mathbf{x}_2^{\mathsf T}T_2^{\mathsf T}GT_1\mathbf{x}_1$. On exact data, the moved pairs are exact matches for the fundamental matrix $T_2^{-\mathsf T}F_0T_1^{-1}$, so the eight-point algorithm on them returns this matrix up to scale, and line L10 gives back $F_0$. The result has rank 2 because $T_1$ and $T_2$ are invertible. If the points of image 1 are moved by a similarity $S_1$ and those of image 2 by $S_2$, the normalized points change only by a rotation and a reflection, and the output becomes the canonical form of $S_2^{-\mathsf T}FS_1^{-1}$. The full proof is below.

## Complexity

Lines L1 and L2 cost $\Theta(n)$, the loop costs $\Theta(n)$, and the SVD of the $n \times 9$ matrix $A$ costs $\Theta(n)$ because the number of columns is fixed. Lines L7 to L11 work on $3 \times 3$ matrices and cost $\Theta(1)$. So the time is $\Theta(n)$ and the extra space is $\Theta(n)$ for $A$, the same as the plain algorithm.

In [floating point](/floating-point-model/) the gain is in the [condition number](/condition-number/) of $A$. After normalization each entry of a row is a product of two numbers of size about 1, so all nine columns of $A$ have about the same size. Hartley (1997) analyses the condition number of $A^{\mathsf T}A$ and shows how it grows with the size of the pixel coordinates when no normalization is done.

## Properties

- **Exact on exact data.** Like the plain algorithm, for eight or more exact matches in general position with two different camera centers.
- **Covariant under similarities.** Moving the points of each image by a similarity changes the output in the same way as the true $F$. The plain algorithm does not have this property.
- **Linear and non-iterative.** The cost is about the same as the plain algorithm.
- **Algebraic, not geometric.** The output minimizes the algebraic error of the normalized points. It is close to, but not equal to, the maximum likelihood estimate.
- **Rank step in normalized coordinates.** The closest rank 2 matrix is taken for $G$, not for $F$. In pixel coordinates the Frobenius norm has no good meaning.

## Variants and improvements

- **Anisotropic scaling.** Scale $u$ and $v$ separately so that each has unit variance. This is a common alternative; the isotropic form of lines L1 and L2 is the usual choice.
- **Essential matrix.** For calibrated cameras, run the essential variant on normalized image coordinates $K^{-1}\mathbf{x}$; those are already small and centered for most cameras, so the extra similarity matters less.
- **Seven points.** The same normalization is used by the [seven-point algorithm](/seven-point-algorithm/), which forces $\det F = 0$ exactly.
- **Geometric refinement.** Use the output to start a minimization of the [Sampson distance](/sampson-distance/) or of the reprojection error. This is the Gold Standard method in Hartley and Zisserman.
- **Inside RANSAC.** Use the [seven-point algorithm](/seven-point-algorithm/) as the minimal solver in [RANSAC](/ransac/), and then the normalized eight-point algorithm on all inliers.

## When to use it

Use it whenever a fundamental matrix must be found linearly from eight or more pixel matches: on the inliers of a robust fit, as the start of a nonlinear refinement, or alone when moderate accuracy is enough. There is no reason to run the plain algorithm on pixel data. For calibrated cameras and data with outliers, the [five-point algorithm](/five-point-algorithm/) in RANSAC is usually the better first step.

## Pitfalls

- **One similarity for both images.** Each image needs its own $T$ from its own points.
- **The rank step after denormalizing.** Forcing rank 2 on $F$ in pixels, instead of on $G$, loses much of the gain.
- **Wrong side of the transpose.** Line L10 is $T_2^{\mathsf T}GT_1$, not $T_2^{-1}GT_1$; the fundamental matrix maps points to lines, so it changes by the transpose on the left.
- **All points equal.** The mean distance is then 0 and the similarity is not defined. Check for this before line L1.
- **Degenerate scenes.** Normalization does not fix planar scenes or pure rotations, where $A$ has rank at most 6.
- **Outliers.** The least squares fit has no robustness. Use it inside or after [RANSAC](/ransac/).

## Implementations

## History

The eight-point algorithm of Longuet-Higgins (1981) was long held to be very sensitive to noise, and iterative methods were preferred. Hartley (1997), in a paper titled "In defense of the eight-point algorithm", showed that the poor results came from the bad condition of the linear system on pixel coordinates, and that translating and scaling the points first gives results close to those of iterative methods in his tests. The same idea applies to other linear estimates, such as the [DLT for homographies](/dlt-homography/). Hartley and Zisserman (2000, second edition 2004) present the normalized eight-point algorithm in Section 11.2.

## References
