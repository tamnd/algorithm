---
tag: W69M2W
kind: algorithm
slug: roberts-cross-operator
name: Roberts cross operator
aliases:
- Roberts cross-gradient
area: graphics-and-signals/image-processing
level: intro
summary: Estimate the image gradient from the two diagonal differences of each 2x2 block of pixels. It is the earliest and smallest of the gradient edge operators.
solves: [edge-detection]
model: word-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels}
  time: {worst: Θ(W H), best: Θ(W H)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, linear: true, separable: false, exact: true, integer_only: true, in_place: false}
history:
  year: 1963
  people: [Lawrence G. Roberts]
  note: Roberts used the two diagonal differences in his 1963 MIT PhD thesis Machine perception of three-dimensional solids, to find the edges of blocks in photographs.
prereqs: [edge-detection, linear-filtering]
see_also: [sobel-operator, prewitt-operator, scharr-operator, canny-edge-detector, image-sharpening, cross-correlation, finite-difference-method]
sources:
  - paper: "Lawrence G. Roberts, Machine perception of three-dimensional solids, in James T. Tippett and others (editors), Optical and Electro-Optical Information Processing, MIT Press, 1965, pages 159 to 197"
    locator: the part on the edge operator (the differences along the two diagonals of a 2x2 block, and the magnitude from the two differences)
  - paper: "Lawrence G. Roberts, Machine perception of three-dimensional solids, PhD thesis, Massachusetts Institute of Technology, 1963 (also MIT Lincoln Laboratory Technical Report 315)"
    locator: the chapter on picture input and the edge operator
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Section 10.2, the subsection Basic Edge Detection (the Roberts cross gradient kernels)
---

The Roberts cross operator estimates the gradient of a gray [digital image](/digital-image/) from each $2 \times 2$ block of pixels. It takes the two differences along the diagonals of the block, which cross at the center of the block. Lawrence Roberts used it in 1963 to find the edges of blocks in photographs, and it was the first gradient operator of [edge detection](/edge-detection/). It needs only two subtractions per pixel and gives a thin response to a step. It has no smoothing, so noise has a large effect on it. Its $3 \times 3$ successors, the [Prewitt](/prewitt-operator/) and [Sobel](/sobel-operator/) operators, add smoothing.

## In plain words

Look at a square of four pixels. Compare the top left pixel with the bottom right pixel, and compare the top right pixel with the bottom left pixel. If the square is all the same brightness, both differences are zero. If an edge crosses the square, at least one difference is large. The two diagonal differences together give the direction of the edge and how strong it is. The method is small and fast, and it finds sharp edges well. It does not average over more pixels, so a single noisy pixel can look like an edge.

## The problem

The input is a gray image $I$ with $H$ rows and $W$ columns. Pixel $(x, y)$ is a point sample at integer coordinates, with $x$ to the right and $y$ downward. There is one channel, with integer values from 0 to 255 that we treat as linear. A read outside the image returns the nearest border pixel (the clamp rule). The output is a pair of integer images $g_1$ and $g_2$, the two diagonal differences. Output $(x, y)$ belongs to the point $(x + \tfrac{1}{2}, y + \tfrac{1}{2})$, the center of the block it reads. This is the gradient step of [edge detection](/edge-detection/).

The operator is the [correlation](/cross-correlation/) of $I$ with the two masks

$$R_1 = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}, \qquad R_2 = \begin{pmatrix} 0 & 1 \\ -1 & 0 \end{pmatrix},$$

with the top left entry at offset $(0, 0)$.

## The algorithm

```pseudo id=main
ROBERTS-CROSS(I)                            ▷ I is H × W, reads use the clamp rule
L1  for y ← 0 to H − 1 do
L2      for x ← 0 to W − 1 do
L3          g_1(x, y) ← I(x, y) − I(x + 1, y + 1)
L4          g_2(x, y) ← I(x + 1, y) − I(x, y + 1)
L5  return (g_1, g_2)
```

The magnitude is $\sqrt{g_1^2 + g_2^2}$. To get the gradient along the axes, turn the pair by 45 degrees: $g_x = g_2 - g_1$ and $g_y = -(g_1 + g_2)$. These are 2 times the estimates of $\partial I / \partial x$ and $\partial I / \partial y$ at the center of the block.

## Example

Take the image with 4 rows and 5 columns where a dark region (10) meets a bright region (80), and the boundary moves one column to the left between rows 1 and 2:

$$I = \begin{pmatrix} 10 & 10 & 10 & 80 & 80 \\ 10 & 10 & 10 & 80 & 80 \\ 10 & 10 & 80 & 80 & 80 \\ 10 & 10 & 80 & 80 & 80 \end{pmatrix}.$$

At $(2, 0)$, line L3 gives $g_1 = I(2, 0) - I(3, 1) = 10 - 80 = -70$, and line L4 gives $g_2 = I(3, 0) - I(2, 1) = 80 - 10 = 70$. At $(1, 1)$, the block holds the corner of the bright region: $g_1 = 10 - 80 = -70$ and $g_2 = 10 - 10 = 0$, so $g_x = 70$ and $g_y = 70$, a gradient at 45 degrees. The full outputs are

