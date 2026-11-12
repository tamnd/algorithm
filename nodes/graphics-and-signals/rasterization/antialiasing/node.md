---
tag: Q3TEXM
kind: problem
slug: antialiasing
name: Antialiasing
aliases:
- anti-aliasing
area: graphics-and-signals/rasterization
level: core
summary: Reduce aliasing artifacts by estimating area coverage or filtered intensity per pixel.
prereqs: [aliasing, sampling-theorem, pixel]
see_also: [supersampling-antialiasing, multisample-antialiasing, morphological-antialiasing, temporal-antialiasing, reconstruction-filter, a-buffer, wu-line-algorithm, stratified-sampling]
sources:
  - paper: doi:10.1145/359863.359869
    title: Franklin C. Crow, The aliasing problem in computer-generated shaded images, Communications of the ACM 20(11), 1977, pages 799 to 805
    locator: the whole paper (jagged edges, small objects and the prefiltering remedy)
  - url: https://alvyray.com/Memos/MemosCG.htm
    title: Alvy Ray Smith, A Pixel Is Not A Little Square, A Pixel Is Not A Little Square, A Pixel Is Not A Little Square! (And a Voxel is Not a Little Cube), Microsoft Technical Memo 6, 1995
    locator: the whole memo (a pixel is a point sample, and the image is reconstructed by a filter)
  - paper: doi:10.1145/237170.237265
    title: Don P. Mitchell, Consequences of stratified sampling in graphics, SIGGRAPH 1996, pages 277 to 280
    locator: the analysis of the variance of stratified sampling for pixels that contain edges
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, 2018
    locator: Chapter 5, Section 5.4, Aliasing and Antialiasing
  - book: isbn:9780128006450
    title: Matt Pharr, Wenzel Jakob and Greg Humphreys, Physically Based Rendering, third edition, 2016
    locator: Chapter 7, Section 7.1 (sampling theory and the sources of aliasing in rendering)
---

Antialiasing is the problem of computing the value of each [pixel](/pixel/) of a rendered image as a filtered average of the scene around the pixel, instead of the value of the scene at one point. A rendered scene has sharp edges, so it is not band-limited, and one point sample per pixel shows [aliasing](/aliasing/): jagged edges, small objects that flicker or vanish, and moiré patterns. An antialiasing method estimates the filtered value, most often the fraction of the pixel's area that each surface covers. This page states the problem; the methods are [supersampling](/supersampling-antialiasing/), [multisampling](/multisample-antialiasing/), [morphological antialiasing](/morphological-antialiasing/), [temporal antialiasing](/temporal-antialiasing/) and analytic coverage.

## In plain words

A screen shows a picture as a grid of colored dots. The simple way to make the dots is to look at the scene through the center of each dot and copy the color seen there. At the edge of a shape this gives a hard choice: the dot gets the shape's color or the background's color, nothing in between. A slanted edge then looks like a staircase. A thin wire can fall between the centers and vanish, and it can blink as it moves. A fine pattern can turn into a large false pattern. Antialiasing gives each dot an average of what the scene shows near it. A dot that is half covered by a black shape on white becomes mid gray. The methods differ in how they estimate this average: by looking at more points, by computing the covered area, or by reusing earlier frames.

## Definition

**Model.** The scene is a function $f : \mathbb{R}^2 \to [0, 1]^3$ that gives the linear color seen at each point of the image plane. The image has $W \times H$ pixels. Pixel $(i, j)$ is a point sample at its center $(i + 1/2, j + 1/2)$, as in the OpenGL and Direct3D 10 rules. A filter $h : \mathbb{R}^2 \to \mathbb{R}$ with $\int h = 1$ is given. Values outside the image are not needed when $h$ is zero beyond half a pixel; for wider filters, the scene is defined beyond the border.

**Task.** Compute, for each pixel,

$$p_{i,j} = \iint h\big(x - i - \tfrac12,\ y - j - \tfrac12\big)\, f(x, y)\, dx\, dy.$$

With the box filter, $h = 1$ on $[-1/2, 1/2]^2$ and $0$ elsewhere, $p_{i,j}$ is the mean of $f$ over the unit square around the center. For a scene of flat-colored polygons this is the sum of each visible polygon's color times its covered area in the square. Other filters are the subject of the [reconstruction filter](/reconstruction-filter/) page. The box filter is one choice of $h$; the pixel itself is a point, not the square (Smith 1995).

**Point sampling.** The method with no antialiasing outputs $f(i + 1/2, j + 1/2)$.

**Quality.** The error of an estimate $\hat p$ is $|\hat p_{i,j} - p_{i,j}|$ per pixel and channel, in the worst case over scenes of a stated class, or as the variance under a stated random sampling.

## Variants

- **Geometric aliasing.** Edges of polygons and thin geometry. This is the case that coverage methods target.
- **Shading aliasing.** A shading function with fine detail, such as a sharp specular highlight on a bumpy surface, aliases even inside one polygon.
- **Texture aliasing.** A texture seen at a distance has more detail than the pixels can show. It is handled by prefiltering the texture, as in [mipmaps](/mipmap/) and [anisotropic filtering](/anisotropic-filtering/), which are part of [texture mapping](/texture-mapping/).
- **Temporal aliasing.** Motion that is fast compared to the frame rate. Its remedy is motion blur, an average over time.
- **Lines and text.** Thin primitives, where the coverage is computed in closed form, as in the [Wu line algorithm](/wu-line-algorithm/).

## Examples

