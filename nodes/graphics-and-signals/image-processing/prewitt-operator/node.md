---
tag: CDGEEG
kind: algorithm
slug: prewitt-operator
name: Prewitt operator
aliases:
- Prewitt filter
area: graphics-and-signals/image-processing
level: intro
summary: Estimate the image gradient with two 3x3 integer kernels that sum three pixels along one axis and take a central difference along the other.
solves: [edge-detection]
model: word-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels}
  time: {worst: Θ(W H), best: Θ(W H)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, linear: true, separable: true, exact: true, integer_only: true, in_place: false}
history:
  year: 1970
  people: [Judith M. S. Prewitt]
  note: Prewitt gave the 3x3 masks in her chapter Object enhancement and extraction, in the 1970 book Picture Processing and Psychopictorics.
prereqs: [edge-detection, linear-filtering]
see_also: [sobel-operator, scharr-operator, roberts-cross-operator, box-blur, separable-filter, least-squares-problem, canny-edge-detector, non-maximum-suppression]
sources:
  - paper: "Judith M. S. Prewitt, Object enhancement and extraction, in Bernard S. Lipkin and Azriel Rosenfeld (editors), Picture Processing and Psychopictorics, Academic Press, 1970, pages 75 to 149"
    locator: the whole chapter (the 3x3 gradient masks with equal weights)
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Section 10.2, the subsection Basic Edge Detection (the Prewitt kernels and their diagonal forms)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Section 7.2, Edges and contours
---

The Prewitt operator estimates the gradient of a gray [digital image](/digital-image/) at each pixel with two $3 \times 3$ integer kernels. One kernel takes a central difference along $x$ and adds the three rows with equal weights. The other does the same with the axes changed. It is the [Sobel operator](/sobel-operator/) with the smoothing $[1, 1, 1]$ instead of $[1, 2, 1]$. Its output is exactly the slope of the [least squares](/least-squares-problem/) plane through the $3 \times 3$ neighborhood, times 6. It is a [separable filter](/separable-filter/) and a simple first step of [edge detection](/edge-detection/).

## In plain words

An edge is a place where the image gets much brighter or darker over a short distance. The Prewitt operator finds such places by a comparison. It adds the three pixels in the column to the right of a pixel, and it subtracts the three pixels in the column to the left. A large result means that the brightness changes from left to right. A second measure does the same with the row below and the row above. Each of the three pixels counts the same, so the operator also averages out a part of the noise. The two measures together give the direction of the fastest change and its size.

## The problem

The input is a gray image $I$ with $H$ rows and $W$ columns. Pixel $(x, y)$ is a point sample at integer coordinates, with $x$ to the right and $y$ downward. There is one channel, with integer values from 0 to 255 that we treat as linear. A read outside the image returns the nearest border pixel (the clamp rule). The output is a pair of integer images $g_x$ and $g_y$ that estimate $6\, \partial I / \partial x$ and $6\, \partial I / \partial y$. This is the gradient step of [edge detection](/edge-detection/).

The operator is the [correlation](/cross-correlation/) of $I$ with

$$P_x = \begin{pmatrix} -1 & 0 & 1 \\ -1 & 0 & 1 \\ -1 & 0 & 1 \end{pmatrix} = [1, 1, 1]^T [-1, 0, 1], \qquad P_y = \begin{pmatrix} -1 & -1 & -1 \\ 0 & 0 & 0 \\ 1 & 1 & 1 \end{pmatrix} = [-1, 0, 1]^T [1, 1, 1].$$

## The algorithm

```pseudo id=main
PREWITT(I)                                  ▷ I is H × W, reads use the clamp rule
L1  for each pixel (x, y): s(x, y) ← I(x, y − 1) + I(x, y) + I(x, y + 1)
L2  for each pixel (x, y): d(x, y) ← I(x − 1, y) + I(x, y) + I(x + 1, y)
L3  for each pixel (x, y): g_x(x, y) ← s(x + 1, y) − s(x − 1, y)
L4  for each pixel (x, y): g_y(x, y) ← d(x, y + 1) − d(x, y − 1)
L5  return (g_x, g_y)
```

Line L1 sums each column over three rows, which is a [box filter](/box-blur/) along $y$. Line L2 sums each row over three columns. Lines L3 and L4 take the central differences. The reads of $s$ and $d$ also use the clamp rule. The magnitude is $\sqrt{g_x^2 + g_y^2}$ and the direction is $\operatorname{atan2}(g_y, g_x)$.

## Example

Take the image with 4 rows and 5 columns where a dark region (10) meets a bright region (80), and the boundary moves one column to the left between rows 1 and 2:

$$I = \begin{pmatrix} 10 & 10 & 10 & 80 & 80 \\ 10 & 10 & 10 & 80 & 80 \\ 10 & 10 & 80 & 80 & 80 \\ 10 & 10 & 80 & 80 & 80 \end{pmatrix}.$$

At pixel $(2, 1)$, line L1 gives $s(3, 1) = 240$ and $s(1, 1) = 30$, so $g_x(2, 1) = 210$. Line L2 gives $d(2, 2) = 170$ and $d(2, 0) = 100$, so $g_y(2, 1) = 70$. The full outputs are

