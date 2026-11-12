---
tag: R3PDJC
kind: algorithm
slug: light-tracing
name: Light tracing
aliases:
- particle tracing
area: graphics-and-signals/ray-tracing
level: advanced
summary: Trace random paths from the lights, connect each vertex to the camera by a shadow ray, and add its contribution to the pixel it falls in. The adjoint of path tracing, also unbiased.
solves: [global-illumination]
model: real-ram
complexity:
  vars: {N: the number of light paths, P: the number of pixels, k: the mean number of vertices of a path, c: the cost of one ray query}
  time: {expected: Θ(N k c + P)}
  space: {extra: Θ(P)}
properties: {deterministic: false, recursive: false, online: true, in_place: false}
history:
  year: 1993
  people: [Philip Dutré, Eric Lafortune, Yves Willems]
  note: Dutré, Lafortune and Willems described Monte Carlo light tracing with a direct computation of the pixel values at Compugraphics 93. Particle tracing from the lights for images was described earlier, among others by Arvo and Kirk in 1990.
prereqs: [path-tracing, path-integral-formulation]
see_also: [bidirectional-path-tracing, photon-mapping, next-event-estimation, russian-roulette, instant-radiosity, pinhole-camera-model, helmholtz-reciprocity]
sources:
  - paper: "Philip Dutré, Eric P. Lafortune and Yves D. Willems, Monte Carlo light tracing with direct computation of pixel intensities, Proceedings of Compugraphics 93, Alvor, Portugal, 1993, 128 to 137"
    locator: tracing particles from the lights and connecting each hit point to the eye
  - paper: doi:10.1145/97879.97886
    title: James Arvo and David Kirk, Particle transport and image synthesis, Computer Graphics (SIGGRAPH 90) 24(4), 1990, 63 to 66
    locator: particle transport from the lights, with Russian roulette and splitting
  - url: https://graphics.stanford.edu/papers/veach_thesis/
    title: Eric Veach, Robust Monte Carlo Methods for Light Transport Simulation, PhD thesis, Stanford University, 1997
    locator: Chapter 4 (importance and the adjoint equation), Chapter 8 (the path integral form) and Chapter 10 (light tracing as the strategy with one camera vertex)
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Section 16.1 The Path-Space Measurement Equation (sampling cameras and the importance function), Section 16.3 Bidirectional Path Tracing
  - book: isbn:9781568813073
    title: Philip Dutré, Kavita Bala and Philippe Bekaert, Advanced Global Illumination, second edition, A K Peters, 2006
    locator: Chapter 5, Stochastic Path-Tracing Algorithms (light tracing)
---

Light tracing computes an image by following random paths in the direction that light travels: from a point on a light source, through bounces on the surfaces, until [Russian roulette](/russian-roulette/) ends the path. Each vertex of the path is connected to the camera by a shadow ray, and its contribution is added to the pixel that the connection passes through. It is the adjoint of [path tracing](/path-tracing/): the same [path integral](/path-integral-formulation/) sampled from the other end, and also unbiased. One light path adds to many pixels at once, and it finds light that leaves small or hidden lights, but it cannot see an emitter or a surface through a mirror, and the noise falls unevenly over the image.

## In plain words

A lamp sends out little packets of light in all directions. Each packet hits a wall, gets weaker by the color of the wall, and goes on in a new random direction, until it is used up.

Light tracing follows such packets. At each wall it hits, it asks: can the camera see this point? If a straight line from the point to the camera is clear, the point would look a little brighter to the camera because of this packet, so the method adds that amount to the pixel where the point shows up. One packet adds light to many pixels on its way. Pixels that show places where many packets land get a good value fast. Pixels that show places where packets rarely land stay noisy.

## The problem

The scene and the [rendering equation](/rendering-equation/) are as for [path tracing](/path-tracing/). Pixel $j$ of a [pinhole camera](/pinhole-camera-model/) at $c$ has the value $I_j = \int W_j(\omega)\, L(h(c, \omega), -\omega)\, d\omega$, where $W_j$ is the importance of the pixel. In the path integral form, each light path $\bar x = x_0 x_1 \cdots x_m$ from a light vertex $x_0$ to a last surface vertex $x_m$ that the camera sees contributes

$$L_e(x_0 \to x_1)\, G(x_0, x_1) \prod_{i=1}^{m-1} f(x_{i-1} \to x_i \to x_{i+1})\, G(x_i, x_{i+1}) \cdot f(x_{m-1} \to x_m \to c)\, W_j(x_m \to c)\, \frac{\cos\theta_{x_m}}{|x_m - c|^2},$$

integrated over the area of each vertex, with $G(x, y) = V(x, y) \cos\theta_x \cos\theta_y / |x - y|^2$. For a pinhole, the camera end has no cosine of its own. The output is an estimate of every $I_j$ with $E[\hat I_j] = I_j$.

## The algorithm

