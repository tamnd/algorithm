---
tag: APW13H
kind: technique
slug: separable-filter
name: Separable filtering
aliases:
- separable convolution
area: graphics-and-signals/image-processing
level: advanced
summary: Factor a 2D kernel into two 1D passes to reduce work from k squared to 2k per pixel.
prereqs: [linear-filtering, singular-value-decomposition]
see_also: [gaussian-filter, box-blur, sobel-operator, laplacian-of-gaussian, integral-image, bicubic-interpolation, image-resampling, discrete-fourier-transform]
sources:
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Section 3.2.1, Separable filtering (rank one kernels and the sum of separable kernels from the SVD)
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Section 3.4, Fundamentals of Spatial Filtering (separable filter kernels and their rank)
  - book: isbn:9781421407944
    title: Gene H. Golub and Charles F. Van Loan, Matrix Computations, fourth edition, Johns Hopkins University Press, 2013
    locator: Section 2.4, The Singular Value Decomposition (the rank and the best low rank approximation)
---

A 2D kernel is separable when it is an outer product, $K[u][v] = a[v]\, b[u]$, a column vector times a row vector. Filtering with it then splits into two 1D passes: filter every row with $b$, then every column of the result with $a$. The cost per pixel drops from $k^2$ multiply-adds to $2k$ for a $k \times k$ kernel, so the whole filter costs $\Theta(WHk)$ in place of $\Theta(WHk^2)$, and it gives exactly the same output as the direct [linear filter](/linear-filtering/) when the border rule acts on each axis separately. A kernel is separable if and only if its matrix has rank one, and the [singular value decomposition](/singular-value-decomposition/) writes any kernel of rank $r$ as a sum of $r$ separable kernels. The [Gaussian](/gaussian-filter/), the [box](/box-blur/) and the [Sobel](/sobel-operator/) kernels are separable; the disk and the 5-point Laplacian are not.

## In plain words

Some blurs and edge filters can be done in two easy steps in place of one hard step. First go along every row and mix each pixel with its left and right neighbors. Then go along every column of the result and mix each pixel with its upper and lower neighbors. The result is the same as mixing each pixel with its whole square of neighbors at once.

The square of $k$ by $k$ neighbors needs $k$ times $k$ products per pixel. The two steps need only $k$ products each. For a wide blur this is a very large saving. It works only for filters whose square of weights is a row of weights times a column of weights.

## When it applies

The technique applies when the kernel matrix has rank one. Then any nonzero row of it is a multiple of any other row, and one row and one column give the two factors. Rank one can be tested without the SVD: $K$ has rank at most one exactly when every 2 by 2 minor is zero, $K[u][v]\,K[u'][v'] = K[u][v']\,K[u'][v]$ for all $u, u', v, v'$. The two passes equal the direct 2D filter when the border rule is a product of rules on the two axes, $\tilde f(i, j) = f[\mathrm{ext}_y(j)][\mathrm{ext}_x(i)]$, as zero, clamp, mirror and wrap are; the [Gaussian filter](/gaussian-filter/) page proves this. The cut window also factors, because the window that remains is a rectangle and its normalizer is a product of two 1D sums. A kernel of rank $r > 1$ is a sum of $r$ separable kernels, and $r$ pairs of passes cost $\Theta(WHrk)$, which pays when $r < k/2$.

## The template

```pseudo id=main
SEPARABLE-FILTER(f, K, ext)
L1  find (u₀, v₀) with K[u₀][v₀] ≠ 0
L2  b[u] ← K[u][v₀] for all u;  a[v] ← K[u₀][v] / K[u₀][v₀] for all v
L3  if K[u][v] ≠ a[v] · b[u] for some (u, v) then K is not separable; stop
L4  for each row y and each x do  h[y][x] ← Σᵤ b[u] · f̃(x + u, y)
L5  for each column x and each y do  g[y][x] ← Σᵥ a[v] · h̃(x, y + v)
L6  return g
```

Lines L1 to L3 factor the kernel once, before the image is seen. With the pivot $(u_0, v_0)$, the factors give $a[v]\,b[u] = K[u_0][v]\,K[u][v_0] / K[u_0][v_0]$, which equals $K[u][v]$ exactly when the 2 by 2 minor of the rows $u_0, u$ and the columns $v_0, v$ is zero, so line L3 is the rank test. Choosing the entry of largest size as the pivot keeps the division well conditioned in floating point; in exact arithmetic any nonzero entry works. Line L4 is the row pass, which reads the input through the border rule of the $x$ axis. Line L5 is the column pass, which reads the intermediate image $h$ through the border rule of the $y$ axis. The intermediate $h$ must be kept at full precision. The two passes can run in either order.

For a kernel that is not separable, take the SVD $K = \sum_{i=1}^{r} \sigma_i\, c_i\, d_i^{\mathsf T}$ and run lines L4 and L5 once per term, with $b = d_i$ and $a = \sigma_i c_i$, adding the outputs. Keeping only the largest terms gives the best approximation of a given rank in the Frobenius norm.

