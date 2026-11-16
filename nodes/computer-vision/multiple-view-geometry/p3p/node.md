---
tag: E145BQ
kind: algorithm
slug: p3p
name: P3P
aliases:
- perspective-three-point
- Grunert's method
area: computer-vision/multiple-view-geometry
level: core
summary: "Solve the pose from three point pairs by finding the distances to the three points from a quartic equation, giving up to four solutions."
solves: [perspective-n-point]
model: real-ram
complexity:
  vars: {n: "the number of point pairs, three to solve and the rest to choose among the solutions"}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1841
  people: [Johann August Grunert, Robert M. Haralick, Martin A. Fischler, Robert C. Bolles]
  note: Grunert solved the problem in 1841 by a quartic in a ratio of distances. Fischler and Bolles used it in 1981 as the minimal solver inside RANSAC, and Haralick and coauthors reviewed the classical solutions in 1994.
prereqs: [perspective-n-point, camera-intrinsic-matrix, polynomial-root-finding]
see_also: [epnp, minimal-solver, ransac, reprojection-error, five-point-algorithm, cheirality, companion-matrix-method, rigid-body-transformation]
sources:
  - paper: doi:10.1007/BF02028352
    title: "Robert M. Haralick, Chung-Nan Lee, Karsten Ottenberg and Michael Nolle, Review and analysis of solutions of the three point perspective pose estimation problem, International Journal of Computer Vision 13(3), 1994, 331-356"
    locator: "Grunert's solution, the other classical direct solutions and their numerical behavior"
  - paper: doi:10.1145/358669.358692
    title: "Martin A. Fischler and Robert C. Bolles, Random sample consensus, a paradigm for model fitting with applications to image analysis and automated cartography, Communications of the ACM 24(6), 1981, 381-395"
    locator: the location determination problem with three points, its quartic and its use inside RANSAC
  - paper: doi:10.1109/TPAMI.2003.1217599
    title: "Xiao-Shan Gao, Xiao-Rong Hou, Jianliang Tang and Hang-Fei Cheng, Complete solution classification for the perspective-three-point problem, IEEE Transactions on Pattern Analysis and Machine Intelligence 25(8), 2003, 930-943"
    locator: the number of real solutions as a function of the data
  - paper: doi:10.1109/34.67632
    title: "William J. Wolfe, Donald Mathis, Cheryl Weber Sklair and Michael Magee, The perspective view of three points, IEEE Transactions on Pattern Analysis and Machine Intelligence 13(1), 1991, 66-73"
    locator: the geometry of the multiple solutions
  - paper: doi:10.1109/CVPR.2011.5995464
    title: "Laurent Kneip, Davide Scaramuzza and Roland Siegwart, A novel parametrization of the perspective-three-point problem for a direct computation of absolute camera position and orientation, CVPR 2011, 2969-2976"
    locator: the direct computation of the pose without the distances
  - paper: doi:10.1007/978-3-030-01225-0_20
    title: "Mikael Persson and Klas Nordberg, Lambda Twist, an accurate fast robust perspective three point (P3P) solver, ECCV 2018, Lecture Notes in Computer Science, 334-349"
    locator: the solver through one real root of a cubic
---

P3P finds the pose of a calibrated camera from three known world points and their images. It is the smallest case of the [perspective-n-point problem](/perspective-n-point/) with a finite number of answers: three pairs give six equations for the six unknowns of the pose. The classical method of Grunert (1841) does not solve for the pose directly. It first finds the distances $s_1, s_2, s_3$ from the camera center to the three points. The angles between the three viewing rays and the sides of the world triangle give three equations from the law of cosines. With the ratios $u = s_2/s_1$ and $v = s_3/s_1$, they reduce to one quartic in $v$. Each positive real root gives the three points in the camera frame, and the pose is the rigid motion that maps the world triangle onto them. There are at most four solutions, and usually two. A fourth point picks the right one. The method is the standard [minimal solver](/minimal-solver/) for pose inside [RANSAC](/ransac/).

## In plain words

