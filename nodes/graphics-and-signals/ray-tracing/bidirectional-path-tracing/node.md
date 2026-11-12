---
tag: RKAS24
kind: algorithm
slug: bidirectional-path-tracing
name: Bidirectional path tracing
aliases:
- BDPT
area: graphics-and-signals/ray-tracing
level: advanced
summary: Trace one path from a light and one from the camera, join every prefix of one to every prefix of the other, and weight the joined paths with multiple importance sampling.
solves: [global-illumination]
model: real-ram
complexity:
  vars: {N: the number of samples per pixel, P: the number of pixels, K: the maximum number of edges of a path, c: the cost of one ray query}
  time: {worst: Θ(N P K² (c + K))}
  space: {extra: Θ(P + K)}
properties: {deterministic: false, recursive: false, online: true, in_place: false}
history:
  year: 1993
  people: [Eric Lafortune, Yves Willems, Eric Veach, Leonidas Guibas]
  note: Lafortune and Willems described bidirectional path tracing at Compugraphics 93, and Veach and Guibas found it on their own in 1994. Veach and Guibas gave the weighting of all strategies by multiple importance sampling in 1995.
prereqs: [path-tracing, light-tracing, multiple-importance-sampling, path-integral-formulation]
see_also: [vertex-connection-and-merging, photon-mapping, metropolis-light-transport, next-event-estimation, pinhole-camera-model, russian-roulette, volumetric-path-tracing, instant-radiosity]
sources:
  - paper: "Eric P. Lafortune and Yves D. Willems, Bi-directional path tracing, Proceedings of Compugraphics 93, Alvor, Portugal, 1993, 145 to 153"
    locator: tracing a light path and an eye path and connecting their vertices
  - paper: "Eric Veach and Leonidas J. Guibas, Bidirectional estimators for light transport, Proceedings of the Fifth Eurographics Workshop on Rendering, 1994, 147 to 162"
    locator: the family of estimators built from a light subpath and an eye subpath
  - paper: doi:10.1145/218380.218498
    title: Eric Veach and Leonidas J. Guibas, Optimally combining sampling techniques for Monte Carlo rendering, SIGGRAPH 95, 1995, 419 to 428
    locator: the balance and power heuristics, applied to bidirectional path tracing
  - url: https://graphics.stanford.edu/papers/veach_thesis/
    title: Eric Veach, Robust Monte Carlo Methods for Light Transport Simulation, PhD thesis, Stanford University, 1997
    locator: Chapter 8 (the path integral form), Chapter 9 (multiple importance sampling) and Chapter 10 (bidirectional path tracing)
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Section 16.3 Bidirectional Path Tracing
  - book: isbn:9781568813073
    title: Philip Dutré, Kavita Bala and Philippe Bekaert, Advanced Global Illumination, second edition, A K Peters, 2006
    locator: Chapter 5, Stochastic Path-Tracing Algorithms (bidirectional path tracing)
---

Bidirectional path tracing computes an image by tracing, for each sample, one random path from a light and one random path from the camera, and then joining every prefix of the light path to every prefix of the camera path with a shadow ray. A full path of $k$ edges can come out of $k + 2$ such joins, one for each split between light vertices and camera vertices, and each join is a different sampling strategy for the same [path integral](/path-integral-formulation/). [Path tracing](/path-tracing/), [next event estimation](/next-event-estimation/) and [light tracing](/light-tracing/) are three of these strategies. [Multiple importance sampling](/multiple-importance-sampling/) weights the strategies so that the result stays unbiased and each kind of path is mostly counted by the strategy that samples it best.

## In plain words

Two people search for the same thing from two ends. One walks from a lamp, the other from the eye. Each takes a few random steps and drops a marker at every step.

Then the method tries every pair of markers, one from each walk. If a straight line joins the two markers with nothing in between, the two walks and the line form one full route from the lamp to the eye, and the light that travels along that route counts toward the picture.

The same route can be found in several ways: almost all from the eye, almost all from the lamp, or half from each. Some ways are good for some routes and bad for others. The method gives each way a share of the credit, more to the way that finds the route more easily, and the shares of one route always add up to one.