$$g_x = \begin{pmatrix} 0 & 0 & 210 & 210 & 0 \\ 0 & 70 & 210 & 140 & 0 \\ 0 & 140 & 210 & 70 & 0 \\ 0 & 210 & 210 & 0 & 0 \end{pmatrix}, \qquad g_y = \begin{pmatrix} 0 & 0 & 0 & 0 & 0 \\ 0 & 70 & 70 & 70 & 0 \\ 0 & 70 & 70 & 70 & 0 \\ 0 & 0 & 0 & 0 & 0 \end{pmatrix}.$$

At $(2, 1)$ the direction is $\operatorname{atan2}(70, 210) \approx 18.4°$. The [Sobel operator](/sobel-operator/) gives $26.6°$ at the same pixel. The two answers differ because the operators weight the middle row differently, and the edge here is a staircase, not a straight line.

## Correctness

The [proof](proofs/correctness.md) shows four facts. The separable passes equal the direct correlation with $P_x$ and $P_y$ at every pixel, the border included. On an affine image $I = a x + b y + c$, at each pixel whose neighborhood is inside the image, $g_x = 6a$ and $g_y = 6b$ exactly. The value $g_x / 6$ is the slope along $x$ of the plane that fits the 9 pixels of the neighborhood best in the least squares sense. For a smooth image with pixel spacing $h$, $g_x / (6h) = I_x + h^2 (\tfrac{1}{6} I_{xxx} + \tfrac{1}{3} I_{xyy}) + O(h^4)$.

## Complexity

Lines L1 and L2 each do 2 additions per pixel, and lines L3 and L4 each do 1 subtraction. So the time is $\Theta(W H)$ in the worst case and in the best case, with 6 additions and no multiplications per pixel. Because the weights are all 1, a running sum along each column gives line L1 with 2 operations per pixel for any length of the box. The temporary images and the outputs take $\Theta(W H)$ extra space, or $\Theta(W)$ besides the output with a stream of three rows. With 8-bit input, $|g_x| \le 3 \cdot 255 = 765$, so a signed 16-bit integer holds each output.

## Properties

- **Exact and integer.** The output has no rounding error.
- **Linear and separable.** Each mask is a box sum times a central difference.
- **A least squares fit.** The plane $a u + b v + k$ that fits the 9 values $I(x + u, y + v)$ best has $a = g_x / 6$ and $b = g_y / 6$. This is the reason for the equal weights.
- **Direction error.** For a plane wave $\cos(\omega_x x + \omega_y y)$, the operator returns $g_x \propto \sin \omega_x (1 + 2 \cos \omega_y)$ and $g_y \propto \sin \omega_y (1 + 2 \cos \omega_x)$. The largest error of the direction over all directions is 0.37 degrees at the frequency radius $\pi/8$, 1.6 degrees at $\pi/4$ and 7.6 degrees at $\pi/2$. These values come from the formula. They are 2.0 to 2.4 times the errors of the [Sobel operator](/sobel-operator/) and close to those of a plain central difference.
- **Response to a step.** A vertical step of height $A$ between two columns gives $g_x = 3A$ on the two columns next to the step, so the response is 2 pixels wide.

## Variants and improvements

- **Sobel and Scharr weights.** The weights $[1, 2, 1]$ give the [Sobel operator](/sobel-operator/), and $[3, 10, 3]$ give the [Scharr operator](/scharr-operator/). Both are more accurate in direction at the same cost.
- **Diagonal masks.** Masks turned by 45 degrees, such as $\begin{pmatrix} 0 & 1 & 1 \\ -1 & 0 & 1 \\ -1 & -1 & 0 \end{pmatrix}$, respond most to diagonal edges. The 8 turned masks make a compass operator that reports the largest response and its direction.
- **Larger fits.** A least squares plane over a $5 \times 5$ or larger window gives a smoother gradient. Its masks are again a box sum times the weights $u$, so the cost per pixel stays constant with running sums.

## When to use it

Use the Prewitt operator when you need a cheap gradient with no multiplications, or when you want the slope of a local plane fit with a clear statistical meaning. For edge maps where the direction matters, the [Sobel operator](/sobel-operator/) or the [Scharr operator](/scharr-operator/) is better at the same cost. For noisy images, smooth with a [Gaussian filter](/gaussian-filter/) first or use [Canny's detector](/canny-edge-detector/).

## Pitfalls

- **Correlation and convolution.** True [convolution](/discrete-convolution/) flips the masks, so it changes the sign of the output. Check the sign on a known step.
- **The factor 6.** The output is 6 times the slope, not 8 times as with Sobel. Thresholds do not carry over from one operator to the other without this factor.
- **Overflow.** Use a signed type of at least 16 bits for the output.
- **Gamma encoded input.** The gradient of sRGB values is not the gradient of the light intensity. Convert to linear values first when the magnitude must be physical.
- **The border.** The outer row and column depend on the border rule. Zero padding makes a false edge.

## Implementations

## History

Judith Prewitt described the masks in 1970, in her long chapter "Object enhancement and extraction" in the book Picture Processing and Psychopictorics, edited by Bernard Lipkin and Azriel Rosenfeld. The equal weights are exactly those of the least squares fit of a plane to the $3 \times 3$ neighborhood. Lawrence Roberts had used $2 \times 2$ differences in 1963, see the [Roberts cross operator](/roberts-cross-operator/). The [Sobel operator](/sobel-operator/), presented in a talk in 1968, weights the middle row more.

## References
