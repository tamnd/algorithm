---
tag: P0YEZ8
kind: algorithm
slug: irradiance-caching
name: Irradiance caching
aliases:
- irradiance cache
area: graphics-and-signals/ray-tracing
level: advanced
summary: Compute the indirect irradiance by hemisphere sampling only at sparse points, and interpolate it elsewhere with weights from an estimate of how fast it changes.
solves: [global-illumination]
model: real-ram
complexity:
  vars: {p: the number of shaded points, r: the number of records, s: the rays per record, k: the records per lookup}
  time: {records: O(r s), lookups: O(p k) expected}
  space: {total: Θ(r)}
properties: {deterministic: false, randomized: true, recursive: false, exact: false}
history:
  year: 1988
  people: [Gregory J. Ward, Francis M. Rubinstein, Robert D. Clear]
  note: Ward, Rubinstein and Clear presented the irradiance cache at SIGGRAPH 1988, as part of the Radiance lighting simulation system.
prereqs: [rendering-equation, monte-carlo-integration, stratified-sampling]
see_also: [final-gathering, photon-mapping, path-tracing, octree, uniform-grid, ambient-occlusion, lambertian-reflectance, instant-radiosity]
sources:
  - paper: doi:10.1145/378456.378490
    title: Gregory J. Ward, Francis M. Rubinstein and Robert D. Clear, A ray tracing solution for diffuse interreflection, Computer Graphics (SIGGRAPH '88 Proceedings) 22(4), 1988, 85 to 92
    locator: the split sphere estimate of the irradiance change, the weights, the cache in an octree, and the harmonic mean distance
  - book: isbn:9781568813073
    title: Philip Dutré, Kavita Bala and Philippe Bekaert, Advanced Global Illumination, second edition, AK Peters, 2006
    locator: Chapter 7, Hybrid Algorithms, the section on irradiance caching
  - book: isbn:9781568811475
    title: Henrik Wann Jensen, Realistic Image Synthesis Using Photon Mapping, AK Peters, 2001
    locator: the chapter A Practical Two-Pass Algorithm, on the irradiance cache for the final gathering of the global photon map
---

Irradiance caching makes the indirect light on diffuse surfaces cheap. The indirect *irradiance* $E(x)$, the light that arrives at a point from all the other surfaces, usually changes slowly over a surface. To compute it at one point takes hundreds of rays over the hemisphere. Irradiance caching computes it only at some points, called *records*, and stores each record with its position, its normal, its value and the *harmonic mean distance* $R_i$ of the surfaces that its rays hit. At a new point $x$ with the normal $n$ it gives each record the weight

$$w_i(x) = \frac{1}{\dfrac{|x - x_i|}{R_i} + \sqrt{1 - n \cdot n_i}},$$

the inverse of an estimate of the relative change of the irradiance between $x_i$ and $x$. If some records have $w_i(x) > 1/a$ for the user's error bound $a$, the method interpolates them with these weights. If none do, it computes a new record. Near walls and corners $R_i$ is small, so the records are dense there. On open floors they are sparse.

## In plain words

To find how much light reaches a spot from the room around it, a renderer shoots hundreds of rays in all directions from that spot. Doing this for every pixel is slow.

But this light changes slowly. Two spots close together in the middle of a floor get almost the same light. So the method computes the light at a few spots, saves the answers, and blends the saved answers for the spots in between.

How close is close enough? It depends on how near the other surfaces are. Near a wall or in a corner, the light changes fast, so the saved spots must be close together. In the middle of a big room they can be far apart. The method measures this distance with the rays it already shot, and it also checks that the surfaces face the same way.

## The problem

At a diffuse point $x$ with the normal $n$, the reflected radiance is $\frac{\rho}{\pi} E(x)$ with the irradiance

$$E(x) = \int_{H^2(n)} L_i(x, \omega) \cos\theta\, d\omega.$$

Monte Carlo estimates of $E$ with $s$ rays, for example with [stratified](/stratified-sampling/) cosine-weighted directions, cost $s$ ray casts for each point. The problem is to estimate $E$ at many points, at most pixels of the image, with far fewer than $s$ rays for each point, and with a controlled error. Usually $E$ here is only the indirect part. Direct light from small lights and caustics change too fast and are computed by other means.

## The algorithm

The records are kept in a spatial index, such as an [octree](/octree/) or a [uniform grid](/uniform-grid/), in which a record is found from every point within $a R_i$ of it.

```pseudo id=main
IRRADIANCE(x, n, a)
L1  S ← the records i near x with w_i(x) > 1/a
L2  if S is not empty then
L3      return Σ_{i∈S} w_i(x) E_i / Σ_{i∈S} w_i(x)
L4  shoot s stratified cosine-weighted rays from x; E ← π · (the mean radiance they see); d_j ← their hit distances
L5  R ← s / Σ_j (1/d_j), clamped to [R_min, R_max]
L6  store the record (x, n, E, R) in the index, valid within the distance a·R
L7  return E
```

With cosine-weighted directions, the estimate of line L4 is $\pi$ times the mean of the incoming radiance. Line L5 is the harmonic mean of the hit distances. It is dominated by the nearest surfaces, which change the irradiance the most. The weight $w_i(x) > 1/a$ needs $|x - x_i| < a R_i$, so line L1 only looks at records whose spheres of radius $aR_i$ contain $x$.

The renderer calls IRRADIANCE at each diffuse point that a camera ray or a final gathering ray hits. The records are made on demand, in the order of the pixels. A common practice is a first pass at a low resolution that fills the cache, so that later records seldom appear in the middle of an image.

Ward derived the weight from the *split sphere* model. The worst case for the change of the irradiance near $x_i$ is a point at the center of a sphere of radius $R_i$ whose one half is bright and the other half dark. A movement $\delta$ of the point changes $E$ by about $\frac{4}{\pi}\frac{\delta}{R_i} E$, and a rotation of the normal by the angle $\theta$ changes it by about $\sqrt{2 - 2\cos\theta}\, E$. The weight is the inverse of a simplified sum of the two.

## Example

The room is the box $[0, 2] \times [0, 2] \times [0, 1]$ with black walls and a square emitter $[0.75, 1.25]^2$ of radiance 1 on the ceiling. The exact irradiance on the floor comes from Lambert's formula. It is 0.230837 at the center and 0.032669 at the point $(0.05, 0.05)$ near a corner. The rays of one record with 16 by 16 strata give $R = 1.210$ at the center and $R = 0.135$ at $(0.05, 0.05)$, so a record in the corner is valid within a radius about nine times smaller.

The floor is shaded at the centers of a 40 by 40 grid of points, 1600 points in scan order, with seed 1. To measure the interpolation error alone, the first table gives each record the exact irradiance, and takes its $R$ from the 256 rays:

| $a$ | records | rms relative error | max relative error |
|---|---|---|---|
| 0.4 | 125 | 0.2613 | 1.0087 |
| 0.2 | 316 | 0.1097 | 0.4013 |
| 0.1 | 692 | 0.0519 | 0.1822 |
| 0.05 | 1316 | 0.0165 | 0.0853 |

Halving $a$ roughly halves the error and multiplies the number of records by 2.5, 2.2 and 1.9. This is less than the factor 4 of the $1/a^2$ growth of the complexity section, because the grid of 1600 points is not fine at these radii: for $a = 0.05$ there are records at 1316 of the 1600 points. The largest errors are near the edge of the bright region below the emitter, where the irradiance changes fastest. With records from 256 sampled rays instead, the record counts are the same, but the rms error is 0.308, 0.259, 0.212 and 0.207. The noise of one record, 0.208 rms for 256 rays in this scene with a small emitter, sets a floor that a smaller $a$ cannot remove. This is why irradiance caching is used for smooth indirect light, and why its records need many rays.

## Correctness

The method is an approximation, and its error has two parts.

**Interpolation error.** If $E$ is smooth near $x$, and every record in $S$ lies within $aR_i$ of $x$ with a normal close to $n$, the interpolated value is a convex combination of values $E_i$ that differ from $E(x)$ by the change of $E$ over at most that distance. Under the split sphere model, the relative change from $x_i$ to $x$ is at most a constant times $|x - x_i|/R_i + \sqrt{1 - n \cdot n_i} = 1/w_i(x)$, and the records in $S$ have $1/w_i(x) < a$. So the relative interpolation error is $O(a)$. The table above shows this rate. The model is a heuristic and not a bound for every scene. A small, bright, nearby object that no record ray hits breaks it.

**Sampling error.** Each record value has the Monte Carlo error of line L4, with the standard deviation $O(s^{-1/2})$, and less with stratification. Interpolation spreads the error of one record over a region, so it shows as smooth blotches, not as grain.

**Consistency.** If $a \to 0$, every point gets its own record, and if $s \to \infty$, each record converges to $E(x)$. So the method converges in this double limit, but for a fixed $a$ and $s$ it is biased.

## Complexity

Each record costs $s$ ray casts, so the records cost $O(rs)$ ray casts. Each lookup visits the records of one cell or of one octree path, $O(k)$ records, with $k$ small in practice, so the lookups cost $O(pk)$ expected time. The number of records $r$ depends on the scene and on $a$. For a fine set of shaded points on a surface it grows about like $1/a^2$, until each point has its own record, and the records are dense where $R$ is small. In typical scenes $r$ is a small fraction of $p$, so the method saves most of the hemisphere rays. The memory is $\Theta(r)$.

## Properties

- **Biased.** The interpolation error does not go away with more rays per record.
- **View driven.** Records are made where the camera needs them. The same cache serves the next frame of a fly-through if the scene does not move.
- **Adaptive.** The density of the records follows the geometry: dense in corners, sparse on open surfaces.
- **Diffuse only.** The irradiance does not depend on the outgoing direction only for a Lambertian surface. Glossy surfaces need radiance caching.
- **Order dependent.** The set of records depends on the order of the queries.

## Variants and improvements

- **Irradiance gradients.** Ward and Heckbert (1992) stored the translational and rotational gradients of $E$ with each record, from the same rays, and used a first order extrapolation instead of a constant. This removes much of the blotchy look.
- **Radiance caching.** Store the incoming radiance in spherical harmonics, so the cache serves glossy surfaces too.
- **Final gathering for photon maps.** Jensen's practical renderer computes the final gathering of the global photon map only at the records of an irradiance cache, as in [final gathering](/final-gathering/).
- **Clamped and neighbor-clamped radius.** Clamp $R_i$ to $[R_{\min}, R_{\max}]$, and limit it by the radii of nearby records, to avoid records that are too large in open areas or too small at the contact of two surfaces.
- **Production use.** Tabellion and Lamorlette described an irradiance cache with one bounce of indirect light for feature animation in 2004.
- **Volumes.** The same idea caches the in-scattered radiance in [participating media](/participating-media/).

## When to use it

Use irradiance caching for the indirect diffuse light in scenes where it is smooth, as in architecture and in interiors. Use it with photon mapping for the final gathering step, and for one-bounce indirect light in production rendering. Do not use it for direct light from small lights, for caustics, for glossy reflection or for scenes with much fine geometry, such as foliage, where the light changes at a small scale. Path tracing with denoising has replaced it in many production renderers.

## Pitfalls

- **Too few rays per record.** The error of one record spreads over a whole region. The example shows that the error does not fall below the noise of one record.
- **Records made late.** A record made in the middle of a rendered image changes the values near it only for the pixels after it, which gives visible seams. Fill the cache in a first pass.
- **Leaks through walls.** A record on one side of a thin wall can be valid on the other side. Test the normal and check that the record is not behind the point, as Ward did.
- **A missing nearby object.** If the record rays miss a small object, $R$ is too large and the object's effect is lost over a large region.
- **Direct light in the cache.** Small lights make the irradiance change fast, and the split sphere model does not apply. Compute direct light separately.
- **Infinite distances.** Rays that leave the scene have $1/d = 0$. If all the rays miss, $R$ is infinite. Clamp $R$ to $R_{\max}$.

## Implementations

## History

Ward, Rubinstein and Clear presented irradiance caching at SIGGRAPH 1988, in their paper on diffuse interreflection in the Radiance lighting simulation system. They derived the weights from the split sphere model, stored the records in an octree and made them on demand during the rendering. Ward and Heckbert added irradiance gradients in 1992. Jensen used an irradiance cache for the final gathering of photon maps in his book of 2001. Tabellion and Lamorlette used it for one bounce of indirect light in feature animation in 2004, and Křivánek and others extended it to radiance caching for glossy surfaces in 2005.

## References