## Classic examples

- **[Gaussian filter](/gaussian-filter/).** $e^{-(u^2 + v^2)/(2\sigma^2)} = e^{-u^2/(2\sigma^2)}\, e^{-v^2/(2\sigma^2)}$; it is the only rotation invariant kernel that is also separable, among the smooth positive kernels.
- **[Box blur](/box-blur/).** The square of ones is the outer product of two rows of ones, and each 1D pass then runs with running sums, for $\Theta(WH)$ in total.
- **[Sobel operator](/sobel-operator/).** The kernel for the $x$ derivative is $[1, 2, 1]^{\mathsf T}\,[-1, 0, 1]$: smoothing across, differencing along.
- **Laplacian.** The 5-point kernel with rows $(0, 1, 0)$, $(1, -4, 1)$, $(0, 1, 0)$ has rank two. It is the sum of the separable kernels $[0, 1, 0]^{\mathsf T} [1, -2, 1]$ and $[1, -2, 1]^{\mathsf T} [0, 1, 0]$, the second differences along the two axes. The [Laplacian of Gaussian](/laplacian-of-gaussian/) is likewise the sum of two separable kernels.
- **Resampling.** Bilinear, [bicubic](/bicubic-interpolation/) and Lanczos [image resampling](/image-resampling/) use products of 1D weights, and so are done as a row pass and a column pass.
- **The 2D DFT.** The [discrete Fourier transform](/discrete-fourier-transform/) of an image is a 1D transform of every row followed by one of every column, the same idea applied to a transform.

## Variations

- **Low rank sums.** A kernel of rank $r$ from the SVD costs $\Theta(WHrk)$. Truncating the SVD to the first few terms approximates kernels that are not separable, such as a disk for lens blur, with a known error.
- **Repeated 1D passes.** Several box passes along each axis approximate a Gaussian, and each pass costs $\Theta(WH)$, independent of the width.
- **Recursive passes.** An IIR filter along each axis, as in the recursive Gaussian of Deriche or of Young and van Vliet, gives a cost per pixel independent of $\sigma$.
- **Cache order.** The column pass reads memory with a large stride. Transposing the intermediate image, or filtering a block of columns at once, keeps the reads in cache.
- **More dimensions.** A $d$-dimensional kernel that is a product of $d$ factors runs as $d$ passes, for $dk$ in place of $k^d$ operations per sample, as for volumes and video.

## Pitfalls

- **Rounding the intermediate.** Rounding $h$ to 8-bit integers after line L4 adds an error that the column pass spreads, and the result then differs from the direct filter. With $[1, 1]/2$ at the offsets 0 and $+1$ along both axes, under the clamp rule, on the 2 by 2 image with rows $(0, 1)$, $(1, 1)$, rounding $h$ half up gives 1 where the exact value is $3/4$. Keep $h$ in a wider type or in floating point.
- **A border rule that is not a product.** A rule defined in 2D, such as filtering only the pixels inside a mask or a round image region, does not factor, and two plain passes then differ from the 2D result. Filter the masked image and the mask itself with the two passes, and divide, as in normalized convolution.
- **The wrong pivot.** Taking $K[0][0]$ as the pivot at line L1 fails when that entry is 0, as it is for many derivative kernels. Choose a nonzero entry, best the largest one.
- **Testing rank in floating point.** A kernel with rounded weights is almost never exactly rank one. Use the ratio $\sigma_2 / \sigma_1$ of the singular values with a tolerance, and accept the rank one approximation when it is small enough.
- **Mixing up the factors.** Using $a$ for the rows and $b$ for the columns filters with the transposed kernel; for a Sobel kernel this computes the derivative along the other axis.

## Exercises

1. Prove that a nonzero matrix $K$ is an outer product $a\, b^{\mathsf T}$ if and only if it has rank one, and that this holds if and only if every 2 by 2 minor is zero.
2. Show that the two passes of lines L4 and L5 equal the direct 2D filter for every product border rule, and give a 3 by 3 image and a mask rule for which they differ.
3. Factor the Sobel kernel for the $y$ derivative and the binomial kernel $[1, 4, 6, 4, 1]^{\mathsf T} [1, 4, 6, 4, 1] / 256$.
4. Find the rank of the 5-point Laplacian and of the 9-point Laplacian with rows $(1, 1, 1)$, $(1, -8, 1)$, $(1, 1, 1)$, and write each as a sum of separable kernels with as few terms as possible.
5. A $k \times k$ kernel has rank $r$. For which $r$ are the $r$ pairs of passes cheaper than direct filtering? Count the extra memory too.
6. Show that if a continuous kernel $\kappa(x, y) = \alpha(x)\,\beta(y)$ with $\alpha, \beta$ positive and continuous depends only on $x^2 + y^2$, then it is a Gaussian or a constant.

## References
