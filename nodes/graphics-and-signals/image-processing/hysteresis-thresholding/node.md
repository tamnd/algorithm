---
tag: 97HN4Z
kind: algorithm
slug: hysteresis-thresholding
name: Hysteresis thresholding
aliases:
- double thresholding
area: graphics-and-signals/image-processing
level: advanced
summary: Threshold an edge strength image with two thresholds. Keep each strong pixel, and keep each weak pixel only if a path of weak pixels connects it to a strong one, as in Canny.
solves: [edge-detection]
model: word-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels}
  time: {worst: Θ(W H), best: Θ(W H)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, exact: true, linear: false, in_place: false}
history:
  year: 1986
  people: [John Canny]
  note: Canny used two thresholds and connectivity to link edge points in his 1986 edge detector, to break fewer edge contours than one threshold does.
prereqs: [connected-components, flood-fill, image-thresholding]
see_also: [canny-edge-detector, non-maximum-suppression, connected-component-labeling, otsu-thresholding, breadth-first-search, depth-first-search, union-find-connectivity]
sources:
  - paper: doi:10.1109/TPAMI.1986.4767851
    title: John Canny, A computational approach to edge detection, IEEE Transactions on Pattern Analysis and Machine Intelligence 8(6), 679 to 698, 1986
    locator: the part on thresholding with hysteresis (two thresholds, and contour segments that are followed while the response stays above the low threshold)
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Section 10.2, the subsection The Canny Edge Detector (hysteresis thresholding with a low and a high threshold, and the connectivity analysis)
  - book: isbn:9780132611084
    title: Emanuele Trucco and Alessandro Verri, Introductory Techniques for 3-D Computer Vision, Prentice Hall, 1998
    locator: Chapter 4, Image Features, the section on the Canny edge detector (the procedure for hysteresis thresholding)
---

