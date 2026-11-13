---
tag: MYHS4D
kind: algorithm
slug: anisotropic-diffusion
name: Anisotropic diffusion
aliases:
- Perona-Malik diffusion
area: graphics-and-signals/image-processing
level: advanced
summary: Iteratively diffuse intensity with a conductance that drops across strong edges.
solves: [image-smoothing]
model: real-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels, n: number of steps}
  time: {worst: Θ(n W H)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, linear: false, edge_preserving: true, conserves_mass: true, in_place: false}
history:
  year: 1990
  people: [Pietro Perona, Jitendra Malik]
  note: Perona and Malik proposed diffusion with a conductance that falls with the gradient, so that smoothing happens inside regions and not across their edges, and gave an explicit 4-neighbor scheme for it.
prereqs: [heat-equation, gaussian-filter]
see_also: [heat-equation, ftcs-method, bilateral-filter, total-variation-denoising, non-local-means, image-smoothing, level-set-method, edge-detection]
sources:
  - paper: doi:10.1109/34.56205
    title: Pietro Perona and Jitendra Malik, Scale-space and edge detection using anisotropic diffusion, IEEE Transactions on Pattern Analysis and Machine Intelligence 12(7), 1990
    locator: the diffusion equation with a conductance of the gradient, the two conductance functions and the explicit 4-neighbor scheme
  - book: isbn:9783519026068
    title: Joachim Weickert, Anisotropic Diffusion in Image Processing, Teubner, 1998
    locator: the chapters on nonlinear diffusion filtering and on its discrete theory
  - paper: "Francine Catté, Pierre-Louis Lions, Jean-Michel Morel and Tomeu Coll, Image selective smoothing and edge detection by nonlinear diffusion, SIAM Journal on Numerical Analysis 29(1), 1992"
    locator: the regularized model with a Gaussian-smoothed gradient
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Section 3.3.1, Non-linear filtering (anisotropic diffusion)
---

Anisotropic diffusion, as Perona and Malik defined it in 1990, smooths an image by letting its values flow between neighboring pixels, as heat does, but with a conductance that falls where the gradient is large. Inside a region the differences are small, the conductance is near 1, and the image is smoothed as by the [heat equation](/heat-equation/). Across an edge the difference is large, the conductance is near 0, and little flows, so the edge stays sharp. The explicit scheme updates each pixel by $\lambda$ times the sum of the conductance-weighted differences to its four neighbors. For $\lambda \le 1/4$ and a conductance between 0 and 1, each new value is a convex combination of old values, so no new extremes appear, and with a reflecting border the sum of all values is conserved. Each step costs $\Theta(WH)$.

## In plain words

Think of the picture as a metal plate, where brightness is heat. Heat flows from warm spots to cold spots and evens things out; that is a blur. Now make the plate conduct well where neighbors are similar and badly where they differ a lot. Small bumps of noise are smoothed away, because the differences are small. A strong edge between a dark and a bright region blocks the flow, so the two sides stay apart.

The process runs in small steps. Each step moves a little brightness between each pixel and its four neighbors. More steps give more smoothing. One setting says how large a difference must be to count as an edge.

## The problem

The input is a gray image $I$ with $W$ columns and $H$ rows, a step size $\lambda > 0$, a number of steps $n$, and a conductance $g$ on the nonnegative numbers with $0 \le g \le 1$. Perona and Malik proposed two conductances with an edge threshold $K > 0$:

$$g_1(s) = e^{-(s/K)^2}, \qquad g_2(s) = \frac{1}{1 + (s/K)^2}.$$

They discretize the equation $\partial_t I = \operatorname{div}(g(|\nabla I|)\, \nabla I)$. One step of the explicit scheme maps $I$ to

$$J(p) = I(p) + \lambda \sum_{q \in N_4(p)} g(|I(q) - I(p)|)\,(I(q) - I(p)),$$

where $N_4(p)$ is the set of the four neighbors of $p$ that lie in the image. The output is the image after $n$ steps. The border rule is the reflecting border: a neighbor outside the image adds no flux, as if it had the value of $p$, which is the discrete form of the condition of zero flux through the border.

## The algorithm

