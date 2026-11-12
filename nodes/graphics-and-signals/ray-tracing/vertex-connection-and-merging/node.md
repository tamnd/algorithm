---
tag: PT5JRY
kind: algorithm
slug: vertex-connection-and-merging
name: Vertex connection and merging
aliases:
- VCM
area: graphics-and-signals/ray-tracing
level: research
summary: Combine the connections of bidirectional path tracing with photon merging, as one more sampling technique, under multiple importance sampling.
solves: [global-illumination]
model: real-ram
complexity:
  vars: {n: the number of light and camera subpaths per iteration, K: the maximum path length, q: the mean number of light vertices within the radius of a camera vertex}
  time: {iteration: "O(n K (K + q)) expected"}
  space: {total: "Θ(n K)"}
properties: {deterministic: false, randomized: true, recursive: false, exact: false}
history:
  year: 2012
  people: [Iliyan Georgiev, Jaroslav Křivánek, Tomáš Davidovič, Philipp Slusallek]
  note: Georgiev, Křivánek, Davidovič and Slusallek presented vertex connection and merging at SIGGRAPH Asia 2012. Hachisuka, Pantaleoni and Jensen published the same combination in the same issue.
prereqs: [bidirectional-path-tracing, photon-mapping, multiple-importance-sampling]
see_also: [progressive-photon-mapping, photon-map, path-tracing, light-tracing, next-event-estimation, spatial-hashing, path-integral-formulation, metropolis-light-transport]
sources:
  - paper: doi:10.1145/2366145.2366211
    title: Iliyan Georgiev, Jaroslav Křivánek, Tomáš Davidovič and Philipp Slusallek, Light transport simulation with vertex connection and merging, ACM Transactions on Graphics 31(6), 2012, article 192
    locator: vertex merging as a path sampling technique, its pdf with the factor n π r², the combined estimator, and the progressive radius reduction
  - title: Iliyan Georgiev, Implementing vertex connection and merging, technical report, Saarland University, 2012
    locator: the recursive quantities dVCM, dVC and dVM and the weights of each technique
  - book: isbn:9781568813073
    title: Philip Dutré, Kavita Bala and Philippe Bekaert, Advanced Global Illumination, second edition, AK Peters, 2006
    locator: Chapter 7, Hybrid Algorithms, on bidirectional path tracing and photon mapping as the two parts that VCM combines
---

Vertex connection and merging (VCM) puts [bidirectional path tracing](/bidirectional-path-tracing/) and [photon mapping](/photon-mapping/) into one estimator. Bidirectional path tracing makes a full light path by *connecting* a vertex of a camera subpath to a vertex of a light subpath with a shadow ray. Photon mapping makes one by *merging*: it takes a light subpath that ends near a camera vertex and treats the two vertices as one. Georgiev and others wrote merging as a path sampling technique with its own pdf, about $\pi r^2$ times the pdf of the light vertex, for the merging radius $r$. All the techniques then sample the same path space, and [multiple importance sampling](/multiple-importance-sampling/) weights them. Each path gets most of its weight from the technique that samples it best. Connections win on diffuse paths, and merging wins on caustics seen through glass, which connections cannot sample. The weights come from three numbers per subpath vertex, so the cost of the weights is constant for each technique.

## In plain words

There are two good ways to find how light reaches the camera. One builds a path from the camera and a path from a light, and joins their ends with a straight line. The other drops many light particles on the surfaces first, then looks for particles near the point the camera sees.

Each way has scenes it handles badly. The straight joins cannot get light that passes through glass and then a mirror to reach the camera. The particles leave blur and need many of them.

This method uses both for every pixel, and for each possible path of light it trusts the way that would find that path more often. A small table of numbers carried along each path makes this choice cheap.

## The problem

Estimate the measurement $I = \int_\Omega f(\bar x)\, d\mu(\bar x)$ of the [path integral](/path-integral-formulation/) for each pixel, where $\bar x = x_0 \dots x_k$ goes from a light to the camera. The scene can have paths of every kind: diffuse, glossy, specular, and the specular-diffuse-specular paths of caustics seen through a refracting surface. The estimator should be robust, so that no kind of path dominates the noise.

## The algorithm

