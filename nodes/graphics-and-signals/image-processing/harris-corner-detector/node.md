---
tag: 824PAC
kind: algorithm
slug: harris-corner-detector
name: Harris corner detector
aliases:
- Harris-Stephens corner detector
area: graphics-and-signals/image-processing
level: advanced
summary: Mark corners at the local maxima of det M minus k times the squared trace of M, where M sums the products of the image gradients over a small window.
solves: [corner-detection]
model: real-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, r: the radius of the window}
  time: {worst: O(W H r), average: O(W H r), best: O(W H r)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, exact: true, rotation_invariant_response: true, scale_invariant: false, heuristic: false}
history:
  year: 1988
  people: [Chris Harris, Mike Stephens]
  note: Harris and Stephens presented the detector at the fourth Alvey Vision Conference in Manchester, as a fix of the 1980 interest operator of Moravec.
prereqs: [corner-detection, eigenvalue, gaussian-filter]
see_also: [feature-detection, non-maximum-suppression, sobel-operator, edge-detection, canny-edge-detector, sift, lucas-kanade-method, image-pyramid]
sources:
  - paper: doi:10.5244/C.2.23
    title: Chris Harris and Mike Stephens, A combined corner and edge detector, Proceedings of the Alvey Vision Conference 1988, Manchester
    locator: the sections Moravec revisited and Corner/edge response function (pages 147-151 of the printed proceedings, 23.1-23.6 in the online record)
  - paper: doi:10.1109/CVPR.1994.323794
    title: Jianbo Shi and Carlo Tomasi, Good features to track, IEEE Conference on Computer Vision and Pattern Recognition, 1994
    locator: the whole paper (the minimum eigenvalue criterion)
  - paper: doi:10.1023/B:VISI.0000027790.02288.f2
    title: Krystian Mikolajczyk and Cordelia Schmid, Scale and affine invariant interest point detectors, International Journal of Computer Vision 60(1), 2004
    locator: the whole paper (the Harris-Laplace and Harris-affine detectors)
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Section 12.6, The Harris-Stephens corner detector
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 7, Feature detection and matching, Section 7.1 Points and patches
---

The Harris corner detector, also called the Harris-Stephens detector, solves [corner detection](/corner-detection/). At each pixel it sums the products of the image gradients over a small window into a $2 \times 2$ matrix $M$, the structure tensor. Its two [eigenvalues](/eigenvalue/) tell how much the image changes when the window moves in its most and its least changing direction. The detector scores each pixel by $R = \det M - k(\operatorname{tr} M)^2$, which is large and positive only when both eigenvalues are large, and it marks the local maxima of $R$ as corners. It needs no eigenvalue computation and no square root. The cost is $O(WHr)$ for a $W \times H$ image and a window of radius $r$, so linear in the number of pixels for a fixed window. Chris Harris and Mike Stephens published it in 1988 to fix the defects of the detector of Moravec. The response does not change under a rotation of the image, but it changes with the scale, so the detector is not scale invariant.

## In plain words

Put a small window on an image and move it a little. On a flat area the content under the window does not change. On an edge it changes when you move across the edge, but not along it. On a corner it changes in every direction. The Harris detector measures this without moving the window. It looks at how fast the brightness changes to the right and downward at each pixel of the window, and it collects these slopes in a small table of four numbers. From that table it computes one score per pixel. The score is high on corners, negative on edges and near zero on flat areas. A corner is a pixel whose score is above a threshold and higher than at the eight pixels around it.

## The problem

The input is a gray [digital image](/digital-image/) $I$ with $W$ columns and $H$ rows, one channel. Pixel $(x, y)$ has its center at the integer point $(x, y)$, with $x$ to the right and $y$ down. The values can be in any range, as integers or reals, linear or gamma encoded; the method uses them as they are, and a change of encoding changes the gradients and so the corners. The border rule is clamp: a read outside the image takes the nearest edge pixel. The output is a set of corner pixels. Corner detection is a problem without one correct answer (see the [problem page](/corner-detection/)), so "corner" here means the points the response below selects.

Moravec measured the change of the window content for a shift $(u, v)$ by $E(u, v) = \sum_{i,j} w(i, j) \, (I(x + i + u, y + j + v) - I(x + i, y + j))^2$. Harris and Stephens expand $I$ to first order, $I(x + i + u, y + j + v) - I(x + i, y + j) \approx uX + vY$ with the gradients $X = \partial I/\partial x$ and $Y = \partial I/\partial y$, which gives

