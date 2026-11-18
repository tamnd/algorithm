---
tag: KJNY6S
kind: technique
slug: fractal-noise
name: Fractal Brownian motion noise
aliases:
- fBm noise
- turbulence function
- fractal sum of noise
area: graphics-and-signals/real-time-rendering
level: core
summary: Sum octaves of a noise function, each with doubled frequency and reduced amplitude, to get a self-similar texture for terrain, clouds and marble.
prereqs: [perlin-noise]
see_also: [perlin-noise, simplex-noise, worley-noise, bump-mapping, displacement-mapping, aliasing, mipmap, sampling-theorem]
sources:
  - paper: doi:10.1145/325165.325247
    title: Ken Perlin, An image synthesizer, Computer Graphics 19(3), SIGGRAPH 1985, pages 287 to 296
    locator: turbulence, a sum of the absolute value of noise over octaves, and its use for marble and fire (general locator)
  - paper: doi:10.1137/1010093
    title: Benoit B. Mandelbrot and John W. Van Ness, Fractional Brownian motions, fractional noises and applications, SIAM Review 10(4), 1968, pages 422 to 437
    locator: the definition of fractional Brownian motion with the exponent H (general locator)
  - book: isbn:9781558608481
    title: David S. Ebert, F. Kenton Musgrave, Darwyn Peachey, Ken Perlin and Steven Worley, Texturing and Modeling, A Procedural Approach, third edition, Morgan Kaufmann, 2003
    locator: the chapters by Musgrave on fractal terrain (the fBm sum with lacunarity, H and octaves, and multifractals) and by Peachey on spectral synthesis (general locator)
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, From Theory to Implementation, third edition, Morgan Kaufmann, 2016
    locator: Section 10.6.3, Noise Idioms and Spectral Synthesis
---

Fractal noise sums copies of a base noise at several scales. Each copy, an octave, has a higher frequency and a lower amplitude than the one before, so the sum has large hills with smaller bumps on them, and still smaller bumps on those. The base noise is any smooth noise with features of about one unit: [Perlin noise](/perlin-noise/), [simplex noise](/simplex-noise/) or [Worley noise](/worley-noise/). Those pages define a single scale. This page is the recipe that combines many scales. The result looks like terrain, clouds, smoke and rock, and it is the input of most [bump mapping](/bump-mapping/) and [displacement mapping](/displacement-mapping/) of natural surfaces.

## In plain words

One layer of noise looks like soft rolling hills, too smooth to be real. Real mountains have ridges on the hills, rocks on the ridges and pebbles on the rocks.

So make the same pattern several times. Make each copy twice as fine and half as tall as the one before, and add them all up. The big copies set the overall shape, and the small copies add the roughness. How fast the copies shrink sets how rough the result looks. Stop adding copies when they become smaller than a pixel, because the screen cannot show them and they would only flicker.

## When it applies

- The target is a natural texture with detail at many scales and no single feature size: terrain heights, clouds, fire, smoke, marble veins, rust and rough stone.
- A base noise with a known feature size and a mean near zero is at hand.
- The texture must be evaluated at any point, with no stored image, or at a resolution that is not known in advance.
- It does not apply when the texture needs large, distinct structures such as rivers, roads or cliffs with a direction. A plain sum of noise has no such features.

## The template

The inputs are a base noise $N$, a point $p$, the number of octaves $K$, the lacunarity $\lambda$ (the frequency ratio between octaves), the gain $g$ (the amplitude ratio, also called the persistence), and optional offsets $o_i$.

1. Set the total to 0, the amplitude to 1 and the frequency to 1.
2. For each octave $i = 0, \dots, K - 1$, add the amplitude times $N(\text{frequency} \cdot p + o_i)$ to the total.
3. After each octave, multiply the amplitude by $g$ and the frequency by $\lambda$.
4. Return the total. In one formula, $\mathrm{fbm}(p) = \sum_{i=0}^{K-1} g^i \, N(\lambda^i p + o_i)$.
5. For turbulence, add $g^i \, |N(\lambda^i p + o_i)|$ in step 2 in place of the signed value.
6. Choose $K$ so that the finest octave still has a period of at least two pixels: $K - 1 \le \log_\lambda \big(1 / (2 w f_0)\big)$, where $w$ is the size of a pixel in the units of $p$ and $f_0$ is the base frequency.

The common choice $\lambda = 2$ and $g = \tfrac12$ is tuning, not a law. Musgrave writes $g = \lambda^{-H}$, where $H$ is a roughness exponent: the amplitude of octave $i$ is then $(\lambda^i)^{-H}$, a power of its frequency, as in the fractional Brownian motion of Mandelbrot and Van Ness. A smaller $H$ gives a rougher texture. The sum only imitates fractional Brownian motion: its spectrum follows a power law in the octave envelope, but the values are not Gaussian and the texture is self-similar only over the $K$ octaves.

If $|N| \le B$, then $|\mathrm{fbm}| \le B \sum_{i<K} g^i = B (1 - g^K)/(1 - g)$, by the triangle inequality. This proved bound is loose. For the 2D gradient noise of the code, $B = 2$, and with 8 octaves and $g = \tfrac12$ the bound is $3.98$. The largest value on 50000 random points with seed 0 is $1.135$, a measurement. The octaves often cancel, because their signs are not correlated.

