---
tag: DED02A
kind: algorithm
slug: supersampling-antialiasing
name: Supersampling antialiasing
aliases:
- SSAA
- full-scene antialiasing
area: graphics-and-signals/rasterization
level: intro
summary: Renders at a higher resolution and averages the samples down to each pixel.
solves: [antialiasing]
model: real-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels, k: samples along each side of a pixel, n: number of triangles}
  time: {worst: Θ(W H k^2 n), average: Θ(W H k^2 n), best: Θ(W H k^2 n)}
  space: {extra: Θ(1)}
properties: {deterministic: true, in_place: false}
history:
  year: 1986
  people: [Robert L. Cook]
  note: Cook replaced the regular grid of samples by jittered samples, which turn aliasing into noise.
prereqs: [antialiasing, pixel, triangle-rasterization]
see_also: [multisample-antialiasing, temporal-antialiasing, morphological-antialiasing, stratified-sampling, reconstruction-filter, distributed-ray-tracing, halton-sequence, monte-carlo-integration]
sources:
  - paper: doi:10.1145/359863.359869
    title: Franklin C. Crow, The aliasing problem in computer-generated shaded images, Communications of the ACM 20(11), 1977, pages 799 to 805
    locator: the whole paper (the causes of aliasing in rendered images and filtering as the remedy)
  - paper: doi:10.1145/7529.8927
    title: Robert L. Cook, Stochastic sampling in computer graphics, ACM Transactions on Graphics 5(1), 1986, pages 51 to 72
    locator: the sections on jittered sampling and on the noise that replaces aliasing
  - paper: doi:10.1145/237170.237265
    title: Don P. Mitchell, Consequences of stratified sampling in graphics, SIGGRAPH 1996, pages 277 to 280
    locator: the variance of stratified sampling in pixels that contain an edge
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, 2018
    locator: Chapter 5, Section 5.4, Aliasing and Antialiasing (supersampling, sampling patterns and the resolve)
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, third edition, 2016
    locator: Chapter 7, Sections 7.3 (stratified sampling) and 7.8 (image reconstruction)
---

Supersampling antialiasing (SSAA) estimates the area average of the scene over each [pixel](/pixel/) by taking $N$ point samples inside the pixel, shading every sample in full, and averaging the results. It is the brute-force solution of the [antialiasing](/antialiasing/) problem: it reduces edge, shading and texture aliasing alike, and its cost grows by the factor $N$. With an ordered $k \times k$ grid, the error at a pixel crossed by one straight edge is at most $(2k-1)/k^2$, so it falls like $N^{-1/2}$; with one jittered sample per grid cell, the estimate is unbiased and its RMS error falls like $N^{-3/4}$. Rendering at a higher resolution and then downscaling the image is the same method.

## In plain words

Each pixel of the screen stands for a small area of the scene. The plain method looks at the scene only through the center of each pixel, so an edge gives a hard step. Supersampling looks through many points inside each pixel, for example a grid of four by four points, and computes the full color at each point as if each point were a pixel of its own. Then it takes the average of these colors as the color of the pixel. A pixel that an edge cuts in half then gets about half of each color. The cost is high: with sixteen points per pixel, the renderer does sixteen times the work. If the points move a little at random inside their grid cells, the regular steps of the grid turn into a fine noise, which the eye accepts more easily.

## The problem

The input is a scene of $n$ triangles with colors, listed in priority order (a later triangle hides an earlier one), a background color, an image size $W \times H$, and a sample count $N = k^2$. Coordinates are in pixel units. Pixel $(i, j)$ is the point sample at the center $(i + 1/2, j + 1/2)$; its box filter covers the square $[i, i+1] \times [j, j+1]$. The pixel is a point and the square is only the support of the box filter. Colors are linear values in $[0, 1]$ per channel. The output is the box-filtered image of the [antialiasing](/antialiasing/) problem, estimated from samples. A sample on a triangle's edge counts as inside (an inclusive rule), and triangles of zero area draw nothing. No border rule is needed, because the box filter of a pixel stays inside the pixel.

