---
tag: XGS21H
kind: technique
slug: path-guiding
name: Path guiding
area: graphics-and-signals/ray-tracing
level: research
summary: Learn from earlier paths where the light comes from, and draw later directions from a mix of the BSDF and the learned distribution. The estimate stays unbiased.
prereqs: [path-tracing, importance-sampling]
see_also: [multiple-importance-sampling, next-event-estimation, quadtree, kd-tree, gaussian-mixture-model, photon-mapping, volumetric-path-tracing, restir]
sources:
  - paper: doi:10.1111/cgf.13227
    title: Thomas Müller, Markus Gross and Jan Novák, Practical Path Guiding for Efficient Light-Transport Simulation, Computer Graphics Forum 36(4), Eurographics Symposium on Rendering, 2017
    locator: the spatial binary tree with directional quadtrees, the training in iterations with twice the samples each time, and the mixture with BSDF sampling
  - paper: doi:10.1145/2601097.2601203
    title: Jiří Vorba, Ondřej Karlík, Martin Šik, Tobias Ritschel and Jaroslav Křivánek, On-line Learning of Parametric Mixture Models for Light Transport Simulation, ACM Transactions on Graphics 33(4), SIGGRAPH 2014
    locator: the Gaussian mixtures fitted on line with a weighted expectation maximization from photon and importance particles
  - url: https://graphics.stanford.edu/papers/veach_thesis/
    title: Eric Veach, Robust Monte Carlo Methods for Light Transport Simulation, PhD thesis, Stanford University, 1997
    locator: the chapters on importance sampling and on multiple importance sampling, which give the estimator that guiding plugs its density into
---

Path guiding is a way to make a [path tracer](/path-tracing/) learn. A plain path tracer picks each new direction from the BSDF and knows nothing about where the light is. A guided path tracer records how much light its earlier paths found in each direction at each place, builds a sampling density from these records, and draws later directions from a mix of that density and the BSDF. Because each direction is weighted by the density it was really drawn from, the estimate is still unbiased, and when the learned density is good the [variance](/variance/) falls. The idea goes back to Jensen and to Lafortune and Willems in 1995. The two methods that made it practical are the parametric mixtures of Vorba and others (2014) and the SD-tree of Müller, Gross and Novák (2017), which this page follows.

## In plain words

Think of a dark room with a small bright window. A path tracer sends rays out of each wall point in random directions, and only a few of them happen to hit the window. Most rays bring back nothing, a few bring back a lot, and the image is noisy.

Path guiding keeps a notebook. For many small parts of the room, it writes down which directions brought back light. The renderer then sends more rays in those directions and fewer in the others. To stay fair, a ray in a popular direction counts for less, and a ray in a rare direction counts for more. The average is still right, but it changes less from sample to sample.

The notebook is never perfect, so the renderer still sends some rays the old way. This protects it from a bad notebook.

## When it applies

- **The sampling density is the main problem.** The light arrives from a small part of the sphere of directions that the BSDF does not know about: a small or hidden light, light through a gap, light from a bright spot on a wall, or caustic light. When the light is spread out, cosine or BSDF sampling is already close to the best, and guiding adds cost without much gain.
- **Many samples go through the same places.** The guide learns from the paths themselves, so it needs many records in each spatial cell. It works best in long renders or in scenes that are rendered again and again.
- **The estimator can take any density.** The path tracer must evaluate the density of each direction it draws, from each strategy it might have used. A [Monte Carlo](/monte-carlo-integration/) estimator with an importance density does this; see [importance sampling](/importance-sampling/).
- **Bias is not allowed.** Guiding changes only the density, not the integrand, so it keeps unbiasedness. If a biased answer is fine, caching methods such as [irradiance caching](/irradiance-caching/) or [photon mapping](/photon-mapping/) can be cheaper.

## The template

GUIDED-RENDER trains a guide $G$ in iterations. Iteration $i$ renders $N_0 2^i$ samples per pixel with the guide of iteration $i - 1$, which stays fixed during the iteration, and records into a new guide $G'$. The holes are the data structure of the guide, the BSDF part of the mixture, and what is recorded.

```pseudo id=main
GUIDED-RENDER(scene, N0, I, α)
L1  G ← a guide with one spatial cell and the uniform density on the sphere
L2  for i ← 0 to I − 1:  G' ← REFINE(G)              ▷ hole: split busy cells and bright direction bins
L3      for each of N0 · 2^i paths, at each vertex x:  draw ω from the BSDF with probability α, else from G(x)   ▷ hole: the BSDF density and α
L4          p ← α · p_BSDF(x, ω) + (1 − α) · p_G(x, ω)
L5          β ← β · f(x, ω) cos θ / p;  continue the path      ▷ hole: Russian roulette, next event estimation
L6      for each vertex (x, ω, p) of each finished path:  add L_i(x, ω) / p to G'(x) at ω   ▷ hole: what to learn
L7      G ← G'
L8  return the image of the last iteration           ▷ hole: or a mean of the images weighted by inverse variance
```