The code in `impl/python/` is deterministic for a fixed seed, and its test checks the sum against the base noise, octave by octave.

## Classic examples

**A trace.** Take the 2D gradient noise of the code with seed 0, the point $(0.3, 0.7)$, $K = 4$, $\lambda = 2$ and $g = \tfrac12$.

| octave $i$ | frequency | amplitude | $N$ | term | running total |
|---|---|---|---|---|---|
| 0 | 1 | 1 | $0.2325$ | $0.2325$ | $0.2325$ |
| 1 | 2 | $0.5$ | $-0.3073$ | $-0.1536$ | $0.0788$ |
| 2 | 4 | $0.25$ | $-0.3276$ | $-0.0819$ | $-0.0031$ |
| 3 | 8 | $0.125$ | $-0.0301$ | $-0.0038$ | $-0.0069$ |

The fBm value is $-0.0069$: the first octave and the next three almost cancel. Turbulence adds the absolute values and gives $0.4718$.

**Terrain.** A height field $h(x, y) = a \cdot \mathrm{fbm}(x / L, y / L)$, with a feature size $L$ and a height $a$, is the classic procedural landscape. The mesh is then displaced as in [displacement mapping](/displacement-mapping/), or the derivative of $h$ perturbs the normal as in [bump mapping](/bump-mapping/).

**Marble.** Perlin's marble is $\sin(x + a \cdot \mathrm{turbulence}(p))$: the turbulence bends straight stripes into veins. The creases of $|N|$ at the zeros of each octave give the sharp, folded look.

**Clouds.** Map fBm through a threshold and a smooth ramp to a density or an opacity. Animate it with a fourth coordinate in time, which is where [simplex noise](/simplex-noise/) costs less than Perlin noise.

**Rock and craters.** Summing octaves of $F_1$ of [Worley noise](/worley-noise/) gives pitted stone, with cells inside cells.

## Variations

- **Turbulence.** $\sum g^i |N|$, from Perlin's 1985 paper. It is positive, and it has creases at the zeros of each octave.
- **Ridged multifractal.** Musgrave's form uses $(c - |N|)^2$ with an offset $c$ near 1, and makes the weight of each octave depend on the value of the octave before, which gives sharp ridges with smooth valleys.
- **Domain warping.** Evaluate $\mathrm{fbm}(p + c \cdot \mathrm{fbm}(p))$, which gives swirls and flows.
- **Lacunarity near 2.** A value such as $1.92$ in place of exactly 2 keeps the lattices of the octaves from lining up. Per-octave offsets or rotations do the same.
- **Analytic derivatives.** The gradient of the sum is the sum of $g^i \lambda^i \nabla N(\lambda^i p)$, so a base noise with derivatives gives the normal for bump mapping at little extra cost.
- **Band limited octaves.** Fade the last octave in or out with a fractional $K$, so that the detail does not pop when the distance changes.

## Pitfalls

- **Zeros at integer points.** With a gradient noise as the base, $\lambda = 2$ and no offsets, every octave is zero at the integer points, so the sum is zero there. The code test checks this on $20 \times 20$ points, and checks that per-octave offsets remove it. Integer sample grids then show a regular pattern.
- **Aliasing.** An octave with a period shorter than two pixels cannot be shown, and it aliases into flicker and moiré. Limit $K$ by the pixel footprint as in step 6. A mipmapped texture filters on its own, but procedural noise does not. See [aliasing](/aliasing/) and the [sampling theorem](/sampling-theorem/).
- **Too many octaves.** Each octave costs one evaluation of the base noise, and octaves below the pixel size cost time and add only noise. The rule of step 6 also bounds the cost.
- **Assuming a range.** The range grows with the amplitude sum, and the true values are much smaller than the proved bound. Normalize by a measured range, or by the bound if a clamp is not acceptable.
- **A biased base.** The sum adds the mean of each octave. A base with a nonzero mean, such as $F_1$ of Worley noise, drifts with $K$. Subtract the mean first.
- **Persistence and lacunarity are tuning.** There are no correct values. Choose them by eye for each material.

## Exercises

1. Show that $\sum_{i<K} g^i = (1 - g^K)/(1 - g)$, and find $K$ so that the octaves after $K$ add at most 1 percent of the total amplitude for $g = \tfrac12$.
2. A terrain spans 1000 m on a screen of 2000 pixels, and the base noise has a period of 100 m. With $\lambda = 2$, how many octaves have a period of at least two pixels?
3. Show that $\mathrm{fbm}(q) = 0$ for every integer point $q$ when the base noise is zero at integer points, $\lambda$ is an integer and there are no offsets.
4. With $g = \lambda^{-H}$, show that the amplitude of an octave is $f^{-H}$ in terms of its frequency $f$, and compute the gain for $H = 0.8$ and $\lambda = 2$.
5. Compute the gradient of $\mathrm{fbm}$ from the gradient of $N$, and explain why the fine octaves dominate the normal of a bump map even when they are small in height.

## References
