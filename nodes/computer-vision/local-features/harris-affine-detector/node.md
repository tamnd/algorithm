---
tag: 3SB3Q7
kind: algorithm
slug: harris-affine-detector
name: Harris-affine and Hessian-affine detectors
aliases:
- Harris-affine
- Hessian-affine
- Mikolajczyk-Schmid affine detector
area: computer-vision/local-features
level: advanced
summary: Detect Harris or Hessian points at their characteristic scale and refine each to an affine covariant ellipse by shape adaptation.
solves: [feature-detection]
model: real-ram
complexity:
  vars: {P: the number of input points, K: the largest number of iterations per point, r: the radius of the largest Gaussian kernel in the normalized patch}
  time: {worst: O(P K r^3), average: O(P K r^3), best: O(P r^3)}
  space: {extra: O(r^2)}
properties: {deterministic: true, exact: false, approximately_affine_invariant: true, iterative: true, heuristic: true}
history:
  year: 2004
  people: [Krystian Mikolajczyk, Cordelia Schmid]
  note: Mikolajczyk and Schmid combined Harris-Laplace points with the affine shape adaptation of Lindeberg and Garding (1997) and Baumberg (2000), and gave the full iterative algorithm in their 2004 journal paper.
prereqs: [harris-laplace-detector, invariant-local-features]
see_also: [maximally-stable-extremal-regions, determinant-of-hessian-detector, detector-repeatability, affine-camera-model, homography, sift, positive-definite-matrix, eigenvalue]
sources:
  - paper: doi:10.1023/B:VISI.0000027790.02288.f2
    title: Krystian Mikolajczyk and Cordelia Schmid, Scale and affine invariant interest point detectors, International Journal of Computer Vision 60(1), 63-86, 2004
    locator: Section 3 (3.2, the affine normalization and the measure Q of Eq. 10; 3.3, the iterative detection algorithm)
  - paper: doi:10.1016/S0262-8856(97)01144-X
    title: Tony Lindeberg and Jonas Garding, Shape-adapted smoothing in estimation of 3-D shape cues from affine deformations of local 2-D brightness structure, Image and Vision Computing 15(6), 415-434, 1997
    locator: the sections on the fixed point of affine shape adaptation
  - paper: doi:10.1109/CVPR.2000.855899
    title: Adam Baumberg, Reliable feature matching across widely separated views, IEEE Conference on Computer Vision and Pattern Recognition (CVPR 2000), 2000
    locator: the section on the affine adaptation of the window
  - paper: doi:10.1007/s11263-005-3848-x
    title: Krystian Mikolajczyk, Tinne Tuytelaars, Cordelia Schmid, Andrew Zisserman, Jiri Matas, Frederik Schaffalitzky, Timor Kadir and Luc Van Gool, A comparison of affine region detectors, International Journal of Computer Vision 65(1-2), 43-72, 2005
    locator: the sections on the Harris-affine and Hessian-affine detectors and on the evaluation
---

The Harris-affine detector solves [feature detection](/feature-detection/) when the views differ by a change of viewpoint, not only by a change of scale. It starts from points with a scale, usually from the [Harris-Laplace detector](/harris-laplace-detector/), and adapts the shape of the window around each point. In a loop, it warps the image near the point by a $2 \times 2$ matrix $U$, measures the second moment matrix $M$ of the warped patch, and multiplies $U$ by $M^{-1/2}$, until $M$ is close to a multiple of the identity. Each step also chooses the integration scale, the differentiation scale and the position again. The result is an ellipse that covers the same part of a surface in two views that differ by an affine map, so the region is affine covariant. The Hessian-affine detector is the same loop with the position chosen by the [determinant of the Hessian](/determinant-of-hessian-detector/) instead of the [Harris](/harris-corner-detector/) measure; it finds blobs instead of corners. With $K$ iterations, kernels of radius $r$ in the warped patch and $P$ start points, the cost is $O(PKr^3)$.

## In plain words