```pseudo id=main
LIGHT-TRACE(N)
L1  for i ← 1 to N
L2      sample y on the lights with the area density pA(y);  β ← 1 / pA(y)
L3      CONNECT(y): if VISIBLE(y, c), add β · Le(y → c) · W(y → c) · cos θy / |y − c|² to the pixel of y
L4      sample ω at y with the density p(ω);  β ← β · Le(y, ω) · cos θ / p(ω)
L5      loop: x ← CLOSEST-HIT(y, ω);  if there is no hit then go to the next path
L6          CONNECT(x): if VISIBLE(x, c), add β · f(−ω, x → c) · W(x → c) · cos θx / |x − c|² to the pixel of x
L7          sample ω′ at x with the density p(ω′);  β ← β · f(−ω, x, ω′) · cos θ′ / p(ω′)
L8          Russian roulette with the survival q: stop if u ≥ q, else β ← β / q
L9          y ← x;  ω ← ω′
L10 for each pixel j: Ij ← (sum of the values added to pixel j) / N
```

The pixel of a point $x$ is the pixel that the camera ray toward $x$ falls in; for a pinhole camera it is found by projecting $x$. $W(x \to c)$ is the importance of that pixel. A pixel that no connection reaches gets $0$ from this path, and the division by $N$ at line L10 counts every path, also those that added nothing to the pixel.

With a Lambertian emitter of radiance $E$, light sampling by power ($p_A = E / \Phi$ with $\Phi = \sum E_i A_i$) and cosine sampling, the weight is $\beta = \Phi$ at line L3, and $\pi \Phi$ after line L4. With $f = \rho / \pi$ at a vertex, the contribution of line L6 at the vertex $x_m$ is $\Phi\, \rho_1 \cdots \rho_m\, W \cos\theta_x / |x - c|^2$, divided by the survival probabilities $q_1 \cdots q_{m-1}$: the power of the lights times the albedos along the path.

## Example

The scene is a sphere of radius $2$ with albedo $\tfrac45$ and no emission, around an emitting sphere of radius $\tfrac35$ with radiance $1$ and albedo $\tfrac12$, both centered at the origin. The pinhole is at $c = (0, 0, -1)$. Pixel 1 holds the directions with $z \ge \tfrac45$, the cone in which the inner sphere fills the view, and pixel 0 the rest; each has $W = 1 / \Omega_j$ with $\Omega_0 = 2\pi \cdot \tfrac95$ and $\Omega_1 = 2\pi \cdot \tfrac15$, so each pixel is the mean radiance over its directions.

By symmetry the radiance is constant on each sphere. A cosine sampled ray from the outer wall hits the inner sphere with the probability $(\tfrac{r}{R})^2 = \tfrac{9}{100}$, and every ray from the inner sphere hits the outer wall. So $L_o = \tfrac45 (\tfrac{91}{100} L_o + \tfrac{9}{100} L_i)$ and $L_i = 1 + \tfrac12 L_o$, which give $L_o = \tfrac{18}{59} \approx 0.3051$ and $L_i = \tfrac{68}{59} \approx 1.1525$. The total power is $\Phi = 4\pi (\tfrac35)^2 \approx 4.5239$.

One light path (seed 3):

| vertex | point | albedo | $\beta$ before L6 | connection | added to pixel 0 |
|---|---|---|---|---|---|
| $y$ on the light | $(-0.409, 0.436, 0.053)$ | | $\Phi$ | faces away from $c$ | |
| $x_1$ on the outer wall | $(-1.966, 0.316, 0.184)$ | $0.8$ | $4.5239$ | $W \cos\theta / d^2 = 0.014871$ | $4.5239 \cdot 0.8 \cdot 0.014871 = 0.05382$ |

At $x_1$ roulette draws $u = 0.837 \ge q = 0.8$ and the path stops. Over $N$ paths (seed 1):

| $N$ | pixel 0 (outer wall) | pixel 1 (light) |
|---|---|---|
| 1000 | $0.2894 \pm 0.0090$ | $1.1753 \pm 0.1085$ |
| 10000 | $0.3032 \pm 0.0030$ | $1.1582 \pm 0.0333$ |

Both pixels converge to $\tfrac{18}{59}$ and $\tfrac{68}{59}$. The standard errors show the typical pattern: the wide pixel that shows reflected light gets many connections and a small error, while the narrow pixel that shows the light itself gets a connection only from paths that start on the side of the light that faces the camera, and its error is 11 times larger. Path tracing with 10000 paths per pixel has the errors $0.0054$ and $0.0042$ for the same two pixels: twice the error of light tracing on the wall, and 8 times less on the light.

## Correctness