```pseudo id=main
ANISOTROPIC-DIFFUSION(I, n, λ, g)
L1  repeat n times
L2      for each pixel p do
L3          flux ← 0
L4          for each of the 4 neighbors q of p that lie in the image do
L5              d ← I[q] − I[p]
L6              flux ← flux + g(|d|) · d
L7          J[p] ← I[p] + λ · flux
L8      I ← J
L9  return I
```

Line L1 runs the steps; the number of steps plays the role of the scale, as the time of the heat equation. Lines L2 to L7 compute one step from the old image $I$ into a new image $J$. Line L4 visits only the neighbors inside the image, which is the reflecting border. Line L5 is the difference to the neighbor, a one-sided estimate of the gradient in its direction, and line L6 adds it, weighted by the conductance of its size. Line L7 moves $p$ by $\lambda$ times the total flux, and line L8 makes the new image current. With $g \equiv 1$ the step is the [FTCS](/ftcs-method/) step of the heat equation with the 5-point Laplacian.

## Example

Take the one-row image $I = (10, 12, 10, 50, 48, 50)$, with $\lambda = 1/4$ and the rational conductance $g_2$ with $K = 10$. On one row each pixel has at most two neighbors. The conductances needed are $g(2) = 100/104 = 25/26 = 0.962$ and $g(40) = 100/1700 = 1/17 = 0.059$. For the pixel $x = 2$ in the first step, line L6 adds $\frac{25}{26} \cdot 2 = 1.923$ from the left neighbor and $\frac{1}{17} \cdot 40 = 2.353$ from the right one, and line L7 gives $10 + \frac14 \cdot 4.276 = 11.069$, exactly $9785/884$.

| step | $x = 0$ | 1 | 2 | 3 | 4 | 5 | sum |
|---|---|---|---|---|---|---|---|
| 0 | 10 | 12 | 10 | 50 | 48 | 50 | 180 |
| 1 | 10.481 | 11.038 | 11.069 | 48.931 | 48.962 | 49.519 | 180 |
| 2 | 10.620 | 10.907 | 11.679 | 48.321 | 49.093 | 49.380 | 180 |
| 1, with $g \equiv 1$ | 10.5 | 11 | 20.5 | 39.5 | 49 | 49.5 | 180 |

The noise of size 2 is smoothed fast, because its conductance is near 1. The step of 40 loses only about 1 per step on each side, because its conductance is $1/17$, while the linear step with $g \equiv 1$ moves the two pixels at the edge by 10.5 at once. The sum stays 180 in every row, and every value stays in $[10, 50]$.

## Correctness

The method is defined by its update, so correctness here means the two properties the update must keep. If $\lambda \le 1/4$ and $0 \le g \le 1$, line L7 gives $J(p) = (1 - \lambda \sum_q g_q) I(p) + \sum_q \lambda g_q I(q)$, where all the coefficients are nonnegative and sum to 1. So $J(p)$ lies between the least and the largest of $I(p)$ and its neighbors, and $\min I \le J \le \max I$: the discrete maximum principle. The flux from $q$ to $p$ is the negative of the flux from $p$ to $q$, because $g(|d|)$ is the same for both, so the sum of all values does not change. The full proof is below.

## Complexity

- **Time.** Each step visits $WH$ pixels and at most 4 neighbors per pixel, $\Theta(WH)$, for $\Theta(nWH)$ over $n$ steps.
- **Space.** The two images $I$ and $J$, $\Theta(WH)$.
- **Steps for a scale.** For the linear case, $n$ steps of size $\lambda$ smooth like a Gaussian of variance about $2n\lambda$ per axis, so a large scale needs many steps. Semi-implicit schemes allow larger steps; see the variants.

## Properties

