---
tag: K93XA7
kind: algorithm
slug: shi-tomasi-corner-detector
name: Shi-Tomasi corner detector
aliases:
- good features to track
- minimum eigenvalue corner detector
area: computer-vision/local-features
level: core
summary: Score each pixel by the smaller eigenvalue of its structure tensor and keep strong local maxima a minimum distance apart, the points a translation tracker follows well.
solves: [corner-detection]
model: real-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, r: the radius of the window, K: the number of candidate pixels, N: the largest number of corners to return}
  time: {worst: O(W H r + K log K + K N), average: O(W H r + K log K + K N), best: O(W H r)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, exact: true, rotation_invariant_response: true, scale_invariant: false, heuristic: false}
history:
  year: 1994
  people: [Jianbo Shi, Carlo Tomasi]
  note: Shi and Tomasi derived the criterion from the conditions under which a window can be tracked, in their 1994 CVPR paper Good features to track.
prereqs: [harris-corner-detector, eigenvalue]
see_also: [moravec-corner-detector, fast-corner-detector, kanade-lucas-tomasi-tracker, lucas-kanade-method, non-maximum-suppression, positive-definite-matrix, feature-detection, harris-laplace-detector]
sources:
  - paper: doi:10.1109/CVPR.1994.323794
    title: Jianbo Shi and Carlo Tomasi, Good features to track, IEEE Conference on Computer Vision and Pattern Recognition, 1994, pages 593-600
    locator: the section on feature selection (a window is accepted when the smaller eigenvalue of the 2 x 2 gradient matrix is above a threshold)
  - paper: doi:10.5244/C.2.23
    title: Chris Harris and Mike Stephens, A combined corner and edge detector, Proceedings of the Alvey Vision Conference 1988, Manchester
    locator: the section Corner/edge response function (the matrix M and the response det M - k tr^2 M)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 7, Section 7.1.1, Feature detectors (the smaller eigenvalue as a corner measure)
  - paper: doi:10.1561/0600000017
    title: Tinne Tuytelaars and Krystian Mikolajczyk, Local invariant feature detectors, a survey, Foundations and Trends in Computer Graphics and Vision 3(3), 177-280, 2008
    locator: the part on corner detectors
---

The Shi-Tomasi corner detector, also called good features to track or the minimum eigenvalue corner detector, solves [corner detection](/corner-detection/). It builds the same $2 \times 2$ structure tensor $M$ as the [Harris corner detector](/harris-corner-detector/), but it scores each pixel by the smaller [eigenvalue](/eigenvalue/) $\lambda_{\min}$ of $M$ instead of by $\det M - k (\operatorname{tr} M)^2$. The smaller eigenvalue is the smallest change of the window over all unit shifts, so it is large exactly when the window changes in every direction. The [Moravec detector](/moravec-corner-detector/) took this minimum over four shifts only. The usual selection keeps the local maxima of $\lambda_{\min}$ above a fraction of the largest value and accepts them, strongest first, when they are at least a given distance from the points already accepted. The cost is $O(WHr)$ for the response plus a sort of the candidates. Shi and Tomasi chose this score in 1994 because it is the condition under which the [Lucas-Kanade](/lucas-kanade-method/) translation tracker can solve for the motion of the window.

## In plain words

Look at the slopes of the brightness inside a small window around a pixel. Collect them in a small table that tells, for each direction, how much the window changes when it moves in that direction. On a flat area it changes in no direction. On an edge it changes across the edge but not along it. On a corner it changes in every direction. The Shi-Tomasi score is the change in the weakest direction. It is near zero on flat areas and on edges, and large only on corners and spots. To pick the final points, keep the pixels that score higher than their neighbours and higher than a fraction of the best score. Then take them from the strongest down, and skip any point that is too close to a point you already took.

## The problem

The input is a gray [digital image](/digital-image/) $I$ with $W$ columns and $H$ rows. A pixel has integer coordinates $(u, v)$: $u$ is the column and goes right, $v$ is the row and goes down. A read outside the image takes the nearest edge pixel (the clamp rule). The parameters are a quality fraction $q$ with $0 \le q \le 1$, a minimum distance $d \ge 0$, a largest number of corners $N \ge 1$, and a window $w$ of radius $r$.

With the gradients $X = \partial I / \partial u$ and $Y = \partial I / \partial v$, the structure tensor at a pixel is

$$M = \begin{pmatrix} A & C \\ C & B \end{pmatrix}, \qquad A = \sum w X^2, \quad B = \sum w Y^2, \quad C = \sum w XY,$$

where each sum runs over the window. For a small shift $s = (a, b)$, the weighted sum of squared changes of the window is about $s^{\mathsf T} M s$. $M$ is symmetric and [positive semidefinite](/positive-definite-matrix/), so its eigenvalues are real and at least $0$. The response is the smaller one,

$$\lambda_{\min} = \frac{A + B}{2} - \sqrt{\Big(\frac{A - B}{2}\Big)^2 + C^2} = \min_{\|s\| = 1} s^{\mathsf T} M s .$$

