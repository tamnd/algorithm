---
tag: C6ZAF6
kind: problem
slug: optical-flow
name: Optical flow
aliases:
- motion estimation from images
area: graphics-and-signals/image-processing
level: advanced
summary: Estimate the apparent motion of the brightness pattern at each pixel between two frames, from brightness constancy, which gives one equation for the two unknowns of each pixel.
model: real-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels}
  time: {worst: Θ(W H)}
prereqs: [digital-image, finite-difference-method]
see_also: [horn-schunck-method, lucas-kanade-method, image-registration, image-pyramid, phase-correlation, template-matching, image-warping, harris-corner-detector]
sources:
  - paper: doi:10.1016/0004-3702(81)90024-2
    title: Berthold K. P. Horn and Brian G. Schunck, Determining optical flow, Artificial Intelligence 17(1 to 3), 185 to 203, 1981
    locator: Section 1 (one measurement per point for two unknowns), Section 2 (optical flow is not the motion field, the rotating uniform sphere) and Section 4 (the constraint equation and the component along the gradient)
  - paper: doi:10.1007/BF01420984
    title: John L. Barron, David J. Fleet and Steven S. Beauchemin, Performance of optical flow techniques, International Journal of Computer Vision 12(1), 1994, 43 to 77
    locator: the classification into differential, matching, energy and phase based methods, and the angular error measure
  - paper: doi:10.1007/s11263-010-0390-2
    title: Simon Baker, Daniel Scharstein, J. P. Lewis, Stefan Roth, Michael J. Black and Richard Szeliski, A database and evaluation methodology for optical flow, International Journal of Computer Vision 92(1), 2011, 1 to 31
    locator: the definitions of the endpoint error and the angular error, and the benchmark with hidden ground truth
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 9, Motion estimation (the sections on optical flow)
---

Optical flow is the problem of finding, at each pixel of a frame, the apparent motion of the brightness pattern to the next frame: a field of two-dimensional vectors $(u, v)$. The usual model is *brightness constancy*, which says that a point of the pattern keeps its brightness as it moves. Linearized, this gives the constraint $E_x u + E_y v + E_t = 0$ at each pixel, one equation for two unknowns. So the data fix only the component of the motion along the brightness gradient, and every method adds an assumption to find the other: the global smoothness of the [Horn-Schunck method](/horn-schunck-method/), or the constant motion in a window of the [Lucas-Kanade method](/lucas-kanade-method/). Optical flow is the motion of the image, not of the scene, and the two can differ.

## In plain words

Take two pictures from a video, one just after the other. For each pixel of the first picture, ask where its content moved in the second picture, and draw a small arrow for that move. The set of all arrows is the optical flow. To find an arrow, a computer assumes that a moving point keeps its brightness. That one fact cannot decide a motion in two directions. In a region of the picture that shows only a straight stripe, a slide along the stripe looks the same as no slide. So each method adds a rule, such as "near pixels move in almost the same way". The arrows also show only what the picture shows: a smooth ball that turns in place can show no motion at all.

## Definition

The input is two gray frames $E^0$ and $E^1$ of the same size, $W$ columns and $H$ rows, taken at the times $t = 0$ and $t = 1$, as a [digital image](/digital-image/) each. Think of them as samples of a brightness $E(x, y, t)$ that is defined for all real $(x, y)$ and $t$. The output is a flow field $w(x, y) = (u(x, y), v(x, y))$, one vector per pixel (dense flow) or per chosen point (sparse flow), in pixels per frame.

**Brightness constancy.** A point of the pattern that is at $(x, y)$ at time $0$ is at $(x + u, y + v)$ at time $1$ with the same brightness:

$$
E^1(x + u, y + v) = E^0(x, y). \tag{1}
$$

**The constraint equation.** If the motion is small and $E$ is smooth, a first-order expansion of (1), or the chain rule applied to $dE/dt = 0$ as in Horn and Schunck, gives

$$
E_x u + E_y v + E_t = 0, \qquad \text{that is,} \qquad \nabla E \cdot (u, v) = -E_t, \tag{2}
$$

with the partial derivatives estimated by [finite differences](/finite-difference-method/) of the two frames.

**The aperture problem.** Equation (2) fixes only the component of $(u, v)$ along the gradient, the *normal flow*

$$
w_\perp = -\frac{E_t}{|\nabla E|^2} \nabla E,
$$

and says nothing about the component along the level curves of brightness. Any $(u, v)$ on the constraint line $w_\perp + s\, \nabla E^{\perp}$ satisfies (2). Where $\nabla E = 0$, the equation is empty. So the problem is ill posed at a single pixel, and a method must add a prior: smoothness of the field, constancy in a window, a parametric model of the motion, or a model of the scene.

**Flow is not scene motion.** The *motion field* is the projection of the true three-dimensional velocities of the surfaces. Optical flow is the motion of the brightness pattern, and it equals the motion field only when brightness constancy holds. Horn and Schunck note that a uniform sphere that rotates under fixed light gives zero optical flow, because the shading does not move with the surface. In the other direction, a changing picture projected onto a still screen gives a flow with no moving surface.

**Error measures.** With a ground truth $w^*$, the *endpoint error* at a pixel is $|w - w^*|$. The *angular error* is the angle between $(u, v, 1)$ and $(u^*, v^*, 1)$. Both are reported as means over the image.

