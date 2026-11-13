---
tag: Y521G8
kind: algorithm
slug: temporal-antialiasing
name: Temporal antialiasing
aliases:
- TAA
area: graphics-and-signals/rasterization
level: advanced
summary: Accumulates jittered samples across frames with reprojection to approximate supersampling.
solves: [antialiasing]
model: real-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels, f: number of frames}
  time: {worst: Θ(f W H), average: Θ(f W H), best: Θ(f W H)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, in_place: false}
history:
  year: 2009
  people: [Lei Yang, Diego Nehab, Pedro V. Sander, Pitchaya Sitthi-amorn, Jason Lawrence, Hugues Hoppe]
  note: Amortized supersampling reused shading samples of earlier frames by reprojection; game engines turned the idea into the TAA of today, and Karis described the version of Unreal Engine 4 in 2014.
prereqs: [supersampling-antialiasing, bilinear-filtering]
see_also: [antialiasing, multisample-antialiasing, morphological-antialiasing, halton-sequence, exponential-moving-average, optical-flow, super-resolution, reconstruction-filter]
sources:
  - paper: doi:10.1145/1618452.1618481
    title: Lei Yang, Diego Nehab, Pedro V. Sander, Pitchaya Sitthi-amorn, Jason Lawrence and Hugues Hoppe, Amortized supersampling, ACM Transactions on Graphics 28(5), article 135, SIGGRAPH Asia 2009
    locator: the whole paper (reprojection of earlier shading samples, the recursive blend and the control of blur from repeated resampling)
  - paper: "Brian Karis, High Quality Temporal Supersampling, Advances in Real-Time Rendering in Games, SIGGRAPH 2014 course"
    locator: the slides (Halton (2,3) jitter, the exponential moving average, reprojection with velocity, the neighborhood clamp to the 3 by 3 minimum and maximum, clipping in YCoCg and the luminance weight)
  - paper: doi:10.1111/cgf.14018
    title: Lei Yang, Shiqiu Liu and Marco Salvi, A Survey of Temporal Antialiasing Techniques, Computer Graphics Forum 39(2), pages 607 to 621, Eurographics 2020 state of the art report
    locator: the whole survey (sample accumulation, history validation and rectification, temporal upsampling and the open problems)
  - book: isbn:9781138627000
    title: Tomas Akenine-Möller, Eric Haines, Naty Hoffman, Angelo Pesce, Michał Iwanicki and Sébastien Hillaire, Real-Time Rendering, fourth edition, 2018
    locator: Chapter 5, Section 5.4, Aliasing and Antialiasing (the part on temporal antialiasing)
---

Temporal antialiasing (TAA) takes one sample per [pixel](/pixel/) in each frame, at a position inside the pixel that changes from frame to frame, and blends it into a history image that it keeps from the frames before. When the scene or the camera moves, it fetches the history at the place where the surface was in the previous frame, by motion vectors and [bilinear filtering](/bilinear-filtering/), and it clamps the fetched value to the colors around the pixel to reject history that no longer fits. On a still image, with the weight $1/t$ for frame $t$ and no clamp, it converges to [supersampling](/supersampling-antialiasing/) with many samples per pixel at the cost of about one sample per pixel and frame; with the usual fixed weight near $0.1$ its noise stays that of a mean of about 19 samples. It is a heuristic: with motion, new surfaces and wrong motion vectors, it can blur, ghost or flicker.

## In plain words

Supersampling takes many samples in each pixel and averages them, which costs many times more work per frame. TAA spreads this work over time. Each frame takes only one sample per pixel, but at a slightly different spot inside the pixel each time. The renderer keeps the result of the last frame and mixes a small part of the new sample into it. After a few frames, each pixel holds an average of many samples, as if it had been supersampled. When things move, each pixel looks up where its surface was in the last frame and takes the old result from there. Sometimes the old result is wrong, for example when a surface comes into view from behind another one. So TAA limits the old value to the range of colors that the pixel and its neighbors have now, which removes most trails of old colors.

## The problem

The input is a scene that a renderer can sample at any point of the screen in each frame $t = 1, 2, \dots$, given as a function $\mathrm{render}(t, x, y)$ that returns a color, and for each frame a motion vector per pixel, the screen motion from frame $t - 1$ to frame $t$ of the surface seen at that pixel. Pixel $(i, j)$ is the cell $[i, i+1] \times [j, j+1]$ with its center at $(i + 1/2, j + 1/2)$; rows grow downward. The output for each frame is an image of $W \times H$ pixels that estimates the box-filtered [antialiasing](/antialiasing/) answer of that frame. The budget is about one call of $\mathrm{render}$ per pixel and frame, and one extra image of memory.

