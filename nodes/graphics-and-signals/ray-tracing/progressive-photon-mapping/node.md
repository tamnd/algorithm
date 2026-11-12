---
tag: N56HR0
kind: algorithm
slug: progressive-photon-mapping
name: Progressive photon mapping
area: graphics-and-signals/ray-tracing
level: research
summary: Photon mapping in passes. Each hit point keeps its photon statistics and shrinks its radius after each pass, so the estimate is biased but consistent and memory stays bounded.
solves: [global-illumination]
model: real-ram
complexity:
  vars: {m: the number of hit points, M: the number of photons per pass, l: the mean number of photon hits per path, P: the number of passes}
  time: {pass: "O(M l + m) expected", total: "O(P (M l + m)) expected"}
  space: {total: "Θ(m + M l)"}
properties: {deterministic: false, randomized: true, recursive: false, exact: false}
history:
  year: 2008
  people: [Toshiya Hachisuka, Shinji Ogaki, Henrik Wann Jensen]
  note: Hachisuka, Ogaki and Jensen presented progressive photon mapping at SIGGRAPH Asia 2008. It was the first photon mapping method that converges to the correct answer with bounded memory.
prereqs: [photon-mapping, photon-map]
see_also: [vertex-connection-and-merging, final-gathering, bidirectional-path-tracing, path-tracing, spatial-hashing, bias-variance-tradeoff, law-of-large-numbers, monte-carlo-integration]
sources:
  - paper: doi:10.1145/1409060.1409083
    title: Toshiya Hachisuka, Shinji Ogaki and Henrik Wann Jensen, Progressive photon mapping, ACM Transactions on Graphics 27(5), 2008, article 130
    locator: the hit point statistics, the radius reduction with the parameter alpha, and the flux correction
  - paper: doi:10.1145/1618452.1618487
    title: Toshiya Hachisuka and Henrik Wann Jensen, Stochastic progressive photon mapping, ACM Transactions on Graphics 28(5), 2009, article 141
    locator: the shared statistics for a region and new eye paths in each pass
  - paper: doi:10.1145/1966394.1966404
    title: Claude Knaus and Matthias Zwicker, Progressive photon mapping, a probabilistic approach, ACM Transactions on Graphics 30(3), 2011, article 25
    locator: the radius sequence, the bias and variance of the average, and the convergence of the mean squared error
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, third edition, Morgan Kaufmann, 2016
    locator: Section 16.2, Stochastic Progressive Photon Mapping
---

Progressive photon mapping (PPM) makes [photon mapping](/photon-mapping/) **consistent**. A first pass traces rays from the camera and stores a *hit point* at each visible diffuse surface. Then the method runs passes without end. Each pass traces a batch of photons from the lights, adds the photons that land near each hit point to that hit point's statistics, and then reduces the hit point's radius. The update keeps only a fraction $\alpha$ of the new photons and reduces the area by the same factor, so the photon density does not change. The radius goes to 0 and the photon count goes to infinity together. The estimate stays **biased** at each pass, but the bias and the variance both go to 0. Photons are not stored after their pass, so the memory is bounded by the hit points and one batch of photons.

## In plain words

Photon mapping counts light packets in a small circle around each point the camera sees. The circle blurs the result, and more packets do not remove the blur.

Progressive photon mapping does the count in rounds. In each round it shoots a new batch of packets and adds the ones that fall in the circle to a running total. After each round it makes the circle a little smaller and adjusts the total so that it still describes the same brightness. The circles get smaller round after round, so the blur goes away. The totals keep growing, so the noise goes away too. You can stop at any round and look at the picture.

## The problem

The goal is the same as for photon mapping: the reflected radiance

$$L_r(x, \omega_o) = \int_{H^2} f_r(x, \omega_i, \omega_o)\, L_i(x, \omega_i) \cos\theta_i\, d\omega_i$$

at each visible diffuse point $x$, from the [rendering equation](/rendering-equation/). Photon mapping estimates it from the photons within a radius $r$ of $x$. The expected value is the mean over a disc of radius $r$, so the error does not go to 0 with a fixed $r$. A smaller $r$ needs more photons, and photon mapping must hold them all in memory at the same time. The problem is to get an estimate that converges to $L_r(x, \omega_o)$ as the work grows, with memory that does not grow.