You know where three marks are in the world, and you see them in one photo of a camera whose lens you know. Each mark in the photo tells you a direction from the camera. So you know the angle between each pair of directions, and you know how far apart the marks are. The camera must sit at a place from which the three marks are seen under exactly these angles. The method finds how far each mark is from the camera, then turns and moves the triangle of marks to match. Usually two places fit, and up to four can fit. A fourth mark tells you which one is right.

## The problem

**Input.** Three world points $\mathbf{X}_1, \mathbf{X}_2, \mathbf{X}_3$ that are not collinear, and their images $\mathbf{y}_1, \mathbf{y}_2, \mathbf{y}_3$ in normalized coordinates, $\mathbf{y} = K^{-1}\mathbf{x}$ for pixels $\mathbf{x}$ and the [intrinsic matrix](/camera-intrinsic-matrix/) $K$. For the selection step, one or more further pairs $(\mathbf{X}_i, \mathbf{y}_i)$.

**Output.** Every pose $(R, \mathbf{t})$ with $R$ a rotation such that $R\mathbf{X}_i + \mathbf{t} = s_i\mathbf{f}_i$ with $s_i > 0$ for $i = 1, 2, 3$, where $\mathbf{f}_i$ is the unit vector along $(y_{i,1}, y_{i,2}, 1)$. The selection step returns the one with the smallest [reprojection error](/reprojection-error/) on the further pairs.

## The algorithm

Write $\cos\alpha$, $\cos\beta$ and $\cos\gamma$ for the cosines of the angles at the center between the rays $(2, 3)$, $(1, 3)$ and $(1, 2)$, and $a = \|\mathbf{X}_2 - \mathbf{X}_3\|$, $b = \|\mathbf{X}_1 - \mathbf{X}_3\|$, $c = \|\mathbf{X}_1 - \mathbf{X}_2\|$ for the sides opposite to them. The three triangles formed by the center and two of the points give
$$s_2^2 + s_3^2 - 2s_2s_3\cos\alpha = a^2, \quad s_1^2 + s_3^2 - 2s_1s_3\cos\beta = b^2, \quad s_1^2 + s_2^2 - 2s_1s_2\cos\gamma = c^2 .$$
Put $s_2 = us_1$, $s_3 = vs_1$, $Q(v) = v^2 - 2v\cos\beta + 1$ and $p = (a^2 - c^2)/b^2$. The second equation gives $s_1^2 = b^2/Q(v)$, and the other two become
$$\text{(A)}\;\; u^2 - 2u\cos\gamma + 1 - \tfrac{c^2}{b^2}Q(v) = 0, \qquad \text{(B)}\;\; u^2 - 2uv\cos\alpha + v^2 - \tfrac{a^2}{b^2}Q(v) = 0 .$$
Their difference is linear in $u$: $uD(v) = N(v)$ with $N(v) = (p - 1)v^2 - 2p\cos\beta\,v + 1 + p$ and $D(v) = 2(\cos\gamma - v\cos\alpha)$. Put $u = N/D$ into (A) and multiply by $D^2$:
$$G(v) = N^2 - 2\cos\gamma\,ND + \Bigl(1 - \tfrac{c^2}{b^2}Q\Bigr)D^2 = A_4v^4 + A_3v^3 + A_2v^2 + A_1v + A_0 = 0 .$$
Written out, this is the quartic of Grunert in the form given by Haralick and coauthors (1994), with $A_4 = (p - 1)^2 - 4\frac{c^2}{b^2}\cos^2\alpha$ and $A_0 = (1 + p)^2 - 4\frac{a^2}{b^2}\cos^2\gamma$.

```pseudo id=main
P3P(X1, X2, X3, y1, y2, y3)
L1  f_i <- (y_i1, y_i2, 1) / || (y_i1, y_i2, 1) ||, for i = 1, 2, 3
L2  cos α <- f2 · f3 ; cos β <- f1 · f3 ; cos γ <- f1 · f2
L3  a <- || X2 - X3 || ; b <- || X1 - X3 || ; c <- || X1 - X2 ||
L4  form the polynomials N(v), D(v) and the quartic G(v)
L5  for each real root v > 0 of G
L6      if D(v) is not close to 0 then U <- { N(v) / D(v) }
L7      else U <- the real roots u of (A)
L8      for each u in U with u > 0
L9          s1 <- b / sqrt(Q(v)) ; s2 <- u s1 ; s3 <- v s1 ; skip u if the three cosine equations fail
L10         Y_i <- s_i f_i, for i = 1, 2, 3
L11         (R, t) <- the rigid motion with R X_i + t = Y_i, from a frame built on each triangle
L12         add (R, t) to the output unless it is already there
L13 return the output

P3P-SELECT(X1 .. Xn, y1 .. yn), n >= 4
L14 S <- P3P(X1, X2, X3, y1, y2, y3)
L15 return the pose in S with the smallest sum of squared reprojection errors on pairs 4 .. n
```

