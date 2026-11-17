---
tag: QXNMEN
kind: algorithm
slug: beier-neely-morphing
name: Beier-Neely morphing
aliases:
- feature-based image metamorphosis
- field morphing
area: graphics-and-signals/keyframing-and-deformation
level: core
summary: Morph between two images by warping each toward the other with weighted line-segment correspondences and cross-dissolving the warped images.
model: real-ram
complexity:
  vars: {n: "the number of pixels of a frame", L: "the number of line pairs"}
  time: {worst: "Θ(n L)"}
  space: {extra: "Θ(n)"}
properties: {deterministic: true, exact: true, online: false, recursive: false}
prereqs: [image-warping, bilinear-interpolation]
see_also: [as-rigid-as-possible-shape-interpolation, alpha-blending, bilinear-filtering, texture-mapping, keyframe-interpolation, principles-of-animation]
sources:
  - paper: doi:10.1145/133994.134003
    title: "Thaddeus Beier and Shawn Neely, Feature-based image metamorphosis, SIGGRAPH 92, Computer Graphics 26(2), 35-42, 1992"
    locator: "Section 3.2 (one line pair, equations 1 to 3), Section 3.3 (several line pairs and the weights), Section 3.4 (the morph), Section 3.5 (the cost) and Section 4 (ghosts and other problems)"
  - book: isbn:9780124158429
    title: "Rick Parent, Computer Animation, Algorithms and Techniques, 3rd edition, Morgan Kaufmann, 2012"
    locator: "Chapter 4, Section 4.5 (morphing in 2D, with the feature-based method)"
---

Beier-Neely morphing turns one image into another over a sequence of frames, so that matching features, such as the eyes and the mouth of two faces, move and change shape smoothly instead of fading.
The animator draws pairs of matching line segments on the two images.
Each frame interpolates the line segments, warps both images so that their lines move to the interpolated positions, and cross-dissolves the two warped images.
The warp of each pixel is a weighted average of the maps that each line pair defines on its own, so the whole image moves, not only the pixels on the lines.
Thaddeus Beier and Shawn Neely (1992) published the method, which they also call field morphing.

## In plain words

Fading one picture into another shows two half-bright pictures on top of each other.
A morph also moves the shapes.
You draw short lines on the first picture, say along the nose and the eyebrows, and the matching lines on the second picture.
Halfway through the morph, the lines are halfway between their two positions.
Each picture is then bent so that its lines sit on the halfway lines, and the rest of the picture follows the nearest lines most.
The two bent pictures are then mixed.
At the start you see only the first picture, at the end only the second, and in between the features slide from one place to the other.

## The problem

The input is two images $I_0$ and $I_1$ of the same size, $L$ pairs of line segments, $(P^0_i, Q^0_i)$ in $I_0$ and $(P^1_i, Q^1_i)$ in $I_1$, a time $t \in [0, 1]$, and three weight parameters $a > 0$, $b$ and $p$.
The output is the frame $M_t$ of the morph, an image of the same size.
The frame must equal $I_0$ at $t = 0$ and $I_1$ at $t = 1$, and the feature that a line marks must be on the interpolated line at time $t$.
The warp is a reverse map, as in [image warping](/image-warping/): for each pixel $X$ of the output, it computes the point $X'$ of the input image to read, which leaves no holes in the output.

## The algorithm

For a vector $d = (d_x, d_y)$, $\operatorname{perp}(d) = (-d_y, d_x)$ is $d$ turned by 90 degrees.
WARP-POINT takes a destination point $X$, the destination lines $(P_i, Q_i)$ and the source lines $(P'_i, Q'_i)$, and returns the source point $X'$.