## The algorithm

Each hit point $h$ holds its position $x$, its normal and BRDF, a radius $R$, a photon count $N$ and a flux $\tau$. A pass emits $M$ photons. Let $M_h$ be the number of them that land within $R$ of $x$ in that pass, and $\Phi_M$ the sum of their BRDF-weighted powers.

```pseudo id=main
PROGRESSIVE-PHOTON-MAPPING(scene, R₀, M, α)
L1  trace the camera rays; for each visible diffuse hit store h with R ← R₀, N ← 0, τ ← 0
L2  for i ← 1, 2, … do                               ▷ the photon passes
L3      build a spatial index over the hit points (a hash grid with cell size max R)
L4      for each hit q of a photon path from M emitted photons do
L5          for each hit point h in the cells near q do
L6              if |q − x_h| < R_h then M_h ← M_h + 1; Φ_M(h) ← Φ_M(h) + f_r(x_h, ω_q, ω_o) ΔΦ_q
L7      for each hit point h with M_h > 0 do
L8          N′ ← N + α M_h
L9          R′² ← R² (N + α M_h) / (N + M_h)
L10         τ ← (τ + Φ_M) R′² / R²;  N ← N′;  R ← R′
L11     the radiance at h after i passes is τ / (π R² N_e), where N_e = i M is the number of emitted photons
```

The parameter $\alpha$ is in $(0, 1)$. Hachisuka, Ogaki and Jensen used $\alpha = 0.7$. Lines L8 and L9 keep the density: $(N + \alpha M_h)/R'^2 = (N + M_h)/R^2$. Line L10 scales the flux by the ratio of the areas, so that $\tau/(\pi R^2)$ stays a flux per area. Line L11 is the photon mapping estimate with all the photons of all the passes, each photon with the power $\Phi/N_e$.

Photon paths are traced as in [photon mapping](/photon-mapping/), with [Russian roulette](/russian-roulette/) at each bounce. The photons of a pass are not stored after the pass. The index of line L3 can be a [kd-tree](/kd-tree/) or a [spatial hash](/spatial-hashing/) over the hit points. The order is the reverse of photon mapping: the photon is the query and the hit points are the data.

## Example

**One update by hand.** A point light of power $\Phi = 1$ is at height $h = 1$ over an absorbing plane. One hit point is at the foot of the light, with $R_0 = 0.5$ and $\alpha = 0.7$. Each pass emits $M = 1000$ photons, so each photon has the power $0.001$ and $N_e = 1000\,i$. Take the counts 50, 40 and 45 in the first three passes.

| pass | $M_h$ | $N$ | $R^2$ | $\tau$ | $\tau / (\pi R^2 i)$ |
|---|---|---|---|---|---|
| 1 | 50 | 35 | 0.175 | 0.0350 | 0.06366 |
| 2 | 40 | 63 | 0.147 | 0.0630 | 0.06821 |
| 3 | 45 | 94.5 | 0.128625 | 0.0945 | 0.07795 |

In pass 2, $N' = 35 + 0.7 \cdot 40 = 63$ and $R'^2 = 0.175 \cdot 63/75 = 0.147$. The count $N$ is not an integer after the first pass, and this is correct. The estimate in the last column is the mean of the photon mapping estimates of the passes, each with the radius at the start of its pass: $50 \cdot 0.001/(\pi \cdot 0.25) = 0.06366$, $40 \cdot 0.001/(\pi \cdot 0.175) = 0.07276$ and $45 \cdot 0.001/(\pi \cdot 0.147) = 0.09744$, with the mean $0.07795$. The correctness section shows that this is always true.

**Convergence.** The exact irradiance at the foot is $E(0) = \Phi/(4\pi h^2) = 0.0795775$. With a fixed radius $R = 0.5$, photon mapping converges to the mean over the disc, $0.0672097$, which is 15.5 percent low. The mean of 20 runs with seeds 0 to 19, with the standard error:

| passes | PPM estimate | relative error | mean $R$ | fixed $R = 0.5$ estimate | relative error |
|---|---|---|---|---|---|
| 1 | 0.06996 ± 0.00205 | −12.1 % | 0.4183 | 0.06996 ± 0.00205 | −12.1 % |
| 4 | 0.07329 ± 0.00152 | −7.9 % | 0.3503 | 0.06772 ± 0.00098 | −14.9 % |
| 16 | 0.07501 ± 0.00071 | −5.7 % | 0.2865 | 0.06751 ± 0.00052 | −15.2 % |
| 64 | 0.07544 ± 0.00056 | −5.2 % | 0.2331 | 0.06715 ± 0.00030 | −15.6 % |
| 256 | 0.07720 ± 0.00030 | −3.0 % | 0.1888 | 0.06728 ± 0.00011 | −15.5 % |

The fixed-radius error stays at −15.5 percent. The PPM error falls as the radius falls. A deterministic model of the recursion, with each count equal to its expected value, predicts −15.5, −11.5, −8.0, −5.4 and −3.6 percent, and the measured values agree with it within about two standard errors. The radius follows $R_i^2 \approx R_0^2\, i^{\alpha - 1}/\Gamma(\alpha)$: the formula gives 0.4183, 0.3519, 0.2886, 0.2350 and 0.1910.

## Correctness

Three facts make the method work. The proofs are in the proof file.

1. **The estimate is a mean of per-pass estimates.** Lines L9 and L10 give $\tau'/R'^2 = (\tau + \Phi_M)/R^2$, so after $i$ passes

$$\frac{\tau_i}{\pi R_i^2\, i M} = \frac{1}{i} \sum_{j=1}^{i} \frac{\Phi_{M,j}}{\pi R_{j-1}^2 M}.$$

Each term is a fixed-radius photon mapping estimate with the radius $R_{j-1}$ and the photons of pass $j$ only. Given the earlier passes, its expected value is the mean of the reflected radiance over the disc of radius $R_{j-1}$.

2. **The radius goes to 0.** Each pass with $M_h > 0$ multiplies $R^2$ by $1 - (1 - \alpha)M_h/(N + M_h) < 1$. If the density of photons at $x$ is positive, the sum of these reductions diverges, so $R_i \to 0$ with probability 1. If each count is replaced by its expected value $c\,M R^2$ for a constant density $c$, the recursion becomes exactly $R_{j+1}^2 = R_j^2 (j + \alpha)/(j + 1)$, with $R_j^2 \sim R_0^2\, j^{\alpha - 1}/\Gamma(\alpha)$.

3. **The bias and the variance go to 0.** With that radius sequence and a twice differentiable irradiance, the bias of pass $j$ is $O(R_j^2) = O(j^{\alpha-1})$ and its variance is $O(1/(M R_j^2)) = O(j^{1-\alpha}/M)$. The passes are independent given the radii, so the mean of $i$ passes has

$$\text{bias} = O(i^{\alpha - 1}), \qquad \text{variance} = O(i^{-\alpha}), \qquad \text{MSE} = O(i^{2\alpha - 2}) + O(i^{-\alpha}).$$

Both go to 0 for each $\alpha \in (0, 1)$, so the estimate is consistent. Knaus and Zwicker gave this analysis in 2011. The MSE is smallest for $\alpha = 2/3$, where it is $O(i^{-2/3})$, the same rate as photon mapping with the best radius for a known photon count.

The method is still biased at each finite pass. Each pass sees a disc of positive radius, so it averages the light over that disc.

## Complexity

A pass traces $M$ photon paths with $l$ hits each on average. Each hit looks up the hit points in the cells near it. With a hash grid and cells as large as the largest radius, a lookup costs $O(1)$ expected plus the number of hit points in the 9 cells, which is $O(1)$ when the hit points are spread evenly. The update of line L7 visits each hit point. So a pass takes $O(Ml + m)$ expected time and $P$ passes take $O(P(Ml + m))$. The memory is $\Theta(m)$ for the hit points and the photons of one pass, $\Theta(Ml)$ at most, which can also be processed one photon at a time. The memory does not grow with the number of passes, which is the main gain over photon mapping.