Line L7 handles the case $D(v) = 0$, where $u = N/D$ is not defined. Then $N(v) = 0$ as well, the equations (A) and (B) are the same, and both roots of (A) are candidates. The check in line L9 has two jobs. In exact arithmetic it always passes. In floating point it rejects a root near a common root of $N$ and $D$, where $N/D$ is only a ratio of rounding errors. Line L11 builds on each triangle the orthonormal frame with $\mathbf{e}_1$ along the first side and $\mathbf{e}_3$ along the normal, and sets $R = F_YF_X^{\mathsf T}$ and $\mathbf{t} = \mathbf{Y}_1 - R\mathbf{X}_1$. Any solver of the [Wahba problem](/wahba-problem/), such as the [Kabsch algorithm](/kabsch-algorithm/), gives the same motion here.

## Example

Take the world points $\mathbf{X}_1 = (0, 0, 0)$, $\mathbf{X}_2 = (1, 0, 0)$, $\mathbf{X}_3 = (0.3, 1, 0)$, the fourth point $\mathbf{X}_4 = (1, 1, 1)$, and the true pose $R = R_y(0.3)R_x(0.2)$, $\mathbf{t} = (0.2, -0.1, 4)$, with angles in radians. The images are $\mathbf{y}_1 = (0.05, -0.025)$, $\mathbf{y}_2 = (0.3119, -0.0270)$, $\mathbf{y}_3 = (0.1330, 0.2146)$ and $\mathbf{y}_4 = (0.3113, 0.1411)$. All values are rounded to four places.

| line | value |
|---|---|
| L2 | $\cos\alpha = 0.9583$, $\cos\beta = 0.9693$, $\cos\gamma = 0.9683$ |
| L3 | $a = \sqrt{1.49} = 1.2207$, $b = \sqrt{1.09} = 1.0440$, $c = 1$, so $p = 0.4495$ |
| L4 | $G(v)/A_4 = v^4 - 3.9974v^3 + 5.9821v^2 - 3.9714v + 0.9866$ |
| L5 | two real roots, $v = 0.8678$ and $v = 1.0558$ |
| L6 | $u = 1.0193$ and $u = 0.9689$ |
| L9 | $(s_1, s_2, s_3) = (3.9253, 4.0011, 3.4063)$ and $(4.0062, 3.8817, 4.2298)$ |
| L11 | the first pose has $\mathbf{t} = (0.1960, -0.0980, 3.9192)$; the second is the true pose |
| L15 | the reprojection errors of $\mathbf{X}_4$ are $0.1798$ and $3 \times 10^{-12}$, so the second pose is chosen |

The second set of distances matches the true camera frame points $(0.2, -0.1, 4)$, $(1.1553, -0.1, 3.7045)$ and $(0.5453, 0.8801, 4.1011)$, whose lengths are $4.0062$, $3.8817$ and $4.2298$. The first pose also puts the three points exactly on their rays in front of the camera, so three points alone cannot tell the two apart.

## Correctness

Each valid pose gives distances that satisfy the three cosine equations. Each solution of those equations with positive distances gives exactly one rotation and translation, because two triangles with the same sides are related by one rigid motion, and a right-handed frame on each makes it a rotation. The substitution $s_2 = us_1$, $s_3 = vs_1$ is reversible, and the difference of (A) and (B) is $N - uD$, so a pair $(u, v)$ solves both if and only if $G(v) = 0$ and either $u = N/D$, or $D(v) = N(v) = 0$ and $u$ solves (A). So the output is exactly the set of valid poses. At a root with $D = N = 0$, the quartic has a double root, so the total count is still at most 4 unless $G$ is the zero polynomial. The full proof is in the proof file of this page.