## The problem

The scene and the [rendering equation](/rendering-equation/) are as for [path tracing](/path-tracing/). In the [path integral form](/path-integral-formulation/), pixel $j$ of a camera at $c$ has the value

$$I_j = \sum_{k \ge 1} \int f_j(\bar x)\, dA(x_0) \cdots dA(x_{k-1}),$$

over the paths $\bar x = x_0 x_1 \cdots x_k$ with $x_0$ on a light and $x_k = c$, where

$$f_j(\bar x) = L_e(x_0 \to x_1) \Big[\prod_{i=0}^{k-1} G(x_i, x_{i+1})\Big] \Big[\prod_{i=1}^{k-1} f_r(x_{i-1} \to x_i \to x_{i+1})\Big] W_j(x_{k-1} \to c)$$

and $G(x, y) = V(x, y) \cos\theta_x \cos\theta_y / |x - y|^2$, with no cosine at a pinhole. The output is an estimate of every $I_j$ with $E[\hat I_j] = I_j$, here for the paths with at most $K$ edges.

## The algorithm

Strategy $(s, t)$ takes the first $s$ vertices $y_0 \cdots y_{s-1}$ of the light subpath and the first $t$ vertices $z_0 = c, z_1, \dots, z_{t-1}$ of the camera subpath, and joins $y_{s-1}$ to $z_{t-1}$. The full path is $\bar x = y_0 \cdots y_{s-1} z_{t-1} \cdots z_0$, with $k = s + t - 1$ edges. With $s = 0$ the camera subpath must end on a light by itself; with $t = 1$ the light vertex is joined to the camera, as in light tracing.

```pseudo id=main
BDPT(N, K)
L1  for i ← 1 to N
L2      trace the light subpath y0 … y(K−1): y0 on a light with the density pA(y0), each next vertex by sampling a direction
L3      trace the camera subpath z0 = c, z1 … zK: z1 by sampling a camera direction, each next vertex by sampling a direction
L4      for each s ≥ 0 and t ≥ 1 with 1 ≤ s + t − 1 ≤ K
L5          if s ≥ 1 and not VISIBLE(y(s−1), z(t−1)) then go to the next pair
L6          x̄ ← y0 … y(s−1) z(t−1) … z0;  compute fj(x̄) and the pixel j of x̄
L7          compute the density pr(x̄) of x̄ under each strategy r = 0 … k, with k = s + t − 1
L8          C ← w_s(x̄) · fj(x̄) / ps(x̄), with the weight w_s from the heuristic of the pr
L9          add C to pixel j
L10 for each pixel j: Ij ← (sum of the values added to pixel j) / N
```

The density $p_r(\bar x)$ of line L7 is the product of the densities of the vertices: $x_0 \cdots x_{r-1}$ as if the light subpath had made them, and $x_r \cdots x_{k-1}$ as if the camera subpath had made them. For a vertex made from its neighbor $x'$ by a direction with the solid angle density $p(\omega)$, the area density is $p(\omega) \cos\theta_x / |x - x'|^2$. The first light vertex has $p_A(x_0)$. The pinhole $c$ itself is never sampled, so the strategy $t = 0$ has the density $0$ and is left out. The balance heuristic is $w_s = p_s / \sum_r p_r$ and the power heuristic is $w_s = p_s^2 / \sum_r p_r^2$.

With Lambertian surfaces of albedo $\rho_i$, cosine sampling and light sampling by power ($p_A = E / \Phi$), two strategies have simple weights: $f_j / p_0 = (4\pi / \Omega_j)\, E\, \rho_1 \cdots \rho_{k-1}$ for the camera alone, when the camera samples the whole sphere of directions, and $f_j / p_k = \Phi\, \rho_1 \cdots \rho_{k-1}\, W_j \cos\theta_{x_{k-1}} / |x_{k-1} - c|^2$ for light tracing. The implementation computes every $f_j$ and $p_r$ from the vertices, which keeps the code short and the weights exact.

## Example

