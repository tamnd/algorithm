---
tag: S56VW3
kind: algorithm
slug: moravec-corner-detector
name: Moravec corner detector
aliases:
- Moravec interest operator
area: computer-vision/local-features
level: intro
summary: Score each pixel by the smallest sum of squared differences between its window and the window shifted by one pixel in four directions, and keep the local maxima.
solves: [corner-detection]
model: word-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, r: the radius of the window in pixels}
  time: {worst: O(W H r^2), average: O(W H r^2), best: O(W H r^2)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, exact: true, rotation_invariant_response: false, scale_invariant: false, heuristic: true}
history:
  year: 1980
  people: [Hans Moravec]
  note: Moravec described the interest operator in Chapter 5 of his 1980 Stanford thesis on the Stanford Cart, a robot that navigated by stereo vision.
prereqs: [corner-detection, digital-image]
see_also: [harris-corner-detector, shi-tomasi-corner-detector, fast-corner-detector, non-maximum-suppression, integral-image, feature-detection, normalized-cross-correlation]
sources:
  - url: https://frc.ri.cmu.edu/~hpm/project.archive/robot.papers/1975.cart/1980.html.thesis/p05.html
    title: Hans P. Moravec, Obstacle avoidance and navigation in the real world by a seeing robot rover, PhD thesis, Stanford University, 1980 (also Stanford AIM-340 and CMU-RI-TR-80-03)
    locator: Chapter 5, Interest Operator (four directions, the minimum of the four sums, the local maximum over the 25 windows that overlap or touch a window)
  - paper: doi:10.5244/C.2.23
    title: Chris Harris and Mike Stephens, A combined corner and edge detector, Proceedings of the Alvey Vision Conference 1988, Manchester
    locator: the section Moravec revisited (the shifts (1,0), (1,1), (0,1), (-1,1) and the three faults of the operator)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 7, Section 7.1.1, Feature detectors (the auto-correlation function of a patch)
  - paper: doi:10.1561/0600000017
    title: Tinne Tuytelaars and Krystian Mikolajczyk, Local invariant feature detectors, a survey, Foundations and Trends in Computer Graphics and Vision 3(3), 177-280, 2008
    locator: the part on corner detectors (the Harris detector and its origin in the Moravec operator)
---

The Moravec corner detector, also called the Moravec interest operator, is the first widely used method for [corner detection](/corner-detection/). For each pixel it compares a small window with the same window moved by one pixel in four directions, horizontal, vertical and the two diagonals. It sums the squared differences for each direction and takes the smallest of the four sums as the score, so a pixel scores high only when the image changes in every one of the four directions. It keeps the pixels whose score is a local maximum above a threshold. The cost is $O(WHr^2)$ for a $W \times H$ image and a window of radius $r$. The [Harris corner detector](/harris-corner-detector/) replaces the four discrete shifts by a quadratic form in the gradients, and the [Shi-Tomasi detector](/shi-tomasi-corner-detector/) by the smaller eigenvalue of that form; both are fixes of the faults of this operator that are shown below.

## In plain words

Put a small square window on the image and move it one pixel to the right. Add up how much each pixel under the window changed, squared. Do the same for a move down and for the two diagonal moves. On a flat area none of the four moves changes anything. On a straight edge the move along the edge changes nothing, so the smallest of the four totals is zero. Only on a corner or on a spot does every move change the window. So the score of a pixel is the smallest of its four totals. A pixel is a corner if its score is above a threshold and no pixel near it has a higher score. The method is simple and uses only integer additions and products.

## The problem

The input is a gray [digital image](/digital-image/) $I$ with $W$ columns and $H$ rows of integer values. A pixel has integer coordinates $(u, v)$: $u$ is the column and goes right, $v$ is the row and goes down, and the origin is the top left pixel. The window has radius $r$, so it holds $(2r + 1)^2$ pixels. For a shift $(a, b)$ the change of the window at $(u, v)$ is

$$E_{ab}(u, v) = \sum_{j=-r}^{r} \sum_{i=-r}^{r} \big(I(u + i + a, v + j + b) - I(u + i, v + j)\big)^2 .$$

The response is the minimum over four shifts,

$$C(u, v) = \min_{(a, b) \in S} E_{ab}(u, v), \qquad S = \{(1, 0), (0, 1), (1, 1), (1, -1)\}.$$

This page uses no border rule: $C$ is defined only where each read is inside the image, that is for $r + 1 \le u \le W - r - 2$ and $r + 1 \le v \le H - r - 2$. The output is the set of defined pixels with $C > \tau$ that are not smaller than $C$ at any defined pixel within a Chebyshev distance $m$. As for every corner detector, "corner" here means the points that this response selects; the [problem page](/corner-detection/) explains why there is no single correct answer.

