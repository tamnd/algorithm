---
tag: 2J26Q3
kind: technique
slug: linear-filtering
name: Linear filtering
aliases:
- 2D convolution filtering
- image convolution
area: graphics-and-signals/image-processing
level: intro
summary: Compute each output pixel as a weighted sum of neighbors given by a kernel.
prereqs: [digital-image, discrete-convolution]
see_also: [separable-filter, box-blur, gaussian-filter, unsharp-masking, sobel-operator, convolution-via-fft, digital-filtering, cross-correlation]
sources:
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Section 3.4, Fundamentals of Spatial Filtering (correlation and convolution, and padding at the border)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Section 3.2, Linear filtering (correlation, convolution, padding modes and separable filtering)
  - book: isbn:9780131988422
    title: Alan V. Oppenheim and Ronald W. Schafer, Discrete-Time Signal Processing, third edition, Pearson, 2010
    locator: Chapter 2, Discrete-Time Signals and Systems (linear shift invariant systems and convolution)
---

Linear filtering computes each output pixel as a fixed weighted sum of the input pixels around it. The weights form a small array, the kernel or mask $K[u][v]$ for offsets $|u|, |v| \le R$, and the output is $g(x, y) = \sum_{u, v} K[u][v]\, \tilde f(x + u, y + v)$, where $\tilde f$ is the image extended past its border by a chosen border rule. This form is correlation; [convolution](/convolution/) flips the kernel, $\sum K[u][v]\, \tilde f(x - u, y - v)$, and the two agree for symmetric kernels. With different kernels the same loop blurs, sharpens, differentiates and matches templates. Direct evaluation costs $\Theta(WHk^2)$ for a $k \times k$ kernel, $k = 2R + 1$; [separable kernels](/separable-filter/), running sums and the [FFT](/convolution-via-fft/) make it faster. The theory of 1D signals and of recursive filters belongs to [digital filtering](/digital-filtering/); this page is about the 2D sliding window on images.

## In plain words

Lay a small grid of numbers over the picture, centered on one pixel. Multiply each number by the pixel under it, add up the products, and write the sum as the new value of the center pixel. Then slide the grid to the next pixel and do it again, always reading the old picture.

The small grid decides what the filter does. Equal numbers that add up to one give a blur. A large center with negative numbers around it gives sharpening. Negative numbers on one side and positive on the other measure how fast the brightness changes, which finds edges. Near the edge of the picture part of the grid hangs outside, so we must decide what values to pretend are there.

## When it applies

Use linear filtering when the wanted operation is linear and the same at every place in the image: when the output for a sum of two images is the sum of the outputs, and moving the input moves the output. Every operation with these two properties is a convolution with some kernel, the impulse response, which is why the technique covers so many tasks: [smoothing](/image-smoothing/) with a [box](/box-blur/) or a [Gaussian](/gaussian-filter/), [sharpening](/image-sharpening/) by [unsharp masking](/unsharp-masking/), gradient estimation with the [Sobel operator](/sobel-operator/), the [Laplacian of Gaussian](/laplacian-of-gaussian/), and template matching by [cross-correlation](/cross-correlation/). It does not apply when the weights must depend on the image values; the [median filter](/median-filter/), the [bilateral filter](/bilateral-filter/) and [anisotropic diffusion](/anisotropic-diffusion/) are not linear.

## The template

The border rule is a map $\mathrm{ext}(i, n)$ from an index to a pixel index of an axis of length $n$, or to "no pixel". The usual rules are zero (no pixel outside, read as 0), clamp (the nearest edge pixel), mirror (reflect with the edge pixel repeated, $-1 \mapsto 0$, $-2 \mapsto 1$), and wrap ($i \bmod n$). The extended image is $\tilde f(i, j) = f[\mathrm{ext}(j, H)][\mathrm{ext}(i, W)]$, with the value 0 when either index has no pixel.

```pseudo id=main
LINEAR-FILTER(f, K, R, ext)
L1  for y ← 0 to H − 1 do
L2      for x ← 0 to W − 1 do
L3          s ← 0
L4          for v ← −R to R do
L5              for u ← −R to R do
L6                  s ← s + K[u][v] · f̃(x + u, y + v)       ▷ f̃ uses ext
L7          g[y][x] ← s
L8  return g
```

Lines L1 and L2 visit every output pixel. Lines L4 to L6 form the weighted sum over the window, reading the extended input through the border rule. The output goes into a new image $g$, so every sum reads only old values. For convolution, replace line L6 by $s \leftarrow s + K[u][v] \cdot \tilde f(x - u, y - v)$, or flip the kernel once before the loops. A color image is filtered channel by channel with the same kernel.

The cost is $(2R+1)^2$ multiply-adds per pixel, $\Theta(WHk^2)$ in total. Three standard ways reduce it. A kernel of rank one is an outer product and runs as two 1D passes in $\Theta(WHk)$, the [separable filter](/separable-filter/). A box kernel runs with running sums or an [integral image](/integral-image/) in $\Theta(WH)$. A large kernel runs by the [FFT](/convolution-via-fft/) in $\Theta(WH \log(WH))$, which computes the wrap rule; padding the image first gives the other rules.

