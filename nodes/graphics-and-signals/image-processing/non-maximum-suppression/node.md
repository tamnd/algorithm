---
tag: 9SMADY
kind: algorithm
slug: non-maximum-suppression
name: Non-maximum suppression
aliases:
- edge thinning
area: graphics-and-signals/image-processing
level: advanced
summary: Thin a gradient image to edges one pixel wide. Keep a pixel only if its gradient magnitude is a maximum among its two neighbors along the quantized gradient direction.
solves: [edge-detection]
model: word-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels}
  time: {worst: Θ(W H), best: Θ(W H)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, exact: true, integer_only: true, linear: false, in_place: false}
history:
  year: 1986
  people: [John Canny]
  note: Canny made the suppression of non-maxima along the gradient direction a step of his edge detector in 1986, after his 1983 master's thesis at MIT.
prereqs: [edge-detection, sobel-operator]
see_also: [canny-edge-detector, hysteresis-thresholding, scharr-operator, image-skeletonization, zhang-suen-thinning, corner-detection, harris-corner-detector]
sources:
  - paper: doi:10.1109/TPAMI.1986.4767851
    title: John Canny, A computational approach to edge detection, IEEE Transactions on Pattern Analysis and Machine Intelligence 8(6), 679 to 698, 1986
    locator: the definition of edge points as maxima of the gradient magnitude in the gradient direction, and the implementation of the detector
  - book: isbn:9780132611084
    title: Emanuele Trucco and Alessandro Verri, Introductory Techniques for 3-D Computer Vision, Prentice Hall, 1998
    locator: Chapter 4, Image Features, the section on the Canny edge detector (the procedure for non-maximum suppression with four directions)
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Section 10.2, the subsection The Canny Edge Detector (nonmaxima suppression with four quantized directions)
---