## The algorithm

```pseudo id=main
SSAA(scene, W, H, k)                 ▷ k × k samples per pixel, box resolve
L1  for each pixel (i, j) do
L2      sum ← 0
L3      for a ← 0 to k − 1 and b ← 0 to k − 1 do
L4          (x, y) ← (i + (a + 1/2)/k, j + (b + 1/2)/k)
L5          t ← the frontmost triangle that contains (x, y), or none
L6          sum ← sum + SHADE(t, x, y)            ▷ the background if there is no t
L7      P[i, j] ← sum / k²
L8  return P
```

Line L4 places the samples at the centers of the $k \times k$ cells of the pixel, the *ordered grid*. In the *jittered* version, line L4 instead picks a uniform random point in cell $(a, b)$. Line L5 is the visibility test of one sample; this version scans the triangles, and a rasterizer does the same work by drawing each triangle into a [z-buffer](/z-buffer/) with $k \times k$ samples per pixel. Line L6 calls the shader once per sample, which is what makes SSAA handle shading and texture aliasing. Line L7 is the *resolve*: a box filter over the samples of the pixel.

## Example

A white triangle with corners $(3/5, 2/5)$, $(7/2, 1)$ and $(1, 3)$ lies on a black image of $4 \times 3$ pixels. Its area is $73/20 = 3.65$ pixels. The table gives the covered fraction of each pixel, row $j$ by column $i$.

| row | exact (box filter) | $k = 1$ | $k = 4$ | $k = 16$ |
|---|---|---|---|---|
| 0 | 0.196, 0.414, 0.207, 0.026 | 0, 0, 0, 0 | 0.125, 0.438, 0.25, 0 | 0.191, 0.414, 0.207, 0.027 |
| 1 | 0.231, 1, 0.775, 0.1 | 0, 1, 1, 0 | 0.25, 1, 0.813, 0.063 | 0.234, 1, 0.777, 0.098 |
| 2 | 0.077, 0.6, 0.025, 0 | 0, 1, 0, 0 | 0.063, 0.625, 0, 0 | 0.074, 0.602, 0.023, 0 |

The exact values are $369/1885$, $12/29$, $6/29$, $3/116$ in row 0, then $3/13$, $1$, $31/40$, $1/10$, then $1/13$, $3/5$, $1/40$, $0$. With one sample per pixel the triangle turns into four whole pixels. The largest error over the 12 pixels is $0.414$ for $k = 1$, $0.071$ for $k = 4$ and $0.0043$ for $k = 16$. Pixel $(1, 1)$ is fully covered, so every $k$ gives the exact value 1 there.

## Correctness

The algorithm outputs the mean of the shaded samples of each pixel; this is a direct reading of lines L2 to L7. The quality statement is a bound against the exact box filter. Call a cell of the $k \times k$ grid *cut* if its interior meets an edge of some triangle. On a cell that is not cut, the visible color is constant, so the center sample equals the cell average exactly. Each cut cell adds an error of at most $1/k^2$ per channel. A straight segment meets the interiors of at most $2k - 1$ cells, because it crosses each of the $2k - 2$ interior grid lines at most once. So the error at a pixel is at most $s(2k-1)/k^2$ for $s$ edges in the pixel, and a horizontal edge just below a row of samples shows that an error close to $1/(2k)$ occurs. For jittered samples, each cell gives an unbiased estimate of its own average, and only cut cells have nonzero variance, at most $1/(4k^4)$ each. The full proofs are below.

## Complexity