```pseudo id=main
WARP-POINT(X, (Pᵢ, Qᵢ), (P'ᵢ, Q'ᵢ), a, b, p)     ▷ destination X to source X'
L1  D ← 0; W ← 0
L2  for each line pair i do
L3      u ← (X - Pᵢ) · (Qᵢ - Pᵢ) / |Qᵢ - Pᵢ|²
L4      v ← (X - Pᵢ) · perp(Qᵢ - Pᵢ) / |Qᵢ - Pᵢ|
L5      Xᵢ' ← P'ᵢ + u (Q'ᵢ - P'ᵢ) + v perp(Q'ᵢ - P'ᵢ) / |Q'ᵢ - P'ᵢ|
L6      dist ← |X - Pᵢ| if u ≤ 0, |X - Qᵢ| if u ≥ 1, |v| otherwise
L7      w ← (|Qᵢ - Pᵢ|ᵖ / (a + dist))ᵇ
L8      D ← D + w (Xᵢ' - X); W ← W + w
L9  return X + D / W
MORPH(I₀, I₁, L⁰, L¹, t)
L10 Lᵗ ← the lines with the endpoints (1 - t) L⁰ + t L¹
L11 for each pixel X do
L12     X₀ ← WARP-POINT(X, Lᵗ, L⁰); X₁ ← WARP-POINT(X, Lᵗ, L¹)
L13     Mₜ(X) ← (1 - t) I₀(X₀) + t I₁(X₁)
L14 return Mₜ
```

Line L3 gives the position of $X$ along the destination line, 0 at $P_i$ and 1 at $Q_i$.
Line L4 gives the signed distance of $X$ from the line, in pixels.
Line L5 puts the point with the same coordinates next to the source line: the position along the line is a fraction of the line, but the distance across the line is kept in pixels.
Line L6 is the distance from $X$ to the segment, and line L7 makes the weight large for long lines and for lines near $X$.
Line L9 averages the displacements.
In line L13, $I_k(X_k)$ is read with [bilinear interpolation](/bilinear-interpolation/), because $X_k$ is not a pixel center in general.

The parameters control the field.
A small $a$ gives precise control: as $a \to 0$, a pixel on a line follows that line exactly.
The exponent $b$ sets how fast the weight falls with the distance; Beier and Neely found the range $[0.5, 2]$ most useful.
The exponent $p \in [0, 1]$ sets how much more a long line counts than a short one; with $p = 0$ all lines count the same.

## Example

**One line.** Let the destination line be $P = (0, 0)$, $Q = (10, 0)$, and the source line $P' = (2, 1)$, $Q' = (2, 21)$, which is turned by 90 degrees and twice as long.
For $X = (5, 3)$, line L3 gives $u = 50/100 = 0.5$ and line L4 gives $v = (5, 3)\cdot(0, 10)/10 = 3$.
Line L5 gives $X' = (2, 1) + 0.5\,(0, 20) + 3\,(-20, 0)/20 = (-1, 11)$.
The point is 5 pixels along the destination line and 10 pixels along the source line, but it is 3 pixels from both lines.
One line pair therefore gives a rotation, a translation and a scale along the line only.

**Two lines.** Take the destination lines from $(0, 0)$ to $(10, 0)$ and from $(0, 10)$ to $(10, 10)$. The matching source lines are the first line itself and the line from $(0, 12)$ to $(10, 12)$, which is moved up by 2.
For $X = (5, 3)$, the first pair gives the displacement $(0, 0)$ at the distance 3, and the second gives $(0, 2)$ at the distance 7.
With $a = 1$, $b = 2$ and $p = 0$, the weights are $1/16$ and $1/64$, so $X' = (5, 3 + 2 \cdot \frac{1/64}{5/64}) = (5, 3.4)$.
With $b = 1$, the weights are $1/4$ and $1/8$, and $X' = (5, 3.667)$: a smaller $b$ lets the far line count more.

**A moving bar.** Let $I_0$ have a bright vertical bar at the column $x = 2$ and $I_1$ the same bar at $x = 8$, each marked by one vertical line along the bar.
At $t = 0.5$ the interpolated line is at $x = 5$, both warps move their bar there, and $M_{0.5}$ has one full-bright bar at $x = 5$.
A plain cross-dissolve at $t = 0.5$ instead shows two half-bright bars, at $x = 2$ and at $x = 8$.

## Correctness

At $t = 0$, line L10 gives $L^t = L^0$, and the warp of $I_0$ from $L^0$ to itself is the identity: for each line, L5 rebuilds $X$ from its coordinates $u$ and $v$, so every displacement in line L8 is 0.
The weight of $I_1$ in line L13 is 0, so $M_0 = I_0$; in the same way $M_1 = I_1$.

For one line pair, lines L3 to L5 write $X$ in the orthogonal frame of the destination line, with the unit vector across the line, and rebuild it in the frame of the source line, with the coordinate along the line scaled by $|Q' - P'|/|Q - P|$.
So the map is a rotation, a translation and a scale along the line, and it takes $P$ to $P'$ and $Q$ to $Q'$.