- **Maximum principle.** For $\lambda \le 1/4$ and $0 \le g \le 1$, every step keeps the values in $[\min I, \max I]$. The bound on $\lambda$ is needed: on a checkerboard of 0 and 1 with $\lambda = 3/10$ and $g_2$ with $K = 10$, an interior pixel of value 1 goes to $1 - \frac{3}{10} \cdot 4 \cdot \frac{100}{101} = -\frac{19}{101}$, outside $[0, 1]$, and its neighbors of value 0 go to $\frac{120}{101}$.
- **Mass conservation.** With the reflecting border, the sum of all values is the same after every step.
- **Linear case.** With $g \equiv 1$, the scheme is the explicit heat equation, a linear filter that tends to a Gaussian blur; the conductance is what makes it nonlinear and edge preserving.
- **Backward diffusion.** In the continuous model the flux $s\,g(s)$ grows with $s$ only up to $s = K$ for $g_2$ and $s = K/\sqrt{2}$ for $g_1$, and falls after it. Edges stronger than this are sharpened, which is why the method also enhances edges, but the continuous equation is then ill-posed, and the discrete result depends on the grid. The explicit scheme still keeps the maximum principle.
- **Staircasing.** Smooth ramps tend to break into flat steps, for the same reason.
- **Long run.** With a conductance that is positive everywhere, values keep flowing, and many steps flatten the image toward its mean. The method is stopped after a chosen number of steps.

## Variants and improvements

- **Regularized model.** Catté, Lions, Morel and Coll (1992) compute the conductance from the gradient of a Gaussian-smoothed image. This makes the continuous problem well-posed and the result less sensitive to noise.
- **Naming.** The conductance of Perona and Malik is a scalar, the same in every direction at a pixel. Weickert (1998) therefore calls it nonlinear isotropic diffusion, and keeps the name anisotropic for filters with a diffusion tensor, such as edge-enhancing and coherence-enhancing diffusion, which smooth along an edge but not across it.
- **Diagonal neighbors.** Using 8 neighbors with suitable weights reduces the dependence on the grid directions; the stable step size is then smaller.
- **Semi-implicit and AOS schemes.** Solving a linear system per step with the conductance of the old image, or splitting it into 1D systems along the axes (additive operator splitting, Weickert, ter Haar Romeny and Viergever 1998), allows large steps at a cost of $O(WH)$ per step with tridiagonal solves.
- **Other conductances.** Tukey's biweight and other robust weights from statistics stop diffusion more sharply at edges. A constant times $1/s$ gives the flow of [total variation](/total-variation-denoising/) denoising.

## When to use it

Use Perona-Malik diffusion for edge preserving smoothing when a scale controlled by the number of steps is wanted, for example as a preprocessing step for [segmentation](/image-segmentation/) or [edge detection](/edge-detection/), and in medical images, where the reflecting border and mass conservation keep mean intensities. Use the [bilateral filter](/bilateral-filter/) or the [guided filter](/guided-filter/) for a one-pass filter, and [non-local means](/non-local-means/) or [total variation](/total-variation-denoising/) denoising when noise removal is the main aim.

## Pitfalls

- **Step too large.** Writing $J[p] \leftarrow I[p] + \lambda \cdot \mathrm{flux}$ at line L7 with $\lambda > 1/4$ breaks the maximum principle and can make the values oscillate; the checkerboard above leaves $[0, 1]$ in one step. Keep $\lambda \le 1/4$ for 4 neighbors and $0 \le g \le 1$.
- **Updating in place.** Writing $I[p] \leftarrow I[p] + \lambda \cdot \mathrm{flux}$ in place of line L7 makes later pixels of the same step read new values; the fluxes are then not antisymmetric, and the sum is not conserved. Write into $J$ and swap at line L8.
- **Zero padding at the border.** Treating a neighbor outside the image as the value 0 at line L4 lets mass flow out and darkens the border. Skip those neighbors, which is the reflecting border.
- **The units of K.** $K$ is in the units of the gradient estimate of line L5. With $K = 10$ for an image stored in $[0, 1]$, every difference counts as small and the method is a plain heat equation. Choose $K$ from the noise level or from a quantile of the gradient sizes.
- **Noise as edges.** Strong noise has large differences and is kept as if it were an edge. Use the regularized gradient of Catté et al. or smooth before computing $g$.

## Implementations

## History

Witkin (1983) and Koenderink (1984) described the Gaussian scale space, in which the blurred images of growing $\sigma$ are the solutions of the heat equation, and observed that it moves and blurs edges. Perona and Malik first presented their remedy in 1987 and published it in IEEE TPAMI in 1990: a conductance that depends on the gradient, with the two functions $g_1$ and $g_2$ and the explicit scheme with $\lambda \le 1/4$. Catté, Lions, Morel and Coll (1992) showed that the original model is ill-posed and gave the regularized version. Weickert (1998) gave the discrete theory with its maximum principle and the tensor-valued anisotropic filters.

## References