A round window around a point covers a circle in one photograph. In a second photograph taken from the side, the same part of the scene is squeezed, so a circle there covers a different part. The detector fixes this by letting the window become an ellipse. It looks at the patch inside the window and asks in which direction the brightness changes more. It then stretches the window in the direction where the change is weaker, and asks again. When the brightness inside the window changes about equally in all directions, the window is right. The same scene part, seen from two directions, gives two ellipses that each look round after this stretching, and so they can be compared.

## The problem

The input is a gray [digital image](/digital-image/) $I$ with $W$ columns and $H$ rows of real values, and a list of points $(\mathbf x, \sigma_I)$ with a position and an integration scale. A pixel has coordinates $(u, v)$: $u$ is the column and goes right, $v$ is the row and goes down. The image is read at real positions with bilinear interpolation.

A window shape is a symmetric positive definite $2 \times 2$ matrix $U$ with largest eigenvalue $1$. The normalized patch is $W(\mathbf p) = I(\mathbf x + U\mathbf p)$, sampled at integer $\mathbf p$. For a patch, $\mu_W(\mathbf p; \sigma_I, \sigma_D) = \sigma_D^2\, g(\sigma_I) \ast \big(\nabla L\, \nabla L^{\mathsf T}\big)(\mathbf p)$ is the second moment matrix, where $L$ is $W$ smoothed with a Gaussian of standard deviation $\sigma_D$ and $g(\sigma_I) \ast$ is a Gaussian sum with standard deviation $\sigma_I$. The isotropy of a matrix is $\lambda_{\min} / \lambda_{\max}$, which is $1$ for a multiple of the identity.

The output is a list of regions $(\mathbf x, \sigma_I, U)$. Each region is the ellipse of the points $\mathbf x + \sigma_I U \mathbf p$ with $\lvert \mathbf p \rvert \le 1$, and at the end the second moment matrix of its patch is close to isotropic. Points where the loop does not converge, or where the shape becomes too long, are dropped.

The parameters are the convergence bound $\varepsilon_C$, the bound $\varepsilon_l$ on the axis ratio of $U$, the number of iterations $K$ and the Harris constant $\alpha$. Mikolajczyk and Schmid use $\varepsilon_C = 0.05$ and drop a point when the eigenvalue ratio of $U$ is above 6. They search the integration scale over $t\sigma_I$ with $t$ from $0.7$ to $1.4$ in steps of the factor $1.1$, and the ratio $s = \sigma_D / \sigma_I$ in $[0.5, 0.75]$. This page uses these values, with $s$ in steps of $0.05$, $K = 10$ and $\alpha = 0.06$.

## The algorithm

```pseudo id=main
HARRIS-AFFINE(I, points, ε_C, ε_l, K)
L1  regions ← ∅
L2  for each (x, σ_I) in points do
L3      U ← the identity matrix
L4      repeat at most K times
L5          W(p) ← I(x + U p) for the integer p in a square around 0       ▷ bilinear
L6          σ_I ← t σ_I for the t in {0.7, 0.77, …, 1.36} with the largest (t σ_I)² |ΔW| at p = 0
L7          σ_D ← s σ_I for the s in {0.5, 0.55, …, 0.75} with the largest isotropy of μ_W(0)
L8          p ← the pixel among 0 and its 8 neighbours with the largest Harris measure, 0 on ties;  x ← x + U p
L9          M ← μ_W(p);  if M is singular then drop the point;  P ← M^(-1/2)
L10         U ← the square root of (U P)(U P)^T, divided by its largest eigenvalue
L11         if λmax(U) / λmin(U) > ε_l then drop the point
L12         if 1 - λmin(P) / λmax(P) < ε_C then add (x, σ_I, U) to regions and go to the next point
L13 return regions
```

Line L6 chooses the integration scale as the maximum of the scale-normalized [Laplacian](/laplacian-of-gaussian/) at the center of the normalized patch, as in [automatic scale selection](/automatic-scale-selection/). Line L7 chooses the differentiation scale that makes the matrix most isotropic; this is the measure $Q = \lambda_{\min}(\mu) / \lambda_{\max}(\mu)$ of the 2004 paper. Line L8 moves the point to the best neighbour in the normalized patch and maps the step back to the image with $U$. For Hessian-affine, line L8 uses $\sigma_D^4 \det \mathcal H L$ in place of the Harris measure $\det\mu - \alpha (\operatorname{tr}\mu)^2$.

