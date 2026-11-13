---
tag: JDAK9Z
kind: algorithm
slug: sobel-operator
name: Sobel operator
aliases:
- Sobel filter
- Sobel-Feldman operator
area: graphics-and-signals/image-processing
level: intro
summary: Estimate the image gradient with two 3x3 integer kernels. Each kernel smooths with [1, 2, 1] along one axis and takes a central difference along the other.
solves: [edge-detection]
model: word-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels}
  time: {worst: Θ(W H), best: Θ(W H)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, linear: true, separable: true, exact: true, integer_only: true, in_place: false}
history:
  year: 1968
  people: [Irwin Sobel, Gary Feldman]
  note: Sobel and Feldman presented the operator in a talk at the Stanford Artificial Intelligence Project in 1968. They did not publish it then. The book of Duda and Hart in 1973 made it widely known.
prereqs: [edge-detection, linear-filtering]
see_also: [prewitt-operator, scharr-operator, roberts-cross-operator, canny-edge-detector, non-maximum-suppression, separable-filter, harris-corner-detector, finite-difference-method]
sources:
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Section 10.2, the subsection Basic Edge Detection (the image gradient, and the Roberts, Prewitt and Sobel kernels)
  - book: isbn:9780471223610
    title: Richard O. Duda and Peter E. Hart, Pattern Classification and Scene Analysis, Wiley, 1973
    locator: Part II, the treatment of gradient operators for edge detection (where the operator is credited to Sobel)
  - paper: "Irwin Sobel, An isotropic 3x3 image gradient operator, a note on the 1968 talk with Gary Feldman, published on ResearchGate in 2014"
    locator: the whole note (the history of the talk, the two kernels and the reason for the weights 1, 2, 1)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Section 7.2, Edges and contours
---

The Sobel operator estimates the gradient of a gray [digital image](/digital-image/) at each pixel with two $3 \times 3$ integer kernels. One kernel takes a central difference along $x$ and smooths with the weights $[1, 2, 1]$ along $y$. The other kernel does the same with the axes changed. It is the most common first step of [edge detection](/edge-detection/), because it is cheap, exact in integer arithmetic and less sensitive to noise than a plain difference. Each kernel is a [separable filter](/separable-filter/), so the operator costs a small constant number of additions per pixel.

## In plain words

To find out if a pixel is on an edge, look at its neighbors. If the pixels on the right are much brighter than the pixels on the left, the brightness changes along the row, and an edge crosses the row there. The Sobel operator measures this change. It adds the three pixels on the right, with the middle one counted two times, and it subtracts the three pixels on the left in the same way. A second measure does the same for the pixels below and above. The two numbers together give the direction in which the brightness grows fastest, and how fast it grows. The middle pixels count more because they are nearest, and this choice makes the result less dependent on the direction of the edge.

## The problem