Light tracing is unbiased for every pixel: the expected value of the sum of line L10 is $I_j$. The path integral writes $I_j$ as a sum over $m \ge 0$ of integrals over light paths $x_0 \cdots x_m$. Lines L2, L4 and L7 sample such a path vertex by vertex, and the area density of vertex $x_{i+1}$ given $x_i$ is $p(\omega)\, \cos\theta_{x_{i+1}} / |x_{i+1} - x_i|^2$. The weight $\beta$ is the product of the integrand factors up to $x_m$ divided by this density and by the survival probabilities, so the contribution of line L6 is the full integrand divided by the density of the path, and its mean is the $m$-th integral. The camera end is not sampled: it is a fixed point, reached by a deterministic connection, which is why the method needs the shadow ray. The full proof is in the proofs folder.

The conditions are the same as for path tracing: $p_A > 0$ on every emitter, each direction density positive where the BSDF is, and $q > 0$ where more light can follow.

## Complexity

Each vertex costs one closest-hit query (line L5) and one shadow ray to the camera (line L6), so $N$ paths cost $\Theta(N k c)$, plus $\Theta(P)$ to clear and divide the image. Memory is $\Theta(P)$ for the image and $O(1)$ for a path.

The variance of a pixel depends on how often paths connect to it. For pixel $j$, it grows roughly with the inverse of the probability that a path lands on the part of the scene that the pixel shows. Pixels that see bright, widely lit surfaces converge fast; pixels that see small regions, or regions lit only through hard paths, converge slowly. Unlike path tracing, the work cannot be aimed at a chosen pixel.

## Properties

- **Unbiased and consistent.** With roulette and no depth limit, the expected image is exact.
- **One path, many pixels.** Each path updates the pixels of all its vertices, so the image is a sum of splats, and parallel versions need atomic additions or one image per thread.
- **Cannot see specular chains from the camera.** A point seen through an ideal mirror or glass has a BSDF with a point mass toward the camera, and the connection of line L6 has probability $0$ to go in that direction. Light tracing misses mirror images of lit surfaces, while it handles caustics on diffuse surfaces well.
- **Cannot see a pinhole by chance.** A random ray never hits a pinhole camera, so all contributions come from connections; a lens camera with a finite aperture can also be hit, which bidirectional methods use.
- **Adjoint of path tracing.** By [Helmholtz reciprocity](/helmholtz-reciprocity/) of the BRDF, both methods sample the same integrand. With refraction, the adjoint BSDF differs by the square of the ratio of the refractive indices, and light tracing must use the adjoint form.

## Variants and improvements

- **[Bidirectional path tracing](/bidirectional-path-tracing/).** Light tracing is the strategy with one camera vertex, $t = 1$. Bidirectional path tracing combines it with path tracing and with all other ways to join a light path and a camera path, with [multiple importance sampling](/multiple-importance-sampling/).
- **[Photon mapping](/photon-mapping/).** Stores the light path vertices and estimates the radiance near camera vertices by density estimation, which handles caustics seen through mirrors at the cost of bias.
- **[Instant radiosity](/instant-radiosity/).** Turns the light path vertices into point lights for a later pass from the camera.
- **Importance-driven emission.** Emit more particles toward the parts of the scene that the camera sees.
- **Splitting.** Emit several directions from each light point, or split paths that land in the view.

## When to use it

Use light tracing for scenes where light reaches diffuse surfaces through specular paths, such as caustics under a glass, since the light paths follow the specular bounces naturally; and when the light sources are hard to reach from the camera, such as a lamp inside a shade. Use it as one strategy inside [bidirectional path tracing](/bidirectional-path-tracing/) rather than alone: alone, it gives poor results for pixels that see small regions, emitters, and anything through a mirror. For most scenes path tracing with [next event estimation](/next-event-estimation/) gives lower noise per unit of work.

## Pitfalls

- **Dividing by the hits of a pixel.** The estimate of a pixel is the sum of its contributions divided by the total number of paths $N$, not by the number of paths that reached it.
- **The camera term.** For a pinhole the measurement has $W\, \cos\theta_x / |x - c|^2$ with no cosine at the camera in this form; renderers that put a $\cos^4$ factor in $W$ must be consistent between light tracing and path tracing, or the two images differ near the edges.
- **The adjoint BSDF.** With refraction or shading normals, the BSDF used on light paths is not the same as on camera paths. Using the camera form gives wrong brightness through glass.
- **The first vertex.** The emission seen directly by the camera comes from line L3. Without it, the lights are black.
- **Self-shadowing of the connection.** The shadow ray from $x$ to the camera must start just off the surface of $x$, or it hits $x$.
- **One-sided emitters and surfaces.** A point that faces away from the camera, or an emitter whose sampled direction leaves the wrong side, must add $0$.

## Implementations

## History

Tracing particles from the lights is the natural method of particle transport, and graphics used it for caustics and illumination maps in the 1980s, among others in the backward ray tracing of Arvo in 1986. Arvo and Kirk described the link between particle transport and image synthesis in 1990, with Russian roulette and splitting. Dutré, Lafortune and Willems described light tracing that connects each hit point directly to the eye at Compugraphics 93, and Lafortune and Willems used it in the same year as one end of bidirectional path tracing. Veach placed it in his path integral framework as the strategy with one camera vertex.

## References