$$E(u, v) \approx (u, v) \, M \begin{pmatrix} u \\ v \end{pmatrix}, \qquad M = \begin{pmatrix} A & C \\ C & B \end{pmatrix}, \quad A = \sum w X^2, \; B = \sum w Y^2, \; C = \sum w XY.$$

$M$ is symmetric and [positive semidefinite](/positive-definite-matrix/), with eigenvalues $\lambda_1 \ge \lambda_2 \ge 0$. Both small means a flat area, one large and one small means an edge, both large means a corner. The response

$$R = \det M - k (\operatorname{tr} M)^2 = AB - C^2 - k(A + B)^2 = \lambda_1 \lambda_2 - k(\lambda_1 + \lambda_2)^2$$

encodes this test without computing the eigenvalues. The paper leaves $k$ open. Values from $0.04$ to $0.06$ are a common choice in practice; this page uses $k = 1/25 = 0.04$.

## The algorithm

```pseudo id=main
HARRIS(I, k, τ, w)                    ▷ I is W × H, w is a window of radius r, τ ≥ 0
L1  X ← I(x + 1, y) − I(x − 1, y);  Y ← I(x, y + 1) − I(x, y − 1)     ▷ at each pixel, clamp border
L2  P ← X²;  Q ← Y²;  S ← X Y                                         ▷ at each pixel
L3  A ← w ∗ P;  B ← w ∗ Q;  C ← w ∗ S                                 ▷ separable window, clamp border
L4  for each pixel (x, y) do
L5      R(x, y) ← A B − C² − k (A + B)²
L6  corners ← ∅
L7  for each pixel (x, y) with R(x, y) > τ do
L8      if R(x, y) > R(x', y') for each of the 8 neighbours (x', y') inside the image then
L9          add (x, y) to corners
L10 return corners
```

Line L1 takes central differences. They are not divided by 2, so the values stay integers; the factor 2 multiplies every $R$ by $2^4$ and does not move a corner when the threshold is $0$. A [Sobel](/sobel-operator/) or derivative of Gaussian filter is a common replacement. Line L2 forms the three products per pixel. Line L3 sums them over the window. Harris and Stephens use a [Gaussian](/gaussian-filter/) window to make the response smooth and isotropic; this page uses the binomial weights $(1, 2, 1)$ in each direction for $r = 1$, which is a small integer approximation of a Gaussian and is [separable](/separable-filter/). Lines L4 and L5 compute the response. Lines L6 to L10 keep the strict local maxima above $\tau$, which is a simple form of [non-maximum suppression](/non-maximum-suppression/).

## Example

Take the $5 \times 5$ image with $0$ everywhere except the block of $9$s at $2 \le x \le 4$ and $2 \le y \le 4$. Its top-left corner is at $(2, 2)$, and the block runs to the right and bottom edges of the image.

| $y$ \ $x$ | 0 | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 0 | 0 | 0 |
| 2 | 0 | 0 | 9 | 9 | 9 |
| 3 | 0 | 0 | 9 | 9 | 9 |
| 4 | 0 | 0 | 9 | 9 | 9 |

Line L1 gives $X = 9$ at $x \in \{1, 2\}$ and $y \in \{2, 3, 4\}$, and $X = 0$ elsewhere. For example $X(1, 2) = I(2, 2) - I(0, 2) = 9$, and $X(4, 2) = I(4, 2) - I(3, 2) = 0$ because the clamp reads $I(4, 2)$ for $x = 5$. In the same way $Y = 9$ at $y \in \{1, 2\}$ and $x \in \{2, 3, 4\}$. Line L3 with the weights $(1, 2, 1)$ then gives, at three pixels:

| pixel | kind | $A$ | $B$ | $C$ | $R$ with $k = 1/25$ |
|---|---|---|---|---|---|
| $(2, 2)$ | corner | 729 | 729 | 324 | $8535861/25 \approx 341434$ |
| $(4, 1)$ | edge | 0 | 972 | 0 | $-944784/25 \approx -37791$ |
| $(4, 4)$ | flat | 0 | 0 | 0 | 0 |