The output is a list of pixels: the candidates are the pixels with $\lambda_{\min} > q \lambda_{\max}^{\ast}$, where $\lambda_{\max}^{\ast}$ is the largest response in the image, that are not smaller than any of their eight neighbours inside the image. The output takes the candidates in order of decreasing response, ties in order of $v$ and then $u$, and keeps a candidate when it is at least $d$ from every kept point and fewer than $N$ points are kept. This selection rule is not in the paper, which only sets a threshold on $\lambda_{\min}$, but it is the rule most libraries use, for example the OpenCV function goodFeaturesToTrack.

## The algorithm

```pseudo id=main
SHI-TOMASI(I, q, d, N, w)             ▷ I is W × H, w is a window of radius r
L1  X ← I(u + 1, v) - I(u - 1, v);  Y ← I(u, v + 1) - I(u, v - 1)     ▷ at each pixel, clamp border
L2  A ← w ∗ X²;  B ← w ∗ Y²;  C ← w ∗ X Y                             ▷ separable window, clamp border
L3  for each pixel: λ(u, v) ← (A + B)/2 - sqrt(((A - B)/2)² + C²)
L4  λmax ← the largest λ(u, v)
L5  P ← the pixels with λ > q λmax and λ ≥ λ at each of their 8 neighbours inside the image
L6  sort P by λ, largest first, ties by v and then u
L7  kept ← empty list
L8  for each p in P in order do
L9      if |kept| < N and ‖p - p'‖ ≥ d for each p' in kept then
L10         append p to kept
L11 return kept
```

Lines L1 and L2 are the first lines of the Harris detector: central differences, not divided by 2, and a window sum. This page uses the binomial weights $(1, 2, 1)$ in each direction for $r = 1$, a small integer approximation of a [Gaussian](/gaussian-filter/) window. Line L3 is the closed form of the smaller eigenvalue of a symmetric $2 \times 2$ matrix. Line L5 is a [non-maximum suppression](/non-maximum-suppression/) with a test that is not strict, so a flat top of equal values gives several candidates; line L9 then removes those that are too close. Lines L8 to L10 are a greedy pass: a point is never removed once it is kept.

For an integer image, $A$, $B$ and $C$ are integers and $2\lambda = s - \sqrt{D}$ with the integers $s = A + B$ and $D = (A - B)^2 + 4C^2$. The implementation keeps the pair $(s, D)$ and compares two values $p_1 - \sqrt{n_1}$ and $p_2 - \sqrt{n_2}$ exactly, by isolating one root and squaring with attention to the signs. So the order, the ties and the test $\lambda > q \lambda_{\max}$ for a rational $q$ do not depend on rounding. A floating point version is the same algorithm and gives the same output except on near ties.

## Example

Take the $8 \times 8$ image with $0$ everywhere except a block of $9$s at $u \ge 4$ and $v \ge 4$, with $r = 1$. The table compares the Shi-Tomasi response with the Harris response $R = AB - C^2 - k(A + B)^2$ for $k = 0.04$:

| pixel | kind | $A$ | $B$ | $C$ | $\lambda_{\min}$ | Harris $R$ |
|---|---|---|---|---|---|---|
| $(4, 4)$ | corner | 729 | 729 | 324 | 405 | 341434.44 |
| $(3, 4)$ | beside the corner | 729 | 243 | 162 | 193.95 | 113111.64 |
| $(3, 3)$ | outside the corner | 243 | 243 | 81 | 162 | 43040.16 |
| $(6, 4)$ | on the top edge | 0 | 972 | 0 | 0 | -37791.36 |
| $(1, 1)$ | flat | 0 | 0 | 0 | 0 | 0 |

At $(4, 4)$, $A = B$, so $\lambda_{\min} = 729 - 324 = 405$. On the edge pixel the gradient is vertical only, so $A = C = 0$ and the smaller eigenvalue is $0$: the score does not separate an edge from a flat area, while the Harris score is negative on the edge. The response is $0$ everywhere except at the nine pixels with $3 \le u, v \le 5$, and the only local maximum is $(4, 4)$. With $q = 1/100$ the output is $[(4, 4)]$.

For the selection, take a $12 \times 12$ image with a square of $9$s at $3 \le u, v \le 8$. Its four corners $(3, 3)$, $(8, 3)$, $(3, 8)$ and $(8, 8)$ all have $\lambda_{\min} = 405$, so the tie rule orders them by $v$ and then $u$. With $d = 3$ all four are kept. With $d = 3$ and $N = 2$ the output is $[(3, 3), (8, 3)]$. With $d = 6$ the output is $[(3, 3), (8, 8)]$: the points $(8, 3)$ and $(3, 8)$ are $5$ from $(3, 3)$, and $(8, 8)$ is $5\sqrt{2} \approx 7.07$ from it. With $q = 1$ the output is empty, because no pixel is strictly larger than the largest value.

## Correctness