The scene is a sphere of radius $2$ with albedo $\tfrac45$ and no emission, around an emitting sphere of radius $\tfrac35$ with radiance $1$ and albedo $\tfrac12$, both centered at the origin. The pinhole is at $c = (0, 0, -1)$ and samples the whole sphere of directions. Pixel 1 holds the directions with $z \ge \tfrac45$, the cone in which the inner sphere fills the view, and pixel 0 the rest. Each pixel is the mean radiance over its directions.

A cosine sampled ray from the outer wall hits the inner sphere with the probability $\tfrac{9}{100}$. The paths of at most $K$ edges carry at most $K - 1$ reflections, so their exact value is the Neumann series of $L_o = \tfrac45 (\tfrac{91}{100} L_o + \tfrac{9}{100} L_i)$, $L_i = 1 + \tfrac12 L_o$ cut after $K - 1$ terms:

| $K$ | pixel 0 (outer wall) | pixel 1 (light) |
|---|---|---|
| 1 | $0$ | $1$ |
| 2 | $0.072$ | $1$ |
| 3 | $0.1244$ | $1.036$ |

The paths of exactly 2 edges go from the light to the wall and then to the camera, and add $\tfrac45 \cdot \tfrac{9}{100} = 0.072$ to pixel 0. Three strategies make them. With $N = 4000$ samples (seed 1):

| strategy | what it does | pixel 0 |
|---|---|---|
| $(0, 3)$ | the camera ray bounces off the wall and hits the light by chance | $0.0653 \pm 0.0037$ |
| $(1, 2)$ | the camera ray hits the wall, which is joined to a point on the light | $0.0703 \pm 0.0023$ |
| $(2, 1)$ | the light ray hits the wall, which is joined to the camera | $0.0729 \pm 0.0010$ |
| all, balance heuristic | | $0.0715 \pm 0.0009$ |
| all, power heuristic | | $0.0723 \pm 0.0010$ |

All five estimates agree with $0.072$ within two standard errors. In this scene light tracing is the best single strategy for the wall, since every light path lands on the wall and is seen by the camera, and the combined estimate is as good as the best strategy without knowing in advance which one it is. With $K = 3$ and the power heuristic, the same run gives $0.1258 \pm 0.0011$ and $1.0422 \pm 0.0351$ against $0.1244$ and $1.036$.

## Correctness

Bidirectional path tracing is unbiased for the paths of at most $K$ edges. Fix $k$. For each strategy $s$, lines L2 and L3 sample the path $\bar x$ of $k$ edges with the density $p_s(\bar x)$, the shadow ray of line L5 supplies the factor $V$ of the joining edge, and so $f_j / p_s$ alone has the mean $\int f_j$ over the paths where $p_s > 0$. The weights of line L8 are zero where $p_s = 0$ and add up to $1$ over the strategies wherever $f_j > 0$, so the weighted sum over $s$ has the mean $\sum_s \int w_s f_j = \int f_j$. A strategy may be removed, as $t = 0$ is here, as long as the remaining weights still add up to $1$ and every path with $f_j > 0$ has at least one strategy with $p_s > 0$. The full proof is in the proofs folder.

The weights do not need the balance or power form for unbiasedness: any weights that add up to $1$ work, even weights that depend on the path. The heuristics only matter for the variance, and the balance heuristic is within a fixed bound of the best weights, as shown on the [multiple importance sampling](/multiple-importance-sampling/) page.

## Complexity

One sample traces at most $K$ light vertices and $K + 1$ camera vertices, with one closest-hit query each, and makes $O(K^2)$ joins, each with one shadow ray. The densities $p_r$ of one path can be computed in $O(K)$ with the recurrence $p_{r+1} / p_r$, which uses only the two densities of vertex $x_r$, so the weights of all joins cost $O(K^3)$. With $N$ samples for each of $P$ pixels, the time is $\Theta(N P K^2 (c + K))$ in the worst case, when no path ends early. The direct method of this implementation recomputes each $p_r$ as a product, which costs $O(K^2)$ for each join and $O(K^4)$ for each sample. Memory is $\Theta(P)$ for the image and $\Theta(K)$ for the two subpaths.