- **Shading.** Line L6 runs $W H k^2$ times, so the shader runs $N = k^2$ times per pixel. This is the cost that limits SSAA in practice.
- **Visibility.** The brute-force scan of line L5 takes $\Theta(n)$ per sample, so this version takes $\Theta(W H k^2 n)$ time in every case. A rasterizer with a z-buffer at the sample resolution takes time proportional to $W H k^2$ plus the number of samples that the triangles cover.
- **Memory.** This version resolves each pixel at once and needs $\Theta(1)$ space besides the image. A GPU renders the whole frame first, so it stores $\Theta(W H k^2)$ color and depth samples, $k^2$ times the memory of the frame.
- **Error.** Ordered grid: at most $(2k-1)/k^2$ per straight edge, worst case $\Theta(N^{-1/2})$. Jittered: unbiased, with variance at most $(2k-1)/(4k^4) < N^{-3/2}/2$ per straight edge between two colors.

## Properties

- **Handles every kind of spatial aliasing.** Edges, shading and textures are all sampled $N$ times per pixel.
- **Consistent.** As $k$ grows, the result converges to the box-filtered image for scenes of triangles.
- **Exact on uniform pixels.** A pixel with no edge in its interior gets the exact value for every $k$.
- **Ordered grid weakness.** Near-horizontal and near-vertical edges see only $k$ distinct sample heights or widths, so they get only $k + 1$ levels of coverage, not $k^2 + 1$.
- **The resolve filter.** The box filter is the simplest choice and it still lets some aliasing through; see [reconstruction filters](/reconstruction-filter/).

## Variants and improvements

- **Jittered, or stratified, sampling.** One random sample per cell, as in [stratified sampling](/stratified-sampling/). Cook introduced it to graphics; aliasing becomes noise of the right mean.
- **Rotated grid.** Four samples on a grid rotated so that all four have different $x$ and different $y$ positions. Near-horizontal and near-vertical edges then get 5 coverage levels instead of 3.
- **Low-discrepancy patterns.** Samples from a [Halton sequence](/halton-sequence/) or another low-discrepancy set, as in [quasi-Monte Carlo integration](/quasi-monte-carlo-integration/).
- **Adaptive supersampling.** Take a few samples first, and add more only where they differ.
- **Wider resolve filters.** A tent, Gaussian or Mitchell-Netravali filter that also weights samples of the neighbor pixels.
- **Multisampling.** [Multisample antialiasing](/multisample-antialiasing/) keeps the coverage and depth samples but shades once per pixel and triangle.
- **Samples over time.** [Temporal antialiasing](/temporal-antialiasing/) takes one jittered sample per pixel in each frame and accumulates them over frames.
- **Ray tracing.** [Distributed ray tracing](/distributed-ray-tracing/) and [path tracing](/path-tracing/) take many samples per pixel and also spread them over the lens, time and light paths.

## When to use it

Use SSAA when quality matters more than time: offline rendering, screenshots, reference images for testing other methods, and scenes with fine shading or texture detail that cheaper methods miss. It is also the simplest correct method to implement. In real-time rendering at high resolution it is usually too expensive, and MSAA, morphological or temporal methods replace it.

## Pitfalls

- **Resolving in sRGB.** The average must be taken on linear values. Averaging sRGB codes makes edges too dark.
- **Too few distinct positions.** A $2 \times 2$ ordered grid gives only 3 levels on a near-horizontal edge. A rotated grid of the same cost gives 5.
- **Sample positions on edges.** With an inclusive rule, a sample on an edge shared by two triangles counts for both. A real rasterizer uses the [top-left fill rule](/top-left-fill-rule/) so that each sample belongs to exactly one triangle.
- **Memory.** A $4 \times 4$ supersampled frame buffer needs 16 times the memory and bandwidth of the plain frame buffer.
- **Thin features still alias.** A line thinner than the sample spacing can still fall between all samples. Supersampling lowers the size at which aliasing starts; it does not remove it.

## Implementations

## History

Crow's 1977 paper set out the aliasing problem in rendered images and argued for filtering the scene over the area of each pixel. Cook (1986) showed that jittered samples turn the aliasing of a regular grid into noise, and used them in distributed ray tracing. Mitchell (1996) analyzed why stratified samples give a lower variance in pixels that contain edges.

## References