## Variants

- **Dense or sparse.** A vector at every pixel, or at a set of points with texture, as in feature tracking.
- **Small or large displacement.** The linearization (2) holds for motions below about a pixel; larger motions need an [image pyramid](/image-pyramid/), warping and repeated solves, or matching of features.
- **Parametric motion.** One global translation, affine map or homography for the whole image, which is [image registration](/image-registration/). A pure translation has closed answers by [phase correlation](/phase-correlation/).
- **Robust and discontinuous flow.** Robust penalties on the data and on the smoothness term, so that the flow can jump at the boundaries of objects and outliers have a bounded effect.
- **Brightness changes.** Constancy of the gradient or of a local normalized patch instead of the brightness, for scenes with changing light.
- **Scene flow and stereo.** Three-dimensional motion from several cameras, and disparity, which is flow along known lines.
- **Learned flow.** Networks trained on synthetic and real sequences now give the most accurate dense flow on benchmarks; the library has no pages on them.

## Examples

- **A translated pattern.** If $E^1(x, y) = E^0(x - 2, y + 1)$, the true flow is $(2, -1)$ at every pixel. With a texture in two directions, a window of pixels gives two independent constraints, and the [Lucas-Kanade method](/lucas-kanade-method/) recovers $(2, -1)$; on a Gaussian blob it reaches the shift to about $10^{-15}$ in 7 iterations.
- **The aperture problem in numbers.** Let $E^0 = 3x + 4y$ and the pattern move by $(1, 2)$, so $E^1 = 3(x - 1) + 4(y - 2)$. Then $\nabla E = (3, 4)$ and $E_t = -11$ everywhere. The normal flow is $\frac{11}{25}(3, 4) = (33/25, 44/25)$, of length $11/5$, which is the component of $(1, 2)$ along the unit gradient $(3, 4)/5$. The motions $(1, 2)$, $(33/25, 44/25)$ and $(-3, 5)$ all satisfy (2), and no local method can choose among them.
- **A flat region.** Inside a region of constant brightness, (2) reads $0 = 0$. A local method returns nothing there, and a global method fills it in from the boundary.
- **Optical flow is not the motion field.** A uniform sphere that spins in place under fixed light: the motion field is not zero, but the image does not change, so the optical flow is zero.

## Known algorithms

| Algorithm | Assumption | Output | Cost |
|---|---|---|---|
| [Lucas-Kanade method](/lucas-kanade-method/) | constant flow in each window | sparse, or dense with box sums | $\Theta(k m)$ per window, $\Theta(k W H)$ dense |
| [Horn-Schunck method](/horn-schunck-method/) | global smoothness of the field | dense | $\Theta(W H)$ per iteration |
| [Phase correlation](/phase-correlation/) | one translation for the whole image | one vector | $\Theta(W H \log(W H))$ |
| [Template matching](/template-matching/) and block matching | constant integer shift in each block | one vector per block | $\Theta(W H s^2)$ for a search range of $s$ by $s$ |

Here $m$ is the window size, $k$ the iteration count and $s$ the side of the search range. Pyramidal versions of the first two handle large motions by running from coarse to fine on a [Gaussian pyramid](/gaussian-pyramid/). Variational methods with robust penalties generalize Horn-Schunck, and matching of features with interpolation handles very large motions.

## Bounds

- **Reading the input.** A dense flow must read every pixel of both frames: a pixel that is not read could change the answer near it. So $\Omega(W H)$ time is needed, and one iteration of Horn-Schunck or a dense Lucas-Kanade step meets this bound.
- **Information per pixel.** Equation (2) gives one scalar equation per pixel for two unknowns, so no method can recover the component along the level curves from the data at one pixel. The rank of the window matrix $\sum \nabla E\, \nabla E^{\mathsf T}$ says how many components a window determines: 2 with texture in two directions, 1 at a straight edge and 0 in a flat region.
- **Range of the linearization.** For a sinusoid of period $P$ pixels, a shift by $s$ and by $s + P$ give the same frames, so no method can recover a motion of more than half a period without a prior. Coarse-to-fine schemes work because the coarse levels keep only the long periods.

## Reductions

- **To least squares.** With constant flow in a window, (2) over the window is a [least-squares problem](/least-squares-problem/) in two unknowns, solved by its [normal equations](/normal-equations/).
- **To a sparse linear system.** The Horn-Schunck energy leads to a sparse system with a discrete Laplacian, solved by [Jacobi](/jacobi-method/), [Gauss-Seidel](/gauss-seidel-method/) or [multigrid](/multigrid-method/) iterations.
- **From registration.** A single global motion model turns the problem into [image registration](/image-registration/); in the other direction, a dense flow gives a warp that registers the two frames through [image warping](/image-warping/).
- **Point selection.** Sparse flow uses the same matrix as the [Harris corner detector](/harris-corner-detector/) to pick points where both components are determined.

## Applications

- Feature tracking in video, for structure from motion, visual odometry and camera stabilization.
- Motion compensation and frame interpolation for video coding and slow motion.
- Segmentation of moving objects and detection of motion for surveillance.
- Estimation of time to contact and of ego motion for robots and vehicles.
- Measurement of fluid velocity from particle images, and of tissue motion in medical images.

## References