## Properties

- **Biased but consistent.** The expected value after $i$ passes differs from the answer, but the estimate converges to it in probability as $i \to \infty$.
- **Bounded memory.** Only the hit points and the current batch of photons are in memory.
- **Fixed hit points.** The camera pass runs once, so the method handles only the points of that pass. Glossy surfaces, depth of field, motion blur and antialiasing need many camera samples per pixel, which the original method cannot give. Stochastic progressive photon mapping removes this limit.
- **Local statistics.** Each hit point has its own radius, which shrinks faster where photons are dense.
- **Robust for specular paths.** Like photon mapping, it handles the light, specular, diffuse, specular, camera paths that local path sampling cannot find.

## Variants and improvements

- **Stochastic progressive photon mapping (SPPM).** Hachisuka and Jensen, 2009. Each pass also traces new camera paths, and the statistics belong to a region of the image, such as a pixel, instead of a single point. This gives glossy reflection, depth of field and the other distributed effects.
- **Probabilistic PPM.** Knaus and Zwicker, 2011. Each pass is a plain photon map with the radius $r_i^2 = r_1^2 \prod_{j=1}^{i-1} (j + \alpha)/(j + 1)$, and the passes are averaged. No local statistics are needed, so any photon mapping renderer, including one for volumes, becomes consistent.
- **Vertex connection and merging.** Georgiev and others, 2012. Combine the shrinking-radius photon merge with the connections of [bidirectional path tracing](/bidirectional-path-tracing/) under [multiple importance sampling](/multiple-importance-sampling/), as in [vertex connection and merging](/vertex-connection-and-merging/).
- **Volumes.** The probabilistic form also makes volume photon mapping and photon beams progressive. The radius sequence then depends on the dimension of the kernel.
- **Adaptive radius.** Choose $\alpha$ or the initial radius per hit point from an estimate of the local error.

## When to use it

Use PPM or SPPM when you need photon mapping for caustics or for specular paths, as seen through glass or in a mirror, and you also need the image to converge to the right answer. It is a good choice for progressive previews that refine without end. In scenes without hard specular paths, an unbiased method such as [path tracing](/path-tracing/) or [bidirectional path tracing](/bidirectional-path-tracing/) usually converges faster. Vertex connection and merging gives the strengths of both.

## Pitfalls

- **Dividing by the wrong count.** The radiance is $\tau/(\pi R^2 N_e)$ with $N_e$ the total number of emitted photons over all passes. It is not the number of photons that hit, and not the count $N$ of the hit point.
- **Forgetting the flux correction.** Line L10 scales $\tau$ by $R'^2/R^2$. Without the scale the estimate grows without bound as the radius shrinks.
- **An integer count.** $N$ takes values such as 94.5. Rounding it changes the density and adds bias.
- **A grid that is too fine.** The grid cell must be at least the largest radius, or a 3 by 3 cell lookup misses hit points. Rebuild the grid as the radii shrink, or use the initial radius.
- **The initial radius.** A small $R_0$ gives noise for many passes. A large $R_0$ gives a large bias that takes many passes to go away. The rate is only $i^{\alpha - 1}$, so a bad start is slow to fix.
- **Expecting an unbiased image.** At each finite pass the image is blurred. Do not use one pass as a reference.

## Implementations

## History

Jensen introduced photon mapping in 1996. Its estimate is biased, and to reduce the bias it needs more photons in memory at the same time. Hachisuka, Ogaki and Jensen presented progressive photon mapping at SIGGRAPH Asia 2008. They moved the photon statistics to the hit points of a camera pass and reduced the radius after each photon pass, so the method converges with bounded memory. Hachisuka and Jensen extended it to stochastic progressive photon mapping in 2009, with new camera paths in each pass. Knaus and Zwicker gave a probabilistic analysis in 2011. They showed that PPM is equivalent to the mean of independent photon maps with a shrinking radius, and they derived the rates of the bias and the variance. In 2012 Georgiev, Křivánek, Davidovič and Slusallek, and in parallel Hachisuka, Pantaleoni and Jensen, combined the progressive merge with bidirectional path tracing.

## References