If all line pairs are related by the same rigid motion, each $X'_i$ of line L5 is that motion applied to $X$, and so is their weighted average.
A point on the segment $i$ has $\text{dist} = 0$, so as $a \to 0$ its weight grows without bound and the result tends to $X'_i$, the matching point on the source segment.
The [proof](proofs/correctness.md) gives the details.

The method has no guarantee that the warp is one-to-one.
With several lines, the averaged field can fold over itself, and a pixel of the source can then appear twice in the output.

## Complexity

WARP-POINT costs $\Theta(L)$, a fixed amount of arithmetic per line pair.
A frame calls it twice per pixel, so it costs $\Theta(nL)$ for $n$ pixels, plus $\Theta(n)$ for the bilinear reads and the dissolve.
The output frame needs $\Theta(n)$ memory.
Beier and Neely report that the cost is proportional to the product of the number of lines and the number of pixels, and that a frame of 720 by 486 pixels with 100 lines took about 2 minutes on an SGI 4D25.
Each pixel is independent of the others, so the method runs well in parallel, as on a GPU.

## Properties

- **Ends are exact.** The first frame is $I_0$ and the last frame is $I_1$.
- **Global control.** Every line affects every pixel, with a weight that falls with the distance. There is no mesh and no triangulation.
- **Not one-to-one.** The field can fold or tear, mainly where lines are close and point in different directions.
- **Reverse mapping.** Every output pixel gets a value, so there are no holes.
- **Linear in $t$ only for the lines.** The endpoints move linearly, but a pixel between lines need not move on a straight path or at a constant speed.
- **Symmetric.** Both images are warped to the same intermediate lines, so swapping the images and replacing $t$ by $1 - t$ gives the same frame.

## Variants and improvements

- **Interpolating center, orientation and length.** Interpolating the endpoints of a line that turns shortens it in the middle of the morph. Interpolating the center, the angle and the length of each line keeps the length and turns the line, as Beier and Neely suggest.
- **Mesh warping.** A grid of control points on each image, interpolated with splines, gives a warp that is cheaper per pixel and easier to keep one-to-one, but the grid is harder to draw.
- **Triangulated warps.** A [Delaunay triangulation](/delaunay-triangulation/) of matching feature points gives a piecewise affine warp, one affine map per triangle, which is fast on graphics hardware.
- **Scattered data interpolation.** Radial basis functions or thin plate splines on matching points give a smooth global field, like the field of the lines.
- **Separate timing.** The warp and the dissolve can use different curves of $t$, for example an ease curve for the motion and a later dissolve, or a different time for each region of the image.
- **Shape interpolation.** For the outlines of shapes, [as-rigid-as-possible shape interpolation](/as-rigid-as-possible-shape-interpolation/) interpolates a triangulation of the shape and avoids the shrinking of linear paths.

## When to use it

Use Beier-Neely morphing to turn one photograph or drawing into another when the features can be marked by a few lines, such as faces, animals or objects of similar shape.
It is easy for an artist to control, because each line says where one feature goes.
For a warp that must be one-to-one, or for many correspondences, mesh or triangle warps are safer and faster.
For the shape of an object in an animation, with no image, use a shape interpolation method instead.

## Pitfalls

- **Ghosts.** If the lines do not mark a feature well, parts of both images show in the same frame at different places. Add lines near the ghosts.
- **Folds.** Lines that are close together and point in different directions make the field fold over, which shows features twice. Keep lines apart or make $b$ larger.
- **Too few lines.** One line pair can only rotate, translate and stretch along the line. A uniform scale or a shear needs several lines.
- **A tiny $a$.** With $a$ near 0, the weight of a line is very large next to it, and the field can change abruptly close to the lines.
- **Different image content.** The dissolve mixes colors, so features that exist in only one image fade in or out, whatever the lines do.
- **Edges of the image.** The warp can ask for source points outside the image. Clamp them, as the implementation does, or pad the image.

## Implementations

## History

Beier and Neely developed the method at Pacific Data Images and published it at SIGGRAPH 92.
It became widely known through the morphing of faces in the music video for "Black or White" (1991).
Earlier morphs, such as the effects in the film Willow (1988), used mesh warping, with a grid of control points on each image.
The field of line segments made the correspondence easier to specify, at a higher cost per pixel.

## References