Two facts make the score right. First, for a symmetric $M$ the minimum of $s^{\mathsf T} M s$ over unit vectors $s$ is the smaller eigenvalue, which is the formula of line L3. So $\lambda_{\min}$ is the smallest change of the window, to first order, over all directions of motion, and it is large only when every direction changes the window. Second, the Lucas-Kanade tracker finds the shift $s$ of a window by solving $M s = e$. Shi and Tomasi point out that this system is well conditioned and above the image noise when both eigenvalues are large, and since $\lambda_{\max} \ge \lambda_{\min}$ it is enough to ask that $\lambda_{\min}$ is large.

The algorithm returns exactly the list defined in The problem: lines L4 and L5 build the candidate set, line L6 fixes the order, and the greedy loop keeps a candidate exactly when it passes the distance and count tests at its turn. The proof of both parts, and of the exact comparison of the implementation, is in [proofs/correctness.md](proofs/correctness.md).

## Complexity

The model is the real RAM with a square root. Let $K$ be the number of candidates of line L5.

- Lines L1 to L3 cost $O(WHr)$ with a separable window, as for the Harris detector.
- Lines L4 and L5 cost $O(WH)$.
- Line L6 costs $O(K \log K)$.
- Each candidate at line L9 is compared with at most $N$ kept points, so lines L8 to L10 cost $O(KN)$. A grid of cells of side $d$ makes each test $O(1)$ on average, since only nearby cells can hold a point closer than $d$.
- The tables take $\Theta(WH)$ extra space.

The total is $O(WHr + K \log K + KN)$, and $O(WHr)$ when there are few candidates. The exact comparison of the implementation squares integers of at most twice the size of $D$, so it costs $O(1)$ word operations for 8-bit images and small windows.

## Properties

- **Isotropic response.** $\lambda_{\min}$ is an eigenvalue, so a rotation of the gradients does not change it. On the pixel grid this holds exactly for rotations by $90°$ and approximately for other angles.
- **Zero on edges.** On an ideal straight edge, $M$ has rank one and $\lambda_{\min} = 0$. Unlike the Harris response, the score does not go negative on edges, so a pixel on an edge and a flat pixel score the same.
- **Contrast.** An offset does not change $M$. A gain $g$ multiplies $M$ and so $\lambda_{\min}$ by $g^2$. The relative threshold $q \lambda_{\max}$ and the order are therefore unchanged by a gain, unlike a fixed threshold.
- **Not scale invariant.** The window and the derivatives have one fixed size. The [Harris-Laplace detector](/harris-laplace-detector/) adds a scale search.
- **Spread of points.** The minimum distance rule spreads the points over the image, which is what a tracker or a pose estimator needs.

## Variants and improvements

- **Harris response.** $\det M - k (\operatorname{tr} M)^2 = \lambda_1 \lambda_2 - k (\lambda_1 + \lambda_2)^2$ avoids the square root and penalizes edges more. See the [Harris corner detector](/harris-corner-detector/).
- **Other combinations of the eigenvalues.** The harmonic mean $\det M / \operatorname{tr} M$ and the ratio $\lambda_{\min} / \lambda_{\max}$ are other common scores.
- **Feature monitoring.** The 1994 paper also checks each tracked feature over time: it fits an affine model of the window between the first frame and the current one and drops the feature when the residual grows. This is part of the [Kanade-Lucas-Tomasi tracker](/kanade-lucas-tomasi-tracker/).
- **Scales.** Run the detector on each level of a [Gaussian pyramid](/gaussian-pyramid/) for a tracker that works coarse to fine.
- **Speed.** [FAST](/fast-corner-detector/) finds candidates with a few comparisons per pixel; ORB then ranks them by the Harris score.

## When to use it

Use it to choose the points for a translation tracker, as in the KLT tracker or in optical flow at sparse points, and whenever the points must be well spread over the image. It is a good default corner detector for frames of video at one scale. For matching between images with different scales or viewpoints, use a scale invariant detector such as the [DoG detector](/difference-of-gaussians-detector/) or Harris-Laplace.

## Pitfalls

- **Quality of 1.** The test $\lambda > q \lambda_{\max}$ is strict, so $q = 1$ returns nothing. A value of about $0.01$ to $0.1$ is common.
- **Flat images.** If the image is flat, $\lambda_{\max} = 0$ and nothing passes; a version that divides by $\lambda_{\max}$ to get a relative score divides by zero.
- **Cancellation.** For $A \approx B$ and small $C$, the subtraction in line L3 loses digits in floating point. The form $\lambda_{\min} = \det M / \lambda_{\max}$ with $\lambda_{\max} = (A + B)/2 + \sqrt{\cdots}$ avoids it.
- **Greedy order matters.** The distance rule depends on the order of the candidates. Two runs that break ties in different ways can return different points; fix the tie rule if results must repeat.
- **Edges near the border.** The clamp rule gives a zero gradient across the image border, so a bright object that touches the border can give corners at the border.

## Implementations

## History

Jianbo Shi and Carlo Tomasi presented the criterion at CVPR in 1994 in the paper Good features to track. Earlier work selected points by interest operators such as Moravec's or by the Harris response, which were defined without reference to a tracker. Shi and Tomasi instead asked which windows the tracker can follow and derived the condition on the smaller eigenvalue of the gradient matrix. The criterion became part of the KLT tracker and is the default corner detector of many vision libraries.

## References