Take one row of 4 pixels, $0 \le y \le 1$, and a black region below the line $y = x/4 + 1/6$ on white. The table gives the black fraction of each pixel: exact (box filter), by one point sample at the center, and by a $4 \times 4$ and a $16 \times 16$ grid of samples.

| pixel | exact | 1 sample | $4 \times 4$ | $16 \times 16$ |
|---|---|---|---|---|
| 0 | $7/24 \approx 0.292$ | $0$ | $5/16 = 0.3125$ | $19/64 \approx 0.297$ |
| 1 | $13/24 \approx 0.542$ | $1$ | $9/16 = 0.5625$ | $35/64 \approx 0.547$ |
| 2 | $19/24 \approx 0.792$ | $1$ | $13/16 = 0.8125$ | $51/64 \approx 0.797$ |
| 3 | $71/72 \approx 0.986$ | $1$ | $1$ | $253/256 \approx 0.988$ |

One sample per pixel gives the staircase $0, 1, 1, 1$. The $4 \times 4$ grid is off by at most $1/48$, and the $16 \times 16$ grid by at most $1/192$.

**A vanishing object.** A vertical bar of width $0.2$ pixel at $0.6 \le x \le 0.8$ covers 20% of each pixel in column 0, but no pixel center has $x$ in that range, so point sampling misses it in every row. If the bar moves sideways, it shows in the frames where it crosses a column of centers and vanishes in the others, so it blinks.

## Known algorithms

- [Supersampling](/supersampling-antialiasing/): take $N$ samples per pixel, shade each one, and average them. It handles all three kinds of spatial aliasing, at $N$ times the shading cost.
- [Multisample antialiasing](/multisample-antialiasing/): test coverage and depth at $N$ samples per pixel, but shade once per pixel and triangle. It handles geometric aliasing only.
- [Morphological antialiasing](/morphological-antialiasing/): find edges in the finished image and blend across them. It is a post process on one sample per pixel.
- [Temporal antialiasing](/temporal-antialiasing/): move the sample point a little in each frame, and blend the frame with the reprojected result of earlier frames.
- Analytic coverage: clip each polygon to the pixel square with [polygon window clipping](/polygon-window-clipping/) and take the area with the [shoelace formula](/shoelace-formula/). The [A-buffer](/a-buffer/) keeps coverage masks per fragment to resolve visibility inside a pixel.
- Stochastic sampling: [distributed ray tracing](/distributed-ray-tracing/) and [path tracing](/path-tracing/) place random or [stratified](/stratified-sampling/) samples and estimate the integral by [Monte Carlo integration](/monte-carlo-integration/) or [quasi-Monte Carlo integration](/quasi-monte-carlo-integration/).
- Texture prefiltering: [mipmaps](/mipmap/), [anisotropic filtering](/anisotropic-filtering/) and summed-area tables (an [integral image](/integral-image/) of the texture).

## Bounds

- **The sampling theorem does not apply.** The [sampling theorem](/sampling-theorem/) needs a band-limited signal. An edge is a step, whose Fourier transform decays only like $1/|\omega|$, so no sampling rate removes aliasing. Antialiasing replaces $f$ by the filtered $h * f$ before the point sample, which is the prefilter that the theorem assumes.
- **No point-sampling method is exact.** Let a deterministic method look at $f$ at finitely many points in a pixel, possibly chosen one after another from the values seen. Run it on an empty pixel and note the points. A polygon with thin slits around those points can cover all of the pixel's area except an amount $\varepsilon$, while every sample sees the background. The method then sees the same values as for an empty pixel, so on one of the two scenes its box-filter error is at least $(1 - \varepsilon)/2$.
- **Ordered grid.** With a $k \times k$ grid ($N = k^2$ samples), the error for a pixel crossed by one straight edge is at most $(2k-1)/k^2 < 2/k$, and a horizontal edge between two sample rows shows that it can be close to $1/(2k)$. So the worst case error is $\Theta(N^{-1/2})$. The proof is on the [supersampling](/supersampling-antialiasing/) page.
- **Random and stratified samples.** With $N$ independent uniform samples, the estimate of a coverage $c$ is unbiased with variance $c(1-c)/N \le 1/(4N)$. With one jittered sample in each cell of a $k \times k$ grid, the variance for one straight edge is at most $(2k-1)/(4k^4) < N^{-3/2}/2$, so the RMS error is $O(N^{-3/4})$. Mitchell (1996) studied this gain of stratified sampling at edges.
- **Analytic coverage.** For a convex polygon with $m$ vertices, clipping to a pixel square and the shoelace formula take $O(m)$ time per pixel, and the result is exact in exact arithmetic. Resolving overlaps between polygons inside a pixel is the hard part.

## Reductions

- Box-filter antialiasing of flat-colored, non-overlapping polygons reduces to the area of a polygon clipped to a square: [polygon window clipping](/polygon-window-clipping/) and then the [polygon area](/polygon-area/).
- With a general filter, the problem is numerical integration of $h \cdot f$ over the filter support, so all of [Monte Carlo integration](/monte-carlo-integration/) applies.
- A high resolution render followed by a downsampling filter is the [image resampling](/image-resampling/) problem.

## Applications

- Real-time rendering in games and user interfaces, usually with MSAA, morphological or temporal methods.
- Offline rendering for film, with many stratified or quasi-random samples per pixel.
- Fonts and 2D vector graphics, where analytic coverage of curves and polygons is common.
- Line drawing in plots, maps and CAD tools.

## References