In practice $c$ dominates for small $K$, and [Russian roulette](/russian-roulette/) on both subpaths makes the mean length small. No bound on the variance holds for all scenes: it depends on how well the best strategy samples each kind of path.

## Properties

- **Unbiased.** For each $K$, and without a limit when Russian roulette ends the subpaths.
- **A superset of path tracing and light tracing.** Keeping only $s = 0$ gives path tracing; $s = 1$ gives next event estimation with area sampling; $t = 1$ gives light tracing.
- **Correlated contributions.** All joins of one sample reuse the same vertices, so their errors are not independent. This is fine for the mean and makes the paths cheap.
- **Splats.** The strategies with $t = 1$ add to the pixel of the light vertex, not to the pixel of the sample, so the image is a sum of splats.
- **Specular vertices cannot be joined.** A joining edge at a vertex with an ideal mirror or glass BSDF has $f_r = 0$ almost surely. Paths of the form light, specular, diffuse, specular, camera have only joins at specular vertices and no strategy with $p_s > 0$, so they are missed. [Vertex connection and merging](/vertex-connection-and-merging/) adds [photon mapping](/photon-mapping/) for them.

## Variants and improvements

- **[Russian roulette](/russian-roulette/).** End each subpath at random instead of at $K$; the survival probabilities enter the vertex densities of line L7.
- **Efficient weights.** Store with each vertex its forward and its reverse density, and compute $\sum_r (p_r / p_s)^2$ by walking from the join toward each end in $O(K)$.
- **[Vertex connection and merging](/vertex-connection-and-merging/).** Adds a merge of nearby light and camera vertices as one more strategy and weights it with the joins by MIS.
- **[Metropolis light transport](/metropolis-light-transport/).** Uses bidirectional path tracing to make the first paths and the mutations of a Markov chain over path space.
- **Lens cameras.** A camera of positive area can be hit by a light subpath, which adds the strategy $t = 0$.
- **Participating media.** The same joins work for paths with vertices inside a medium, as in [volumetric path tracing](/volumetric-path-tracing/).

## When to use it

Use bidirectional path tracing when the light reaches the visible surfaces by indirect paths that path tracing finds only by chance: a room lit through a gap, a lamp inside a shade, caustics on diffuse surfaces, light from small emitters through several diffuse bounces. For open scenes with direct light from large or distant lights, path tracing with [next event estimation](/next-event-estimation/) and MIS reaches the same quality for less work and is simpler to run on a GPU. For paths with a specular vertex between two diffuse ones seen through glass, use [vertex connection and merging](/vertex-connection-and-merging/) or [photon mapping](/photon-mapping/).

## Pitfalls

- **The densities must match the code.** The weight of line L8 needs $p_r$ of the strategies as they are really sampled: the same light selection, the same direction densities, the same survival probabilities. A density that is wrong for one strategy biases the image even if each strategy alone is unbiased.
- **Weights that do not add up to one.** A strategy that the code leaves out, such as $t = 0$ for a pinhole or a join at a specular vertex, must also be left out of the sum of line L7.
- **Short joins.** The factor $G$ of a joining edge has $1 / |y - z|^2$, which is large in corners. The heuristics give such joins a small weight, but only if the other strategies can make the same path.
- **Counting the emission twice.** The emission seen directly comes from $(0, 2)$ and $(1, 1)$ together; with the weights, each takes its share, and adding either one at full weight adds the light twice.
- **Underflow.** Products of many densities underflow in single precision. Compute the ratios $p_r / p_s$ instead of the densities.
- **Self-intersection.** The shadow ray of a join must start and end just off the two surfaces.

## Implementations

## History

Lafortune and Willems described bidirectional path tracing at Compugraphics 93, and Veach and Guibas found it on their own and described it at the Eurographics Workshop on Rendering in 1994. Veach and Guibas gave multiple importance sampling at SIGGRAPH 95, with the balance and power heuristics, and used it to weight all the strategies of bidirectional path tracing. Veach collected the path integral form, multiple importance sampling and bidirectional path tracing in his 1997 thesis, which is still the main reference. Later work kept the joins and added more strategies, the merges of vertex connection and merging in 2012 among them.

## References