At $(2, 2)$ the sum $A$ has $X^2 = 81$ at the window pixels with $x \in \{1, 2\}$ and $y \in \{2, 3\}$, with weights $1 + 2$ in $x$ and $2 + 1$ in $y$, so $A = 81 \cdot 3 \cdot 3 = 729$. Only the center has $X$ and $Y$ both nonzero, so $C = 81 \cdot 2 \cdot 2 = 324$. The eigenvalues of $M$ are $729 \pm 324$, that is $1053$ and $405$; both are large, and $R = 729^2 - 324^2 - (1458^2)/25 > 0$. At $(4, 1)$, on the top edge of the block, only $Y$ is nonzero, so $M$ has eigenvalues $972$ and $0$, and $R = -k \cdot 972^2 < 0$. At $(4, 4)$ the clamp makes both gradients zero. Lines L7 to L9 with $\tau = 0$ keep exactly one corner, $(2, 2)$.

On a $12 \times 12$ image with a $6 \times 6$ square of value $10$ at $3 \le x, y \le 8$, the detector returns the four corners $(3, 3)$, $(8, 3)$, $(3, 8)$ and $(8, 8)$. The response is $R(3, 3) = 520400$ at a corner, $R(5, 3) = -57600$ on the middle of the top edge and $0$ at the center $(5, 5)$. Moravec's measure on the same image, with a $3 \times 3$ window and the eight unit shifts, gives the minima $200$ at the corner, $0$ on the edge (the shift along the edge does not change anything) and $0$ in the flat center, so it also separates the three cases on this image. Its faults show on noisy edges and on edges at angles that are not multiples of $45°$, which this image does not have.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It shows three things. First, lines L1 to L5 compute $R = AB - C^2 - k(A + B)^2$ with $A$, $B$, $C$ the windowed sums of the definition, and $R = \lambda_1\lambda_2 - k(\lambda_1 + \lambda_2)^2$ for the eigenvalues of $M$. Second, for $0 < k < 1/4$ and $\lambda_1 > 0$ the sign of $R$ depends only on the ratio $t = \lambda_2/\lambda_1$: $R > 0$ exactly when $t > t_0 = \frac{(1 - 2k) - \sqrt{1 - 4k}}{2k}$. For $k = 1/25$ this is $t_0 = (23 - 5\sqrt{21})/2 \approx 0.0436$. So an edge pixel, with $t = 0$, has $R < 0$, and a pixel with two equal nonzero eigenvalues has $R > 0$. Third, lines L6 to L10 return exactly the pixels with $R > \tau$ that are strict maxima over their neighbours inside the image. The proof also shows the invariances listed below.

The detector is correct with respect to its own response. Whether a returned point is a corner in the sense of a person depends on the image, the window and $k$; that part is a model and not a theorem.

## Complexity

- Line L1 and line L2 cost $\Theta(WH)$.
- Line L3 applies a separable window of $2r + 1$ weights in each direction to three tables, so it costs $\Theta(WHr)$. A non-separable window would cost $\Theta(WHr^2)$.
- Lines L4 and L5 cost $\Theta(WH)$, and lines L6 to L10 cost $\Theta(WH)$, with at most 8 comparisons per pixel.

The total is $\Theta(WHr)$ in the worst case, and the same on every input. For a fixed window it is $\Theta(WH)$. The extra space is $\Theta(WH)$ for the gradient and tensor tables. With a box window instead of a Gaussian, an [integral image](/integral-image/) of each product makes line L3 cost $\Theta(WH)$ for any $r$.

With 8-bit pixels and the gradients of line L1, $|X|, |Y| \le 255$. For $r = 1$ the weights sum to $16$, so $A, B \le 16 \cdot 255^2$, and $|R|$ is less than about $1.1 \cdot 10^{12}$. A 64-bit integer holds it. A 32-bit float at that size has a spacing of about $10^5$ between values, which matters for weak corners.

## Properties