Write $\overrightarrow{p}_i$ for the area pdf of $x_i$ when the light subpath samples it, and $\overleftarrow{p}_i$ for the area pdf when the camera subpath samples it. The connection technique with $s$ light vertices samples $\bar x$ with the pdf $p_{\mathrm{VC}}(s) = \prod_{i < s}\overrightarrow{p}_i \prod_{i \ge s}\overleftarrow{p}_i$. Merging at $x_s$ samples the light subpath up to $x_s^\ast$ and the camera subpath down to $x_s$, and accepts the pair when $|x_s^\ast - x_s| < r$. Its pdf is about $p_{\mathrm{VM}}(s) = \pi r^2\, \overrightarrow{p}_s\, p_{\mathrm{VC}}(s)$. Each camera subpath connects to one light subpath but merges with all $n$ of them, so merging counts $n$ times. With $\eta = n \pi r^2$, the balance heuristic gives each technique its pdf, times its count, divided by

$$D(\bar x) = \sum_{s} p_{\mathrm{VC}}(s) + \eta \sum_{s} \overrightarrow{p}_s\, p_{\mathrm{VC}}(s).$$

So a connection with $s$ light vertices has the weight $p_{\mathrm{VC}}(s)/D$, and a merge at $x_s$ has the weight $\eta\, \overrightarrow{p}_s\, p_{\mathrm{VC}}(s)/D$.

```pseudo id=main
VCM-ITERATION(n, r, K)
L1  η ← n·π·r²
L2  trace n light subpaths; store each vertex with its throughput β and its dVCM, dVC, dVM
L3  put all the light vertices in a hash grid with the cell size r
L4  for each camera subpath j ← 1 to n do
L5      for each camera vertex z, with c edges from the camera, while c ≤ K do
L6          if z is on an emitter then add β·Le·w_emission
L7          connect z to a sampled point on a light, with the weight w_nee
L8          connect z to each vertex of light subpath j, with the weight w_vc
L9          merge z with each light vertex within the distance r, add β·f·β_light·w_vm / η
L10         sample the next direction and update β, dVCM, dVC, dVM
L11 return the estimates of the n camera subpaths
```

The three quantities are partial sums of the denominator, divided by the pdf of the current vertex. After a step with the solid angle pdf $p_\omega$ and the cosine $\cos\theta_o$ at the vertex that sampled it, line L10 sets

$$\mathrm{dVCM} \leftarrow \frac{1}{p_\omega}, \quad \mathrm{dVC} \leftarrow \frac{\cos\theta_o}{p_\omega}\big(\mathrm{dVC}\, p^{\mathrm{rev}}_\omega + \mathrm{dVCM} + \eta\big), \quad \mathrm{dVM} \leftarrow \frac{\cos\theta_o}{p_\omega}\Big(\mathrm{dVM}\, p^{\mathrm{rev}}_\omega + \frac{\mathrm{dVCM}}{\eta} + 1\Big),$$

where $p^{\mathrm{rev}}_\omega$ is the pdf of the reverse direction. At the next hit, at the distance $d$ with the cosine $\cos\theta_i$, $\mathrm{dVCM}$ is multiplied by $d^2/\cos\theta_i$ and the other two are divided by $\cos\theta_i$. This turns $1/p_\omega$ into $1/\overrightarrow{p}$. A connection of the light vertex $y$ to the camera vertex $z$ then has the weight

$$w_{\mathrm{vc}} = \frac{1}{1 + \overleftarrow{p}_y\big(\eta + \mathrm{dVCM}_y + \mathrm{dVC}_y\, p^{\mathrm{rev}}_{\omega, y}\big) + \overrightarrow{p}_z\big(\eta + \mathrm{dVCM}_z + \mathrm{dVC}_z\, p^{\mathrm{rev}}_{\omega, z}\big)},$$

with the pdfs of the new edge, and a merge has the weight $1/\big(1 + \mathrm{dVCM}_y/\eta + \mathrm{dVM}_y p^{\mathrm{rev}}_\omega + \mathrm{dVCM}_z/\eta + \mathrm{dVM}_z p^{\mathrm{rev}}_\omega\big)$. Emitter hits and next event estimation have similar short forms. The implementation follows the technical report, with the [spatial hash](/spatial-hashing/) of line L3 for the range query of line L9.

The camera of the implementation measures the radiance along one ray, so the light subpath cannot connect to it. Its camera subpath starts with all three quantities at 0, and the weights leave out light tracing. A pinhole camera with an image plane adds light tracing as one more connection, as in the report.

## Example