The input is a gray image $I$ with $H$ rows and $W$ columns. Pixel $(x, y)$ is a point sample at integer coordinates, with $x$ to the right and $y$ downward. There is one channel, with integer values from 0 to 255 that we treat as linear in the light intensity. A read outside the image returns the nearest border pixel (the clamp rule). The output is a pair of integer images $g_x$ and $g_y$ that estimate $8\, \partial I / \partial x$ and $8\, \partial I / \partial y$. This is the gradient step of the [edge detection](/edge-detection/) problem. The page on [edge detection](/edge-detection/) covers the full problem, and [Canny's detector](/canny-edge-detector/) turns the gradient into thin edges.

The operator is the [correlation](/cross-correlation/) of $I$ with the two masks

$$K_x = \begin{pmatrix} -1 & 0 & 1 \\ -2 & 0 & 2 \\ -1 & 0 & 1 \end{pmatrix}, \qquad K_y = \begin{pmatrix} -1 & -2 & -1 \\ 0 & 0 & 0 \\ 1 & 2 & 1 \end{pmatrix},$$

so that $g_x(x, y) = \sum_{u, v} K_x[v][u]\, I(x + u, y + v)$ for $u, v \in \{-1, 0, 1\}$. Each mask is the outer product of a smoothing vector and a difference vector: $K_x = [1, 2, 1]^T [-1, 0, 1]$ and $K_y = [-1, 0, 1]^T [1, 2, 1]$.

## The algorithm

The algorithm uses the separable form. Two passes make the smoothed images, and two more passes take the differences.

```pseudo id=main
SOBEL(I)                                    ▷ I is H × W, reads use the clamp rule
L1  for each pixel (x, y): s(x, y) ← I(x, y − 1) + 2 I(x, y) + I(x, y + 1)
L2  for each pixel (x, y): d(x, y) ← I(x − 1, y) + 2 I(x, y) + I(x + 1, y)
L3  for each pixel (x, y): g_x(x, y) ← s(x + 1, y) − s(x − 1, y)
L4  for each pixel (x, y): g_y(x, y) ← d(x, y + 1) − d(x, y − 1)
L5  return (g_x, g_y)
```

Line L1 smooths each column and line L2 smooths each row. Line L3 takes a central difference of the column smoothed image along $x$, and line L4 takes a central difference of the row smoothed image along $y$. The reads of $s$ and $d$ outside the image also use the clamp rule. The gradient magnitude is $\sqrt{g_x^2 + g_y^2}$, and the gradient direction is $\operatorname{atan2}(g_y, g_x)$. To compare magnitudes exactly, use the integer $g_x^2 + g_y^2$.

## Example

Take this image with 4 rows and 5 columns. A dark region with value 10 meets a bright region with value 80, and the boundary moves one column to the left between rows 1 and 2.

$$I = \begin{pmatrix} 10 & 10 & 10 & 80 & 80 \\ 10 & 10 & 10 & 80 & 80 \\ 10 & 10 & 80 & 80 & 80 \\ 10 & 10 & 80 & 80 & 80 \end{pmatrix}$$

At pixel $(2, 1)$, line L1 gives $s(3, 1) = 80 + 160 + 80 = 320$ and $s(1, 1) = 10 + 20 + 10 = 40$, so $g_x(2, 1) = 280$. Line L2 gives $d(2, 2) = 10 + 160 + 80 = 250$ and $d(2, 0) = 10 + 20 + 80 = 110$, so $g_y(2, 1) = 140$. The full outputs are

$$g_x = \begin{pmatrix} 0 & 0 & 280 & 280 & 0 \\ 0 & 70 & 280 & 210 & 0 \\ 0 & 210 & 280 & 70 & 0 \\ 0 & 280 & 280 & 0 & 0 \end{pmatrix}, \qquad g_y = \begin{pmatrix} 0 & 0 & 0 & 0 & 0 \\ 0 & 70 & 140 & 70 & 0 \\ 0 & 70 & 140 & 70 & 0 \\ 0 & 0 & 0 & 0 & 0 \end{pmatrix}.$$

At $(2, 1)$ the direction is $\operatorname{atan2}(140, 280) \approx 26.6°$, so the gradient points to the right and a little down, toward the bright pixels. A step of height 70 across one column gives $g_x = 4 \cdot 70 = 280$, which is 8 times the slope of 35 per pixel of a central difference. Columns 0 and 4 are 0 because the clamp rule repeats the border column.

## Correctness

The [proof](proofs/correctness.md) shows three facts. First, the separable passes give the same result as the direct correlation with $K_x$ and $K_y$ at every pixel, the border included, because the clamp rule acts on each coordinate on its own. Second, on an affine image $I = a x + b y + c$, and at each pixel whose $3 \times 3$ neighborhood is inside the image, the output is exactly $g_x = 8a$ and $g_y = 8b$. Third, for a smooth image, $g_x / (8h) = I_x + h^2 \left(\tfrac{1}{6} I_{xxx} + \tfrac{1}{4} I_{xyy}\right) + O(h^4)$ for pixel spacing $h$, so the estimate has second order accuracy.

## Complexity

Lines L1 and L2 each do 2 additions and 1 doubling per pixel, and lines L3 and L4 each do 1 subtraction. So the time is $\Theta(W H)$ in the worst case and in the best case, with 6 additions and 2 doublings per pixel. The direct form with two $3 \times 3$ masks does 10 additions and 4 doublings per pixel, so here the separable form saves less than it does for a large kernel. The two temporary images $s$ and $d$ and the two outputs take $\Theta(W H)$ extra space. A streaming form that keeps three rows of $s$ and $d$ needs only $\Theta(W)$ extra space besides the output.

With 8-bit input, $|g_x| \le 4 \cdot 255 = 1020$, so a signed 16-bit integer holds each output, and $g_x^2 + g_y^2 \le 2\,080\,800$ fits in a signed 32-bit integer.

## Properties

- **Exact and integer.** All weights are small integers, so the output has no rounding error. Divide by 8 only when you need the slope in intensity units per pixel.
- **Linear and shift invariant.** The operator is a [linear filter](/linear-filtering/), away from the border.
- **Separable.** Each mask is a smoothing vector times a difference vector, as shown above.
- **A smoothed Roberts gradient.** $K_x$ is the $2 \times 2$ box sum of the $2 \times 2$ difference mask $\begin{pmatrix} -1 & 1 \\ -1 & 1 \end{pmatrix}$. This mask is the [Roberts cross](/roberts-cross-operator/) pair turned by 45 degrees. So the Sobel direction estimate on a plane wave equals the Roberts one: for $I = \cos(\omega_x x + \omega_y y)$, $\tan \hat\theta = \tan(\omega_y / 2) / \tan(\omega_x / 2)$.
- **Direction error.** The formula above gives the largest error of the direction estimate over all directions of a plane wave. At the frequency radius $|\omega| = \pi/8$ the error is 0.19 degrees, at $\pi/4$ it is 0.75 degrees, and at $\pi/2$ it is 3.2 degrees. These values come from the formula, not from measured images. The [Prewitt operator](/prewitt-operator/) has about twice this error, and the [Scharr operator](/scharr-operator/) has much less.
- **Response to a step.** A vertical step of height $A$ between two columns gives $g_x = 4A$ on the two columns next to the step. The response is 2 pixels wide, so a thinning step such as [non-maximum suppression](/non-maximum-suppression/) is needed for thin edges.

## Variants and improvements

- **Scharr weights.** The weights $[3, 10, 3]$ instead of $[1, 2, 1]$ make the direction estimate much more accurate. See the [Scharr operator](/scharr-operator/).
- **Prewitt weights.** The weights $[1, 1, 1]$ give the [Prewitt operator](/prewitt-operator/), which is a little older and less accurate in direction.
- **Larger kernels.** Use binomial smoothing $[1, 4, 6, 4, 1]$ with the derivative $[-1, -2, 0, 2, 1]$ for a $5 \times 5$ Sobel kernel. Larger binomial kernels approach a derivative of Gaussian, which the [Gaussian filter](/gaussian-filter/) and [Canny's detector](/canny-edge-detector/) use with a free scale $\sigma$.
- **Cheaper magnitude.** Some hardware uses $|g_x| + |g_y|$ instead of $\sqrt{g_x^2 + g_y^2}$. This magnitude depends on the direction: it is $\sqrt{2}$ times larger at 45 degrees than at 0 degrees for the same step.
- **Compass kernels.** The masks turned to 8 directions (as in the Kirsch and Robinson operators) give the largest of 8 responses instead of a gradient vector.

## When to use it

Use the Sobel operator when you need a fast gradient image: for an edge map, as the gradient step of [Canny's detector](/canny-edge-detector/), for the [Harris corner detector](/harris-corner-detector/), or for a gradient based [thresholding](/image-thresholding/). Use the [Scharr operator](/scharr-operator/) at the same cost when the gradient direction must be accurate, for example in optical flow or in orientation histograms. Smooth first with a [Gaussian filter](/gaussian-filter/), or use a derivative of Gaussian, when the image has much noise or when the edges you want are wider than 2 or 3 pixels.

## Pitfalls

- **Correlation and convolution.** The masks above are correlation masks. True [convolution](/discrete-convolution/) flips the mask, which changes the sign of $g_x$ and $g_y$. Library documentation often shows the kernel for one form and applies the other, so check the sign on a known step.
- **The direction of the y axis.** With $y$ downward, a positive $g_y$ means that the image is brighter below. With $y$ upward, the sign is the opposite.
- **Overflow.** An unsigned 8-bit output cannot hold $g_x$. Use a signed 16-bit or wider type, and do not clip negative values to 0 before you compute the direction.
- **The factor 8.** The output is 8 times the slope. Thresholds taken from a text that divides by 8 (or by 4) are off by that factor.
- **Gamma encoded input.** Most stored images are gamma encoded, for example in sRGB. The gradient of the encoded values is not the gradient of the light intensity, and dark edges get a larger response than bright edges of the same contrast. Convert to linear values first if the magnitude must be physical.
- **Color images.** Convert to one channel first, or combine the gradients of the channels with a rule such as the largest magnitude. The gradients of the channels can cancel if you add them.
- **The border.** Clamp, mirror and zero padding give different values in the outer row and column. Zero padding makes a false edge along the border of a bright image.

## Implementations

## History

Irwin Sobel and Gary Feldman presented the operator in 1968 in a talk at the Stanford Artificial Intelligence Project, with the title "An isotropic 3x3 image gradient operator". They did not publish a paper. The operator became known through the book of Richard Duda and Peter Hart in 1973, which credits it to Sobel. In 2014 Sobel put a note on the history and the definition online, and the name Sobel-Feldman operator, which credits both authors, is now also in use. The idea of a gradient from small masks is older: Lawrence Roberts used $2 \times 2$ differences in 1963, see the [Roberts cross operator](/roberts-cross-operator/), and Judith Prewitt published the $3 \times 3$ form with equal weights in 1970.

## References