Here $L_i(x, \omega)$ is the radiance that the path found after leaving $x$ in the direction $\omega$, divided by the throughput up to that point. Line L6 adds $L_i / p$ because the sum of these values over the samples that land in a direction bin $B$ estimates $N \int_B L_i\, d\omega$. So the recorded energy of a bin is proportional to the light from that bin, and the density of the next guide is proportional to $L_i$, cut into bins.

**Why the estimate is unbiased.** At each vertex the direction is drawn from the mixture density $p = \alpha p_{\text{BSDF}} + (1 - \alpha) p_G$, and the weight is $f \cos\theta / p$. This is [importance sampling](/importance-sampling/) with the density $p$. It is unbiased when $p > 0$ wherever $f \cos\theta\, L_i > 0$, and the BSDF part makes sure of that for each $\alpha > 0$, whatever the guide is. The guide used in an iteration depends only on the earlier iterations, so given those iterations it is a fixed density, and each image is unbiased. The tests check this for every iteration, including the first ones where the guide is still bad.

**Why it can lower the variance.** For direct light from one vertex, the estimate is $\rho / \pi \cdot \cos\theta\, L_i(\omega) / p(\omega)$. If $p$ were proportional to $\cos\theta\, L_i$, the estimate would be a constant: zero variance. A guide that learns $L_i$ alone and mixes with $\alpha = \tfrac12$ cannot reach this, but it moves samples to the directions where $L_i$ is large. The mixture also bounds the loss: $p \ge \alpha\, p_{\text{BSDF}}$, so each weight is at most $1 / \alpha$ times the weight of BSDF sampling.

## Classic examples

**A small light seen from the floor.** This is the example of the implementation. The scene is the inside of a sphere of radius $1$. The cap $z > 0.9$ emits $20$, and the walls have the albedo $\tfrac14$. Because a sphere sees each part of itself in proportion to its area, the direct light at every wall point is exactly $\tfrac14 \cdot 0.05 \cdot 20 = \tfrac14$. The camera at the center looks at the floor band $-1 < z < -0.8$ and at the wide band $-0.8 < z < 0.9$. The guide uses $\alpha = \tfrac12$, a quadtree split threshold of $0.01$ of the energy, and spatial cells that split above $2000$ records. Iteration $i$ takes $500 \cdot 2^i$ samples per pixel. The table shows the standard deviation of one sample (the standard error times $\sqrt N$), measured with seeded random numbers; plain cosine sampling gives about $1.09$ for both pixels.

| iteration | samples | spatial cells | floor, mean | floor, sd of one sample | wide band, sd of one sample |
|---|---|---|---|---|---|
| 0 | 500 | 1 | 0.270 | 1.44 | 1.76 |
| 2 | 2000 | 1 | 0.234 | 0.88 | 1.47 |
| 4 | 8000 | 3 | 0.227 | 0.73 | 1.17 |
| 5 | 16000 | 9 | 0.237 | 0.64 | 1.13 |
| 6 | 32000 | 23 | 0.248 | 0.56 | 1.03 |

Iteration 0 is worse than cosine sampling, because half of its samples are uniform on the sphere and half of those go into the floor. At the end, the floor pixel has about a quarter of the variance of cosine sampling. From one floor point, the trained guide sends more than four times as many samples to the cap as cosine sampling does; the tests check this. The wide band covers most of the sphere, its records are spread over many cells, and its gain is small.

**Two bounces.** With the albedo $\tfrac34$ below $z = 0$, $\tfrac12$ above it, and paths cut after two reflections, the exact values are $1.2$ on the floor and $0.988$ on the wide band. Cosine sampling gives $3.74$ and $3.18$ per sample; the same training with $4000$ records per cell reaches $2.85$ and $2.89$ in iteration 6. These numbers are measurements on one seed, not bounds.