**Weights of one path.** Inside the unit sphere a chord of length $d$ meets the sphere at the angle with the cosine $d/2$ at both ends. Let a light emit with a cosine distribution from a point chosen with the area pdf $1/(4\pi)$, and let the surfaces scatter in uniform directions, with $p_\omega = 1/(2\pi)$. Then a sampled surface point has the area pdf $\frac{1}{2\pi}\cdot\frac{d/2}{d^2} = \frac{1}{4\pi d}$, and a point after the emission has the area pdf $\frac{1}{4\pi}$. Take the path $x_0 x_1 x_2 x_3$, with $x_3$ the camera at the center, $|x_0 x_1| = 1$ and $|x_1 x_2| = \frac12$, and let $\eta = 10\pi$, from $n = 1000$ and $r = 0.1$. In units of $1/(4\pi)$, $\overrightarrow{p}_0 = \overrightarrow{p}_1 = 1$, $\overrightarrow{p}_2 = 2$, $\overleftarrow{p}_0 = 1$, $\overleftarrow{p}_1 = 2$, and $\eta = 2.5$ in units of $4\pi$:

| technique | relative pdf | weight |
|---|---|---|
| emitter hit, $s = 0$ | $\overleftarrow{p}_0 \overleftarrow{p}_1 = 2$ | 2/15 |
| next event estimation, $s = 1$ | $\overrightarrow{p}_0 \overleftarrow{p}_1 = 2$ | 2/15 |
| connect $x_1$ to $x_2$, $s = 2$ | $\overrightarrow{p}_0 \overrightarrow{p}_1 = 1$ | 1/15 |
| merge at $x_1$ | $\eta\, \overrightarrow{p}_1 \cdot 2 = 5$ | 1/3 |
| merge at $x_2$ | $\eta\, \overrightarrow{p}_2 \cdot 1 = 5$ | 1/3 |

The recursion gives the same weight for the connection: the light side is $\overleftarrow{p}_1(1/\overrightarrow{p}_1 + \eta + \overleftarrow{p}_0/(\overrightarrow{p}_0\overrightarrow{p}_1)) = 2(1 + 2.5 + 1) = 9$, the camera side is $\eta\, \overrightarrow{p}_2 = 5$, and $1/(1 + 9 + 5) = 1/15$. With 1000 light paths and this radius, merging takes two thirds of the weight of this diffuse path.

**A furnace.** The inside of the unit sphere is Lambertian with the albedo $\rho = \frac12$ and emits the radiance 1. With paths of at most $K = 4$ edges, the radiance along every camera ray is $1 + \rho + \rho^2 + \rho^3 = 1.875$. Each iteration has $n = 64$ light and camera subpaths, and the table gives the mean of 1000 iterations with seeds 5000 to 5999:

| method | mean | standard error | standard deviation per iteration |
|---|---|---|---|
| connections only ($\eta = 0$) | 1.87442 | 0.00084 | 0.0265 |
| VCM, $r = 0.1$ | 1.87460 | 0.00090 | 0.0286 |
| VCM, $r = 0.4$ | 1.87504 | 0.00104 | 0.0329 |
| VCM, $r = 0.8$ | 1.87450 | 0.00086 | 0.0272 |

All four agree with 1.875 within one standard error. In this scene a merge disc on the sphere has the area $\pi r^2$ exactly, and the photon density is constant, so merging adds no visible bias even at $r = 0.8$. The furnace has only diffuse paths, where connections already do well, so merging does not reduce the noise here. Its gain is on caustic paths through specular surfaces, which the connections cannot sample at all.

## Correctness

**The weights.** For a fixed path, the balance heuristic weights of all the techniques sum to 1, because they share one denominator. The recursion computes this denominator exactly: by induction along each subpath, $\overleftarrow{p}_y(\eta + \mathrm{dVCM}_y + \mathrm{dVC}_y p^{\mathrm{rev}}_\omega)$ is the sum of the pdfs of all the techniques with fewer light vertices, divided by $p_{\mathrm{VC}}(s)$, and the camera side is the same sum for the techniques with more light vertices. The proof page gives the induction, and the tests compare the recursion with the brute force sum in exact fractions for paths of up to 7 vertices.

**The connections.** Each connection estimate is $f(\bar x) w_t(\bar x)/p_t(\bar x)$, which is unbiased for its part of the integral. Without merging, the weights of the possible techniques sum to 1 on every path, so the sum is unbiased. This is bidirectional path tracing.