## Complexity

The solver does a fixed number of arithmetic steps and solves one quartic. In the real RAM model, with the roots of a quartic as one step, P3P takes $\Theta(1)$ time and space. In floating point the roots come from a closed form or from a few iterations of a root finder such as the [companion matrix method](/companion-matrix-method/). P3P-SELECT adds $\Theta(1)$ work for each further pair and each of at most four poses, so it takes $\Theta(n)$ time and $\Theta(1)$ extra space.

## Properties

- **At most four solutions.** This is a theorem. On random scenes with the camera a few units away, two solutions are by far the most common case, and one or four occur in a few percent of the scenes.
- **Minimal.** Three pairs give six equations for six unknowns, so P3P has no redundancy and cannot detect an error in its own data.
- **Rotation always proper.** The output is a rotation with determinant $+1$, not a reflection, because both frames of line L11 are right-handed.
- **Positive depths built in.** Only $u > 0$ and $v > 0$ are kept, so every point is in front of the camera.
- **Independent of the world frame.** Only the side lengths of the world triangle enter the quartic.

## Variants and improvements

- **Other eliminations.** Haralick and coauthors (1994) compared Grunert's method with the later direct solutions of Finsterwalder, Merritt, Fischler and Bolles, Linnainmaa and others. They differ in which ratio is the unknown and in their numerical stability.
- **Direct pose.** Kneip, Scaramuzza and Siegwart (2011) solve a quartic for parameters of the pose itself and skip the distances.
- **Cubic first.** Lambda Twist of Persson and Nordberg (2018) finds one real root of a cubic and then two quadratics, followed by a short Gauss-Newton polish. It is faster and more stable than the quartic solvers.
- **Generalized cameras.** With rays that do not meet in one center, the problem becomes the generalized P3P of the [generalized camera model](/generalized-camera-model/).
- **More points.** For $n \ge 4$ points, linear and iterative methods such as [EPnP](/epnp/) solve the overdetermined problem. P3P stays the solver inside RANSAC and is followed by refinement of the reprojection error on all inliers.

## When to use it

Use P3P inside RANSAC when you have many 2D-3D matches with outliers, for example to place a new image in [incremental structure from motion](/incremental-structure-from-motion/) or to relocalize a camera against a map. The small sample of three keeps the number of RANSAC iterations low. Test each of the up to four poses on the other matches, then refine the best one on its inliers. When the matches are already clean and many, use a method for $n$ points instead.

## Pitfalls

- **Pixels instead of normalized coordinates.** The angles between rays need $\mathbf{y} = K^{-1}\mathbf{x}$; pixels give wrong cosines.
- **Danger cylinder.** When the camera center lies on the cylinder through the three points with its axis normal to their plane, two solutions merge into a double root. Near it the pose is unstable, as Thompson (1966) described for space resection.
- **Division by zero.** $D(v) = 0$ happens at true solutions, for example when the second ray is perpendicular to the side $\mathbf{X}_1\mathbf{X}_3$. An implementation that always divides then returns a wrong pose.
- **False roots.** A common root of $N$ and $D$ is a root of $G$ that is not a solution; without the check of line L9 it gives a pose that does not fit the rays.
- **Collinear points.** Three collinear world points do not fix the rotation about their line; the solver must reject them.
- **Picking one solution blindly.** The smallest distance or the first root is not the true pose in general. Use a fourth point or the RANSAC consensus.

## Implementations

## History

Grunert (1841) solved the problem of finding the position of a point from the angles under which it sees three known points, the extended Pothenot problem of surveying, by a quartic in a ratio of distances. Photogrammetry used the same problem for space resection, and Thompson (1966) described its failure on the danger cylinder. Fischler and Bolles (1981) brought it into computer vision as the location determination problem and used it as the solver inside RANSAC. Wolfe and coauthors (1991) explained the geometry of the multiple solutions, and Haralick and coauthors (1994) reviewed the classical direct solutions and their numerical stability. Gao and coauthors (2003) classified the number of real solutions completely. Kneip and coauthors (2011) and Persson and Nordberg (2018) gave faster and more stable solvers.

## References