Hysteresis thresholding turns an edge strength image into an edge mask with two thresholds, a high one and a low one. A pixel at or above the high threshold is a strong pixel and is always an edge. A pixel between the two thresholds is a weak pixel, and it is an edge only if a path of weak or strong pixels connects it to a strong pixel. So an edge contour can fall below the high threshold for a part of its length without a break, while isolated weak responses, which are often noise, go. It is the last step of [Canny's detector](/canny-edge-detector/), after [non-maximum suppression](/non-maximum-suppression/). The search is a [flood fill](/flood-fill/) from the strong pixels, and it costs time linear in the number of pixels.

## In plain words

One threshold forces a bad choice. A high threshold breaks real edges into short pieces where they get faint. A low threshold keeps the real edges, but also many small spots of noise. Hysteresis uses both. Each very bright pixel is sure to be an edge. A pixel that is only a little bright is kept only if it touches a chain of bright pixels that leads to a sure one. You start at each sure pixel and spread out along the chain, the way paint spreads, and you stop where the brightness drops below the low threshold. Noise spots that do not touch a sure pixel are never reached.

## The problem

The input is an image $s$ of edge strengths with $H$ rows and $W$ columns, for example the gradient magnitudes left by [non-maximum suppression](/non-maximum-suppression/), and two thresholds $t_\ell \le t_h$. Pixel $(x, y)$ holds $s(x, y)$, with $x$ to the right and $y$ downward. A pixel $p$ is a *candidate* if $s(p) \ge t_\ell$ and *strong* if $s(p) \ge t_h$. Two pixels are *neighbors* if they differ by at most 1 in each coordinate, the 8-neighborhood. The output is the mask $E$ of the candidates that a path of candidates, each a neighbor of the next, connects to a strong pixel. Equivalently, $E$ is the union of the connected components of the candidate pixels that hold at least one strong pixel, as in [connected components](/connected-components/) of the grid graph.

## The algorithm

```pseudo id=main
HYSTERESIS(s, t_ℓ, t_h)                     ▷ E starts as all false, S is an empty stack
L1  for each pixel p do
L2      if s(p) ≥ t_h then E(p) ← true; push p on S
L3  while S is not empty do
L4      p ← pop S
L5      for each of the 8 neighbors q of p inside the image do
L6          if not E(q) and s(q) ≥ t_ℓ then
L7              E(q) ← true; push q on S
L8  return E
```

Lines L1 and L2 are a plain threshold at $t_h$ that also fills the stack. Lines L3 to L7 are a [depth-first](/depth-first-search/) flood fill with many sources. A queue in place of the stack gives a [breadth-first search](/breadth-first-search/) and the same mask. The mark $E(q)$ is set when $q$ is pushed, not when it is popped, so no pixel is on the stack two times.

## Example

Take $t_\ell = 4$, $t_h = 8$ and the image with 5 rows and 6 columns

$$s = \begin{pmatrix} 0 & 3 & 0 & 0 & 0 & 0 \\ 0 & 0 & 4 & 9 & 0 & 0 \\ 0 & 0 & 0 & 0 & 5 & 0 \\ 4 & 0 & 0 & 0 & 0 & 4 \\ 5 & 0 & 3 & 0 & 0 & 0 \end{pmatrix}.$$

The only strong pixel is $(3, 1)$ with the value 9. Lines L1 and L2 mark it and push it. Popping it, line L5 finds the candidates $(2, 1)$ with 4 and $(4, 2)$ with 5 among its neighbors, and line L7 marks both. Popping $(4, 2)$ finds the candidate $(5, 3)$ with 4, a diagonal neighbor. Popping $(5, 3)$ and $(2, 1)$ finds nothing new. The pixel $(1, 0)$ with 3 is a neighbor of $(2, 1)$, but it is below $t_\ell$. The pixels $(0, 3)$ and $(0, 4)$ are candidates, but no path of candidates joins them to a strong pixel, so they stay unmarked. The output is $\{(2, 1), (3, 1), (4, 2), (5, 3)\}$, a chain of 4 pixels. A single threshold at 8 keeps only $(3, 1)$, and a single threshold at 4 also keeps the two pixels in the corner.

## Correctness

The [proof](proofs/correctness.md) shows that the algorithm marks a pixel exactly when it is a candidate that a path of candidates joins to a strong pixel. Every marked pixel is a candidate with such a path, by induction on the order of marking: line L2 marks strong pixels, and line L7 marks a candidate neighbor of a pixel that is already marked. For the other direction, every pushed pixel is popped and has all its neighbors examined, so along each path of candidates from a strong pixel each pixel is marked in turn. The stack holds each pixel at most once, so the loop stops.

## Complexity

Each pixel is pushed at most once, because line L7 marks a pixel at the time it is pushed and line L6 skips marked pixels. Each pop examines 8 neighbors. So lines L3 to L7 do at most $8 W H$ neighbor tests, and lines L1 and L2 do $W H$ comparisons. The time is $\Theta(W H)$ in the worst case and in the best case. The mask is $W H$ bits and the stack holds at most $W H$ pixels, so the extra space is $\Theta(W H)$ in the worst case. Most edge maps have few candidates, and then the stack stays small.

## Properties

- **Between the two thresholds.** Every strong pixel is in $E$, and every pixel of $E$ is a candidate. So $E$ contains the threshold at $t_h$ and is contained in the threshold at $t_\ell$.
- **Equal thresholds.** With $t_\ell = t_h$, every candidate is strong, and $E$ is the plain threshold.
- **Monotone.** Raising $t_\ell$ or $t_h$ can only remove pixels from $E$. Raising a strength value can only add pixels.
- **Order independent.** The mask does not depend on the scan order or on the use of a stack or a queue, because it is a property of the components.
- **Not local.** One strong pixel can keep a weak chain of any length. So the result at a pixel can depend on pixels far away, unlike a plain threshold.
- **Exact.** The algorithm only compares values, so it has no rounding error. In Canny's detector, compare squared magnitudes with squared thresholds to keep integer inputs exact.

## Variants and improvements

- **Union-find.** Label the components of the candidates with a [union-find](/union-find-connectivity/) pass in scan order, as in [connected component labeling](/connected-component-labeling/), mark each label that holds a strong pixel, and keep the pixels with a marked label. This needs two passes but no stack, which suits hardware and stream processing.
- **4-connectivity.** With 4 neighbors, a diagonal chain breaks into pieces. Most edge detectors use 8 neighbors, because thinned edges are often only 8-connected.
- **Thresholds from the image.** Canny suggested a ratio of 2 to 1 or 3 to 1 between the thresholds. A common rule takes $t_h$ at a high percentile of the strengths and $t_\ell$ as a fixed fraction of $t_h$. [Otsu's method](/otsu-thresholding/) on the strengths is another choice.
- **Contour following.** Canny's own version follows each contour from a strong pixel and stops when the strength falls below $t_\ell$. This also gives the pixels in order along the contour.
- **Other uses.** The same rule with two thresholds removes noise in segmentation masks and in detections over time, for example in the tracking of a signal that must rise above one level to start and fall below a lower level to stop.

## When to use it

Use hysteresis thresholding after [non-maximum suppression](/non-maximum-suppression/) when you need connected edge contours and one threshold gives either broken edges or too much noise. It is also useful on any score image, such as a probability map of a segmentation, where you trust high values, and you trust lower values only next to high ones. If the output must not depend on pixels far away, for example in tiles processed separately, use a plain threshold, or let the tiles overlap.

## Pitfalls

- **Marking at pop time.** If the mark is set when a pixel is popped, a pixel can be pushed by each of its 8 neighbors before it is popped, and the stack grows by up to 8 times.
- **Recursion.** A recursive flood fill can recurse $W H$ levels deep on a long contour, which is more than the default stack of many languages. Use an explicit stack.
- **4 against 8 neighbors.** Edges that are thinned by suppression are often only 8-connected. With 4 neighbors, hysteresis breaks them at every diagonal step.
- **Thresholds on squared values.** If the strength is the squared magnitude, square the thresholds too.
- **Long false chains.** One strong noise pixel next to a weak texture can keep a large region of weak pixels. Raising $t_\ell$ is the usual fix.

## Implementations

## History

John Canny introduced thresholding with hysteresis in edge detection in his 1986 paper on edge detection, which grew out of his master's thesis at MIT in 1983. He found that one threshold breaks edge contours where the response fluctuates about the threshold, a problem he called streaking, and he used a high threshold to start a contour and a low one to continue it. The name comes from the hysteresis of magnetic materials and of electronic circuits such as the Schmitt trigger, where the level to switch on is higher than the level to switch off.

## References