## The algorithm

```pseudo id=main
TAA-FRAME(t, history, α)               ▷ history is the output of frame t − 1, or none
L1  (o, o') ← (h₂(t), h₃(t))           ▷ point t of the Halton sequence in bases 2 and 3
L2  x[i, j] ← render(t, i + o, j + o') for every pixel
L3  for each pixel p = (i, j) do
L4      if there is no history then out[p] ← x[p]; continue
L5      q ← p + (1/2, 1/2) − v[p]       ▷ the center of p, moved back by the motion vector
L6      h ← BILINEAR(history, q)
L7      (lo, hi) ← per-channel minimum and maximum of x over the 3 × 3 pixels around p
L8      h ← min(max(h, lo), hi)
L9      out[p] ← α · x[p] + (1 − α) · h
L10 return out
```

Line L1 picks the jitter of frame $t$: the radical inverses of $t$ in bases 2 and 3, the [Halton sequence](/halton-sequence/) that Karis used. Its points spread evenly over the pixel for any number of frames. Line L2 takes the one sample per pixel at the jittered point; a real renderer does this by moving the projection by a subpixel offset. Line L4 handles the first frame, where there is no history yet. Line L5 finds where the surface of $p$ was one frame earlier; the motion vectors come from the renderer, which knows how each vertex moved, and point from frame $t - 1$ to frame $t$. Line L6 reads the history there with bilinear filtering, since the point is in general not a pixel center; the history stores pixel values at pixel centers, without jitter. Lines L7 and L8 are the *neighborhood clamp*: an antialiased pixel should be a mix of the colors near it, so a history value outside the range of the current $3 \times 3$ neighborhood is stale, and the clamp moves it to the nearest point of that range. Line L9 is an [exponential moving average](/exponential-moving-average/): it keeps most of the history and adds a small part $\alpha$ of the new sample. Real-time renderers use a fixed $\alpha$ near $0.1$; $\alpha = 1/t$ on a still scene gives the plain mean of all samples so far.

## Example

**A still edge.** Let the scene be white ($1$) where $x > 4/3$ and black ($0$) elsewhere, on an image of 3 by 1 pixels, with $\alpha = 1/t$. The middle pixel is the cell $[1, 2] \times [0, 1]$, and the edge covers $2/3$ of it, the box-filtered answer. Its samples lie at $x = 1 + h_2(t)$ with $h_2(t) = 1/2, 1/4, 3/4, 1/8, 5/8, 3/8, 7/8, 1/16$ for $t = 1$ to $8$, so they are white, black, white, black, white, white, white, black. The output of the middle pixel in frames 1 to 8 is $1, 1/2, 2/3, 1/2, 3/5, 2/3, 5/7, 5/8$, the running means of these samples. One sample per frame would flip between 0 and 1; TAA settles near $2/3$. The neighbors of the middle pixel are always 0 and 1, so the clamp does nothing here.

**The clamp on a lone pixel.** The same scene on an image of a single pixel, the cell of the middle pixel above, gives $1, 0, 1, 0, 1, 1, 1, 0$: the output just repeats the current sample. The $3 \times 3$ neighborhood holds only the pixel itself, so the clamp cuts the history to the current value, and the history has no effect. The clamp needs neighbors that show both sides of an edge; it trades some antialiasing for robustness.

**Ghosting.** Let a $2 \times 2$ image be white for frames 1 to 20 and black from frame 21 on, as when a dark object moves in front of a light wall without motion vectors, with $\alpha = 1/10$. Without the clamp, frame $20 + k$ shows $(9/10)^k$, and frame 30 still shows $(9/10)^{10} \approx 0.349$: a ghost of the old white. With the clamp, the neighborhood of frame 21 is black only, the history is clamped to 0, and frame 21 is black at once.

## Correctness

TAA has no guarantee for a general moving scene, but four facts hold, and they explain what it computes. With a still scene and no clamp, each output is a weighted mean of the samples of all frames so far, with weight $\alpha (1 - \alpha)^{t-k}$ for frame $k \ge 2$ and $(1 - \alpha)^{t-1}$ for frame 1, which sum to 1. With $\alpha_t = 1/t$ this is the plain mean of the samples at the first $t$ Halton points, which is supersampling of each pixel with that pattern. With motion by a whole number of pixels per frame and exact motion vectors, the bilinear fetch reads exactly one history pixel, and the same mean follows each surface point, away from the image border. With the clamp, each output lies in the range of the current $3 \times 3$ neighborhood, since it is a convex combination of the current sample and a value in that range. For a constant $\alpha$ and samples with independent noise, the variance tends to $\alpha / (2 - \alpha)$ times that of one sample, the noise of a mean of $(2 - \alpha)/\alpha$ samples, 19 for $\alpha = 1/10$. The proofs are below.