Moravec's thesis states the operator as the sum of squares of the differences of adjacent pixels in each of four directions over the window. The shift form above, which Harris and Stephens use when they analyze the operator, counts the same kind of pairs; the two forms differ only in which pairs at the border of the window they include. Some texts use all eight unit shifts. The opposite shift adds nothing new in the limit of a large window, since $E_{-a,-b}(u, v) = E_{ab}(u - a, v - b)$: it is the same sum, taken at the neighbouring pixel.

## The algorithm

```pseudo id=main
MORAVEC(I, r, τ, m)                      ▷ I is W × H with integer values, τ ≥ 0, m ≥ 1
L1  S ← {(1, 0), (0, 1), (1, 1), (1, -1)}
L2  for each pixel (u, v) with r + 1 ≤ u ≤ W - r - 2 and r + 1 ≤ v ≤ H - r - 2 do
L3      C(u, v) ← min over (a, b) ∈ S of E_ab(u, v)
L4  corners ← ∅
L5  for each pixel (u, v) where C is defined and C(u, v) > τ do
L6      if C(u, v) ≥ C(u', v') for each defined (u', v') with |u' - u| ≤ m and |v' - v| ≤ m then
L7          add (u, v) to corners
L8  return corners
```

Line L1 fixes the four directions: right, down, and the two diagonals. Lines L2 and L3 compute the response at every pixel where the shifted window stays inside the image. Each $E_{ab}$ is a sum of $(2r + 1)^2$ squared integer differences. Lines L4 to L7 keep the pixels above the threshold that are local maxima of $C$. The test at line L6 is not strict, so two equal neighbours are both kept. Moravec spaced his windows half a window apart and kept a window when its score was the largest of the 25 windows that overlap or touch it; this page uses every pixel and the neighbourhood of radius $m$, which is the usual dense form.

## Example

Take the $8 \times 8$ image with $0$ everywhere except a block of $9$s at $u \ge 4$ and $v \ge 4$. The block has one corner, at $(4, 4)$, and two edges, along the row $v = 4$ and the column $u = 4$. With $r = 1$, $C$ is defined for $2 \le u, v \le 5$. The four sums at some pixels are:

| pixel | kind | $E_{1,0}$ | $E_{0,1}$ | $E_{1,1}$ | $E_{1,-1}$ | $C$ |
|---|---|---|---|---|---|---|
| $(4, 4)$ | corner | 162 | 162 | 405 | 243 | 162 |
| $(3, 3)$ | next to the corner | 81 | 81 | 243 | 81 | 81 |
| $(5, 4)$ | on the top edge | 0 | 243 | 243 | 243 | 0 |
| $(4, 5)$ | on the left edge | 243 | 0 | 243 | 324 | 0 |

At $(4, 4)$ the window covers $3 \le u, v \le 5$, and four of its pixels are $9$. The shift $(1, 0)$ changes the two pixels $(3, 4)$ and $(3, 5)$ from $0$ to $9$, so $E_{1,0} = 2 \cdot 81 = 162$. At $(5, 4)$ the shift along the edge, $(1, 0)$, changes nothing, so $C = 0$. The full table of $C$ for $2 \le u, v \le 5$ is $0$ except for $C(3, 3) = C(4, 3) = C(3, 4) = 81$ and $C(4, 4) = 162$. With $\tau = 0$ and $m = 1$ the detector returns one corner, $(4, 4)$.

Now take a $10 \times 10$ image with $I = 9$ where $2v \ge u + 3$ and $0$ elsewhere. This is a straight edge with a slope of $1/2$, at about $27°$, which is not one of the four directions. At $(5, 4)$ the sums are $81$, $243$, $162$ and $324$, so $C = 81$. Every pixel of the defined area that touches the edge has $C = 81$, and with $\tau = 0$ and $m = 1$ the detector returns 17 "corners", all on the edge. A vertical edge or an edge at $45°$ gives $C = 0$ everywhere, because one of the four shifts runs along it.

## Correctness

The detector computes exactly the response it defines. Lines L2 and L3 visit each pixel of the defined area once and set $C(u, v)$ to the minimum of the four sums. Lines L5 to L7 add a pixel exactly when it passes the threshold and the neighbourhood test, and no line removes a pixel. So the output is the set described in The problem. The full proof is in [proofs/correctness.md](proofs/correctness.md). It also proves the facts that justify the response:

- $C(u, v) = 0$ when the window lies in a region where $I$ is constant along one of the four directions. So a straight edge along a direction of $S$ gives no response.
- On a window where $I$ is constant, all four sums are $0$.
- An offset $I + c$ gives the same $C$, and a gain $gI$ gives $g^2 C$; with $\tau = 0$ the output does not change.