Line L10 is the shape step. If the patch has matrix $M$, the patch $W'(\mathbf p) = W(P\mathbf p)$ with $P = M^{-1/2}$ has the matrix $P M P = \mathrm{Id}$, to first order. So the new window is $UP$. The product of two symmetric matrices is not symmetric in general, and $UP = S Q$ with $S = \sqrt{(UP)(UP)^{\mathsf T}}$ symmetric and $Q$ a rotation. A rotation of the patch does not change its isotropy, so line L10 keeps $S$. The division by the largest eigenvalue keeps the long axis of the ellipse at $\sigma_I$; the scale is set by line L6.

## Example

Take a $41 \times 41$ image of an elongated Gaussian blob centered at $(20, 20)$, $I(\mathbf x) = \exp\!\big(-\frac12 (\mathbf x - \mathbf c)^{\mathsf T} \Sigma^{-1} (\mathbf x - \mathbf c)\big)$, with standard deviations $3$ and $1.5$ along axes turned by $30°$ from the $u$ axis. Start at $(20, 20)$ with $\sigma_I = 2$, and use Hessian-affine, since the pattern is a blob.

| | iteration 1 | iteration 2 |
|---|---|---|
| $U$ before the step | identity | $(0.874, 0.210; 0.210, 0.648)$ |
| $\sigma_I$ from line L6 | 2.050 | 2.796 |
| $s$ from line L7 | 0.75 | 0.75 |
| isotropy of $M$ | 0.2725 | 0.9498 |
| isotropy of $P = M^{-1/2}$ | 0.522 | 0.9746 |
| $U$ after the step | $(0.874, 0.210; 0.210, 0.648)$ | $(0.878, 0.211; 0.211, 0.635)$ |

In iteration 1 the round window sees a long blob. $M$ has eigenvalues $0.0070$ and $0.0257$, so the brightness changes almost four times faster across the blob than along it, and $U$ becomes an ellipse with eigenvalues $1$ and $0.522$. In iteration 2 the warped patch is nearly round, the isotropy of $P$ is $0.9746$, and $1 - 0.9746 = 0.025 < 0.05$, so the loop stops. The region has axes $\sigma_I \cdot 1 = 2.80$ and $\sigma_I \cdot 0.5135 = 1.44$, turned by $30.0°$. The blob has the axis ratio $0.5$ and the angle $30°$, so the shape is found within 3 percent. The position stays at $(20, 20)$. A round blob gives $U = \mathrm{Id}$ after one iteration, and a straight edge or a flat patch gives a singular $M$ and is dropped.

## Correctness

The proof in [proofs/correctness.md](proofs/correctness.md) shows four things. The $2 \times 2$ formulas for the square root, the inverse square root and the eigenvalues are exact. Line L10 makes the new patch isotropic to first order and keeps $U$ symmetric positive definite with largest eigenvalue $1$. The loop is covariant: if $I'(\mathbf x) = I(A^{-1}\mathbf x)$ for an invertible $A$, the second moment matrices satisfy $M_L = A^{\mathsf T} M_R A$, so a window that is isotropic for one image maps to one that is isotropic for the other, and the two regions cover the same part of the pattern. And for an elongated Gaussian blob with covariance $\Sigma$ in the continuous plane, a shape with $U U^{\mathsf T} \propto \Sigma$ makes the patch an isotropic Gaussian, so the loop stops there.

The method does not prove that the loop converges from any start. It is a fixed point iteration, and in the experiments of the 2004 paper about 40 percent of the start points do not converge and are dropped. How well the regions repeat on real images is measured; see [detector repeatability](/detector-repeatability/).

## Complexity

The model is the real RAM. Let $r$ be the radius of the largest Gaussian kernel used in the normalized patch, so the patch has $O(r^2)$ pixels.