- **Gain and offset.** Adding a constant to $I$ does not change any gradient, so it does not change $R$. Multiplying $I$ by $c$ multiplies $R$ by $c^4$. With $\tau = 0$ the corners do not change; with a fixed $\tau > 0$ they do.
- **Rotation.** $\det M$ and $\operatorname{tr} M$ depend only on the eigenvalues, which do not change when the gradient field rotates. On the pixel grid this is exact for rotations by multiples of $90°$ (the tests check it) and approximate for other angles, because the finite differences and the window are not isotropic.
- **Not scale invariant.** The window has a fixed size in pixels. A corner that is sharp at one scale can be round at a larger scale, and a fine texture can give many corners that vanish when the image is reduced.
- **Translation.** Moving the image moves the corners by the same amount, away from the border.
- **Edges.** On a straight edge $\lambda_2 = 0$, so $R = -k\lambda_1^2 < 0$. This is what Harris and Stephens add to Moravec, whose measure is not negative on an edge and can be large on a noisy one.
- **Corner position.** The maximum of $R$ is at a pixel near the true corner, not always on it. The location depends on the window and on the blur of the image.

## Variants and improvements

- **Shi-Tomasi.** Shi and Tomasi (1994) use the smaller eigenvalue $\lambda_2 = \frac{A + B}{2} - \sqrt{\left(\frac{A - B}{2}\right)^2 + C^2}$ as the score. They derive it as the condition for a window that a tracker such as [Lucas-Kanade](/lucas-kanade-method/) can follow. It needs one square root per pixel and no $k$.
- **Multi scale.** Run the detector on each level of an [image pyramid](/image-pyramid/), or with windows and gradient filters of growing scale. Harris-Laplace (Mikolajczyk and Schmid) keeps the points whose normalized [Laplacian of Gaussian](/laplacian-of-gaussian/) is a maximum over scale, and Harris-affine also adapts the window shape.
- **Subpixel position.** Fit a quadratic through $R$ at the maximum and its neighbours and take the vertex.
- **Spread corners over the image.** Keep only the strongest corner in each cell of a grid, or keep a corner only when no stronger corner is within a given radius. This gives a fixed number of corners that are not all on one textured area.
- **Other detectors.** FAST compares the pixels on a circle with the center and needs no gradients; detectors such as [SIFT](/sift/) find blobs over scale instead of corners. A learned detector from a CNN is the other main choice today.

## When to use it

Use the Harris detector to find points that can be found again in a second view of the same scene with small changes of scale: tracking in video, the input of a [Lucas-Kanade](/lucas-kanade-method/) tracker, calibration targets such as chessboards, and the matching of frames taken close together. Use a scale-space detector such as SIFT when the views differ by a large change of scale. Use [edge detection](/edge-detection/) when you want curves rather than points.

## Pitfalls

- **Threshold and contrast.** $R$ grows with $c^4$ under a gain $c$, so a fixed threshold finds many corners in a bright high contrast image and none in a dark one. Use a threshold relative to the largest $R$, or keep the $n$ strongest corners.
- **Scale of the gradient.** Changing the gradient filter, for example from central differences to Sobel, multiplies $R$ by a constant. A threshold tuned for one filter does not fit the other.
- **The value of $k$.** A larger $k$ rejects more edge pixels but also weaker corners. The paper gives no value; $0.04$ to $0.06$ is a habit, not a derived optimum.
- **Border rule.** With zero padding, a bright image has strong corners at its own four corners and edges along its border. Clamp or mirror the border, or ignore a margin of $r + 1$ pixels.
- **Plateaus.** Two neighbours with the same $R$ are both rejected by the strict test at line L8. A non-strict test keeps both. Choose one rule and use it everywhere.
- **Precision.** $R$ is a fourth power of the gradient. In single precision the subtraction $AB - C^2$ loses the digits of weak corners. Use double precision or integers.
- **Noise.** The gradients amplify noise. Blur the image a little before line L1, or use a larger window, at the cost of corner position.

## Implementations

## History

Hans Moravec described an interest operator in his 1980 Stanford thesis on a robot rover: shift a window in eight directions and score a pixel by the smallest change. Chris Harris and Mike Stephens worked at Plessey on tracking features through image sequences to rebuild 3D scenes from a moving camera. At the fourth Alvey Vision Conference in Manchester in 1988 they listed three faults of Moravec's operator: it sees only shifts in eight directions, its square window makes it noisy, and it takes only the minimum of $E$, so it reacts too much to edges. They fixed the first by the expansion with gradients, the second by a Gaussian window and the third by the response $\det M - k(\operatorname{tr} M)^2$. Shi and Tomasi proposed the minimum eigenvalue in 1994, and Mikolajczyk and Schmid made the detector adapt to scale and affine changes in the early 2000s.

## References