$$g_1 = \begin{pmatrix} 0 & 0 & -70 & 0 & 0 \\ 0 & -70 & -70 & 0 & 0 \\ 0 & -70 & 0 & 0 & 0 \\ 0 & -70 & 0 & 0 & 0 \end{pmatrix}, \qquad g_2 = \begin{pmatrix} 0 & 0 & 70 & 0 & 0 \\ 0 & 0 & 0 & 0 & 0 \\ 0 & 70 & 0 & 0 & 0 \\ 0 & 70 & 0 & 0 & 0 \end{pmatrix}.$$

The response is one block wide along the boundary. In the last row, the clamp rule makes the block repeat the row, so the operator becomes a horizontal difference there.

## Correctness

The [proof](proofs/correctness.md) shows three facts. On an affine image $I = a x + b y + c$, at each pixel whose block is inside the image, $g_1 = -(a + b)$ and $g_2 = a - b$ exactly, so $g_x = 2a$, $g_y = 2b$ and $g_1^2 + g_2^2 = 2(a^2 + b^2)$. So the magnitude is exact up to the factor $\sqrt{2}$, for every direction of the gradient. For a smooth image with pixel spacing $h$, $g_1$ and $g_2$ are central differences about the center of the block, so $g_x / (2h) = I_x + O(h^2)$ at that center. At the pixel $(x, y)$ itself, the error is $O(h)$, because the center is half a pixel away.

## Complexity

Each pixel costs 2 subtractions, so the time is $\Theta(W H)$ in the worst case and in the best case. The two outputs take $\Theta(W H)$ space. The operator reads only the current row and the next row, so a stream form needs $\Theta(W)$ extra space besides the output. With 8-bit input, $|g_1|, |g_2| \le 255$, so each output fits in a signed 16-bit integer.

## Properties

- **Exact and integer.** The output has no rounding error.
- **Smallest support.** Each output reads 4 pixels, the least that can give both components of a gradient.
- **Thin response.** A vertical step between columns $c$ and $c + 1$ gives a nonzero output only at column $c$, one block wide, located at $x = c + \tfrac{1}{2}$, the true position of the step.
- **Not separable.** The masks are not outer products. The turned pair $g_x = g_2 - g_1$ is the outer product $[1, 1]^T [-1, 1]$.
- **Direction error.** On a plane wave $\cos(\omega_x x + \omega_y y)$, the estimate has $\tan \hat\theta = \tan(\omega_y / 2) / \tan(\omega_x / 2)$, the same as for the [Sobel operator](/sobel-operator/). The largest error is 0.19 degrees at the frequency radius $\pi/8$ and 3.2 degrees at $\pi/2$.
- **No smoothing.** The noise in each output is the noise of two pixels. A $3 \times 3$ operator averages 6 pixels and so reduces the noise more.

## Variants and improvements

- **Sobel as a smoothed Roberts.** The $2 \times 2$ box sum of $g_x = g_2 - g_1$ is exactly the [Sobel](/sobel-operator/) output $g_x$. So the Sobel operator is the Roberts operator after a $2 \times 2$ box smoothing, and it is centered on a pixel instead of a block.
- **Cheap magnitude.** Roberts used the sum of squares and its root. Hardware often uses $|g_1| + |g_2|$ or $\max(|g_1|, |g_2|)$. These forms change with the direction of the edge.
- **A square root of the intensities first.** Accounts of the thesis say that Roberts took the square root of each intensity before the differences. This compresses the bright values, which makes the response depend less on the brightness of the scene.

## When to use it

Use the Roberts cross operator on clean images with sharp edges, when the cost per pixel or the memory must be very small, or when you need the position of a step to half a pixel. It is a good choice to teach the idea of a gradient. For noisy images, use the [Sobel operator](/sobel-operator/) or the [Scharr operator](/scharr-operator/), or smooth first with a [Gaussian filter](/gaussian-filter/).

## Pitfalls

- **The half pixel shift.** The output at $(x, y)$ belongs to $(x + \tfrac{1}{2}, y + \tfrac{1}{2})$. If you combine it with values at the pixels, such as a mask from another operator, the edges move by half a pixel along both axes.
- **Diagonal components.** $g_1$ and $g_2$ are along the diagonals, not along $x$ and $y$. Use $g_x = g_2 - g_1$ and $g_y = -(g_1 + g_2)$ before you compute an angle in the usual frame.
- **Noise.** One wrong pixel gives a full response in up to 4 outputs. Smooth first or use a larger operator when the noise is strong.
- **The last row and column.** With the clamp rule the block of the last row repeats that row, so the operator measures a different thing there.
- **Correlation and convolution.** True [convolution](/discrete-convolution/) flips the masks and so changes the signs.

## Implementations

## History

Lawrence Roberts wrote his PhD thesis "Machine perception of three-dimensional solids" at MIT in 1963, with a version as a Lincoln Laboratory report. It was published in 1965 in the book Optical and Electro-Optical Information Processing. The thesis took a photograph of a scene of polyhedral blocks, found edges with the $2 \times 2$ operator, fitted lines to them, and matched the lines to 3D models. It is often given as the start of computer vision. Judith Prewitt's $3 \times 3$ operator of 1970 and the Sobel operator of 1968 added smoothing to the gradient estimate, see the [Prewitt operator](/prewitt-operator/) and the [Sobel operator](/sobel-operator/).

## References