## Classic examples

- **[Box blur](/box-blur/).** All weights $1/k^2$: the plainest smoothing filter, in $\Theta(WH)$ with running sums.
- **[Gaussian filter](/gaussian-filter/).** Weights $e^{-(u^2+v^2)/(2\sigma^2)}$, normalized: smoothing without the ringing of the box, and separable.
- **[Unsharp masking](/unsharp-masking/).** The kernel $(1+\lambda)\delta - \lambda K$ for a blur $K$: sharpening by boosting the detail.
- **[Sobel operator](/sobel-operator/).** The kernel $[1, 2, 1]^{\mathsf T} [-1, 0, 1]$ and its transpose: the gradient for [edge detection](/edge-detection/).
- **Laplacian.** The 5-point kernel with $-4$ at the center and $1$ at the four neighbors; with a Gaussian before it, the [Laplacian of Gaussian](/laplacian-of-gaussian/).
- **Template matching.** Correlation of the image with a small template, usually normalized, as in [normalized cross-correlation](/normalized-cross-correlation/).
- **Pyramids and resampling.** Smoothing with a small binomial kernel before taking every second pixel builds a [Gaussian pyramid](/gaussian-pyramid/), and [image resampling](/image-resampling/) is linear filtering at fractional positions.

## Variations

- **Correlation and convolution.** For the 3 by 3 image with rows $(1, 2, 3)$, $(4, 5, 6)$, $(7, 8, 9)$ and the kernel with a single 1 at the offset $u = +1$, $v = 0$, correlation gives 6 at the center pixel, the value to the right, and convolution gives 4, the value to the left. Convolution is associative and commutative, so two filters in a row are one filter with the convolved kernel; correlation is not associative.
- **Border rules.** Zero padding darkens the border of a blur; clamp and mirror keep constants; wrap is what the FFT computes and gives exact shift invariance on the torus. Two more rules avoid extension: "valid" output, only where the window fits, which shrinks the image by $2R$ in each direction, and the cut window, which drops the outside pixels and divides by the sum of the weights that remain.
- **Even kernels.** A kernel of even size, such as $[1, 1]/2$, has no center pixel; its output lies at half-pixel positions, and using it as if it were centered shifts the image by half a pixel.
- **Normalized convolution.** With a mask $m$ of valid pixels, $\big(K * (m f)\big) / \big(K * m\big)$ filters only the valid pixels, as the cut window does at the border.
- **Integer kernels.** Kernels with integer weights and a power of two as divisor, such as $[1, 2, 1]/4$, run exactly in integer arithmetic with one shift at the end.
- **Steerable and multiscale banks.** A set of kernels, such as Gaussian derivatives in several directions and scales, filters the image into many channels at once, the input of texture analysis and of convolutional networks.

## Pitfalls

- **Flipping by accident.** A gradient kernel used by a correlation routine where a convolution was meant gives the gradient with the wrong sign. Know which one the library computes; most image libraries compute correlation and call it filtering.
- **In place.** Writing $g$ into $f$ inside the loops makes later sums read filtered values. Keep a separate output.
- **Border rule left unstated.** Different rules give different results within $R$ pixels of the border, and zero padding darkens it. Choose the rule and say which one.
- **Overflow and rounding.** Sums of 8-bit pixels with large weights overflow 8 or 16 bits, and kernels with negative weights give negative values. Accumulate in a wider signed type and round or clip once, at the end.
- **Kernels that do not sum to 1.** A blur kernel whose weights sum to more or less than 1 makes the image brighter or darker. Normalize after rounding the weights, or let the weights of a derivative kernel sum to 0 as they should.

## Exercises

1. Show that correlation with $K$ equals convolution with the flipped kernel $K'[u][v] = K[-u][-v]$, and that the two agree for every image exactly when $K' = K$.
2. Under the wrap rule, show that filtering commutes with cyclic shifts of the image and that filtering with $K_1$ and then $K_2$ equals filtering with $K_1 * K_2$. Find a 1D image of 3 pixels and two kernels for which this fails under the zero rule.
3. Prove that a constant image stays constant under clamp, mirror and wrap if and only if the weights sum to 1. What happens under the zero rule?
4. Write the mirror rule with the edge pixel repeated as a closed formula for any integer index $i$ and length $n$, using the period $2n$. Do the same for the rule without the repeated edge pixel, of period $2n - 2$.
5. For a $512 \times 512$ image, compare the multiply-adds of direct filtering with $k = 3, 15, 63$ and the cost of an FFT of size $1024 \times 1024$ with padding, counting about $5N \log_2 N$ operations for an FFT of $N$ points. Where is the crossover?
6. Apply the 5-point Laplacian to the image with rows $(1, 2, 3)$, $(4, 5, 6)$, $(7, 8, 9)$ under the clamp rule, and explain why the result is 0 at the center but not at the corners.

## References