- Line L5 samples $O(r^2)$ pixels.
- Line L6 evaluates the Laplacian at the center for 8 scales, $O(r^2)$ each.
- Line L7 smooths a square of side $O(r)$ for 6 values of $s$, each a separable blur of $O(r^3)$, and sums at the center.
- Lines L8 and L9 compute $\mu$ at 9 pixels with separable sums, $O(r^2)$.
- Lines L10 to L12 are $O(1)$.

So one iteration costs $O(r^3)$, and a point costs $O(Kr^3)$. The total time is $O(PKr^3)$; a point dropped in the first iteration costs $O(r^3)$. The extra space is the patch and its smoothed copies, $O(r^2)$. In practice the iterations for the many start points of Harris-Laplace dominate the time, and many points converge to the same region and must be merged.

## Properties

- **Affine covariance.** If two views differ by an affine map near a point, the converged ellipses correspond under that map, up to a rotation, which the shape does not fix.
- **Rotation is not fixed.** An isotropic patch can still be turned. A descriptor must choose an orientation in the normalized patch, for example the main gradient direction, as [SIFT](/sift/) does.
- **Fixed point.** At a converged region the patch is isotropic within $\varepsilon_C$. The final $\sigma_I$ need not be a maximum of the Laplacian, because the stop test looks only at the shape.
- **Corners and blobs.** Harris-affine puts regions on corners and textured parts. Hessian-affine puts them on blobs and ridges. The two give different and complementary sets of regions.
- **Brightness.** An offset changes nothing. A gain scales $M$ but not its isotropy, so the shape is the same.

## Variants and improvements

- **Hessian-affine.** Use the determinant of the Hessian for the position; the shape step is the same. The 2005 comparison of affine region detectors evaluates it next to Harris-affine.
- **Fixed scales.** Keep $\sigma_I$ and $\sigma_D$ from the start point and run only the shape and position steps. This is faster and is close to the method of Baumberg.
- **Shape only once.** Use one step of line L10 without iteration. On the example this already gives the axis ratio $0.522$ instead of $0.5135$.
- **Other start points.** Any detector with a scale can give the start points, for example the [DoG](/difference-of-gaussians-detector/) or the [determinant of the Hessian](/determinant-of-hessian-detector/).
- **Other affine regions.** [MSER](/maximally-stable-extremal-regions/) finds affine covariant regions without iteration, from the level sets of the image.

## When to use it

Use it to match images of the same scene from viewpoints that differ a lot, such as wide-baseline stereo and object recognition on flat surfaces, where scale invariant detectors lose many points. For small changes of viewpoint the scale invariant [Harris-Laplace](/harris-laplace-detector/) or DoG detectors are faster and need no iteration. For scenes with many uniform regions, MSER is a good choice and is much faster.

## Pitfalls

- **Wrong order of the factors.** The new window is $U$ times $M^{-1/2}$ when the patch is $I(\mathbf x + U\mathbf p)$. With the other convention, $I(\mathbf x + U^{-1}\mathbf p)$, the update changes; mixing the two gives a wrong shape.
- **Singular matrices.** On an edge or a flat patch $M$ is singular, and $M^{-1/2}$ does not exist. Drop the point.
- **Long shapes.** On edges the shape grows longer each iteration. The bound $\varepsilon_l$ stops this.
- **Too small a patch.** The normalized patch must hold the Gaussian sums at the largest scale tried, or the border rule distorts $M$.
- **Duplicates.** Several start points near the same corner converge to the same region. Merge regions whose ellipses overlap strongly.
- **Thin structures.** When the short axis of $\sigma_I U$ falls below about one pixel, the bilinear samples cannot show the structure, and $M$ is poor.

## Implementations

## History

Tony Lindeberg and Jonas Garding introduced affine shape adaptation in 1997, to estimate surface shape from the deformation of texture: they iterate a second moment matrix until it is the fixed point of the adaptation. Adam Baumberg used this iteration in 2000 to make windows for matching across widely separated views. Krystian Mikolajczyk and Cordelia Schmid joined it with their Harris-Laplace points, and in their 2004 journal paper they gave the full iterative algorithm, with the search for the integration scale, the differentiation scale and the position in each step. The 2005 comparison of affine region detectors by Mikolajczyk and others describes the Hessian-affine variant and compares both with MSER and other affine detectors.

## References