**The merges.** A merge evaluates the path with $x_s^\ast$ in place of $x_s$. This is a density estimate with a disc kernel, and it has the bias of photon mapping, which goes to 0 as $r \to 0$ for a continuous integrand. The weights are also computed with two slightly different vertices, so they sum to 1 only in the limit. VCM is biased for a fixed $r$. If the radius shrinks over the iterations as in [progressive photon mapping](/progressive-photon-mapping/), with $r_i^2 = r_1^2\, i^{\alpha - 1}$ for $0 < \alpha < 1$, the average over the iterations is consistent: its bias and variance both go to 0.

## Complexity

An iteration traces $n$ light subpaths and $n$ camera subpaths with at most $K$ vertices each, and stores $O(nK)$ light vertices. Each camera vertex makes one light connection and at most $K$ vertex connections, so the connections cost $O(nK^2)$. Each camera vertex visits a constant number of grid cells and the $q$ light vertices in its disc, so the merges cost $O(nKq)$ expected time. Every weight costs $O(1)$ because of the recursion; the brute force sum would cost $O(K)$ for each technique. The memory is $\Theta(nK)$ for the light vertices and the grid.

## Properties

- **Robust.** One estimator handles diffuse, glossy and caustic paths, including specular-diffuse-specular paths.
- **Consistent with a shrinking radius.** It is biased for a fixed radius.
- **Constant cost per weight.** The three quantities per vertex replace a sum over all the techniques.
- **Two parameters.** The radius $r$ and the number $n$ of light subpaths enter the weights through $\eta = n\pi r^2$.
- **Embarrassingly parallel within an iteration.** Light subpaths, then camera subpaths, are independent.

## Variants and improvements

- **Unified path sampling.** Hachisuka, Pantaleoni and Jensen (2012) derived the same combination as an extension of path space, in the same issue of the journal.
- **Progressive VCM.** The radius shrinks with each iteration, as in progressive photon mapping, so the result converges.
- **Volumes.** Křivánek and others (2014) unified points, beams and paths in participating media with the same weighting.
- **Light tracing.** With a pinhole camera, light subpath vertices also connect to the camera, which is one more connection technique.
- **Power heuristic.** Raise each pdf to a power, usually 2, before the sum. The recursion stays the same with powered quantities.

## When to use it

Use VCM for scenes with caustics seen through glass or water, light through refracting objects, and mixed diffuse and specular materials, where bidirectional path tracing leaves noise and photon mapping leaves blur. In a scene with only diffuse and glossy surfaces, merging adds cost and some variance without much gain, and [path tracing](/path-tracing/) or bidirectional path tracing is simpler. Do not use it when an unbiased result is required at each iteration.

## Pitfalls

- **The camera term.** The first camera quantities depend on whether light tracing to the camera is a technique. If the renderer leaves light tracing out, the camera subpath must start with dVCM = 0, or the weights do not sum to 1.
- **Inconsistent pdfs.** The forward and reverse pdfs in the recursion must be the pdfs that the sampler really uses, including Russian roulette if it is part of the pdf. A mismatch gives a biased image that still looks plausible.
- **Delta surfaces.** Specular vertices cannot be connected or merged. Skip them, and keep the quantities consistent across them.
- **The number of merges.** The factor $n$ in $\eta$ is the number of light subpaths that each camera vertex merges with. Using another count gives wrong weights.
- **The merge normalization.** Each merge divides by $\eta = n\pi r^2$, the same factor that appears in the weights.
- **Too large a radius.** The merge bias grows with $r$, and a large disc also merges across edges and corners.

## Implementations

## History

Bidirectional path tracing (Lafortune and Willems 1993, Veach and Guibas 1994 and 1995) and photon mapping (Jensen 1996) had been two separate families for more than fifteen years. Photon mapping was seen as a biased density estimate, not as a path sampling technique, so multiple importance sampling could not weight it against connections. In 2012 Georgiev, Křivánek, Davidovič and Slusallek wrote merging as a sampling technique with an explicit pdf and combined the two at SIGGRAPH Asia. Hachisuka, Pantaleoni and Jensen presented the same idea as unified path sampling in the same issue. Georgiev's technical report gave the recursive weights, and the SmallVCM renderer made a reference implementation public. Production renderers such as RenderMan later added a VCM integrator.

## References