Whether a returned pixel is a corner for a human is not a theorem. The slanted edge above shows that the operator reports edges at angles between the four directions.

## Complexity

The model is the [word RAM](/word-ram/). Let the pixels be integers of $b$ bits. Each squared difference has at most $2b$ bits, and a sum of $(2r + 1)^2$ of them has at most $2b + 2\lceil \log_2(2r + 1) \rceil$ bits, so it fits in one word for 8-bit images and any window that fits in the image.

- Lines L2 and L3 compute 4 sums of $(2r + 1)^2$ terms at each of at most $WH$ pixels: $O(WHr^2)$ time.
- Lines L5 to L7 compare each pixel with at most $(2m + 1)^2 - 1$ neighbours: $O(WHm^2)$ time, which is $O(WH)$ for a fixed $m$.
- The table $C$ takes $\Theta(WH)$ extra space.

The total is $O(WHr^2)$ for a fixed $m$, in every case. For each shift, the squared differences $(I(p + s) - I(p))^2$ form one image, and a box sum over it can use an [integral image](/integral-image/). Then each $E_{ab}$ costs $O(1)$ per pixel and the whole response costs $O(WH)$ for any $r$.

## Properties

- **Not isotropic.** The response looks only in four directions. An edge at an angle between them gets a positive score, as the example shows. This is the first fault that Harris and Stephens list.
- **Noisy.** The square window weighs all pixels the same, so a pixel that enters or leaves the window changes the score by a jump. Harris and Stephens use a Gaussian window instead.
- **Edges and noise.** The minimum of four sums is large on any pixel where all four shifts change the window, which also happens on noisy edges and on single noisy pixels.
- **Gain and offset.** $C$ does not change under an offset and is multiplied by $g^2$ under a gain $g$. A fixed threshold $\tau > 0$ therefore depends on the contrast.
- **Not scale invariant.** The window and the shift are one pixel in size, so a blurred corner or a corner seen from far away gives a different response.
- **Exact integer arithmetic.** No division and no square root is needed.

## Variants and improvements

- **Harris and Stephens.** Expand $E_{ab}$ to first order in the shift. Then $E(a, b) \approx (a, b) M (a, b)^{\mathsf T}$ with the structure tensor $M$, and every direction is covered at once. This is the [Harris corner detector](/harris-corner-detector/).
- **Smallest eigenvalue.** Take the smallest value of the quadratic form over unit shifts, which is the smaller eigenvalue of $M$. This is the [Shi-Tomasi detector](/shi-tomasi-corner-detector/).
- **Eight shifts.** Take the minimum over the eight unit shifts. By the identity in The problem, this adds the four sums of the neighbours $(u - a, v - b)$, so the response is a little smoother but has the same faults.
- **Sparse windows.** Moravec computed the operator on windows spaced half a window apart, on an image reduced in size, to save time on the computers of his day.
- **Segment tests.** The [FAST detector](/fast-corner-detector/) compares the pixels on a circle with the center and needs no sums of squares.

## When to use it

Use it to teach corner detection, or when only integer additions are available and the edges of interest are horizontal, vertical or diagonal. For any other use, the Harris or Shi-Tomasi detector gives a better response at a similar cost, and FAST is faster on 8-bit images.

## Pitfalls

- **Reads outside the image.** Line L3 reads up to $r + 1$ pixels away from $(u, v)$. A loop over $r \le u \le W - r - 1$, as for a window without a shift, reads outside the image. Use the bounds of line L2, or a border rule.
- **Strict maxima on plateaus.** A test $C(u, v) > C(u', v')$ in place of $\ge$ at line L6 drops both pixels of two equal neighbours. On the corner example both forms return $(4, 4)$, but on symmetric shapes the strict test can return nothing.
- **Threshold zero on slanted edges.** With $\tau = 0$ every pixel on an edge between the four directions passes, as in the example. Choose $\tau$ above the response of the edges you expect, or use a detector with an isotropic response.
- **Overflow.** In 16-bit arithmetic, a $5 \times 5$ window of 8-bit differences can reach $25 \cdot 255^2 = 1625625$, which does not fit. Use 32-bit or 64-bit sums.

## Implementations

## History

Hans Moravec built the interest operator for the Stanford Cart, a small robot that found its way among obstacles by stereo vision. His 1980 Stanford thesis describes it in Chapter 5: the score of a window is the minimum of the four sums of squared differences of adjacent pixels, and a window is a feature when its score is the largest among the 25 windows that overlap or touch it. The cart then matched these features between stereo images with a correlator. In 1988 Chris Harris and Mike Stephens analyzed the operator, listed its three faults (the discrete set of shifts, the binary window and the use of the minimum), and fixed them with the gradient form that became the Harris detector.

## References