Non-maximum suppression thins a gradient image to edges one pixel wide. At each pixel it looks at the two neighbors along the gradient direction, which is the direction across the edge, and it keeps the pixel only if its gradient magnitude is a maximum among the three. Each [edge detection](/edge-detection/) gradient, such as the output of the [Sobel operator](/sobel-operator/), gives a ridge of large values 2 or more pixels wide across each edge. Non-maximum suppression keeps the top of each ridge. It is the second step of [Canny's detector](/canny-edge-detector/), between the Gaussian gradient and [hysteresis thresholding](/hysteresis-thresholding/). The version here rounds the direction to one of four directions and makes every decision in exact integer arithmetic.

## In plain words

A gradient image shows how fast the brightness changes. Across an edge, the values rise to a peak and fall again, like a ridge on a map. The edge is the line along the top of the ridge. To find it, stand on each pixel and look across the ridge, that is, along the direction of the fastest change. Look at the one neighbor in front of you and the one behind you. If you are higher than both, you are on the top line, and the pixel stays. If not, the pixel is on the side of the ridge, and it goes. The grid has only four directions to look in, so each direction is rounded to the nearest of them.

## The problem

The input is a gradient field, two images $g_x$ and $g_y$ with $H$ rows and $W$ columns, for example from the [Sobel operator](/sobel-operator/) or from a derivative of Gaussian. Pixel $(x, y)$ holds the gradient at the integer point $(x, y)$, with $x$ to the right and $y$ downward. The output is an image that keeps the squared magnitude $m(p) = g_x(p)^2 + g_y(p)^2$ at each pixel $p$ that is a maximum along its gradient direction, and holds 0 at each other pixel. The border pixels have only one neighbor in some directions, so the output is 0 there.

The squared magnitude has the same order as the magnitude, so the decisions are the same, and with integer gradients it needs no square root.

## The algorithm

The direction of $(g_x, g_y)$ is rounded to the nearest of 0, 45, 90 and 135 degrees, modulo 180 degrees. A sector index $k$ gives the step $d_k$ to the neighbor along the gradient: $d_0 = (1, 0)$, $d_1 = (1, 1)$, $d_2 = (0, 1)$ and $d_3 = (-1, 1)$. With $y$ downward, $d_1$ points to the right and down. The rounding uses $\tan 22.5° = \sqrt{2} - 1$. An angle is within 22.5 degrees of the $x$ axis exactly when $|g_y| < (\sqrt{2} - 1)|g_x|$, which is the same as $(|g_x| + |g_y|)^2 < 2 g_x^2$. So SECTOR is:

- $k = 0$ if $(|g_x| + |g_y|)^2 < 2 g_x^2$,
- else $k = 2$ if $(|g_x| + |g_y|)^2 < 2 g_y^2$,
- else $k = 1$ if $g_x g_y > 0$, and $k = 3$ if not.

```pseudo id=main
NON-MAXIMUM-SUPPRESSION(g_x, g_y)           ▷ out starts as all 0
L1  for each pixel p: m(p) ← g_x(p)² + g_y(p)²
L2  for each pixel p = (x, y) with 1 ≤ x ≤ W − 2 and 1 ≤ y ≤ H − 2 do
L3      if m(p) = 0 then continue
L4      d ← d_k with k = SECTOR(g_x(p), g_y(p))
L5      b ← m(p − d), a ← m(p + d)
L6      if m(p) > b and m(p) ≥ a then
L7          out(p) ← m(p)
```

Line L6 is not symmetric: it asks for more than the neighbor behind and at least the neighbor in front. So if two neighbors along $d$ have the same sector and the same magnitude, and together they are a maximum, exactly one of them stays: the one at the smaller position along $d$. With $>$ on both sides, both would be removed, and the edge would get a gap. With $\ge$ on both sides, both would stay.

## Example

**A vertical step.** Take 6 rows of the row $0, 0, 0, 0, 100, 100, 100, 100$, so the step is between columns 3 and 4. The Sobel $g_x$ in each row is $0, 0, 0, 400, 400, 0, 0, 0$ and $g_y = 0$. At column 3, SECTOR gives 0 and $d = (1, 0)$. Line L5 gives $b = m(2) = 0$ and $a = m(4) = 160\,000$, so line L6 holds with $m = a$ and column 3 stays. At column 4, $b = m(3) = 160\,000$ equals $m(4)$, so the strict test fails and column 4 goes. Each interior row keeps exactly column 3.

**A diagonal step.** Take a $12 \times 12$ image with 0 where $x + y < 12$, 50 where $x + y = 12$ and 100 where $x + y > 12$. Along each row, the Sobel gradient is $(g, g)$ with $g = 50, 200, 300, 200, 50$ on the anti-diagonals $x + y = 10, 11, 12, 13, 14$, so the squared magnitudes are $5000$, $80\,000$, $180\,000$, $80\,000$ and $5000$. SECTOR gives 1 and $d = (1, 1)$. But a step of $(1, 1)$ adds 2 to $x + y$. So the pixel on $x + y = 12$ is compared with the lines 10 and 14 and stays. The pixel on $x + y = 11$ is compared with the lines 9 and 13: $80\,000 > 0$ and $80\,000 \ge 80\,000$, so it also stays. The result is a staircase of two pixels per row, a 4-connected line. This is a known limit of the method with four directions, not an error of this implementation.

## Correctness

The [proof](proofs/correctness.md) shows four facts. First, SECTOR returns the nearest of the four directions, modulo 180 degrees, for every gradient that is not exactly at an odd multiple of 22.5 degrees, and integer gradients other than $(0, 0)$ are never at such an angle. Second, a pixel that is a strict maximum along $d$ always stays. Third, two neighbors along $d$ that have the same sector never both stay, which is the single response property along the gradient. Fourth, on a run of equal maxima along $d$, exactly the first pixel stays.

## Complexity

Line L1 does 2 multiplications and 1 addition per pixel. Lines L3 to L7 do a constant number of operations per pixel: the sector test needs a few multiplications and comparisons, and line L6 two comparisons. So the time is $\Theta(W H)$ in the worst case and in the best case. The image $m$ and the output take $\Theta(W H)$ extra space. A stream form that keeps three rows of $m$ needs $\Theta(W)$ besides the output. With Sobel gradients of 8-bit images, $m \le 2\,080\,800$, so 32-bit integers are enough.

## Properties

- **Exact.** With integer gradients, there are no square roots, no arc tangents and no rounding. The sector test of the implementation gives the same answer as rounding $\operatorname{atan2}$ to 45 degrees.
- **Scale invariant.** Multiplying both $g_x$ and $g_y$ by a positive constant does not change the output mask.
- **Not linear.** The output is a selection, not a filter.
- **Local.** Each decision reads 3 pixels of $m$ and one gradient.
- **Thin, but not always one pixel wide.** Along each gradient direction no two neighbors of the same sector both stay. But for edges near 45 degrees the neighbors along $(1, 1)$ skip every other anti-diagonal, so two adjacent anti-diagonals can both stay.

## Variants and improvements

- **Interpolated suppression.** Compare $m(p)$ with the magnitude at the points $p \pm u$, where $u$ is the unit gradient direction, by bilinear interpolation of the magnitudes. This removes the rounding of the direction. It gives a single response on a diagonal edge through pixel centers, but an edge exactly halfway between two anti-diagonals still keeps both. The implementation of [Canny's detector](/canny-edge-detector/) on this site has both forms.
- **Subpixel location.** Fit a parabola through $m(p - d)$, $m(p)$ and $m(p + d)$, and report the position of its vertex. This gives the edge position to a fraction of a pixel.
- **Window suppression.** For keypoints, such as the output of the [Harris corner detector](/harris-corner-detector/), keep a pixel only if it is the maximum of a full $n \times n$ window. Neubeck and Van Gool gave an algorithm for this in 2006 whose cost per pixel does not grow with $n$.
- **Suppression of boxes.** In object detection, non-maximum suppression means a different method: sort the detected boxes by score, keep the best one and remove each box that overlaps it too much, then repeat. It shares only the name with this page.
- **Thinning of binary images.** If the input is a binary edge mask with no gradient, use [skeletonization](/image-skeletonization/), for example [Zhang-Suen thinning](/zhang-suen-thinning/), instead.

## When to use it

Use non-maximum suppression after a gradient operator when you need thin edges, for example before [hysteresis thresholding](/hysteresis-thresholding/), contour following or the [Hough transform](/hough-transform/). The version with four directions is fast and exact. Use the interpolated variant when the edges are at many angles and you need one pixel per edge, or when you want a subpixel position.

## Pitfalls

- **The tie rule.** With $>$ on both sides, a plateau of 2 equal pixels gives no edge at all. With $\ge$ on both sides, both pixels stay. Use the asymmetric test of line L6.
- **The direction of the y axis.** With $y$ downward, the gradient $(1, 1)$ points to the bottom right, so the step $d_1$ is $(1, 1)$. With $y$ upward the diagonal steps change. A wrong sign compares a pixel with neighbors along the edge, not across it, and the result is a dotted edge.
- **Gradient and edge direction.** The step must follow the gradient direction, which is across the edge. The edge itself runs at 90 degrees to it.
- **Threshold before suppression.** Suppress first and threshold later. A threshold first can cut the ridge so that its top pixel has no lower neighbor on one side.
- **Floating point ties.** With floating point gradients, two pixels that should have equal magnitude can differ in the last bit, so which one stays depends on the rounding. Integer gradients avoid this.

## Implementations

## History

John Canny made the search for maxima of the gradient magnitude in the gradient direction a step of his edge detector, in his master's thesis at MIT in 1983 and in his 1986 paper. His criterion of a single response per edge is the reason for the step. The idea of keeping only local maxima of an edge response is older, for example in the work of Azriel Rosenfeld and his group on edge operators at several sizes in the early 1970s. The version with four quantized directions is the one in most textbooks, for example in the book of Trucco and Verri of 1998.

## References