**[Practical path guiding](https://doi.org/10.1111/cgf.13227) (Müller, Gross and Novák, 2017).** The guide is an SD-tree: a binary tree over space that splits its cells along the three axes in turn, and in each leaf a [quadtree](/quadtree/) over the cylindrical map of the sphere of directions, $u = (\cos\theta + 1) / 2$, $v = \phi / 2\pi$. This map has the constant Jacobian $d\omega = 4\pi\, du\, dv$, so the quadtree density divided by $4\pi$ is a solid angle density. A quadtree node splits for the next iteration when it holds more than a fixed fraction of the energy, and a spatial leaf splits when it got many records. The implementation here is the same, with the sphere surface as the space.

**[Gaussian mixtures](/gaussian-mixture-model/) (Vorba and others, 2014).** Each cache point keeps a mixture of a few Gaussians over a two-dimensional map of the directions. A pass of photons and importance particles fits the mixtures on line with a weighted form of [expectation maximization](/expectation-maximization/), and the path tracer samples from the mixture of the nearest cache point.

**[Photon map](/photon-mapping/) guiding (Jensen, 1995).** A first pass traces photons. At a point, the photons nearby give a histogram of incoming directions, and the path tracer draws from it. This is the earliest guiding with a learned density from a light pass.

**Spatial and directional trees (Lafortune and Willems, 1995).** A 5D tree over position and direction, close to a [k-d tree](/kd-tree/), caches the radiance, and the path tracer samples the cells in proportion to the cached values.

**Guiding in volumes.** In [volumetric path tracing](/volumetric-path-tracing/), the guide can also choose the distance to the next scattering point, and the phase function takes the place of the BSDF in the mixture.

## Variations

- **What is learned.** $L_i$ alone (Müller 2017), or the product of $L_i$ with the BSDF and the cosine. The product is closer to the integrand and to zero variance, but it must be built for each BSDF and each normal.
- **The data structure.** Histograms, quadtrees, Gaussian or von Mises Fisher mixtures, or neural networks that map a position to a density (neural importance sampling).
- **The mixture weight.** A fixed $\alpha$ such as $\tfrac12$, or an $\alpha$ learned per cell by minimizing the measured variance.
- **Combining the iterations.** The images of the training iterations are all unbiased, so they can be averaged with weights by their inverse variance instead of thrown away.
- **Learning as reinforcement learning.** Dahm and Keller linked the update of the guide to [Q-learning](/q-learning/): the value of a direction is the light it brings, estimated from the values stored at the next vertex.
- **Guiding other choices.** The same records can choose which light to sample in [next event estimation](/next-event-estimation/), when to stop with Russian roulette, or how often to split a path.

## Pitfalls

- **Too few records per cell.** A guide learned from a few hundred records is noisy. Bins that are bright but got no record have $p_G = 0$, and the mixture weight there is $1 / \alpha$ times the BSDF weight. In the scratch runs for this page, a spatial cell that split at $200$ records gave a worse variance than cosine sampling; at $2000$ it gave the gains of the table. The spatial and the directional resolution must grow with the data, which is why the iterations double the samples.
- **No BSDF part.** With $\alpha = 0$, a guide with a hole in a bright region gives bias, because $p = 0$ where the integrand is not $0$. Keep $\alpha > 0$, or prove that the guide has full support.
- **A density that does not match the sampler.** The density in line L4 must be exactly the density of line L3, including the Jacobian of the direction map. A quadtree on the cylindrical map has the constant Jacobian $4\pi$; on other maps the factor changes with the direction.
- **Recording with the wrong weight.** Record $L_i / p$ with the density of the mixture, not $L_i$ alone. Without the division, the guide learns $L_i\, p$, which follows its own old density and does not correct itself.
- **Roulette on the albedo.** With guiding, the throughput after a step can be more than the albedo. A survival probability from the albedo alone then kills paths of high weight; base it on the throughput, as the implementation does.
- **Expecting a gain everywhere.** Where the light is spread out, cosine sampling is already good, and the guide only adds cost. The gain of guiding is measured, scene by scene; it is not guaranteed.

## Exercises

1. Show that for direct light from one Lambertian vertex, a density proportional to $\cos\theta\, L_i(\omega)$ gives an estimate with zero variance, and that a density proportional to $L_i$ alone does not.
2. Prove that the map $u = (\cos\theta + 1) / 2$, $v = \phi / 2\pi$ has the Jacobian $d\omega = 4\pi\, du\, dv$. This is Archimedes' hat box theorem.
3. With the mixture $p = \alpha p_{\text{BSDF}} + (1 - \alpha) p_G$, show that the second moment of the estimate is at most $1 / \alpha$ times the second moment of BSDF sampling.
4. A quadtree has the energies $E_n$ at its nodes. Show that the density $p(u, v) = \prod 4 E_c / E_n$ along the path from the root to the leaf integrates to $1$ over the unit square, and that the sampler that picks a child with the probability $E_c / E_n$ has this density.
5. Show that a guide updated after each path, from the earlier paths only, still gives an unbiased image. Then show that weighting a path with a density that was updated with that same path gives bias, with a one-dimensional example.

## References