## Complexity

- **Time per frame.** One call of the renderer per pixel, one bilinear fetch of four history pixels, nine reads for the clamp and one blend: $\Theta(W H)$ besides the cost of rendering. Over $f$ frames this is $\Theta(f W H)$.
- **Memory.** One history image of $\Theta(W H)$, plus the motion vectors. A $k$-sample supersampler needs $k$ samples per pixel in each frame; TAA approaches its quality on still regions after about $k$ frames at the cost of one sample per pixel and frame.

## Properties

- **Amortized.** The cost of the samples is spread over frames, so one sample per pixel and frame suffices on still parts of the image.
- **Antialiases shading, too.** Unlike [multisampling](/multisample-antialiasing/), each new sample is fully shaded, so TAA also removes aliasing from textures, specular highlights and shader detail.
- **Temporally stable.** On still and slowly moving regions the output changes little from frame to frame, which suppresses crawling and flicker that post-process filters such as [MLAA](/morphological-antialiasing/) leave.
- **Blurs a little.** Bilinear fetches with motion by fractions of a pixel blur the history slightly in every frame, and the blur adds up over frames.
- **Needs motion vectors.** Without correct motion vectors for every moving surface, old colors leave trails.

## Variants and improvements

- **Clipping in place of clamping.** Karis clips the history toward the mean of the neighborhood along a line, in place of clamping each channel, and does it in the YCoCg color space with a box that follows luminance; colors no longer collect in the corners of the box.
- **Variance clipping.** Salvi proposed a box from the mean and the standard deviation of the neighborhood, which is tighter than the minimum and maximum.
- **Luminance weights.** Weighting each sample by $1/(1 + \text{luma})$ before the blend keeps rare very bright samples from dominating and flickering in high dynamic range.
- **Velocity dilation.** Taking the motion vector of the nearest surface in the $3 \times 3$ neighborhood keeps edges of moving objects antialiased.
- **History rejection.** Depth or object identifier tests reject history from a different surface, as in the reverse reprojection caching of Nehab and coworkers (2007).
- **Temporal upsampling.** Rendering at a lower resolution and accumulating jittered samples into a higher resolution history is the basis of temporal upscalers, a form of [super-resolution](/super-resolution/).

## When to use it

Use TAA in real-time renderers with deferred shading or complex shaders, where [multisampling](/multisample-antialiasing/) is expensive or does not help, and where shading aliasing matters as much as edge aliasing. It is the usual choice in game engines. Use [supersampling](/supersampling-antialiasing/) for offline rendering and reference images, where the cost is acceptable and blur and ghosting are not. Use a post-process filter such as [MLAA](/morphological-antialiasing/) when the renderer cannot supply motion vectors.

## Pitfalls

- **Wrong or missing motion vectors.** Animated textures, particles, translucent surfaces and procedural animation often have no correct motion vectors, and they leave trails or smear.
- **Disocclusion.** A surface that comes into view has no history; the clamp hides most of the error, but the new region is aliased for a few frames.
- **Over-blurring.** A small $\alpha$ and repeated bilinear fetches soften the image; many engines sharpen the result afterwards.
- **Jitter in the history.** The history must store unjittered pixel values, and the motion vectors must not contain the jitter, or the image shakes.
- **Clamp artifacts.** On thin features and high-contrast texture, the clamp throws away good history, and flicker returns, as in the lone-pixel example.
- **Order in the pipeline.** Run TAA before bloom, depth of field and other post effects, and blend in a space where bright values do not dominate.

## Implementations

## History

Nehab and coworkers (2007) introduced reverse reprojection caching, which reuses shading of the previous frame at the reprojected position. Yang and coworkers (2009) built on it amortized supersampling: jittered samples, reprojection, a recursive blend and control of the blur that repeated resampling causes. Game engines adopted the idea from about 2011, with neighborhood clamping by Lottes and Malan, and Karis (2014) described the TAA of Unreal Engine 4, which became the common reference design. Yang, Liu and Salvi (2020) surveyed the field, and temporal upscalers grew from the same accumulation.

## References
