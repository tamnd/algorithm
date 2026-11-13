---
tag: J0BY18
kind: algorithm
slug: horn-schunck-method
name: Horn-Schunck method
aliases:
- Horn-Schunck optical flow
area: graphics-and-signals/image-processing
level: advanced
summary: Dense optical flow that minimizes the brightness constancy error plus alpha squared times the flow roughness over the whole image, solved by a Jacobi-type iteration.
solves: [optical-flow]
model: real-ram
complexity:
  vars: {n: the number of flow points, k: the number of iterations}
  time: {worst: Θ(k n), average: Θ(k n), best: Θ(k n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: false, dense: true, local: false, iterative: true}
history:
  year: 1981
  people: [Berthold K. P. Horn, Brian G. Schunck]
  note: Horn and Schunck added a smoothness term to the brightness constancy constraint, so that the flow is found at every point, and solved the discrete equations by iteration.
prereqs: [optical-flow, jacobi-method, finite-difference-method]
see_also: [lucas-kanade-method, gauss-seidel-method, multigrid-method, poisson-equation, heat-equation, image-pyramid, total-variation-denoising, markov-random-field]
sources:
  - paper: doi:10.1016/0004-3702(81)90024-2
    title: Berthold K. P. Horn and Brian G. Schunck, Determining optical flow, Artificial Intelligence 17(1-3), 1981, 185 to 203
    locator: Section 7 (the derivative estimates on the 2 x 2 x 2 cube), Section 8 (the Laplacian as κ(ū − u) with weights 1/6 and 1/12), Section 9 (the energy and the discrete equations), Sections 12 to 14, pages 193 to 194 (the iteration, the boundary rule, filling in and the tightness of the constraint)
  - paper: doi:10.1109/TIP.2004.827235
    title: Amar Mitiche and Abdol-Reza Mansouri, On convergence of the Horn and Schunck optical-flow estimation method, IEEE Transactions on Image Processing 13(6), 2004, 848 to 852
    locator: the whole paper (the discrete system as a block tridiagonal system, and the convergence of its Jacobi and Gauss-Seidel iterations)
  - paper: doi:10.1007/BF01420984
    title: John L. Barron, David J. Fleet and Steven S. Beauchemin, Performance of optical flow techniques, International Journal of Computer Vision 12(1), 1994, 43 to 77
    locator: the section on differential techniques (the Horn and Schunck implementation and its measured errors on synthetic and real sequences)
  - book: isbn:9780262081597
    title: Berthold K. P. Horn, Robot Vision, MIT Press, 1986
    locator: Chapter 12, Motion Field and Optical Flow (the smoothness constraint and the iterative solution)
---

The Horn-Schunck method computes a dense [optical flow](/optical-flow/) field $(u, v)$ between two frames by minimizing one global energy: the squared error of the brightness constancy constraint $E_x u + E_y v + E_t = 0$, plus $\alpha^2$ times the squared size of the flow gradient. The smoothness term fills in the flow where the image gives no information, and it removes the aperture problem of a single pixel. On a grid the minimum solves a sparse linear system with two unknowns per pixel, and Horn and Schunck solve it with a [Jacobi](/jacobi-method/) style iteration in which each point moves from the mean flow of its neighbors toward its own constraint line. Each iteration costs $\Theta(n)$ for $n$ flow points.

## In plain words

Two frames of a video differ because things moved. At one pixel you can measure how fast the brightness changes in space and in time, and that gives one equation for a motion with two unknown parts. One equation is not enough: along an edge, any slide along the edge looks the same. Horn and Schunck add a second wish: the motion field should be smooth, so neighbors move almost alike. Then they repeat a simple update at every pixel. Take the average motion of the eight neighbors, check how badly it breaks this pixel's brightness equation, and move it straight toward the line of motions that would satisfy the equation, but only part of the way. One weight decides how much smoothness counts against the data. After enough rounds, motion from textured places spreads into flat places, and the field settles.

## The problem

The input is two gray frames $E^0$ and $E^1$ of $W \times H$ samples, taken one time unit apart, with real values (linear or gamma encoded, but the same in both frames). Sample $(x, y)$ has integer indices and its center at $(x + 1/2, y + 1/2)$; $x$ grows to the right and $y$ grows down. The output is a flow $(u, v)$ in pixels per frame at the $(W - 1) \times (H - 1)$ centers of the $2 \times 2 \times 2$ cubes of samples, so that the scene point at a cube center moves by about $(u, v)$ from frame 0 to frame 1.

With the brightness derivatives $E_x, E_y, E_t$, the continuous problem is to minimize

$$
\iint \Big( (E_x u + E_y v + E_t)^2 + \alpha^2 \big( |\nabla u|^2 + |\nabla v|^2 \big) \Big) \, dx \, dy
$$

over the flow fields. The first term is zero when brightness is conserved along the motion (the linearized brightness constancy constraint), the second penalizes roughness, and $\alpha^2 > 0$ sets the balance. The page uses Horn and Schunck's discretization: $E_x$, $E_y$ and $E_t$ are each the mean of the four first differences along their axis in the cube, and the Laplacian of $u$ is approximated by $\kappa(\bar u - u)$, where $\bar u$ is the mean of the 8 neighbors with weight $1/6$ for the 4 edge neighbors and $1/12$ for the 4 corner neighbors. The constant $\kappa = 3$ is absorbed into $\alpha^2$. At the image border a missing neighbor takes the value of the nearest point inside, the discrete form of a zero normal derivative.

## The algorithm

```pseudo id=main
HORN-SCHUNCK(E⁰, E¹, α², k)
L1  for each cube center p: E_x(p), E_y(p), E_t(p) ← the means of the 4 first differences along x, y and t
L2  u ← 0;  v ← 0                                   ▷ or the flow of the previous frame pair
L3  repeat k times
L4      ū, v̄ ← the 8-neighbor means of u and v (1/6 at edges, 1/12 at corners, border clamped)
L5      for each p: r(p) ← (E_x ū + E_y v̄ + E_t) / (α² + E_x² + E_y²)
L6                  u(p) ← ū(p) − E_x r(p);  v(p) ← v̄(p) − E_y r(p)
L7  return u, v
```

Line L5 measures how far the mean flow $(\bar u, \bar v)$ is from the constraint line $E_x u + E_y v + E_t = 0$ of the point, in units scaled by the gradient. Line L6 moves $(\bar u, \bar v)$ along the gradient direction $(E_x, E_y)$, which is perpendicular to that line. With $\alpha^2 = 0$ the step lands on the line; with $\alpha^2 > 0$ it stops short by the factor $|\nabla E|^2 / (\alpha^2 + |\nabla E|^2)$. All points use the means of the previous iterate, which is the Jacobi form. Using the new values of already visited neighbors gives the [Gauss-Seidel](/gauss-seidel-method/) form, which the paper also names.

## Example

**One point.** Let a point have $E_x = 3$, $E_y = 4$, $E_t = -5$ and neighbors whose mean flow is $\bar u = \bar v = 0$. Its constraint line is $3u + 4v = 5$. With $\alpha^2 = 0$, line L5 gives $r = -5/25 = -1/5$, and line L6 gives $(u, v) = (3/5, 4/5)$: the point of the line closest to the mean, which is the normal flow of length $|E_t| / |\nabla E| = 1$. With $\alpha^2 = 25$, $r = -5/50 = -1/10$ and $(u, v) = (3/10, 4/10)$, halfway, because smoothness and data have equal weight here.

**A synthetic constant flow.** Take $16 \times 16$ frames of the bowl $f(x, y) = 2((x - 15/2)^2 + (y - 15/2)^2)$ with frame 1 equal to $f(x - 1/2, y + 1/4)$, so the true flow is $(u, v) = (1/2, -1/4)$ everywhere, of length $0.559$. For a quadratic brightness the cube estimates of line L1 equal the true derivatives at the cube centers, so $E_x u + E_y v + E_t = 0$ holds exactly for the true flow and the constant field $(1/2, -1/4)$ is an exact fixed point of lines L4 to L6. Starting from zero with $\alpha^2 = 10$, the largest error over the $15 \times 15$ flow points is $0.0766$ after 100 iterations, $0.00741$ after 200 and $6.86 \times 10^{-5}$ after 400, and it never grows between iterations. The gradient of the bowl points in all directions, so each normal component is known locally, and the full vectors fill in from the neighbors after a number of iterations of the order of the image width.

**One direction of texture.** If the brightness is $x^2 + 10x$, which does not depend on $y$, then $E_y = 0$ at every point, line L6 never changes $v$, and $v$ stays at its start value 0 whatever the true motion along $y$. The method recovers only the component along the gradient, as Horn and Schunck state for brightness that varies in one direction.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It shows three things. First, for fixed means $(\bar u, \bar v)$ at a point, the pair of discrete equations of Horn and Schunck

$$
(\alpha^2 + E_x^2)\,u + E_x E_y\, v = \alpha^2 \bar u - E_x E_t, \qquad E_x E_y\, u + (\alpha^2 + E_y^2)\, v = \alpha^2 \bar v - E_y E_t
$$

has determinant $\alpha^2(\alpha^2 + E_x^2 + E_y^2) > 0$, and its unique solution is line L6. So a fixed point of the iteration is exactly a solution of the discrete minimization problem. Second, the error $\max_p |(u, v)(p) - (u^*, v^*)(p)|$ to any fixed point $(u^*, v^*)$ never grows from one iteration to the next: the 8-neighbor mean is an average, and the map of line L6 is, for the error, a matrix with eigenvalues 1 and $\alpha^2/(\alpha^2 + |\nabla E|^2)$ along two orthogonal directions. Third, the cube estimates are exact for brightness that is a quadratic function of $(x, y, t)$, which makes a constant translation an exact fixed point in the example above. That the iteration converges to the fixed point is proved by Mitiche and Mansouri (2004), who write the discrete equations as a block tridiagonal system and show that its Jacobi and Gauss-Seidel iterations converge.

## Complexity

- **Time per iteration.** Lines L4 to L6 do a constant amount of work per flow point: 8 neighbor reads for each of $\bar u$ and $\bar v$, one division and a few products. So one iteration is $\Theta(n)$ with $n = (W - 1)(H - 1)$, and $k$ iterations are $\Theta(kn)$ in the [real RAM](/real-ram/). Line L1 is $\Theta(n)$ once.
- **Space.** The derivatives and two copies of the flow, so $\Theta(n)$ extra.
- **Number of iterations.** The flow spreads by about one point per iteration, so filling in a region with no gradient that is $d$ points across needs more than $d$ iterations; Horn and Schunck give this rule and suggest the image width when $d$ is unknown. The Jacobi iteration for such a Laplacian-type system needs a number of iterations that grows with the square of the width for a fixed accuracy, in the worst case, which is why later work uses [multigrid](/multigrid-method/) solvers or [coarse-to-fine pyramids](/image-pyramid/).

## Properties

- **Dense.** Every point gets a flow, including points with zero gradient, where the flow is the mean of the neighbors.
- **Global.** A change of one pixel can change the flow everywhere, through the smoothness term.
- **Linear in the data term.** For fixed derivatives, the fixed point depends linearly on $E_t$, so the flow scales with the time differences.
- **Not robust.** The quadratic penalties make the method smooth the flow across motion boundaries and let outliers in the data pull the flow.
- **Small motions only.** The linearized constraint holds only when the motion is small compared with the scale of the brightness variation, about a pixel for unfiltered images.

## Variants and improvements

- **Gauss-Seidel and over-relaxation.** Updating in place, in raster order or in a red-black order, usually converges faster than the Jacobi form, and successive over-relaxation can speed it up further.
- **Multigrid and pyramids.** Solving the system on a [Gaussian pyramid](/gaussian-pyramid/), coarse to fine, handles large motions and reduces the iteration count. The warping form re-linearizes the constraint after each level.
- **Robust and total variation penalties.** Replacing the squares by robust functions or by the $L^1$ norm of the flow gradient, as in [total variation denoising](/total-variation-denoising/), keeps motion boundaries sharp.
- **Local and global combined.** Integrating the data term over a small window, as in the [Lucas-Kanade method](/lucas-kanade-method/), and keeping the global smoothness term gives a method that is less sensitive to noise than either.
- **Discrete labels.** A [Markov random field](/markov-random-field/) over a discrete set of motion labels replaces the continuous minimization.

## When to use it

Use Horn-Schunck when a dense, smooth flow is needed and the motion is small, a few pixels at most or less after a pyramid: fluid and cloud motion, small camera motion, or as the start for a more refined method. It is short to implement and easy to run on a GPU, since each point reads only its neighbors. Use the [Lucas-Kanade method](/lucas-kanade-method/) for a sparse set of well-textured points, and a robust variational method when the flow must keep sharp edges between objects.

## Pitfalls

- **The scale of $\alpha^2$.** $\alpha^2$ is compared with $E_x^2 + E_y^2$, so it depends on the brightness range: an image scaled by 255 needs $\alpha^2$ scaled by $255^2$ for the same result.
- **Too few iterations.** The flow inside a flat region is still the start value until enough iterations reach it. An answer after a few iterations can look smooth and still be far from the minimum.
- **Large motions.** A shift of several pixels breaks the linearization, and the method then finds a wrong flow with no warning. Use a pyramid with warping.
- **The grid of the flow.** The cube estimates give the flow at the cube centers $(x + 1, y + 1)$ in the corner coordinates of the samples, half a pixel away from the sample centers along each axis. Mixing it with a flow on the sample grid gives a shift of half a pixel.
- **Noise in the derivatives.** Differences of raw frames amplify noise. Presmooth both frames with the same [Gaussian filter](/gaussian-filter/) before line L1.
- **Brightness changes.** A global change of exposure breaks brightness constancy and shows up as a false flow along the gradient.

## Implementations

## History

Horn and Schunck published the method in 1981 in Artificial Intelligence. They formulated optical flow as the minimum of the brightness constancy error plus a smoothness term, discretized it on the $2 \times 2 \times 2$ cube of samples with an 8-neighbor Laplacian, and solved the resulting equations by iteration, with the remark that the number of iterations must exceed the width of the largest region to fill in. They also pointed out that brightness that varies in only one direction gives only the normal component of the flow. Barron, Fleet and Beauchemin included the method in their 1994 comparison of optical flow techniques. Mitiche and Mansouri proved in 2004 that the iteration converges.

## References
